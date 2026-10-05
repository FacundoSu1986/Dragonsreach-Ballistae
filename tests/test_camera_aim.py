"""Actual PSC arithmetic/branches, with explicit native fixtures, not a Papyrus VM."""
import math
import re
import unittest
from pathlib import Path
from types import SimpleNamespace

from tests.test_control_lease import NativeControlFixture, SOURCE
from tests.test_session_contract import InputContractEvaluator

ROOT = Path(__file__).resolve().parents[1]
ACTI = ROOT / 'mod/scripts/source/AstraAsedioActi.psc'
IDENTITY = [1., 0., 0., 0., 1., 0., 0., 0., 1.]


def rz(degrees):
    c, s = math.cos(math.radians(degrees)), math.sin(math.radians(degrees))
    return [c, -s, 0., s, c, 0., 0., 0., 1.]


class AimFixture:
    def __init__(self, camera=0):
        self.vm = InputContractEvaluator(ACTI.read_text())
        self.vm.state['UseSightCamera'] = False
        if 'UseMouseAim' not in self.vm.state or 'cameraEntryPending' not in self.vm.state:
            raise AssertionError('v04 mouse aim and bounded first-person entry are missing from actual PSC')
        self.lease = NativeControlFixture(SOURCE.read_text(), camera=camera)
        self.look = [0., 180.]
        self.matrix = IDENTITY.copy()
        self.hooks = {}
        self.applied = []
        self.angles_set = []
        self.registered = []
        self.self_ref = SimpleNamespace(EndSession=lambda: self.vm.run('EndSession'), UseSightCamera=False)
        player = SimpleNamespace(
            GetAngleX=lambda: self.angle(0), GetAngleZ=lambda: self.angle(1),
            SetAngle=self.set_angle, IsDead=lambda: self.lease.dead,
            GetItemCount=lambda ammo: 10,
        )
        self.vm.state.update(
            Self=self.self_ref, player=player, rootWorldMatrix=IDENTITY.copy(),
            Camera=self.lease.vm.state['Camera'],
            Game=SimpleNamespace(GetPlayer=lambda: player, IsLookingControlsEnabled=lambda:self.lease.controls[3]), SKSE=SimpleNamespace(GetVersion=lambda: 2, GetPluginVersion=lambda name: 0x03030000),
            AstraSightNative=self.lease.vm.state['AstraSightNative'],
            Launcher=object(), ShotAmmo=object(), SteelBolt=object(),
            NetImmerse=SimpleNamespace(GetNodeWorldRotationMatrix=self.root_matrix),
            Math=SimpleNamespace(Abs=abs, Sin=lambda x: math.sin(math.radians(x)),
                Cos=lambda x: math.cos(math.radians(x)), Sqrt=math.sqrt,
                ASin=lambda x: math.degrees(math.asin(x)), ACos=lambda x: math.degrees(math.acos(x))),
            Input=SimpleNamespace(GetMappedKey=lambda *args: 18),
            Session=SimpleNamespace(IsRunning=lambda: True,
                Acquire=lambda gun: self.lease.vm.run('Acquire', gun),
                IsCurrent=lambda gun, token: self.lease.vm.run('IsCurrent', gun, token),
                Release=lambda gun, token: self.lease.vm.run('Release', gun, token),
                EmergencyCleanup=lambda: self.lease.vm.run('EmergencyCleanup')),
        )
        self.vm.native.update(CaptureMatrices=lambda: True, NearOperator=lambda: True,
            ApplyAim=lambda: self.applied.append((self.vm.state['yaw'], self.vm.state['pitch'])),
            RegisterForSingleUpdate=lambda interval: self.registered.append(interval),
            RegisterForMenu=lambda *args: None, RegisterForKey=lambda *args: None,
            RegisterForControl=lambda *args: None, BlockActivation=lambda *args: None)
        # CanOperate executes the source guard, with only scene-node natives stubbed.
        self.vm.native.pop('CanOperate')
        self.vm.state['NetImmerse'].HasNode = lambda *args: True

    def hook(self, name):
        callback = self.hooks.pop(name, None)
        if callback:
            callback()

    def angle(self, index):
        value = self.look[index]
        self.hook('x' if index == 0 else 'z')
        return value

    def set_angle(self, x, y, z):
        self.angles_set.append((x, y, z))
        self.look = [x, z]
        self.hook('setangle')

    def root_matrix(self, ref, node, target, first):
        target[:] = self.matrix
        self.hook('matrix')
        return True

    def enter(self):
        self.vm.run('OnActivate', self.vm.state['player'])

    def active(self):
        token = self.lease.vm.run('Acquire', self.self_ref)
        self.vm.state.update(operating=True, generation=7, token=token,
            inputPaused=False, menuWasOpen=False, heldFire=False, cameraEntryPending=False,
            lastTick=self.vm.now)


