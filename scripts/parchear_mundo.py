# -*- coding: utf-8 -*-
"""OBSOLETO (2026-10-07): usar scripts/colocar_en_mundo.py. No instalar el esm que genera.

Este camino tiene cuatro defectos medidos: los REFR propios llevan NAME 03xxxxxx dentro de
un archivo sin masters (se leerian como 00xxxxxx de Skyrim.esm); la celda nueva repite el
grid (1,-4) de la vanilla 0000963D; DATA del REFR se escribe como u16 cuando son 6 float en
radianes; copia las 18 losas del laboratorio interior; y obliga a sustituir Skyrim.esm. Se
conserva porque auditoria/verificar_parche.py lo importa y como registro.

Parchea Skyrim.esm para anadir una SUBCELDA con la torre de asedio, en el punto
del mundo que pidio el usuario.

POR QUE HAY QUE TOCAR Skyrim.esm Y NO BASTA UN ESP
--------------------------------------------------
Medido en 249.753.412 bytes de Skyrim.esm (no de memoria ni de otra version):

  1. No hay NI UN record XXXX. El 'chunk = record XXXX' es de Skyrim LE.
     La jerarquia real de una celda EXTERIOR es:
         GRUP 'WRLD' > tipo=1 > tipo=4 > tipo=5 > CELL
     y las interiores son GRUP 'CELL' > tipo=2 > tipo=3 > CELL. Por eso
     WhiterunWatchtowerExterior02 no aparecia buscando en el GRUP 'CELL'.

  2. El GRUP tipo=5 NO es un chunk. El control que lo decide recorre los 793
     tipo=5 de Tamriel y cuenta cuantos grids distintos (XCLC) hay dentro:
     208 tienen VARIOS, ninguno tiene UNO. El tipo=5 agrupa 8x8 chunks y su
     label los codifica: label = (X_bloque << 16) | (Y_bloque & 0xFFFF), con
     X_chunk en 8*X_bloque + i e Y_chunk en 8*Y_bloque + j, i,j en 0..7.
     Comprobado con label 0x0000FFFF -> X 0..7, Y -8..-1, que es donde cae
     el chunk (1,-4).

  3. El grid de una celda esta en su subrecord XCLC, con el layout
     [i32 X][i32 Y][i32 ?]. Eso se contrasto contra el rango real de los REFR
     de 745 celdas exteriores: 745/745 para esta lectura, y 13/745, 21/745 y
     24/745 para las otras tres. El control puede fallar y esta es la que pasa.

  4. Skyrim.esm NO tiene FMAP, asi que anadir FormIDs no obliga a reescribir la
     tabla de forms. Su TES4 mide 54 bytes y no cambia al crecer el archivo.

QUE TOCA ESTE SCRIPT
--------------------
Solo cuatro campos: el campo size de los GRUP tipo=5, tipo=4, tipo=1 y 'WRLD'.
Ni un byte mas. La cabecera TES4, el GMST, los 920.181 bloques restantes y los
68.688 GRUPs quedan byte a byte donde estaban.

POR QUE LOS REFR APUNTAN A FormIDs 03xxxxxx DE NUESTRO ESP
-----------------------------------------------------------
Los REFR se resuelven al ACTIVAR la celda, no al cargar el plugin, y para esa
hora todos los plugins ya estan cargados. Asi que un REFR living en Skyrim.esm
puede apuntar a un STAT de un plugin posterior. NO se puede comprobar aqui sin
arrancar el juego: es la hipotesis mas fragile de este trabajo y esta marcada
como tal en el informe.

FALSIFICACION
-------------
--sin-celda tiene que producir un archivo IDENTICO byte a byte, y abortar si no.
Es la unica forma de saber que el recorrido y el rearmado no tocan nada.
"""
import json
import math
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "vendor"))
sys.path.insert(0, str(ROOT / "auditoria"))
from parser_esm import Plugin, CABECERA  # noqa: E402
import v11_layout as L  # noqa: E402
import mundo_v11 as M  # noqa: E402
from chunk_o_xclc import camino  # noqa: E402

ESM = Path(r"G:\Modding\Skyrim_Runtime_1.6.1170\Data\Skyrim.esm")
ESP = ROOT / "mod" / "AstraAsedio.esp"
CELDA_ANCLA = 0x0000963D
EDID_CELDA = "AstraAsedioAtalayaOeste"
U64 = 65536


# --- serializacion ------------------------------------------------------------

def sub(tipo, datos):
    return tipo + struct.pack("<H", len(datos)) + datos


