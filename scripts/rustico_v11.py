"""Rustic primitives for the v11 tower: logs, planks and rope lashings (pure Python, no bpy).

Nothing in Skyrim is straight (the user, 2026-10-05). Every log bends along its axis, tapers,
has ridged bark and ends cut at an angle; every plank has its own width, end positions and a
slight twist; ropes sit on the log they wrap. Sizes are game units. Each primitive is
deterministic: the same name and seed give the same mesh (spec §2, irregularity parameters in
config.json -> tower_v11.irregularity). build_tower_v11.py turns the lists into Blender meshes.

Returned meshes: {'verts': [(x,y,z)], 'faces': [(i,j,k[,l])], 'uvs': [(a,b)] one per vertex,
'meta': {...}}. 'uvs' are parametric coordinates that the builder maps onto each texture's layout:
logs (fraction around, units along) and, on the end caps, a unit disc; planks (units across, units
along); ropes (fraction around the log, fraction around the rope). Logs also give 'rings', the
vertex indices of each cross-section (seam excluded), and 'cap_face_start', the first end-cap face.
"""
import math, random, zlib

def _rng(name, seed): return random.Random((int(seed)*1000003) ^ zlib.crc32(name.encode('utf-8')))
def _sub(a, b): return tuple(p - q for p, q in zip(a, b))
def _add(a, b): return tuple(p + q for p, q in zip(a, b))
def _mul(a, k): return tuple(p*k for p in a)
def _dot(a, b): return sum(p*q for p, q in zip(a, b))
def _cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def _unit(a):
    n = math.sqrt(_dot(a, a)); return tuple(p/n for p in a)

def frame(axis):
    """Two unit vectors perpendicular to the axis and to each other."""
    ax = _unit(axis)
    e1 = _unit(_cross(ax, (1.0, 0.0, 0.0) if abs(ax[0]) < 0.9 else (0.0, 1.0, 0.0)))
    return ax, e1, _cross(ax, e1)

