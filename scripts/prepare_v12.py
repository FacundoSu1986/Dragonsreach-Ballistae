"""Generate the lowered configuration from the untouched, tested v11 project."""
import argparse
import json
from pathlib import Path
import v11_layout as L

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.with_name('Ballesta_Astra_Vanilla_SE_v11')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--deck', type=float, choices=(140.0, 210.0), default=140.0)
    height = ap.parse_args().deck
    cfg = json.loads((BASE / 'config.json').read_text(encoding='utf-8'))
    delta = height - 453.95
    cfg['source'] = str(ROOT / 'source/Torre_Ballesta_lowpoly_v04.blend')
    cfg['tower_top_units'] += delta
    lay = cfg['tower_v11']
    lay['note'] = 'v12: lower platform, no room or door, own full-diameter foundation.'
    lay['room']['size'] = [0, 0]
    lay['room']['removed'] = True
    lay['platform']['pile_top'] += delta
    lay['platform']['deck_top'] = height
    lay['corner_posts']['top_z'] += delta
    lay['pieces'] = []
    lay['mundo']['origen_del_datum'] = 'Local Z=0 remains ground; short stair starts at zero.'
    esc = lay['escudos']
    old = {it['nombre']: it for it in esc['items']}
    # Match real post axes. The east shields stay before the upper stair approach.
    sites = [('O', 'O', 0.0), ('N1', 'N', -78.846154), ('N2', 'N', 115.307692),
             ('E', 'E', 4.8), ('S', 'S', 0.0), ('O2', 'O', -182.0),
             ('O3', 'O', 182.0), ('N3', 'N', -175.923077), ('N4', 'N', 212.384615),
             ('S2', 'S', -182.0), ('S3', 'S', 182.0), ('E2', 'E', -180.4)]
    items = []
    for name, side, along in sites:
        template = old['N1' if side == 'N' else side]
        item = dict(template, nombre=name, side=side)
        x, y = {'O': (-303.0, along), 'E': (303.0, along),
                'N': (along, 303.0), 'S': (along, -303.0)}[side]
        item['pos'] = [x, y, height + 43.0]
        # Vanilla IronShield's front is -Z; +Z is the handle. Keep local +Y upright.
        m = L.transform_matrix(item['pos'], item['rot_deg'], 1.0, *L.engine_convention())
        flipped = [[m['r'][r][c] * (-1 if c in (0, 2) else 1) for c in range(3)] for r in range(3)]
        item['rot_deg'] = [round(a, 6) for a in L.euler_from_matrix(flipped)]
        item.pop('wood_contact_units', None)
        items.append(item)
    esc['items'] = items
    esc.pop('radio_exterior', None)
    esc['nota'] = 'v12: 12 shields. Individual handle-to-wood fitting measured on written torre.nif.'
    cfg['revision_v12'] = {'deck_units': height, 'delta_units': delta, 'room_removed': True,
                           'source_project': str(BASE), 'game_tested': False}
    (ROOT / 'config.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print('V12_CONFIG', 'deck', height, 'mount', cfg['tower_top_units'], 'shields', len(items))

if __name__ == '__main__': main()
