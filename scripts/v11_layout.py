"""Single transform shared by the ESP writer and every Blender verifier (v11).

Vanilla meshes are read from config.extracted into memory only. Nothing here writes vanilla
geometry to disk (spec §4, compliance).
"""
import itertools, json, math, struct, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
for _p in (ROOT/'scripts', ROOT/'scripts/vendor'):
    if str(_p) not in sys.path: sys.path.insert(0, str(_p))

def load_cfg():
    return json.loads((ROOT/'config.json').read_text(encoding='utf-8'))

def esm_path(cfg, name='Skyrim.esm'):
    return Path(cfg['runtime'])/'Data'/name

def zstr(b): return b.rstrip(b'\0').decode('cp1252', 'replace')

def mesh_vertices(model, cfg=None):
    """Visual vertices of a vanilla mesh (path relative to meshes/), in the NIF frame, as a numpy array."""
    import numpy as np, nif_nodos, nif_fisica
    cfg = cfg or load_cfg()
    nif = nif_nodos.leer(str(Path(cfg['extracted'])/'meshes'/model))
    d = nif['datos']; mundo_padre = nif_fisica._mundo_padre(nif); pts = []
    for i, _n, _o, local, _shader, _a, desc, nv, datos in nif_fisica._shapes(nif):
        if not nv: continue
        # Measured on stockadewoodbeam01.nif: SSE BSTriShape positions are 3 floats even without
        # the FULLPREC descriptor flag (flags 0x3b); reading half floats gives NaN.
        m = nif_fisica._mul(mundo_padre(i), local); paso = (desc & 0xF)*4
        pts += [nif_fisica._aplicar(m, struct.unpack_from('<3f', d, datos + k*paso)) for k in range(nv)]
    if not pts: raise ValueError('no geometry: %s' % model)
    return np.array(pts)

def nif_triangles(path):
    """(vertices, triangles) of every BSTriShape of a NIF file, in its frame (memory only)."""
    import numpy as np, nif_nodos, nif_fisica
    nif = nif_nodos.leer(str(path)); d = nif['datos']; mundo_padre = nif_fisica._mundo_padre(nif)
    verts, tris = [], []
    for i, _n, _o, local, _shader, _a, desc, nv, datos in nif_fisica._shapes(nif):
        if not nv: continue
        nt = struct.unpack_from('<H', d, datos - 8)[0]          # BSTriShape: triangle count, vertex count, data size
        m = nif_fisica._mul(mundo_padre(i), local); paso = (desc & 0xF)*4; base = len(verts)
        verts += [nif_fisica._aplicar(m, struct.unpack_from('<3f', d, datos + k*paso)) for k in range(nv)]
        tris += [tuple(base + j for j in struct.unpack_from('<3H', d, datos + nv*paso + 6*k)) for k in range(nt)]
    return np.array(verts), np.array(tris, dtype=int)

def door_swing(cfg=None, door=None):
    """How the room door turns, all read rather than assumed.

    pivot_local: the hinge node Door01 of its NIF; key_range_deg: the Z keys of its NiTransformData
    (Open/Close); local_sign: +1 when an XYZ euler key a turns points by +a in standard math, the
    reading probe_key_rotation.py decided from vanilla furniture (reports/key_rotation_convention.json);
    opens_local: the side of the door frame the free end of the leaf swings to.
    """
    import nif_nodos
    cfg = cfg or load_cfg(); door = door or next(p for p in cfg['tower_v11']['pieces'] if p['role'] == 'puerta')
    nif = nif_nodos.leer(str(Path(cfg['extracted'])/'meshes'/door['modl'])); d = nif['datos']
    pivot = next(n['tr'] for n in nif['nodos'].values() if n['nombre'] == 'Door01')
    angles = []
    for t, o, _s in nif['bloques']:
        if t != 'NiTransformData': continue
        p = o; nr, = struct.unpack_from('<I', d, p); p += 4
        if not nr: continue
        kt, = struct.unpack_from('<I', d, p); p += 4
        if kt != 4: raise ValueError('door rotation keys are not XYZ euler keys')
        for axis in range(3):
            nk, = struct.unpack_from('<I', d, p); p += 4
            if not nk: continue
            it, = struct.unpack_from('<I', d, p); p += 4; size = {1: 8, 2: 16, 3: 20}.get(it, 8)
            for _k in range(nk):
                _time, value = struct.unpack_from('<2f', d, p); p += size
                if axis == 2: angles.append(math.degrees(value))
    conv = json.loads((ROOT/'reports/key_rotation_convention.json').read_text(encoding='utf-8'))
    if conv.get('decided') not in ('H1_clockwise', 'H2_counterclockwise'): raise RuntimeError('key rotation convention not decided')
    sign = 1.0 if conv['decided'] == 'H2_counterclockwise' else -1.0
    extreme = max(angles, key=abs); a = math.radians(sign*extreme)
    # The leaf runs from the hinge towards local -X; where does its free end go at the extreme key?
    free_end_y = -math.sin(a)
    return {'pivot_local': tuple(pivot), 'key_range_deg': (min(angles), max(angles)), 'local_sign': sign,
            'opens_local': (0.0, 1.0 if free_end_y > 0 else -1.0, 0.0), 'convention': conv['decided']}

