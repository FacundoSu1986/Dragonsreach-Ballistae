"""Open the western-watchtower stair without moving the tower.

ImpExtRubble03 fills the approach and ImpExtRubble02 sits on that same walk.
The first tread is about 45 units above the landscape, so deleting the rubble
and leaving the ground would still stop the player. This disables those two
references and raises nine height vertices to the tread. It does not edit
NAVM, quests, or any owned reference.

place_atalaya_v21 copies the v20 plugin and then calls apply(). Running apply
again rebuilds the same LAND and the same disabled references.
"""
import hashlib
import json
import struct
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'scripts' / 'vendor')]
import nivelar_terreno as T
import tower_v12_geometry as TG
import v11_layout as L
from colocar_escudos import etiqueta, hijos, rearmar
from parser_esm import Plugin
import escritor_plugin as W

LAND_ID = 0x0000A63D
DISABLED = (0x000E4396, 0x000E4397)  # ImpExtRubble03, ImpExtRubble02
INITIALLY_DISABLED = 0x00000800
COMPRESSED = 0x00040000
# Absolute world heights. Multiples of 8. Only raises, and only beside the stair.
HEIGHTS = {
    (12, 1): -5344.0,
    (12, 2): -5304.0,
    (12, 3): -5312.0,
    (13, 1): -5320.0,
    (13, 2): -5280.0,
    (13, 3): -5296.0,
    (14, 1): -5344.0,
    (14, 2): -5304.0,
    (14, 3): -5312.0,
}
SITE = {'x': 4665.54, 'y': -14922.81, 'z': -5217.81, 'rot_z_deg': 187.63}
FOOT_Y = -135.00011456100805


def runtime():
    return Path(json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))['runtime']) / 'Data'


def matrix():
    return L.transform_matrix((SITE['x'], SITE['y'], SITE['z']), (0, 0, SITE['rot_z_deg']), 1, *L.engine_convention())


def find_record(path, form_id, kind):
    plugin = Plugin(str(path))
    for typ, offset, _size, _depth in plugin.recorrer():
        if typ == kind and plugin.form_id(offset) == form_id:
            header = plugin.d[offset:offset + 24]
            return header, plugin.datos(offset)
    raise KeyError(hex(form_id))


def edited_grid(heights):
    grid = [row[:] for row in heights]
    for (row, col), z in HEIGHTS.items():
        if not (0 < row < 32 and 0 < col < 32):
            raise ValueError('Stair grade reaches the cell border')
        if z < heights[row][col] - 1e-6:
            raise ValueError('Stair grade digs a vertex')
        grid[row][col] = z
    return grid


def land_record():
    header, body = find_record(runtime() / 'Update.esm', LAND_ID, 'LAND')
    subs = Plugin.subrecords(body)
    names = [name for name, _data in subs]
    if names[:5] != ['DATA', 'VNML', 'VHGT', 'VCLR', 'ATXT']:
        raise ValueError('Unexpected LAND layout %s' % names[:5])
    by_name = {name: data for name, data in subs}
    _offset, heights = T.decodificar_vhgt(by_name['VHGT'])
    grid = edited_grid(heights)
    normals = T.decodificar_vnml(by_name['VNML'])
    touched = set(HEIGHTS)
    recalc = set(touched)
    for row, col in touched:
        recalc.update(T.vecinos(row, col))
    recalc = {(row, col) for row, col in recalc if 0 < row < 32 and 0 < col < 32}
    for row, col in recalc:
        normals[row][col] = T.normal_vertice(grid, row, col)
    replaced = {'VHGT': T.codificar_vhgt(grid, by_name['VHGT'][-3:]), 'VNML': T.codificar_vnml(normals)}
    new_body = b''.join(W.sub(name, replaced.get(name, data)) for name, data in subs)
    flags = struct.unpack_from('<I', header, 8)[0] & ~COMPRESSED
    record = header[:4] + struct.pack('<II', len(new_body), flags) + header[12:24] + new_body
    if struct.unpack_from('<I', record, 12)[0] != LAND_ID:
        raise ValueError('LAND form id changed')
    return record


