"""Exercise actual PSC branches with native boundary fixtures; not the engine.

Weapon.Fire from an object reference plays no attack sound, so the controller
plays one SOUN per launched bolt, after the launch, and never for a refused shot.
"""
import unittest
from pathlib import Path
from types import SimpleNamespace
from tests.test_native_sight import NativeSightFixture

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'mod/scripts/source/AstraAsedioActi.psc'


class ShotSound(unittest.TestCase):
    def fixture(self):
        f = NativeSightFixture(); f.active()
        f.vm.state['AstraSightNative'].ValidateShot = lambda *args: True
        f.vm.native.pop('RejectShot')
        f.vm.state.update(fireMouse=256, activateKeyboard=18, modeKeyboard=42, modeMouse=-1)
        f.played = []
        f.vm.state['ShotSound'] = SimpleNamespace(Play=lambda ref: (f.played.append((f.launches, ref)), 7)[1])
        return f

    def cycle(self, f):
        for _ in range(45):
            f.vm.now += .05; f.vm.run('OnUpdate')

    def test_one_cue_per_launched_bolt_after_the_launch(self):
        f = self.fixture(); f.vm.run('OnKeyDown', 256); self.cycle(f)
        self.assertEqual(f.launches, 1)
        self.assertEqual(f.played, [(1, f.vm.state['Self'])])

    def test_continuous_fire_plays_one_cue_per_cycle(self):
        f = self.fixture(); f.vm.state['ContinuousFire'] = True; f.vm.run('OnKeyDown', 256)
        self.cycle(f); self.cycle(f)
        self.assertGreaterEqual(f.launches, 2)
        self.assertEqual([launch for launch, ref in f.played], list(range(1, f.launches + 1)))

    def test_refused_shot_without_ammo_is_silent(self):
        f = self.fixture(); f.ammo = 0; f.vm.run('OnKeyDown', 256); self.cycle(f)
        self.assertEqual(f.launches, 0); self.assertEqual(f.played, [])

    def test_shot_cancelled_by_a_menu_before_commit_is_silent(self):
        f = self.fixture(); f.hooks['freeze_after'] = f.open_menu
        f.vm.run('OnKeyDown', 256); self.cycle(f)
        self.assertEqual(f.launches, 0); self.assertEqual(f.played, [])

    def test_missing_sound_property_never_blocks_the_shot(self):
        f = self.fixture(); f.vm.state['ShotSound'] = None
        f.vm.run('OnKeyDown', 256); self.cycle(f)
        self.assertEqual(f.launches, 1)

    def test_source_plays_once_in_commit_after_fire(self):
        source = SOURCE.read_text()
        self.assertIn('Sound Property ShotSound Auto', source)
        self.assertEqual(source.count('ShotSound.Play(Self)'), 1)
        commit = source.split('Function CommitShot(')[1].split('EndFunction')[0]
        self.assertLess(commit.index('Launcher.Fire(Self, ShotAmmo)'), commit.index('ShotSound.Play(Self)'))
        self.assertLess(commit.index('shotCommitted = true'), commit.index('ShotSound.Play(Self)'))
        # Review finding: the native Play must not delay the thaw or the visual-bolt hide.
        self.assertLess(commit.index('ThawSight(expectedGeneration, committedToken)'), commit.index('ShotSound.Play(Self)'))
        self.assertLess(commit.index('NetImmerse.SetNodeScale(Self, VisualBoltNode, 0.0, false)'), commit.index('ShotSound.Play(Self)'))


if __name__ == '__main__':
    unittest.main()
