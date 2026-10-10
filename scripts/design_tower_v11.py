"""Derive config.json -> tower_v11: the vanilla pieces of the rustic tower (spec §1).

config.json is the single source of truth the builds read. This script records how its numbers
were derived: change a parameter below, rerun it, then rebuild. The small tilts come from a fixed
seed, so every run writes the same layout. The checks at the end fail closed when a piece would
enter a space the v10 game test proved (stair walk, room, door swing, entrance).
"""
import hashlib, json, math, random, sys, zlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import v11_layout as L

# v10 invariants (reports/collision_walkable.json, spec "Invariantes").
DECK_TOP = 453.95
FLOOR_COLLISION_BOTTOM = 442.75
STAIR_Y = (-535.9503875968993, 196.0)
STAIR_WALK_X = (286.3, 360.5)          # between the two invariant edge barriers
def ramp_z(y): return DECK_TOP*(y - STAIR_Y[0])/(STAIR_Y[1] - STAIR_Y[0])

# Structure.
GRID = (-262.0, -128.0, 128.0, 262.0)  # piling axes: platform edge ±280, room corners ±128
PILE_TOP = 423.0                       # underside of the own joists
PILE_BOTTOM = -20.0                    # sunk below the cell floor
STAIR_PILE_X = (285.6, 361.2)          # under the stringers, where v10 had its 'Pilar' boxes
STAIR_PILE_T = (0.24, 0.48, 0.72)
# Pile top under the own log stringer (tower_v11_geometry.py), measured straight down from the ramp
# line: the stringer's top stays >= 18 u under it (tread 10.5 + half riser 6.7) and a 10 u log on a
# 31.8 degree slope is 2r/cos = 23.5 u deep vertically. v10's square pilar stopped at 17.5.
STAIR_PILE_DROP = 41.5
LANDING_PILES = ((361.2, 205.0), (361.2, 271.0))
ROOM_HALF, WALL_T, WALL_TOP = 128.0, 20.0, 192.0
BEAM_LEN, SHORT_LEN = 305.4, 143.4     # measured StockadeWoodbeam01 / StockadeWoodbeamShort01
X_LOW = 225.0                          # lower ends of the central X braces
TIE_Z = 205.0
SIDE_DIAG_TOP = 410.0
SEED = 2026
MAX_PILE_TILT, MAX_BRACE_TILT, MAX_SPIN = 1.2, 0.8, 10.0
CORNER_POST_TOP = 560.0                # own corner posts above the deck; verify_shot_clearance.py bounds it

BEAMS = ('StockadeWoodbeam01', 'StockadeWoodbeam02', 'StockadeWoodbeam03')
SHORTS = ('StockadeWoodbeamShort01', 'StockadeWoodbeamShort02')
WALL, CEILING, DOOR = 'StockadeBuildingStraight01', 'StockadeScaffoldTop0Sided01', 'FarmhouseAnimDoor01'

def add(a, b): return tuple(p + q for p, q in zip(a, b))
def sub(a, b): return tuple(p - q for p, q in zip(a, b))
def mul(a, k): return tuple(p*k for p in a)
def norm(a): return math.sqrt(sum(p*p for p in a))
def unit(a): return mul(a, 1/norm(a))
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def rotate(v, axis, deg):
    """Rodrigues rotation of v about the unit axis."""
    k = unit(axis); t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    kv = sum(p*q for p, q in zip(k, v))
    return tuple(v[i]*c + cross(k, v)[i]*s + k[i]*kv*(1 - c) for i in range(3))

def pile_name(x, y): return 'pilote_%+04d_%+04d' % (round(x), round(y))

