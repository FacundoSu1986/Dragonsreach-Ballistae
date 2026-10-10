"""Execute controller PSC with explicit native boundary fixtures; not a game VM."""
import math
import unittest
from types import SimpleNamespace
from tests.test_camera_aim import AimFixture, ACTI
from tests.test_control_lease import NativeControlFixture, SOURCE


class NativeSightFixture(AimFixture):
    def __init__(self, camera=0):
        super().__init__(camera)
        self.vm.state['UseSightCamera'] = True
        self.version = 0x03040000
        self.available = True
        self.accepted = True
        self.ready = True
        self.pose = [37., 24.]
        self.snapshot = None
        self.native_token = None
        self.frozen = False
        self.calls = []
        self.ammo = 10
        self.launches = 0
        self.thaw_ok = True
        self.vm.state['SKSE'].GetPluginVersion = lambda name: self.version
        self.vm.state['AstraSightNative'] = SimpleNamespace(
            GetAPIVersion=lambda: 3, GetCameraState=self.lease.camera_state,
            IsAvailable=self.is_available, BeginSight=self.begin, IsSightReady=self.is_ready,
            CaptureAim=self.capture, SetFrozen=self.set_frozen, EndSight=self.end)
        self.self_ref.UseSightCamera = True
        self.lease.vm.state['SKSE'] = self.vm.state['SKSE']
        self.lease.vm.state['AstraSightNative'] = self.vm.state['AstraSightNative']
        self.vm.state['player'].GetItemCount = lambda ammo: self.ammo
        self.vm.state['player'].RemoveItem = self.remove
        self.vm.state['Launcher'] = SimpleNamespace(Fire=self.fire)
        self.vm.state['NetImmerse'].SetNodeScale = lambda *args: self.calls.append(('visual',))
        self.vm.native['ShotTransformReady'] = lambda: True
        self.vm.native['PlayGamebryoAnimation'] = lambda *args: True
        release = self.vm.state['Session'].Release
        self.vm.state['Session'].Release = lambda *args: (self.calls.append(('release', args[1])), release(*args))[-1]
        self.vm.native['RejectActivation'] = lambda reason: self.calls.append(('reject', reason))
        self.vm.native['RejectShot'] = lambda reason: self.calls.append(('shot_error', reason))

    def is_available(self):
        self.calls.append(('available',))
        self.hook('available')
        return self.available

    def begin(self, gun, token, yaw, pitch):
        self.calls.append(('begin', token, yaw, pitch))
        self.hook('begin_before')
        # v09: like Session::begin, a Begin while a lease is active is rejected.
        accepted = self.accepted and self.native_token is None
        if accepted:
            self.native_token = token
        self.hook('begin_after')
        return accepted

    def is_ready(self, gun, token):
        result = self.native_token == token and self.ready
        self.calls.append(('ready', token))
        self.hook('ready')
        return result

    def capture(self, gun, token, freeze):
        result = list(self.pose if self.snapshot is None else self.snapshot)
        self.calls.append(('capture', token, freeze))
        self.hook('freeze_before' if freeze else 'sample')
        if token == self.native_token and freeze:
            self.frozen = True
        self.hook('freeze_after' if freeze else 'sample_after')
        return result if token == self.native_token else []

    def set_frozen(self, gun, token, frozen):
        self.calls.append(('frozen', token, frozen))
        self.hook('thaw')
        if token == self.native_token and self.thaw_ok:
            self.frozen = frozen
            return True
        return False

    def end(self, gun, token):
        self.calls.append(('end', token))
        if token == self.native_token:
            self.native_token = None
            self.frozen = False
        self.hook('end')
        return True

    def remove(self, ammo, count, silent):
        self.ammo -= count
        self.hook('remove')

    def fire(self, gun, ammo):
        self.launches += 1
        self.hook('fire')

    def active(self):
        super().active()
        self.native_token = self.vm.state['token']
        self.vm.state['nativeSightRequested'] = True

    def close_menu(self):
        self.vm.menu = False
        self.vm.run('ResumeInput')

    def open_menu(self):
        self.vm.menu = True
        self.vm.run('OnMenuOpen', 'InventoryMenu')

    def replace(self):
        self.vm.run('EndSession')
        self.vm.now += .4
        self.enter()
        self.vm.run('OnUpdate')


