"""Patch the tested v11 ESP without rebuilding weapon, scripts or world/terrain.

Always read the immutable v11 baseline. Preserve reference identities in both cells.
Only structure, shield DATA, ballista Z, and laboratory NAVM/NAVI may change.
"""
import json
import hashlib
import math
import struct
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.with_name('Ballesta_Astra_Vanilla_SE_v11')
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]
import colocar_escudos as C
import build_plugin as B
import mundo_v11 as M
from parser_esm import Plugin
import escritor_plugin as W

def modify_subs(raw, updates):
    body = b''.join(W.sub(k, updates.get(k, v)) for k, v in Plugin.subrecords(raw[24:]))
    return raw[:4] + struct.pack('<I', len(body)) + raw[8:24] + body

def record_map(p):
    return {p.form_id(o): p.d[o:o+24+n] for t, o, n, dep in p.recorrer() if t not in ('GRUP', 'TES4')}

def transform_groups(group, changes, removed, added):
    label, typ = C.etiqueta(group)
    children = []
    for off, size, raw in C.hijos(group):
        if raw[:4] == b'GRUP':
            children.append(transform_groups(raw, changes, removed, added))
        else:
            fid = struct.unpack_from('<I', raw, 12)[0]
            if fid not in removed: children.append(changes.get(fid, raw))
    if typ == 9: children.extend(added.get(label, []))
    return C.rearmar(group, children)

def update_header(raw, count, next_id):
    body = []
    for k, v in Plugin.subrecords(raw[24:]):
        if k == 'HEDR': v = v[:4] + struct.pack('<II', count, next_id)
        body.append(W.sub(k, v))
    body = b''.join(body)
    return raw[:4] + struct.pack('<I', len(body)) + raw[8:24] + body

def main():
    cfg = json.loads((ROOT/'config.json').read_text(encoding='utf-8'))
    p = Plugin(str(BASE/'mod/AstraAsedio.esp'))
    source = record_map(p)
    delta = cfg['revision_v12']['delta_units']
    mapping = {int(r['origen'], 16): int(r['nuevo'], 16) for r in
               json.loads((BASE/'reports/mundo_esp_v11.json').read_text())['refr_en_mundo']}
    oldcfg = json.loads((BASE/'config.json').read_text(encoding='utf-8'))
    removed_local = set(range(B.VANILLA_FIRST, B.VANILLA_FIRST + len(oldcfg['tower_v11']['pieces'])))
    removed = removed_local | {mapping[i] for i in removed_local}
    changes = {}
    bbox = json.loads((ROOT/'reports/assets.json').read_text())['torre']['bbox_units']
    obnd = [math.floor(v) for v in bbox['min']] + [math.ceil(v) for v in bbox['max']]
    changes[B.IDS['tower']] = modify_subs(source[B.IDS['tower']], {'OBND': struct.pack('<6h', *obnd)})
    for fid in (B.IDS['ballesta_ref'], mapping[B.IDS['ballesta_ref']]):
        data = dict(Plugin.subrecords(source[fid][24:]))['DATA']
        xyz = list(struct.unpack('<6f', data)); xyz[2] += delta
        changes[fid] = modify_subs(source[fid], {'DATA': struct.pack('<6f', *xyz)})
    added = {B.IDS['cell']: [], 0x963D: []}
    for i, item in enumerate(cfg['tower_v11']['escudos']['items']):
        local_fid = C.REFR_BASE + i
        old = i < 5
        world_fid = mapping[local_fid] if old else 0x03000A48 + i - 5
        pos, rot = item['pos'], item['rot_deg']
        world_pos, world_rot = M.llevar({'pos': pos, 'rot_deg': rot, 'scale': 1.0}, cfg['tower_v11']['mundo'])
        for fid, position, rotation, cell, suffix in (
            (local_fid, pos, rot, B.IDS['cell'], ''),
            (world_fid, world_pos, world_rot, 0x963D, 'Mundo')):
            data = struct.pack('<6f', *position, *(math.radians(v) for v in rotation))
            if old:
                changes[fid] = modify_subs(source[fid], {'DATA': data})
            else:
                if fid in source: raise ValueError('New FormID already used: %08X' % fid)
                added[cell].append(C.referencia(fid, C.STAT_ESCUDO, position,
                                   tuple(math.radians(v) for v in rotation), 'AstraEscudo'+item['nombre']+suffix))
    nv, mi, navreport = B.navmesh_geometry()
    changes[B.IDS['navmesh']] = modify_subs(source[B.IDS['navmesh']], {'NVNM': nv})
    changes[0x12FB4] = modify_subs(source[0x12FB4], {'NVMI': mi})
    original = p.d
    start = C.leer_cabecera(original)[4]
    groups = []
    off = start
    while off < len(original):
        size = struct.unpack_from('<I', original, off+4)[0]
        raw = original[off:off+size]
        groups.append(transform_groups(raw, changes, removed, added))
        off += size
    body = b''.join(groups)
    count = C.bloques_totales(body, 0)
    header = update_header(original[:start], count, 0xA4F)
    out = ROOT/'mod/AstraAsedio.esp'
    out.write_bytes(header+body)
    result = record_map(Plugin(str(out)))
    for fid, raw in source.items():
        if fid not in removed and fid not in changes and result.get(fid) != raw:
            raise ValueError('Unexpected record change: %08X' % fid)
    expected_new = {struct.unpack_from('<I', r, 12)[0] for items in added.values() for r in items}
    if result.keys() != (source.keys() - removed | expected_new):
        raise ValueError('Record IDs differ from allowlist')
    checked = B.validate_plugin(str(out))
    if checked['navmesh_components'] != 1: raise ValueError('Disconnected navigation')
    report = {'source_sha256': hashlib.sha256(original).hexdigest(),
              'sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'bytes': out.stat().st_size,
              'removed_refs': ['%08X'%i for i in sorted(removed)],
              'changed_records': ['%08X'%i for i in sorted(changes)],
              'added_refs': ['%08X'%i for i in sorted(expected_new)],
              'all_other_records_preserved_byte_for_byte': True,
              'land_and_vanilla_overrides_preserved': True,
              'navmesh': navreport, 'validation': checked,
              'world_own_refs': 15, 'local_shields': 12, 'world_shields': 12,
              'game_tested': False}
    (ROOT/'reports/plugin_v12.json').write_text(json.dumps(report, indent=2))
    print('V12_PLUGIN_PATCHED', report['bytes'], 'removed', len(removed), 'new', len(expected_new),
          'navmesh', checked['navmesh_vertices'], checked['navmesh_triangles'], 'components', checked['navmesh_components'])

if __name__ == '__main__': main()
