"""v29: the hold clip grips; the runtime only steers the mount and never gates on telemetry.

Source contracts for the decisions in docs/superpowers/specs/2026-10-11-guardias-v29-design.md.
They pin structure, not engine behaviour: grip, tracking and firing still need an in-game test.
"""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CPP = (ROOT/'native/src/GuardRuntime.cpp').read_text()


def body(signature):
    """Text of a top-level function, from its signature to the next top-level definition."""
    start = CPP.index(signature)
    following = re.search(r'\n(?:void|bool|int|GuardRuntime::Slot\*) GuardRuntime::', CPP[start+len(signature):])
    return CPP[start:start+len(signature)+(following.start() if following else len(CPP))]


class Guard29(unittest.TestCase):
    def test_tick_never_gates_aim_or_fire_on_grip_or_clip_samples(self):
        tick = body('void GuardRuntime::tick(float dt)')
        for gate in ('settleGrip(', 'guardGripFresh(', 'gripIK(', 'feetIK(', 'guardPoseFresh(',
                     'observationFresh(', 'guardStepPhase('):
            self.assertNotIn(gate, tick, gate)
        for cancel in ('hold replacement not observable', 'frame delta cannot preserve clip phase',
                       '"menu/pause"', 'turn playback timeout', 'body Fire'):
            self.assertNotIn(cancel, tick, cancel)
        self.assertNotIn('requestClip(s,actor.get(),s.stepDelta', tick)
        self.assertNotIn('requestClip(s,actor.get(),1)', tick)

    def test_tick_tracks_rate_limited_and_fires_from_policy(self):
        tick = body('void GuardRuntime::tick(float dt)')
        self.assertIn('guardTrackYaw(', tick)
        self.assertIn('guardShouldFire(', tick)
        self.assertIn('.hold.reissue(', tick)
        self.assertIn('.hold.entered(', tick)
        # Firing is decided only after the mount has been steered this frame.
        self.assertLess(tick.index('guardTrackYaw('), tick.index('guardShouldFire('))

    def test_paused_frames_skip_instead_of_cancelling(self):
        tick = body('void GuardRuntime::tick(float dt)')
        self.assertRegex(tick, r'if\(pause\)\s*\{?\s*continue;')
        menu = body('void GuardRuntime::menu(')
        self.assertIn('"Loading Menu"', menu)
        self.assertIn('invalidate()', menu)

    def test_blocked_moves_hold_the_previous_yaw(self):
        tick = body('void GuardRuntime::tick(float dt)')
        self.assertIn('Pose::blocked', tick)
        self.assertIn('Pose::invalid', tick)

    def test_shoot_keeps_safety_but_drops_body_clip_synchronisation(self):
        shoot = body('bool GuardRuntime::shoot(')
        for removed in ('fireObserved', 'guardGripFresh(', 'cycle.release(', 'lastScaledTime', 'stepPhase'):
            self.assertNotIn(removed, shoot, removed)
        # v29.2 supersedes the flat-shot pieces: enemy() takes `hunted`, the flat horizontalFlight gate became the
        # elevation solution (aimAt) and the player is protected unless they are the target (see test_guard_aim_contracts.py).
        for kept in ('enemy(target,guard,hunted)', 'guardProjectileContract(', 'guardPathSafe(', 'visible(target,guard,muzzle)',
                     'aimAt(gun,center)', 'protect.push_back(*playerBounds)', 'RE::Projectile::Launch('):
            self.assertIn(kept, shoot, kept)
        # The mechanism's own Fire sequence starts with the real launch, not before.
        self.assertLess(shoot.index('RE::Projectile::Launch('), shoot.index('GetSequence("Fire")'))

    def test_observation_is_telemetry_without_weight_filter(self):
        observe = body('void GuardRuntime::observe(')
        self.assertNotIn('weight<.99', observe)
        self.assertIn('guardClipKind(', observe)

    def test_pose_telemetry_measures_hands_without_correcting(self):
        self.assertIn('guard v29 pose', CPP)
        self.assertNotIn('rotateBone(', body('void GuardRuntime::tick(float dt)'))

    def test_version_is_363_everywhere(self):
        """Superseded 3.6.0/3.6.2 contracts: v29.2 (docs/superpowers/specs/2026-10-12-guardia-apuntado-disparo.md) is 3.6.3."""
        plugin = (ROOT/'native/src/Plugin.cpp').read_text()
        for value in ('v.PluginVersion({3,6,3,0})', 'info->version=0x03060030', 'AstraSight 3.6.3 API 4'):
            self.assertIn(value, plugin)
        self.assertIn('REL::Version{3,6,3,0}', CPP)
        self.assertIn('project(AstraSight VERSION 3.6.3', (ROOT/'native/CMakeLists.txt').read_text())
        self.assertIn('0x03060030', (ROOT/'native/verify_binary.py').read_text())
        self.assertIn('50724912', (ROOT/'scripts/build_native.py').read_text())

    def test_scene_assets_are_identical_to_v27(self):
        manifest = json.loads((ROOT/'dist/MANIFEST_v27.json').read_text())['files_sha256']
        folders = [ROOT/'mod', ROOT/'addons/WhiterunTorres', ROOT/'addons/Atalaya', ROOT/'addons/GuardAnim']
        checked = 0
        for name, digest in manifest.items():
            if not name.endswith(('.esp', '.nif', '.hkx', '.json', '.seq')):
                continue
            path = next(f/name for f in folders if (f/name).is_file())
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest, name)
            checked += 1
        self.assertGreaterEqual(checked, 30)


if __name__ == '__main__':
    unittest.main()
