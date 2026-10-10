# -*- coding: utf-8 -*-
"""Coloca la torre en el mundo como OVERRIDE de la celda vanilla, dentro de AstraAsedio.esp.

POR QUE ESTE SCRIPT REEMPLAZA A parchear_mundo.py
-------------------------------------------------
parchear_mundo.py metia una celda NUEVA dentro de Skyrim.esm. Tenia cuatro defectos,
medidos (no supuestos):

  1. Los REFR propios llevaban NAME 03xxxxxx. Skyrim.esm no tiene ningun master (su
     TES4 no trae MAST), y un byte alto >= cantidad de masters significa "este mismo
     archivo": 03000800 se leeria como 00000800 de Skyrim.esm, no como la torre.
  2. La celda 00F00001 repetia el grid (1,-4) de la vanilla 0000963D. En Skyrim.esm hay
     16.978 celdas exteriores y ningun grid tiene dos (salvo la celda persistente
     (0,0) de cada mundo).
  3. DATA del REFR son 3 float de posicion + 3 float de rotacion en RADIANES; el
     parche los escribia como u16 y leia como u16 los del ESP: rotaciones basura.
  4. Obligaba a sustituir Skyrim.esm (249,7 MB), contra THIRD_PARTY_POLICY.md.

Un plugin SI puede sobrescribir una celda exterior con sus hijos: Update.esm de
Bethesda sobrescribe 2.296 celdas y 1.737 LAND de Tamriel asi. Este script escribe la
misma estructura que Update.esm:

    GRUP WRLD > WRLD 0000003C > GRUP tipo1 (3C) > tipo4 > tipo5 >
        CELL 0000963D + GRUP tipo6 > GRUP tipo9 { LAND + REFR... }

QUE ESCRIBE
-----------
  - WRLD: la version ganadora entre los masters del plugin (Dawnguard.esm) SIN OFST ni
    RNAM, que es lo que guarda el CK (medido en NordicMonument.esp, HappyLittleTrees.esp
    y Skyrim Unbound.esp). No revierte nada de los DLC: los campos son iguales. Con una
    excepcion: FULL (el nombre) se escribe como texto "Skyrim", porque en los masters es
    un ID de string localizado y este plugin no es localizado. Lo encontro SSEEdit.
  - CELL 0000963D y su LAND 0000A63D: la version ganadora es la de Update.esm (el LAND
    de Update.esm cambia VNML y texturas respecto de Skyrim.esm; copiar la de
    Skyrim.esm las revertiria). Registros en version 44, sin comprimir, como el CK.
  - El LAND lleva la plataforma de terreno de nivelar_terreno.py.
  - REFR: los de la celda de prueba, menos las luces de relleno, los blancos de tiro, el
    marcador y las 18 losas de piso (son del laboratorio interior). Mismos NAME/XSCL/DATA,
    llevados al mundo con mundo_v11.llevar. La ballesta pierde la bandera "persistente":
    en Tamriel solo 1 de ~15 mil celdas con grid tiene hijos persistentes, el resto va a la
    celda persistente del mundo. DATA son 6 float: posicion y rotacion en radianes.
  - REFR vanilla de la celda cuyo suelo se movio mas de 15 u (hoy una pila de rocas y tres
    arbustos): override del REFR ganador con la Z corrida el mismo cambio.

HIGIENE
-------
  - Fusiona el segundo GRUP STAT de nivel superior (el de los escudos, agregado al final)
    con el primero.
  - nextObjectID del HEDR (valia 0x980 con FormIDs hasta 0x9C5) pasa a max+1.

FALSIFICACION
-------------
--sin-mundo no cambia nada y tiene que reproducir el archivo byte a byte; aborta si no.
El script se puede repetir: quita el WRLD que ya escribio antes de volver a escribirlo.
"""
import argparse
import hashlib
import json
import math
import shutil
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "vendor"))
import escritor_plugin as W  # noqa: E402
import mundo_v11 as M  # noqa: E402
import nivelar_terreno as T  # noqa: E402
from parser_esm import Plugin  # noqa: E402

CAB = 24
U = lambda i: struct.pack("<I", i)

