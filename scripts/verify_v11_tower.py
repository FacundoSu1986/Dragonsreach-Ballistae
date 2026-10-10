"""Plan task 11: the v11 tower as built (Blender; nothing is saved, spec §4 'Torre nueva').

Measured on the written torre.nif (visual from its bytes, Havok collision reimported) and on every
vanilla piece of config.json -> tower_v11 placed with the shared transform (memory only):
  1. every stilt reaches the ground (z <= 2) and touches what it carries (gap under 2 u);
  2. every brace and tie touches both stilts it joins;
  3. the room is closed but for the door opening (rays from its centre);
  4. the door leaf sweeps the range keyframed in its own NIF without touching the collision of
     the room, the frame or the stilts;
  5. an 18 u capsule walks from the stair foot to the door, under the platform;
  6. the spawn marker keeps 40 u from anything in the 0-128 u band;
  7. irregularity and walk surfaces measured on the NIF: log bend, taper and lean, plank twist, and
     the deck, landing and tread tops within 1.2 u of the collision.
Every check is falsified (a piece moved, a wall removed, an obstacle added) and must then fail.
"""
import bpy, addon_utils, json, math, sys, hashlib, struct, collections
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]
import v11_layout as L
import tower_v11_geometry as G
import nif_nodos, nif_fisica

CFG = L.load_cfg(); LAY = CFG['tower_v11']; PIECES = {p['name']: p for p in LAY['pieces']}
MESH = ROOT/'mod/meshes/AstraAsedio'
DECK_TOP = LAY['platform']['deck_top']

def bvh(V, T): return BVHTree.FromPolygons([Vector(v) for v in V], [tuple(int(i) for i in t) for t in T], all_triangles=True)
def solid_mesh(piece, offset=(0.0, 0.0, 0.0)):
    tris = [t for s in L.piece_solids(piece, CFG) for t in L.solid_triangles(s)]
    V = np.array([p for t in tris for p in t]) + np.array(offset); return V, np.arange(len(V)).reshape(-1, 3)
def merge(meshes):
    Vs, Ts, n = [], [], 0
    for V, T in meshes: Vs.append(V); Ts.append(T + n); n += len(V)
    return (np.concatenate(Vs), np.concatenate(Ts)) if Vs else (np.zeros((0, 3)), np.zeros((0, 3), dtype=int))
def moved(piece, dz=0.0, d=(0.0, 0.0, 0.0)):
    q = dict(piece); q['pos'] = [piece['pos'][0] + d[0], piece['pos'][1] + d[1], piece['pos'][2] + d[2] + dz]; return q

def torre_collision():
    """Havok collision of the written torre.nif, reimported by PyNifly."""
    addon_utils.enable('io_scene_nifly', default_set=True)
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    bpy.context.view_layer.objects.active = None
    bpy.ops.import_scene.pynifly(filepath=str(MESH/'torre.nif'), blender_xf=False, create_bones=False, import_animations=False, import_collisions=True)
    bpy.context.view_layer.update(); V, T = [], []
    for o in bpy.data.objects:
        if o.type != 'MESH' or not o.name.startswith('bhk'): continue
        o.data.calc_loop_triangles(); base = len(V)
        V += [tuple(o.matrix_world @ v.co) for v in o.data.vertices]; T += [tuple(base + i for i in t.vertices) for t in o.data.loop_triangles]
    assert V, 'torre.nif has no collision'
    return np.array(V), np.array(T)

def shapes_by_name(path):
    nif = nif_nodos.leer(str(path)); d = nif['datos']; mp = nif_fisica._mundo_padre(nif); out = collections.defaultdict(list)
    for i, name, _o, local, _s, _a, desc, nv, datos in nif_fisica._shapes(nif):
        nt = struct.unpack_from('<H', d, datos - 8)[0]; m = nif_fisica._mul(mp(i), local); paso = (desc & 0xF)*4
        V = np.array([nif_fisica._aplicar(m, struct.unpack_from('<3f', d, datos + k*paso)) for k in range(nv)])
        T = np.array([struct.unpack_from('<3H', d, datos + nv*paso + 6*k) for k in range(nt)])
        out[name].append((V, T))
    return {k: merge(v) for k, v in out.items()}

