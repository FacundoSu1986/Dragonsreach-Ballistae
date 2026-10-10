import math, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import v11_layout as L

class Transform(unittest.TestCase):
    def test_identidad(self):
        m = L.transform_matrix((1,2,3),(0,0,0),1.0,'XYZ',(1,1,1))
        self.assertEqual(L.apply(m,(0,0,0)),(1,2,3))
    def test_escala(self):
        m = L.transform_matrix((0,0,0),(0,0,0),1.45,'XYZ',(1,1,1))
        self.assertAlmostEqual(L.apply(m,(0,0,100))[2],145.0,6)
    def test_giro_z(self):
        m = L.transform_matrix((0,0,0),(0,0,90),1.0,'XYZ',(1,1,1))
        x,y,z = L.apply(m,(1,0,0)); self.assertAlmostEqual(x,0,6); self.assertAlmostEqual(abs(y),1,6)
    def test_orden_importa(self):
        a = L.transform_matrix((0,0,0),(30,40,50),1,'XYZ',(1,1,1))
        b = L.transform_matrix((0,0,0),(30,40,50),1,'ZYX',(1,1,1))
        self.assertNotEqual([round(v,6) for v in L.apply(a,(1,2,3))],[round(v,6) for v in L.apply(b,(1,2,3))])
    def test_todas_las_convenciones(self):
        self.assertEqual(len(L.all_conventions()),6*8)
    def test_solo_z_no_depende_de_la_convencion(self):
        ref = L.apply(L.transform_matrix((5,6,7),(0,0,37),1.2,'XYZ',(1,1,1)),(3,-2,9))
        for o,s in L.all_conventions():
            if s[2] != 1: continue
            got = L.apply(L.transform_matrix((5,6,7),(0,0,37),1.2,o,s),(3,-2,9))
            for a,b in zip(ref,got): self.assertAlmostEqual(a,b,9)


class Convention(unittest.TestCase):
    def test_convencion_decidida(self):
        import json
        d = json.loads((L.ROOT/'reports/angle_convention.json').read_text(encoding='utf-8'))
        self.assertTrue(d['decided'] and d['falsified'])
        o, s = L.engine_convention(); self.assertIn((o, s), L.all_conventions())
        self.assertEqual((o, s), ('ZYX', (-1, -1, -1)))  # R = Rx(-x)·Ry(-y)·Rz(-z), measured on Skyrim.esm

class Euler(unittest.TestCase):
    def test_ida_y_vuelta(self):
        import random
        rng = random.Random(7); o, s = L.engine_convention()
        for _ in range(300):
            rot = (rng.uniform(-180, 180), rng.uniform(-80, 80), rng.uniform(-180, 180))
            R = L.transform_matrix((0,0,0), rot, 1.0, o, s)['r']
            R2 = L.transform_matrix((0,0,0), L.euler_from_matrix(R), 1.0, o, s)['r']
            for i in range(3):
                for j in range(3): self.assertAlmostEqual(R[i][j], R2[i][j], 9)
    def test_gimbal_lock(self):
        # A vertical piling with its wide axis along +Y puts the decomposition exactly at b = 90 degrees.
        o, s = L.engine_convention()
        R = [[0,0,1],[1,0,0],[0,1,0]]
        R2 = L.transform_matrix((0,0,0), L.euler_from_matrix(R), 1.0, o, s)['r']
        for i in range(3):
            for j in range(3): self.assertAlmostEqual(R[i][j], R2[i][j], 9)
    def test_viga_vertical(self):
        # StockadeWoodbeam runs along local +Y; a piling sends it to world +Z.
        rot = L.rot_for_axes((0,0,1), (1,0,0))
        m = L.transform_matrix((0,0,0), rot, 1.0, *L.engine_convention())
        for local, world in (((0,1,0),(0,0,1)), ((1,0,0),(1,0,0)), ((0,0,1),(0,-1,0))):
            for a, b in zip(L.apply(m, local), world): self.assertAlmostEqual(a, b, 9)

