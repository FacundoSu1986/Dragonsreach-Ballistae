"""Acceptance of the actual mounted-camera node, not a proposed Blender empty."""
from pathlib import Path
import hashlib,json,sys,unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/vendor'))
import nif_nodos

class SightAnchorAcceptance(unittest.TestCase):
    def test_final_nif_camera_is_child_of_pitch_with_logical_forward(self):
        info=nif_nodos.leer(str(ROOT/'mod/meshes/AstraAsedio/ballesta.nif'))
        by_name={n['nombre']:(i,n) for i,n in info['nodos'].items()}
        self.assertIn('AstraSightCameraNode',by_name)
        index,node=by_name['AstraSightCameraNode']
        self.assertIn(index,by_name['CTRL_ELEVACION'][1]['hijos'])
        for a,b in zip(node['tr'],(0,80,40)):self.assertAlmostEqual(a,b,places=3)
        for a,b in zip(node['rot'],(-1,0,0,0,-1,0,0,0,1)):self.assertAlmostEqual(a,b,places=5)

    def test_current_pose_probe_is_clear_and_uses_same_forward_as_projectile(self):
        p=ROOT/'reports/sight_anchor_verified.json'
        self.assertTrue(p.is_file(),'Run actual NIF sight-anchor pose inspection')
        report=json.loads(p.read_text())
        self.assertTrue(report['ok'])
        self.assertEqual(report['nif_sha256'],hashlib.sha256((ROOT/'mod/meshes/AstraAsedio/ballesta.nif').read_bytes()).hexdigest())
        self.assertGreaterEqual(len(report['poses']),24)
        self.assertGreater(report['minimum_floor_clearance'],5)
        self.assertGreater(report['minimum_mesh_distance'],10)
        self.assertGreater(report['minimum_direction_dot'],.99999)
        self.assertFalse(report['in_game_camera_verified'])

if __name__=='__main__':unittest.main()
