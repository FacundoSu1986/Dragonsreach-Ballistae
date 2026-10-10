"""Rustic primitives of the v11 tower, measured on the generated meshes (plan task 6)."""
import math, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import rustico_v11 as R

def sub(a, b): return [p - q for p, q in zip(a, b)]
def dot(a, b): return sum(p*q for p, q in zip(a, b))
def norm(a): return math.sqrt(dot(a, a))
def mean(ps): return [sum(p[i] for p in ps)/len(ps) for i in range(3)]

def point_line(p, a, b):
    d = sub(b, a); t = dot(sub(p, a), d)/dot(d, d)
    return norm(sub(p, [a[i] + t*d[i] for i in range(3)]))

def newell(ps):
    """Unit normal of a planar polygon given in order (Newell's method)."""
    n = [0.0, 0.0, 0.0]
    for p, q in zip(ps, ps[1:] + ps[:1]):
        n[0] += (p[1] - q[1])*(p[2] + q[2]); n[1] += (p[2] - q[2])*(p[0] + q[0]); n[2] += (p[0] - q[0])*(p[1] + q[1])
    return [v/norm(n) for v in n]

LOG = dict(name='tronco_test', a=(0, 0, 0), b=(0, 0, 400), r0=20.0, seed=1105)
# The builder makes logs from short braces to 450 u stilts; every guarantee must hold for each one.
LOGS = [dict(name='tronco_%d' % k, a=(k, -k, 3*k), b=(k + 30, 50 - k, 3*k + 100 + 12*k), r0=8 + k % 15, seed=1105)
        for k in range(30)]

class Tronco(unittest.TestCase):
    def rings(self, m): return [[m['verts'][i] for i in ring] for ring in m['rings']]
    def test_misma_semilla_misma_malla(self):
        m = R.tronco(**LOG)
        self.assertEqual(R.tronco(**LOG), m)
        self.assertNotEqual(R.tronco(**dict(LOG, seed=7))['verts'], m['verts'])
    def test_eje_curvado_al_menos_1_por_ciento(self):
        for spec in LOGS:
            m = R.tronco(**spec); centers = [mean(r) for r in self.rings(m)]
            bend = max(point_line(c, centers[0], centers[-1]) for c in centers)
            self.assertTrue(0.01*m['meta']['length'] <= bend <= 0.03*m['meta']['length'], spec['name'])
    def test_conicidad_8_a_20_por_ciento(self):
        # The end cut moves vertices along the axis only, so the end rings keep their radius.
        for spec in LOGS:
            m = R.tronco(**spec); rings = self.rings(m); c0, c1 = mean(rings[0]), mean(rings[-1])
            r0, r1 = [sum(point_line(p, c0, c1) for p in r)/len(r) for r in (rings[0], rings[-1])]
            taper = 1 - min(r0, r1)/max(r0, r1)
            self.assertTrue(0.08 <= taper <= 0.20, (spec['name'], taper))
    def test_cortes_de_punta_en_rango_y_distintos(self):
        for spec in LOGS:
            m = R.tronco(**spec); rings = self.rings(m)
            axis = sub(mean(rings[-1]), mean(rings[0])); axis = [v/norm(axis) for v in axis]
            cuts = [math.degrees(math.acos(min(1, abs(dot(newell(r), axis))))) for r in (rings[0], rings[-1])]
            self.assertTrue(all(1.9 <= c <= 12.1 for c in cuts), (spec['name'], cuts))
            self.assertGreater(abs(cuts[0] - cuts[1]), 0.5, spec['name'])
    def test_curvatura_forzada_de_costado(self):
        # A joist along x may only crook along y: its ring centres keep their height.
        for k in range(20):
            m = R.tronco(name='vigueta_%d' % k, a=(-296, 0, 434), b=(296, 0, 434), r0=11, seed=1105, bend_dir=(0, 1, 0))
            centers = [mean(r) for r in self.rings(m)]
            # Ridged bark moves a ring's centroid off the axis by up to ridge*r (0.55 u here); a
            # vertical crook would move it 6-13 u.
            self.assertLess(max(abs(c[2] - 434) for c in centers), 0.6)
            self.assertGreaterEqual(max(abs(c[1]) for c in centers), 0.01*592 - 0.6)
    def test_caras_validas(self):
        m = R.tronco(**LOG); n = len(m['verts'])
        self.assertTrue(all(len(f) >= 3 and all(0 <= i < n for i in f) for f in m['faces']))
        self.assertEqual(len(m['uvs']), n)
    def test_radio_para_la_soga(self):
        # axis_at + radius_at never under-report the bark: a rope placed with them cannot sink into the log.
        for spec in LOGS:
            m = R.tronco(**spec); rings = self.rings(m)
            ax = sub(spec['b'], spec['a']); ax = [v/norm(ax) for v in ax]
            for k, ring in enumerate(rings):
                t = k/(len(rings) - 1); c = R.axis_at(m, t)
                bark = max(norm([w - dot(sub(p, c), ax)*a_ for w, a_ in zip(sub(p, c), ax)]) for p in ring)
                self.assertLessEqual(bark, R.radius_at(m, t) + 1e-6, (spec['name'], k))
                self.assertGreater(bark, 0.9*R.radius_at(m, t), (spec['name'], k))

