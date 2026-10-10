"""How does the engine turn an XYZ euler rotation key? Decided by vanilla furniture that can only open one way.

FarmhouseAnimDoor01's Open sequence turns its hinge node with an XYZ euler key of -95 degrees
about Z. Two readings are possible: Gamebryo's elementary rotations are clockwise for a positive
angle (H1: the key a turns a point by -a in standard right-handed math), or counter-clockwise (H2:
by +a). Vanilla placements of the door did not tell them apart (reports/door_swing.json). This
probe uses meshes whose moving part has one physical way out: wardrobe doors swing out of the
cabinet, chest lids lift off the box. Under each reading every animated node of the Open sequence
is turned through its keys, and its vertices are tested against the fixed part of the same mesh;
vertices that already touch it at rest are ignored. The reading that leaves them free is the
engine's. Meshes come from config.extracted, read in memory only.
"""
import collections, json, math, struct, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]
import nif_nodos, nif_fisica
import v11_layout as L

CFG = L.load_cfg()
MESHES = ('clutter/common/wardrobe01.nif', 'clutter/upperclass/upperwardrobe01.nif', 'clutter/containers/chest01/chest01.nif',
          'clutter/upperclass/upperchest01.nif', 'clutter/ruins/ruins_largechest.nif', 'clutter/ruins/ruins_smallchest.nif',
          'clutter/nightmother/nmcoffin01.nif', 'architecture/riften/interior/smallroomfirst/rifrmsmsecretcabinetdoor01.nif',
          'architecture/whiterun/wrclutter/wrburialurn01.nif', 'clutter/ruins/ruinslargeurnnostand01.nif', 'clutter/ruins/ruinslargeurnwithstand01.nif')
CONTACT = 0.5

def sequences(nif):
    """{sequence name: [(node name, NiTransformData block)]} from NiControllerSequence controlled blocks."""
    d, b, s = nif['datos'], nif['bloques'], nif['strings']; out = {}
    for t, o, _size in b:
        if t != 'NiControllerSequence': continue
        name, = struct.unpack_from('<i', d, o); count, = struct.unpack_from('<I', d, o + 4); p = o + 12; blocks = []
        for _ in range(count):
            interp, _ctrl = struct.unpack_from('<ii', d, p); node, = struct.unpack_from('<i', d, p + 9); p += 29
            if 0 <= interp < len(b) and b[interp][0] == 'NiTransformInterpolator':
                data, = struct.unpack_from('<i', d, b[interp][1] + 32)
                if 0 <= data < len(b) and b[data][0] == 'NiTransformData': blocks.append((s[node], data))
        out[s[name] if 0 <= name < len(s) else '?'] = blocks
    return out

def euler_keys(nif, block):
    """[(time, (x, y, z) degrees)] of an XYZ-key NiTransformData, or None if it uses quaternions."""
    d = nif['datos']; o = nif['bloques'][block][1]; nr, = struct.unpack_from('<I', d, o)
    if not nr: return None
    kt, = struct.unpack_from('<I', d, o + 4)
    if kt != 4: return None
    p = o + 8; axes = []
    for _axis in range(3):
        nk, = struct.unpack_from('<I', d, p); p += 4; keys = []
        if nk:
            it, = struct.unpack_from('<I', d, p); p += 4; size = {1: 8, 2: 16, 3: 20}.get(it, 8)
            for _k in range(nk):
                t, v = struct.unpack_from('<2f', d, p); p += size; keys.append((t, math.degrees(v)))
        axes.append(keys)
    times = sorted({t for keys in axes for t, _v in keys})
    def at(keys, t):
        if not keys: return 0.0
        if t <= keys[0][0]: return keys[0][1]
        for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
            if t0 <= t <= t1: return v0 + (v1 - v0)*(t - t0)/max(t1 - t0, 1e-9)
        return keys[-1][1]
    return [(t, tuple(at(axes[i], t) for i in range(3))) for t in times]

def rot(axis, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return {0: np.array([[1, 0, 0], [0, c, -s], [0, s, c]]), 1: np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]]),
            2: np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])}[axis]

def point_tri(p, A, B, C):
    n = np.cross(B - A, C - A); nn = np.linalg.norm(n, axis=1); ok = nn > 1e-9; n = n/np.where(ok, nn, 1)[:, None]
    d = np.einsum('pk,mk->pm', p, n) - np.einsum('mk,mk->m', A, n)[None, :]
    proj = p[:, None, :] - d[:, :, None]*n[None, :, :]
    def side(u, v): return np.einsum('pmk,mk->pm', np.cross((v - u)[None, :, :], proj - u[None, :, :]), n) >= -1e-9
    inside = ok[None, :] & side(A, B) & side(B, C) & side(C, A)
    def seg(u, v):
        e = v - u; t = np.clip(np.einsum('pmk,mk->pm', p[:, None, :] - u[None, :, :], e)/np.maximum(np.einsum('mk,mk->m', e, e), 1e-12)[None, :], 0, 1)
        return np.linalg.norm(p[:, None, :] - (u[None, :, :] + t[:, :, None]*e[None, :, :]), axis=2)
    return np.where(inside, np.abs(d), np.minimum(np.minimum(seg(A, B), seg(B, C)), seg(C, A)))

