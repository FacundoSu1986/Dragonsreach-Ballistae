"""Replay observed unbound-camera behavior in real PSC branches, not a game VM."""
import re
import unittest
from pathlib import Path
from tests.test_native_sight import NativeSightFixture

ROOT = Path(__file__).resolve().parents[1]
API_V2 = 0x03040000  # current AstraSight 3.4 (v13 depression); the name is historical


class RuntimeBindingContract(unittest.TestCase):
    def fixture(self, camera=0):
        f = NativeSightFixture(camera=camera)
        f.version = API_V2
        f.unbound_camera_calls = 0
        def absent_camera():
            # Observed VM error returns None, cast to Int=0. Preserve that defect.
            f.unbound_camera_calls += 1
            return 0
        f.vm.state['Camera'].GetCameraState = absent_camera
        f.vm.state['AstraSightNative'].GetAPIVersion = lambda: 3
        f.vm.state['AstraSightNative'].GetCameraState = f.lease.camera_state
        f.lease.vm.state['AstraSightNative'] = f.vm.state['AstraSightNative']
        return f

    def test_special_camera_is_rejected_despite_old_unbound_default_zero(self):
        f = self.fixture(camera=5)
        f.enter()
        self.assertFalse(f.vm.state['operating'])
        self.assertEqual(f.lease.controls, [True]*8)
        self.assertEqual(f.unbound_camera_calls, 0)

    def test_third_person_entry_observes_real_state_and_forces_first_person(self):
        f = self.fixture(camera=9)
        f.enter()
        self.assertEqual(f.lease.camera, 0)
        self.assertIn('first', f.lease.camera_calls)
        self.assertEqual(f.unbound_camera_calls, 0)

    def test_periodic_aim_does_not_call_unbound_camera_namespace(self):
        f = self.fixture()
        f.active()
        self.assertEqual(f.vm.run('SampleSightAimResult', 7, False), 1)
        self.assertEqual(f.unbound_camera_calls, 0)

    def test_old_dll_rejected_before_controls_acquired(self):
        f = self.fixture()
        f.version = 0x01000000
        f.enter()
        self.assertFalse(f.vm.state['operating'])
        self.assertEqual(f.lease.controls, [True]*8)
        self.assertFalse(any(c[0]=='begin' for c in f.calls))

    def test_api_mismatch_rejected_before_controls_acquired(self):
        f = self.fixture()
        f.vm.state['AstraSightNative'].GetAPIVersion = lambda: 1
        f.enter()
        self.assertFalse(f.vm.state['operating'])
        self.assertEqual(f.lease.controls, [True]*8)

    def test_missing_dll_cleanup_restores_owned_controls_without_new_native_call(self):
        f = self.fixture(camera=9)
        f.active()
        f.version = -1
        f.vm.state['AstraSightNative'].GetCameraState = lambda: self.fail('absent DLL called during cleanup')
        f.vm.state['AstraSightNative'].GetAPIVersion = lambda: self.fail('absent DLL called during cleanup')
        f.vm.run('EndSession')
        self.assertEqual(f.lease.controls, [True]*8)
        self.assertFalse(f.vm.state['operating'])

    def test_api_version_boundary_cannot_adopt_a_replacement_session(self):
        f = self.fixture()
        def replaced():
            f.vm.state.update(generation=77, operating=True, token=55)
            return 1
        f.vm.state['AstraSightNative'].GetAPIVersion = replaced
        f.enter()
        self.assertEqual(f.vm.state['generation'], 77)
        self.assertEqual(f.vm.state['token'], 55)
        self.assertFalse(any(c[0] in ('begin', 'reject') for c in f.calls))

    def test_final_bytecode_validator_rejects_both_broken_runtime_wrappers(self):
        import sys
        sys.path.insert(0, str(ROOT/'scripts'))
        import compile_papyrus
        self.assertTrue(hasattr(compile_papyrus, 'validate_camera_assembly'))
        for namespace in ('camera', 'game'):
            with self.assertRaisesRegex(ValueError, 'camera state'):
                compile_papyrus.validate_camera_assembly('CallStatic '+namespace+' GetCameraState ::temp1')
        self.assertTrue(compile_papyrus.validate_camera_assembly(
            'CallStatic astrasightnative GetCameraState ::temp1')['own_camera_state_binding'])

    def test_session_native_calls_avoid_unneeded_main_thread_hops(self):
        source = (ROOT/'native/src/Plugin.cpp').read_text()
        for name in ('IsAvailable','GetAPIVersion','GetCameraState','BeginSight','IsSightReady','SetFrozen','EndSight'):
            self.assertRegex(source, rf'RegisterFunction\("{name}",\s*"AstraSightNative",\s*{name},\s*true\)')
        self.assertRegex(source, r'SetCallableFromTasklets\("AstraSightNative",\s*"CaptureAim",\s*true\)')


if __name__ == '__main__':
    unittest.main()