CELDA_PRUEBA = 0x03000807          # AstraAsedioTest
CELDA_MUNDO = 0x0000963D           # WhiterunWatchtowerExterior02, grid (1,-4)
WRLD_TAMRIEL = 0x0000003C
PRIMER_REFR = 0x03000A00           # por encima de todo FormID propio existente
COMPRIMIDO = 0x00040000
PERSISTENTE = 0x00000400
MASTERS_ORDEN = ("Skyrim.esm", "Update.esm", "Dawnguard.esm")     # orden de carga

# lo que NO viaja al mundo: es del laboratorio interior. WRIntFloorSTMid01Large son las 18
# losas de piso del laboratorio (x -1536..1536, y -2324..1024: build_plugin.py las genera
# para que el interior tenga suelo y para los blancos). parchear_mundo.py las copiaba:
# 18 losas flotando sobre la tundra.
VANILLA_EXCLUIDOS = ("ArcheryTarget", "ArcheryTargetTripod", "XMarkerHeading",
                     "WRIntFloorSTMid01Large")
ESPERADOS = 72                     # torre + ballesta + cofre + 64 piezas + 5 escudos
UMBRAL_OBJETO = 15.0               # u de cambio de suelo desde el cual se corrige un objeto
NOMBRE_MUNDO = "Skyrim"            # nombre visible de Tamriel (el que escribe HappyLittleTrees.esp)
CAMPOS_DE_TEXTO = ("FULL", "DESC", "SHRT", "NAM1")   # strings localizables en un master localizado


class ErrorMundo(Exception):
    pass


# --- bloques crudos -------------------------------------------------------------

def hijos(bloque):
    """[(offset, total, raw)] de los hijos de un GRUP serializado (incluye su cabecera)."""
    out, p, n = [], CAB, len(bloque)
    while p < n:
        if n - p < CAB:
            raise ErrorMundo("cola de %d bytes en un grupo" % (n - p))
        tam, = struct.unpack_from("<I", bloque, p + 4)
        total = tam if bloque[p:p + 4] == b"GRUP" else tam + CAB
        if total <= 0 or p + total > n:
            raise ErrorMundo("bloque en %d con tamano %d no entra en %d" % (p, tam, n))
        out.append((p, total, bloque[p:p + total]))
        p += total
    return out


def grup(label, tipo, cuerpo):
    """GRUP con etiqueta u32 (los tipos 1,4,5,6,9 la llevan; el 0 usa 4 letras)."""
    if isinstance(label, str):
        label = label.encode("ascii")
    else:
        label = struct.pack("<I", label)
    return (b"GRUP" + struct.pack("<I", len(cuerpo) + CAB) + label
            + struct.pack("<i", tipo) + b"\0" * 8 + cuerpo)


def etiqueta4(bloque):
    return bloque[8:12]


def reemplazar_cuerpo(bloque, nuevo_cuerpo):
    return bloque[:4] + struct.pack("<I", len(nuevo_cuerpo) + CAB) + bloque[8:CAB] + nuevo_cuerpo


def contar(bloque):
    """records + GRUP de una secuencia de bloques, en todos los niveles (lo que pide HEDR)."""
    total, p, n = 0, 0, len(bloque)
    while p < n:
        tam, = struct.unpack_from("<I", bloque, p + 4)
        if bloque[p:p + 4] == b"GRUP":
            total += 1 + contar(bloque[p + CAB:p + tam])
            p += tam
        else:
            total += 1
            p += CAB + tam
    return total


def desarmar(d, inicio):
    """Bloques de nivel superior del ESP tras el TES4."""
    out, p = [], inicio
    while p < len(d):
        tam, = struct.unpack_from("<I", d, p + 4)
        paso = tam if d[p:p + 4] == b"GRUP" else tam + CAB
        out.append(d[p:p + paso])
        p += paso
    return out


# --- lectura de masters ---------------------------------------------------------

def ruta_master(nombre):
    cfg = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    return Path(cfg["runtime"]) / "Data" / nombre


def cadena_de_grupos(p, form_celda):
    """[(tipo, etiqueta u32)] de los GRUP que contienen al CELL, de afuera hacia adentro."""
    pila = []
    for t, o, tam, pr in p.recorrer():
        if t == "GRUP":
            gt, = struct.unpack_from("<i", p.d, o + 12)
            lab, = struct.unpack_from("<I", p.d, o + 8)
            pila[pr:] = [(gt, lab)]
        elif t == "CELL" and p.form_id(o) == form_celda:
            return list(pila[:pr])
    return None


