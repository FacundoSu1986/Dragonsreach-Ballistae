"""scripts/analyze_guard_log.py on synthetic AstraSight.log text (formats copied from GuardRuntime.cpp)."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('analyze_guard_log', ROOT/'scripts/analyze_guard_log.py')
analyzer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyzer)

STAMP = '[2026-10-12 20:00:00.000] [AstraSight] '
BANNER = STAMP+'[info] AstraSight 3.6.3 API 4 runtime 1.6.1170, native input/launch, release 66.7ms, cycle 1s, per-session sectors; v29.1 guards'
OAR_OK = STAMP+'[info] AstraGuardNative API1 frame pump PlayerCharacter::Update (0xAD); v29 hold clip grips, mount steered rigidly, OAR samples are telemetry only; OAR Animations V1=True (module loaded=True)'
ACQUIRED = STAMP+'[info] guard v26 acquired gun=14000B70 actor=14000B71 package=14000B90 yaw=-0 heightOffset=0.0 supportZ=-3544.0 actorScale=1.03 referenceScale=1 baseHeight=1.03 holdRequested=true'
PLAY = STAMP+'[info] guard v29.1 PlayIdle gun=14000B70 actor=14000B71 accepted=true'
HOLDING = STAMP+'[info] guard v29 holding gun=14000B70 actor=14000B71 yaw=0.00'


def pose(left, right, target='00000000', writes=(0, 0), drift='0.000', status=1, refused='none', pitch=0.0, wanted=0.0):
    return (STAMP+f'[info] guard v29 pose gun=14000B70 actor=14000B71 status={status} yaw=0.00 desired=0.00 target={target} clip=0 phase=0.500 '
            f'sampleAge=0.02 handErrorL={left} handErrorR={right} moveRefused={refused} characterMain=120 characterWorker=0 '
            f'writesPos={writes[0]} writesRot={writes[1]} maxDrift={drift} reissues=0 held=true pitch={pitch:.2f} desiredPitch={wanted:.2f} hunted=false')


def keys(report):
    return {key for key, _ in report['verdicts']}


class Analyzer(unittest.TestCase):
    def test_healthy_hold(self):
        log = '\n'.join([BANNER, OAR_OK, ACQUIRED, PLAY, HOLDING]+[pose(3.1, 3.4) for _ in range(5)])
        report = analyzer.analyze(log)
        self.assertEqual(report['acquired'], 1)
        self.assertIn('H1-OK', keys(report))
        self.assertIn('LOOKS-HEALTHY', keys(report))
        self.assertNotIn('H3-HANDS-FAR', keys(report))

    def test_wrists_far_from_the_grips(self):
        log = '\n'.join([BANNER, OAR_OK, ACQUIRED, PLAY, HOLDING]+[pose(31.0, 29.5) for _ in range(5)])
        self.assertIn('H3-HANDS-FAR', keys(analyzer.analyze(log)))

    def test_hand_nodes_not_measured(self):
        log = '\n'.join([BANNER, OAR_OK, ACQUIRED, HOLDING]+[pose(-1.0, -1.0) for _ in range(3)])
        self.assertIn('H3-NOT-MEASURED', keys(analyzer.analyze(log)))

    def test_per_frame_writes_are_flagged(self):
        log = '\n'.join([BANNER, OAR_OK, ACQUIRED, HOLDING]+[pose(3, 3, writes=(118, 118)) for _ in range(4)])
        self.assertIn('H1-WRITING-EVERY-FRAME', keys(analyzer.analyze(log)))

    def test_a_target_may_write_every_frame(self):
        log = '\n'.join([BANNER, OAR_OK, ACQUIRED, HOLDING]+[pose(3, 3, target='00000014', writes=(118, 118)) for _ in range(4)])
        self.assertNotIn('H1-WRITING-EVERY-FRAME', keys(analyzer.analyze(log)))

    def test_re_request_cycle_and_foreign_clip(self):
        rerequest = STAMP+'[info] guard v29 hold re-request gun=14000B70 actor=14000B71: no own clip sample and wrists not on the grips for 3 s (try 1/3)'
        foreign = STAMP+"[info] guard v29.1 unexpected clip slot=0 animation='Meshes/actors/character/animations/OpenAnimationReplacer/Other/Idle/IdleHandsBehindBack.hkx' project='DefaultMale' mod='Other Idles' submod='Guards' variant=''"
        vanilla = STAMP+"[info] guard v29.1 unexpected clip slot=0 animation='' project='' mod='' submod='' variant=''"
        unresolved = STAMP+'[warning] guard v29.1 hold unresolved gun=14000B70 actor=14000B71 reissues=3 handErrorL=30.0 handErrorR=29.0: keeping the pose, no more re-requests'
        report = analyzer.analyze('\n'.join([BANNER, OAR_OK, ACQUIRED, HOLDING, pose(30, 29), rerequest, rerequest, foreign, vanilla, unresolved]))
        found = keys(report)
        self.assertIn('H2-RE-REQUEST-CYCLE', found)
        self.assertIn('H4-OTHER-CLIP', found)
        text = analyzer.render(report)
        self.assertIn('Other Idles', text)
        self.assertIn('vanilla clip', text)

    def test_playidle_rejected(self):
        rejected = STAMP+'[info] guard v29.1 PlayIdle gun=14000B70 actor=14000B71 accepted=false'
        self.assertIn('PLAYIDLE-REJECTED', keys(analyzer.analyze('\n'.join([BANNER, OAR_OK, ACQUIRED, rejected, pose(3, 3)]))))

    def test_never_acquired_names_the_clause(self):
        reject = STAMP+'[warning] guard v26 reject gun=14000B70 actor=14000B71 token=3 clause=floor support unknown / self-hit / slope / height changed actorXYZ=(1.000,2.000,3.000) gunXYZ=(1.000,2.000,3.000) actorScale=1.03'
        report = analyzer.analyze('\n'.join([BANNER, OAR_OK, reject, reject]))
        self.assertEqual(keys(report), {'NEVER-ACQUIRED'})
        self.assertIn('floor support unknown', analyzer.render(report))

    def test_acquired_but_no_pose_lines_reports_the_cancel_reason(self):
        cancel = STAMP+'[info] guard cancel gun=14000B70 token=3 epoch=1 fault=true reason=operator cannot be held on the mount'
        report = analyzer.analyze('\n'.join([BANNER, OAR_OK, ACQUIRED, cancel]))
        self.assertIn('NO-POSE-LOG', keys(report))
        self.assertIn('operator cannot be held on the mount', analyzer.render(report))

    def test_wrong_dll_and_missing_oar(self):
        old = BANNER.replace('3.6.3', '3.6.0')
        no_oar = OAR_OK.replace('V1=True (module loaded=True)', 'V1=False (module loaded=False)')
        report = analyzer.analyze('\n'.join([old, no_oar, ACQUIRED, pose(3, 3)]))
        self.assertIn('DLL', keys(report))
        self.assertIn('OAR', keys(report))
        self.assertEqual(analyzer.analyze('\n'.join([old, OAR_OK]), expect='3.6.0')['version'], '3.6.0')

    def test_v292_pitch_following_refusals_hunted_player_and_launch(self):
        launch = STAMP+'[info] guard real projectile gun=14000B70 guard=14000B71 target=00000014 token=3 epoch=1 handle=5 yaw=10.00 pitch=-12.00 solvedPitch=-12.10 speed=5400 velocityZ={vz} expectedZ={ez} blast=0 player={pl}'
        refused = STAMP+'[info] guard v29.2 shot refused gun=14000B70 target=00000014 yaw=1.00 pitch=0.00 desiredPitch=-12.00 reason=path blocked before the target'
        hunted = STAMP+'[info] guard v29.2 player-hostile gun=14000B70 hunted=true'
        tracking = [pose(3, 3, target='00000014', pitch=-11.9, wanted=-12.0) for _ in range(4)]
        report = analyzer.analyze('\n'.join([BANNER, OAR_OK, ACQUIRED, HOLDING]+tracking+[hunted, refused, refused,
                                            launch.format(vz='-1122', ez='-1122', pl='true')]))
        found = keys(report)
        self.assertIn('PITCH-OK', found)
        self.assertIn('SHOT-REFUSED', found)
        self.assertIn('PLAYER-HUNTED', found)
        self.assertNotIn('LAUNCH-VELOCITY-MISMATCH', found)
        text = analyzer.render(report)
        self.assertIn('path blocked before the target x2', text)
        self.assertIn('1 at the player', text)
        stuck = [pose(3, 3, target='00000014', pitch=0.0, wanted=-25.0) for _ in range(4)]
        flat = analyzer.analyze('\n'.join([BANNER, OAR_OK, ACQUIRED, HOLDING]+stuck+[launch.format(vz='0', ez='-1122', pl='false')]))
        self.assertIn('PITCH-NOT-TRACKING', keys(flat))
        self.assertIn('LAUNCH-VELOCITY-MISMATCH', keys(flat))

    def test_v291_logs_without_the_new_fields_still_parse(self):
        old = STAMP+'[info] guard v29 pose gun=14000B70 actor=14000B71 status=1 yaw=0.00 desired=0.00 target=00000014 clip=0 phase=0.500 sampleAge=0.02 handErrorL=3 handErrorR=3 moveRefused=none characterMain=1 characterWorker=0 writesPos=0 writesRot=0 maxDrift=0.000 reissues=0 held=true'
        report = analyzer.analyze('\n'.join([BANNER, OAR_OK, ACQUIRED, HOLDING, old]))
        self.assertNotIn('PITCH-OK', keys(report))
        self.assertNotIn('PITCH-NOT-TRACKING', keys(report))

    def test_empty_or_foreign_text(self):
        self.assertEqual(keys(analyzer.analyze('')), {'NO-DATA'})
        self.assertEqual(keys(analyzer.analyze('some other log\nline two')), {'NO-DATA'})

    def test_real_v26_lines_from_the_repo_evidence(self):
        """Lines copied by the project from a real 2026-10-11 session (reports/diagnosis_v26_context.json)."""
        import json
        evidence = json.loads((ROOT/'reports/diagnosis_v26_context.json').read_text())
        lines = [evidence['dll_line'].join([STAMP+'[info] ', ''])]+evidence['first_acquisition']+evidence['first_context_clause']+evidence['first_cancel']
        report = analyzer.analyze('\n'.join(lines), expect='3.5.7')
        self.assertEqual(report['version'], '3.5.7')
        self.assertEqual(report['acquired'], 2)
        self.assertEqual(sum(report['cancels'].values()), 2)
        self.assertIn('running package has no owned idle override', report['rejects'])
        self.assertIn('NO-POSE-LOG', keys(report))

    def test_main_reports_unreadable_files(self):
        self.assertEqual(analyzer.main(['/nonexistent/AstraSight.log']), 2)


if __name__ == '__main__':
    unittest.main()
