"""Which way does the FarmhouseAnimDoor leaf swing in game? Decided from Bethesda's own placements.

The Open sequence turns the hinge node Door01 from 0 to -95 degrees about Z (read from the NIF).
Whether that is clockwise or counter-clockwise in the engine is not assumed: for every vanilla
placement of FarmhouseAnimDoor01/02 in Skyrim.esm the leaf is swung both ways (angles of the NIF
keys, from the hinge, in the engine's measured reference convention) and its hinge-side corners
are tested against the meshes Bethesda placed around it (the frame, walls). The swing that real
placements leave free is the engine's. Meshes are read from config.extracted in memory only; the
report keeps FormIDs and counts.
"""
import collections, json, math, struct, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import v11_layout as L

CFG = L.load_cfg()
DOOR_MODELS = ('architecture\\farmhouse\\farmhouseanimdoor01.nif', 'architecture\\farmhouse\\farmhouseanimdoor02.nif')
PIVOT = (48.0, 4.0)            # Door01 node of the NIF (x, y); its rotation axis is local Z
NEAR = 60.0                    # neighbour triangles considered around the hinge
CONTACT = 1.0                  # a leaf point closer than this to a placed mesh counts as a clash
ANGLES = range(10, 96, 5)

def point_tri(p, A, B, C):
    """Distances from points p (n,3) to every triangle (m) -> (n,m)."""
    n = np.cross(B - A, C - A); nn = np.linalg.norm(n, axis=1); ok = nn > 1e-9; n = n/np.where(ok, nn, 1)[:, None]
    d = np.einsum('pk,mk->pm', p, n) - np.einsum('mk,mk->m', A, n)[None, :]
    proj = p[:, None, :] - d[:, :, None]*n[None, :, :]
    def side(u, v): return np.einsum('pmk,mk->pm', np.cross((v - u)[None, :, :], proj - u[None, :, :]), n) >= -1e-9
    inside = ok[None, :] & side(A, B) & side(B, C) & side(C, A)
    def seg(u, v):
        e = v - u; t = np.clip(np.einsum('pmk,mk->pm', p[:, None, :] - u[None, :, :], e)/np.maximum(np.einsum('mk,mk->m', e, e), 1e-12)[None, :], 0, 1)
        return np.linalg.norm(p[:, None, :] - (u[None, :, :] + t[:, :, None]*e[None, :, :]), axis=2)
    return np.where(inside, np.abs(d), np.minimum(np.minimum(seg(A, B), seg(B, C)), seg(C, A)))

