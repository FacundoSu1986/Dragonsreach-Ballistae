"""Exercise actual PSC branches with native boundary fixtures; not the engine."""
import unittest
from tests.test_native_sight import NativeSightFixture

class ContinuousFiring(unittest.TestCase):
    def fixture(self):
        f=NativeSightFixture();f.active()
        f.version=0x03030000
        f.vm.state['AstraSightNative'].GetAPIVersion=lambda:3
        f.vm.state['AstraSightNative'].ValidateShot=lambda *args: True
        f.vm.native.pop('RejectShot')
        f.vm.state.update(fireMouse=256,activateKeyboard=18,modeKeyboard=42,modeMouse=-1)
        return f
    def cycle(self,f):
        for _ in range(45):
            f.vm.now+=.05;f.vm.run('OnUpdate')
    def test_native_prepares_first_scheduled_tick(self):
        f=self.fixture();f.vm.run('RequestShot');f.vm.now+=.05;f.vm.run('OnUpdate')
        self.assertEqual(f.vm.state['phase'],2)
    def test_tick_during_freeze_handshake_waits_for_snapshot_publication(self):
        for boundary in ['freeze_before','freeze_after']:
            f=self.fixture();f.vm.native.pop('ShotTransformReady')
            f.vm.state['AstraSightNative'].ValidateShot=lambda *args:f.frozen
            def tick():f.vm.now+=.05;f.vm.run('OnUpdate')
            f.hooks[boundary]=tick;f.vm.run('RequestShot')
            self.assertEqual(f.vm.state['phase'],1,boundary);self.assertTrue(f.frozen,boundary)
            tick();self.assertEqual(f.vm.state['phase'],2)
            f.vm.now+=.11;f.vm.run('OnUpdate');self.assertEqual(f.launches,1)
    def test_fast_defaults(self):
        f=self.fixture()
        self.assertEqual([f.vm.state[n] for n in ['FireSeconds','ReleaseSeconds','ResetSeconds','CycleSeconds']],[.3,.1,1.2,1.5])
    def test_native_can_operate_does_not_poll_scene_nodes_or_operator(self):
        f=self.fixture()
        f.vm.native['NearOperator']=lambda:self.fail('expensive Papyrus operator poll')
        f.vm.state['NetImmerse'].HasNode=lambda *args:self.fail('Papyrus HasNode poll')
        self.assertTrue(f.vm.run('CanOperate',7))
    def test_preflight_calls_native_snapshot_once(self):
        f=self.fixture();f.vm.native.pop('ShotTransformReady');calls=[]
        f.vm.state['AstraSightNative'].ValidateShot=lambda *args:(calls.append(args),True)[1]
        self.assertTrue(f.vm.run('ShotTransformReady'));self.assertEqual(len(calls),1)
        f.vm.state['AstraSightNative'].ValidateShot=lambda *args:False
        self.assertFalse(f.vm.run('ShotTransformReady'))
    def test_repeat_release_at_ammo_boundary_never_starts_another_cycle(self):
        for stop in ['release','menu','mode']:
            f=self.fixture();f.vm.state.update(ContinuousFire=True,repeatFire=True)
            def ammo_boundary(ammo):
                if stop=='release':f.vm.run('OnKeyUp',256,.5)
                elif stop=='menu':f.open_menu()
                else:f.vm.run('RequestFireMode')
                return 10
            f.vm.state['player'].GetItemCount=ammo_boundary
            f.vm.run('TryRepeatShot',7)
            self.assertEqual(f.vm.state['phase'],0);self.assertFalse(f.frozen)
            self.assertEqual(f.launches,0)
    def test_old_repeat_callback_cannot_adopt_replacement_session(self):
        f=self.fixture();f.vm.state.update(ContinuousFire=True,repeatFire=True)
        f.vm.state['player'].GetItemCount=lambda ammo:(f.replace(),10)[1]
        f.vm.run('TryRepeatShot',7)
        self.assertTrue(f.vm.state['operating']);self.assertEqual(f.vm.state['phase'],0)
        self.assertFalse(f.vm.state['repeatFire']);self.assertEqual(f.launches,0)
    def test_continuous_holding_repeats_once_per_cycle(self):
        f=self.fixture();f.vm.state['ContinuousFire']=True;f.vm.run('OnKeyDown',256)
        self.cycle(f);self.cycle(f)
        self.assertGreaterEqual(f.launches,2);self.assertEqual(f.ammo,10-f.launches)
    def test_single_hold_never_repeats(self):
        f=self.fixture();f.vm.state['ContinuousFire']=False;f.vm.run('OnKeyDown',256)
        self.cycle(f);self.cycle(f)
        self.assertEqual(f.launches,1)
    def test_release_stops_future_shots(self):
        for delivery in ['key','control']:
            f=self.fixture();f.vm.state['ContinuousFire']=True;f.vm.run('OnKeyDown',256)
            for _ in range(8):f.vm.now+=.05;f.vm.run('OnUpdate')
            if delivery=='key':f.vm.run('OnKeyUp',256,.4)
            else:f.vm.run('OnControlUp','Right Attack/Block',.4)
            self.cycle(f);self.cycle(f);self.assertEqual(f.launches,1)
    def test_menu_requires_new_press_and_has_no_catchup(self):
        f=self.fixture();f.vm.state['ContinuousFire']=True;f.vm.run('OnKeyDown',256)
        self.cycle(f);f.open_menu();before=f.launches;f.vm.now+=25;f.close_menu()
        self.cycle(f);self.cycle(f);self.assertEqual(f.launches,before)
        f.vm.run('OnKeyUp',256,1.);f.vm.run('OnKeyDown',256);self.cycle(f)
        self.assertGreater(f.launches,before)
    def test_mode_key_control_deduplicate_and_clear_repeat(self):
        f=self.fixture();f.vm.run('OnKeyDown',42);f.vm.run('OnControlDown','Sprint')
        self.assertTrue(f.vm.state['ContinuousFire'])
        f.vm.run('OnKeyUp',42,.1);f.vm.run('OnControlUp','Sprint',.1)
        f.vm.run('OnKeyDown',256);f.vm.run('OnControlDown','Right Attack/Block')
        self.cycle(f);f.vm.run('OnKeyDown',42);before=f.launches;self.cycle(f);self.cycle(f)
        self.assertFalse(f.vm.state['ContinuousFire']);self.assertLessEqual(f.launches,before+1)
    def test_ammo_exhaustion_disarms_repeat(self):
        f=self.fixture();f.ammo=1;f.vm.state['ContinuousFire']=True;f.vm.run('OnKeyDown',256)
        self.cycle(f);self.cycle(f);self.assertEqual(f.launches,1);self.assertEqual(f.ammo,0)
        self.assertFalse(f.vm.state['repeatFire'])
    def test_exit_during_reload_cannot_repeat(self):
        f=self.fixture();f.vm.state['ContinuousFire']=True;f.vm.run('OnKeyDown',256)
        for _ in range(8):f.vm.now+=.05;f.vm.run('OnUpdate')
        f.vm.run('EndSession');before=f.launches;self.cycle(f)
        self.assertEqual(f.launches,before);self.assertEqual(f.lease.controls,[True]*8)

if __name__=='__main__':unittest.main()
