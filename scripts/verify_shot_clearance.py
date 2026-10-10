"""Plan task 9: no shot touches the tower before leaving its footprint (spec §4, 'Disparo').

For every yaw (1 degree steps, 360) and pitch from pitch_min to pitch_max (1 degree), the bolt's
path is a segment from the muzzle to the 600 u cylinder around the tower. It must stay farther
than the projectile's collision radius from every triangle of the written torre.nif, every box of
the tower's walking collision and every vanilla piece's collision.

The pose is the native one (Plugin.cpp): CTRL_GIRO_360 local = Rz(yaw) * rest, CTRL_ELEVACION
local = Rx(-pitch) * rest; node positions, rest rotations and the ProjectileNode axis are read
from ballesta.nif, not assumed. Falsified with a synthetic 600 u corner post.
"""
import json, math, struct, sys, hashlib
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]
import nif_nodos, nif_fisica
import v11_layout as L

FOOTPRINT = 600.0
MESH = ROOT/'mod/meshes/AstraAsedio'

def node_matrices(nif):
    """name -> (parent name, 4x4 local) of every node of the NIF."""
    nodos = nif['nodos']; parent = {h: b for b, n in nodos.items() for h in n['hijos']}; out = {}
    for b, n in nodos.items():
        M = np.eye(4); M[:3, :3] = np.array(n['rot']).reshape(3, 3)*n['esc']; M[:3, 3] = n['tr']
        out[n['nombre']] = (nodos[parent[b]]['nombre'] if b in parent else None, M)
    return out

def rz(a):
    c, s = math.cos(a), math.sin(a); M = np.eye(4); M[:2, :2] = [[c, -s], [s, c]]; return M
def rx(a):
    c, s = math.cos(a), math.sin(a); M = np.eye(4); M[1:3, 1:3] = [[c, -s], [s, c]]; return M

class Aim:
    def __init__(self, cfg):
        nodes = node_matrices(nif_nodos.leer(str(MESH/'ballesta.nif')))
        self.nodes = nodes; self.root = np.eye(4); self.root[2, 3] = cfg['tower_top_units']
        chain = []; name = 'ProjectileNode'
        while name is not None: chain.append(name); name = nodes[name][0]
        self.chain = list(reversed(chain))
        assert 'CTRL_GIRO_360' in self.chain and 'CTRL_ELEVACION' in self.chain, self.chain
    def pose(self, yaw_deg, pitch_deg):
        M = self.root.copy()
        for name in self.chain:
            local = self.nodes[name][1].copy()
            if name == 'CTRL_GIRO_360':
                local[:3, :3] = rz(math.radians(yaw_deg))[:3, :3] @ local[:3, :3]
            elif name == 'CTRL_ELEVACION':
                local[:3, :3] = rx(-math.radians(pitch_deg))[:3, :3] @ local[:3, :3]
            M = M @ local
        muzzle = M[:3, 3]; bore = M[:3, :3] @ np.array([0.0, 1.0, 0.0])
        return muzzle, bore/np.linalg.norm(bore)

def nif_triangles(path):
    """World triangles of every BSTriShape of a written NIF (vertices are full-precision floats in SSE)."""
    nif = nif_nodos.leer(str(path)); d = nif['datos']; mundo_padre = nif_fisica._mundo_padre(nif); tris = []
    for i, _n, o, local, _sh, _a, desc, nv, datos in nif_fisica._shapes(nif):
        nt = struct.unpack_from('<H', d, datos - 8)[0]
        m = np.array(nif_fisica._mul(mundo_padre(i), local)); stride = (desc & 0xF)*4
        V = np.array([struct.unpack_from('<3f', d, datos + k*stride) for k in range(nv)])
        V = V @ m[:, :3].T + m[:, 3]
        T = np.array([struct.unpack_from('<3H', d, datos + nv*stride + 6*k) for k in range(nt)])
        tris.append(V[T])
    return np.concatenate(tris) if tris else np.zeros((0, 3, 3))

def box_triangles(lo, hi):
    c = np.array([[lo[0], lo[1], lo[2]], [hi[0], lo[1], lo[2]], [hi[0], hi[1], lo[2]], [lo[0], hi[1], lo[2]],
                  [lo[0], lo[1], hi[2]], [hi[0], lo[1], hi[2]], [hi[0], hi[1], hi[2]], [lo[0], hi[1], hi[2]]])
    q = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return np.array([[c[a], c[b], c[cc]] for a, b, cc, dd in q for (a, b, cc) in ((a, b, cc), (a, cc, dd))])