def tronco(name, a, b, r0, seed, sides=9, bend=(0.011, 0.022), taper=(0.09, 0.19), cut=(2.0, 12.0),
           ridge=0.05, ring_step=36.0, bend_dir=None):
    """A log from a to b with nominal radius r0 at its thick end.

    bend_dir forces the crook into one direction (projected across the log, random sign): a joist
    or a stringer may bend sideways only, or it would leave its supports or hit the treads.
    """
    rng = _rng(name, seed)
    d = _sub(b, a); length = math.sqrt(_dot(d, d)); ax, e1, e2 = frame(d)
    bend_frac = rng.uniform(*bend); phi = rng.uniform(0, 2*math.pi)
    bdir = _add(_mul(e1, math.cos(phi)), _mul(e2, math.sin(phi)))
    if bend_dir is not None:     # same random draws either way: other logs keep their shapes
        side = _unit(_sub(bend_dir, _mul(ax, _dot(bend_dir, ax))))
        bdir = side if math.cos(phi) >= 0 else _mul(side, -1)
    tp = rng.uniform(*taper); thin_at_b = rng.random() < 0.5
    ridges = [1 + rng.uniform(-ridge, ridge) for _ in range(sides)]   # bark ridges run the whole log
    rot0 = rng.uniform(0, 2*math.pi)
    cuts = [rng.uniform(*cut), rng.uniform(*cut)]
    if abs(cuts[0] - cuts[1]) < 1.0: cuts[1] = cuts[0] + 1.0 if cuts[0] + 1.0 <= cut[1] else cuts[0] - 1.0
    cut_dirs = [rng.uniform(0, 2*math.pi), rng.uniform(0, 2*math.pi)]
    n = max(4, int(math.ceil(length/ring_step)))
    n += n % 2                    # a ring at mid length, where the bend peaks (an odd count measured 0.87 of it)
    verts, uvs, faces, rings = [], [], [], []
    for k in range(n + 1):
        t = k/n
        c = _add(_add(a, _mul(d, t)), _mul(bdir, bend_frac*length*math.sin(math.pi*t)))
        r = r0*(1 - tp*(t if thin_at_b else 1 - t))
        ring = []
        for j in range(sides + 1):                                   # last column repeats the first (UV seam)
            th = rot0 + 2*math.pi*(j % sides)/sides
            radial = _add(_mul(e1, math.cos(th)), _mul(e2, math.sin(th)))
            off = _mul(radial, r*ridges[j % sides])
            p = _add(c, off)
            if k in (0, n):                                          # end cut: tilt the end ring's plane
                e = 0 if k == 0 else 1
                cd = _add(_mul(e1, math.cos(cut_dirs[e])), _mul(e2, math.sin(cut_dirs[e])))
                p = _add(p, _mul(ax, math.tan(math.radians(cuts[e]))*_dot(off, cd)))
            if j < sides: ring.append(len(verts))
            verts.append(p); uvs.append((j/sides, length*t))
        rings.append(ring)
    row = sides + 1
    for k in range(n):
        for j in range(sides):
            i0 = k*row + j
            faces.append((i0, i0 + 1, i0 + 1 + row, i0 + row))
    cap_face_start = len(faces)
    for k, flip in ((0, True), (n, False)):                         # end caps, facing outwards
        ring = rings[k]; centre = tuple(sum(verts[i][q] for i in ring)/sides for q in range(3))
        ci = len(verts); verts.append(centre); uvs.append((0.5, 0.5))
        cap = []
        for j in range(sides):
            vi = len(verts); src = verts[ring[j]]; verts.append(src)
            th = 2*math.pi*j/sides; uvs.append((0.5 + 0.5*math.cos(th), 0.5 + 0.5*math.sin(th))); cap.append(vi)
        for j in range(sides):
            f = (ci, cap[j], cap[(j + 1) % sides]); faces.append(tuple(reversed(f)) if flip else f)
    return {'verts': verts, 'faces': faces, 'uvs': uvs, 'rings': rings, 'cap_face_start': cap_face_start,
            'meta': {'a': tuple(a), 'b': tuple(b), 'length': length, 'bend_fraction': bend_frac,
                     'bend_vector': _mul(bdir, bend_frac*length), 'taper': tp, 'thin_end': 'b' if thin_at_b else 'a',
                     'cut_deg': cuts, 'radius_a': r0*(1 - (0 if thin_at_b else tp)), 'radius_b': r0*(1 - (tp if thin_at_b else 0)),
                     'ridge_max': max(ridges)}}

def axis_at(log, t):
    """Point of the bent log axis at fraction t (0 at a, 1 at b): where a rope must be centred."""
    m = log['meta']
    return _add(_add(m['a'], _mul(_sub(m['b'], m['a']), t)), _mul(m['bend_vector'], math.sin(math.pi*t)))

def radius_at(log, t):
    """Largest bark radius of the log at fraction t, across the straight a-b axis."""
    m = log['meta']; return (m['radius_a'] + (m['radius_b'] - m['radius_a'])*t)*m['ridge_max']