class Layout:
    def __init__(self, index):
        self.index, self.pieces, self.n = index, [], 0
    def rng(self, name): return random.Random(SEED ^ zlib.crc32(name.encode()))
    def put(self, name, role, edid, pos, rot, scale=1.0, **extra):
        base = self.index[edid.lower()]
        self.pieces.append(dict(name=name, role=role, edid=base['edid'], modl=base['modl'],
                                pos=[round(v, 3) for v in pos], rot_deg=[round(v, 4) for v in rot],
                                scale=round(scale, 4), **extra))
    def piling(self, x, y, top, supports, tilt_dirs=None, side=None):
        name = pile_name(x, y); r = self.rng(name)
        scale = max(1.0, (top - PILE_BOTTOM)/BEAM_LEN); length = BEAM_LEN*scale
        t = math.radians(r.uniform(0.3, MAX_PILE_TILT))
        psi = math.radians(r.choice(tilt_dirs) if tilt_dirs else r.uniform(0, 360))
        up = (math.sin(t)*math.cos(psi), math.sin(t)*math.sin(psi), math.cos(t))
        phi = math.radians(r.uniform(-60, 60))
        side = side or (math.cos(phi), math.sin(phi), 0.0)
        long_dir = up if r.random() < 0.5 else mul(up, -1)      # either cut end on top
        center = sub((x, y, top), mul(up, length/2))            # the top touches what it carries
        edid = BEAMS[self.n % 3]; rot = L.rot_for_axes(long_dir, side)
        # The vanilla beam ends are cut at a slant (4.7-4.9 u along the axis, x scale): under a level log
        # lift the stilt until the lowest point of its top cut is 1 u inside it (measured on the mesh).
        # Under the 31.8 degree stringer the downhill edge of the cut already sits in the log.
        import numpy as np
        m = L.transform_matrix(center, rot, scale, *L.engine_convention())
        W = L.mesh_vertices(self.index[edid.lower()]['modl']) @ (np.array(m['r'])*m['s']).T + np.array(m['t'])
        along = (W - np.array(center)) @ np.array(up); cut = W[along > along.max() - 12.0*scale]
        lift = 0.0 if supports == 'escalera' else max(0.0, (top - 1.0) - float(cut[:, 2].min()))
        center = (center[0], center[1], center[2] + lift)
        self.put(name, 'pilote', edid, center, rot, scale, supports=supports, top_cut_lift=round(lift, 2))
        self.n += 1
    def brace(self, name, role, edid, a, b, normal, joins):
        """A log whose centre line runs from a to b, its thin side facing `normal`."""
        r = self.rng(name)
        d = rotate(unit(sub(b, a)), normal, r.uniform(-MAX_BRACE_TILT, MAX_BRACE_TILT))
        d = rotate(d, cross(normal, d), r.uniform(-MAX_BRACE_TILT/2, MAX_BRACE_TILT/2))
        if r.random() < 0.5: d = mul(d, -1)
        side = rotate(cross(d, normal), d, r.uniform(-MAX_SPIN, MAX_SPIN))
        self.put(name, role, edid, mul(add(a, b), 0.5), L.rot_for_axes(d, side), joins=joins)

FACES = {  # u: along the face, n: outward normal, o: piling line
    'S': ((1, 0, 0), (0, -1, 0), (0, -262.0, 0)),
    'N': ((1, 0, 0), (0, 1, 0), (0, 262.0, 0)),
    'O': ((0, 1, 0), (-1, 0, 0), (-262.0, 0, 0)),
    'E': ((0, 1, 0), (1, 0, 0), (262.0, 0, 0)),
}
# East face braces sit inside the piling line: the stair and its supports run just outside it.
# The second X log at -18 passed 2.8 u beside the stilt at y +128 (verify_v11_tower.py, exact triangle
# distance); at -14 it crosses both stilts and still clears the stair supports (x >= 271.6).
OFFSETS = {'S': (4, -10, 0, 4), 'N': (4, -10, 0, 4), 'O': (4, -10, 0, 4), 'E': (-4, -14, -8, -4)}