def piece_mesh(piece, cfg=None):
    """World (vertices, triangles) of a vanilla piece's visual mesh in its layout place (memory only)."""
    import numpy as np
    cfg = cfg or load_cfg()
    V, T = nif_triangles(Path(cfg['extracted'])/'meshes'/piece['modl'])
    m = piece_matrix(piece)
    return V @ (np.array(m['r'])*m['s']).T + np.array(m['t']), T

def _rot(axis, rad):
    c, s = math.cos(rad), math.sin(rad)
    return {'X': [[1,0,0],[0,c,-s],[0,s,c]],
            'Y': [[c,0,s],[0,1,0],[-s,0,c]],
            'Z': [[c,-s,0],[s,c,0],[0,0,1]]}[axis]

def _mul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

def transform_matrix(pos, rot_deg, scale, order, signs):
    """order: application order of the axes, e.g. 'XYZ' = X first. signs: +1/-1 per axis X,Y,Z."""
    r = [[1,0,0],[0,1,0],[0,0,1]]
    idx = {'X':0,'Y':1,'Z':2}
    for ax in order:
        r = _mul(_rot(ax, signs[idx[ax]]*math.radians(rot_deg[idx[ax]])), r)
    return {'r': r, 't': tuple(pos), 's': scale}

def apply(m, p):
    r, s, t = m['r'], m['s'], m['t']
    return tuple(sum(r[i][j]*p[j]*s for j in range(3)) + t[i] for i in range(3))

def all_conventions():
    return [(''.join(o), sg) for o in itertools.permutations('XYZ')
            for sg in itertools.product((1,-1), repeat=3)]

def engine_convention():
    """Read the convention proven by probe_angle_convention.py; refuse to guess."""
    data = json.loads((ROOT/'reports/angle_convention.json').read_text(encoding='utf-8'))
    if data.get('decided'): return data['order'], tuple(data['signs'])
    if data.get('fallback') == 'z_only': return 'XYZ', (1, 1, 1)  # valid only with rotX = rotY = 0
    raise RuntimeError('angle convention not decided')

def piece_matrix(piece):
    order, signs = engine_convention()
    return transform_matrix(piece['pos'], piece['rot_deg'], piece.get('scale', 1.0), order, signs)

def euler_from_matrix(R):
    """REFR DATA angles (degrees) that make the engine build rotation R (column vectors)."""
    order, signs = engine_convention()
    if order == 'ZYX':  # R = Rx(sx*x)·Ry(sy*y)·Rz(sz*z)
        b = math.asin(max(-1.0, min(1.0, R[0][2])))
        if abs(math.cos(b)) < 1e-9:  # gimbal lock: only a -/+ c is defined; take c = 0
            b = math.copysign(math.pi/2, R[0][2]); c = 0.0; a = math.atan2(R[2][1], R[1][1])
        else:
            a = math.atan2(-R[1][2], R[2][2]); c = math.atan2(-R[0][1], R[0][0])
        return tuple(math.degrees(v)*s for v, s in zip((a, b, c), signs))
    if all(abs(R[i][j] - (1.0 if i == j else 0.0)) < 1e-9 for i, j in ((2,2),(0,2),(1,2),(2,0),(2,1))):
        return (0.0, 0.0, math.degrees(math.atan2(R[1][0], R[0][0]))*signs[2])  # z-only fallback
    raise ValueError('convention %s %s only supports rotations about Z' % (order, signs))

