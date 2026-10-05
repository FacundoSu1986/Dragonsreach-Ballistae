"""v09 fixes for the v08 in-game findings, on the actual PSC with native boundary fixtures.

Evidence: reports/user_evidence_v08.json. These tests run Papyrus branches outside the
engine; they reproduce the orderings the logs imply, not the Skyrim VM scheduler.
"""
import unittest
from tests.test_native_sight import NativeSightFixture


class Base(unittest.TestCase):
    def fixture(self):
        f = NativeSightFixture(); f.active()
        f.vm.state['AstraSightNative'].ValidateShot = lambda *args: True
        f.vm.state.update(fireMouse=256, fireKeyboard=-1, activateKeyboard=18, modeKeyboard=42, modeMouse=-1)
        return f

    def cycle(self, f, ticks=45):
        for _ in range(ticks):
            f.vm.now += .05; f.vm.run('OnUpdate')

    def errors(self, f):
        return [c[1] for c in f.calls if c[0] == 'shot_error']


class StuckBurst(Base):
    """07:31:59-07:32:21: ten launches with no key event after the last click."""

    def test_release_handled_while_the_press_is_suspended_stops_the_burst(self):
        f = self.fixture(); f.vm.state['ContinuousFire'] = True
        utility = f.vm.state['Utility']; original = utility.IsInMenuMode; done = []
        def suspended_read():
            # The press handler waits on this native; the release event runs meanwhile.
            if not done:
                done.append(1); f.vm.run('OnKeyUp', 256, .08)
            return original()
        utility.IsInMenuMode = suspended_read
        f.vm.run('OnKeyDown', 256)
        utility.IsInMenuMode = original
        self.cycle(f); self.cycle(f); self.cycle(f)
        self.assertEqual(f.launches, 1)
        self.assertFalse(f.vm.state['repeatFire'])

    def test_release_after_the_press_completed_still_stops_the_burst(self):
        f = self.fixture(); f.vm.state['ContinuousFire'] = True
        f.vm.run('OnKeyDown', 256)
        for _ in range(8):
            f.vm.now += .05; f.vm.run('OnUpdate')
        f.vm.run('OnKeyUp', 256, .4)
        self.cycle(f); self.cycle(f)
        self.assertEqual(f.launches, 1)

    def test_next_press_after_a_suspended_release_is_accepted(self):
        # v08 latched heldFire over the release, so the following click was ignored.
        f = self.fixture()
        utility = f.vm.state['Utility']; original = utility.IsInMenuMode; done = []
        def suspended_read():
            if not done:
                done.append(1); f.vm.run('OnKeyUp', 256, .08)
            return original()
        utility.IsInMenuMode = suspended_read
        f.vm.run('OnKeyDown', 256)
        utility.IsInMenuMode = original
        self.cycle(f)
        f.vm.run('OnKeyDown', 256); self.cycle(f)
        self.assertEqual(f.launches, 2)

    def test_attack_release_is_traced_for_the_next_in_game_log(self):
        # No Papyrus poll is used for the key (v02: Input.IsKeyPressed never answered in game);
        # the release event itself must leave evidence.
        body = self.fixture().vm.source.split('Event OnKeyUp(')[1].split('EndEvent')[0]
        fire = body.split('if keyCode == fireKeyboard || keyCode == fireMouse')[1].split('elseif')[0]
        self.assertIn('Debug.Trace("AstraAsedio OnKeyUp code="', fire)
        self.assertLess(fire.index('fireReleaseSerial += 1'), fire.index('Debug.Trace('))

    def test_held_key_still_repeats(self):
        f = self.fixture(); f.vm.state['ContinuousFire'] = True
        f.vm.run('OnKeyDown', 256)
        self.cycle(f); self.cycle(f)
        self.assertGreaterEqual(f.launches, 2)

    def test_control_only_delivery_keeps_edge_semantics(self):
        # Without a key event there is no physical key to read; the control release governs.
        f = self.fixture(); f.vm.state['ContinuousFire'] = True
        f.vm.run('OnControlDown', 'Right Attack/Block')
        self.cycle(f); self.cycle(f)
        self.assertGreaterEqual(f.launches, 2)
        f.vm.run('OnControlUp', 'Right Attack/Block', .5); before = f.launches
        self.cycle(f); self.cycle(f)
        self.assertLessEqual(f.launches, before + 1)