def version_ganadora(tipo, form_id, celda_padre=None):
    """(master, flags, [(clave, bytes)]) de la ultima version del record entre los masters
    del plugin, en orden de carga. `celda_padre` filtra LAND por la celda que lo contiene."""
    ganadora = None
    for nombre in MASTERS_ORDEN:
        p = Plugin(str(ruta_master(nombre)))
        cur = None
        for t, o, tam, pr in p.recorrer():
            if t == "CELL":
                cur = p.form_id(o)
            if t != tipo:
                continue
            if tipo == "LAND":
                if cur != celda_padre:
                    continue
            elif p.form_id(o) != form_id:
                continue
            flags, = struct.unpack_from("<I", p.d, o + 8)
            ganadora = (nombre, flags, list(Plugin.subrecords(p.datos(o))),
                        p.form_id(o))
    if ganadora is None:
        raise ErrorMundo("no encontre %s %08X en %s" % (tipo, form_id, MASTERS_ORDEN))
    return ganadora


def refrs_de_celda(celda):
    """{form_id: (master, flags, [(clave, bytes)])} de los REFR de la celda, con la version
    ganadora entre los masters del plugin (un pase por master)."""
    out = {}
    for nombre in MASTERS_ORDEN:
        p = Plugin(str(ruta_master(nombre)))
        cur = None
        for t, o, tam, pr in p.recorrer():
            if t == "CELL":
                cur = p.form_id(o)
            elif t == "REFR" and cur == celda:
                flags, = struct.unpack_from("<I", p.d, o + 8)
                out[p.form_id(o)] = (nombre, flags, list(Plugin.subrecords(p.datos(o))))
    return out


def record_override(tipo, form_id, flags, subs):
    """Record en version 44, sin comprimir, como lo guarda el CK."""
    return W.record(tipo, form_id, [W.sub(k, v) for k, v in subs],
                    banderas=flags & ~COMPRIMIDO, version=44)


# --- REFR de la celda de prueba ---------------------------------------------------

def refrs_de_prueba(p):
    """[(form_id, flags, [(clave, bytes)])] de los REFR de la celda de prueba."""
    salida = []
    cur = None
    for t, o, tam, pr in p.recorrer():
        if t == "CELL":
            cur = p.form_id(o)
        elif t == "REFR" and cur == CELDA_PRUEBA:
            flags, = struct.unpack_from("<I", p.d, o + 8)
            salida.append((p.form_id(o), flags, list(Plugin.subrecords(p.datos(o)))))
    return salida


def bases_excluidas(p):
    """FormIDs base que no viajan: las luces propias y los vanilla de laboratorio."""
    ex = set()
    for t, o, tam, pr in p.recorrer():
        if t == "LIGH":
            ex.add(p.form_id(o))
    skyrim = Plugin(str(ruta_master("Skyrim.esm")))
    for t, o, tam, pr in skyrim.recorrer():
        if t == "STAT":
            ss = dict(Plugin.subrecords(skyrim.datos(o)))
            if ss.get("EDID", b"").rstrip(b"\0").decode("cp1252", "replace") in VANILLA_EXCLUIDOS:
                ex.add(skyrim.form_id(o))
    return ex


def llevar_refr(subs, flags, mundo, nuevo_id):
    """Un REFR de la celda de prueba, ya en coordenadas de mundo y con FormID nuevo."""
    d = dict(subs)
    data = d["DATA"]
    if len(data) != 24:
        raise ErrorMundo("DATA de %d bytes, un REFR lleva 24" % len(data))
    x, y, z, rx, ry, rz = struct.unpack("<6f", data)
    escala = struct.unpack("<f", d["XSCL"])[0] if "XSCL" in d else 1.0
    pieza = {"pos": (x, y, z), "rot_deg": tuple(math.degrees(a) for a in (rx, ry, rz)),
             "scale": escala}
    pos, rot = M.llevar(pieza, mundo)
    nuevos = []
    for k, v in subs:
        if k == "EDID":
            e = v.rstrip(b"\0").decode("cp1252")
            e = e[:-3] + "MundoREF" if e.endswith("REF") else e + "Mundo"
            nuevos.append((k, W.zstr(e)))
        elif k == "DATA":
            nuevos.append((k, struct.pack("<6f", *pos, *(math.radians(a) for a in rot))))
        else:
            nuevos.append((k, v))
    return W.record("REFR", nuevo_id, [W.sub(k, v) for k, v in nuevos],
                    banderas=flags & ~PERSISTENTE, version=44), pos


