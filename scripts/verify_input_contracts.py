"""Run the current PSC boundary contracts; this does not execute the game VM."""
from pathlib import Path
import hashlib, io, json, sys, unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run_contract(module_name, report_name, source_name, source_key, dependencies=()):
    test_path = ROOT / (module_name.replace('.', '/') + '.py')
    source_path = ROOT / 'mod/scripts/source' / source_name
    test_hash, source_hash = sha(test_path), sha(source_path)
    dependency_hashes = {str(p.relative_to(ROOT)): sha(p) for p in dependencies}
    suite = unittest.defaultTestLoader.loadTestsFromName(module_name)
    output = io.StringIO()
    result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
    unchanged = (test_hash, source_hash) == (sha(test_path), sha(source_path)) and all(sha(ROOT/p) == value for p,value in dependency_hashes.items())
    report = {
        'success': result.wasSuccessful() and unchanged,
        'test_count': result.testsRun,
        'command': [sys.executable, '-m', 'unittest', module_name],
        'output': output.getvalue(),
        'test_source_sha256': test_hash,
        source_key: source_hash,
        'sources_unchanged_during_verification': unchanged,
        'runtime_execution': False,
        'dependency_sha256': dependency_hashes,
        'interpretation': 'Actual scalar PSC branches with explicit native fixtures; no Papyrus VM or SKSE event dispatch execution.',
    }
    (ROOT / 'reports' / report_name).write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(output.getvalue())
    if not report['success']:
        raise RuntimeError('Contract failed: ' + module_name)
    return result.testsRun

