"""Own rustic geometry of the v11 tower in game units (pure Python, spec §2).

What torre.nif draws besides the v04 turntable: deck planks and joists, the landing, the railing
with its tall corner posts, the stair (log stringers, plank treads, handrails and their supports),
the room's front wall with its door frame, and rope lashings at the joints. The vanilla stilts,
braces, room walls and door are references placed by the ESP (config.json -> tower_v11); this
module only reads them to rest the own logs on them and to size the ropes around them.

build_tower_v11.py turns `build(cfg)` into Blender meshes; tests/test_v11_tower.py checks it here.
Every part: {'name', 'verts', 'faces', 'uvs' (Blender UV, V already flipped), 'mats' (one key per
face), 'kind'}. UVs follow the measured vanilla layouts: StockadeWood01 bark along V (~162 u per
V, a band of ~0.0025 U per unit around, clear of the seam at U 0.65), StockadeExtra01 end grain
around (0.755, 0.445) of the NIF, StockadePlanks01 one clean board stripe per plank, Rope01 rope
along U (53.6 u per U) in the NIF band V 0.79-0.98.
"""
import math, random, zlib
import rustico_v11 as R
import v11_layout as L

BOX_PREFIXES = ('Baranda_poste_', 'Pared_frente_', 'Marco_puerta_')
UNITS = 70.0
# v10 stair (build_stairs.py, metres x 70): ramp, landing and edge barriers are invariants.
SX0, SX1, SY1, SZ1 = 4.02*UNITS, 5.22*UNITS, 2.8*UNITS, 6.485*UNITS
SLOPE = 3.225/5.2
SY0 = SY1 - SZ1/SLOPE
COUNT = 34
TREAD, RISE = (SY1 - SY0)/COUNT, SZ1/COUNT
STRINGER_X = ((4.02 + .06)*UNITS, (5.22 - .06)*UNITS)      # where v10 had its stringers and pilars
def ramp_z(y): return SZ1*(y - SY0)/(SY1 - SY0)

DECK_TOP, PLANK_T, TREAD_T = 453.95, 8.0, 10.5
LANDING_X = (280.0, 365.4)
POST_TOP = 531.65                       # v10 railing posts
RAIL_Z = (492.0, 524.0)
HANDRAIL_ABOVE_RAMP = 74.0              # the edge barrier tops at the ramp + 73.5
STRINGER_TOP_BELOW_RAMP = 18.0          # tread 10.5 + half riser 6.7, rounded up
WALL_Y = (-121.0, -115.0)               # front wall planks, inside the room's front line (-128..-108)
DOOR_HALF, DOOR_TOP = 50.0, 178.0       # opening for FarmhouseAnimDoor01 (96 x 176)
# Frame logs stand 5 u outside the wall line: the leaf's hinge-side corner on the room face sweeps up
# to 5 u past the hinge line while opening (measured on the vanilla leaf), but only inside the wall plane.
FRAME_Y = WALL_Y[0] - 2.0
PLANK_STRIPES = ((0.16, 0.26), (0.36, 0.44), (0.55, 0.63), (0.645, 0.735), (0.75, 0.84), (0.855, 0.945))
DECK_PATTERNS = (((-280, -128), (-128, 128), (128, 280)), ((-280, 128), (128, 280)),
                 ((-280, -128), (-128, 280)), ((-280, 280),))
DECK_WEIGHTS = (0.3, 0.3, 0.3, 0.1)

def _add(a, b): return tuple(p + q for p, q in zip(a, b))
def _sub(a, b): return tuple(p - q for p, q in zip(a, b))
def _mul(a, k): return tuple(p*k for p in a)
def _dot(a, b): return sum(p*q for p, q in zip(a, b))
def _norm(a): return math.sqrt(_dot(a, a))