def collision_triangles(cfg):
    """The tower's walking collision as written by build_tower_v11.py (boxes, floors, stair barriers)."""
    data = json.loads((ROOT/'reports/collision_walkable.json').read_text()); tris = []
    for b in data['solid_boxes_units'] + data['floors_units'] + data['stair_edge_barriers_units']:
        tris.append(box_triangles(b['min'], b['max']))
    return np.concatenate(tris)

def vanilla_triangles(cfg):
    tris = [np.array(t) for p in cfg['tower_v11']['pieces'] for s in L.piece_solids(p, cfg) for t in L.solid_triangles(s)]
    return np.array(tris)

def seg_seg(p0, p1, q0, q1):
    """Distance between segment p (one) and segments q (arrays)."""
    d1 = p1 - p0; d2 = q1 - q0; r = p0 - q0
    a = d1 @ d1; e = np.einsum('ij,ij->i', d2, d2); f = np.einsum('ij,ij->i', d2, r); c = r @ d1
    b = d2 @ d1; den = a*e - b*b
    s = np.where(den > 1e-12, np.clip((b*f - c*e)/np.where(den > 1e-12, den, 1), 0, 1), 0.0)
    t = np.where(e > 1e-12, (b*s + f)/np.where(e > 1e-12, e, 1), 0.0)
    s = np.where(t < 0, np.clip(-c/a, 0, 1), np.where(t > 1, np.clip((b - c)/a, 0, 1), s)); t = np.clip(t, 0, 1)
    return np.linalg.norm((p0 + s[:, None]*d1) - (q0 + t[:, None]*d2), axis=1)

def point_tri(p, A, B, C):
    """Distance from one point to triangles (inside the face: plane distance; outside: edges)."""
    n = np.cross(B - A, C - A); nn = np.linalg.norm(n, axis=1); ok = nn > 1e-12; n = n/np.where(ok, nn, 1)[:, None]
    dist = np.einsum('ij,ij->i', p - A, n); proj = p - dist[:, None]*n
    def edge(u, v, w): return np.einsum('ij,ij->i', np.cross(v - u, proj - u), n) >= -1e-9
    inside = ok & edge(A, B, C) & edge(B, C, A) & edge(C, A, B)
    seg = lambda u, v: np.linalg.norm(p - (u + np.clip(np.einsum('ij,ij->i', p - u, v - u)/np.maximum(np.einsum('ij,ij->i', v - u, v - u), 1e-12), 0, 1)[:, None]*(v - u)), axis=1)
    return np.where(inside, np.abs(dist), np.minimum(np.minimum(seg(A, B), seg(B, C)), seg(C, A)))

def seg_tri(p0, p1, T):
    """Distance between one segment and triangles T (n,3,3); 0 when the segment crosses a triangle."""
    A, B, C = T[:, 0], T[:, 1], T[:, 2]
    d = np.minimum.reduce([seg_seg(p0, p1, A, B), seg_seg(p0, p1, B, C), seg_seg(p0, p1, C, A), point_tri(p0, A, B, C), point_tri(p1, A, B, C)])
    # Moller-Trumbore crossing
    e1, e2 = B - A, C - A; dirv = p1 - p0; h = np.cross(np.broadcast_to(dirv, e2.shape), e2); a = np.einsum('ij,ij->i', e1, h)
    ok = np.abs(a) > 1e-12; f = 1/np.where(ok, a, 1); s = p0 - A; u = f*np.einsum('ij,ij->i', s, h)
    q = np.cross(s, e1); v = f*(q @ dirv); t = f*np.einsum('ij,ij->i', e2, q)
    cross = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t >= 0) & (t <= 1)
    return np.where(cross, 0.0, d)

def azimuth_bins(T, margin_deg):
    """For each integer degree, the triangles whose azimuth span (seen from the tower axis) reaches it."""
    ang = np.degrees(np.arctan2(T[:, :, 1], T[:, :, 0]))
    bins = [[] for _ in range(360)]
    r = np.linalg.norm(T[:, :, :2], axis=2).min(axis=1)
    for k in range(len(T)):
        a = np.sort(ang[k]); span = max(a[1] - a[0], a[2] - a[1], 360 - (a[2] - a[0]))
        # Smallest arc covering the three azimuths; near the axis every direction counts.
        if r[k] < 30: rng_ = range(360)
        else:
            gaps = [(a[1] - a[0], a[0], a[1]), (a[2] - a[1], a[1], a[2]), (360 - (a[2] - a[0]), a[2], a[0] + 360)]
            g, lo, hi = max(gaps)                       # the arc not covered is the largest gap
            start, end = hi, lo + 360
            rng_ = range(int(math.floor(start - margin_deg)), int(math.ceil(end + margin_deg)) + 1)
        for deg in rng_: bins[deg % 360].append(k)
    return [np.array(sorted(set(b)), dtype=int) for b in bins]