class CameraLeaseContract(unittest.TestCase):
    def fixture(self, **kwargs):
        return NativeControlFixture(SOURCE.read_text(), **kwargs)

    def test_first_person_is_requested_only_for_saved_third_person(self):
        for saved in (0, 8, 9):
            f = self.fixture(camera=saved)
            gun = f.gun(); token = f.vm.run('Acquire', gun)
            self.assertGreater(token, 0)
            self.assertEqual(f.camera, 0)
            self.assertEqual(f.controls[:4], [False, False, False, True])
            f.vm.run('Release', gun, token)
            self.assertEqual(f.controls, [True] * 8)
            self.assertEqual(f.camera_calls, [] if saved == 0 else ['first', 'third'])
            if saved != 0:
                self.assertLess(f.order.index('enable'), f.order.index('third'))

    def test_special_camera_and_prelocked_looking_reject_without_global_toggles(self):
        for camera in (-1, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 99):
            f = self.fixture(camera=camera)
            self.assertEqual(f.vm.run('Acquire', f.gun()), -1)
            self.assertEqual(f.calls, []); self.assertEqual(f.camera_calls, [])
        f = self.fixture(looking=False, camera=9)
        self.assertEqual(f.vm.run('Acquire', f.gun()), -1)
        self.assertFalse(f.controls[3]); self.assertEqual(f.calls, [])

    def test_force_first_person_cancellation_rolls_back_and_keeps_acquisition_guard(self):
        for phase in ('before', 'after'):
            for cleanup in ('EmergencyCleanup', 'RestoreControls'):
                f = self.fixture(camera=8, movement=False, camswitch=False)
                gun, contender = f.gun(), f.gun(); observations = []
                def cancel():
                    observations.append(f.vm.run('Acquire', contender))
                    f.vm.run(cleanup)
                f.hooks[('first', phase)] = cancel
                self.assertEqual(f.vm.run('Acquire', gun), -1)
                self.assertEqual(observations, [-1])
                self.assertEqual(f.controls, [False, True, False, True, True, True, True, True])
                self.assertEqual(f.camera_calls, ['first', 'third'])
                self.assertFalse(f.vm.state['acquiring'])

    def test_camera_restore_guard_blocks_new_lease_through_native_third_person(self):
        for phase in ('before', 'after'):
            f = self.fixture(camera=9)
            gun, contender = f.gun(), f.gun(); token = f.vm.run('Acquire', gun)
            observations = []
            f.hooks[('third', phase)] = lambda: observations.append(f.vm.run('Acquire', contender))
            f.vm.run('Release', gun, token)
            self.assertEqual(observations, [-1]); self.assertFalse(f.vm.state['releasing'])

    def test_restore_skips_dead_menu_and_foreign_camera_including_special_after_enable(self):
        for state in (1, 3, 5, 6, 7, 8, 9, 10, 11, 12):
            f = self.fixture(camera=9); gun = f.gun(); token = f.vm.run('Acquire', gun)
            f.camera = state; f.vm.run('Release', gun, token)
            self.assertEqual(f.camera_calls, ['first'])
        for attribute in ('dead', 'menu'):
            f = self.fixture(camera=9); gun = f.gun(); token = f.vm.run('Acquire', gun)
            setattr(f, attribute, True); f.vm.run('Release', gun, token)
            self.assertEqual(f.camera_calls, ['first']); self.assertEqual(f.controls, [True] * 8)
        f = self.fixture(camera=8); gun = f.gun(); token = f.vm.run('Acquire', gun)
        f.hooks[('enable', 'after')] = lambda: setattr(f, 'camera', 5)
        f.vm.run('Release', gun, token); self.assertEqual(f.camera_calls, ['first'])

    def test_cancellation_before_camera_or_look_snapshot_never_forces_a_camera(self):
        for boundary in ('looking', 'camera', 'camswitch'):
            for phase in ('before', 'after'):
                f = self.fixture(camera=9)
                f.hooks[(boundary, phase)] = lambda: f.vm.run('EmergencyCleanup')
                self.assertEqual(f.vm.run('Acquire', f.gun()), -1)
                self.assertEqual(f.calls, []); self.assertEqual(f.camera_calls, [])