def record(tipo, formid, flags, subs):
    """Cabecera de 24 bytes, como Bethesda: tipo, dataSize, flags, formID y 8 de
    control de version. Escribiendo 16 (tipo+size+flags+formID) el archivo deja
    de embaldosar 8 bytes por record: lo detecta el recorrido, no la vista."""
    cuerpo = b"".join(subs)
    return (tipo + struct.pack("<III", len(cuerpo), flags, formid)
            + b"\0" * 8 + cuerpo)


def grup(label, tipo, cuerpo):
    """GRUP: 'GRUP' + size(incluye los 24) + label + tipo(i32) + 8 de relleno."""
    return (b"GRUP" + struct.pack("<I", len(cuerpo) + CABECERA)
            + struct.pack("<Ii", label, tipo) + b"\0" * 8 + cuerpo)


def refr(formid, stat, pos, rot_deg, flags):
    """REFR con NAME y DATA de 24 bytes: 3 float, 3 u16 de angulo, u16, u32 flags."""
    ang = [int(round(a / 360.0 * U64)) % U64 for a in rot_deg]
    data = struct.pack("<3f3H2xI", pos[0], pos[1], pos[2],
                       ang[0], ang[1], ang[2], flags)
    return record(b"REFR", formid, 0, [sub(b"NAME", struct.pack("<I", stat)), sub(b"DATA", data)])


# --- lectura de los REFR del ESP ----------------------------------------------

def refrs_del_esp(ruta=ESP):
    p = Plugin(str(ruta))
    salida = []
    for t, o, tam, pr in p.recorrer():
        if t != "REFR":
            continue
        ss = dict(Plugin.subrecords(p.datos(o)))
        data = ss["DATA"]
        if len(data) != 24:
            continue
        x, y, z = struct.unpack_from("<3f", data, 0)
        a, b, c = struct.unpack_from("<3H", data, 12)
        flags = struct.unpack_from("<I", data, 20)[0]
        salida.append({
            "origen": p.form_id(o),
            "stat": struct.unpack_from("<I", ss["NAME"], 0)[0],
            "pos": (x, y, z),
            # los angulos del ESP se leen como los da el motor; config.json usa
            # otros numeros y no coinciden, asi que se clona lo REAL del ESP
            "rot": (a / U64 * 360.0, b / U64 * 360.0, c / U64 * 360.0),
            "flags": flags,
        })
    return salida


def transformar(items, mundo):
    """Devuelve los items con pos y rot ya en coordenadas de mundo."""
    conv = L.engine_convention()
    rt = L.transform_matrix((0, 0, 0), (0, 0, mundo["rot_z_deg"]), 1.0, *conv)["r"]
    salida = []
    for it in items:
        rl = L.transform_matrix((0, 0, 0), it["rot"], 1.0, *conv)["r"]
        r = [[sum(rt[i][k] * rl[k][j] for k in range(3)) for j in range(3)]
             for i in range(3)]
        px, py, pz = it["pos"]
        salida.append({
            "origen": it["origen"], "stat": it["stat"], "flags": it["flags"],
            "pos": (mundo["x"] + px, mundo["y"] + py, mundo["z"] + pz),
            "rot": L.euler_from_matrix(r),
        })
    return salida


# --- FormIDs libres del modulo 00 ---------------------------------------------

def formids_libres(d, cuantos, desde=0x00F00000):
    usados = set()
    for t, o, tam, pr in Plugin(str(ESM)).recorrer():
        usados.add(struct.unpack_from("<I", d, o + 12)[0])
    libres = []
    cand = desde
    while len(libres) < cuantos:
        cand += 1
        if cand > 0x00FFFFFF:
            raise SystemExit("no quedan FormIDs 00 libres")
        if cand not in usados:
            libres.append(cand)
    return libres


# --- el parche ----------------------------------------------------------------