# --- el armado ------------------------------------------------------------------

def construir_grupo_mundo(p_esp, mundo, pilotes):
    """(bloque GRUP WRLD, informe)."""
    # 1. cadena de GRUP de la celda vanilla y comprobacion contra Update.esm
    skyrim = Plugin(str(ruta_master("Skyrim.esm")))
    cadena = cadena_de_grupos(skyrim, CELDA_MUNDO)
    cadena_up = cadena_de_grupos(Plugin(str(ruta_master("Update.esm"))), CELDA_MUNDO)
    if cadena is None or cadena != cadena_up:
        raise ErrorMundo("la cadena de GRUP de %08X no coincide entre Skyrim.esm y "
                         "Update.esm: %s vs %s" % (CELDA_MUNDO, cadena, cadena_up))
    tipos = [g[0] for g in cadena]
    if tipos != [0, 1, 4, 5] or cadena[1][1] != WRLD_TAMRIEL:
        raise ErrorMundo("cadena inesperada %s" % cadena)
    etiqueta_t4, etiqueta_t5 = cadena[2][1], cadena[3][1]

    # 2. versiones ganadoras
    _m, fl_w, subs_w, _f = version_ganadora("WRLD", WRLD_TAMRIEL)
    # FULL de los masters es un ID de la tabla de strings (4 bytes) porque Skyrim.esm es
    # LOCALIZADO; este plugin no lo es, asi que ahi FULL tiene que ser el texto. Copiarlo
    # tal cual daba el nombre basura "æ " (SSEEdit: "Unused data in ... FULL - Name").
    subs_w = [(k, W.zstr(NOMBRE_MUNDO) if k == "FULL" else v)
              for k, v in subs_w if k not in ("OFST", "RNAM")]
    m_c, fl_c, subs_c, _f = version_ganadora("CELL", CELDA_MUNDO)
    m_l, fl_l, subs_l, id_land = version_ganadora("LAND", None, CELDA_MUNDO)
    for tipo, subs in (("WRLD", subs_w), ("CELL", subs_c), ("LAND", subs_l)):
        for k, v in subs:
            if k in CAMPOS_DE_TEXTO and not (v.endswith(b"\0") and b"\0" not in v[:-1]):
                raise ErrorMundo("%s copia %s como ID de string localizado (%r): el plugin "
                                 "no es localizado, hay que escribir el texto" % (tipo, k, v))

    # 3. terreno
    sub_land = dict(subs_l)
    nuevo, inf_t = T.aplicar_a_land(sub_land, mundo)
    subs_l2 = [(k, nuevo[k] if k in ("VHGT", "VNML") else v) for k, v in subs_l]
    off0, h0 = T.decodificar_vhgt(sub_land["VHGT"])
    off1, h1 = T.decodificar_vhgt(nuevo["VHGT"])
    inf_t["antes"] = T.medir(h0, mundo, pilotes)
    inf_t["despues"] = T.medir(h1, mundo, pilotes)

    # objetos vanilla de la celda cuyo suelo se movio: un override de su Z por el mismo
    # cambio, para que un arbol o una roca no queden 40 u enterrados ni 20 u en el aire
    movidos, overrides_refr = [], []
    for fid, (maestro, fl_r, subs_r) in refrs_de_celda(CELDA_MUNDO).items():
        dd = dict(subs_r).get("DATA", b"")
        if len(dd) < 24 or fl_r & PERSISTENTE:
            continue
        x, y, z = struct.unpack_from("<3f", dd, 0)
        dz = T.interpolar(h1, x, y) - T.interpolar(h0, x, y)
        if abs(dz) <= UMBRAL_OBJETO:
            continue
        dz = round(dz, 1)
        nuevos = [(k, dd[:8] + struct.pack("<f", z + dz) + dd[12:] if k == "DATA" else v)
                  for k, v in subs_r]
        overrides_refr.append(record_override("REFR", fid, fl_r, nuevos))
        movidos.append({"form_id": "%08X" % fid, "version": maestro,
                        "base": "%08X" % struct.unpack("<I", dict(subs_r)["NAME"])[0],
                        "pos": [round(x, 1), round(y, 1), round(z, 1)],
                        "cambio_suelo": dz, "z_nuevo": round(z + dz, 1)})
    inf_t["objetos_vanilla_con_suelo_movido"] = movidos

    # 4. REFR
    excl = bases_excluidas(p_esp)
    refs, lista, mundo_pos = [], [], []
    for fid, flags, subs in refrs_de_prueba(p_esp):
        base, = struct.unpack("<I", dict(subs)["NAME"])
        if base in excl:
            continue
        lista.append((fid, flags, subs, base))
    if len(lista) != ESPERADOS:
        raise ErrorMundo("%d REFR viajan al mundo y se esperaban %d" % (len(lista), ESPERADOS))
    for i, (fid, flags, subs, base) in enumerate(lista):
        rec, pos = llevar_refr(subs, flags, mundo, PRIMER_REFR + i)
        refs.append(rec)
        mundo_pos.append({"origen": "%08X" % fid, "nuevo": "%08X" % (PRIMER_REFR + i),
                          "base": "%08X" % base, "pos": [round(a, 3) for a in pos]})

    # 5. ensamblado
    rec_land = record_override("LAND", id_land, fl_l, subs_l2)
    rec_cell = record_override("CELL", CELDA_MUNDO, fl_c, subs_c)
    rec_wrld = record_override("WRLD", WRLD_TAMRIEL, fl_w, subs_w)
    g9 = grup(CELDA_MUNDO, 9, rec_land + b"".join(overrides_refr) + b"".join(refs))
    g6 = grup(CELDA_MUNDO, 6, g9)
    g5 = grup(etiqueta_t5, 5, rec_cell + g6)
    g4 = grup(etiqueta_t4, 4, g5)
    g1 = grup(WRLD_TAMRIEL, 1, g4)
    bloque = grup("WRLD", 0, rec_wrld + g1)
    informe = {"celda": "%08X" % CELDA_MUNDO, "land": "%08X" % id_land,
               "version_ganadora": {"WRLD": MASTERS_ORDEN[-1], "CELL": m_c, "LAND": m_l},
               "etiquetas": {"tipo4": "%08X" % etiqueta_t4, "tipo5": "%08X" % etiqueta_t5},
               "refr": len(refs), "primer_refr": "%08X" % PRIMER_REFR,
               "terreno": inf_t, "refr_en_mundo": mundo_pos}
    return bloque, informe


