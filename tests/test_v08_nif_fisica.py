"""Havok box bodies and alpha properties across EVERY shipped NIF, plus falsification.

The family tests enumerate mod/meshes, so a new NIF is covered without editing
this file. Falsification runs the same checks on the sealed v07 NIFs (a real bad
case: a 57 u steel-bolt box on a 284 u siege bolt, inertia rotated 90 degrees and
alpha-tested floors) and on synthetic mutations of the current virote.
"""
import json, shutil, struct, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts')); sys.path.insert(0, str(ROOT/'scripts/vendor'))
import nif_fisica, nif_nodos

MESHES = ROOT/'mod/meshes/AstraAsedio'

def shipped():
    return sorted(MESHES.glob('*.nif'))

def read(path):
    return nif_nodos.leer(str(path))

def parent_meshes():
    baseline = json.loads((ROOT/'reports/v08_baseline.json').read_text())
    return Path(baseline['parent_project'])/'mod/meshes/AstraAsedio'


class ShippedNifFamily(unittest.TestCase):
    def test_the_family_is_the_shipped_nifs(self):
        # La familia creció respecto de v08: `torre_whiterun.nif` (STAT del addon de ciudad) y
        # `ballesta_guardia.nif` (v22, la torreta baja del guardia, pivote 117). Las dos son
        # NIF embarcados con colision Havok, asi que las pruebas de fisica de arriba las
        # recorren solas; esta lista es la que hace visible que aparecio una nueva.
        self.assertEqual({p.name for p in shipped()},
                         {'torre.nif', 'torre_whiterun.nif', 'ballesta.nif',
                          'ballesta_guardia.nif', 'virote.nif'})

    def test_no_shipped_shape_carries_an_alpha_property(self):
        # No material of this mod needs alpha: the walkway DXT1 has zero transparent texels.
        for path in shipped():
            with self.subTest(nif=path.name):
                self.assertEqual(nif_fisica.propiedades_alfa(read(path)), [])

    def test_every_box_covers_its_visual_length(self):
        for path in shipped():
            for row in nif_fisica.cobertura(read(path)):
                with self.subTest(nif=path.name, body=row['cuerpo']):
                    self.assertGreaterEqual(row['fraccion'], nif_fisica.COBERTURA_MINIMA)

    def test_every_massive_box_has_least_inertia_on_its_long_axis_and_vanilla_rules(self):
        for path in shipped():
            for box in nif_fisica.cuerpos_caja(read(path)):
                with self.subTest(nif=path.name, body=box['cuerpo']):
                    self.assertTrue(nif_fisica.inercia_alineada(box))
                    self.assertEqual(nif_fisica.reglas_vanilla(box), [])

    def test_virote_body_matches_configured_mass_and_restitution(self):
        boxes = nif_fisica.cuerpos_caja(read(MESHES/'virote.nif'))
        self.assertEqual(len(boxes), 1)
        body = json.loads((ROOT/'config.json').read_text())['projectile_body']
        self.assertAlmostEqual(boxes[0]['masa'], body['mass'], places=4)
        self.assertAlmostEqual(boxes[0]['restitucion'], body['restitution'], places=4)


