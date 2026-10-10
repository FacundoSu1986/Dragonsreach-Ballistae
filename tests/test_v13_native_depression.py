"""Player controller bounds and version gate, evaluated from the actual PSC source."""
import unittest
from tests.test_camera_aim import AimFixture
from tests.test_native_sight import NativeSightFixture


class NativeDepressionV13(unittest.TestCase):
    def test_player_default_admits_minus_twenty(self):
        f = AimFixture()
        self.assertEqual(f.vm.state['PitchMin'], -20.0)
        self.assertEqual(f.vm.state['PitchMax'], 80.0)

    def test_native_snapshot_at_minus_twenty_is_accepted(self):
        f = NativeSightFixture()
        f.version = 0x03040000
        f.pose = [37.0, -20.0]
        f.enter()
        f.vm.run('OnUpdate')
        self.assertTrue(f.vm.state['operating'])
        self.assertEqual(f.vm.state['pitch'], -20.0)

    def test_v10_dll_is_rejected_before_api_or_controls(self):
        f = NativeSightFixture()
        f.version = 0x03030000
        f.enter()
        self.assertFalse(f.vm.state['operating'])
        self.assertEqual(f.lease.calls, [])
        self.assertFalse(any(call[0] in ('available', 'begin') for call in f.calls))
        self.assertTrue(any(call[0] == 'reject' and '3.4.0' in call[1] for call in f.calls))


if __name__ == '__main__':
    unittest.main()
