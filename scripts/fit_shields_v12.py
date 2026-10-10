"""Fit shield handle vertices against the actual exported wooden tower (Blender)."""
import sys
import json
import hashlib
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]
import v11_layout as L

def main():
    cfg = L.load_cfg()
    esc = cfg['tower_v11']['escudos']
    v, tri = L.nif_triangles(ROOT/'mod/meshes/AstraAsedio/torre.nif')
    tree = BVHTree.FromPolygons([Vector(p) for p in v], tri.tolist(), all_triangles=True)
    shield = L.mesh_vertices(esc['modl'], cfg)
    back = shield[shield[:, 2] > 0.0]
    rows = []
    for item in esc['items']:
        m = L.transform_matrix(item['pos'], item['rot_deg'], 1.0, *L.engine_convention())
        n = Vector((*item['mirar'], 0))
        handle = back @ np.array(m['r']).T + np.array(m['t'])
        hits = []
        for point in handle:
            hit, normal, face, distance = tree.ray_cast(Vector(point), -n, 80.0)
            if hit is not None: hits.append(float(distance))
        if not hits: raise RuntimeError('No wooden support behind shield ' + item['nombre'])
        shift = min(hits) + 0.10  # slight seating, rather than an air gap at the handle
        initial = item['pos'][:]
        item['pos'] = [round(item['pos'][k] - n[k]*shift, 6) for k in range(3)]
        adjusted = handle - np.array(n)*shift
        nearest = min(tree.find_nearest(Vector(p))[3] for p in adjusted)
        if nearest > .25: raise RuntimeError('Shield handle misses wood after fit')
        item['wood_contact_units'] = round(nearest, 6)
        rows.append({'name': item['nombre'], 'before': initial, 'after': item['pos'],
                     'inward_shift_units': shift, 'handle_contact_distance_units': nearest})
    (ROOT/'config.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1)+'\n', encoding='utf-8')
    report = {'torre_sha256': hashlib.sha256((ROOT/'mod/meshes/AstraAsedio/torre.nif').read_bytes()).hexdigest(),
              'shields': rows, 'max_handle_contact_distance_units': max(r['handle_contact_distance_units'] for r in rows),
              'method': 'Back handle vertices raycast inward against written tower triangles; seat 0.10 u.',
              'game_tested': False}
    (ROOT/'reports/shields_v12.json').write_text(json.dumps(report, indent=2))
    print('SHIELDS_FITTED', len(rows), 'max_contact_gap', report['max_handle_contact_distance_units'])

if __name__ == '__main__': main()