class Falsification(unittest.TestCase):
    def test_sealed_v07_virote_fails_coverage_and_inertia(self):
        nif = read(parent_meshes()/'virote.nif')
        self.assertLess(nif_fisica.cobertura(nif)[0]['fraccion'], nif_fisica.COBERTURA_MINIMA)
        self.assertFalse(nif_fisica.inercia_alineada(nif_fisica.cuerpos_caja(nif)[0]))

    def test_sealed_v07_floors_fail_alpha(self):
        for name in ('torre.nif', 'ballesta.nif'):
            with self.subTest(nif=name):
                self.assertTrue(nif_fisica.propiedades_alfa(read(parent_meshes()/name)))

    def test_synthetic_mutations_of_the_current_virote_are_rejected(self):
        original = (MESHES/'virote.nif').read_bytes()
        box = nif_fisica.cuerpos_caja(read(MESHES/'virote.nif'))[0]
        with tempfile.TemporaryDirectory() as td:
            copy = Path(td)/'virote.nif'
            # Inertia swapped between the long axis and a thin axis.
            b = bytearray(original); o = box['offset_cuerpo']
            ix, iy, iz = box['inercia']
            struct.pack_into('<f', b, o + 136, iz); struct.pack_into('<f', b, o + 156, iy)
            copy.write_bytes(bytes(b))
            self.assertFalse(nif_fisica.inercia_alineada(nif_fisica.cuerpos_caja(read(copy))[0]))
            # Box cut to a fifth of its length, centre unchanged.
            b = bytearray(original)
            struct.pack_into('<f', b, box['offset_forma'] + 20, box['semiejes_hk'][1] / 5)
            copy.write_bytes(bytes(b))
            self.assertLess(nif_fisica.cobertura(read(copy))[0]['fraccion'], nif_fisica.COBERTURA_MINIMA)
            # Convex radius copied from the steel-bolt donor.
            b = bytearray(original)
            struct.pack_into('<f', b, box['offset_forma'] + 4, 0.0017859373474493623)
            copy.write_bytes(bytes(b))
            self.assertTrue(nif_fisica.reglas_vanilla(nif_fisica.cuerpos_caja(read(copy))[0]))
            # Mass kept but inertia zeroed: the Havok NaN case of the skill's trap 4.
            b = bytearray(original)
            for k in (116, 136, 156):
                struct.pack_into('<f', b, o + k, 0.0)
            copy.write_bytes(bytes(b))
            self.assertTrue(nif_fisica.reglas_vanilla(nif_fisica.cuerpos_caja(read(copy))[0]))

    def test_a_full_length_box_lying_across_the_bolt_is_rejected(self):
        # Review finding: coverage measured on the box's own long axis passed a
        # 284 u box standing on Z with 1.0. Same length, wrong orientation.
        original = (MESHES/'virote.nif').read_bytes()
        box = nif_fisica.cuerpos_caja(read(MESHES/'virote.nif'))[0]
        s = 0.5 ** 0.5
        with tempfile.TemporaryDirectory() as td:
            copy = Path(td)/'virote.nif'
            for label, q in (('v07 exporter frame, box on Z', (0.0, s, s, 0.0)), ('90 deg about Z, box on X', (0.0, 0.0, s, s))):
                with self.subTest(rotation=label):
                    b = bytearray(original)
                    struct.pack_into('<4f', b, box['offset_cuerpo'] + 68, *q)
                    copy.write_bytes(bytes(b))
                    row = nif_fisica.cobertura(read(copy))[0]
                    self.assertNotEqual(row['eje_caja'], row['eje'])
                    self.assertLess(row['fraccion'], nif_fisica.COBERTURA_MINIMA)

    def test_a_box_tilted_off_the_bolt_is_rejected_but_a_small_tilt_is_not(self):
        # Re-review: axis-aligned extents still covered 90 % up to ~26 degrees of tilt.
        import math
        def mul(a, b):  # Hamilton product, xyzw
            ax, ay, az, aw = a; bx, by, bz, bw = b
            return (aw*bx + ax*bw + ay*bz - az*by, aw*by - ax*bz + ay*bw + az*bx,
                    aw*bz + ax*by - ay*bx + az*bw, aw*bw - ax*bx - ay*by - az*bz)
        original = (MESHES/'virote.nif').read_bytes()
        box = nif_fisica.cuerpos_caja(read(MESHES/'virote.nif'))[0]
        with tempfile.TemporaryDirectory() as td:
            copy = Path(td)/'virote.nif'
            for degrees, passes in ((20, False), (5, True)):
                h = math.radians(degrees) / 2
                q = mul(tuple(box['rotacion']), (math.sin(h), 0.0, 0.0, math.cos(h)))  # about the body's thin X axis
                b = bytearray(original); struct.pack_into('<4f', b, box['offset_cuerpo'] + 68, *q)
                copy.write_bytes(bytes(b))
                row = nif_fisica.cobertura(read(copy))[0]
                with self.subTest(tilt=degrees):
                    self.assertAlmostEqual(row['coseno_eje'], math.cos(math.radians(degrees)), places=3)
                    if passes:
                        self.assertGreaterEqual(row['fraccion'], nif_fisica.COBERTURA_MINIMA)
                    else:
                        self.assertLess(row['fraccion'], nif_fisica.COBERTURA_MINIMA)

    def test_coverage_follows_the_node_that_owns_the_collision(self):
        # Moving the root moves the shapes AND the box it owns: coverage must stay.
        # Reading the box without the owner's transform left it behind (fraction 0).
        nif = read(MESHES/'virote.nif')
        root_offset = nif['bloques'][0][1]
        _name, p = nif_fisica._saltar_net(nif['datos'], root_offset)
        b = bytearray((MESHES/'virote.nif').read_bytes())
        struct.pack_into('<3f', b, p + 4, 0.0, 500.0, 0.0)
        with tempfile.TemporaryDirectory() as td:
            copy = Path(td)/'virote.nif'; copy.write_bytes(bytes(b))
            self.assertGreaterEqual(nif_fisica.cobertura(read(copy))[0]['fraccion'], nif_fisica.COBERTURA_MINIMA)

    def test_an_unreferenced_alpha_block_still_counts(self):
        # The rule is "no NiAlphaProperty", not "none linked": unlink v07's floor alpha.
        path = parent_meshes()/'torre.nif'; nif = read(path)
        shape = next(s for s in nif_fisica._shapes(nif) if s[5] >= 0 and nif['bloques'][s[5]][0] == 'NiAlphaProperty')
        b = bytearray(path.read_bytes())
        struct.pack_into('<i', b, shape[8] - 20, -1)
        with tempfile.TemporaryDirectory() as td:
            copy = Path(td)/'torre.nif'; copy.write_bytes(bytes(b))
            found = nif_fisica.propiedades_alfa(read(copy))
            self.assertTrue(found)
            self.assertIsNone(found[0]['shape'])

    def test_patcher_refuses_a_nif_without_exactly_one_box(self):
        with tempfile.TemporaryDirectory() as td:
            copy = Path(td)/'torre.nif'; shutil.copy2(MESHES/'torre.nif', copy)
            with self.assertRaisesRegex(ValueError, 'exactamente un cuerpo de caja'):
                nif_fisica.parchear_cuerpo_caja(copy, (1, 1, 1), (0, 0, 0), 1.0, 0.1, (1, 1, 1))


if __name__ == '__main__':
    unittest.main()