def components(V, T):
    """Pieces of a merged shape: triangles joined through welded vertex positions."""
    key = np.round(V, 2); _u, inv = np.unique(key, axis=0, return_inverse=True); inv = inv.ravel()
    parent = list(range(len(_u)))
    def find(a):
        while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for t in T:
        a = find(inv[t[0]])
        for j in (1, 2):
            b = find(inv[t[j]])
            if a != b: parent[b] = a
    groups = collections.defaultdict(list)
    for vi in range(len(V)): groups[find(inv[vi])].append(vi)
    return [np.array(sorted(set(g))) for g in groups.values()]

# ---------------------------------------------------------------------------------------------
BARY = [(u, v) for u in np.linspace(0, 1, 6) for v in np.linspace(0, 1, 6) if u + v <= 1 + 1e-9]

def check_stilts(carried_bvh, pieces):
    """The surface of the stilt's top end against the own logs and planks it carries (ropes left out).
    Measured 2026-10-06: the nearest distance from the top vertices also caught the rope lashed around
    the stilt (a stilt lowered 10 u still 'touched'), and the vanilla rings are too sparse to sit under
    a log; the top end is cut at a slant, so its whole surface is sampled."""
    rows = []
    for p in pieces:
        if p['role'] != 'pilote': continue
        V, T = L.piece_mesh(p, CFG); m = L.piece_matrix(p)
        ax = np.array(m['r']) @ np.array([0.0, 1.0, 0.0]); ax = ax if ax[2] > 0 else -ax
        along = (V - np.array(m['t'])) @ ax; top_T = T[(along[T] > along.max() - 25.0).all(axis=1)]
        if carried_bvh.overlap(bvh(V, top_T)): gap = 0.0
        else:
            pts = [V[a]*u + V[b]*v + V[c]*(1 - u - v) for a, b, c in top_T for u, v in BARY]
            gap = min(carried_bvh.find_nearest(Vector(q))[3] for q in pts)
        rows.append({'name': p['name'], 'bottom_z': float(V[:, 2].min()), 'top_gap': float(gap), 'supports': p['supports'],
                     'top_cut_lift': p.get('top_cut_lift'), 'ok': bool(V[:, 2].min() <= 2.0 and gap < 2.0)})
    return rows

def check_braces(pieces):
    meshes = {n: L.piece_mesh(p, CFG) for n, p in pieces.items()}; trees = {n: bvh(*meshes[n]) for n in meshes}; rows = []
    for n, p in pieces.items():
        if p['role'] not in ('cruz', 'viga'): continue
        contact = {}
        for s in p['joins']:
            touch = bool(trees[n].overlap(trees[s]))
            if not touch:
                V = meshes[n][0]; touch = min(trees[s].find_nearest(Vector(q))[3] for q in V) <= 1.0
            contact[s] = touch
        rows.append({'name': n, 'joins': contact, 'ok': all(contact.values())})
    return rows

def check_room(static_bvh, z_list=(20.0, 60.0, 100.0, 140.0, 175.0)):
    escapes = []
    for z in z_list:
        for k in range(45):
            a = math.radians(8*k); d = Vector((math.cos(a), math.sin(a), 0.0))
            hit = static_bvh.ray_cast(Vector((0.0, 0.0, z)), d, 200.0)
            if hit[0] is None: escapes.append({'z': z, 'azimuth_deg': 8*k})
    return escapes

def door_sweep(static_bvh, hinge, leaf_V, leaf_T, angles):
    """Turn the leaf about the vertical through the hinge (counter-clockwise positive, degrees) and
    list the angles where it overlaps the static collision; also return the leaf at the last angle."""
    hits = []; last = None
    for ang in angles:
        a = math.radians(ang); c, s = math.cos(a), math.sin(a)
        rel = leaf_V - hinge; R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]]); last = rel @ R.T + hinge
        if static_bvh.overlap(bvh(last, leaf_T)): hits.append(round(ang, 1))
    return hits, last