def disabled_records():
    out = []
    for form_id in DISABLED:
        header, body = find_record(runtime() / 'Skyrim.esm', form_id, 'REFR')
        flags = struct.unpack_from('<I', header, 8)[0] | INITIALLY_DISABLED
        if struct.unpack_from('<I', header, 12)[0] != form_id:
            raise ValueError(hex(form_id))
        out.append(header[:4] + struct.pack('<II', len(body), flags) + header[12:24] + body)
    return out


def top_blocks(data, start):
    blocks = []
    pos = start
    while pos < len(data):
        size = struct.unpack_from('<I', data, pos + 4)[0]
        total = size if data[pos:pos + 4] == b'GRUP' else size + 24
        if total <= 0 or pos + total > len(data):
            raise ValueError('Block at %d does not fit' % pos)
        blocks.append(data[pos:pos + total])
        pos += total
    return blocks


def form_id(raw):
    return struct.unpack_from('<I', raw, 12)[0]


def rebuild(group, additions):
    label, group_type = etiqueta(group)
    children = []
    for _off, _size, raw in hijos(group):
        if raw[:4] == b'GRUP':
            children.append(rebuild(raw, additions))
        elif form_id(raw) not in additions:
            children.append(raw)
    if group_type == 9 and label == 0x963D:
        children = [additions[key] for key in (LAND_ID,) + DISABLED] + children
    return rearmar(group, children)


def block_count(data, start):
    pos = start
    count = 0
    while pos < len(data):
        kind = data[pos:pos + 4]
        size = struct.unpack_from('<I', data, pos + 4)[0]
        if kind == b'GRUP':
            count += 1 + block_count(data[pos + 24:pos + size], 0)
            pos += size
        else:
            count += 1
            pos += 24 + size
    if pos != len(data):
        raise ValueError('Count walk ended at %d' % pos)
    return count


def set_record_count(tes4, count):
    idx = tes4.find(b'HEDR')
    if idx < 0 or struct.unpack_from('<H', tes4, idx + 4)[0] != 12:
        raise ValueError('TES4 has no 12-byte HEDR')
    version, _old, nxt = struct.unpack_from('<fII', tes4, idx + 6)
    return tes4[:idx + 10] + struct.pack('<I', count) + tes4[idx + 14:]


def foot_clearance(grid):
    """Tread top minus landscape, sampled across the first step. Positive is a step up."""
    place = matrix()
    tread = SITE['z'] + TG.SLOPE * (FOOT_Y - TG.SY0) + 5.25
    lips = []
    for x in np.linspace(TG.SX0, TG.SX1, 9):
        wx, wy, _wz = L.apply(place, (float(x), FOOT_Y, 0.0))
        lips.append(tread - T.interpolar(grid, wx, wy))
    return lips


def apply(path=None):
    path = Path(path or ROOT / 'addons' / 'Atalaya' / 'AstraAsedio_Atalaya.esp')
    plugin = Plugin(str(path))
    additions = {LAND_ID: land_record()}
    for raw in disabled_records():
        additions[form_id(raw)] = raw
    blocks = top_blocks(plugin.d, plugin.inicio_datos)
    rebuilt = []
    for block in blocks:
        if block[:4] == b'GRUP' and etiqueta(block) == (0x444C5257, 0):
            rebuilt.append(rebuild(block, additions))
        else:
            rebuilt.append(block)
    body = b''.join(rebuilt)
    tes4 = set_record_count(plugin.d[:plugin.inicio_datos], block_count(body, 0))
    path.write_bytes(tes4 + body)
    # The same bytes have to come back out: a second pass is the identity.
    check = Plugin(str(path))
    list(check.recorrer())
    return {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'records_added': 3}


def main():
    first = apply()
    second = apply()
    if first != second:
        raise SystemExit('Stair patch is not idempotent')
    print('STAIR_CLEARED', first['bytes'], first['sha256'])


if __name__ == '__main__':
    main()