class Resolve(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = L.load_cfg(); cls.index = L.esm_index(cls.cfg)
        cls.pieces = L.resolve_pieces(cls.cfg, cls.index)
    def test_todas_las_piezas_resuelven(self):
        self.assertTrue(40 <= len(self.pieces) <= 80, len(self.pieces))
        for p in self.pieces:
            self.assertEqual(p['formid'] & 0xFF000000, 0)        # Skyrim.esm
            self.assertFalse(p['edid'].lower().endswith('snow'))
            self.assertFalse(p['has_snow_material'])
        self.assertEqual(sum(p['role'] == 'puerta' for p in self.pieces), 1)
    def test_la_puerta_es_la_del_spec(self):
        door = next(p for p in self.pieces if p['role'] == 'puerta')
        self.assertEqual((door['edid'], door['formid'], door['type']), ('FarmhouseAnimDoor01', 0x000C78A3, 'DOOR'))
    def test_cada_cruz_y_viga_une_dos_pilotes(self):
        roles = {p['name']: p['role'] for p in self.pieces}
        for p in self.pieces:
            if p['role'] in ('cruz', 'viga'):
                self.assertEqual(len(p['joins']), 2, p['name'])
                self.assertTrue(all(roles[j] == 'pilote' for j in p['joins']), p['name'])
            if p['role'] == 'pilote': self.assertIn(p['supports'], ('plataforma', 'descanso', 'escalera'))
    def test_edid_falso_falla(self):
        import copy
        cfg = copy.deepcopy(self.cfg); cfg['tower_v11']['pieces'][0]['edid'] = 'NoExiste01'
        with self.assertRaises(ValueError): L.resolve_pieces(cfg, self.index)
    def test_modl_distinto_falla(self):
        import copy
        cfg = copy.deepcopy(self.cfg); cfg['tower_v11']['pieces'][0]['modl'] = 'x\\y.nif'
        with self.assertRaises(ValueError): L.resolve_pieces(cfg, self.index)
    def test_variante_con_nieve_falla(self):
        import copy
        cfg = copy.deepcopy(self.cfg); p = cfg['tower_v11']['pieces'][0]
        p['edid'] = 'StockadeWoodbeam01Light_SN'; p['modl'] = 'clutter\\stockade\\stockadewoodbeam01.nif'
        with self.assertRaises(ValueError): L.resolve_pieces(cfg, self.index)
    def test_nombre_repetido_falla(self):
        import copy
        cfg = copy.deepcopy(self.cfg); ps = cfg['tower_v11']['pieces']; ps[1]['name'] = ps[0]['name']
        with self.assertRaises(ValueError): L.resolve_pieces(cfg, self.index)

class DesignChecks(unittest.TestCase):
    """The layout guards in design_tower_v11.py must be able to fail (falsification)."""
    @classmethod
    def setUpClass(cls):
        import design_tower_v11 as D
        cls.D = D; cls.index = L.esm_index(L.load_cfg()); cls.pieces = D.design(cls.index)
    def moved(self, name, pos):
        import copy
        pieces = copy.deepcopy(self.pieces); next(p for p in pieces if p['name'] == name)['pos'] = list(pos)
        return self.D.checks(pieces, self.index)[0]
    def test_el_diseno_actual_pasa(self):
        found = self.D.checks(self.pieces, self.index)[0]
        self.assertEqual({k: v for k, v in found.items() if k != 'door_swing_other'}, {})
    def test_pieza_en_la_escalera(self):
        self.assertIn('viga_O_c', self.moved('viga_O_c', (323, -200, 300)).get('stair_walk_volume', []))
    def test_pieza_dentro_del_cuarto(self):
        self.assertIn('viga_O_c', self.moved('viga_O_c', (0, 0, 100)).get('room_interior', []))
    def test_pieza_en_la_entrada(self):
        self.assertIn('viga_S_c', self.moved('viga_S_c', (0, -200, 120)).get('entrance', []))
    def test_pieza_en_el_giro_de_la_puerta(self):
        found = self.moved('viga_S_c', (0, -60, 90))
        self.assertIn('viga_S_c', found.get('door_swing_open', []))
    def test_pieza_sobre_el_piso(self):
        self.assertIn('viga_N_c', self.moved('viga_N_c', (0, 262, 450)).get('above_deck_underside', []))

class Config(unittest.TestCase):
    def test_la_fuente_es_de_v11(self):
        # Copied configs used to open the previous version's source blend.
        self.assertEqual(Path(L.load_cfg()['source']).resolve().parents[1], L.ROOT.resolve())

if __name__ == '__main__': unittest.main()