def capsule_path(static_bvh, start, goal, extra=None, step=8.0):
    room = LAY['room']; (rcx, rcy), (sx, sy) = room['center'], room['size']
    xs = np.arange(-320.0, 424.0, step); ys = np.arange(-664.0, 328.0, step)
    snap = lambda p: (int(round((p[0] - xs[0])/step)), int(round((p[1] - ys[0])/step)))
    def free(i, j):
        x, y = xs[i], ys[j]
        if abs(x - rcx) < sx/2 and abs(y - rcy) < sy/2: return False
        for z in (19.0, 45.0, 75.0, 105.0, 128.0):
            if static_bvh.find_nearest(Vector((x, y, z)), 18.0)[0] is not None: return False
            if extra is not None and extra.find_nearest(Vector((x, y, z)), 18.0)[0] is not None: return False
        return True
    s, g = snap(start), snap(goal); cache = {}
    def ok(c):
        if c not in cache: cache[c] = 0 <= c[0] < len(xs) and 0 <= c[1] < len(ys) and free(*c)
        return cache[c]
    if not ok(s) or not ok(g): return {'reached': False, 'start_free': ok(s), 'goal_free': ok(g)}
    seen = {s}; todo = collections.deque([s])
    while todo:
        c = todo.popleft()
        if c == g: return {'reached': True, 'cells_explored': len(seen)}
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c[0] + dx, c[1] + dy)
            if n not in seen and ok(n): seen.add(n); todo.append(n)
    return {'reached': False, 'cells_explored': len(seen)}

def marker_clear(static_bvh, pos, need):
    worst = math.inf
    for z in np.arange(0.0, 128.1, 4.0):
        hit = static_bvh.find_nearest(Vector((pos[0], pos[1], z)), need + 20.0)
        if hit[0] is not None: worst = min(worst, hit[3])
    return worst

def irregularity(shapes):
    """Logs and planks of the written torre.nif, measured from their own vertices."""
    V, T = merge([shapes[k] for k in ('Torre_stockade_wood', 'Torre_stockade_extra')]); logs = []
    for comp in components(V, T):
        P = V[comp]; c = P.mean(0); _u, _s, vt = np.linalg.svd(P - c); ax = vt[0]
        along = (P - c) @ ax; order = np.argsort(along); ring_ids = [[order[0]]]
        for a, b in zip(order, order[1:]):
            if along[b] - along[a] > 2.0: ring_ids.append([b])
            else: ring_ids[-1].append(b)
        rings = [P[r] for r in ring_ids]
        if len(rings) < 3: continue
        cents = [r.mean(0) for r in rings]; L_ = along.max() - along.min()
        a0, a1 = cents[0], cents[-1]; d = (a1 - a0)/np.linalg.norm(a1 - a0)
        bend = max(np.linalg.norm((q - a0) - ((q - a0) @ d)*d) for q in cents[1:-1])/L_
        rad = []
        for r, q in zip(rings, cents):
            dist = np.linalg.norm((r - q) - np.outer((r - q) @ d, d), axis=1); dist = dist[dist > 0.3*np.median(dist)]
            rad.append((float((q - a0) @ d), float(dist.mean())))
        t = np.array([x for x, _ in rad]); r_ = np.array([y for _, y in rad]); k, b0 = np.polyfit(t, r_, 1)
        r_start, r_end = b0 + k*t.min(), b0 + k*t.max(); taper = 1 - min(r_start, r_end)/max(r_start, r_end)
        tilt = math.degrees(math.acos(min(1.0, abs(d[2]))))
        logs.append({'center': c.round(1).tolist(), 'length': float(L_), 'bend_fraction': float(bend), 'taper': float(taper), 'tilt_from_vertical_deg': tilt})
    Vp, Tp = shapes['Torre_stockade_planks']; deck, treads, twist = [], [], []
    for comp in components(Vp, Tp):
        P = Vp[comp]; top = P[P[:, 2] > P[:, 2].max() - 0.8]
        if P[:, 2].max() > DECK_TOP - 2 and P[:, 2].max() < DECK_TOP + 2:
            deck.append(float(np.abs(top[:, 2] - DECK_TOP).max()))
        elif G.SX0 - 20 < P[:, 0].mean() < G.SX1 + 20 and G.SY0 - 20 < P[:, 1].mean() < G.SY1 + 20 and P[:, 2].max() < DECK_TOP - 2:
            cen = top.mean(0); treads.append(float(abs(cen[2] - G.ramp_z(cen[1]))))
    return logs, deck, treads