PLANK = dict(name='tablon_test', center=(0, 0, 453.95), axis=(1, 0, 0), up=(0, 0, 1), length=120.0, width=24.0, thickness=8.0, seed=1105)

class Tablon(unittest.TestCase):
    def test_variaciones_en_rango(self):
        for k in range(40):
            m = R.tablon(**dict(PLANK, name='tablon_%d' % k))
            v = m['verts']; xs = [p[0] for p in v]; ys = [p[1] for p in v]
            self.assertLessEqual(max(ys) - min(ys), 24*1.15 + 2*4*math.sin(math.radians(1.2)) + 0.6)   # width plus twist and cut skew
            top = [p for p in v if p[2] > 453.95 - 4]
            self.assertTrue(all(abs(p[2] - 453.95) <= 24*1.15/2*math.sin(math.radians(1.2)) + 1e-6 for p in top))
            self.assertLessEqual(abs(max(xs) - 60), 12 + 24*1.15/2*math.tan(math.radians(4)) + 1e-6)
            self.assertLessEqual(abs(min(xs) + 60), 12 + 24*1.15/2*math.tan(math.radians(4)) + 1e-6)
            w = m['meta']['width']; self.assertTrue(24*0.85 - 1e-9 <= w <= 24*1.15 + 1e-9)
    def test_el_centro_de_la_cara_de_arriba_no_se_mueve(self):
        # Feet stand on the plank centre line: it stays on the collision top (spec §2, ±1.2 u).
        for k in range(40):
            m = R.tablon(**dict(PLANK, name='tablon_%d' % k))
            self.assertLessEqual(m['meta']['top_centre_deviation'], 1e-6)
            self.assertLessEqual(max(abs(p[2] - 453.95) for p in m['verts'] if p[2] > 450), 1.2)
    def test_misma_semilla_misma_malla(self):
        self.assertEqual(R.tablon(**PLANK), R.tablon(**PLANK))

def surface_points(m):
    """Vertices plus edge midpoints: a polygonal coil can pass inside the bark between its corners."""
    v = m['verts']; pts = list(v)
    for f in m['faces']:
        for a, b in zip(f, f[1:] + f[:1]): pts.append([(p + q)/2 for p, q in zip(v[a], v[b])])
    return pts

class Amarre(unittest.TestCase):
    def test_radio_interno_pegado_al_tronco(self):
        for k in range(30):
            m = R.amarre(name='amarre_%d' % k, center=(10, 20, 200), axis=(0, 0, 1), radius=18.0, seed=1105)
            inner = min(math.hypot(p[0] - 10, p[1] - 20) for p in surface_points(m))
            self.assertTrue(18.0 <= inner <= 18.6, inner)
            self.assertTrue(3 <= m['meta']['coils'] <= 5)
    def test_soga_de_seccion_triangular(self):
        # Three tube sides put the rope's inner face half a tube from the coil line, not a whole one.
        for k in range(20):
            m = R.amarre(name='amarre_t%d' % k, center=(0, 0, 0), axis=(0, 0, 1), radius=18.0, seed=1105, tube=1.6, ring_sides=8, tube_sides=3)
            inner = min(math.hypot(p[0], p[1]) for p in surface_points(m))
            self.assertTrue(18.0 <= inner <= 18.6, inner)
    def test_eje_inclinado(self):
        n = math.sqrt(2.04); axis = (1/n, 1/n, 0.2/n)
        m = R.amarre(name='amarre_x', center=(0, 0, 0), axis=axis, radius=15.0, seed=3)
        inner = min(norm(sub(p, [dot(p, axis)*c for c in axis])) for p in surface_points(m))
        self.assertTrue(15.0 <= inner <= 15.6, inner)

if __name__ == '__main__': unittest.main()