class Tower:
    def __init__(self, cfg):
        self.cfg = cfg; self.lay = cfg['tower_v11']; self.irr = self.lay['irregularity']; self.seed = self.irr['seed']
        self.parts, self.boxes, self.logs, self.planks, self.ropes = [], [], [], [], []
        self.supports = []                  # handrail supports: never collision (spec, invariants)
    def rng(self, name): return random.Random((self.seed*7919) ^ zlib.crc32(name.encode('utf-8')))

    # ---- primitives into parts -----------------------------------------------------------
    def log(self, name, a, b, r, sides=7, ring_step=60.0, bend=None, taper=None, bend_dir=None, offset_dir=None,
            box=False, lean=None):
        """A log; with offset_dir, a and b are points of its surface and the axis sits one radius away."""
        kw = dict(sides=sides, ring_step=ring_step, bend_dir=bend_dir)
        if bend: kw['bend'] = bend
        kw['taper'] = taper or tuple(self.irr['log_taper'])
        first = R.tronco(name, a, b, r, self.seed, **kw)
        if offset_dir is not None:
            ra, rb = first['meta']['radius_a'], first['meta']['radius_b']
            a, b = _add(a, _mul(offset_dir, ra)), _add(b, _mul(offset_dir, rb))
            first = R.tronco(name, a, b, r, self.seed, **kw)
        m = first; rng = self.rng(name + ':uv')
        span = 2*math.pi*r*0.0025
        u0 = rng.uniform(0.02, 0.63 - span)
        v0 = rng.uniform(0.0, 1.0)
        caps = {i for f in m['faces'][m['cap_face_start']:] for i in f}
        uvs = [(0.755 + (p - 0.5)*0.09, 0.555 + (q - 0.5)*0.09) if i in caps else (u0 + p*span, v0 + q/162.0)
               for i, (p, q) in enumerate(m['uvs'])]
        mats = ['stockade_wood']*m['cap_face_start'] + ['stockade_extra']*(len(m['faces']) - m['cap_face_start'])
        self.parts.append({'name': name, 'verts': m['verts'], 'faces': m['faces'], 'uvs': uvs, 'mats': mats, 'kind': 'log'})
        meta = dict(m['meta'], name=name, lean_deg=lean)
        self.logs.append(meta)
        if box: self.add_box(name, m['verts'])
        return m

    def post(self, name, x, y, z0, z1, r, lean_range, sides=7, box=False, ring_step=60.0, lean_dir=None):
        rng = self.rng(name + ':lean'); lean = rng.uniform(*lean_range); psi = rng.uniform(0, 2*math.pi)
        if lean_dir is not None:     # same draws; the lean only points within 30 degrees of lean_dir
            psi = math.atan2(lean_dir[1], lean_dir[0]) + (psi/math.pi - 1)*math.radians(30)
        h = z1 - z0; dx = h*math.tan(math.radians(lean))
        return self.log(name, (x, y, z0), (x + dx*math.cos(psi), y + dx*math.sin(psi), z1), r, sides=sides,
                        ring_step=ring_step, box=box, lean=lean)

    def plank(self, name, center, axis, up, length, width, thickness, fixed_width=False, kind='plank', twist=None):
        m = R.tablon(name, center, axis, up, length, width, thickness, self.seed,
                     width_var=0.0 if fixed_width else self.irr['plank_width_variation'], end_shift=0.0,
                     twist=self.irr['plank_twist_deg'] if twist is None else twist, cut=3.0, segments=2)
        rng = self.rng(name + ':uv'); lo, hi = rng.choice(PLANK_STRIPES); v0 = rng.uniform(0.0, 1.0); w = m['meta']['width']
        uvs = [(lo + (p/w)*(hi - lo), v0 + q/256.0) for p, q in m['uvs']]
        # Per face corner: the board stripe across the top and bottom; a narrow slice of the same
        # board on the long edges and ends (shared corners would stretch one texel column there).
        depth = lambda i: 0.0 if i % 4 in (0, 1) else 1.0           # tablon: two top corners, then two bottom
        face_uvs = []
        for k, f in enumerate(m['faces']):
            q = k % 4 if k < len(m['faces']) - 2 else None
            if q in (0, 2): face_uvs.append([uvs[i] for i in f])
            elif q in (1, 3): face_uvs.append([(lo + 0.004 + 0.02*depth(i), uvs[i][1]) for i in f])
            else: face_uvs.append([(uvs[i][0], v0 + 0.02*depth(i)) for i in f])
        self.parts.append({'name': name, 'verts': m['verts'], 'faces': m['faces'], 'uvs': uvs, 'face_uvs': face_uvs,
                           'mats': ['stockade_planks']*len(m['faces']), 'kind': kind})
        self.planks.append(dict(m['meta'], name=name, length=length))
        return m

    def plank_width(self, name, width):
        return R.tablon(name, (0, 0, 0), (1, 0, 0), (0, 0, 1), 100.0, width, 8.0, self.seed,
                        width_var=self.irr['plank_width_variation'], end_shift=0.0)['meta']['width']

    def rope(self, name, center, axis, radius, wraps):
        m = R.amarre(name, center, axis, radius, self.seed, coils=(2, 3), tube=1.6, ring_sides=8, tube_sides=3)
        c = m['meta']['circumference']
        uvs = [(p*c/53.6, 0.02 + q*0.19) for p, q in m['uvs']]
        self.parts.append({'name': name, 'verts': m['verts'], 'faces': m['faces'], 'uvs': uvs,
                           'mats': ['rope']*len(m['faces']), 'kind': 'rope'})
        self.ropes.append({'name': name, 'center': list(center), 'axis': list(axis), 'bark_radius': radius,
                           'inner_radius': m['meta']['inner_radius'], 'wraps': wraps})

    def add_box(self, name, verts):
        lo = [min(v[i] for v in verts) for i in range(3)]; hi = [max(v[i] for v in verts) for i in range(3)]
        if name.startswith('Baranda_poste_'): lo[2] = max(lo[2], DECK_TOP)   # the floor below is its own box
        if name.startswith(('Pared_frente_', 'Marco_puerta_')): lo[2] = max(lo[2], 0.0)
        self.boxes.append({'name': name, 'min': lo, 'max': hi})

    # ---- structure -------------------------------------------------------------------------
    def joists(self):
        """Logs along x on the piling rows and along y on the east and west piling lines, resting on the pile tops."""
        top = self.lay['platform']['pile_top']; grid = self.lay['platform']['grid']
        flat = dict(r=11.0, sides=9, taper=(0.08, 0.10), offset_dir=(0, 0, 1))
        for y in grid:
            x1 = 375.0 if y == grid[-1] else 296.0          # the north joist also carries the landing
            self.log('Vigueta_y%+04d' % y, (-296.0, y, top), (x1, y, top), bend_dir=(0, 1, 0), **flat)
        for x in (grid[0] - 4, grid[-1] + 4):
            self.log('Viga_borde_x%+04d' % x, (x, -296.0, top), (x, 296.0, top), bend_dir=(1, 0, 0), **flat)
        self.log('Vigueta_descanso', (250.0, 205.0, top), (375.0, 205.0, top), bend_dir=(0, 1, 0), **flat)

    def deck(self):
        """Planks along y across the joists; joints sit over a joist, a few run the full depth."""
        x, k, cols = -280.0, 0, []
        while 280.0 - x > 56.0:
            rng = self.rng('Tablon_columna_%02d' % k); pattern = rng.choices(DECK_PATTERNS, DECK_WEIGHTS)[0]
            names = ['Tablon_azotea_%02d_%d' % (k, j) for j in range(len(pattern))]
            w = max(self.plank_width(n, 28.0) for n in names)
            cols.append((k, x + 0.4 + w/2, w, pattern, names, False)); x += w + 0.8; k += 1
        rest = 280.0 - x; n = 2 if rest > 36.0 else 1
        for j in range(n):
            w = rest/n - 0.8; rng = self.rng('Tablon_columna_%02d' % k); pattern = rng.choices(DECK_PATTERNS, DECK_WEIGHTS)[0]
            cols.append((k, x + 0.4 + w/2, w, pattern, ['Tablon_azotea_%02d_%d' % (k, s) for s in range(len(pattern))], True))
            x += w + 0.8; k += 1
        for k, xc, w, pattern, names, fixed in cols:
            for (ya, yb), name in zip(pattern, names):
                rng = self.rng(name + ':ends')
                y0 = -280.0 - rng.uniform(-self.irr['plank_end_shift_units'], 6.0) if ya == -280 else ya + 1.2
                y1 = 280.0 + rng.uniform(-self.irr['plank_end_shift_units'], 6.0) if yb == 280 else yb - 1.2
                self.plank(name, (xc, (y0 + y1)/2, DECK_TOP), (0, 1, 0), (0, 0, 1), y1 - y0, w if fixed else 28.0, PLANK_T, fixed_width=fixed, kind='deck')
        return cols

    def landing(self):
        x, k, start = LANDING_X[0] + 0.4, 0, LANDING_X[0]
        widths = []
        for k in range(2):
            name = 'Tablon_descanso_%d' % k; w = self.plank_width(name, 28.0); widths.append((name, w, False))
        widths.append(('Tablon_descanso_2', LANDING_X[1] - start - sum(w + 0.8 for _n, w, _f in widths) - 0.8, True))
        x = start
        for name, w, fixed in widths:
            rng = self.rng(name + ':ends'); y0 = SY1 + 0.6; y1 = 280.0 + rng.uniform(-self.irr['plank_end_shift_units'], 6.0)
            self.plank(name, (x + 0.4 + w/2, (y0 + y1)/2, DECK_TOP), (0, 1, 0), (0, 0, 1), y1 - y0, w if fixed else 28.0, PLANK_T, fixed_width=fixed, kind='landing')
            x += w + 0.8

    def railing(self):
        """The v10 post line (50 posts, ~45 u apart), six of them tall, and two log rails per side."""
        line = [('O', (-273.0, -273.0 + 45.5*k)) for k in range(13)]
        line += [('S', (-273.0 + 45.5*k, -273.0)) for k in range(1, 13)]
        line += [('E', (273.0, -273.0 + 46.3*k)) for k in range(1, 11)]
        line += [('N', (-273.0 + (358.0 + 273.0)/13*k, 273.0)) for k in range(1, 14)]
        line += [('D', (358.0, 196.0)), ('D', (358.0, 234.5))]
        tall = {(-273.0, -273.0), (-273.0, 273.0), (273.0, -273.0), (358.0, 273.0), (273.0, round(-273.0 + 46.3*10, 6)), (358.0, 196.0)}
        posts = {}
        for side, (x, y) in line:
            key = (round(x, 6), round(y, 6)); is_tall = key in tall
            name = 'Baranda_poste_%s_%+04d_%+04d' % ('alto' if is_tall else side, round(x), round(y))
            rng = self.rng(name + ':top')
            if is_tall:
                # Corner posts lean outwards; the two at the stair's head lean away from the stair.
                lean_dir = {(273.0, 190.0): (-1.0, 0.0), (358.0, 196.0): (1.0, 0.0)}.get(key, (x, y))
                m = self.post(name, x, y, DECK_TOP - 6, self.lay['corner_posts']['top_z'] + rng.uniform(-5, 0), 10.0, (0.5, 1.5),
                              sides=9, box=True, lean_dir=lean_dir)
            else:
                m = self.post(name, x, y, DECK_TOP - 6, POST_TOP + rng.uniform(-3.0, 6.0), rng.uniform(5.5, 6.5), tuple(self.irr['log_tilt_deg']), box=True)
            posts[key] = (name, m, is_tall)
        # Rails: outside the post line, except on the east side, where the stair climbs right outside it.
        sides = {'O': ([(-273.0, -273.0 + 45.5*k) for k in range(13)], (-1, 0, 0)),
                 'S': ([(-273.0 + 45.5*k, -273.0) for k in range(13)], (0, -1, 0)),
                 'E': ([(273.0, -273.0 + 46.3*k) for k in range(11)], (-1, 0, 0)),
                 'N': ([(-273.0 + (358.0 + 273.0)/13*k, 273.0) for k in range(14)], (0, 1, 0)),
                 'D': ([(358.0, 196.0), (358.0, 234.5), (358.0, 273.0)], (1, 0, 0))}
        joints = []
        for side, (pts, out) in sides.items():
            cuts = list(range(0, len(pts) - 1, 4)) + [len(pts) - 1]
            for h, z in zip(('bajo', 'alto'), RAIL_Z):
                for s, (i, j) in enumerate(zip(cuts, cuts[1:])):
                    name = 'Baranda_riel_%s_%s_%d' % (side, h, s); rng = self.rng(name)
                    r = rng.uniform(4.5, 5.5); off = 6.0 + r
                    a = _add((pts[i][0], pts[i][1], z), _mul(out, off)); b = _add((pts[j][0], pts[j][1], z), _mul(out, off))
                    d = _sub(b, a); d = _mul(d, 1/_norm(d))
                    a, b = _sub(a, _mul(d, 5.0)), _add(b, _mul(d, 5.0))      # ends reach into the end posts
                    self.log(name, a, b, r, bend=(0.003, 0.008), bend_dir=out)
                    if h == 'bajo' and 0 < j < len(pts) - 1: joints.append((pts[j], out, z))
        return posts, joints

    def stair(self):
        """Log stringers, plank treads on the ramp line, handrails on supports without collision."""
        for x, tag in zip(STRINGER_X, ('int', 'ext')):
            y0, y1 = SY0 - 30.0, SY1 + 4.0
            # The stringer's bottom line runs where the stair stilts end; its top stays 18-20 u under the
            # ramp line (thick to thin end), below every tread.
            drop = self.lay['stair']['pile_drop']
            a = (x, y0, ramp_z(y0) - drop); b = (x, y1, ramp_z(y1) - drop)
            d = _sub(b, a); n = (0.0, -d[2], d[1]); n = _mul(n, 1/_norm(n))      # perpendicular to the ramp, upwards
            # A 760 u stringer with the usual 1-2 % crook would leave its stilts by up to 17 u.
            self.log('Zanca_%s' % tag, a, b, 10.0, sides=9, bend=(0.003, 0.008), taper=(0.08, 0.10), bend_dir=(1, 0, 0), offset_dir=n)
        for i in range(COUNT):
            y = SY0 + (i + .5)*TREAD; z = (i + .5)*RISE
            name = 'Peldano_%02d' % i; rng = self.rng(name + ':ends'); sh = rng.uniform(-3.0, 3.0)
            self.plank(name, ((SX0 + SX1)/2 + sh, y, z), (1, 0, 0), (0, 0, 1), SX1 - SX0, TREAD*0.97, TREAD_T, kind='tread')
        # Handrail supports: newel at the foot, nine along each side; the tall railing posts end the rails on top.
        ys = [SY0 + 8.0] + [SY0 + 45.0 + k*(SY1 - 90.0 - SY0)/8 for k in range(9)]
        joints = []
        for x, tag in zip(STRINGER_X, ('int', 'ext')):
            for k, y in enumerate(ys):
                name = 'Pasamanos_soporte_%s_%d' % (tag, k)
                z0 = max(-8.0, ramp_z(y) - STRINGER_TOP_BELOW_RAMP - 4.0); z1 = ramp_z(y) + HANDRAIL_ABOVE_RAMP + 6.0
                m = self.post(name, x, y, z0, z1, 7.0 if k == 0 else 4.5, (0.5, 2.0), sides=7)
                self.supports.append({'name': name, 'min': [min(v[i] for v in m['verts']) for i in range(3)],
                                      'max': [max(v[i] for v in m['verts']) for i in range(3)]})
                if k in (3, 6): joints.append(((x, y), ramp_z(y) + HANDRAIL_ABOVE_RAMP))
            top_post = (273.0, -273.0 + 46.3*10) if tag == 'int' else (358.0, 196.0)
            stops = [ys[0], ys[3], ys[6], top_post[1]]
            for s, (ya, yb) in enumerate(zip(stops, stops[1:])):
                name = 'Pasamanos_%s_%d' % (tag, s)
                xa, xb = x, (top_post[0] + x)/2 if s == len(stops) - 2 else x
                self.log(name, (xa, ya - 4.0, ramp_z(ya - 4.0) + HANDRAIL_ABOVE_RAMP), (xb, yb + 4.0, ramp_z(min(yb + 4.0, SY1)) + HANDRAIL_ABOVE_RAMP),
                         4.5, bend=(0.003, 0.008), bend_dir=(1, 0, 0))
        return joints

    def front_wall(self):
        """Vertical planks of the room's front with the door opening, battens and a log frame."""
        jamb_r = 7.0
        for side, (xa, xb) in (('izq', (-128.0, -DOOR_HALF - jamb_r)), ('der', (DOOR_HALF + jamb_r, 128.0))):
            span = xb - xa; names = ['Pared_frente_%s_tabla_%d' % (side, k) for k in range(3)]
            widths = [self.plank_width(n, 24.0) for n in names[:2]]
            widths.append(span - sum(w + 0.6 for w in widths) - 0.6)
            verts = []; x = xa
            for name, w, fixed in zip(names, widths, (False, False, True)):
                rng = self.rng(name + ':ends'); z0 = -6.0 - rng.uniform(0.0, 2.0); z1 = 192.0 - rng.uniform(0.0, 1.5)
                m = self.plank(name, (x + 0.3 + w/2, WALL_Y[0], (z0 + z1)/2), (0, 0, 1), (0, -1, 0), z1 - z0, w if fixed else 24.0, WALL_Y[1] - WALL_Y[0],
                               fixed_width=fixed, kind='wall')
                verts += m['verts']; x += w + 0.6
            for k, z in enumerate((40.0, 150.0)):
                name = 'Pared_frente_%s_liston_%d' % (side, k)
                m = self.log(name, (xa - 2.0, WALL_Y[0] - 4.0, z), (xb + 2.0, WALL_Y[0] - 4.0, z), 4.0, sides=6, bend=(0.003, 0.008), bend_dir=(0, 0, 1))
                verts += m['verts']
            self.add_box('Pared_frente_' + side, verts)
        for side, x in (('izq', -DOOR_HALF - jamb_r), ('der', DOOR_HALF + jamb_r)):
            self.log('Marco_puerta_' + side, (x, FRAME_Y, -4.0), (x, FRAME_Y, 186.0), jamb_r, sides=8,
                     bend=(0.003, 0.006), bend_dir=(0, 1, 0), box=True)
        self.log('Marco_puerta_dintel', (-DOOR_HALF - 2*jamb_r - 6, FRAME_Y, 184.0), (DOOR_HALF + 2*jamb_r + 6, FRAME_Y, 184.0),
                 jamb_r, sides=8, bend=(0.003, 0.006), taper=(0.08, 0.10), bend_dir=(0, 1, 0), box=True)

    # ---- rope lashings ---------------------------------------------------------------------
    def vanilla_ropes(self):
        """One lashing per stilt at its highest brace joint, sized on the stilt's own vanilla mesh."""
        import numpy as np
        pieces = {p['name']: p for p in self.lay['pieces']}
        axes = {}
        for p in pieces.values():
            m = L.piece_matrix(p); R_ = np.array(m['r'])
            axes[p['name']] = (np.array(m['t']), R_ @ np.array([0.0, 1.0, 0.0]))
        joints = {}
        for p in pieces.values():
            if p['role'] != 'cruz': continue
            pb, db = axes[p['name']]
            for pile in p['joins']:
                pa, da = axes[pile]; w = pa - pb; a_, b_, c_ = da @ da, da @ db, db @ db
                den = a_*c_ - b_*b_
                if den < 1e-9: continue
                s = (b_*(db @ w) - c_*(da @ w))/den
                point = pa + s*da
                if pile not in joints or point[2] > joints[pile][2]: joints[pile] = point
        for p in pieces.values():                        # stair stilts: just under the stringer they carry
            if p['role'] == 'pilote' and p.get('supports') == 'escalera':
                pa, da = axes[p['name']]; da = da if da[2] > 0 else -da
                top = max((L.apply(L.piece_matrix(p), (0.0, sgn*152.7, 0.0)) for sgn in (1, -1)), key=lambda q: q[2])
                joints[p['name']] = np.array(top) - 14.0*da
        for pile, point in sorted(joints.items()):
            p = pieces[pile]; m = L.piece_matrix(p); R_ = np.array(m['r'])*m['s']
            world = L.mesh_vertices(p['modl'], self.cfg) @ R_.T + np.array(m['t'])
            pa, da = axes[pile]; da = da/np.linalg.norm(da)
            rel = world - point; along = rel @ da
            # The vanilla logs are low-poly: take the rings of vertices just below and just above the
            # joint and keep the larger radius, so the rope always clears the bark.
            lo = along[along <= 0].max() if (along <= 0).any() else along.min()
            hi = along[along >= 0].min() if (along >= 0).any() else along.max()
            near = rel[(along >= lo - 2.0) & (along <= hi + 2.0)]; radial = near - np.outer(near @ da, da)
            radius = float(np.linalg.norm(radial, axis=1).max())
            self.rope('Amarre_%s' % pile, tuple(float(v) for v in point), tuple(float(v) for v in da), radius, pile)

    def own_ropes(self, posts, rail_joints, handrail_joints):
        logs = {m['name']: m for m in self.logs}
        def on_post(name, z):
            meta = logs[name]; a, b = meta['a'], meta['b']; t = (z - a[2])/(b[2] - a[2])
            log = {'meta': meta}; c = R.axis_at(log, t); axis = _sub(b, a); axis = _mul(axis, 1/_norm(axis))
            self.rope('Amarre_' + name, c, axis, R.radius_at(log, t), name)
        for key, (name, m, is_tall) in sorted(posts.items()):
            if is_tall: on_post(name, RAIL_Z[0])
        for (xy, out, z) in rail_joints:
            key = (round(xy[0], 6), round(xy[1], 6))
            if key in posts and not posts[key][2]: on_post(posts[key][0], z)
        for (xy, z) in handrail_joints:
            name = next(s['name'] for s in self.supports
                        if s['min'][0] - 1 <= xy[0] <= s['max'][0] + 1 and s['min'][1] - 1 <= xy[1] <= s['max'][1] + 1 and not s['name'].endswith('_0'))
            on_post(name, z)

    # ---- totals ------------------------------------------------------------------------------
    def triangles(self):
        return sum(len(f) - 2 for p in self.parts for f in p['faces'])

def build(cfg):
    t = Tower(cfg)
    t.joists(); cols = t.deck(); t.landing()
    posts, rail_joints = t.railing()
    handrail_joints = t.stair()
    t.front_wall()
    t.vanilla_ropes(); t.own_ropes(posts, rail_joints, handrail_joints)
    counts = {'tablones_piso': sum(p['kind'] == 'deck' for p in t.parts), 'tablones_descanso': sum(p['kind'] == 'landing' for p in t.parts),
              'peldanos': sum(p['kind'] == 'tread' for p in t.parts), 'tablas_pared': sum(p['kind'] == 'wall' for p in t.parts),
              'troncos': sum(p['kind'] == 'log' for p in t.parts), 'amarres': sum(p['kind'] == 'rope' for p in t.parts),
              'postes_baranda': sum(p['name'].startswith('Baranda_poste_') for p in t.parts),
              'soportes_pasamanos': len(t.supports), 'columnas_piso': len(cols)}
    return {'parts': t.parts, 'boxes': t.boxes, 'logs': t.logs, 'planks': t.planks, 'ropes': t.ropes,
            'supports': t.supports, 'counts': counts, 'triangles': t.triangles()}