def run(cfg, extra=None, yaws=range(360)):
    aim = Aim(cfg)
    radius = json.loads((ROOT/'reports/plugin_build.json').read_text())['siege']['projectile_collision_radius']
    groups = {'torre_visual': nif_triangles(MESH/'torre.nif'), 'torre_colision': collision_triangles(cfg), 'vanilla': vanilla_triangles(cfg)}
    if extra is not None: groups['falsificacion'] = extra
    pitches = range(int(cfg['pitch_min']), int(cfg['pitch_max']) + 1)
    # The lowest any shot gets inside the footprint: geometry below it cannot be reached.
    floor = math.inf; shots = {}
    for yaw in yaws:
        for pitch in pitches:
            m, b = aim.pose(yaw, pitch); h = np.linalg.norm(b[:2])
            # Leave the footprint: the horizontal distance from the axis reaches FOOTPRINT.
            r0 = np.linalg.norm(m[:2]); length = (FOOTPRINT - r0)/h if h > 1e-6 else FOOTPRINT
            end = m + b*max(length, 0.0); shots[(yaw, pitch)] = (m, end); floor = min(floor, m[2], end[2])
    worst = {'clearance': math.inf}; hits = []; tested = 0
    for gname, T in groups.items():
        keep = T[:, :, 2].max(axis=1) >= floor - radius - 1.0; T = T[keep]
        if not len(T): continue
        bins = azimuth_bins(T, 6.0)
        for (yaw, pitch), (p0, p1) in shots.items():
            az = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0])) if np.linalg.norm(p1[:2] - p0[:2]) > 1e-6 else None
            idx = np.arange(len(T)) if az is None else bins[int(round(az)) % 360]
            if not len(idx): continue
            d = seg_tri(p0, p1, T[idx]); tested += len(idx); k = int(np.argmin(d))
            if d[k] < worst['clearance']:
                worst = {'clearance': float(d[k]), 'yaw': yaw, 'pitch': pitch, 'group': gname, 'triangle': T[idx][k].round(2).tolist()}
            if d[k] <= radius: hits.append({'yaw': yaw, 'pitch': pitch, 'group': gname, 'clearance': float(d[k])})
    return {'radius': radius, 'shots': len(shots), 'floor_z': floor, 'pairs_tested': tested, 'hits': hits, 'worst': worst,
            'triangles': {k: int(len(v)) for k, v in groups.items()}}

def main():
    cfg = L.load_cfg()
    result = run(cfg)
    # Falsification: a 600 u post at the south-east corner must be hit by the low shots towards it.
    # The bore points along -Y of the yaw node, so a shot's azimuth is yaw - 90 degrees.
    post = box_triangles((266.0, -280.0, 453.95), (280.0, -266.0, 1053.95))
    yaw_c = int(round(math.degrees(math.atan2(-273.0, 273.0)) + 90.0)) % 360
    fake = run(cfg, extra=post, yaws=range(yaw_c - 5, yaw_c + 6))
    falsified = any(h['group'] == 'falsificacion' for h in fake['hits'])
    highest = {k: float(v[:, :, 2].max()) for k, v in (('torre_visual', nif_triangles(MESH/'torre.nif')), ('vanilla', vanilla_triangles(cfg)))}
    inputs = {n: hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in
              ('mod/meshes/AstraAsedio/torre.nif', 'mod/meshes/AstraAsedio/ballesta.nif', 'reports/collision_walkable.json', 'config.json', 'scripts/verify_shot_clearance.py')}
    report = {'ok': not result['hits'] and falsified, 'hits': len(result['hits']), 'first_hits': result['hits'][:10],
              'worst': result['worst'], 'projectile_radius': result['radius'], 'shots': result['shots'], 'footprint_units': FOOTPRINT,
              'pitch_range': [cfg['pitch_min'], cfg['pitch_max']], 'lowest_shot_z': result['floor_z'], 'highest_geometry_z': highest,
              'vertical_margin_units': result['floor_z'] - max(highest.values()), 'pairs_tested': result['pairs_tested'],
              'triangles': result['triangles'], 'falsified': falsified, 'falsification_hits': len(fake['hits']), 'inputs_sha256': inputs}
    (ROOT/'reports/shot_clearance_v11.json').write_text(json.dumps(report, indent=2))
    print('SHOT_CLEARANCE', 'ok' if report['ok'] else 'FAIL', 'hits', report['hits'], 'worst %.1f u at yaw %s pitch %s (%s)' %
          (result['worst']['clearance'], result['worst'].get('yaw'), result['worst'].get('pitch'), result['worst'].get('group')), 'falsified', falsified)
    return 0 if report['ok'] else 1

if __name__ == '__main__': sys.exit(main())
