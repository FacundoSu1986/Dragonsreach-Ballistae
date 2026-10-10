"""Sight zero: native constants re-derived from config, final NIF and final ESP.

The camera node stays parallel to the bore in the NIF (the native direction
checks need that). Since v10 the camera uses Astra::sightPose (tests/test_v10_sight.py); the v08
constants and sightZeroRadians/sightCameraRotation are legacy, kept as the record of the v08 zero and
not on the camera path. These are source and data contracts: no hook, camera or projectile runs here.
"""
import json, math, re, struct, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts')); sys.path.insert(0, str(ROOT/'scripts/vendor'))
import nif_nodos
from parser_esm import Plugin

G = 9.81  # m/s^2: the drop model scales Havok gravity by the PROJ gravity multiplier


def native_constants():
    source = (ROOT/'native/src/Core.cpp').read_text()
    match = re.search(r'constexpr double kSightParallax=([\d.]+),kSightZeroDrop=([\d.]+),kSightZeroRange=([\d.]+);', source)
    return [float(v) for v in match.groups()] if match else None


def nodes():
    return {n['nombre']: n for n in nif_nodos.leer(str(ROOT/'mod/meshes/AstraAsedio/ballesta.nif'))['nodos'].values()}


def derived():
    cfg = json.loads((ROOT/'config.json').read_text())
    camera, muzzle = nodes()['AstraSightCameraNode']['tr'], nodes()['ProjectileNode']['tr']
    plugin = Plugin(ROOT/'mod/AstraAsedio.esp')
    proj = next(dict(plugin.subrecords(plugin.datos(o)))['DATA'] for t, o, n, d in plugin.recorrer() if t == 'PROJ')
    gravity, speed = struct.unpack_from('<ff', proj, 4)
    zero = cfg['sight_zero_meters'] * cfg['meters_to_units']
    drop = .5 * gravity * G * cfg['meters_to_units'] * (zero / speed) ** 2
    return camera[2] - muzzle[2], drop, zero + camera[1] - muzzle[1]


class SightZero(unittest.TestCase):
    def test_native_constants_match_config_nif_and_esp(self):
        constants = native_constants()
        self.assertIsNotNone(constants, 'sight zero constants missing from Core.cpp')
        for name, value, expected in zip(('parallax', 'drop', 'range'), constants, derived()):
            with self.subTest(name=name):
                self.assertAlmostEqual(value, expected, delta=max(1e-3, abs(expected) * 1e-5))

    def test_flat_zero_is_about_1_38_degrees(self):
        parallax, drop, distance = derived()
        self.assertAlmostEqual(math.degrees(math.atan((parallax + drop) / distance)), 1.382, places=3)

    def test_nif_camera_stays_parallel_to_the_bore(self):
        n = nodes()
        cfg = json.loads((ROOT/'config.json').read_text())
        for a, b in zip(n['AstraSightCameraNode']['tr'], cfg['camera_local_units']):
            self.assertAlmostEqual(a, b, places=3)
        for a, b in zip(n['AstraSightCameraNode']['rot'], n['ProjectileNode']['rot']):
            self.assertAlmostEqual(a, b, places=6)

    def test_plugin_views_along_sight_pose_and_keeps_direction_checks(self):
        # v10: the closed-form v08 tilt is superseded by sightPose (tests/test_v10_sight.py): the camera
        # looks along the line rear sight -> zero target, the same 75 m zero in general form.
        source = (ROOT/'native/src/Plugin.cpp').read_text()
        self.assertIn('Transform worldCamera{pose.rotation()*binding.adapter,pose.camera,1};', source)
        self.assertNotIn('anchor.rotation*binding.adapter', source)
        self.assertNotIn('sightCameraRotation(', source)
        self.assertNotIn('sightZeroRadians(', source)
        self.assertIn('length(anchorForward-expected)>0.02||length(anchorForward-projectile.rotation*Vec{0,1,0})>0.02', source)
        # Player look is still reconciled to the bore, not to the tilted view.
        self.assertIn('player->SetRotationX(float(-std::asin(std::clamp(expected.z,-1.,1.))));', source)
        self.assertIn('v.PluginVersion({3,4,0,0})', source)
        self.assertIn('info->version=0x03040000', source)

    def test_controller_refuses_the_v07_dll_before_any_native_call(self):
        from tests.test_native_sight import NativeSightFixture
        f = NativeSightFixture(); f.version = 0x03000000; f.enter()
        self.assertFalse(f.vm.state['operating'])
        self.assertFalse(any(call[0] == 'begin' for call in f.calls))
        self.assertEqual(f.lease.controls, [True] * 8)


if __name__ == '__main__':
    unittest.main()
