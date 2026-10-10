import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

def test_lowered_layout_and_shields():
    cfg = json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))
    assert cfg['tower_v11']['platform']['deck_top'] in (140.0, 210.0)
    assert cfg['tower_v11']['room']['size'] == [0, 0]
    assert cfg['tower_v11']['pieces'] == []
    assert len(cfg['tower_v11']['escudos']['items']) == 12
    assert abs(cfg['tower_top_units'] - cfg['tower_v11']['platform']['deck_top'] - 11.55) < .001

def test_short_stair_no_room_and_grounded_supports():
    import tower_v12_geometry as G
    cfg = json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))
    geo = G.build(cfg)
    assert geo['counts']['tablas_pared'] == 0
    assert not any(p['name'].startswith(('Marco_puerta', 'Pared_frente')) for p in geo['parts'])
    assert 10 <= geo['counts']['peldanos'] <= 16
    piles = [m for m in geo['logs'] if m['name'].startswith('Pilote_bajo_')]
    assert len(piles) >= 16
    assert all(m['a'][2] <= 0 and m['b'][2] > 0 for m in piles)
    assert abs(G.SZ1 - cfg['tower_v11']['platform']['deck_top']) < .001
    assert abs(G.ramp_z(G.SY0)) < .001
    assert abs(G.ramp_z(G.SY1) - G.SZ1) < .001

def test_navigation_connects_ground_stair_and_operator():
    import build_plugin as B
    report = B.validate_plugin(str(ROOT/'mod/AstraAsedio.esp'))
    assert report['navmesh_components'] == 1

def test_shield_front_faces_outward():
    import numpy as np
    import v11_layout as L
    cfg = L.load_cfg()
    for item in cfg['tower_v11']['escudos']['items']:
        m = L.transform_matrix(item['pos'], item['rot_deg'], 1.0, *L.engine_convention())
        # Measured vanilla IronShield: handle on +Z; decorated front on -Z.
        front = np.array(m['r']) @ np.array([0., 0., -1.])
        assert np.dot(front[:2], item['mirar']) > .999

def test_step_envelope_does_not_remove_low_ceiling_obstruction():
    import build_plugin as B
    slab = {'min': [-10., -10., 128.8], 'max': [10., 10., 140.], 'nav_step_units': 16.}
    assert B.triangle_blocked([(-2., -2., 2.), (2., -2., 2.), (0., 2., 2.)], slab)
    assert not B.triangle_blocked([(-2., -2., 130.), (2., -2., 130.), (0., 2., 130.)], slab)
    assert B.triangle_blocked([(-2., -2., 123.), (2., -2., 123.), (0., 2., 123.)], slab)
