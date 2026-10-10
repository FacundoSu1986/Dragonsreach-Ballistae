"""Place the atalaya back on the western site. Never edit terrain, navmesh, or quests.

The fitted mesh and the fifteen owned references already exist in the v20
plugin at this origin. The ballista stays on the same X/Y, 151.55 units above
the tower. Copying that plugin is the placement: rebuilding from the northeast
heightmaps would put the other hillside's pilings on this ground.
"""
import json, struct, math, hashlib
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import patch_plugin_v12 as P
from build_modular_v13 import subs

SITE = {
    'x': 4665.54,
    'y': -14922.81,
    'z': -5217.81,
    'rot_z_deg': 187.63,
    'cell': '0000963D',
    'grid': [1, -4],
}
MUNDO_BLOCK = '''  "mundo": {
   "x": 4665.54,
   "y": -14922.81,
   "z": -5217.81,
   "rot_z_deg": 187.63,
   "cell": "0000963D",
   "grid": [
    1,
    -4
   ]
  }'''

def main():
    parent = ROOT.with_name('Ballesta_Astra_Vanilla_SE_v20')
    rel = 'addons/Atalaya/AstraAsedio_Atalaya.esp'
    source = Plugin(str(parent/rel))
    old = P.record_map(source)
    oldsite = json.loads((parent/'config.json').read_text())['tower_v11']['mundo']
    for key in ('x', 'y', 'z', 'rot_z_deg'):
        assert abs(oldsite[key] - SITE[key]) < 1e-4, (key, oldsite[key], SITE[key])
    assert oldsite['cell'] == SITE['cell'] and oldsite['grid'] == SITE['grid']
    tower = struct.unpack('<6f', subs(old[0x04000A01])['DATA'])
    gun = struct.unpack('<6f', subs(old[0x04000A00])['DATA'])
    assert max(abs(a-b) for a, b in zip(tower[:3], (SITE['x'], SITE['y'], SITE['z']))) < 0.01
    assert abs(gun[0]-tower[0]) < 0.01 and abs(gun[1]-tower[1]) < 0.01
    assert abs(gun[2]-tower[2]-151.55) < 0.01
    assert abs(math.degrees(tower[5]) % 360 - SITE['rot_z_deg']) < 0.01
    model = subs(old[0x04000A50])['MODL'].rstrip(b'\0').decode().replace('\\', '/')
    nif = ROOT/'addons/Atalaya/meshes'/model
    assert nif.is_file(), nif
    owned = [fid for fid, raw in old.items() if fid >> 24 == 4 and raw[:4] == b'REFR']
    assert len(owned) == 15, owned
    raw = (parent/rel).read_bytes()
    (ROOT/rel).write_bytes(raw)
    # The copied plugin stops the stair on the rubble. apply() is the entrance fix.
    import clear_stair_entrance_v21
    clear_stair_entrance_v21.apply(ROOT/rel)
    raw = (ROOT/rel).read_bytes()
    cfg_path = ROOT/'config.json'
    text = cfg_path.read_text(encoding='utf-8')
    start = text.index('  "mundo": {')
    end = text.index('\n  }', start)
    cfg_path.write_text(text[:start] + MUNDO_BLOCK + text[end+4:], encoding='utf-8')
    written = json.loads(cfg_path.read_text(encoding='utf-8'))['tower_v11']['mundo']
    assert written == SITE
    result = {
        'path': rel.replace('/', '\\'),
        'sha256': hashlib.sha256(raw).hexdigest(),
        'bytes': len(raw),
        'records': len(P.record_map(Plugin(str(ROOT/rel)))),
        'site': SITE,
        'model': model,
        'nif_sha256': hashlib.sha256(nif.read_bytes()).hexdigest(),
        'moved_owned_refs': [f'{fid:08X}' for fid in sorted(owned)],
        'stable_form_ids': True,
        'ballista_above_origin': 151.55,
        'LAND_edits': 1,
        'NAVM_edits': 0,
        'quest_edits': 0,
        'vanilla_refs_edited': 2,
        'disabled_refs': ['000E4396', '000E4397'],
        'cell': SITE['cell'],
        'game_tested': False,
    }
    (ROOT/'reports/atalaya_placement_v21.json').write_text(json.dumps(result, indent=2))
    print('ATALAYA_PLACED', len(owned), SITE, model)

if __name__ == '__main__':
    main()