def repair_encoding(value):
    if isinstance(value, dict):
        return {k: repair_encoding(v) for k, v in value.items()}
    if isinstance(value, list):
        return [repair_encoding(v) for v in value]
    if isinstance(value, str):
        try:
            return value.encode('latin1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
    return value

def main():
    count = run_contract('tests.test_session_contract', 'input_behavior.json', 'AstraAsedioActi.psc', 'controller_source_sha256')
    lease_count = run_contract('tests.test_control_lease', 'control_lease_behavior.json', 'AstraAsedioSession.psc', 'session_source_sha256')
    camera_count = run_contract('tests.test_camera_aim', 'camera_aim_behavior.json', 'AstraAsedioActi.psc', 'controller_source_sha256')
    camera_path=ROOT/'reports/camera_aim_behavior.json'
    camera=json.loads(camera_path.read_text())
    camera['session_source_sha256']=sha(ROOT/'mod/scripts/source/AstraAsedioSession.psc')
    camera_path.write_text(json.dumps(camera,indent=2),encoding='utf-8')
    native_count = run_contract('tests.test_native_sight', 'native_sight_behavior.json', 'AstraAsedioActi.psc', 'controller_source_sha256', (
        ROOT/'mod/scripts/source/AstraAsedioSession.psc',
        ROOT/'mod/scripts/source/AstraSightNative.psc',
        ROOT/'tests/test_camera_aim.py', ROOT/'tests/test_session_contract.py', ROOT/'tests/test_control_lease.py',
        ROOT/'scripts/build_plugin.py', ROOT/'config.json', ROOT/'mod/AstraAsedio.esp',
    ))
    native_path = ROOT/'reports/native_sight_behavior.json'
    native = json.loads(native_path.read_text())
    native.update({
        'session_source_sha256': sha(ROOT/'mod/scripts/source/AstraAsedioSession.psc'),
        'native_api_source_sha256': sha(ROOT/'mod/scripts/source/AstraSightNative.psc'),
        'fixture_limits': [
            'Executes actual PSC scalar branches, array length/range checks and arithmetic with explicit native boundary fixtures.',
            'Does not execute the Papyrus VM, DLL, scene graph, real input dispatch, frame scheduling or save serialization.',
            'Native pose fixture represents last applied scene pose; native serialization/token isolation requires separate C++ evidence and game verification.',
        ],
    })
    native_path.write_text(json.dumps(native,indent=2),encoding='utf-8')
    runtime_count = run_contract('tests.test_v06_runtime_bindings', 'runtime_bindings_behavior.json', 'AstraAsedioActi.psc', 'controller_source_sha256', (
        ROOT/'mod/scripts/source/AstraAsedioSession.psc', ROOT/'mod/scripts/source/AstraSightNative.psc',
        ROOT/'native/src/Plugin.cpp', ROOT/'scripts/compile_papyrus.py',
        ROOT/'tests/test_native_sight.py', ROOT/'tests/test_camera_aim.py', ROOT/'tests/test_control_lease.py',
    ))
    run_contract('tests.test_v07_firing', 'v07_firing_behavior.json', 'AstraAsedioActi.psc', 'controller_source_sha256', (
        ROOT/'tests/test_native_sight.py', ROOT/'tests/test_control_lease.py',ROOT/'tests/test_camera_aim.py',
        ROOT/'mod/scripts/source/AstraSightNative.psc', ROOT/'native/src/Plugin.cpp', ROOT/'config.json',
    ))
    run_contract('tests.test_v07_camera_contract', 'v07_camera_wiring_behavior.json', 'AstraAsedioActi.psc', 'controller_source_sha256', (
        ROOT/'native/src/Plugin.cpp', ROOT/'scripts/retime_v07.py',ROOT/'scripts/build_plugin.py',ROOT/'config.json',ROOT/'mod/AstraAsedio.esp',
    ))
    run_contract('tests.test_v08_shot_sound', 'v08_shot_sound_behavior.json', 'AstraAsedioActi.psc', 'controller_source_sha256', (
        ROOT/'tests/test_native_sight.py', ROOT/'scripts/build_plugin.py', ROOT/'mod/AstraAsedio.esp',
    ))
    run_contract('tests.test_v08_sight_zero', 'v08_sight_zero_behavior.json', 'AstraAsedioActi.psc', 'controller_source_sha256', (
        ROOT/'native/src/Core.cpp', ROOT/'native/src/Plugin.cpp', ROOT/'config.json',
        ROOT/'mod/meshes/AstraAsedio/ballesta.nif', ROOT/'mod/AstraAsedio.esp', ROOT/'tests/test_native_sight.py',
    ))
    # v09: the v08 in-game findings (reports/user_evidence_v08.json) on the actual PSC.
    run_contract('tests.test_v09_input_fixes', 'v09_input_fixes_behavior.json', 'AstraAsedioActi.psc', 'controller_source_sha256', (
        ROOT/'tests/test_native_sight.py', ROOT/'tests/test_camera_aim.py', ROOT/'tests/test_control_lease.py',
        ROOT/'mod/scripts/source/AstraSightNative.psc', ROOT/'reports/user_evidence_v08.json',
    ))
    # v10: tail sight constants, pose and native contract (reports/user_evidence_v09.json).
    run_contract('tests.test_v10_sight', 'v10_sight_behavior.json', 'AstraAsedioActi.psc', 'controller_source_sha256', (
        ROOT/'scripts/sight_pose.py', ROOT/'native/src/Core.cpp', ROOT/'native/src/Plugin.cpp', ROOT/'config.json',
        ROOT/'mod/meshes/AstraAsedio/ballesta.nif', ROOT/'mod/AstraAsedio.esp', ROOT/'reports/sight_path_verified.json',
    ))
    from tests.test_session_contract import InputBehaviorContract
    behavior_count = unittest.defaultTestLoader.loadTestsFromTestCase(InputBehaviorContract).countTestCases()
    compile_report = json.loads((ROOT / 'reports/plugin_compile.json').read_text(encoding='utf-8'))
    if not compile_report['success']:
        raise RuntimeError('Compiler failed')
    for item in compile_report['scripts']:
        if sha(ROOT / item['source']) != item['source_sha256'] or sha(ROOT / item['pex']) != item['sha256']:
            raise RuntimeError('Compile evidence is stale')
    path = ROOT / 'reports/input_revision.json'
    revision = repair_encoding(json.loads(path.read_text(encoding='utf-8')))
    revision['revision']='v10'
    revision['user_v03_evidence']='reports/user_evidence_v03.json'
    revision['hypothesis_and_limits'][-1] = (
        'La cancelación anterior al commit se revalida después del preflight. RemoveItem y Weapon.Fire '
        'son llamadas externas: una vez comprometido el disparo no se promete cancelarlo o deshacerlo. '
        'Weapon.Fire devuelve void; compilación y trazas no prueban proyectil visible ni daño.'
    )
    revision['implemented_contract'].update({
        'post_preflight_scalar_generation_revalidation': True,
        'controls_released_before_visual_cleanup': True,
        'acquisition_cleanup_rollback_contract': True,
        'atomic_native_ammo_launch_transaction': False,
        'first_person_on_entry': True,
        'mouse_look_drives_aim': True,
        'camera_switch_control_owned': True,
        'previous_perspective_restoration_policy': 'owned change, eligible camera only; no exact third-person substate claim',
        'pitch_max_degrees': 80.0,
        'native_sight_camera': True,
        'native_plugin_required_before_controls': True,
        'legacy_aim_requires_use_sight_camera_false': True,
    })
    revision['verification'].update({
        'session_contract_tests_passed': count,
        'source_level_behavior_cases': behavior_count,
        'control_lease_contract_tests_passed': lease_count,
        'control_lease_test_result': 'reports/control_lease_behavior.json',
        'controller_source_sha256': sha(ROOT / 'mod/scripts/source/AstraAsedioActi.psc'),
        'session_source_sha256': sha(ROOT / 'mod/scripts/source/AstraAsedioSession.psc'),
        'camera_contract_tests_passed': camera_count,
        'camera_contract_report': 'reports/camera_aim_behavior.json',
        'native_sight_contract_tests_passed': native_count,
        'native_sight_contract_report': 'reports/native_sight_behavior.json',
    })
    path.write_text(json.dumps(revision, indent=2, ensure_ascii=False), encoding='utf-8')
    regression = {
        'revision': 'v10',
        'pre_fix_results': {
            'exit_inside_transform_preflight': 'failed: ammo -1, launches 1',
            'menu_inside_transform_preflight': 'failed: ammo -1, launches 1',
            'controls_release_before_visual_reset': 'failed: visual reset preceded release',
        },
        'post_fix_contracts_pass': True,
        'controller_source_sha256': sha(ROOT / 'mod/scripts/source/AstraAsedioActi.psc'),
        'test_source_sha256': sha(ROOT / 'tests/test_session_contract.py'),
        'runtime_execution': False,
        'scope': 'Three actual PSC boundary regressions observed red before the fix and green afterwards. Native fixtures do not execute the game VM.',
    }
    (ROOT / 'reports/shot_cleanup_regression.json').write_text(json.dumps(regression, indent=2), encoding='utf-8')
    sight_revision = {
        'revision': 'v10', 'success': native['success'], 'runtime_execution': False,
        'controller_source_sha256': sha(ROOT/'mod/scripts/source/AstraAsedioActi.psc'),
        'session_source_sha256': sha(ROOT/'mod/scripts/source/AstraAsedioSession.psc'),
        'native_api_source_sha256': sha(ROOT/'mod/scripts/source/AstraSightNative.psc'),
        'implemented_contract': {
            'UseSightCamera_default_and_vmad': True,
            'native_missing_visible_rejection_before_acquire': True,
            'entry': 'Initial look alignment, actual FP state 0, one BeginSight per positive token; IsSightReady polled within 1.5 seconds.',
            'aim': 'Native owns in-session yaw/pitch/node writes; PSC caches validated CaptureAim(false) actual pose.',
            'shot': 'Ammo checked before atomic CaptureAim(true) freeze/snapshot; one native settle tick and cached native preflight; legacy three ticks retained.',
            'stale_result': 'Generation, token, phase, menu and ownership gates discard old reads/freezes/prepare/commit, Reset animation results, reload visual restoration returns and clock reads without releasing or changing a newer lease.',
            'clock': 'OnUpdate, PauseInput and ResumeInput publish lastTick only if the captured generation/token still owns the session; PauseInput captures generation after legitimate shot cancellation.',
            'input_ownership': 'RequestShot, RequestExit, InputReady, SetAimKey and event dispatch capture generation/token before external reads or Trace; stale callbacks cannot adopt a replacement lease or alter its input gates.',
            'thaw': 'Scoped token/generation on precommit cancellation, preparation failure and committed release; pending native boundaries block a replacement freeze on the same token.',
            'exit': 'EndSight before Session.Release, perspective/control restoration and visual/aim cleanup.',
            'exit_pose': 'One coherent cached ApplyAim after End and Release, protected by endingSession plus generation/token guards; next Begin uses that restored initial pose.',
            'load': 'Interrupted controller cleanup recovered through EmergencyCleanup; older stacks invalidated before restored 3D can launch or overwrite a new lease.',
            'legacy_aim': 'Mouse/arrow source paths are available only when UseSightCamera is explicitly false.',
            'native_ammo_launch_atomic': False,
        },
        'verification': {
            'native_sight_test_count': native_count, 'native_sight_report': 'reports/native_sight_behavior.json',
            'red_logs': ['reports/native_sight_psc_red.txt','reports/native_sight_psc_lifecycle_red.txt','reports/native_sight_psc_load_red.txt','reports/native_sight_psc_context_red.txt','reports/native_sight_psc_cleanup_red.txt','reports/native_sight_psc_vmad_red.txt','reports/native_sight_psc_reset_red.txt','reports/native_sight_psc_reload_red.txt','reports/native_sight_psc_clock_red.txt','reports/native_sight_psc_input_owner_red.txt'],
            'bethesda_compile_report': 'reports/plugin_compile.json',
            'legacy_contract_tests': count + lease_count + camera_count,
        },
        'limits': native['fixture_limits'],
    }
    (ROOT/'reports/sight_control_revision.json').write_text(json.dumps(sight_revision,indent=2),encoding='utf-8')
    print(json.dumps({'input_contracts': count, 'behavior_cases': behavior_count, 'control_lease_contracts': lease_count, 'camera_contracts':camera_count,'native_sight_contracts':native_count,'game_vm_executed': False}))

if __name__ == '__main__':
    main()
