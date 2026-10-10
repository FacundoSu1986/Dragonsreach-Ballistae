"""Colga escudos vanilla de la baranda del deck parcheando el ESP.

POR QUE NO SE RECONSTRUYE EL PLUGIN
-----------------------------------
build_plugin.py ya no reproduce el ESP instalado. Medido: el navmesh que genera el
codigo tiene 525 vertices y 706 triangulos; el del ESP sellado tiene 403 y 566, y
564 de los 566 triangulos difieren. Regenerar entregaria un plugin distinto del que
esta verificado y empaquetado, asi que aca no se regenera nada.

COMO SE PARCHA
--------------
El ESP es una cabecera TES4 seguida de GRUP de nivel superior. Se desarma en bloques
crudos, se reconstruye SOLO el grupo de contenidos (tipo 9) de la celda 03000807 para
anexar los REFR, y se reensambla el resto byte a byte. El STAT del escudo es un grupo
de nivel superior nuevo.

LA FALSIFICACION
----------------
Con --sin-escudos este script tiene que ser la identidad: el archivo de salida debe
ser identico byte a byte al de entrada. Un parcheador que siempre cambia algo no esta
probando nada. Con escudos, el NVNM del navmesh tiene que seguir identico y el
numero de blocks crecer exactamente lo que dicen los nuevos records.
"""
import argparse
import hashlib
import json
import math
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "vendor"))
import escritor_plugin as W  # noqa: E402
from parser_esm import Plugin  # noqa: E402

U = lambda i: struct.pack("<I", i)
CAB = 24

CELDA = 0x03000807          # AstraAsedioTest
STAT_ESCUDO = 0x030009C0    # por encima de VANILLA_FIRST + 64 = 0x03000980
REFR_BASE = 0x030009C1


# --- estructura de bloques ------------------------------------------------------
def hijos(bloque):
    """[(offset, tamano_total, raw)] de los bloques hijos de un GRUP."""
    out, p, n = [], CAB, len(bloque)
    while p < n:
        if n - p < CAB:
            raise ValueError("cola de %d bytes en un grupo" % (n - p))
        tam, = struct.unpack_from("<I", bloque, p + 4)
        total = tam if bloque[p:p + 4] == b"GRUP" else tam + CAB
        if total <= 0 or p + total > n:
            raise ValueError("bloque en %d con tamano %d no entra en %d" % (p, tam, n))
        out.append((p, total, bloque[p:p + total]))
        p += total
    return out


def etiqueta(grup):
    """(etiqueta u32, tipo i32) de un GRUP serializado."""
    return struct.unpack_from("<Ii", grup, 8)


def rearmar(grup, nuevos_hijos):
    """Reescribe el cuerpo de un GRUP conservando etiqueta, tipo y relleno.

    Solo se reemplazan los bytes 4..7 (groupSize). Los bytes 8..23 son etiqueta,
    tipo de grupo y relleno: hay que conservarlos. Ojo: 'grup[:8] + ... + grup[16:]'
    se come la etiqueta y el tipo, y produce un archivo que el parser no puede leer.
    """
    cuerpo = b"".join(nuevos_hijos)
    # grup[8:24] son etiqueta, tipo de grupo y relleno. Tomar grup[8:] entero arrastraria
    # el CUERPO VIEJO ademas del nuevo y el archivo crecia 24 bytes por nivel de anidaje.
    return grup[:4] + U(len(cuerpo) + CAB) + grup[8:24] + cuerpo


def buscar_y_reemplazar(grup, tipo, etiqueta_objetivo, sustituto):
    """Sustituye, en cualquier profundidad, el primer hijo con ese (tipo, etiqueta)."""
    etiqueta_actual, tipo_actual = etiqueta(grup)
    if tipo_actual == tipo and etiqueta_actual == etiqueta_objetivo:
        return sustituto, True
    out, encontrado = [], False
    for _p, _t, raw in hijos(grup):
        if encontrado or raw[:4] != b"GRUP":
            out.append(raw)
            continue
        nuevo, ok = buscar_y_reemplazar(raw, tipo, etiqueta_objetivo, sustituto)
        out.append(nuevo)
        encontrado = encontrado or ok
    return (rearmar(grup, out) if encontrado else grup), encontrado