class FirstEntryYaw(Base):
    """07:30:03: float(pi) heading makes the native yaw 359.999995, returned as float 360.0."""

    def test_sample_of_exactly_360_is_the_same_direction_as_zero(self):
        f = self.fixture(); f.snapshot = [360.0, 0.0]
        self.cycle(f, 3)
        self.assertTrue(f.vm.state['operating'])
        self.assertEqual(f.vm.state['yaw'], 0.0)
        self.assertNotIn('NATIVE_SIGHT_SAMPLE_FAILED: se perdió la mira nativa.', self.errors(f))

    def test_out_of_range_yaw_is_still_rejected(self):
        f = self.fixture(); f.snapshot = [360.5, 0.0]
        self.cycle(f, 3)
        self.assertFalse(f.vm.state['operating'])


class MenuSuspension(Base):
    """07:32:21: a menu camera made AstraSight drop the sight while a shot was frozen; the thaw
    failed and Papyrus ended the session. v09: AstraSight suspends (the lease, pose and freeze
    survive, the fixture's native token stays) and Papyrus waits for first person after a menu."""

    def tween(self, f, state):
        f.lease.camera = state

    def open_menu(self, f, menu='TweenMenu'):
        self.tween(f, 7); f.vm.menu = True; f.vm.run('OnMenuOpen', menu)

    def close_menu(self, f, menu='TweenMenu'):
        f.vm.menu = False; f.vm.run('OnMenuClose', menu)

    def test_frozen_shot_during_a_menu_keeps_the_session(self):
        f = self.fixture(); f.vm.state['ContinuousFire'] = True
        f.vm.run('OnKeyDown', 256)
        self.assertEqual(f.vm.state['phase'], 1); self.assertTrue(f.frozen)
        self.open_menu(f)                     # PauseInput -> CancelPendingShot -> ThawSight
        self.assertTrue(f.vm.state['operating'])
        self.assertFalse(f.frozen)
        self.assertNotIn('NATIVE_SIGHT_THAW_FAILED: se perdió la mira nativa.', self.errors(f))
        self.close_menu(f); self.cycle(f, 6)  # camera still in the tween state, within grace
        self.assertTrue(f.vm.state['operating'])
        self.tween(f, 0); self.cycle(f)
        self.assertTrue(f.vm.state['operating'])
        self.assertEqual(f.launches, 0)       # the cancelled shot never fires, no catch-up
        f.vm.run('OnKeyUp', 256, 1.); f.vm.run('OnKeyDown', 256); self.cycle(f)
        self.assertGreaterEqual(f.launches, 1)   # Continuo with Attack held keeps firing

    def test_click_right_after_the_menu_while_the_camera_returns_does_not_end(self):
        f = self.fixture()
        self.open_menu(f); self.close_menu(f)
        f.vm.run('OnKeyDown', 256)            # camera state 7 within grace: discarded, not fatal
        self.assertEqual(f.vm.state['phase'], 0)   # no half-started shot left for the next tick
        self.cycle(f, 4)
        self.assertTrue(f.vm.state['operating']); self.assertEqual(f.launches, 0)
        self.assertEqual(self.errors(f), [])
        self.tween(f, 0); f.vm.run('OnKeyUp', 256, .2); self.cycle(f, 2)
        f.vm.run('OnKeyDown', 256); self.cycle(f)
        self.assertEqual(f.launches, 1)

    def test_camera_not_back_after_the_grace_ends_the_session(self):
        f = self.fixture(); self.open_menu(f); self.close_menu(f)
        self.cycle(f, 80)                     # 4 s in the tween state
        self.assertFalse(f.vm.state['operating'])

    def test_camera_leaving_first_person_without_a_menu_still_ends(self):
        f = self.fixture(); self.tween(f, 7)
        self.cycle(f, 2)
        self.assertFalse(f.vm.state['operating'])

    def test_sight_lost_without_a_menu_still_ends_the_session(self):
        f = self.fixture(); f.native_token = None
        self.cycle(f, 3)
        self.assertFalse(f.vm.state['operating'])
        self.assertEqual(len([c for c in f.calls if c[0] == 'begin']), 0)

    def test_long_menu_tick_before_menu_close_waits_for_the_camera(self):
        # Re-check N1: the grace must count from the first post-menu observation, not the open.
        f = self.fixture(); self.open_menu(f)
        f.vm.now += 5.0                       # menu held open 5 s
        f.vm.menu = False                     # the pending tick runs before OnMenuClose arrives
        self.cycle(f, 3)
        self.assertTrue(f.vm.state['operating'])
        self.close_menu(f); self.cycle(f, 3)
        self.assertTrue(f.vm.state['operating'])
        self.tween(f, 0); self.cycle(f, 3)
        self.assertTrue(f.vm.state['operating'])

    def test_long_menu_tick_inside_menu_close_waits_for_the_camera(self):
        f = self.fixture(); self.open_menu(f)
        f.vm.now += 5.0; f.vm.menu = False
        utility = f.vm.state['Utility']; original = utility.GetCurrentRealTime; done = []
        def clock():
            if not done:
                done.append(1); f.vm.now += .05; f.vm.run('OnUpdate')   # tick inside OnMenuClose's native call
            return original()
        utility.GetCurrentRealTime = clock
        f.vm.run('OnMenuClose', 'TweenMenu')
        utility.GetCurrentRealTime = original
        self.cycle(f, 3)
        self.assertTrue(f.vm.state['operating'])

    def test_menu_inside_a_tick_during_a_frozen_shot_keeps_the_tick_chain(self):
        # Re-check M4: CancelPendingShot changes the generation mid-tick; the tick must reschedule.
        f = self.fixture()
        f.vm.run('OnKeyDown', 256); self.assertEqual(f.vm.state['phase'], 1)
        f.hooks['ready'] = lambda: self.open_menu(f)
        before = len(f.registered)
        f.vm.now += .05; f.vm.run('OnUpdate')
        self.assertTrue(f.vm.state['operating'])
        self.assertGreater(len(f.registered), before, 'tick chain stopped after the cancelled shot')
        self.close_menu(f); self.tween(f, 0); self.cycle(f)
        f.vm.run('OnKeyUp', 256, 1.); f.vm.run('OnKeyDown', 256); self.cycle(f)
        self.assertGreaterEqual(f.launches, 1)

    def test_no_papyrus_reentry_is_left(self):
        source = self.fixture().vm.source
        self.assertNotIn('Reentry', source)
        sample = source.split('int Function SampleSightAimResult(')[1].split('EndFunction')[0]
        self.assertIn('(cameraState == 6 || cameraState == 7) && graceNow < cameraGraceUntil', sample)


