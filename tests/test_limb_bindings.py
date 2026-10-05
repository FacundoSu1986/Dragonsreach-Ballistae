"""Accept measured bindings on both limbs only for the current final NIF."""
import hashlib,json,unittest
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class LimbBindingAcceptance(unittest.TestCase):
    def test_fourteen_closed_bindings_hug_the_reimported_limbs(self):
        report=json.loads((ROOT/'reports/limb_ties_verified.json').read_text())
        self.assertTrue(report['ok']);self.assertTrue(report['both_limbs_verified'])
        self.assertEqual(report['nif_sha256'],hashlib.sha256((ROOT/'mod/meshes/AstraAsedio/ballesta.nif').read_bytes()).hexdigest())
        self.assertEqual(Counter(p['parent'] for p in report['parts']),{'CTRL_BRAZO_I':7,'CTRL_BRAZO_D':7})
        for part in report['parts']:
            self.assertGreaterEqual(part['clearance_min_units'],0.)
            self.assertLessEqual(part['clearance_max_units'],.15)
            self.assertTrue(part['rope_shapes']);self.assertTrue(part['limb_shapes'])
        revision=json.loads((ROOT/'reports/limb_ties_revision.json').read_text())
        self.assertTrue(all(p['closed_manifold'] for p in revision['parts']))
        self.assertFalse(revision['original_files_modified'])
if __name__=='__main__':unittest.main()