def referencia(fid, base, pos, rot, edid):
    ss = [W.sub("EDID", W.zstr(edid)), W.sub("NAME", U(base)),
          W.sub("DATA", struct.pack("<6f", *pos, *rot))]
    return W.record("REFR", fid, ss)


def stat(edid, model, obnd, modt):
    return [W.sub("EDID", W.zstr(edid)), W.sub("OBND", obnd),
            W.sub("MODL", W.zstr(model)), W.sub("MODT", modt),
            W.sub("DNAM", struct.pack("<fI", 90.0, 0))]


def leer_cabecera(d):
    """(maestros, autor, descripcion, esl, inicio_datos)."""
    p = Plugin  # solo para no dejar el import huerfano
    tam0, = struct.unpack_from("<I", d, 4)
    flags, = struct.unpack_from("<I", d, 8)
    inicio = CAB + tam0
    subs = dict(Plugin.subrecords(d[:inicio][CAB:]))
    masters = []
    for k, v in Plugin.subrecords(d[:inicio][CAB:]):
        if k == "MAST":
            masters.append(v.rstrip(b"\0").decode("cp1252"))
    z = lambda b: b.rstrip(b"\0").decode("cp1252") if b else ""
    return masters, z(subs.get("CNAM", b"")), z(subs.get("SNAM", b"")), \
        bool(flags & 0x200), inicio


def navmesh_bytes(ruta):
    """NVNM crudo del navmesh del plugin: tiene que sobrevivir al parche."""
    p = Plugin(ruta)
    for t, o, tam, pr in p.recorrer():
        if t == "NAVM":
            return dict(p.subrecords(p.datos(o)))["NVNM"]
    return None


def _contar(bloque):
    """records + GRUP de una secuencia, en todos los niveles (lo que pide HEDR).

    Falsificado: contar solo los GRUP de nivel superior daba 12 donde el archivo tiene
    126. El HEDR de un plugin de Bethesda cuenta todos los blocks, anidados.
    """
    total, p, n = 0, 0, len(bloque)
    while p < n:
        if n - p < CAB:
            raise ValueError("cola de %d bytes sin encabezado completo" % (n - p))
        tam, = struct.unpack_from("<I", bloque, p + 4)
        if bloque[p:p + 4] == b"GRUP":
            if tam < CAB or p + tam > n:
                raise ValueError("GRUP en %d con tamano %d no entra en %d" % (p, tam, n))
            total += 1 + _contar(bloque[p + CAB:p + tam])
            p += tam
        else:
            if p + CAB + tam > n:
                raise ValueError("record en %d declara %d bytes y no entra en %d" % (p, tam, n))
            total += 1
            p += CAB + tam
    return total


def bloques_totales(d, inicio):
    return _contar(d[inicio:])


