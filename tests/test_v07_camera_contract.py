"""Source wiring + NIF timing contracts; these do not execute engine hooks."""
import unittest,re,json,sys,hashlib,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from retime_v07 import retime,transform_times,nif_nodos
class V07Integration(unittest.TestCase):
    def test_post_camera_adapter_uses_current_parent_and_transaction(self):
        s=(ROOT/'native/src/Plugin.cpp').read_text()
        body=s.split('void cameraUpdate(RE::PlayerCamera* camera){')[1].split('void rotation(')[0]
        self.assertLess(body.index('originalCameraUpdate(camera)'),body.index('session.visitSnapshot(ticket'))
        self.assertIn('cr->parent?from(cr->parent->world)',body)
        self.assertIn('toLocal(parent,snap.worldCamera)',body)
        self.assertIn('updateWorld(cr)',body)
        self.assertNotIn('binding.cameraParent!=',s)
        self.assertIn('cameraVtable.write_vfunc(2,cameraUpdate)',s)
        # v09: the failed post-camera check still invalidates the ticket, now through drop(), which logs why.
        self.assertIn('drop(ticket,failure)',body)
        drop=s.split('void drop(Ticket ticket,const std::string& reason){')[1].split('\n}')[0]
        self.assertIn('session.invalidate(ticket)',drop)
        self.assertIn('spdlog::warn("sight dropped: {}",reason)',drop)
    def test_v06_api_cannot_enter_new_controller(self):
        from tests.test_native_sight import NativeSightFixture
        f=NativeSightFixture();f.version=0x02000000;f.enter()
        self.assertFalse(f.vm.state['operating']);self.assertEqual(f.lease.calls,[])
    def test_both_final_sequences_have_configured_duration_and_scaled_key_times(self):
        cfg=json.loads((ROOT/'config.json').read_text());report=json.loads((ROOT/'reports/animation_retime.json').read_text())
        p=ROOT/'mod/meshes/AstraAsedio/ballesta.nif';b=nif_nodos.leer(str(p));raw=b['datos']
        self.assertEqual(hashlib.sha256(raw).hexdigest(),report['after_sha256'])
        for typ,off,size in b['bloques']:
            if typ!='NiControllerSequence':continue
            name=b['strings'][struct.unpack_from('<I',raw,off)[0]];n=struct.unpack_from('<I',raw,off+4)[0]
            start,stop=struct.unpack_from('<ff',raw,off+12+n*29+16)
            expected=cfg['fire_seconds' if name=='Fire' else 'reset_seconds']
            self.assertAlmostEqual(stop-start,expected,places=5)
            for i in range(n):
                interp=struct.unpack_from('<i',raw,off+12+i*29)[0];_,io,_=b['bloques'][interp]
                data=struct.unpack_from('<i',raw,io+32)[0];_,do,ds=b['bloques'][data]
                times=[struct.unpack_from('<f',raw,t)[0] for t in transform_times(raw,do,ds)]
                self.assertGreater(len(times),0);self.assertLessEqual(max(times),expected+.00001)
    def test_esp_timing_and_mode_match_config(self):
        from build_plugin import validate_plugin
        self.assertTrue(validate_plugin(ROOT/'mod/AstraAsedio.esp')['structural_valid'])

if __name__=='__main__':unittest.main()