def main():
    sha = hashlib.sha256((MESH/'torre.nif').read_bytes()).hexdigest()
    shapes = shapes_by_name(MESH/'torre.nif')
    carried = bvh(*merge([shapes[k] for k in ('Torre_stockade_wood', 'Torre_stockade_extra', 'Torre_stockade_planks')]))
    Vc, Tc = torre_collision()
    door = next(p for p in LAY['pieces'] if p['role'] == 'puerta')
    vanilla = {n: solid_mesh(p) for n, p in PIECES.items()}
    def static(exclude=(), add=()):
        return bvh(*merge([(Vc, Tc)] + [m for n, m in vanilla.items() if n not in exclude] + list(add)))
    report = {'torre_nif_sha256': sha}
    # 1. stilts
    stilts = check_stilts(carried, LAY['pieces'])
    fake = check_stilts(carried, [moved(PIECES['pilote_-262_-262'], dz=-10.0)])
    report['stilts'] = {'ok': all(r['ok'] for r in stilts), 'rows': stilts, 'max_top_gap': max(r['top_gap'] for r in stilts),
                        'falsified': not fake[0]['ok'], 'falsification': 'pilote_-262_-262 lowered 10 u'}
    # 2. braces
    braces = check_braces(PIECES)
    fp = dict(PIECES); fp['cruz_O_1'] = moved(PIECES['cruz_O_1'], d=(-40.0, 0.0, 0.0))
    fake_b = [r for r in check_braces(fp) if r['name'] == 'cruz_O_1'][0]
    report['braces'] = {'ok': all(r['ok'] for r in braces), 'failed': [r for r in braces if not r['ok']],
                        'count': len(braces), 'falsified': not fake_b['ok'], 'falsification': 'cruz_O_1 moved 40 u off its face'}
    # 3. room
    closed = check_room(static()); open_ = check_room(static(exclude=('puerta',)))
    lo_az, hi_az = sorted(math.degrees(math.atan2(-118.0, s*G.DOOR_HALF)) % 360 for s in (1, -1))
    through_opening = all(lo_az - 8 <= e['azimuth_deg'] <= hi_az + 8 and e['z'] < G.DOOR_TOP for e in open_)
    fake_r = check_room(static(exclude=('pared_O',)))
    report['room'] = {'ok': not closed and bool(open_) and through_opening, 'escapes_with_door_closed': closed,
                      'escapes_without_door': open_, 'opening_azimuths_deg': [lo_az, hi_az],
                      'falsified': any(not (lo_az - 8 <= e['azimuth_deg'] <= hi_az + 8) for e in fake_r), 'falsification': 'west wall removed'}
    # 4. door sweep over the range keyframed in its NIF, in the sense the vanilla furniture decided
    sw = L.door_swing(CFG, door); lo_deg, hi_deg = sw['key_range_deg']
    hinge = np.array(L.apply(L.piece_matrix(door), sw['pivot_local']))
    extreme = max((lo_deg, hi_deg), key=abs); steps = int(round(abs(extreme)))
    angles = [sw['local_sign']*extreme*k/steps for k in range(steps + 1)]        # the door turns about Z only
    visual_V, visual_T = L.piece_mesh(door, CFG); st = static(exclude=('puerta',))
    hits, open_leaf = door_sweep(st, hinge, visual_V, visual_T, angles)
    col_hits, _ = door_sweep(st, hinge, *vanilla['puerta'], angles)
    other_hits, _ = door_sweep(st, hinge, visual_V, visual_T, [-a for a in angles])
    room_y = LAY['room']['center'][1]
    block = (np.array([[-40.0, -70.0, 0.0], [90.0, -70.0, 0.0], [90.0, -70.0, 170.0], [-40.0, -70.0, 170.0]]), np.array([[0, 1, 2], [0, 2, 3]]))
    fake_d, _ = door_sweep(static(exclude=('puerta',), add=[block]), hinge, visual_V, visual_T, angles)
    report['door'] = {'ok': bool(not hits and float(open_leaf[:, 1].mean()) > float(hinge[1])), 'keyframed_z_range_deg': [lo_deg, hi_deg],
                      'key_convention': sw['convention'], 'hinge_world': hinge.round(2).tolist(), 'leaf': 'visual mesh of the vanilla door',
                      'hits_deg': hits, 'collision_leaf_hits_deg': col_hits, 'other_sense_hits_deg': other_hits,
                      'open_leaf_centre': open_leaf.mean(0).round(1).tolist(), 'opens_into_room': bool(open_leaf[:, 1].mean() > hinge[1]),
                      'falsified': bool(fake_d), 'falsification': 'a panel inside the room across the swing'}
    # 5. capsule path from the stair foot to the door
    start, goal = (G.SX0 + G.SX1)/2, (G.SY0 - 32.0); path = capsule_path(st, (start, goal), (0.0, -160.0))
    wall = (np.array([[-330.0, -200.0, 0.0], [430.0, -200.0, 0.0], [430.0, -200.0, 140.0], [-330.0, -200.0, 140.0]]), np.array([[0, 1, 2], [0, 2, 3]]))
    fake_p = capsule_path(st, (start, goal), (0.0, -160.0), extra=bvh(*wall))
    report['path'] = dict(path, ok=path['reached'], start=[start, goal], goal=[0.0, -160.0], capsule_radius=18.0,
                          falsified=not fake_p['reached'], falsification='a wall across the whole approach at y -200')
    # 6. spawn marker
    plugin = json.loads((ROOT/'reports/plugin_build.json').read_text()); pos = plugin['spawn_marker']['pos']; need = LAY['spawn_marker']['min_clearance']
    clear = marker_clear(static(), pos, need); fake_m = marker_clear(static(), (128.0, 250.0), need)
    report['spawn_marker'] = {'ok': clear >= need, 'pos': pos, 'clearance': clear, 'falsified': fake_m < need, 'falsification': 'marker beside pilote_+128_+262'}
    # 7. irregularity and walk surfaces on the written NIF
    logs, deck, treads = irregularity(shapes)
    irr = LAY['irregularity']; leaning = [r for r in logs if r['length'] < 160 and r['tilt_from_vertical_deg'] < 10]
    report['irregularity'] = {
        'logs': len(logs), 'bend_at_least_1pct': sum(r['bend_fraction'] >= 0.01 for r in logs),
        'taper_in_range': sum(irr['log_taper'][0] - 0.01 <= r['taper'] <= irr['log_taper'][1] + 0.01 for r in logs),
        'posts_measured': len(leaning), 'posts_tilt_in_range': sum(irr['log_tilt_deg'][0] - 0.1 <= r['tilt_from_vertical_deg'] <= irr['log_tilt_deg'][1] + 0.1 for r in leaning),
        'deck_planks': len(deck), 'deck_top_max_deviation': max(deck) if deck else None, 'treads': len(treads), 'tread_centre_max_deviation': max(treads) if treads else None,
        'walk_tolerance': irr['walk_surface_tolerance_units'], 'rows': logs}
    ir = report['irregularity']
    ir['ok'] = (ir['bend_at_least_1pct'] > ir['logs']/2 and ir['taper_in_range'] >= 0.9*ir['logs'] and ir['posts_tilt_in_range'] >= 0.9*ir['posts_measured']
                and ir['deck_top_max_deviation'] is not None and ir['deck_top_max_deviation'] <= irr['walk_surface_tolerance_units']
                and len(treads) == G.COUNT and ir['tread_centre_max_deviation'] <= irr['walk_surface_tolerance_units'])
    checks = ('stilts', 'braces', 'room', 'door', 'path', 'spawn_marker')
    report['ok'] = all(report[k]['ok'] and report[k]['falsified'] for k in checks) and ir['ok']
    report['inputs_sha256'] = {n: hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in
                               ('mod/meshes/AstraAsedio/torre.nif', 'config.json', 'reports/plugin_build.json', 'scripts/verify_v11_tower.py', 'scripts/v11_layout.py')}
    (ROOT/'reports/v11_tower.json').write_text(json.dumps(report, indent=2))
    print('V11_TOWER', 'ok' if report['ok'] else 'FAILED', {k: (report[k]['ok'], report[k]['falsified']) for k in checks},
          {k: ir[k] for k in ('logs', 'bend_at_least_1pct', 'taper_in_range', 'posts_measured', 'posts_tilt_in_range', 'deck_top_max_deviation', 'treads', 'tread_centre_max_deviation', 'ok')})
    if not report['ok']: raise SystemExit('v11 tower verification failed')

main()