class NativeSightContract(unittest.TestCase):
    def test_session_emergency_native_end_precedes_control_and_camera_restore(self):
        f = NativeControlFixture(SOURCE.read_text(), camera=9)
        gun = f.gun(); gun.UseSightCamera = True
        f.vm.state['SKSE'] = SimpleNamespace(GetPluginVersion=lambda name: 0x03040000)
        f.vm.state['AstraSightNative'].EndSight = lambda ref, token: f.order.append('native_end')
        gun.token = f.vm.run('Acquire', gun)
        f.vm.run('EmergencyCleanup')
        self.assertIn('native_end', f.order)
        self.assertLess(f.order.index('native_end'), f.order.index('enable'))
        self.assertEqual(f.controls, [True]*8)

    def test_session_end_boundary_retains_releasing_guard(self):
        f = NativeControlFixture(SOURCE.read_text())
        gun, contender = f.gun(), f.gun(); gun.UseSightCamera = True
        f.vm.state['SKSE'] = SimpleNamespace(GetPluginVersion=lambda name: 0x03040000)
        observed = []
        f.vm.state['AstraSightNative'].EndSight = lambda ref, token: observed.append(f.vm.run('Acquire', contender))
        gun.token = f.vm.run('Acquire', gun); f.vm.run('Release', gun, gun.token)
        self.assertEqual(observed, [-1]); self.assertEqual(f.controls, [True]*8)

    def test_final_esp_binds_native_sight_true(self):
        import sys
        from tests.test_camera_aim import ROOT
        sys.path.insert(0, str(ROOT/'scripts')); sys.path.insert(0, str(ROOT/'scripts/vendor'))
        from parser_esm import Plugin
        from build_plugin import read_vmad
        p = Plugin(ROOT/'mod/AstraAsedio.esp')
        record = next(o for t,o,n,d in p.recorrer() if t == 'ACTI')
        props = read_vmad(dict(p.subrecords(p.datos(record)))['VMAD'])['scripts'][0]['properties']
        self.assertIn('UseSightCamera', props)
        self.assertIs(props['UseSightCamera']['value'], True)

    def test_final_esp_validator_rejects_silent_legacy_mode(self):
        import sys, tempfile
        from pathlib import Path
        from tests.test_camera_aim import ROOT
        sys.path.insert(0, str(ROOT/'scripts')); sys.path.insert(0, str(ROOT/'scripts/vendor'))
        from parser_esm import Plugin
        from build_plugin import validate_plugin
        p = Plugin(ROOT/'mod/AstraAsedio.esp')
        record = next(o for t,o,n,d in p.recorrer() if t == 'ACTI')
        vmad = dict(p.subrecords(p.datos(record)))['VMAD']
        marker = b'UseSightCamera'
        offset = p.d.find(vmad, record+24) + vmad.index(marker) + len(marker) + 2
        corrupted = bytearray(p.d); corrupted[offset] = 0
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'silent_legacy.esp'; path.write_bytes(corrupted)
            with self.assertRaisesRegex(ValueError, 'UseSightCamera'):
                validate_plugin(path)

    def test_native_sight_default_is_explicit_and_true(self):
        f = AimFixture()
        self.assertRegex(ACTI.read_text(), r'bool Property UseSightCamera = true Auto')

    def test_missing_plugin_does_not_call_api_or_acquire_controls(self):
        f = NativeSightFixture(); f.version = -1; f.enter()
        self.assertFalse(f.vm.state['operating']); self.assertEqual(f.lease.calls, [])
        self.assertFalse(any(c[0] == 'available' for c in f.calls))
        self.assertTrue(any(c[0] == 'reject' and 'NATIVE' in c[1] for c in f.calls))

    def test_unavailable_api_rejects_before_acquiring_controls(self):
        f = NativeSightFixture(); f.available = False; f.enter()
        self.assertFalse(f.vm.state['operating']); self.assertEqual(f.lease.calls, [])

    def test_begin_once_after_fp_and_wait_for_ready(self):
        f = NativeSightFixture(camera=9); f.ready = False; f.enter()
        self.assertTrue(f.vm.state['cameraEntryPending'])
        f.vm.run('OnUpdate'); f.vm.now += .05; f.vm.run('OnUpdate')
        self.assertEqual(len([c for c in f.calls if c[0] == 'begin']), 1)
        self.assertTrue(f.vm.state['cameraEntryPending']); self.assertFalse(f.vm.run('InputReady'))
        f.ready = True; f.vm.now += .05; f.vm.run('OnUpdate')
        self.assertFalse(f.vm.state['cameraEntryPending']); self.assertEqual(f.lease.camera, 0)

    def test_begin_rejection_and_ready_timeout_release_controls(self):
        for cause in ('rejected', 'timeout'):
            f = NativeSightFixture(); f.accepted = cause != 'rejected'; f.ready = False
            f.enter(); f.vm.run('OnUpdate')
            if cause == 'timeout':
                f.vm.now += 1.5; f.vm.run('OnUpdate')
            self.assertFalse(f.vm.state['operating']); self.assertEqual(f.lease.controls, [True]*8)
            self.assertTrue(any(c[0] == 'reject' for c in f.calls))

    def test_exit_during_begin_before_or_after_effect_ends_old_token(self):
        for boundary in ('begin_before', 'begin_after'):
            f = NativeSightFixture(); f.enter(); old = f.vm.state['token']
            f.hooks[boundary] = lambda: f.vm.run('EndSession')
            f.vm.run('OnUpdate')
            self.assertFalse(f.vm.state['operating']); self.assertIsNone(f.native_token)
            self.assertGreaterEqual(len([c for c in f.calls if c == ('end', old)]), 1)
            self.assertEqual(f.lease.controls, [True]*8)

    def test_late_begin_does_not_release_replacement_lease(self):
        f = NativeSightFixture(); f.enter(); old = f.vm.state['token']
        f.hooks['begin_after'] = f.replace; f.vm.run('OnUpdate')
        self.assertTrue(f.vm.state['operating']); self.assertGreater(f.vm.state['token'], old)
        self.assertEqual(f.native_token, f.vm.state['token'])
        self.assertEqual(f.lease.controls[:4], [False, False, False, True])

    def test_native_sample_uses_applied_snapshot_without_node_writes(self):
        f = NativeSightFixture(); f.active(); f.look = [-72., 260.]
        f.vm.run('UpdateAim', .05)
        self.assertEqual((f.vm.state['yaw'], f.vm.state['pitch']), tuple(f.pose))
        self.assertEqual(f.applied, []); self.assertIn(('capture', f.vm.state['token'], False), f.calls)

    def test_invalid_native_snapshot_is_visible_and_releases_controls(self):
        # v09: exactly 360.0 is no longer invalid. The native double yaw in [0,360) reaches
        # Papyrus as float, and 359.99999x rounds to 360.0 (reports/user_evidence_v08.json).
        for sample in ([], [1.], [1.,2.,3.], [math.nan,0.], [0.,math.inf], [-1.,0.], [360.5,0.], [0.,-21.], [0.,81.]):
            f = NativeSightFixture(); f.active(); f.snapshot = sample
            f.vm.run('UpdateAim', .05)
            self.assertFalse(f.vm.state['operating']); self.assertEqual(f.lease.controls, [True]*8)
            self.assertTrue(any(c[0] == 'shot_error' for c in f.calls))

    def test_readiness_lost_ends_operating_session(self):
        f = NativeSightFixture(); f.active(); f.ready = False; f.vm.run('UpdateAim', .05)
        self.assertFalse(f.vm.state['operating']); self.assertEqual(f.lease.controls, [True]*8)

    def test_attack_during_native_sample_discards_periodic_pose_preserves_shot(self):
        f = NativeSightFixture(); f.active()
        f.hooks['sample'] = lambda: f.vm.run('OnControlDown', 'Right Attack/Block')
        f.vm.run('OnUpdate')
        self.assertTrue(f.vm.state['operating']); self.assertEqual(f.vm.state['phase'], 1)
        self.assertEqual(f.vm.state['settleFrames'], 0); self.assertTrue(f.frozen)

    def test_menu_during_native_sample_discards_even_empty_old_result(self):
        f = NativeSightFixture(); f.active(); f.snapshot = []; f.hooks['sample'] = f.open_menu
        f.vm.run('OnUpdate')
        self.assertTrue(f.vm.state['operating']); self.assertTrue(f.vm.state['inputPaused'])

    def test_stale_sample_cannot_end_replacement_session(self):
        f = NativeSightFixture(); f.active(); old = f.vm.state['token']; f.snapshot = []
        def replacement():
            f.snapshot = None; f.replace()
        f.hooks['sample'] = replacement; f.vm.run('UpdateAim', .05)
        self.assertTrue(f.vm.state['operating']); self.assertGreater(f.vm.state['token'], old)
        self.assertEqual(f.native_token, f.vm.state['token'])

    def test_no_ammo_rejects_without_freezing(self):
        f = NativeSightFixture(); f.active(); f.ammo = 0; f.vm.run('BeginShot', 7)
        self.assertEqual(f.vm.state['phase'], 0); self.assertFalse(f.frozen)
        self.assertFalse(any(c[0] == 'capture' and c[2] for c in f.calls))

    def test_shot_freezes_actual_pose_atomically_without_applyaim(self):
        f = NativeSightFixture(); f.active(); f.vm.run('BeginShot', 7)
        self.assertTrue(f.frozen); self.assertEqual(f.vm.state['phase'], 1)
        self.assertEqual((f.vm.state['yaw'], f.vm.state['pitch']), tuple(f.pose)); self.assertEqual(f.applied, [])
        self.assertIn(('capture', f.vm.state['token'], True), f.calls)

    def test_invalid_freeze_snapshot_ends_session_without_launch(self):
        f = NativeSightFixture(); f.active(); f.snapshot = []; f.vm.run('BeginShot', 7)
        self.assertFalse(f.vm.state['operating']); self.assertFalse(f.frozen)
        self.assertEqual((f.ammo, f.launches), (10,0))

    def test_menu_cancellation_thaws_before_and_after_freeze_effect(self):
        for boundary in ('freeze_before', 'freeze_after'):
            f = NativeSightFixture(); f.active(); f.hooks[boundary] = f.open_menu
            f.vm.run('BeginShot', 7)
            self.assertTrue(f.vm.state['operating']); self.assertFalse(f.frozen)
            self.assertEqual(f.vm.state['phase'], 3); self.assertEqual((f.ammo,f.launches),(10,0))

    def test_freeze_return_cannot_mutate_or_thaw_new_lease(self):
        f = NativeSightFixture(); f.active(); old = f.vm.state['token']
        def replace_and_shoot():
            f.replace(); f.vm.state['heldFire'] = False
            f.vm.state.update(phase=0, needsReset=False)
            f.vm.run('BeginShot', f.vm.state['generation'])
        f.hooks['freeze_after'] = replace_and_shoot; f.vm.run('BeginShot', 7)
        self.assertTrue(f.vm.state['operating']); self.assertGreater(f.vm.state['token'], old)
        self.assertTrue(f.frozen); self.assertEqual(f.vm.state['phase'], 1)
        self.assertFalse(any(c[0] == 'frozen' and c[1] == f.vm.state['token'] for c in f.calls))

    def test_prepare_failure_thaws_and_returns_to_idle(self):
        f = NativeSightFixture(); f.active(); f.vm.run('BeginShot', 7)
        f.vm.native['PrepareShotAnimation'] = lambda generation: False
        f.vm.state['settleFrames'] = 2; f.vm.run('OnUpdate')
        self.assertFalse(f.frozen); self.assertEqual(f.vm.state['phase'], 0)

    def test_commit_thaws_after_single_launch_and_reload_can_aim(self):
        f = NativeSightFixture(); f.active(); f.vm.run('BeginShot', 7); f.vm.state['phase'] = 2
        f.vm.run('CommitShot', 7); f.vm.run('CommitShot', 7)
        self.assertEqual((f.ammo,f.launches),(9,1)); self.assertFalse(f.frozen)
        f.pose = [92., 45.]; f.vm.run('UpdateAim', .05)
        self.assertEqual((f.vm.state['yaw'],f.vm.state['pitch']),tuple(f.pose))

    def test_end_native_precedes_release_and_visual_cleanup(self):
        f = NativeSightFixture(); f.active(); f.vm.now += .4; f.vm.run('OnControlDown', 'Activate')
        order = [c[0] for c in f.calls]
        self.assertIn('end', order)
        self.assertLess(order.index('end'), order.index('release'))
        self.assertFalse(f.vm.state['operating']); self.assertIsNone(f.native_token)

    def test_end_boundary_cannot_reenter_before_old_cleanup_finishes(self):
        f = NativeSightFixture(); f.active()
        def try_reenter():
            f.vm.now += .4; f.enter()
        f.hooks['end'] = try_reenter; f.vm.run('EndSession')
        self.assertFalse(f.vm.state['operating']); self.assertEqual(f.lease.controls,[True]*8)

    def test_exit_rebases_cached_pose_after_end_before_next_entry(self):
        f = NativeSightFixture(); f.active(); f.vm.state['matricesReady'] = True
        f.vm.native['Is3DLoaded'] = lambda: True
        f.vm.state.update(yaw=37., pitch=24.)
        f.pose = [122., 66.]  # native frame occurred after the last PSC tick
        def restore():
            self.assertIsNone(f.native_token)
            f.pose = [f.vm.state['yaw'], f.vm.state['pitch']]
            f.calls.append(('restore_aim',))
        f.vm.native['ApplyAim'] = restore
        f.vm.run('EndSession')
        self.assertEqual(f.pose, [37.,24.])
        f.vm.now += .4; f.enter(); f.vm.run('OnUpdate')
        begin = [c for c in f.calls if c[0] == 'begin'][-1]
        self.assertEqual(list(begin[2:]), f.pose)
        self.assertLess([c[0] for c in f.calls].index('end'), [c[0] for c in f.calls].index('restore_aim'))

    def test_readiness_lost_while_frozen_is_visible_and_ends_before_launch(self):
        f = NativeSightFixture(); f.active(); f.vm.run('BeginShot',7)
        f.ready = False; f.vm.run('OnUpdate')
        self.assertFalse(f.vm.state['operating']); self.assertEqual((f.ammo,f.launches),(10,0))
        self.assertTrue(any(c[0] == 'shot_error' for c in f.calls))

    def test_stale_prepare_return_cannot_change_replacement_phase(self):
        for result in (False, True):
            f = NativeSightFixture(); f.active(); f.vm.run('BeginShot',7)
            f.vm.state['settleFrames'] = 2
            def prepare(generation):
                f.replace()
                return result
            f.vm.native['PrepareShotAnimation'] = prepare; f.vm.run('OnUpdate')
            self.assertTrue(f.vm.state['operating']); self.assertEqual(f.vm.state['phase'],3)
            self.assertIsNotNone(f.native_token)

    def test_stale_commit_failure_cannot_end_replacement_session(self):
        for boundary in ('CanOperate', 'ShotTransformReady'):
            f = NativeSightFixture(); f.active(); f.vm.run('BeginShot',7); f.vm.state['phase']=2
            def fail_late(*args):
                f.vm.native.pop(boundary, None)
                f.replace()
                return False
            f.vm.native[boundary] = fail_late; f.vm.run('CommitShot',7)
            self.assertTrue(f.vm.state['operating']); self.assertIsNotNone(f.native_token)
            self.assertEqual((f.ammo,f.launches),(10,0))

    def test_async_thaw_blocks_replacement_shot_on_same_token(self):
        f = NativeSightFixture(); f.active(); f.vm.run('BeginShot',7)
        attempted = []
        def nested():
            f.vm.state.update(phase=0,inputPaused=False,menuWasOpen=False)
            f.vm.run('BeginShot', f.vm.state['generation'])
            attempted.append(f.vm.state['phase'])
        f.hooks['thaw'] = nested; f.vm.run('PauseInput')
        self.assertEqual(attempted,[0]); self.assertFalse(f.frozen)

    def test_begin_return_after_deadline_cannot_mark_entry_ready(self):
        f = NativeSightFixture(); f.enter()
        f.hooks['begin_after'] = lambda: setattr(f.vm, 'now', f.vm.now + 2.)
        f.vm.run('OnUpdate')
        self.assertFalse(f.vm.state['operating']); self.assertEqual(f.lease.controls,[True]*8)

    def test_release_boundary_cannot_reenter_or_restore_under_new_native_lease(self):
        f = NativeSightFixture(); f.active(); f.vm.state['matricesReady'] = True
        f.vm.native['Is3DLoaded'] = lambda: True
        observed = []
        release = f.vm.state['Session'].Release
        def release_then_try(*args):
            release(*args); f.vm.now += .4; f.enter()
            observed.append(f.vm.state['operating'])
        f.vm.state['Session'].Release = release_then_try
        def apply():
            self.assertIsNone(f.native_token)
            f.applied.append((f.vm.state['yaw'],f.vm.state['pitch']))
        f.vm.native['ApplyAim'] = apply; f.vm.run('EndSession')
        self.assertEqual(observed,[False]); self.assertEqual(len(f.applied),1)

    def test_saved_cleanup_flag_onload_recovers_controls_and_allows_entry(self):
        f = NativeSightFixture(); f.active()
        f.vm.state.update(endingSession=True, operating=False, token=-1)
        f.vm.native['CaptureMatrices'] = lambda: False
        f.vm.run('OnLoad')
        self.assertFalse(f.vm.state['endingSession']); self.assertEqual(f.lease.controls,[True]*8)
        self.assertIsNone(f.native_token)
        f.vm.native['CaptureMatrices'] = lambda: True
        f.vm.now += .4; f.enter(); f.vm.run('OnUpdate')
        self.assertTrue(f.vm.state['operating']); self.assertIsNotNone(f.native_token)

    def test_old_end_after_load_recovery_cannot_restore_or_release_new_lease(self):
        f = NativeSightFixture(); f.active(); old = f.vm.state['token']
        f.vm.state['matricesReady'] = True; f.vm.native['Is3DLoaded'] = lambda: True
        def load_then_enter():
            f.vm.native['CaptureMatrices'] = lambda: False
            f.vm.run('OnLoad')
            f.vm.native['CaptureMatrices'] = lambda: True
            f.vm.now += .4; f.enter(); f.vm.run('OnUpdate')
        f.hooks['end'] = load_then_enter; f.vm.run('EndSession')
        self.assertTrue(f.vm.state['operating']); self.assertGreater(f.vm.state['token'],old)
        self.assertEqual(f.native_token,f.vm.state['token']); self.assertEqual(f.applied,[])
        self.assertEqual(f.lease.controls[:4],[False,False,False,True])

    def test_menu_during_operability_camera_read_preserves_valid_native_session(self):
        for boundary in ('before','after'):
            f = NativeSightFixture(); f.active()
            def menu_camera():
                f.lease.camera = 7; f.open_menu()
            f.lease.hooks[('camera',boundary)] = menu_camera; f.vm.run('OnUpdate')
            self.assertTrue(f.vm.state['operating']); self.assertTrue(f.vm.state['inputPaused'])
            self.assertEqual(f.lease.controls[:4],[False,False,False,True])

    def test_menu_mode_without_event_during_ready_read_discards_instead_of_fatal(self):
        f = NativeSightFixture(); f.active(); f.ready = False
        f.hooks['ready'] = lambda: setattr(f.vm, 'menu', True)
        f.vm.run('UpdateAim', .05)
        self.assertTrue(f.vm.state['operating'])

    def test_native_readiness_lost_before_attack_or_commit_cannot_launch(self):
        for function in ('BeginShot','CommitShot'):
            f = NativeSightFixture(); f.active()
            if function == 'CommitShot':
                f.vm.run('BeginShot',7); f.vm.state['phase'] = 2
            f.ready = False; f.vm.run(function, 7)
            self.assertFalse(f.vm.state['operating']); self.assertEqual((f.ammo,f.launches),(10,0))

    def test_reentrant_availability_check_cannot_overwrite_new_entry_token(self):
        f = NativeSightFixture(); f.hooks['available'] = f.enter
        f.enter(); f.vm.run('OnUpdate')
        self.assertTrue(f.vm.state['operating']); self.assertGreater(f.vm.state['token'],0)
        self.assertEqual(f.native_token,f.vm.state['token'])

    def test_old_cleanup_clock_or_unregister_cannot_reset_replacement_phase(self):
        for boundary in ('clock', 'UnregisterForAllKeys'):
            f = NativeSightFixture(); f.active(); f.vm.run('BeginShot',7)
            def load_and_replace():
                f.vm.native['CaptureMatrices'] = lambda: False
                f.vm.run('OnLoad')
                f.vm.native['CaptureMatrices'] = lambda: True
                f.vm.now += .4; f.enter(); f.vm.run('OnUpdate')
            if boundary == 'clock':
                def clock():
                    f.hook('clock'); return f.vm.now
                f.vm.state['Utility'].GetCurrentRealTime = clock
                f.hooks['clock'] = load_and_replace
            else:
                def unregister():
                    f.hook('unregister')
                f.vm.native[boundary] = unregister
                f.hooks['unregister'] = load_and_replace
            f.vm.run('EndSession')
            self.assertTrue(f.vm.state['operating']); self.assertEqual(f.vm.state['phase'],3)
            self.assertEqual(f.native_token,f.vm.state['token'])

    def test_restore_applyaim_can_never_write_during_native_operation(self):
        f = NativeSightFixture(); f.active()
        f.vm.native.pop('ApplyAim')
        f.vm.state.update(yawBase=[1.,0.,0.,0.,1.,0.,0.,0.,1.],pitchBase=[1.,0.,0.,0.,1.,0.,0.,0.,1.],yawMatrix=[0.]*9,pitchMatrix=[0.]*9)
        f.vm.state['NetImmerse'].SetNodeLocalRotationMatrix = lambda *args: f.applied.append(args[1])
        f.vm.run('ApplyAim')
        self.assertEqual(f.applied,[])

    def test_unfreeze_failure_is_visible_and_ends_session(self):
        f = NativeSightFixture(); f.active(); f.vm.run('BeginShot',7); f.thaw_ok = False
        f.vm.run('PauseInput')
        self.assertFalse(f.vm.state['operating']); self.assertEqual(f.lease.controls,[True]*8)

    def test_fire_reset_return_cannot_end_or_rephase_replacement_shot(self):
        for reset_result in (False, True):
            with self.subTest(reset_result=reset_result):
                f = NativeSightFixture(); f.active(); f.vm.run('BeginShot',7)
                old_token = f.vm.state['token']
                f.vm.state.update(phase=2, shotCommitted=True, elapsed=.6)
                armed = [True]
                def reset(animation, start):
                    if animation == 'Reset' and armed[0]:
                        armed[0] = False
                        f.replace()
                        f.vm.state.update(phase=0, needsReset=False, heldFire=False)
                        f.vm.run('BeginShot',f.vm.state['generation'])
                        f.vm.state['elapsed'] = .123
                        return reset_result
                    return True
                f.vm.native['PlayGamebryoAnimation'] = reset
                f.vm.run('OnUpdate')
                self.assertTrue(f.vm.state['operating'])
                self.assertGreater(f.vm.state['token'],old_token)
                self.assertEqual(f.native_token,f.vm.state['token'])
                self.assertEqual(f.vm.state['phase'],1)
                self.assertEqual(f.vm.state['shotGeneration'],f.vm.state['generation'])
                self.assertEqual(f.vm.state['elapsed'],.123)
                self.assertTrue(f.frozen)
                self.assertEqual((f.ammo,f.launches),(10,0))

    def test_cancel_reset_return_cannot_end_replacement_shot(self):
        for reset_result in (False, True):
            with self.subTest(reset_result=reset_result):
                f = NativeSightFixture(); f.active(); f.vm.run('BeginShot',7)
                old_token = f.vm.state['token']
                f.vm.native['Is3DLoaded'] = lambda: True
                armed = [True]
                def reset(animation, start):
                    if animation == 'Reset' and armed[0]:
                        armed[0] = False
                        f.replace()
                        f.vm.state.update(phase=0, needsReset=False, heldFire=False)
                        f.vm.run('BeginShot',f.vm.state['generation'])
                        f.vm.state['elapsed'] = .123
                        return reset_result
                    return True
                f.vm.native['PlayGamebryoAnimation'] = reset
                f.vm.run('CancelPendingShot')
                self.assertTrue(f.vm.state['operating'])
                self.assertGreater(f.vm.state['token'],old_token)
                self.assertEqual(f.native_token,f.vm.state['token'])
                self.assertEqual(f.vm.state['phase'],1)
                self.assertEqual(f.vm.state['shotGeneration'],f.vm.state['generation'])
                self.assertEqual(f.vm.state['elapsed'],.123)
                self.assertTrue(f.frozen)
                self.assertEqual((f.ammo,f.launches),(10,0))

    def test_reload_visual_return_preserves_replacement_shot_or_menu_context(self):
        for interruption in ('replacement_shot', 'menu'):
            with self.subTest(interruption=interruption):
                f = NativeSightFixture(); f.active()
                old_token = f.vm.state['token']
                f.vm.state.update(phase=3, needsReset=True, shotCommitted=True, elapsed=4.4)
                armed = [True]
                def scale(ref, node, value, first):
                    if armed[0]:
                        armed[0] = False
                        if interruption == 'replacement_shot':
                            f.replace()
                            f.vm.state.update(phase=0, needsReset=False, heldFire=False)
                            f.vm.run('BeginShot',f.vm.state['generation'])
                        else:
                            f.open_menu()
                f.vm.state['NetImmerse'].SetNodeScale = scale
                f.vm.run('OnUpdate')
                self.assertTrue(f.vm.state['operating'])
                self.assertEqual(f.native_token,f.vm.state['token'])
                self.assertEqual((f.ammo,f.launches),(10,0))
                if interruption == 'replacement_shot':
                    self.assertGreater(f.vm.state['token'],old_token)
                    self.assertEqual(f.vm.state['phase'],1)
                    self.assertEqual(f.vm.state['shotGeneration'],f.vm.state['generation'])
                    self.assertTrue(f.frozen)
                else:
                    self.assertEqual(f.vm.state['token'],old_token)
                    self.assertEqual(f.vm.state['phase'],3)
                    self.assertTrue(f.vm.state['needsReset'])
                    self.assertTrue(f.vm.state['shotCommitted'])
                    self.assertTrue(f.vm.state['inputPaused'])

    def test_old_update_clock_cannot_overwrite_replacement_reload_clock(self):
        f = NativeSightFixture(); f.active(); f.vm.now = 100.
        f.vm.state.update(phase=3, needsReset=True, shotCommitted=True, lastTick=100., elapsed=0.)
        armed = [True]
        def clock():
            captured = f.vm.now
            if armed[0]:
                armed[0] = False
                f.replace()
            return captured
        f.vm.state['Utility'].GetCurrentRealTime = clock
        f.vm.run('OnUpdate')
        self.assertTrue(f.vm.state['operating'])
        self.assertEqual(f.vm.state['phase'],3)
        self.assertAlmostEqual(f.vm.state['lastTick'],100.4)
        self.assertAlmostEqual(f.vm.state['elapsed'],0.)
        f.vm.now = 100.45; f.vm.run('OnUpdate')
        self.assertAlmostEqual(f.vm.state['elapsed'],.05)

    def test_old_pause_or_resume_clock_cannot_overwrite_replacement_clock(self):
        for function in ('PauseInput','ResumeInput'):
            with self.subTest(function=function):
                f = NativeSightFixture(); f.active(); f.vm.now = 100.
                f.vm.state.update(phase=3, needsReset=True, shotCommitted=True, lastTick=100.,elapsed=0.)
                if function == 'ResumeInput':
                    f.vm.state.update(inputPaused=True,menuWasOpen=True)
                armed = [True]
                def clock():
                    captured = f.vm.now
                    if armed[0]:
                        armed[0] = False
                        f.replace()
                    return captured
                f.vm.state['Utility'].GetCurrentRealTime = clock
                f.vm.run(function)
                self.assertTrue(f.vm.state['operating'])
                self.assertEqual(f.vm.state['phase'],3)
                self.assertFalse(f.vm.state['inputPaused'])
                self.assertFalse(f.vm.state['menuWasOpen'])
                self.assertAlmostEqual(f.vm.state['lastTick'],100.4)
                f.vm.now = 100.45; f.vm.run('OnUpdate')
                self.assertAlmostEqual(f.vm.state['elapsed'],.05)

    def test_stale_request_shot_after_resume_cannot_freeze_replacement(self):
        f = NativeSightFixture(); f.active()
        f.vm.state.update(inputPaused=True,menuWasOpen=True,heldFire=False)
        old_token = f.vm.state['token']; armed = [True]
        def clock():
            captured = f.vm.now
            if armed[0]:
                armed[0] = False; f.replace()
            return captured
        f.vm.state['Utility'].GetCurrentRealTime = clock
        f.vm.run('RequestShot')
        self.assertTrue(f.vm.state['operating']); self.assertGreater(f.vm.state['token'],old_token)
        self.assertEqual(f.vm.state['phase'],0); self.assertFalse(f.frozen)
        self.assertFalse(f.vm.state['heldFire'])
        self.assertEqual((f.ammo,f.launches),(10,0))

    def test_stale_request_exit_clock_cannot_end_replacement(self):
        f = NativeSightFixture(); f.active(); old_token = f.vm.state['token']; armed = [True]
        def clock():
            if armed[0]:
                armed[0] = False; f.replace(); f.vm.now += .4
            return f.vm.now
        f.vm.state['Utility'].GetCurrentRealTime = clock
        f.vm.run('RequestExit','old E')
        self.assertTrue(f.vm.state['operating']); self.assertGreater(f.vm.state['token'],old_token)
        self.assertEqual(f.native_token,f.vm.state['token']); self.assertEqual(f.vm.state['phase'],0)

    def test_input_ready_discards_replacement_during_menu_read_or_resume(self):
        for boundary in ('menu', 'resume_clock'):
            with self.subTest(boundary=boundary):
                f = NativeSightFixture(); f.active(); armed = [True]
                if boundary == 'resume_clock':
                    f.vm.state.update(inputPaused=True,menuWasOpen=True)
                def native_read():
                    captured = f.vm.menu if boundary == 'menu' else f.vm.now
                    if armed[0]:
                        armed[0] = False; f.replace()
                    return captured
                if boundary == 'menu':
                    f.vm.state['Utility'].IsInMenuMode = native_read
                else:
                    f.vm.state['Utility'].GetCurrentRealTime = native_read
                self.assertFalse(f.vm.run('InputReady'))
                self.assertTrue(f.vm.state['operating']); self.assertEqual(f.vm.state['phase'],0)

    def test_old_aim_key_after_resume_cannot_set_replacement_holds_or_release_gates(self):
        f = NativeSightFixture(); f.active()
        f.vm.state.update(inputPaused=True,menuWasOpen=True); armed = [True]
        def clock():
            captured = f.vm.now
            if armed[0]:
                armed[0] = False; f.replace()
            return captured
        f.vm.state['Utility'].GetCurrentRealTime = clock
        f.vm.run('SetAimKey',203,True)
        self.assertTrue(f.vm.state['operating'])
        self.assertFalse(f.vm.state['heldLeft']); self.assertFalse(f.vm.state['releaseLeft'])

    def test_old_event_after_trace_cannot_adopt_replacement_shot_or_exit(self):
        cases = [('OnKeyDown',256),('OnKeyDown',18),('OnControlDown','Right Attack/Block'),('OnControlDown','Activate'),('OnActivate',None)]
        for event, argument in cases:
            with self.subTest(event=event,argument=argument):
                f = NativeSightFixture(); f.active(); old_token = f.vm.state['token']
                f.vm.state.update(activateKeyboard=18,activateMouse=18,fireKeyboard=256,fireMouse=256)
                f.vm.state['Input'].GetMappedKey = lambda control,device: 18 if control == 'Activate' else 256
                f.vm.state['Debug'] = SimpleNamespace(Trace=lambda *args:f.hook('dispatch_trace'),Notification=lambda *args:None)
                def replace():
                    f.replace(); f.vm.now += .4
                f.hooks['dispatch_trace'] = replace
                f.vm.run(event,f.vm.state['player'] if event == 'OnActivate' else argument)
                self.assertTrue(f.vm.state['operating']); self.assertGreater(f.vm.state['token'],old_token)
                self.assertEqual(f.native_token,f.vm.state['token'])
                self.assertEqual(f.vm.state['phase'],0); self.assertFalse(f.frozen)
                self.assertEqual((f.ammo,f.launches),(10,0))


if __name__ == '__main__':
    unittest.main()
