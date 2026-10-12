"""v29.2 source contracts: elevation, ballistic aim, hunted player as a target, shot-refusal log.

They pin structure, not engine behaviour (GuardRuntime.cpp needs MSVC + CommonLibSSE-NG, so it is
not compiled here). The pure policy is covered by native/tests/guard_aim_tests.cpp.
Design: docs/superpowers/specs/2026-10-12-guardia-apuntado-disparo.md.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CPP = (ROOT/'native/src/GuardRuntime.cpp').read_text()
HEADER = (ROOT/'native/include/Astra/GuardRuntime.h').read_text()
POLICY = (ROOT/'native/include/Astra/GuardPolicy.h').read_text()
CMAKE = (ROOT/'native/CMakeLists.txt').read_text()


def body(signature):
    start = CPP.index(signature)
    following = re.search(r'\n(?:void|bool|int|GuardRuntime::Slot\*|GuardRuntime::Pose) GuardRuntime::', CPP[start+len(signature):])
    return CPP[start:start+len(signature)+(following.start() if following else len(CPP))]


class Elevation(unittest.TestCase):
    def test_pose_drives_the_elevation_node_like_the_player_sight(self):
        pose = body('GuardRuntime::Pose GuardRuntime::pose(')
        # Plugin.cpp (player sight): pitch->local.rotate = rx(-rad(pitch)) * pitchBase.
        self.assertIn('pitch->local.rotate=into(rx(-rad(pitchValue))*s.pitchBase)', pose)
        self.assertNotIn('pitch->local.rotate=into(s.pitchBase)', pose)
        self.assertIn('s.pitch=pitchValue', pose)
        self.assertIn('GuardPitchMin', pose)

    def test_tick_tracks_pitch_and_poses_with_it(self):
        tick = body('void GuardRuntime::tick(float dt)')
        self.assertIn('guardTrackPitch(s.pitch,desiredPitch,step)', tick)
        self.assertIn('pose(s,gun.get(),actor.get(),*next,*nextPitch)', tick)
        self.assertIn('pose(s,gun.get(),actor.get(),s.yaw,s.pitch)', tick)
        self.assertIn('aimAt(gun.get(),center)', tick)
        # A passer-by is followed along the line of sight; only an enemy gets the ballistic elevation.
        self.assertRegex(tick, r'if\(aim&&enemy\(target,actor\.get\(\),s\.hunted\)\)desiredPitch=aim->pitch;else desiredPitch=aimFromWorld')

    def test_fire_needs_the_elevation_to_have_been_reached(self):
        tick = body('void GuardRuntime::tick(float dt)')
        self.assertIn('std::abs(desiredPitch-s.pitch)<=GuardAimTolerance', tick)
        self.assertNotIn('horizontalFlight', tick)

    def test_cleanup_still_restores_the_authored_pitch(self):
        self.assertIn('pitch->local.rotate=into(s.pitchBase)', body('void GuardRuntime::cleanup('))

    def test_the_flat_shot_contract_is_gone_from_shoot(self):
        shoot = body('bool GuardRuntime::shoot(')
        self.assertNotIn('std::abs(bore.z)>.001', shoot)
        self.assertNotIn('horizontalFlight', shoot)
        self.assertNotIn('guardTrajectory(', shoot)
        self.assertIn('guardArcTrajectory(muzzle,bore,seconds,5400,240.345)', shoot)
        self.assertIn('GuardBoreTolerance', shoot)
        self.assertIn('data.linearVelocity=into(bore*5400)', shoot)


class HuntedPlayer(unittest.TestCase):
    def test_enemy_only_admits_the_player_while_hunted(self):
        enemy = CPP[CPP.index('bool enemy(RE::Actor* a,RE::Actor* guard,bool hunted=false)'):]
        enemy = enemy[:enemy.index('\n}')]
        self.assertIn('GuardAllowPlayerTarget&&hunted&&a->IsInCombat()', enemy)
        self.assertRegex(enemy, r'a==RE::PlayerCharacter::GetSingleton\(\)\)return GuardAllowPlayerTarget')

    def test_player_hunted_looks_at_town_guards_not_at_the_operator(self):
        hunted = CPP[CPP.index('bool playerHunted('):]
        hunted = hunted[:hunted.index('\n}')]
        self.assertIn('0x28172', hunted)
        self.assertIn('0x2BE39', hunted)
        self.assertIn('a==operatorGuard', hunted)          # the isolated operator never reports combat
        self.assertIn('a->IsHostileToActor(player)', hunted)
        self.assertIn('GuardAllowPlayerTarget', hunted)    # one switch turns the feature off

    def test_shoot_does_not_protect_the_player_it_is_aiming_at(self):
        shoot = body('bool GuardRuntime::shoot(')
        self.assertIn('if(!targetIsPlayer)protect.push_back(*playerBounds);', shoot)
        self.assertEqual(shoot.count('protect.push_back(*playerBounds)'), 1)
        self.assertIn('protect.push_back(*guardBounds)', shoot)
        # ...and every enemy() check inside shoot() carries the freshly computed `hunted`.
        self.assertNotIn('enemy(target,guard)', shoot)
        self.assertIn('bool hunted=targetIsPlayer&&playerHunted(guard)', shoot)

    def test_targets_marks_the_player_candidate(self):
        targets = body('void GuardRuntime::targets(')
        self.assertIn('playerHunted(guard)', targets)
        self.assertIn('isPlayer?hunted:', targets)
        self.assertIn('hunted,hunted,true,false,bounds->height*.5,false,hunted', targets)
        self.assertIn('from(muzzle->world.translate),true)', targets)   # ballistic reach for far enemies
        self.assertIn('guard v29.2 player-hostile', targets)


class Diagnostics(unittest.TestCase):
    def test_every_return_false_in_shoot_names_its_reason(self):
        shoot = body('bool GuardRuntime::shoot(')
        silent = re.findall(r'return false;', shoot)
        # Two remain: the refuse() lambda itself, and the launch that returned no projectile (cancel() names it).
        self.assertEqual(len(silent), 2, silent)
        self.assertIn('auto refuse=[&](const char* reason){s.shotRefusal=reason;return false;}', shoot)
        self.assertGreaterEqual(shoot.count('refuse("'), 18)

    def test_refusals_are_logged_and_rate_limited(self):
        tick = body('void GuardRuntime::tick(float dt)')
        self.assertIn('guard v29.2 shot refused', tick)
        self.assertIn('s.nextRefusalLog=clock_+5', tick)

    def test_pose_log_keeps_its_prefix_and_adds_the_elevation(self):
        log = body('void GuardRuntime::poseLog(')
        self.assertIn('guard v29 pose gun=', log)
        for key in ('pitch={:.2f}', 'desiredPitch={:.2f}', 'hunted={}', 'writesPos={}'):
            self.assertIn(key, log)

    def test_spdlog_placeholders_match_arguments(self):
        bad = []
        for m in re.finditer(r'spdlog::(?:info|warn)\(', CPP):
            i = m.end()
            self.assertEqual(CPP[i], '"')
            j = i+1
            while CPP[j] != '"':
                j += 2 if CPP[j] == '\\' else 1
            fmt = CPP[i+1:j]
            depth, k, args = 1, j+1, 0
            while depth:
                ch = CPP[k]
                if ch in '([{':
                    depth += 1
                elif ch in ')]}':
                    depth -= 1
                elif ch == ',' and depth == 1:
                    args += 1
                elif ch == '"':
                    k += 1
                    while CPP[k] != '"':
                        k += 2 if CPP[k] == '\\' else 1
                k += 1
            if len(re.findall(r'\{[^{}]*\}', fmt.replace('{{', '').replace('}}', ''))) != args:
                bad.append(fmt[:50])
        self.assertEqual(bad, [])


class PolicyAndBuild(unittest.TestCase):
    def test_policy_exports_exist_and_the_player_switch_defaults_on(self):
        for name in ('guardAimSolution', 'guardTrackPitch', 'guardBore', 'guardArcTrajectory', 'guardEnemy'):
            self.assertIn(name, POLICY)
        self.assertIn('inline constexpr bool GuardAllowPlayerTarget=true', POLICY)
        self.assertIn('GuardPitchMin=-30.', POLICY)
        self.assertIn('GuardPitchMax=30.', POLICY)

    def test_slot_carries_the_new_state(self):
        for field in ('double pitch{}', 'bool hunted{}', 'shotRefusal{'):
            self.assertIn(field, HEADER)
        self.assertIn('const Observation&,double,double);', HEADER)

    def test_aim_tests_are_registered(self):
        self.assertIn('add_test(NAME AstraGuardAimTests COMMAND AstraGuardAimTests)', CMAKE)


if __name__ == '__main__':
    unittest.main()