class MouseAimContract(unittest.TestCase):
    def test_papyrus_array_length_keyword_is_not_a_local_identifier(self):
        self.assertEqual(re.findall(r'(?im)^\s*(?:float|int|bool|string)\s+(length)\b',ACTI.read_text()),[])

    def sample(self, heading, angle_x=0., matrix=None, prior_yaw=0.):
        f = AimFixture(); f.active(); f.look = [angle_x, heading]
        if matrix is not None: f.matrix = matrix
        f.vm.state['yaw'] = prior_yaw
        self.assertTrue(f.vm.run('SampleLookAim', 7))
        return f.vm.state['yaw'], f.vm.state['pitch']

    def test_cardinal_mouse_heading_and_wrap_use_actual_psc_formula(self):
        for heading, expected in ((0,180), (90,90), (180,0), (270,270), (359,181), (1,179), (360,180)):
            with self.subTest(heading=heading):
                yaw, pitch = self.sample(heading)
                self.assertAlmostEqual(yaw, expected, places=5); self.assertAlmostEqual(pitch, 0.)

    def test_signed_x_pitch_clamp_and_vertical_yaw_preservation(self):
        for x, expected in ((-40,40), (320,40), (10,-5), (350,10), (-89,80), (89,-5)):
            yaw, pitch = self.sample(180, x)
            self.assertAlmostEqual(pitch, expected, places=5)
        yaw, pitch = self.sample(45, -90, prior_yaw=123.)
        self.assertEqual(yaw,123.); self.assertEqual(pitch,80.)

    def test_rotated_root_uses_transpose_without_heading_sign_regression(self):
        for turn in (35., 90., 180., 270.):
            yaw, pitch = self.sample(90., -25., rz(turn))
            self.assertAlmostEqual(yaw, (90.-turn)%360., places=5)
            self.assertAlmostEqual(pitch,25.,places=5)
        # Tilted root: world north/up direction becomes local south-forward.
        tilted = [1.,0.,0.,0.,0.,-1.,0.,1.,0.]
        yaw, pitch = self.sample(0., -90., tilted, prior_yaw=21.)
        self.assertAlmostEqual(yaw,180., places=5); self.assertAlmostEqual(pitch,0.,places=5)

    def test_invalid_angle_matrix_and_cancelled_native_sample_do_not_apply(self):
        for bad in (float('nan'), float('inf'), 1000001.):
            f = AimFixture(); f.active(); f.look[0] = bad
            self.assertFalse(f.vm.run('SampleLookAim',7)); self.assertEqual(f.applied,[])
        f = AimFixture(); f.active(); f.matrix[0] = float('nan')
        self.assertFalse(f.vm.run('SampleLookAim',7)); self.assertEqual(f.applied,[])
        for boundary in ('x','z','matrix'):
            f = AimFixture(); f.active(); f.hooks[boundary] = lambda: f.vm.run('EndSession')
            self.assertFalse(f.vm.run('SampleLookAim',7)); self.assertEqual(f.applied,[])

    def test_late_camera_boundary_cancel_and_special_camera_freeze_even_before_commit(self):
        f = AimFixture(); f.active()
        f.lease.hooks[('camera','after')] = lambda: f.vm.run('EndSession')
        self.assertFalse(f.vm.run('SampleLookAim',7)); self.assertEqual(f.applied,[])
        for phase in (0,1,2,3):
            f = AimFixture(camera=9); f.active(); f.lease.camera=5
            f.vm.state.update(phase=phase,shotGeneration=7)
            f.vm.run('OnUpdate')
            self.assertFalse(f.vm.state['operating']); self.assertEqual(f.applied,[])
            self.assertEqual(f.lease.camera,5); self.assertEqual(f.lease.camera_calls,['first'])

    def test_actual_muzzle_guard_uses_raised_pivot_for_rotated_roots(self):
        for yaw, pitch, turn in ((0.,0.,0.), (45.,80.,0.), (359.,-5.,35.), (120.,30.,90.)):
            f = AimFixture(); matrix=rz(turn); root=[20.,30.,465.5]
            c,s=math.cos(math.radians(pitch)),math.sin(math.radians(pitch))
            yc,ys=math.cos(math.radians(yaw)),math.sin(math.radians(yaw))
            local_forward=[ys*c,-yc*c,s]
            local_position=[(224.*c-19.6*s)*ys,(-224.*c+19.6*s)*yc,153.+224.*s+19.6*c]
            def transform(v): return [sum(matrix[row*3+col]*v[col] for col in range(3)) for row in range(3)]
            forward=transform(local_forward); translated=transform(local_position)
            muzzle=[root[i]+translated[i] for i in range(3)]
            projectile=IDENTITY.copy()
            for i in range(3): projectile[1+3*i]=forward[i]
            def rotation(ref,node,target,first):
                target[:]=projectile if node=='ProjectileNode' else matrix
                return True
            def position(ref,node,target,first):
                target[:]=muzzle if node=='ProjectileNode' else root
                return True
            f.vm.state.update(yaw=yaw,pitch=pitch,rootPosition=[0.]*3,muzzlePosition=[0.]*3,muzzleWorldMatrix=[0.]*9)
            f.vm.state['NetImmerse'].GetNodeWorldRotationMatrix=rotation
            f.vm.state['NetImmerse'].GetNodeWorldPosition=position
            f.vm.state['NetImmerse'].GetNodeScale=lambda *args:1.
            self.assertTrue(f.vm.run('ShotTransformReady'),f.vm.state['shotFailure'])

    def test_update_freezes_menu_and_precommit_fire_but_reload_samples_current_look(self):
        for phase, committed, expected in ((0,False,True),(1,False,False),(2,False,False),(2,True,True),(3,False,True)):
            f = AimFixture(); f.active(); f.look=[-50.,90.]
            f.vm.state.update(phase=phase,shotCommitted=committed)
            f.vm.run('OnUpdate')
            self.assertEqual(bool(f.applied), expected)
        f = AimFixture(); f.active(); f.vm.menu=True
        f.vm.run('OnUpdate'); self.assertEqual(f.applied,[])
        f.vm.menu=False; f.look=[-25.,270.]; f.vm.now=100.
        f.vm.run('OnUpdate'); self.assertEqual(f.applied,[(270.,25.)])
        self.assertEqual(f.registered[-1],.05)

    def test_aim_defaults_and_muzzle_height_are_linked_to_v04(self):
        f = AimFixture()
        self.assertTrue(f.vm.state['UseMouseAim']); self.assertEqual(f.vm.state['PitchMax'],80.)
        self.assertEqual(f.vm.state['PitchPivotHeight'],153.)
        body = ACTI.read_text().split('bool Function ShotTransformReady()')[1].split('EndFunction')[0]
        self.assertIn('lz = PitchPivotHeight +',body); self.assertNotIn('lz = 133.0 +',body)

    def test_mouse_attack_samples_fresh_look_before_freezing_shot(self):
        f = AimFixture(); f.active(); f.look=[-80.,90.]; phases=[]
        f.vm.native['ApplyAim']=lambda:phases.append(f.vm.state['phase'])
        f.vm.run('BeginShot',7)
        self.assertAlmostEqual(f.vm.state['yaw'],90.); self.assertAlmostEqual(f.vm.state['pitch'],80.)
        self.assertEqual(phases,[0]); self.assertEqual(f.vm.state['phase'],1)
        self.assertEqual(f.vm.state['settleFrames'],0); self.assertEqual(f.vm.state['shotGeneration'],7)

    def test_attack_during_periodic_mouse_read_preserves_shot_and_starts_settle_next_tick(self):
        for boundary in ('x','z','matrix'):
            with self.subTest(boundary=boundary):
                f = AimFixture(); f.active(); f.look=[-40.,90.]
                f.hooks[boundary]=lambda:f.vm.run('OnControlDown','Right Attack/Block')
                f.vm.run('OnUpdate')
                self.assertTrue(f.vm.state['operating'])
                self.assertEqual((f.vm.state['phase'],f.vm.state['shotGeneration'],f.vm.state['settleFrames']),(1,7,0))
                self.assertEqual(f.vm.state['generation'],7)
                self.assertAlmostEqual(f.vm.state['yaw'],90.); self.assertAlmostEqual(f.vm.state['pitch'],40.)
                f.vm.now+=.05; f.vm.run('OnUpdate')
                self.assertEqual(f.vm.state['settleFrames'],1)

    def test_menu_during_periodic_mouse_read_pauses_without_advancing_phase_or_timer(self):
        for boundary in ('x','z','matrix'):
            for phase, committed in ((0,False),(2,True),(3,False)):
                with self.subTest(boundary=boundary,phase=phase):
                    f = AimFixture(); f.active(); f.vm.state.update(phase=phase,shotCommitted=committed,elapsed=.1)
                    f.vm.now+=.1
                    def menu_open():
                        f.vm.menu=True
                        f.vm.run('OnMenuOpen','InventoryMenu')
                    f.hooks[boundary]=menu_open
                    f.vm.run('OnUpdate')
                    self.assertTrue(f.vm.state['operating']); self.assertTrue(f.vm.state['inputPaused'])
                    self.assertTrue(f.vm.state['menuWasOpen']); self.assertEqual(f.vm.state['phase'],phase)
                    self.assertEqual(f.vm.state['elapsed'],.1); self.assertEqual(f.applied,[])
                    self.assertEqual(f.lease.controls[:4],[False,False,False,True])

    def test_menu_mode_without_callback_during_mouse_native_also_pauses_cycle(self):
        f = AimFixture(); f.active(); f.vm.state.update(phase=3,elapsed=.1)
        f.vm.now+=.1; f.hooks['x']=lambda:setattr(f.vm,'menu',True)
        f.vm.run('OnUpdate')
        self.assertTrue(f.vm.state['operating']); self.assertTrue(f.vm.state['inputPaused'])
        self.assertEqual(f.vm.state['phase'],3); self.assertEqual(f.vm.state['elapsed'],.1)

    def test_menu_camera_transition_during_sample_preserves_pause_and_lease(self):
        f = AimFixture(); f.active(); f.vm.state.update(phase=3,elapsed=.1)
        f.vm.now+=.1
        def tween_menu():
            f.lease.camera=7
            f.vm.menu=True
            f.vm.run('OnMenuOpen','TweenMenu')
        f.hooks['x']=tween_menu
        f.vm.run('OnUpdate')
        self.assertTrue(f.vm.state['operating']); self.assertTrue(f.vm.state['inputPaused'])
        self.assertEqual(f.vm.state['elapsed'],.1); self.assertEqual(f.lease.controls[:4],[False,False,False,True])
        self.assertEqual(f.lease.camera,7); self.assertEqual(f.lease.camera_calls,[])

    def test_stale_periodic_sample_cannot_close_a_replacement_generation(self):
        for old_angle in (0.,float('nan')):
            with self.subTest(old_angle=old_angle):
                f = AimFixture(); f.active(); f.look[0]=old_angle
                original_token=f.vm.state['token']
                def replace_session():
                    f.vm.run('EndSession')
                    f.vm.now+=.4
                    f.enter()
                f.hooks['x']=replace_session
                f.vm.run('OnUpdate')
                self.assertTrue(f.vm.state['operating']); self.assertTrue(f.vm.state['cameraEntryPending'])
                self.assertEqual(f.vm.state['generation'],9); self.assertGreater(f.vm.state['token'],original_token)
                self.assertTrue(f.lease.vm.run('IsCurrent',f.self_ref,f.vm.state['token']))
                self.assertEqual(f.vm.state['phase'],0); self.assertEqual(f.lease.controls[:4],[False,False,False,True])

    def test_periodic_invalid_arithmetic_root_camera_and_lease_still_end_current_session(self):
        for cause in ('angle','root','camera','lease'):
            with self.subTest(cause=cause):
                f = AimFixture(); f.active()
                if cause=='angle': f.look[0]=float('nan')
                if cause=='root': f.matrix[0]=float('nan')
                if cause=='camera': f.hooks['x']=lambda:setattr(f.lease,'camera',5)
                if cause=='lease': f.hooks['x']=lambda:f.lease.vm.run('RestoreControls')
                f.vm.run('OnUpdate')
                self.assertFalse(f.vm.state['operating']); self.assertEqual(f.applied,[])
                self.assertEqual(f.lease.controls,[True]*8)

    def test_sample_result_distinguishes_applied_context_change_and_invalid_data(self):
        f = AimFixture(); f.active()
        self.assertIn('SampleLookAimResult',f.vm.bodies)
        f.vm.state['phase']=1
        self.assertEqual(f.vm.run('SampleLookAimResult',7),0)
        f.vm.state['phase']=0; f.look[0]=float('nan')
        self.assertEqual(f.vm.run('SampleLookAimResult',7),-1)
        f.look=[-40.,90.]
        self.assertEqual(f.vm.run('SampleLookAimResult',7),1)

    def test_cancellation_during_click_sample_or_last_ammo_read_never_freezes_stale_shot(self):
        for boundary in ('sample','ammo'):
            with self.subTest(boundary=boundary):
                f = AimFixture(); f.active()
                if boundary=='sample': f.hooks['x']=lambda:f.vm.run('EndSession')
                else:
                    def count(ammo):
                        f.vm.run('EndSession')
                        return 10
                    f.vm.state['player'].GetItemCount=count
                f.vm.run('BeginShot',7)
                self.assertFalse(f.vm.state['operating']); self.assertEqual(f.vm.state['phase'],0)
                self.assertEqual(f.vm.state['shotGeneration'],-1)

    def test_arrow_fallback_begin_shot_preserves_direction_and_entry_wait_cannot_fire(self):
        f = AimFixture(); f.active(); f.vm.state.update(UseMouseAim=False,yaw=42.,pitch=10.)
        f.vm.native['SampleLookAim']=lambda *args:(_ for _ in ()).throw(AssertionError('fallback must not sample mouse'))
        f.vm.run('BeginShot',7)
        self.assertEqual((f.vm.state['yaw'],f.vm.state['pitch'],f.vm.state['phase']),(42.,10.,1))
        f = AimFixture(camera=9); f.lease.force_immediate=False; f.enter()
        f.vm.run('BeginShot',f.vm.state['generation'])
        self.assertEqual(f.vm.state['phase'],0)