class OperatorMessage(Base):
    """07:32:21: "OPERATOR_OUT_OF_RANGE dx=-63 dy=56" although 85 u < 160 u and 11 u < 64 u."""

    def test_sight_failure_does_not_blame_the_operator_position(self):
        f = self.fixture()
        f.vm.state['operatorFailure'] = 'OPERATOR_OUT_OF_RANGE: Acércate a la manivela. dx=-63 dy=56 dz=-11'
        f.ready = False
        f.vm.run('OnKeyDown', 256)
        reasons = self.errors(f)
        self.assertTrue(reasons)
        self.assertFalse(any('OPERATOR_OUT_OF_RANGE' in r for r in reasons), reasons)
        self.assertTrue(any('NATIVE_SIGHT' in r for r in reasons), reasons)

    def test_operator_check_clears_its_message_when_in_range(self):
        source = (f := self.fixture()).vm.source
        gate = source.split('bool Function NearOperator()')[1].split('EndFunction')[0]
        self.assertIn('operatorFailure = ""', gate.split('return dx*dx')[0].split('OPERATOR_POSITION_INVALID')[1])


class SprintLatch(Base):
    def test_sprint_release_handled_during_the_press_does_not_swallow_the_next_toggle(self):
        f = self.fixture(); utility = f.vm.state['Utility']; original = utility.IsInMenuMode; done = []
        def suspended_read():
            if not done:
                done.append(1); f.vm.run('OnKeyUp', 42, .08)
            return original()
        utility.IsInMenuMode = suspended_read
        f.vm.run('OnKeyDown', 42)
        utility.IsInMenuMode = original
        self.assertTrue(f.vm.state['ContinuousFire'])
        f.vm.run('OnKeyDown', 42); f.vm.run('OnKeyUp', 42, .08)
        self.assertFalse(f.vm.state['ContinuousFire'])


class NativeGate(Base):
    def test_older_dlls_without_the_tail_sight_are_rejected(self):
        # v10: the PSC needs AstraSight 3.3 (tail camera + front post); 3.1 (v08) and 3.2 (v09) are refused.
        for version in (0x03010000, 0x03020000):
            f = NativeSightFixture(); f.version = version; f.enter()
            self.assertFalse(f.vm.state['operating'])
            self.assertTrue(any(c[0] == 'reject' and 'AstraSight.dll 3.3.0' in c[1] for c in f.calls), f.calls)

    def test_v10_dll_is_accepted(self):
        f = NativeSightFixture(); f.version = 0x03030000; f.enter()
        self.assertTrue(f.vm.state['operating'])


if __name__ == '__main__':
    unittest.main()