def design(index):
    lay = Layout(index)
    for x in GRID:
        for y in GRID:
            east = abs(x - GRID[-1]) < 1e-6
            # East pilings keep their thin side and their tilt along y, clear of the stair edge.
            lay.piling(x, y, PILE_TOP, 'plataforma', tilt_dirs=(90, 270) if east else None,
                       side=(0.0, 1.0, 0.0) if east else None)
    stair_tops = []
    for t in STAIR_PILE_T:
        y = STAIR_Y[0] + t*(STAIR_Y[1] - STAIR_Y[0]); top = ramp_z(y) - STAIR_PILE_DROP
        stair_tops.append((y, top))
        for x in STAIR_PILE_X:
            lay.piling(x, y, top, 'escalera', tilt_dirs=(90, 270), side=(0.0, 1.0, 0.0))
    for x, y in LANDING_PILES:
        lay.piling(x, y, PILE_TOP, 'descanso', tilt_dirs=(90, 270), side=(0.0, 1.0, 0.0))
    for f, (u, n, o) in FACES.items():
        xo1, xo2, to, do = OFFSETS[f]
        P = lambda s, h, off: add(add(o, mul(u, s)), add((0, 0, h), mul(n, off)))
        pile = lambda s: pile_name(*add(o, mul(u, s))[:2])
        rise = math.sqrt(BEAM_LEN**2 - (2*GRID[2])**2)
        lay.brace('cruz_%s_1' % f, 'cruz', BEAMS[0], P(-128, X_LOW, xo1), P(128, X_LOW + rise, xo1), n, [pile(-128), pile(128)])
        lay.brace('cruz_%s_2' % f, 'cruz', BEAMS[1], P(-128, X_LOW + rise, xo2), P(128, X_LOW, xo2), n, [pile(-128), pile(128)])
        lay.brace('viga_%s_c' % f, 'viga', BEAMS[2], P(-BEAM_LEN/2, TIE_Z, to), P(BEAM_LEN/2, TIE_Z, to), n, [pile(-128), pile(128)])
        side_rise = math.sqrt(BEAM_LEN**2 - (GRID[3] - GRID[2])**2)
        for k, sgn in (('i', -1), ('d', 1)):
            mid = sgn*(GRID[2] + GRID[3])/2
            lay.brace('viga_%s_%s' % (f, k), 'viga', SHORTS[(sgn + 1)//2], P(mid - SHORT_LEN/2, TIE_Z, to),
                      P(mid + SHORT_LEN/2, TIE_Z, to), n, [pile(sgn*GRID[2]), pile(sgn*GRID[3])])
            lay.brace('diagonal_%s_%s' % (f, k), 'cruz', BEAMS[(sgn + 1)//2 + 1], P(sgn*GRID[3], SIDE_DIAG_TOP, do),
                      P(sgn*GRID[2], SIDE_DIAG_TOP - side_rise, do), n, [pile(sgn*GRID[3]), pile(sgn*GRID[2])])
    # Stair: a short diagonal across each support pair and a long one along each stringer line.
    span = STAIR_PILE_X[1] - STAIR_PILE_X[0]; drop = math.sqrt(SHORT_LEN**2 - span**2)
    for k, (y, top) in enumerate(stair_tops):
        hi, lo = (STAIR_PILE_X[0], STAIR_PILE_X[1]) if k % 2 else (STAIR_PILE_X[1], STAIR_PILE_X[0])
        lay.brace('escalera_trans_%d' % k, 'cruz', SHORTS[k % 2], (hi, y, top - 12), (lo, y, top - 12 - drop), (0, 1, 0),
                  [pile_name(STAIR_PILE_X[0], y), pile_name(STAIR_PILE_X[1], y)])
    for x, tag in zip(STAIR_PILE_X, ('int', 'ext')):
        for k in range(len(stair_tops) - 1):
            (y0, _t0), (y1, t1) = stair_tops[k], stair_tops[k + 1]
            z1 = t1 - 12; z0 = z1 - math.sqrt(BEAM_LEN**2 - (y1 - y0)**2)
            lay.brace('escalera_long_%s_%d' % (tag, k), 'cruz', BEAMS[k % 3], (x, y0, z0), (x, y1, z1), (1, 0, 0),
                      [pile_name(x, y0), pile_name(x, y1)])
    # Room: three plank walls sunk 64 u (as the vanilla StockadeBuildingCorner01 sits), the front wall is own.
    c = ROOM_HALF - WALL_T/2
    for name, pos, out, along in (('pared_N', (0, c, -64.0), (0, 1, 0), (1, 0, 0)),
                                  ('pared_O', (-c, 0, -64.0), (-1, 0, 0), (0, 1, 0)),
                                  ('pared_E', (c, 0, -64.0), (1, 0, 0), (0, -1, 0))):
        lay.put(name, 'pared', WALL, pos, L.rot_for_axes(out, along))
    lay.put('techo', 'techo', CEILING, (0, 0, WALL_TOP + 15.4), (0.0, 0.0, 0.0))
    # Door: the side its leaf swings to (v11_layout.door_swing: hinge and keys from its NIF, the key
    # convention from vanilla furniture) faces the room.
    s = L.door_swing(door={'modl': index[DOOR.lower()]['modl'], 'role': 'puerta'})['opens_local'][1]
    lay.put('puerta', 'puerta', DOOR, (0, -c, 0), L.rot_for_axes((0, s, 0), (s, 0, 0)))
    return lay.pieces

def obb_points(piece, index, step=10.0):
    lo, hi = index[piece['edid'].lower()]['obnd'][:3], index[piece['edid'].lower()]['obnd'][3:]
    m = L.piece_matrix(piece)
    axes = [[lo[i] + (hi[i] - lo[i])*k/max(1, math.ceil((hi[i] - lo[i])/step)) for k in range(int(max(1, math.ceil((hi[i] - lo[i])/step))) + 1)] for i in range(3)]
    return [L.apply(m, (a, b, c)) for a in axes[0] for b in axes[1] for c in axes[2]]

def checks(pieces, index):
    found = {}
    def inside_stair(p):
        return STAIR_Y[0] < p[1] < STAIR_Y[1] and STAIR_WALK_X[0] < p[0] < STAIR_WALK_X[1] and ramp_z(p[1]) + 1 < p[2] < ramp_z(p[1]) + 128
    door = next(p for p in pieces if p['role'] == 'puerta')
    sw = L.door_swing(door=door); m = L.piece_matrix(door)
    hinge = L.apply(m, sw['pivot_local'])
    closed = (-m['r'][0][0], -m['r'][1][0])                    # the leaf runs from the hinge along local -X
    extreme = max(sw['key_range_deg'], key=abs)
    opening = 1 if sw['local_sign']*extreme > 0 else -1        # counter-clockwise positive, about +Z
    def in_swing(p, sense):
        dx, dy = p[0] - hinge[0], p[1] - hinge[1]
        if not (0 <= p[2] <= 180 and math.hypot(dx, dy) <= 100): return False
        a = (math.degrees(math.atan2(dy, dx) - math.atan2(closed[1], closed[0])) + 180) % 360 - 180
        return 0 <= sense*a <= 100
    room_in = ROOM_HALF - WALL_T - 2
    for piece in pieces:
        pts = obb_points(piece, index)
        tag = piece['name']
        if any(inside_stair(p) for p in pts): found.setdefault('stair_walk_volume', []).append(tag)
        if max(p[2] for p in pts) > FLOOR_COLLISION_BOTTOM: found.setdefault('above_deck_underside', []).append(tag)
        if piece['role'] not in ('pared', 'techo', 'puerta', 'pilote') and \
           any(abs(p[0]) < room_in and abs(p[1]) < room_in and 0 < p[2] < WALL_TOP for p in pts):
            found.setdefault('room_interior', []).append(tag)
        if piece['role'] != 'pilote' and any(-ROOM_HALF + 20 < p[0] < ROOM_HALF - 20 and -280 < p[1] < -ROOM_HALF and 0 < p[2] < 190 for p in pts):
            found.setdefault('entrance', []).append(tag)
        if piece is not door:
            for sense, key in ((opening, 'door_swing_open'), (-opening, 'door_swing_other')):
                if any(in_swing(p, sense) for p in pts): found.setdefault(key, []).append(tag)
    return found, hinge

def main():
    cfg = L.load_cfg(); index = L.esm_index(cfg)
    pieces = design(index)
    cfg['tower_v11'] = {
        'note': 'Generated by scripts/design_tower_v11.py; the builds read this block (spec §1).',
        'room': {'center': [0, 0], 'size': [2*ROOM_HALF, 2*ROOM_HALF], 'wall_thickness': WALL_T, 'wall_height': WALL_TOP,
                 'door_side': '-y', 'door_opens': 'inward', 'door_opening': [100, 178]},
        'platform': {'grid': list(GRID), 'pile_top': PILE_TOP, 'deck_top': DECK_TOP},
        'corner_posts': {'top_z': CORNER_POST_TOP},
        'stair': {'pile_drop': STAIR_PILE_DROP, 'pile_t': list(STAIR_PILE_T), 'pile_x': list(STAIR_PILE_X)},
        'irregularity': {'seed': 1105, 'log_bend_min_fraction': 0.01, 'log_tilt_deg': [0.5, 3.0], 'log_taper': [0.08, 0.20],
                         'plank_width_variation': 0.15, 'plank_end_shift_units': 12.0, 'plank_twist_deg': 1.2,
                         'walk_surface_tolerance_units': 1.2, 'tread_edge_tolerance_units': 6.7},
        'vanilla_jitter': {'seed': SEED, 'pile_tilt_deg': MAX_PILE_TILT, 'brace_tilt_deg': MAX_BRACE_TILT},
        'spawn_marker': {'pos': [120, 250, 18], 'min_clearance': 40, 'band': [0, 128]},
        'pieces': pieces}
    L.resolve_pieces(cfg, index)                               # fail closed before writing
    found, hinge = checks(pieces, index)
    blocking = {k: v for k, v in found.items() if k != 'door_swing_other'}
    report = {'pieces': len(pieces), 'by_role': {r: sum(p['role'] == r for p in pieces) for r in L.ROLES},
              'hinge_world': [round(v, 2) for v in hinge], 'violations': found,
              'door_other_side_also_clear': 'door_swing_other' not in found,
              'layout_sha256': hashlib.sha256(json.dumps(cfg['tower_v11'], sort_keys=True).encode()).hexdigest()}
    print(json.dumps(report, indent=1))
    if blocking: raise SystemExit('layout enters a protected space: %s' % sorted(blocking))
    (ROOT/'config.json').write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    (ROOT/'reports/v11_layout_design.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('V11_LAYOUT_WRITTEN', len(pieces), 'pieces')

if __name__ == '__main__': main()
