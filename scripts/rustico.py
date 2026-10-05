"""Hand-built irregularity for the tower's visual pieces (Blender).

Skyrim's wooden structures are never square: logs stick out by different
lengths, posts lean, rails sag and planks sit unevenly. This pass moves
vertices of the visual meshes only. It runs after the collision boxes are
measured, so the Havok shapes, the walkable route and the navmesh do not move.
Deterministic: every offset is seeded by the object name.
"""
import math, random, zlib
import bmesh
from mathutils import Vector, Matrix

# name fragment -> (perpendicular jitter per end m, along-axis jitter per end m,
#                   spin about the long axis deg, whole-piece yaw deg, sag m, base end fixed)
# v09 (user, 2026-10-05: "más marcada"): roughly twice the v01 amplitudes, plus uneven
# log thickness. Walk surfaces keep the same vertical tope; collision never moves.
REGLAS = [
    ('Tronco_',             (.025, .13,  180., 0.,  0.,   False)),  # logs: ends stick out unevenly, varied grain
    ('Parapeto_poste',      (.045, .07,  30.,  0.,  0.,   True)),   # rooftop posts lean ~2 deg, uneven tops
    ('Parapeto_travesa',    (.025, .04,  25.,  0.,  0.,   False)),
    ('Balaustre',           (.035, .06,  25.,  0.,  0.,   True)),
    ('Baranda',             (.030, .0,   0.,   0.,  .045, False)),  # handrails sag between posts
    ('Pilar',               (.050, .0,   20.,  0.,  0.,   True)),
    ('Jabalcon',            (.025, .0,   20.,  0.,  0.,   False)),
    ('Travesano',           (.022, .05,  25.,  0.,  0.,   False)),
    ('Zanca',               (.012, .0,   0.,   0.,  .022, False)),
    ('Viga',                (.020, .08,  20.,  0.,  .030, False)),
    ('Peldano',             (.015, .04,  0.,   3.0, 0.,   False)),  # treads not square to the stringers
    ('Tablon_azotea',       (.006, .06,  0.,   .6,  0.,   False)),
    ('Descanso_azotea',     (.006, .04,  0.,   1.0, 0.,   False)),
    ('Dintel',              (.015, .03,  15.,  0.,  0.,   False)),
    ('Marco_puerta',        (.010, .0,   0.,   0.,  0.,   True)),
    ('Puerta_tabla',        (.008, .02,  0.,   0.,  0.,   True)),
]
# Cross-section scale range per piece (logs are never the same thickness). Mostly growing,
# so stacked logs never open gaps between courses.
GROSOR = {'Tronco_': (.97, 1.10), 'Pilar': (.95, 1.08), 'Parapeto_poste': (.95, 1.08)}
SUBDIVIDIR = ('Baranda', 'Zanca', 'Viga')   # long pieces get loops so they can sag
CORTES = 6
# Vertical drift of walk surfaces stays below this, so feet never float above
# or sink below the unchanged collision (tread 0.15 m, plank 0.16 m thick).
TOPE_PISO_Z = .006


def regla(nombre):
    for frag, r in REGLAS:
        if frag in nombre:
            return frag, r
    return None, None


def _rng(nombre):
    return random.Random(zlib.crc32(nombre.encode('utf-8')))


def _eje_largo(o):
    """Long axis in world space, the centre and the half length."""
    M = o.matrix_world
    pts = [M @ v.co for v in o.data.vertices]
    c = sum(pts, Vector()) / len(pts)
    best = None
    for j in range(3):
        a = (M.to_3x3() @ Vector([1. if k == j else 0. for k in range(3)])).normalized()
        ts = [(p - c).dot(a) for p in pts]
        ext = max(ts) - min(ts)
        if best is None or ext > best[0]:
            best = (ext, a, min(ts), max(ts))
    _ext, a, t0, t1 = best
    return c, a, t0, t1


def _perp(a, rng, mag):
    ref = Vector((0, 0, 1)) if abs(a.z) < .9 else Vector((1, 0, 0))
    u = a.cross(ref).normalized(); w = a.cross(u).normalized()
    ang = rng.uniform(0, math.tau); r = rng.uniform(.35, 1.) * mag
    return (u * math.cos(ang) + w * math.sin(ang)) * r


def _subdividir(o):
    if o.data.users > 1:
        o.data = o.data.copy()
    _c, a, t0, t1 = _eje_largo(o)
    bm = bmesh.new(); bm.from_mesh(o.data)
    al = (o.matrix_world.inverted().to_3x3() @ a).normalized()
    largas = [e for e in bm.edges if abs((e.verts[1].co - e.verts[0].co).normalized().dot(al)) > .95]
    if largas:
        bmesh.ops.subdivide_edges(bm, edges=largas, cuts=CORTES, use_grid_fill=True)
    bm.to_mesh(o.data); bm.free(); o.data.update()


def envejecer(objetos):
    """Apply the irregularity pass. Returns a per-object report."""
    informe = {}
    for o in sorted(objetos, key=lambda x: x.name):
        frag, r = regla(o.name)
        if r is None or o.type != 'MESH':
            continue
        perp, largo, giro, yaw, sag, base_fija = r
        if any(k in o.name for k in SUBDIVIDIR):
            _subdividir(o)
        if o.data.users > 1:
            o.data = o.data.copy()
        rng = _rng(o.name)
        M = o.matrix_world.copy(); Mi = M.inverted()
        c, a, t0, t1 = _eje_largo(o)
        es_piso = frag in ('Peldano', 'Tablon_azotea', 'Descanso_azotea')
        # Posts: the bottom end is the lower one along world Z.
        bajo_en_t0 = (c + a * t0).z <= (c + a * t1).z
        ends = []
        for i in range(2):
            fijo = base_fija and ((i == 0) == bajo_en_t0)
            d = _perp(a, rng, perp * (.25 if fijo else 1.))
            dl = 0. if fijo else rng.uniform(-largo, largo)
            if es_piso:
                d.z = max(-TOPE_PISO_Z, min(TOPE_PISO_Z, d.z))
            ends.append((d, dl))
        spin = math.radians(rng.uniform(-giro, giro))
        rot = Matrix.Rotation(spin, 3, a)
        yaw_m = Matrix.Rotation(math.radians(rng.uniform(-yaw, yaw)), 3, 'Z')
        grosor = next((rng.uniform(*g) for k, g in GROSOR.items() if k in o.name), 1.0)
        mover = 0.
        vertical = 0.
        for v in o.data.vertices:
            p = M @ v.co
            t = (p - c).dot(a)
            s = 0. if t1 == t0 else (t - t0) / (t1 - t0)
            radial = (p - c) - a * t
            p_eje = p + radial * (grosor - 1.)           # uneven thickness about the long axis
            q = c + rot @ (p_eje - c)                   # spin about own axis
            q = c + yaw_m @ (q - c)                     # slight skew of flat pieces
            (d0, l0), (d1, l1) = ends
            q += d0 * (1 - s) + d1 * s                  # each end drifts: lean, crook
            q += a * (-l0 * (1 - s) + l1 * s)           # uneven lengths at both ends
            if sag:
                q.z -= sag * math.sin(math.pi * s)
            mover = max(mover, (q - p).length)
            vertical = max(vertical, abs(q.z - p.z))
            v.co = Mi @ q
        o.data.update()
        informe[o.name] = {'regla': frag, 'desplazamiento_max_m': round(mover, 4), 'grosor': round(grosor, 4),
                           'piso': es_piso, 'desplazamiento_vertical_max_m': vertical}
    return informe