def _cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def _unit(a):
    n = math.sqrt(sum(v*v for v in a)); return tuple(v/n for v in a)

def rot_for_axes(long_dir, side_dir):
    """Angles that send the mesh's local +Y to long_dir and local +X towards side_dir."""
    y = _unit(long_dir)
    x = _unit(tuple(s - sum(p*q for p, q in zip(side_dir, y))*v for s, v in zip(side_dir, y)))
    z = _cross(x, y)
    return euler_from_matrix([[x[i], y[i], z[i]] for i in range(3)])

ROLES = ('pilote', 'cruz', 'viga', 'pared', 'techo', 'puerta')

# --- Vanilla collision as convex solids (plan task 5) ----------------------------------------
# A solid is a convex polytope {x : n_i·x <= h_i} in game units. Every shape is turned into one
# that contains it (sharp edges instead of Havok's rounded convex radius): conservative for
# clearance checks. Read in memory only; never written to v11.
HK = 69.99125           # game units per Havok unit (nif_fisica.HK)
CAPSULE_SIDES = 16
_I3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]

def _dot(a, b): return sum(p*q for p, q in zip(a, b))

def _solid(normals, offsets):
    return {'normals': [[float(c) for c in n] for n in normals], 'offsets': [float(h) for h in offsets]}

def capsule_solid(a, b, r, sides=CAPSULE_SIDES):
    """Prism of planes tangent to the capsule a-b of radius r, capped r beyond each end."""
    d = _unit(tuple(q - p for p, q in zip(a, b)))
    e1 = _unit(_cross(d, (1.0, 0.0, 0.0) if abs(d[0]) < 0.9 else (0.0, 1.0, 0.0))); e2 = _cross(d, e1)
    normals, offsets = [], []
    for k in range(sides):
        t = 2*math.pi*k/sides; n = tuple(math.cos(t)*e1[i] + math.sin(t)*e2[i] for i in range(3))
        normals.append(n); offsets.append(_dot(n, a) + r)
    normals += [d, tuple(-v for v in d)]; offsets += [_dot(d, b) + r, -_dot(d, a) + r]
    return _solid(normals, offsets)

def _trs(rows):
    """(R, s, t) of a 3x4 matrix whose 3x3 part is a rotation times a uniform scale."""
    s = math.sqrt(sum(rows[r][0]**2 for r in range(3)))
    return ([[rows[r][c]/s for c in range(3)] for r in range(3)], s, [rows[r][3] for r in range(3)])