def main():
    esm = Plugin(str(L.esm_path(CFG))); models = {}; doors = []; cell = None
    for tipo, o, _t, _p in esm.recorrer():
        if tipo in ('STAT', 'DOOR', 'FURN', 'CONT', 'MSTT', 'ACTI'):
            ss = dict(esm.subrecords(esm.datos(o)))
            if 'MODL' in ss: models[esm.form_id(o)] = (tipo, L.zstr(ss['MODL']).lower())
    refs = collections.defaultdict(list)
    for tipo, o, _t, _p in esm.recorrer():
        if tipo == 'CELL': cell = esm.form_id(o)
        elif tipo == 'REFR':
            ss = dict(esm.subrecords(esm.datos(o)))
            base = struct.unpack('<I', ss['NAME'])[0]
            if base not in models or 'DATA' not in ss: continue
            x, y, z, rx, ry, rz = struct.unpack('<6f', ss['DATA'])
            scale = struct.unpack('<f', ss['XSCL'])[0] if 'XSCL' in ss else 1.0
            r = {'fid': esm.form_id(o), 'base': base, 'model': models[base][1], 'pos': (x, y, z),
                 'rot_deg': tuple(math.degrees(a) for a in (rx, ry, rz)), 'scale': scale}
            refs[cell].append(r)
            if r['model'] in DOOR_MODELS: doors.append((cell, r))
    order, signs = L.engine_convention(); cache = {}
    def mesh(model):
        if model not in cache:
            try:
                V, T = L.nif_triangles(Path(CFG['extracted'])/'meshes'/model)
                cache[model] = (V, T) if len(V) and len(T) else None   # no BSTriShape: nothing to hit
            except Exception: cache[model] = None
        return cache[model]
    def world(r, V):
        m = L.transform_matrix(r['pos'], r['rot_deg'], r['scale'], order, signs)
        return V @ (np.array(m['r'])*m['s']).T + np.array(m['t'])
    rows = []; votes = collections.Counter()
    for cell, door in doors:
        DV, DT = mesh(door['model'])
        # Leaf points around the hinge that really move (4-25 u from its axis): the corners that
        # sweep past the hinge line. Points on the axis touch the frame at every angle and tell nothing.
        rad = np.hypot(DV[:, 0] - PIVOT[0], DV[:, 1] - PIVOT[1])
        # Measured 2026-10-06: the vanilla frames hug the leaf, so the corners near the hinge decide
        # nothing (17 of 17 ties). The whole leaf decides: Bethesda leaves room on the side it opens to.
        near_hinge = DV[rad > 4.0]
        m = L.transform_matrix(door['pos'], door['rot_deg'], door['scale'], order, signs)
        Rm = np.array(m['r'])*m['s']; pivot_w = Rm @ np.array([PIVOT[0], PIVOT[1], 0.0]) + np.array(m['t'])
        tris = []
        for r in refs[cell]:
            if r['fid'] == door['fid'] or math.dist(r['pos'], door['pos']) > 400: continue
            mm = mesh(r['model'])
            if mm is None: continue
            V, T = mm; W = world(r, V); Tw = W[T]
            close = np.hypot(Tw[:, :, 0] - pivot_w[0], Tw[:, :, 1] - pivot_w[1]).min(axis=1) < NEAR + 100.0
            if close.any(): tris.append(Tw[close])
        if not tris: continue
        Tn = np.concatenate(tris)
        closed = point_tri(world(door, near_hinge), Tn[:, 0], Tn[:, 1], Tn[:, 2]).min(axis=1)
        free = closed > CONTACT + 1.0                        # only points clear of everything when closed
        if not free.any(): continue
        result = {}
        for name, sign in (('local_ccw', 1), ('local_cw', -1)):     # ccw = counter-clockwise in the NIF frame
            hits = 0
            for ang in ANGLES:
                a = math.radians(sign*ang); c, s = math.cos(a), math.sin(a)
                rel = near_hinge[free, :2] - np.array(PIVOT)
                # Rotate counter-clockwise by a (column vectors): [[c,-s],[s,c]] applied as rel @ R.T.
                P = np.c_[rel @ np.array([[c, s], [-s, c]]) + np.array(PIVOT), near_hinge[free, 2]]
                if point_tri(world(door, P), Tn[:, 0], Tn[:, 1], Tn[:, 2]).min() < CONTACT: hits += 1
            result[name] = hits
        verdict = 'ccw' if result['local_cw'] > result['local_ccw'] else 'cw' if result['local_ccw'] > result['local_cw'] else 'tie'
        votes[verdict] += 1
        rows.append({'door': '%08X' % door['fid'], 'cell': '%08X' % (cell or 0), 'hits_local_ccw': result['local_ccw'], 'hits_local_cw': result['local_cw'], 'verdict': verdict})
    decided = None
    if votes['ccw'] >= 5 and votes['ccw'] >= 4*max(votes['cw'], 1): decided = 'ccw'
    if votes['cw'] >= 5 and votes['cw'] >= 4*max(votes['ccw'], 1): decided = 'cw'
    keys = []
    nif_angles = 'Open keys turn Door01 from 0 to -95 degrees about Z (NiTransformData); ccw/cw below are seen from +Z in the door frame'
    out = {'decided': decided, 'votes': dict(votes), 'doors_with_neighbours': len(rows), 'angles_tested_deg': list(ANGLES),
           'contact_units': CONTACT, 'note': nif_angles, 'rows': rows}
    (ROOT/'reports/door_swing.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    print('DOOR_SWING', decided, dict(votes), len(rows), 'doors')
    return 0 if decided else 1

if __name__ == '__main__': sys.exit(main())
