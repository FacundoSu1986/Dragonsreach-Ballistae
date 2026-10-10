"""Own geometry of the v11 tower (tower_v11_geometry.build), checked on the generated meshes (plan task 7)."""
import hashlib, json, math, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import v11_layout as L
import tower_v11_geometry as G
import rustico_v11 as R

def tops(part):
    """Top corners of every cross-section of a plank (tablon writes 4 corners per section, top ones first)."""
    v = part['verts']; return [v[i] for k in range(0, len(v), 4) for i in (k, k + 1)]

class Geometry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = L.load_cfg(); cls.out = G.build(cls.cfg)
        cls.parts = {p['name']: p for p in cls.out['parts']}
    def kind(self, k): return [p for p in self.out['parts'] if p['kind'] == k]

    def test_misma_semilla_misma_torre(self):
        digest = lambda o: hashlib.sha256(json.dumps(o['parts'], sort_keys=True).encode()).hexdigest()
        self.assertEqual(digest(G.build(self.cfg)), digest(self.out))

    def test_piso_cubierto_sin_solapes(self):
        cols = {}
        for p in self.kind('deck'):
            xs = [v[0] for v in p['verts']]; cols.setdefault(p['name'].split('_')[2], []).append((min(xs), max(xs)))
        spans = sorted((min(a for a, b in c), max(b for a, b in c)) for c in cols.values())
        self.assertLess(abs(spans[0][0] + 280), 1.0); self.assertLess(abs(spans[-1][1] - 280), 1.0)
        for (a0, a1), (b0, b1) in zip(spans, spans[1:]):
            self.assertGreaterEqual(b0, a1 - 1e-6)            # no two boards overlap (no z-fighting)
            self.assertLess(b0 - a1, 1.5)                       # and no wide cracks

    def test_superficie_pisable_a_1_2_u_de_la_colision(self):
        for p in self.kind('deck') + self.kind('landing'):
            self.assertLessEqual(max(abs(v[2] - G.DECK_TOP) for v in tops(p)), 1.2, p['name'])
        for p in self.kind('tread'):
            pts = tops(p); centre = [sum(q[i] for q in pts)/len(pts) for i in range(3)]
            # The ramp collision crosses each tread at its centre; the front and back edges sit +-6.7 u by design.
            self.assertLessEqual(abs(centre[2] - G.ramp_z(centre[1])), 1.2, p['name'])
            self.assertLessEqual(max(abs(v[2] - G.ramp_z(v[1])) for v in pts), G.RISE/2 + 2.0, p['name'])

    def test_una_caja_por_poste_y_ninguna_en_los_soportes(self):
        names = [b['name'] for b in self.out['boxes']]
        posts = [p for p in self.parts if p.startswith('Baranda_poste_')]
        self.assertEqual(sorted(n for n in names if n.startswith('Baranda_poste_')), sorted(posts))
        self.assertEqual(len(posts), 50)
        self.assertTrue(all(n.startswith(G.BOX_PREFIXES) for n in names))
        self.assertFalse(any(n.startswith(('Pasamanos', 'Baranda_riel')) for n in names))
        self.assertEqual(len(self.out['supports']), 20)

    def test_la_pared_del_frente_cierra_salvo_el_vano(self):
        front = [b for b in self.out['boxes'] if b['name'].startswith(('Pared_frente_', 'Marco_puerta_'))]
        def covered(x, z):
            return any(b['min'][0] <= x <= b['max'][0] and b['min'][2] <= z <= b['max'][2] and b['min'][1] <= -118 <= b['max'][1] for b in front)
        for z in range(2, 190, 4):
            for x in range(-127, 128, 2):
                if abs(abs(x) - G.DOOR_HALF) <= 1.5 and z < G.DOOR_TOP + 1.5 or abs(z - G.DOOR_TOP) <= 1.5 and abs(x) < G.DOOR_HALF + 1.5:
                    continue                                    # the opening's own edge (log radius and ridges)
                inside_opening = abs(x) < G.DOOR_HALF and z < G.DOOR_TOP
                self.assertEqual(covered(x, z), not inside_opening, (x, z))
        # The door (176.4 u, collision) fits under the frame with clearance.
        lintel = next(b for b in front if b['name'] == 'Marco_puerta_dintel')
        self.assertTrue(176.4 < lintel['min'][2] < G.DOOR_TOP + 1.0, lintel['min'][2])

    def test_nada_propio_ocupa_el_lugar_de_la_puerta(self):
        # FarmhouseAnimDoor01 closed: x +-48.5, y -127..-109, z 0..176.4 (its collision, layout task 5).
        for p in self.out['parts']:
            for v in p['verts']:
                self.assertFalse(-49 < v[0] < 49 and -127.5 < v[1] < -108.5 and 0.5 < v[2] < 176.5, p['name'])

    def test_las_sogas_no_se_hunden(self):
        for rope in self.out['ropes']:
            part = self.parts['Amarre_' + rope['wraps']] if 'Amarre_' + rope['wraps'] in self.parts else None
            part = part or next(p for p in self.out['parts'] if p['kind'] == 'rope' and p['name'].endswith(rope['wraps']))
            c, ax = rope['center'], rope['axis']
            pts = list(part['verts'])
            for f in part['faces']:
                for a, b in zip(f, f[1:] + f[:1]): pts.append([(p + q)/2 for p, q in zip(part['verts'][a], part['verts'][b])])
            d = min(math.sqrt(max(0.0, sum((p[i] - c[i])**2 for i in range(3)) - sum((p[i] - c[i])*ax[i] for i in range(3))**2)) for p in pts)
            self.assertGreaterEqual(d, rope['bark_radius'] - 1e-6, rope['name'])
            self.assertLessEqual(d, rope['bark_radius'] + 0.6, rope['name'])

    def test_viguetas_y_largueros_apoyan_en_los_pilotes(self):
        """Each stilt's top meets the underside of the log it carries (spec §4: gap under 2 u)."""
        pieces = {p['name']: p for p in self.cfg['tower_v11']['pieces']}
        logs = [m for m in self.out['logs'] if m['name'].startswith(('Vigueta', 'Viga_borde', 'Zanca'))]
        import numpy as np
        for pile in pieces.values():
            if pile['role'] != 'pilote': continue
            # The vanilla beam ends are cut at a slant. Every point of the top cut that lies under a log
            # is compared with that log's underside straight above it: the closest one must touch
            # (gap under 2 u) or sit inside the log (negative, at most the slant of the cut).
            V, _T = L.piece_mesh(pile, self.cfg); m = L.piece_matrix(pile)
            ax = np.array(m['r']) @ np.array([0.0, 1.0, 0.0]); ax = ax if ax[2] > 0 else -ax
            along = (V - np.array(m['t'])) @ ax; cut = V[along > along.max() - 12.0*pile['scale']]
            gaps = []
            # Each stilt is measured against what it is there to carry; other logs may cross it
            # (the outer stringer ends in a landing stilt like a tenon), as in any log joint.
            carries = {'plataforma': ('Vigueta_y', 'Viga_borde'), 'descanso': ('Vigueta_descanso', 'Vigueta_y+262'),
                       'escalera': ('Zanca',)}[pile['supports']]
            for meta in logs:
                if not meta['name'].startswith(carries): continue
                a, b = meta['a'], meta['b']; d = [q - p for p, q in zip(a, b)]
                cos_slope = math.hypot(d[0], d[1])/math.sqrt(sum(v*v for v in d))
                for q in cut:
                    t = ((q[0] - a[0])*d[0] + (q[1] - a[1])*d[1])/(d[0]**2 + d[1]**2)
                    if not 0 <= t <= 1: continue
                    c = R.axis_at({'meta': meta}, t); r = meta['radius_a'] + (meta['radius_b'] - meta['radius_a'])*t
                    side = abs((q[0] - c[0])*d[1] - (q[1] - c[1])*d[0])/math.hypot(d[0], d[1])   # across the log, horizontal
                    if side >= r: continue
                    gaps.append(c[2] - math.sqrt(r*r - side*side)/cos_slope - q[2])
            self.assertTrue(gaps, pile['name'])
            g = min(gaps)
            # Under a level log the cut sits at most its slant inside; under the 31.8 degree stringer the
            # underside also drops 0.62 u per unit across the stilt, so the downhill edge sits deeper.
            deepest = -16.0 if pile['supports'] == 'escalera' else -9.0
            self.assertTrue(deepest < g < 2.0, (pile['name'], g))

    def test_irregularidad(self):
        logs = self.out['logs']; irr = self.cfg['tower_v11']['irregularity']
        self.assertGreater(sum(m['bend_fraction'] >= 0.01 for m in logs), len(logs)/2)
        self.assertTrue(all(irr['log_taper'][0] <= m['taper'] <= irr['log_taper'][1] for m in logs))
        posts = [m for m in logs if m['lean_deg'] is not None]
        self.assertTrue(posts and all(0.5 <= m['lean_deg'] <= 3.0 for m in posts))
        for m in self.out['planks']:
            self.assertLessEqual(max(abs(t) for t in m['twist_deg']), irr['plank_twist_deg'])

    def test_presupuesto_de_triangulos(self):
        # verify_assets.py caps the three NIFs at 40 000 visual triangles; ballesta + virote use 20 600
        # and the kept v04 turntable about 1 700, so the own geometry stays under 17 000.
        self.assertLessEqual(self.out['triangles'], 17000)

