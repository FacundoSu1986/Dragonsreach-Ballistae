"""The shipped plugin must bind the requested mouse mode and measured pivot."""
import json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'scripts/vendor'))
from parser_esm import Plugin
from build_plugin import read_vmad

class MouseModePlugin(unittest.TestCase):
    def test_camera_mode_and_elevation_are_bound_in_final_esp(self):
        p=Plugin(ROOT/'mod/AstraAsedio.esp')
        record=next(o for t,o,n,d in p.recorrer() if t=='ACTI')
        props=read_vmad(dict(p.subrecords(p.datos(record)))['VMAD'])['scripts'][0]['properties']
        self.assertIn('UseMouseAim',props)
        self.assertEqual(props['UseMouseAim']['value'],True)
        self.assertEqual(props['PitchMax']['value'],80.)
        self.assertEqual(props['PitchPivotHeight']['value'],153.)
        nodes=json.loads((ROOT/'reports/assets_verified.json').read_text())['files']['ballesta']['nodes']
        measured=nodes['CTRL_GIRO_360']['translation'][2]+nodes['CTRL_ELEVACION']['translation'][2]
        self.assertAlmostEqual(props['PitchPivotHeight']['value'],measured,places=3)

if __name__=='__main__':unittest.main()