def _compose(A, B):
    """A after B, both (R, s, t)."""
    (Ra, sa, ta), (Rb, sb, tb) = A, B
    R = [[sum(Ra[i][k]*Rb[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return (R, sa*sb, [sa*sum(Ra[i][k]*tb[k] for k in range(3)) + ta[i] for i in range(3)])

def transform_solid(T, solid):
    R, s, t = T; normals, offsets = [], []
    for n, h in zip(solid['normals'], solid['offsets']):
        n2 = [sum(R[i][k]*n[k] for k in range(3)) for i in range(3)]
        normals.append(n2); offsets.append(s*h + _dot(n2, t))
    return _solid(normals, offsets)

_MODEL_SOLIDS = {}

def collision_solids(model, cfg=None):
    """Collision of a vanilla mesh (path under meshes/) as solids in its NIF frame; fails closed."""
    import nif_nodos, nif_fisica
    if model in _MODEL_SOLIDS: return _MODEL_SOLIDS[model]
    cfg = cfg or load_cfg()
    nif = nif_nodos.leer(str(Path(cfg['extracted'])/'meshes'/model)); d, bloques = nif['datos'], nif['bloques']
    out = []
    for i, (t, o, _size) in enumerate(bloques):
        if not t.startswith('bhkRigidBody'): continue
        shape, = struct.unpack_from('<i', d, o)
        st, so, _ss = bloques[shape]
        node = _trs(nif_fisica.mundo_del_cuerpo(nif, i))
        body = (_I3, 1.0, [0.0, 0.0, 0.0])
        if t == 'bhkRigidBodyT':
            # Only the T body places its shape with its own pose. A plain bhkRigidBody stores the
            # node's pose there (FarmhouseAnimDoor01: body at 48,4,88 = node Door01); adding it
            # would move the door collision twice.
            tr = struct.unpack_from('<3f', d, o + 52); ax = nif_fisica._ejes(struct.unpack_from('<4f', d, o + 68))
            body = ([[ax[c][r] for c in range(3)] for r in range(3)], 1.0, list(tr))
        T = _compose(node, _compose((_I3, HK, [0.0, 0.0, 0.0]), body))
        _material, radius = struct.unpack_from('<If', d, so)
        if st == 'bhkBoxShape':
            semi = struct.unpack_from('<3f', d, so + 16)
            normals = [tuple(sg*(1.0 if j == k else 0.0) for j in range(3)) for k in range(3) for sg in (1, -1)]
            solid = _solid(normals, [semi[k] + radius for k in range(3) for _sg in (1, -1)])
        elif st == 'bhkCapsuleShape':
            solid = capsule_solid(struct.unpack_from('<3f', d, so + 16), struct.unpack_from('<3f', d, so + 32), radius)
        elif st == 'bhkConvexVerticesShape':
            nv, = struct.unpack_from('<I', d, so + 32)
            verts = [struct.unpack_from('<3f', d, so + 36 + 16*k) for k in range(nv)]
            p = so + 36 + 16*nv; nn, = struct.unpack_from('<I', d, p)
            normals = [_unit(struct.unpack_from('<3f', d, p + 4 + 16*k)) for k in range(nn)]
            # The stored planes sit 0.035-0.05 Havok units outside the vertices; rebuild each one at
            # exactly the convex radius from the hull so the solid always contains the real shape.
            solid = _solid(normals, [max(_dot(n, v) for v in verts) + radius for n in normals])
        else:
            raise ValueError('%s: unsupported collision shape %s' % (model, st))
        out.append(transform_solid(T, solid))
    if not out: raise ValueError('%s: no collision' % model)
    _MODEL_SOLIDS[model] = out
    return out

def piece_solids(piece, cfg=None):
    m = piece_matrix(piece)
    return [transform_solid((m['r'], m['s'], list(m['t'])), s) for s in collision_solids(piece['modl'], cfg)]

def solid_vertices(solid):
    """Corners of the polytope (every feasible intersection of three planes)."""
    import numpy as np
    N = np.array(solid['normals']); H = np.array(solid['offsets']); n = len(N)
    tol = 1e-6*max(1.0, float(np.abs(H).max()))
    idx = np.array([(i, j, k) for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n)])
    A = N[idx]; ok = np.abs(np.linalg.det(A)) > 1e-9
    X = np.linalg.solve(A[ok], H[idx[ok]][..., None])[..., 0]
    X = X[(X @ N.T <= H + tol).all(axis=1)]
    out = []
    for p in X:
        if not any(abs(p[0]-q[0]) < 1e-4 and abs(p[1]-q[1]) < 1e-4 and abs(p[2]-q[2]) < 1e-4 for q in out): out.append(tuple(float(c) for c in p))
    return out

def solid_triangles(solid):
    """Closed outward-facing triangle surface of the polytope."""
    verts = solid_vertices(solid); tris = []
    tol = 1e-6*max(1.0, max(abs(h) for h in solid['offsets']))
    for n, h in zip(solid['normals'], solid['offsets']):
        face = [v for v in verts if abs(_dot(n, v) - h) <= max(tol, 1e-5)]
        if len(face) < 3: continue
        c = [sum(v[i] for v in face)/len(face) for i in range(3)]
        e1 = _unit(tuple(face[0][i] - c[i] for i in range(3))); e2 = _cross(n, e1)
        face.sort(key=lambda v: math.atan2(_dot(e2, [v[i] - c[i] for i in range(3)]), _dot(e1, [v[i] - c[i] for i in range(3)])))
        tris += [(face[0], face[k], face[k + 1]) for k in range(1, len(face) - 1)]
    return tris

def band_box(solid, z0, z1):
    """Axis-aligned box of the part of the solid between heights z0 and z1, or None."""
    cut = _solid(solid['normals'] + [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]], solid['offsets'] + [z1, -z0])
    vs = solid_vertices(cut)
    if not vs: return None
    return {'min': [min(v[i] for v in vs) for i in range(3)], 'max': [max(v[i] for v in vs) for i in range(3)]}

def band_boxes(pieces, z0=0.0, z1=128.0, cfg=None):
    """Navmesh obstacles: what each vanilla piece occupies where an actor walks (spec §3)."""
    out = []
    for piece in pieces:
        for solid in piece_solids(piece, cfg):
            b = band_box(solid, z0, z1)
            if b: out.append(dict(b, name=piece['name']))
    return out

def _norm_model(m):
    m = m.replace('/', '\\').lower()
    return m[len('meshes\\'):] if m.startswith('meshes\\') else m

def esm_index(cfg, types=('STAT', 'DOOR')):
    """EDID -> base object data, reading only the top-level groups of the given record types."""
    from parser_esm import Plugin
    esm = Plugin(str(esm_path(cfg))); d = esm.d; out = {}
    p = esm.inicio_datos
    while p < len(d):
        size, = struct.unpack_from('<I', d, p + 4); label = d[p+8:p+12].decode('ascii', 'replace')
        if d[p:p+4] != b'GRUP': raise ValueError('unexpected top-level record at %d' % p)
        if label in types:
            for tipo, o, _t, _prof in esm.recorrer(p + 24, p + size):
                if tipo != label: continue
                ss = esm.subrecords(esm.datos(o)); sd = dict(ss)
                edid = zstr(sd.get('EDID', b''))
                if not edid: continue
                dnam = sd.get('DNAM', b'')
                material = struct.unpack_from('<I', dnam, 4)[0] if label == 'STAT' and len(dnam) >= 8 else 0
                out[edid.lower()] = {'edid': edid, 'type': label, 'formid': esm.form_id(o),
                                     'modl': _norm_model(zstr(sd.get('MODL', b''))),
                                     'obnd': list(struct.unpack('<6h', sd['OBND'])) if 'OBND' in sd else None,
                                     'has_snow_material': material != 0,
                                     'alternate_textures': any(k == 'MODS' for k, _v in ss)}
        p += size
    return out

def resolve_pieces(cfg, index=None):
    """Layout pieces with their Skyrim.esm base object; fails closed on any mismatch (spec §1)."""
    layout = cfg['tower_v11']; index = index or esm_index(cfg)
    fallback = json.loads((ROOT/'reports/angle_convention.json').read_text(encoding='utf-8')).get('decided') is not True
    names = set(); out = []
    for piece in layout['pieces']:
        name, edid = piece['name'], piece['edid']
        if name in names: raise ValueError('duplicate piece name: %s' % name)
        names.add(name)
        if piece['role'] not in ROLES: raise ValueError('%s: unknown role %r' % (name, piece['role']))
        base = index.get(edid.lower())
        if base is None: raise ValueError('%s: EDID %s not in Skyrim.esm' % (name, edid))
        if base['modl'] != _norm_model(piece['modl']):
            raise ValueError('%s: MODL of %s is %s, layout says %s' % (name, edid, base['modl'], piece['modl']))
        low = edid.lower()
        if 'snow' in low or low.endswith('_sn') or base['has_snow_material'] or base['alternate_textures']:
            raise ValueError('%s: %s is a snow/alternate-texture variant' % (name, edid))
        if (piece['role'] == 'puerta') != (base['type'] == 'DOOR'):
            raise ValueError('%s: role %s does not match record type %s' % (name, piece['role'], base['type']))
        if fallback and any(abs(a) > 1e-9 for a in piece['rot_deg'][:2]):
            raise ValueError('%s: X/Y rotation needs a decided angle convention' % name)
        out.append(dict(piece, formid=base['formid'], type=base['type'], has_snow_material=base['has_snow_material']))
    for piece in out:
        for other in piece.get('joins', []):
            if other not in names: raise ValueError('%s joins unknown piece %s' % (piece['name'], other))
    return out