def tablon(name, center, axis, up, length, width, thickness, seed, width_var=0.15, end_shift=12.0,
           twist=1.2, cut=4.0, segments=4):
    """A plank whose top face is centred on `center`; it twists about its own top centre line."""
    rng = _rng(name, seed)
    ax = _unit(axis); upv = _unit(_sub(up, _mul(ax, _dot(up, ax)))); side = _cross(upv, ax)
    w = width*(1 + rng.uniform(-width_var, width_var))
    s0 = -length/2 + rng.uniform(-end_shift, end_shift); s1 = length/2 + rng.uniform(-end_shift, end_shift)
    tw = (rng.uniform(-twist, twist), rng.uniform(-twist, twist))
    cuts = (rng.uniform(-cut, cut), rng.uniform(-cut, cut))
    corners = ((-w/2, 0.0), (w/2, 0.0), (w/2, -thickness), (-w/2, -thickness))
    verts, uvs = [], []
    for k in range(segments + 1):
        f = k/segments; s = s0 + (s1 - s0)*f; th = math.radians(tw[0] + (tw[1] - tw[0])*f)
        for q, (x, z) in enumerate(corners):
            x2, z2 = x*math.cos(th) - z*math.sin(th), x*math.sin(th) + z*math.cos(th)
            sk = s
            if k in (0, segments): sk += math.tan(math.radians(cuts[0 if k == 0 else 1]))*x
            verts.append(_add(_add(center, _mul(ax, sk)), _add(_mul(side, x2), _mul(upv, z2))))
            uvs.append((x + w/2, sk - s0))
    faces = []
    for k in range(segments):
        b0, b1 = 4*k, 4*(k + 1)
        for q in range(4):
            faces.append((b0 + q, b0 + (q + 1) % 4, b1 + (q + 1) % 4, b1 + q))
    faces.append((3, 2, 1, 0)); last = 4*segments; faces.append((last, last + 1, last + 2, last + 3))
    # The top face rotates about its own centre line, so that line keeps the collision height.
    return {'verts': verts, 'faces': faces, 'uvs': uvs,
            'meta': {'width': w, 'ends': [s0, s1], 'twist_deg': list(tw), 'cut_deg': list(cuts), 'top_centre_deviation': 0.0}}

def amarre(name, center, axis, radius, seed, coils=(3, 5), tube=1.4, gap=(0.1, 0.5), ring_sides=12,
           tube_sides=4, tilt=3.0):
    """Rope coils wrapped around a log of the given bark radius at `center`."""
    rng = _rng(name, seed)
    ax, e1, e2 = frame(axis)
    n = rng.randint(*coils); g = rng.uniform(*gap)
    # Both outlines are polygons. The coil's edges pass closer to the log than its corners, and the
    # rope's innermost corner sits tube*min(cos) from the coil line (half a tube for a triangle, a
    # whole one for a square): place the coil so the innermost edge lies exactly on radius + gap.
    min_cos = min(math.cos(2*math.pi*j/tube_sides) for j in range(tube_sides))
    major = (radius + g)/math.cos(math.pi/ring_sides) - tube*min_cos
    pitch = 2*tube*0.9; shift = rng.uniform(-tube, tube)
    verts, uvs, faces = [], [], []
    for k in range(n):
        off = (k - (n - 1)/2)*pitch + shift
        a = math.radians(rng.uniform(-tilt, tilt)); psi = rng.uniform(0, 2*math.pi)
        # Tilt the coil plane slightly about a direction across the log.
        tdir = _add(_mul(e1, math.cos(psi)), _mul(e2, math.sin(psi))); other = _cross(ax, tdir)
        U = tdir; V = _add(_mul(other, math.cos(a)), _mul(ax, math.sin(a))); W = _cross(U, V)
        c = _add(center, _mul(ax, off)); base = len(verts)
        for i in range(ring_sides + 1):
            ph = 2*math.pi*i/ring_sides; rad = _add(_mul(U, math.cos(ph)), _mul(V, math.sin(ph)))
            for j in range(tube_sides + 1):
                ps = 2*math.pi*j/tube_sides
                p = _add(c, _add(_mul(rad, major + tube*math.cos(ps)), _mul(W, tube*math.sin(ps))))
                verts.append(p); uvs.append((i/ring_sides, j/tube_sides))
        row = tube_sides + 1
        for i in range(ring_sides):
            for j in range(tube_sides):
                i0 = base + i*row + j
                faces.append((i0, i0 + row, i0 + row + 1, i0 + 1))
    # A coil tilted by a stays at least major*cos(a) - tube from the axis; with a <= 3 deg and gap
    # >= 0.1 the rope never sinks into the bark.
    return {'verts': verts, 'faces': faces, 'uvs': uvs,
            'meta': {'coils': n, 'gap': g, 'inner_radius': radius + g, 'circumference': 2*math.pi*major}}