def escribir_conservando_cabecera(original, grupos, destino, inicio):
    """Escribe cabecera + grupos reusando la cabecera original byte a byte.

    No se vuelve a llamar a W.escribir: esa rehace el TES4 y en particular recalcula
    `siguiente_id`, que en el archivo original vale 0x...80 y salia en 0 (falsificado
    con --sin-escudos: primer byte distinto en el 38). Lo unico que DEBE cambiar es el
    conteo de bloques de HEDR, porque se agregan records.
    """
    cabecera = bytearray(original[:inicio])
    total = bloques_totales(b"".join(grupos), 0)
    p, n, parcheado = CAB, len(cabecera), None
    while p + 6 <= n:
        tipo = bytes(cabecera[p:p + 4])
        tam, = struct.unpack_from("<H", cabecera, p + 4)
        if tipo == b"HEDR":
            parcheado = p + 6
            break
        p += 6 + tam
    if parcheado is None:
        raise ValueError("la cabecera no tiene HEDR")
    struct.pack_into("<i", cabecera, parcheado + 4, total)
    with open(destino, "wb") as fh:
        fh.write(bytes(cabecera))
        for g in grupos:
            fh.write(g)
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sin-escudos", action="store_true",
                    help="no agrega nada: debe reproducir el archivo byte a byte")
    ap.add_argument("--salida", default=str(ROOT / "mod" / "AstraAsedio.esp"))
    args = ap.parse_args()

    origen = ROOT / "mod" / "AstraAsedio.esp"
    original = origen.read_bytes()
    nv_original = navmesh_bytes(str(origen))
    bloques_originales = bloques_totales(original, leer_cabecera(original)[4])
    print("ESP de entrada: %d B, %d bloques" % (len(original), bloques_originales))

    masters, autor, desc, esl, inicio = leer_cabecera(original)
    print("  maestros=%s  autor=%r  esl=%s" % (masters, autor, esl))

    if args.sin_escudos:
        grupos = []
        p = inicio
        while p < len(original):
            tam, = struct.unpack_from("<I", original, p + 4)
            grupos.append(original[p:p + (tam if original[p:p + 4] == b"GRUP" else tam + CAB)])
            p += (tam if original[p:p + 4] == b"GRUP" else tam + CAB)
        escribir_conservando_cabecera(original, grupos, args.salida, inicio)
        salida = Path(args.salida).read_bytes()
        igual = salida == original
        print("\n--sin-escudos: salida identica = %s  (%d B)" % (igual, len(salida)))
        if not igual:
            for i, (a, b) in enumerate(zip(original, salida)):
                if a != b:
                    print("  primer byte distinto en %d: %02X vs %02X" % (i, a, b))
                    break
            raise SystemExit("el parcheador tiene que ser la identidad y no lo es")
        print("FALSIFICACION OK: sin escudos no cambia ni un byte")
        return

    # --- datos del escudo, leidos de los archivos de la auditoria -------------
    esc = json.loads((ROOT / "auditoria" / "escudos_vanilla.json").read_text(encoding="utf-8"))
    cfg = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    bloque = cfg["tower_v11"]["escudos"]
    eb = esc[bloque["edid"]]
    modt = bytes.fromhex(eb["mo2t"])
    obnd = bytes.fromhex(eb["obnd"])
    print("escudo: %s (%s)  malla=%s  MO2T=%d B" % (bloque["edid"], eb["form_id"], eb["mod2"], len(modt)))

    # --- el STAT del escudo, clonando un STAT vanilla limpio -------------------
    esm = Plugin(str(Path(cfg["runtime"]) / "Data" / "Skyrim.esm"))
    donante = None
    for t, o, tam, pr in esm.recorrer():
        if t != "STAT":
            continue
        sd = dict(esm.subrecords(esm.datos(o)))
        if sd.get("EDID", b"").rstrip(b"\0") == bloque["donor_stat"].encode():
            donante = esm.form_id(o)
            break
    if donante is None:
        raise SystemExit("no encontre el STAT donante %s" % bloque["donor_stat"])
    print("  STAT donante %s = %08X" % (bloque["donor_stat"], donante))

    nuevo_stat = W.record("STAT", STAT_ESCUDO, stat("AstraEscudoBaranda", eb["mod2"], obnd, modt))
    grupo_stat = W.grupo("STAT", [nuevo_stat])

    # --- desarmar, parchear el grupo de contenidos, reensamblar ----------------
    grupos, p = [], inicio
    while p < len(original):
        tam, = struct.unpack_from("<I", original, p + 4)
        grupos.append(original[p:p + (tam if original[p:p + 4] == b"GRUP" else tam + CAB)])
        p += (tam if original[p:p + 4] == b"GRUP" else tam + CAB)

    nuevos_refs = []
    for i, item in enumerate(bloque["items"]):
        rot = tuple(math.radians(a) for a in item["rot_deg"])
        nuevos_refs.append(referencia(REFR_BASE + i, STAT_ESCUDO, item["pos"], rot,
                                     "AstraEscudo" + item["nombre"]))
    contenido = b"".join(nuevos_refs)

    parcheado = False
    salida_grupos = []
    for g in grupos:
        if g[:4] == b"GRUP" and g[8:12] == b"CELL":
            g2, ok = _contenido(g, CELDA, contenido)
            parcheado = parcheado or ok
            salida_grupos.append(g2)
        else:
            salida_grupos.append(g)
    if not parcheado:
        raise SystemExit("no encontre el grupo de contenidos (tipo 9) de la celda %08X" % CELDA)
    salida_grupos.append(grupo_stat)

    nuevos_ids = [STAT_ESCUDO] + [REFR_BASE + i for i in range(len(nuevos_refs))]
    escribir_conservando_cabecera(original, salida_grupos, args.salida, inicio)

    # --- verificacion ----------------------------------------------------------
    salida = Path(args.salida)
    print("\nescrito %s: %d B" % (salida.name, salida.stat().st_size))
    print("  FormIDs nuevos: %s" % ", ".join("%08X" % f for f in nuevos_ids))
    nv_nuevo = navmesh_bytes(str(salida))
    print("navmesh NVNM identico: %s  (%d B)" % (nv_original == nv_nuevo, len(nv_nuevo or b"")))
    if nv_original != nv_nuevo:
        raise SystemExit("EL NAVMESH CAMBIO: el parche esta roto")
    nuevos_bloques = bloques_totales(salida.read_bytes(), inicio)
    delta = nuevos_bloques - bloques_originales
    esperado = 2 + len(nuevos_refs)   # 1 GRUP + 1 STAT + N REFR
    print("bloques: %d -> %d (delta %d, esperado %d)" %
          (bloques_originales, nuevos_bloques, delta, esperado))
    if delta != esperado:
        raise SystemExit("el delta de bloques no es el esperado")

    p = Plugin(str(salida))
    recs = {}
    for t, o, tam, pr in p.recorrer():
        if t in ("REFR", "STAT"):
            recs[p.form_id(o)] = (t, dict(p.subrecords(p.datos(o))))
    print("records REFR+STAT tras el parche: %d" % len(recs))
    if STAT_ESCUDO not in recs or recs[STAT_ESCUDO][0] != "STAT":
        raise SystemExit("el STAT del escudo no quedo escrito")
    print("  STAT %08X MODL=%s" % (STAT_ESCUDO,
                                   recs[STAT_ESCUDO][1]["MODL"].rstrip(b"\0").decode()))
    for i, item in enumerate(bloque["items"]):
        fid = REFR_BASE + i
        if fid not in recs or recs[fid][0] != "REFR":
            raise SystemExit("falta el REFR %08X" % fid)
        ss = recs[fid][1]
        base, = struct.unpack("<I", ss["NAME"])
        pos = struct.unpack_from("<3f", ss["DATA"], 0)
        if base != STAT_ESCUDO:
            raise SystemExit("el REFR %08X no apunta al STAT del escudo" % fid)
        print("  REFR %08X -> %08X  pos=(%.1f, %.1f, %.1f)  %s"
              % (fid, base, pos[0], pos[1], pos[2],
                 ss["EDID"].rstrip(b"\0").decode()))
    print("\nPASTE OK: navmesh intacto, %d escudos colocados" % len(nuevos_refs))


def _contenido(g, celda, extra):
    """El GRUP tipo 9 de la celda, con `extra` anexado. Devuelve (bytes, encontrado).

    La jerarquia es GRUP Cell -> bloque(2) -> sub-bloque(3) -> celda(6) -> contenidos(9),
    asi que hay que bajar cuatro niveles: mirar solo los hijos directos no lo encuentra.
    """
    lab, tipo = etiqueta(g)
    if tipo == 9 and lab == celda:
        return rearmar(g, [h[2] for h in hijos(g)] + [extra]), True
    out, ok = [], False
    for _p, _t, raw in hijos(g):
        if ok or raw[:4] != b"GRUP":
            out.append(raw)
            continue
        nuevo, enc = _contenido(raw, celda, extra)
        out.append(nuevo)
        ok = ok or enc
    return (rearmar(g, out) if ok else g), ok


if __name__ == "__main__":
    main()