def fusionar_stat(bloques):
    """Un solo GRUP STAT de nivel superior: el segundo se anexa al primero."""
    idx = [i for i, b in enumerate(bloques) if b[:4] == b"GRUP" and etiqueta4(b) == b"STAT"]
    if len(idx) <= 1:
        return bloques, False
    primero = bloques[idx[0]]
    cuerpo = primero[CAB:]
    for j in idx[1:]:
        cuerpo += bloques[j][CAB:]
    salida = []
    for i, b in enumerate(bloques):
        if i == idx[0]:
            salida.append(reemplazar_cuerpo(primero, cuerpo))
        elif i in idx[1:]:
            continue
        else:
            salida.append(b)
    return salida, True


def quitar_mundo_previo(bloques):
    return [b for b in bloques if not (b[:4] == b"GRUP" and etiqueta4(b) == b"WRLD")]


def insertar_despues_de_cell(bloques, nuevo):
    for i, b in enumerate(bloques):
        if b[:4] == b"GRUP" and etiqueta4(b) == b"CELL":
            return bloques[:i + 1] + [nuevo] + bloques[i + 1:]
    raise ErrorMundo("el ESP no tiene GRUP CELL")


def ids_propios(bloques):
    """FormIDs de todos los records (no GRUP) de los bloques."""
    ids = []

    def rec(b):
        p = 0
        while p < len(b):
            tam, = struct.unpack_from("<I", b, p + 4)
            if b[p:p + 4] == b"GRUP":
                rec(b[p + CAB:p + tam])
                p += tam
            else:
                ids.append(struct.unpack_from("<I", b, p + 12)[0])
                p += CAB + tam
    for b in bloques:
        rec(b)
    return ids


def escribir(original, inicio, bloques, destino, siguiente_id=None):
    """Cabecera original byte a byte; solo HEDR (numRecords y, si se pide, nextObjectID)."""
    cab = bytearray(original[:inicio])
    total = sum(contar(b) for b in bloques)
    p = CAB
    while p + 6 <= len(cab):
        tipo = bytes(cab[p:p + 4])
        tam, = struct.unpack_from("<H", cab, p + 4)
        if tipo == b"HEDR":
            struct.pack_into("<i", cab, p + 6 + 4, total)
            if siguiente_id is not None:
                struct.pack_into("<I", cab, p + 6 + 8, siguiente_id)
            break
        p += 6 + tam
    else:
        raise ErrorMundo("la cabecera no tiene HEDR")
    Path(destino).write_bytes(bytes(cab) + b"".join(bloques))
    return total


