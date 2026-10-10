import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ExportAcceptance(unittest.TestCase):
    def test_source_is_unchanged(self):
        m = json.loads((ROOT / 'reports/source_manifest.json').read_text())
        for key in ('source_original', 'source_copy'):
            self.assertEqual(hashlib.sha256(Path(m[key]).read_bytes()).hexdigest(), m['sha256'])

    def test_exported_artifacts_meet_contract(self):
        path = ROOT / 'reports/assets_verified.json'
        self.assertTrue(path.is_file(), 'Final NIFs have not yet passed independent verification')
        if not path.is_file():
            return
        r = json.loads(path.read_text())
        self.assertTrue(r['ok'])
        for name,artifact in r['files'].items():
            current=ROOT/'mod/meshes/AstraAsedio'/f'{name}.nif'
            self.assertEqual(hashlib.sha256(current.read_bytes()).hexdigest(),artifact['sha256'],'NIF changed after verification: '+name)
        self.assertLessEqual(r['visual_triangles_total'], 40000)
        self.assertLessEqual(r['collision_triangles_total'], 2000)
        self.assertLessEqual(r['files']['torre']['shapes'], 8)
        self.assertLessEqual(r['files']['ballesta']['shapes'], 32)
        self.assertEqual(set(r['files']), {'torre', 'ballesta', 'virote'})
        self.assertEqual(set(r['files']['ballesta']['sequences']), {'Fire', 'Reset'})
        self.assertTrue(r['aim_nodes_have_no_animation_tracks'])
        self.assertTrue(r['vanilla_textures_exist'])
        self.assertTrue(r['rope_endpoint_checks_pass'])

if __name__ == '__main__':
    unittest.main()
