"""ESP of v11: vanilla references, the door, the navmesh around the room and stilts, the spawn marker (plan task 8)."""
import collections, json, math, struct, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]
import v11_layout as L
import build_plugin as P
from parser_esm import Plugin

ESP = ROOT/'mod/AstraAsedio.esp'

def load_esp():
    p = Plugin(str(ESP)); refs, nv = {}, None
    for t, o, _s, _d in p.recorrer():
        if t == 'REFR': refs[p.form_id(o)] = p.subrecords(p.datos(o))
        if t == 'NAVM': nv = dict(p.subrecords(p.datos(o)))['NVNM']
    return refs, nv

def parse_navmesh(nv):
    off = 16; vc = struct.unpack_from('<I', nv, off)[0]; off += 4
    vs = [struct.unpack_from('<3f', nv, off + 12*i) for i in range(vc)]; off += vc*12
    tc = struct.unpack_from('<I', nv, off)[0]; off += 4
    return vs, [struct.unpack_from('<3H3hHH', nv, off + 16*i) for i in range(tc)]

def contains(tri, x, y):
    (ax, ay, _), (bx, by, _), (cx, cy, _) = tri
    d = (by - cy)*(ax - cx) + (cx - bx)*(ay - cy)
    if abs(d) < 1e-9: return False
    l1 = ((by - cy)*(x - cx) + (cx - bx)*(y - cy))/d; l2 = ((cy - ay)*(x - cx) + (ax - cx)*(y - cy))/d
    return min(l1, l2, 1 - l1 - l2) >= -1e-6

def ground_triangle(vs, ts, x, y):
    for i, t in enumerate(ts):
        tri = [vs[j] for j in t[:3]]
        if max(v[2] for v in tri) <= 10 and contains(tri, x, y): return i
    return None

class VanillaReferences(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = L.load_cfg(); cls.pieces = L.resolve_pieces(cls.cfg)
        cls.refs, _nv = load_esp()
        cls.report = json.loads((ROOT/'reports/plugin_build.json').read_text())
    def test_una_referencia_por_pieza_con_su_transformacion(self):
        by_name = {r['name']: int(r['form_id'], 16) for r in self.report['vanilla_references']}
        self.assertEqual(set(by_name), {p['name'] for p in self.pieces})
        for p in self.pieces:
            fid = by_name[p['name']]; ss = self.refs[fid]; d = dict(ss); keys = [k for k, _v in ss]
            self.assertEqual(struct.unpack('<I', d['NAME'])[0], p['formid'], p['name'])
            data = struct.unpack('<6f', d['DATA'])
            for a, b in zip(data[:3], p['pos']): self.assertAlmostEqual(a, b, 3)
            for a, b in zip(data[3:], p['rot_deg']): self.assertAlmostEqual(a, math.radians(b), 5)
            self.assertEqual(keys[-1], 'DATA')                     # vanilla order: ... NAME, XSCL, DATA
            if abs(p['scale'] - 1) > 1e-9:
                self.assertAlmostEqual(struct.unpack('<f', d['XSCL'])[0], p['scale'], 5)
                self.assertEqual(keys.index('XSCL'), len(keys) - 2)
            else:
                self.assertNotIn('XSCL', d)
            self.assertLess(fid & 0xFFFFFF, 0xFFF)                 # the plugin stays ESL-compatible
    def test_la_puerta_es_vanilla_y_no_teletransporta(self):
        doors = [ss for ss in self.refs.values() if struct.unpack('<I', dict(ss)['NAME'])[0] == 0x000C78A3]
        # una en la celda de prueba y su copia en la celda del mundo (scripts/colocar_en_mundo.py)
        self.assertEqual(len(doors), 2)
        for door in doors:
            self.assertNotIn('XTEL', dict(door))
    def test_xscl_va_antes_de_data_como_en_skyrim_esm(self):
        esm = Plugin(str(L.esm_path(self.cfg))); seen = 0
        for t, o, _s, _d in esm.recorrer():
            if t != 'REFR': continue
            keys = [k for k, _v in esm.subrecords(esm.datos(o))]
            if 'XSCL' in keys:
                self.assertEqual(keys[-2:], ['XSCL', 'DATA']); seen += 1
                if seen == 50: break
        self.assertEqual(seen, 50)

class Navmesh(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = L.load_cfg(); _refs, nv = load_esp(); cls.vs, cls.ts = parse_navmesh(nv)
        cls.band = L.band_boxes(cls.cfg['tower_v11']['pieces'], cfg=cls.cfg)
        cls.report = json.loads((ROOT/'reports/plugin_build.json').read_text())
    def tri(self, t): return [self.vs[j] for j in t[:3]]
    def test_nada_dentro_del_cuarto(self):
        room = self.cfg['tower_v11']['room']; hx, hy = room['size'][0]/2, room['size'][1]/2
        for t in self.ts:
            c = [sum(v[i] for v in self.tri(t))/3 for i in range(3)]
            self.assertFalse(abs(c[0] - room['center'][0]) < hx and abs(c[1] - room['center'][1]) < hy and c[2] < 300, c)
    def test_limite_de_triangulos(self):
        self.assertLessEqual(len(self.ts), 32767)
    def test_el_suelo_esquiva_las_piezas_vanilla(self):
        for t in self.ts:
            tri = self.tri(t)
            if max(v[2] for v in tri) > 10: continue
            for b in self.band: self.assertFalse(P.triangle_blocked(tri, b), b['name'])
    def test_sin_las_piezas_vanilla_el_suelo_las_atravesaria(self):
        # Falsification: the same generator without the vanilla obstacles crosses at least one stilt.
        P.navmesh_geometry(vanilla_obstacles=False); vs, ts = P.LAST_NAVMESH
        hits = sum(1 for t in ts if max(vs[j][2] for j in t[:3]) <= 10 and any(P.triangle_blocked([vs[j] for j in t[:3]], b) for b in self.band))
        self.assertGreater(hits, 0)
    def test_se_llega_del_pie_de_la_escalera_a_la_puerta(self):
        start = ground_triangle(self.vs, self.ts, 323.4, -560.0); goal = ground_triangle(self.vs, self.ts, 0.0, -175.0)
        self.assertIsNotNone(start); self.assertIsNotNone(goal)
        seen = {start}; todo = [start]
        while todo:
            for j in self.ts[todo.pop()][3:6]:
                if j >= 0 and j not in seen: seen.add(j); todo.append(j)
        self.assertIn(goal, seen)
    def test_marcador_de_aparicion_libre(self):
        m = self.report['spawn_marker']; x, y, z = m['pos']; spec = self.cfg['tower_v11']['spawn_marker']
        room = self.cfg['tower_v11']['room']
        self.assertFalse(abs(x - room['center'][0]) < room['size'][0]/2 and abs(y - room['center'][1]) < room['size'][1]/2)
        self.assertIsNotNone(ground_triangle(self.vs, self.ts, x, y))
        obstacles = P.band_obstacles(self.cfg)
        clear = min(math.hypot(max(b['min'][0] - x, 0, x - b['max'][0]), max(b['min'][1] - y, 0, y - b['max'][1])) for b in obstacles)
        self.assertGreaterEqual(clear, spec['min_clearance'] - 1e-6)
        self.assertAlmostEqual(clear, m['clearance'], 3)

if __name__ == '__main__': unittest.main()
