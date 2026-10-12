"""Acceptance gates on actual v23 artifacts, independent of archived releases."""
import hashlib
import json
import math
import struct
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(ROOT/'scripts/vendor'))
from platforms_v15_geometry import site
from parser_esm import Plugin
import build_plugin as B


class GuardV23(unittest.TestCase):
    def test_persistent_operator_bindings_and_floor(self):
        p = Plugin(ROOT/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp')
        records = {p.form_id(o)&0xFFFFFF:(t,dict(p.subrecords(p.datos(o))))
                   for t,o,n,d in p.recorrer() if t not in ('GRUP','TES4')}
        for gun,guard,marker in ((0xB70,0xB71,0xB72),(0xB80,0xB81,0xB82)):
            x,y,z,rx,ry,yaw = struct.unpack('<6f',records[gun][1]['DATA'])
            expected = (x-151*math.sin(yaw),y+151*math.cos(yaw),z,0,0,yaw+math.pi)
            for local in (guard,marker):
                actual = struct.unpack('<6f',records[local][1]['DATA'])
                for a,b in zip(actual,expected):self.assertAlmostEqual(a,b,places=3)
            self.assertEqual(records[guard][0],'ACHR')
            self.assertEqual(struct.unpack('<I',records[gun][1]['NAME'])[0],0x03000B04)
            scripts = B.read_vmad(records[gun][1]['VMAD'])['scripts']
            controller = next(s for s in scripts if s['name']=='AstraAsedioGuard')
            props = controller['properties']
            self.assertEqual(props['Artillero']['value']['form_id'],0x04000000+guard)
            self.assertEqual(props['Puesto']['value']['form_id'],0x04000000+marker)
            self.assertFalse(props['AllowPlayerTakeover']['value'])
            self.assertEqual(props['PitchMin']['value'],0)
            self.assertEqual(props['PitchMax']['value'],0)

    def test_alias_sensors_bind_real_refs_and_oar_payloads(self):
        p = Plugin(ROOT/'addons/GuardAnim/AstraAsedio_GuardAnim.esp')
        masters = [v.rstrip(b'\0').decode() for k,v in p.subrecords(p.datos(0)) if k=='MAST']
        self.assertEqual(masters,['Skyrim.esm','AstraAsedio.esp','AstraAsedio_WhiterunTorres.esp'])
        quests = [(p.form_id(o),p.subrecords(p.datos(o))) for t,o,n,d in p.recorrer() if t=='QUST']
        self.assertEqual(len(quests),1)
        fid,subs = quests[0]
        self.assertEqual(fid,0x03000806)
        self.assertEqual([struct.unpack('<I',v)[0] for k,v in subs if k=='ALFR'],[0x02000B71,0x02000B81])
        vm = B.read_vmad(dict(subs)['VMAD'],quest=True)
        for alias,gun in zip(vm['aliases'],(0xB70,0xB80)):
            self.assertEqual(alias['form_id'],fid)
            script = alias['scripts'][0]
            self.assertEqual(script['name'],'AstraGuardOperatorAlias')
            self.assertEqual(script['properties']['Controller']['value']['form_id'],0x02000000+gun)
        self.assertEqual((ROOT/'addons/GuardAnim/seq/AstraAsedio_GuardAnim.seq').read_bytes(),struct.pack('<I',fid))
        oar = ROOT/'addons/GuardAnim/meshes/actors/character/animations/OpenAnimationReplacer/AstraAsedioGuard'
        for name,clip in [('Operate','operate'),('Fire','fire'),('TurnLeft','turn_left'),('TurnRight','turn_right')]:
            config = json.loads((oar/name/'config.json').read_text())
            self.assertEqual(config['name'],'Astra Guard '+name)
            for leaf in ('IdleHandsBehindBack.hkx','IdleHandsBehindBack_Enter.hkx'):
                self.assertEqual((oar/name/leaf).read_bytes(),(ROOT/'source/anim'/f'astra_guard_{clip}.hkx').read_bytes())

    def test_whole_operator_arc_fits_both_fenced_decks(self):
        # Swept actor capsule, plus shoulders/boots; no stepping through rails.
        for name in ('este','oeste'):
            data = site(name)
            center = data['gun_local_pos']
            deck = data['floor_boxes'][0]
            for half_degree in range(-120,121):
                angle = math.radians(half_degree/2)
                x = center[0]-151*math.sin(angle)
                y = center[1]+151*math.cos(angle)
                self.assertGreater(x-40,deck['lo'][0]+12)
                self.assertLess(x+40,deck['hi'][0]-12)
                self.assertGreater(y-40,deck['lo'][1]+12)
                self.assertLess(y+40,deck['hi'][1]-12)
                self.assertAlmostEqual(center[2],data['deck_local_z'])

    def test_no_papyrus_projectile_owner_remains(self):
        for name in ('AstraAsedioGuard','AstraGuardiaAuto'):
            text = (ROOT/'mod/scripts/source'/f'{name}.psc').read_text()
            self.assertNotIn('Launcher.Fire(',text,name)
        guard = (ROOT/'mod/scripts/source/AstraAsedioGuard.psc').read_text()
        self.assertIn('AstraGuardNative.BeginOperation(',guard)
        self.assertIn('AstraGuardNative.EndOperation(',guard)

    def test_authored_grips_and_planted_feet(self):
        report = json.loads((ROOT/'reports/authoring_v23.json').read_text())
        self.assertTrue(report['success'])
        self.assertEqual(report['blender'],'5.2.2 LTS')
        self.assertEqual(report['operator_foot_gun_local'],[0,151,0])
        self.assertLess(report['max_wrist_error_units'],.01)
        self.assertLess(report['max_step_foot_error_units'],.01)
        self.assertEqual(len(report['clips']),4)
        for clip in report['clips']:
            path = ROOT/'source/anim'/clip['file']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),clip['sha256'])
        for side in ('left','right'):
            samples = report['samples']['astra_guard_turn_'+side]
            lead = 'L' if side=='left' else 'R'
            trailing = 'R' if side=='left' else 'L'
            for foot,subset in ((trailing,samples[:13]),(lead,samples[12:])):
                anchor = subset[0]['feet'][foot]['world']
                for sample in subset:
                    self.assertLess(math.dist(anchor,sample['feet'][foot]['world']),.01)


if __name__ == '__main__':
    unittest.main()
