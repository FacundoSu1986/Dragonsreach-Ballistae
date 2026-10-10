import importlib.util
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]

def test_railing_below_depressed_shot():
    import tower_v12_geometry as G
    import verify_shot_clearance_v12 as S
    cfg = json.loads((ROOT/'config.json').read_text())
    muzzle, bore = S.Aim(cfg).pose(0, -20)
    origin_r = math.hypot(*muzzle[:2])
    for part in G.build(cfg)['parts']:
        if not part['name'].startswith(('Baranda_', 'Pasamanos_', 'Amarre_Baranda_', 'Amarre_Pasamanos_')):
            continue
        for x,y,z in part['verts']:
            radial = math.hypot(x,y)
            line = muzzle[2] + (radial-origin_r)*bore[2]/math.hypot(*bore[:2])
            assert z <= line-5, (part['name'], z, line)

def test_v13_pitch_config():
    cfg = json.loads((ROOT/'config.json').read_text())
    assert cfg['pitch_min'] == -20