ROOT = Path(__file__).resolve().parents[1]

class Invariants(unittest.TestCase):
    """What the v10 game test proved stays exactly as it was (spec, 'Invariantes')."""
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads((ROOT/'reports/v11_baseline.json').read_text(encoding='utf-8'))
        cls.v10 = json.loads((Path(cls.base['parent'])/'reports/collision_walkable.json').read_text())
        cls.v11 = json.loads((ROOT/'reports/collision_walkable.json').read_text())
        cls.stair = json.loads((ROOT/'reports/stair_design.json').read_text())
    def test_suelos_rampa_barreras_disco_y_pedestal_iguales(self):
        for key in ('floors_units', 'ramps', 'stair_edge_barriers_units', 'walkable_disk_units', 'ballesta_fixed_box_units'):
            self.assertEqual(self.v11[key], self.v10[key], key)
    def test_los_cinco_topes_bajos_iguales(self):
        low = lambda boxes: sorted(json.dumps(b, sort_keys=True) for b in boxes if abs(b['max'][2] - b['min'][2] - 24.5) < 0.6 and b['min'][2] > 450)
        self.assertEqual(len(low(self.v10['solid_boxes_units'])), 5)
        self.assertEqual(low(self.v11['solid_boxes_units']), low(self.v10['solid_boxes_units']))
    def test_sin_cabina_vieja(self):
        # v10's log cabin: four ~300 u walls up to z 423.5 and the painted door's boxes.
        old = {json.dumps(b, sort_keys=True) for b in self.v10['solid_boxes_units'] if b['max'][2] < 450 and b['min'][2] < 5}
        self.assertTrue(old)
        self.assertFalse(old & {json.dumps(b, sort_keys=True) for b in self.v11['solid_boxes_units']})
    def test_cada_caja_tiene_su_origen(self):
        sources = self.stair['solid_box_sources']
        self.assertEqual(len(sources), len(self.v11['solid_boxes_units']))
        self.assertEqual(sum(s.startswith('Baranda_poste_') for s in sources), 50)
        self.assertEqual(sum(s.startswith('barrera_baja_') for s in sources), 5)
        self.assertFalse(any('Pasamanos' in s for s in sources))
        self.assertEqual(len(self.stair['pasamanos_soporte_bboxes']), 20)
    def test_informe_rustico_es_de_este_torre_nif(self):
        rustic = json.loads((ROOT/'reports/rustico.json').read_text())
        self.assertEqual(rustic['torre_nif_sha256'], hashlib.sha256((ROOT/'mod/meshes/AstraAsedio/torre.nif').read_bytes()).hexdigest())
    def test_ballesta_virote_dll_y_scripts_como_v10(self):
        for rel, digest in self.base['invariant_sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest(), digest, rel)
            self.assertEqual(hashlib.sha256((Path(self.base['parent'])/rel).read_bytes()).hexdigest(), digest, rel)

if __name__ == '__main__': unittest.main()