def analyse(rel):
    nif = nif_nodos.leer(str(Path(CFG['extracted'])/'meshes'/rel)); d = nif['datos']
    nodes = nif['nodos']; parent = {h: p for p, n in nodes.items() for h in n['hijos']}; byname = {n['nombre']: b for b, n in nodes.items()}
    mp = nif_fisica._mundo_padre(nif)
    def local(b): n = nodes[b]; return np.array(nif_fisica._local(n['tr'], n['rot'], n['esc']))
    shapes = []
    for i, name, _o, loc, _s, _a, desc, nv, datos in nif_fisica._shapes(nif):
        nt = struct.unpack_from('<H', d, datos - 8)[0]; paso = (desc & 0xF)*4
        V = np.array([struct.unpack_from('<3f', d, datos + k*paso) for k in range(nv)])
        T = np.array([struct.unpack_from('<3H', d, datos + nv*paso + 6*k) for k in range(nt)])
        chain = []; b = parent.get(i)
        while b is not None: chain.append(b); b = parent.get(b)
        shapes.append({'name': name, 'local': np.array(loc), 'V': V, 'T': T, 'chain': chain})
    seqs = sequences(nif); seq = seqs.get('Open') or next(iter(seqs.values()), [])
    animated = {}
    for node, block in seq:
        keys = euler_keys(nif, block)
        if keys and node in byname and max(max(abs(v) for v in k[1]) for k in keys) > 5: animated[byname[node]] = keys
    if not animated: return None
    def world_points(shape, pose):
        """Shape vertices in the root frame; animated nodes take the key rotation `pose` as their local rotation."""
        M = np.vstack([shape['local'], [0, 0, 0, 1]]); P = np.c_[shape['V'], np.ones(len(shape['V']))].T
        P = M @ P
        for b in shape['chain']:
            Lb = np.vstack([local(b), [0, 0, 0, 1]])
            if b in pose:
                Lb = Lb.copy(); Lb[:3, :3] = pose[b]*np.linalg.norm(Lb[:3, 0])
            P = Lb @ P
        return P[:3].T
    moving = [s for s in shapes if any(b in animated for b in s['chain'])]; fixed = [s for s in shapes if s not in moving]
    F = np.concatenate([world_points(s, {})[s['T']] for s in fixed]) if fixed else np.zeros((0, 3, 3))
    if not len(F): return None
    result = {}
    for reading, sign in (('H1_clockwise', -1.0), ('H2_counterclockwise', 1.0)):
        hits = 0; samples = 0
        rest = np.concatenate([world_points(s, {}) for s in moving])
        free = point_tri(rest, F[:, 0], F[:, 1], F[:, 2]).min(axis=1) > CONTACT + 1.0
        for k in range(1, 11):
            pose = {}
            for b, keys in animated.items():
                t0, t1 = keys[0][0], keys[-1][0]; t = t0 + (t1 - t0)*k/10
                ang = min(keys, key=lambda kv: abs(kv[0] - t))[1]
                R = np.eye(3)
                for axis in (0, 1, 2):            # X, Y, Z euler, each turned by sign*value
                    R = rot(axis, sign*ang[axis]) @ R
                pose[b] = R
            P = np.concatenate([world_points(s, pose) for s in moving])[free]
            if len(P): hits += int((point_tri(P, F[:, 0], F[:, 1], F[:, 2]).min(axis=1) < CONTACT).sum() > 0); samples += 1
        result[reading] = hits
    return {'mesh': rel, 'animated_nodes': [nodes[b]['nombre'] for b in animated],
            'key_extremes_deg': {nodes[b]['nombre']: [list(k[1]) for k in (keys[0], keys[-1])] for b, keys in animated.items()}, **result}

def main():
    rows = [r for r in (analyse(m) for m in MESHES) if r]
    votes = collections.Counter()
    for r in rows:
        if r['H1_clockwise'] < r['H2_counterclockwise']: votes['H1_clockwise'] += 1
        elif r['H2_counterclockwise'] < r['H1_clockwise']: votes['H2_counterclockwise'] += 1
        else: votes['tie'] += 1
    # A tie (both readings free, or both blocked) says nothing; only the two readings compete.
    other = {'H1_clockwise': 'H2_counterclockwise', 'H2_counterclockwise': 'H1_clockwise'}
    decided = next((k for k in other if votes[k] >= 3 and votes[other[k]] == 0), None)
    out = {'decided': decided, 'votes': dict(votes), 'rows': rows, 'contact_units': CONTACT,
           'meaning': 'H1: a key value a turns points by -a (Gamebryo elementary rotations clockwise, like the measured REFR angles); H2: by +a'}
    (ROOT/'reports/key_rotation_convention.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    for r in rows: print(r['mesh'], r['animated_nodes'], 'H1 hits', r['H1_clockwise'], 'H2 hits', r['H2_counterclockwise'], r['key_extremes_deg'])
    print('KEY_ROTATION', decided, dict(votes))
    return 0 if decided else 1

if __name__ == '__main__': sys.exit(main())
