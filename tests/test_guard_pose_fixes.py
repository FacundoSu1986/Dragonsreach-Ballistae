"""v29.1 source contracts: pose written on change, split idle re-request, unexpected-clip log.

They pin structure, not engine behaviour (GuardRuntime.cpp needs MSVC + CommonLibSSE-NG, so it is
not compiled in CI here). The pure policy behind them is covered by native/tests/guard_pose_tests.cpp.
Design and the log lines that confirm each hypothesis: docs/superpowers/specs/2026-10-12-guardia-pose-fixes.md.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CPP = (ROOT/'native/src/GuardRuntime.cpp').read_text()
HEADER = (ROOT/'native/include/Astra/GuardRuntime.h').read_text()
POLICY = (ROOT/'native/include/Astra/GuardPolicy.h').read_text()


def body(signature):
    """Text of a top-level GuardRuntime function, from its signature to the next top-level definition."""
    start = CPP.index(signature)
    following = re.search(r'\n(?:void|bool|int|GuardRuntime::Slot\*|GuardRuntime::Pose) GuardRuntime::', CPP[start+len(signature):])
    return CPP[start:start+len(signature)+(following.start() if following else len(CPP))]


def balanced_call(text, name):
    """The argument text of the first `name(...)` call, balancing parentheses."""
    start = text.index(name+'(')+len(name)+1
    depth, i = 1, start
    while depth:
        depth += {'(': 1, ')': -1}.get(text[i], 0)
        i += 1
    return text[start:i-1]


class PoseWrittenOnChange(unittest.TestCase):
    def test_pose_never_writes_the_transform_unconditionally(self):
        pose = body('GuardRuntime::Pose GuardRuntime::pose(')
        self.assertIn('guardPoseWrites(', pose)
        self.assertRegex(pose, r'if\(writes\.position\)\s*\{')
        self.assertRegex(pose, r'if\(writes\.rotation\)\s*\{')
        # Every SetPosition/SetRotation sits inside one of those two guards.
        guarded_position = pose[pose.index('if(writes.position)'):pose.index('if(writes.rotation)')]
        self.assertEqual(pose.count('actor->SetPosition(into(p),true)'), 1)
        self.assertIn('actor->SetPosition(into(p),true)', guarded_position)
        rotation = pose[pose.index('if(writes.rotation)'):]
        self.assertIn('SetRotationZ(', rotation)
        before_rotation = pose[:pose.index('if(writes.rotation)')]
        self.assertNotIn('SetRotationZ(', before_rotation)
        self.assertNotIn('SetRotationX(', before_rotation)

    def test_pose_keeps_its_safety_checks(self):
        pose = body('GuardRuntime::Pose GuardRuntime::pose(')
        for kept in ('actor/controller displacement mismatch', 'actor pose did not settle', 'capsule move exceeds bounded horizontal step',
                     'operator swept clearance obstructed / unknown', 'floor support unknown / self-hit / slope / height changed'):
            self.assertIn(kept, pose, kept)

    def test_write_counters_reach_the_log(self):
        self.assertIn('++s.writesPos', body('GuardRuntime::Pose GuardRuntime::pose('))
        self.assertIn('++s.writesRot', body('GuardRuntime::Pose GuardRuntime::pose('))
        pose_log = body('void GuardRuntime::poseLog(')
        for field in ('writesPos={}', 'writesRot={}', 'maxDrift={:.3f}', 'reissues={}', 'held={}'):
            self.assertIn(field, pose_log, field)
        self.assertIn('guard v29 pose', pose_log)  # the v29 prefix stays: scripts and the QA protocol grep for it


class IdleRequestIsSplit(unittest.TestCase):
    def test_first_request_plays_the_idle_without_forcing_default_in_the_same_frame(self):
        request = body('bool GuardRuntime::requestClip(')
        self.assertIn('bool again', request)
        first_request = request[request.index('return playHold(s,actor);')-60:]
        self.assertNotIn('NotifyAnimationGraph', first_request)
        # IdleForceDefaultState exists only on the re-request branch, which schedules the replay.
        branch = request[request.index('if(again){'):request.index('return playHold(s,actor);')]
        self.assertIn('NotifyAnimationGraph("IdleForceDefaultState")', branch)
        self.assertIn('replayAt=clock_+GuardReplayDelay', branch)
        self.assertNotIn('PlayIdle(', branch)

    def test_play_hold_is_the_only_place_that_plays_the_owned_idle(self):
        self.assertEqual(len(re.findall(r'PlayIdle\(actor,owned,nullptr\)', CPP)), 1)
        self.assertEqual(len(re.findall(r'PlayIdle\(actor,idle\(\),nullptr\)', CPP)), 0)
        self.assertIn('bool playHold(Slot&,RE::Actor*)', HEADER)
        self.assertIn('bool requestClip(Slot&,RE::Actor*,int,bool again=false)', HEADER)

    def test_tick_replays_after_the_delay_and_never_cancels_for_silence(self):
        tick = body('void GuardRuntime::tick(float dt)')
        self.assertIn('requestClip(s,actor.get(),0,true)', tick)
        self.assertRegex(tick, r's\.replayAt>=0&&clock_>=s\.replayAt')
        self.assertIn('playHold(s,actor.get())', tick)
        self.assertIn('s.hold.restart(clock_)', tick)
        self.assertLess(tick.index('playHold(s,actor.get())'), tick.index('requestClip(s,actor.get(),0,true)'))
        # Giving up is a warning, not a cancellation (v29 principle: telemetry never cancels).
        gave_up = tick[tick.index('if(s.hold.exhausted()'):]
        gave_up = gave_up[:gave_up.index('\n')]
        self.assertIn('guard v29.1 hold unresolved', gave_up)
        self.assertNotIn('cancel(', gave_up)

    def test_hands_on_the_grips_count_as_a_held_pose(self):
        tick = body('void GuardRuntime::tick(float dt)')
        self.assertIn('guardHandsHeld(s.handError[0],s.handError[1])', tick)
        self.assertLess(tick.index('guardHandsHeld('), tick.index('s.hold.reissue(clock_)'))

    def test_policy_exposes_the_new_constants(self):
        for name in ('GuardReplayDelay=.35', 'GuardMaxReissues=3', 'GuardHeldHandError=12.', 'GuardPoseEpsilonPosition=.05',
                     'GuardPoseEpsilonAngle=.001', 'guardPoseWrites(', 'guardHandsHeld('):
            self.assertIn(name, POLICY.replace(' ', ''), name)


class UnexpectedClipsAreReported(unittest.TestCase):
    def test_observe_names_clips_that_are_not_ours(self):
        observe = body('void GuardRuntime::observe(')
        branch = observe[observe.index('if(kind<0){'):observe.index('std::lock_guard lock(observationsMutex_);auto& o=observations_[index];')]
        self.assertIn('guard v29.1 unexpected clip', branch)
        for field in ('animationPath', 'projectName', 'modName', 'subModName', 'variantFilename'):
            self.assertIn('info.'+field+'.c_str()', branch, field)
        self.assertIn('return;', branch)
        self.assertIn('std::chrono::seconds(10)', branch)   # rate limit: the hook runs every frame

    def test_observe_only_takes_the_observation_mutex_and_never_the_slot_mutex(self):
        observe = body('void GuardRuntime::observe(')
        self.assertNotIn('mutex_);', observe.replace('observationsMutex_);', ''))
        self.assertIn('loggedClips_', HEADER)

    def test_oar_state_is_still_read_telemetry_only(self):
        observe = body('void GuardRuntime::observe(')
        self.assertNotIn('weight<.99', observe)
        self.assertIn('guardClipKind(', observe)


if __name__ == '__main__':
    unittest.main()
