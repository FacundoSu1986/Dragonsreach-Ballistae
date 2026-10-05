"""The current final NIF must clear the roof at the requested high angle."""
import hashlib, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class ElevationAcceptance(unittest.TestCase):
    def test_eighty_degree_moving_geometry_clears_the_roof(self):
        report=json.loads((ROOT/'reports/elevation_diagnosis.json').read_text())
        self.assertEqual(report['nif_sha256'],hashlib.sha256((ROOT/'mod/meshes/AstraAsedio/ballesta.nif').read_bytes()).hexdigest())
        sample=next(value for value in report['samples'] if value['pitch']==80)
        self.assertGreaterEqual(sample['moving_min_z_relative_to_roof'],2.,'upper assembly would penetrate the roof at dragon elevation')

if __name__=='__main__':unittest.main()