class FirstPersonEntryContract(unittest.TestCase):
    def test_activation_rejections_explain_prelocked_looking_and_special_camera(self):
        for reason in ('looking','camera'):
            f = AimFixture(camera=5 if reason=='camera' else 9); rejected=[]
            if reason=='looking': f.lease.controls[3]=False
            f.vm.native['RejectActivation']=lambda message:rejected.append(message)
            f.enter()
            self.assertFalse(f.vm.state['operating']); self.assertEqual(f.lease.calls,[])
            self.assertEqual(len(rejected),1)
            self.assertIn('LOOKING_CONTROLS_DISABLED' if reason=='looking' else 'CAMERA_STATE_UNSUPPORTED',rejected[0])
        source=ACTI.read_text().split('Event OnActivate(')[1].split('EndEvent')[0]
        self.assertNotIn('otra ballesta tiene',source)

    def test_entry_aligns_rotated_weapon_before_mouse_sample_without_player_translation(self):
        f = AimFixture(camera=9); f.matrix=rz(90.); f.vm.state.update(yaw=35.,pitch=25.)
        f.enter(); self.assertTrue(f.vm.state['operating']); self.assertTrue(f.vm.state['cameraEntryPending'])
        self.assertEqual(len(f.angles_set),1)
        f.vm.run('OnUpdate')
        self.assertFalse(f.vm.state['cameraEntryPending'])
        self.assertAlmostEqual(f.vm.state['yaw'],35.,places=5); self.assertAlmostEqual(f.vm.state['pitch'],25.,places=5)
        source=ACTI.read_text()
        for forbidden in ('MoveTo(', 'SetPosition(', 'SetWorldFOV(', 'SetFirstPersonFOV('):
            self.assertNotIn(forbidden,source)

    def test_transition_uses_finite_deadline_instead_of_treating_void_force_as_success(self):
        f = AimFixture(camera=9); f.lease.force_immediate=False
        f.enter(); self.assertTrue(f.vm.state['cameraEntryPending'])
        f.lease.camera=6; f.vm.now=10.2; f.vm.run('OnUpdate')
        self.assertTrue(f.vm.state['operating']); self.assertEqual(f.applied,[])
        f.vm.now=12.; f.vm.run('OnUpdate')
        self.assertFalse(f.vm.state['operating']); self.assertEqual(f.applied,[])
        self.assertEqual(f.lease.controls,[True]*8)
        self.assertEqual(f.lease.camera_calls,['first'])

    def test_invalidated_lease_during_entry_ends_instead_of_rescheduling_forever(self):
        f = AimFixture(camera=9); f.lease.force_immediate=False
        f.enter(); f.lease.vm.run('RestoreControls')
        f.vm.run('OnUpdate')
        self.assertFalse(f.vm.state['operating']); self.assertFalse(f.vm.state['cameraEntryPending'])
        self.assertEqual(len(f.registered),1)

    def test_nonfinite_initial_clock_rolls_back_without_rotating_player(self):
        for value in (float('inf'),float('-inf'),float('nan'),-1.):
            f = AimFixture(camera=9); f.vm.now=value
            f.enter()
            self.assertFalse(f.vm.state['operating'])
            self.assertEqual(f.angles_set,[]); self.assertEqual(f.lease.controls,[True]*8)

    def test_cancel_in_last_alignment_preflight_does_not_rotate_after_release(self):
        f = AimFixture(camera=9); reads=[]
        def dead_read():
            reads.append(True)
            if len(reads)==2: f.vm.run('EndSession')
            return False
        f.vm.state['player'].IsDead=dead_read
        f.enter()
        self.assertFalse(f.vm.state['operating']); self.assertEqual(f.angles_set,[])
        self.assertEqual(f.lease.controls,[True]*8)

    def test_menu_death_nan_clock_special_camera_or_setangle_cancel_roll_back_entry(self):
        for reason in ('menu','dead','nan','special','setangle'):
            f = AimFixture(camera=9)
            if reason=='setangle': f.hooks['setangle']=lambda:f.vm.run('EndSession')
            f.enter()
            if reason=='menu': f.vm.menu=True; f.lease.menu=True
            if reason=='dead': f.lease.dead=True
            if reason=='nan': f.vm.now=float('nan')
            if reason=='special': f.lease.camera=5
            if reason!='setangle': f.vm.run('OnUpdate')
            self.assertFalse(f.vm.state['operating'],reason)
            self.assertEqual(f.lease.controls,[True]*8,reason)
            self.assertEqual(f.applied,[],reason)

    def test_saved_active_session_load_releases_before_restoring_visuals(self):
        f = AimFixture(camera=9); f.enter()
        f.vm.native.update(CaptureMatrices=lambda:False, BlockActivation=lambda *args:None)
        f.vm.run('OnLoad')
        self.assertFalse(f.vm.state['operating']); self.assertEqual(f.lease.controls,[True]*8)
        self.assertEqual(f.lease.camera_calls,['first','third'])


if __name__=='__main__': unittest.main()
