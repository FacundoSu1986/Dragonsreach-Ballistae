"""Vanilla collision of the v11 layout: solids, the 0-128 u band and fail-closed reading (plan task 5)."""
import collections, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import v11_layout as L

class Band(unittest.TestCase):
    def test_cruz_en_x_solo_cuenta_su_pie(self):
        one = L.capsule_solid((0, 0, 0), (200, 0, 300), 5.0)
        two = L.capsule_solid((200, 0, 0), (0, 0, 300), 5.0)
        b1, b2 = L.band_box(one, 0, 128), L.band_box(two, 0, 128)
        self.assertLess(b1['max'][0], 100)        # not the whole 0..200 span of the cross
        self.assertGreater(b2['min'][0], 100)
        self.assertLessEqual(b1['max'][2], 128 + 1e-6)
    def test_fuera_de_la_franja_no_hay_caja(self):
        self.assertIsNone(L.band_box(L.capsule_solid((0, 0, 200), (100, 0, 300), 5.0), 0, 128))
    def test_la_caja_guarda_su_altura_real(self):
        # A pile under the stair stops 17.5 u below the ramp; its band box must not reach the band top.
        b = L.band_box(L.capsule_solid((0, 0, -50), (0, 0, 91), 5.0), 0, 128)
        self.assertAlmostEqual(b['max'][2], 96.0, delta=0.5)
        self.assertAlmostEqual(b['min'][2], 0.0, delta=1e-6)

class Pieces(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = L.load_cfg(); cls.pieces = cls.cfg['tower_v11']['pieces']
        cls.solids = {p['name']: L.piece_solids(p, cls.cfg) for p in cls.pieces}
        cls.band = {b['name'] for b in L.band_boxes(cls.pieces, cfg=cls.cfg)}
    def test_cada_pieza_tiene_colision(self):
        for name, solids in self.solids.items(): self.assertGreaterEqual(len(solids), 1, name)
    def test_pilotes_en_la_franja_y_lo_alto_fuera(self):
        for p in self.pieces:
            if p['role'] == 'pilote': self.assertIn(p['name'], self.band)
        for high in ('techo', 'cruz_S_1', 'cruz_N_2', 'viga_O_c'): self.assertNotIn(high, self.band)
    def test_pilote_escalado(self):
        p = next(p for p in self.pieces if p['role'] == 'pilote' and p['scale'] > 1.4)
        ys = [v[1] for s in L.collision_solids(p['modl'], self.cfg) for v in L.solid_vertices(s)]
        zs = [v[2] for s in self.solids[p['name']] for v in L.solid_vertices(s)]
        self.assertAlmostEqual(max(zs) - min(zs), p['scale']*(max(ys) - min(ys)), delta=2.0)
    def test_puerta_cerrada_en_su_vano(self):
        vs = [v for s in self.solids['puerta'] for v in L.solid_vertices(s)]
        self.assertTrue(-132 < min(v[1] for v in vs) and max(v[1] for v in vs) < -104)
        self.assertTrue(-52 < min(v[0] for v in vs) and max(v[0] for v in vs) < 52)
        self.assertTrue(-1 < min(v[2] for v in vs) and max(v[2] for v in vs) < 180)
    def test_pared_coincide_con_su_malla(self):
        vs = [v for s in self.solids['pared_N'] for v in L.solid_vertices(s)]
        for i, (lo, hi) in enumerate(((-128, 128), (108, 128), (-64, 192))):
            self.assertAlmostEqual(min(v[i] for v in vs), lo, delta=0.6); self.assertAlmostEqual(max(v[i] for v in vs), hi, delta=0.6)
    def test_triangulos_cerrados(self):
        for name in ('puerta', 'pared_N', 'techo', 'pilote_-262_-262', 'cruz_E_1', 'viga_S_i'):
            for solid in self.solids[name]:
                edges = collections.Counter()
                for tri in L.solid_triangles(solid):
                    keys = [tuple(round(c, 3) for c in v) for v in tri]
                    for a, b in ((0, 1), (1, 2), (2, 0)): edges[frozenset((keys[a], keys[b]))] += 1
                self.assertTrue(edges and all(n == 2 for n in edges.values()), name)
    def test_malla_mopp_falla_cerrada(self):
        with self.assertRaises(ValueError): L.collision_solids('clutter\\stockade\\stockadebarrier01.nif', self.cfg)
    def test_malla_sin_colision_falla_cerrada(self):
        with self.assertRaises(ValueError): L.collision_solids('clutter\\stockade\\stockadewall01.nif', self.cfg)
    def test_subir_un_pilote_lo_saca_de_la_franja(self):
        import copy
        p = copy.deepcopy(next(p for p in self.pieces if p['name'] == 'pilote_-262_-262')); p['pos'][2] += 400
        self.assertEqual(L.band_boxes([p], cfg=self.cfg), [])

if __name__ == '__main__': unittest.main()