def leer_pilotes():
    tw = json.loads((ROOT / "reports" / "v11_tower.json").read_text(encoding="utf-8"))
    out = []
    for r in tw["stilts"]["rows"]:
        a = r["name"].split("_")
        out.append((float(a[1]), float(a[2]), r["bottom_z"]))
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", default=str(ROOT / "mod" / "AstraAsedio.esp"))
    ap.add_argument("--salida", default=str(ROOT / "mod" / "AstraAsedio.esp"))
    ap.add_argument("--informe", default=str(ROOT / "reports" / "mundo_esp_v11.json"))
    ap.add_argument("--sin-mundo", action="store_true",
                    help="no cambia nada: debe reproducir el archivo byte a byte")
    a = ap.parse_args()

    original = Path(a.entrada).read_bytes()
    tam0, = struct.unpack_from("<I", original, 4)
    inicio = CAB + tam0
    bloques = desarmar(original, inicio)
    print("ESP de entrada: %d B, %d bloques de nivel superior" % (len(original), len(bloques)))

    if a.sin_mundo:
        tmp = Path(a.salida).with_suffix(".identidad.tmp")
        escribir(original, inicio, bloques, tmp)
        salida = tmp.read_bytes()
        tmp.unlink()
        if salida != original:
            for i, (x, y) in enumerate(zip(original, salida)):
                if x != y:
                    print("primer byte distinto en %d: %02X vs %02X" % (i, x, y))
                    break
            raise SystemExit("el armador tiene que ser la identidad y no lo es")
        print("FALSIFICACION OK: --sin-mundo reproduce el archivo (%d B)" % len(salida))
        return 0

    mundo = dict(M.cargar_colocacion())
    p_esp = Plugin(a.entrada)
    hubo_mundo = any(b[:4] == b"GRUP" and etiqueta4(b) == b"WRLD" for b in bloques)
    if not hubo_mundo:
        respaldo = ROOT / "auditoria" / "AstraAsedio.esp.antes_de_mundo"
        if not respaldo.exists():
            shutil.copyfile(a.entrada, respaldo)
            print("respaldo del ESP original: %s" % respaldo.name)
    bloques = quitar_mundo_previo(bloques)
    # el WRLD previo no afecta a los REFR de prueba, que siguen en la celda interior
    nuevo, informe = construir_grupo_mundo(p_esp, mundo, leer_pilotes())
    bloques, fusionado = fusionar_stat(bloques)
    bloques = insertar_despues_de_cell(bloques, nuevo)
    ids = [f & 0xFFFFFF for f in ids_propios(bloques) if (f >> 24) == 3]
    siguiente = max(ids) + 1
    total = escribir(original, inicio, bloques, a.salida, siguiente)
    informe["grupos_stat_fusionados"] = fusionado
    informe["next_object_id"] = "%08X" % siguiente
    informe["bloques"] = total
    informe["bytes"] = Path(a.salida).stat().st_size
    informe["sha256"] = hashlib.sha256(Path(a.salida).read_bytes()).hexdigest()
    Path(a.informe).write_text(json.dumps(informe, indent=1, ensure_ascii=False), encoding="utf-8")

    t = informe["terreno"]
    print("\nescrito %s: %d B, %d bloques" % (Path(a.salida).name, informe["bytes"], total))
    print("  %d REFR al mundo desde %s; STAT fusionados: %s; nextObjectID %08X"
          % (informe["refr"], informe["primer_refr"], fusionado, siguiente))
    print("  terreno: plataforma Z %.0f, %d vertices planos, anillos %s, cambio max %.0f u"
          % (t["z_plataforma"], t["vertices_planos"], t["vertices_anillo"], t["cambio_max"]))
    print("  antes  : %s" % t["antes"])
    print("  despues: %s" % t["despues"])
    print("  objetos vanilla con suelo movido >15 u: %d" % len(t["objetos_vanilla_con_suelo_movido"]))
    for o in t["objetos_vanilla_con_suelo_movido"]:
        print("     %(form_id)s pos=%(pos)s  suelo %(cambio_suelo)+.1f u" % o)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