def parchar(d, mundo, items, con_celda=True):
    off_ancla, cadena = camino(Plugin(str(ESM)), d, CELDA_ANCLA)
    if off_ancla is None:
        raise SystemExit("no se encontro la celda ancla %08X" % CELDA_ANCLA)

    # el ancla tiene que estar en el chunk que digamos; si no, el GRUP tipo=5
    # que toques no es el correcto y se aborta en vez de escribir basura
    xc = dict(Plugin.subrecords(Plugin(str(ESM)).datos(off_ancla)))
    gx, gy = struct.unpack_from("<2i", xc["XCLC"], 0)
    if (gx, gy) != (mundo["celda_x"], mundo["celda_y"]):
        raise SystemExit(
            "el ancla %08X esta en el chunk (%d,%d) y el mundo pide (%d,%d): "
            "se parchearia el chunk equivocado"
            % (CELDA_ANCLA, gx, gy, mundo["celda_x"], mundo["celda_y"]))

    if not con_celda:
        return d, {"delta": 0, "formids": []}

    total = len(items) + 1
    ids = formids_libres(d, total)
    id_celda = ids[0]
    bloques = b"".join(refr(ids[i + 1], it["stat"], it["pos"], it["rot"], it["flags"])
                       for i, it in enumerate(items))
    interior = grup(id_celda, 9, bloques)
    arbol = grup(id_celda, 6, interior)
    celda = record(b"CELL", id_celda, 0, [
        sub(b"EDID", EDID_CELDA.encode("cp1252") + b"\0"),
        sub(b"DATA", b"\x42\x00"),
        sub(b"XCLC", struct.pack("<3i", mundo["celda_x"], mundo["celda_y"],
                                 struct.unpack_from("<i", xc["XCLC"], 8)[0])),
    ])

    # Punto de insercion: justo antes del cierre del cuerpo del GRUP tipo=5.
    # El campo size de un bloque YA incluye sus 24 bytes de cabecera, asi que
    # el fin del cuerpo es off + size y NO off + CABECERA + size. Sumar la
    # cabecera dos veces mete la insercion 24 bytes mas alla del final, dentro
    # del bloque siguiente: el archivo podria seguir embaldosando si el size
    # del GRUP queda corto, pero el contenido queda en el sitio equivocado.
    o5 = cadena[3][2]
    t5 = cadena[3][3]
    ins = o5 + t5
    # El fin del cuerpo tiene que ser justo donde empieza el SIGUIENTE bloque,
    # que aqui es el GRUP tipo=5 hermano (label 0x0001FFFC). Mirar detras es
    # un error: un GRUP termina en 8 bytes de relleno, no con la etiqueta del
    # siguiente. Este control puede fallar y fallo la primera vez por eso.
    if d[ins:ins + 4] != b"GRUP":
        raise SystemExit(
            "el punto de insercion +%d no coincide con el inicio de un bloque: "
            "alli hay %r. El size del GRUP no es el que se cree."
            % (ins, d[ins:ins + 4]))

    salida = bytearray(d[:ins]) + celda + arbol + bytearray(d[ins:])
    delta = len(celda) + len(arbol)
    # los cuatro GRUP ancestros crecen; el size esta en offset+4 y el campo
    # mide el bloque completo, asi que se suma el delta tal cual
    for _gt, _lbl, off, _tam in cadena:
        v = struct.unpack_from("<I", salida, off + 4)[0] + delta
        struct.pack_into("<I", salida, off + 4, v)
    return bytes(salida), {"delta": delta, "formids": ids, "ins": ins,
                           "id_celda": id_celda}


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", required=True)
    ap.add_argument("--sin-celda", action="store_true")
    ap.add_argument("--esm", default=str(ESM))
    a = ap.parse_args()

    d = Plugin(a.esm).d
    mundo = M.cargar_colocacion()
    mundo = dict(mundo)
    mundo["celda_x"] = 1
    mundo["celda_y"] = -4

    items = transformar(refrs_del_esp(), mundo)
    salida, info = parchar(d, mundo, items, con_celda=not a.sin_celda)

    if a.sin_celda:
        if salida != d:
            print("FALLA DE FALSIFICACION: --sin-celda cambio el archivo")
            raise SystemExit(1)
        print("FALSIFICACION OK: --sin-celda produce un archivo identico (%d bytes)"
              % len(salida))
        return 0

    Path(a.salida).write_bytes(salida)

    # El recorrido tiene que embaldosar el archivo resultante. Un size mal
    # puesto NO se ve comparando offsets: se ve porque el recorrido revienta.
    # Sin esto el script escribiria un archivo plausible y corrupto.
    try:
        n = sum(1 for _ in Plugin(a.salida).recorrer())
        ident = "identidad OK, %d bloques" % n
        ok = True
    except Exception as e:
        ident = "REVIENTA: %s" % e
        ok = False

    print("escrito %s: %d -> %d bytes (delta +%d)"
          % (a.salida, len(d), len(salida), info["delta"]))
    print("  %s" % ident)
    print("  celda %08X '%s' con %d REFR, insertada en +%d"
          % (info["id_celda"], EDID_CELDA, len(items), info["ins"]))
    print("  primer REFR %08X -> STAT %08X pos=(%.1f, %.1f, %.1f)"
          % (info["formids"][1], items[0]["stat"], *items[0]["pos"]))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())