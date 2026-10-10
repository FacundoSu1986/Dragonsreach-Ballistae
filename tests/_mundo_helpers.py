"""Lectores independientes para los tests de la colocacion en el mundo.

No importan nada de colocar_en_mundo.py ni de nivelar_terreno.py: un test que usa el
mismo codigo que produce el archivo solo prueba que el codigo se parece a si mismo.
Aqui el terreno y la estructura se leen con el parser del repo (validado contra el
corpus vanilla) y las transformaciones se rehacen a mano.
"""
import json
import math
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'scripts/vendor')]
from parser_esm import Plugin  # noqa: E402

CFG = json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))
DATA = Path(CFG['runtime']) / 'Data'
HAY_JUEGO = all((DATA / m).exists() for m in ('Skyrim.esm', 'Update.esm', 'Dawnguard.esm'))
ESP = ROOT / 'mod/AstraAsedio.esp'
ANTES = ROOT / 'auditoria/AstraAsedio.esp.antes_de_mundo'
MUNDO = CFG['tower_v11']['mundo']
CELDA = 0x0000963D
MASTERS = ('Skyrim.esm', 'Update.esm', 'Dawnguard.esm')      # orden de carga
CHUNK = (4096.0, 8192.0, -16384.0, -12288.0)                 # x0, x1, y0, y1 del grid (1,-4)
COMPRIMIDO = 0x00040000
PERSISTENTE = 0x00000400

_cache = {}


def cacheado(clave, f):
    if clave not in _cache:
        _cache[clave] = f()
    return _cache[clave]


def plugin(nombre):
    return cacheado(('plugin', nombre), lambda: Plugin(str(DATA / nombre)))


def altura(h, x, y):
    """Altura bilineal del mundo en (x, y) sobre la rejilla h[fila][col] de la celda."""
    gx, gy = (x - 4096.0) / 128.0, (y + 16384.0) / 128.0
    c, r = min(31, max(0, int(gx))), min(31, max(0, int(gy)))
    fx, fy = gx - c, gy - r
    return (h[r][c] * (1 - fx) * (1 - fy) + h[r][c + 1] * fx * (1 - fy)
            + h[r + 1][c] * (1 - fx) * fy + h[r + 1][c + 1] * fx * fy)


def decodificar(vhgt):
    """Alturas del mundo de un VHGT: float offset + 1089 int8, fila a fila, por 8."""
    off, = struct.unpack_from('<f', vhgt, 0)
    ds = struct.unpack_from('<1089b', vhgt, 4)
    h, arrastre = [], off
    for r in range(33):
        arrastre += ds[r * 33]
        acum, fila = arrastre, [arrastre * 8.0]
        for c in range(1, 33):
            acum += ds[r * 33 + c]
            fila.append(acum * 8.0)
        h.append(fila)
    return h


def a_mundo(lx, ly):
    """Marco local de la torre -> mundo, a mano: rot_z de motor 43,15 = giro -43,15."""
    t = math.radians(MUNDO['rot_z_deg'])
    return (MUNDO['x'] + lx * math.cos(t) + ly * math.sin(t),
            MUNDO['y'] - lx * math.sin(t) + ly * math.cos(t))


def land_de(nombre):
    """dict de subrecords del LAND de la celda 0000963D en ese master."""
    def leer():
        p = plugin(nombre)
        cur = None
        for t, o, _n, _d in p.recorrer():
            if t == 'CELL':
                cur = p.form_id(o)
            elif t == 'LAND' and cur == CELDA:
                return list(Plugin.subrecords(p.datos(o)))
        return None
    return cacheado(('land', nombre), leer)


def land_ganador():
    return land_de('Update.esm') or land_de('Skyrim.esm')


def land_del_esp(p):
    cur = None
    for t, o, _n, _d in p.recorrer():
        if t == 'CELL':
            cur = p.form_id(o)
        elif t == 'LAND' and cur == CELDA:
            return list(Plugin.subrecords(p.datos(o)))
    return None


def pilotes():
    tw = json.loads((ROOT / 'reports/v11_tower.json').read_text(encoding='utf-8'))
    out = []
    for r in tw['stilts']['rows']:
        a = r['name'].split('_')
        out.append((r['name'], float(a[1]), float(a[2]), r['bottom_z']))
    return out


def refrs_vanilla_de_la_celda():
    """{form_id: (flags, [(clave, bytes)])}: version ganadora de cada REFR de la celda."""
    def leer():
        out = {}
        for nombre in MASTERS:
            p = plugin(nombre)
            cur = None
            for t, o, _n, _d in p.recorrer():
                if t == 'CELL':
                    cur = p.form_id(o)
                elif t == 'REFR' and cur == CELDA:
                    out[p.form_id(o)] = (struct.unpack_from('<I', p.d, o + 8)[0],
                                         list(Plugin.subrecords(p.datos(o))))
        return out
    return cacheado('refrs_vanilla', leer)


def cadena(p, form_celda):
    """[(tipo, etiqueta)] de los GRUP que contienen al CELL."""
    pila = []
    for t, o, _n, pr in p.recorrer():
        if t == 'GRUP':
            pila[pr:] = [(struct.unpack_from('<i', p.d, o + 12)[0],
                          struct.unpack_from('<I', p.d, o + 8)[0])]
        elif t == 'CELL' and p.form_id(o) == form_celda:
            return list(pila[:pr])
    return None
