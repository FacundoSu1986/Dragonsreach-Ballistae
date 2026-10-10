"""Seal verified files into a MO2 ZIP and a separate editable source ZIP."""
from pathlib import Path
import json,hashlib,zipfile,unittest,io,tempfile,shutil,sys
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
REVISION='v10'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assets=json.loads((ROOT/'reports/assets_verified.json').read_text())
    if not assets['ok']: raise RuntimeError('Asset verification is not passing')
    for name,record in assets['files'].items():
        if sha(ROOT/'mod/meshes/AstraAsedio'/f'{name}.nif')!=record['sha256']: raise RuntimeError('Stale NIF evidence: '+name)
    renders=json.loads((ROOT/'reports/renders.json').read_text())
    for name,digest in renders['nifs'].items():
        if sha(ROOT/'mod/meshes/AstraAsedio'/f'{name}.nif')!=digest: raise RuntimeError('Renders do not reflect current NIFs')
    compiler=json.loads((ROOT/'reports/plugin_compile.json').read_text())
    if not compiler['success']: raise RuntimeError('Compiler failed')
    sys.path.insert(0,str(ROOT/'scripts'))
    from compile_papyrus import validate_assembly,validate_input_assembly,validate_camera_assembly
    for item in compiler['scripts']:
        if sha(ROOT/item['pex'])!=item['sha256']: raise RuntimeError('Stale PEX evidence')
        if sha(ROOT/item['source'])!=item['source_sha256']: raise RuntimeError('PSC changed after compile')
        safety=item['bytecode_safety']
        assembly=ROOT/safety['disassembly']
        if sha(assembly)!=safety['disassembly_sha256']: raise RuntimeError('Stale PEX disassembly evidence')
        validate_assembly(assembly.read_text(encoding='utf-8-sig'))
        if Path(item['source']).stem=='AstraAsedioActi': validate_input_assembly(assembly.read_text(encoding='utf-8-sig'))
        if Path(item['source']).stem in ('AstraAsedioActi','AstraAsedioSession'): validate_camera_assembly(assembly.read_text(encoding='utf-8-sig'))
    behavior=json.loads((ROOT/'reports/input_behavior.json').read_text())
    if not behavior['success'] or behavior['test_source_sha256']!=sha(ROOT/'tests/test_session_contract.py') or behavior['controller_source_sha256']!=sha(ROOT/'mod/scripts/source/AstraAsedioActi.psc'):
        raise RuntimeError('The input behavior evidence is stale')
    lease_behavior=json.loads((ROOT/'reports/control_lease_behavior.json').read_text())
    if not lease_behavior['success'] or lease_behavior['test_source_sha256']!=sha(ROOT/'tests/test_control_lease.py') or lease_behavior['session_source_sha256']!=sha(ROOT/'mod/scripts/source/AstraAsedioSession.psc'):
        raise RuntimeError('The control lease evidence is stale')
    camera=json.loads((ROOT/'reports/camera_aim_behavior.json').read_text())
    if not camera['success'] or camera['test_source_sha256']!=sha(ROOT/'tests/test_camera_aim.py') or camera['controller_source_sha256']!=sha(ROOT/'mod/scripts/source/AstraAsedioActi.psc') or camera['session_source_sha256']!=sha(ROOT/'mod/scripts/source/AstraAsedioSession.psc'):
        raise RuntimeError('The camera aim evidence is stale')
    sight=json.loads((ROOT/'reports/native_sight_behavior.json').read_text())
    if not sight['success'] or sight['test_source_sha256']!=sha(ROOT/'tests/test_native_sight.py') or sight['controller_source_sha256']!=sha(ROOT/'mod/scripts/source/AstraAsedioActi.psc'):
        raise RuntimeError('Native sight control evidence is stale')
    for name,digest in sight['dependency_sha256'].items():
        if sha(ROOT/name)!=digest:raise RuntimeError('Native sight test dependency changed: '+name)
    runtime_binding=json.loads((ROOT/'reports/runtime_bindings_behavior.json').read_text())
    if not runtime_binding['success'] or runtime_binding['test_source_sha256']!=sha(ROOT/'tests/test_v06_runtime_bindings.py') or runtime_binding['controller_source_sha256']!=sha(ROOT/'mod/scripts/source/AstraAsedioActi.psc'):
        raise RuntimeError('Runtime binding regression evidence is stale')
    for name,digest in runtime_binding['dependency_sha256'].items():
        if sha(ROOT/name)!=digest:raise RuntimeError('Runtime binding dependency changed: '+name)
    native=json.loads((ROOT/'reports/native_build_receipt.json').read_text())
    for name,digest in native['files_sha256'].items():
        if sha(ROOT/name)!=digest:raise RuntimeError('Native build evidence is stale: '+name)
    native_checks=json.loads((ROOT/'reports/native_artifacts_verified.json').read_text())
    dll=ROOT/'mod/SKSE/Plugins/AstraSight.dll'
    if not native_checks['success'] or native_checks['dll_sha256']!=sha(dll) or native_checks['native_build_receipt_sha256']!=sha(ROOT/'reports/native_build_receipt.json') or native_checks['verification_script_sha256']!=sha(ROOT/'scripts/verify_native_artifacts.py'):
        raise RuntimeError('Current native portable verification is unavailable')
    pe=json.loads((ROOT/'reports/native_binary_checks.json').read_text())
    if pe['sha256']!=sha(dll) or pe['machine']!='AMD64 (0x8664)' or pe['metadata']['packed_plugin_version']!=50528256:raise RuntimeError('Current native binary not verified')
    for license in (ROOT/'native/licenses').iterdir():
        if not license.is_file():continue
        delivered=ROOT/'mod/Docs/AstraAsedio/Licenses'/license.name
        if not delivered.is_file() or sha(delivered)!=sha(license):raise RuntimeError('Missing native dependency notice: '+license.name)
    review=json.loads((ROOT/'reports/v10_final_review.json').read_text())
    if not review['success'] or review['open_findings'] or review['reviews']['code_review']['status']!='PASS':
        raise RuntimeError('Final independent reviews are not closed')
    for name,digest in review['files_sha256'].items():
        if sha(ROOT/name)!=digest:raise RuntimeError('Reviewed file changed after approval: '+name)
    for report in ('v07_firing_behavior','v07_camera_wiring_behavior','v08_shot_sound_behavior','v08_sight_zero_behavior','v09_input_fixes_behavior','v10_sight_behavior'):
        evidence=json.loads((ROOT/f'reports/{report}.json').read_text())
        if not evidence['success'] or evidence['controller_source_sha256']!=sha(ROOT/'mod/scripts/source/AstraAsedioActi.psc'):raise RuntimeError('Stale contract '+report)
        for name,digest in evidence['dependency_sha256'].items():
            if sha(ROOT/name)!=digest:raise RuntimeError('Stale '+report+' dependency '+name)
    rebuild=json.loads((ROOT/'reports/rebuild_v10.json').read_text())
    if not rebuild['success'] or rebuild['builder_sha256']!=sha(ROOT/'scripts/build_assets.py') or rebuild['config_sha256']!=sha(ROOT/'config.json'):raise RuntimeError('Stale rebuild evidence')
    # The rebuild must have compared against THESE NIFs, built by THESE scripts.
    for name,digest in rebuild['inputs_sha256'].items():
        if sha(ROOT/name)!=digest:raise RuntimeError('Stale rebuild evidence, input changed: '+name)
    for name,digest in rebuild['shipped_nif_sha256'].items():
        if sha(ROOT/'mod/meshes/AstraAsedio'/f'{name}.nif')!=digest:raise RuntimeError('Rebuild evidence is for another '+name+'.nif')
    if set(rebuild['shipped_nif_sha256'])!={'torre','ballesta','virote'} or not all(rebuild['equivalent_to_shipped'].values()):raise RuntimeError('Rebuild did not cover every shipped NIF')
    # v09: the straight rustic stair tower. Route/navmesh evidence must be for THESE files.
    route=json.loads((ROOT/'reports/stair_route_verified.json').read_text())
    if route['nif_sha256']!=sha(ROOT/'mod/meshes/AstraAsedio/torre.nif') or route['esp_sha256']!=sha(ROOT/'mod/AstraAsedio.esp') or not route['collision_layout_equal_to_reference'] or route['body_clearance_blocking_hits'] or route['uncovered_navmesh_samples']:
        raise RuntimeError('Stair route evidence is stale or failing')
    walk=json.loads((ROOT/'reports/collision_walkable.json').read_text());reference=json.loads((ROOT/'reports/reference_collision_escalera_directa.json').read_text())
    if any(walk[k]!=reference[k] for k in reference if k!='ballesta_fixed_box_units'):
        raise RuntimeError('Walkable collision differs from the square stair reference')
    pedestal=walk['ballesta_fixed_box_units'];ref_pedestal=reference['ballesta_fixed_box_units']
    if pedestal['min']!=ref_pedestal['min'] or pedestal['max'][:2]!=ref_pedestal['max'][:2]:
        raise RuntimeError('Pedestal collision footprint differs from the reference')
    if abs(pedestal['max'][2]-pedestal['min'][2]-json.loads((ROOT/'config.json').read_text())['sight']['pedestal_collision_height_units'])>1e-3:
        raise RuntimeError('Pedestal collision is not the v10 lowered box')
    # v10: the tail sight path must be verified on THESE NIFs with THESE camera parameters (camera pull-in found in the v09 log).
    sight_path=json.loads((ROOT/'reports/sight_path_verified.json').read_text())
    if not sight_path['success'] or any(sight_path['nif_sha256'][n]!=sha(ROOT/'mod/meshes/AstraAsedio'/f'{n}.nif') for n in ('torre','ballesta')):
        raise RuntimeError('Sight path evidence is stale or failing')
    if set(sight_path.get('inputs_sha256',{}))!={'scripts/sight_pose.py','scripts/verify_sight_path.py','config.json'} or any(sha(ROOT/n)!=d for n,d in sight_path['inputs_sha256'].items()):
        raise RuntimeError('Sight path evidence is for other camera parameters or another verifier')
    if sight_path['min_head_to_camera_collision_clearance']<25 or sight_path['min_camera_to_sight_meshes']<15 or not sight_path['operator_positions_on_pedestal']:
        raise RuntimeError('Sight path evidence below the fixed v10 thresholds')
    anchor=json.loads((ROOT/'reports/sight_anchor_verified.json').read_text())
    if not anchor['ok'] or len(anchor['poses'])!=24 or anchor['nif_sha256']!=sha(ROOT/'mod/meshes/AstraAsedio/ballesta.nif'):
        raise RuntimeError('Current camera anchor is not verified')
    elevation=json.loads((ROOT/'reports/elevation_diagnosis.json').read_text())
    if not elevation['muzzle_transforms_verified'] or elevation['floor_minimum_clearance']<2.0 or elevation['nif_sha256']!=sha(ROOT/'mod/meshes/AstraAsedio/ballesta.nif'):
        raise RuntimeError('High elevation is not verified for the current NIF')
    profile=json.loads((ROOT/'reports/test_profile.json').read_text())
    current_mod_hashes={str(p.relative_to(ROOT/'mod')):sha(p) for p in (ROOT/'mod').rglob('*') if p.is_file()}
    if set(profile['enabled_mo2_mods'])!={'AstraAsedio_QA_v10','Address Library All in One'} or profile['installed_sha256']!=current_mod_hashes or sha(Path(profile['address_library']))!=profile['address_library_sha256']:
        raise RuntimeError('The v10 QA profile report is stale')
    bindings=json.loads((ROOT/'reports/limb_ties_verified.json').read_text())
    if not bindings['ok'] or bindings['binding_count']!=14 or bindings['nif_sha256']!=sha(ROOT/'mod/meshes/AstraAsedio/ballesta.nif'):
        raise RuntimeError('Current limb bindings are not verified')
    # Actual acceptance suite must pass before packaging.
    stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.discover(str(ROOT/'tests')))
    (ROOT/'reports/tests.log').write_text(stream.getvalue())
    print(stream.getvalue())
    if not result.wasSuccessful(): raise RuntimeError('Acceptance checks failed')
    # Falsify a copied artifact: an unchanged green report must reject it.
    sys.path.insert(0,str(ROOT/'tests')); import test_assets
    with tempfile.TemporaryDirectory(prefix='astra_verifier_') as tmp:
        dest=Path(tmp); shutil.copytree(ROOT/'mod/meshes',dest/'mod/meshes'); (dest/'reports').mkdir()
        shutil.copy2(ROOT/'reports/assets_verified.json',dest/'reports/assets_verified.json')
        p=dest/'mod/meshes/AstraAsedio/ballesta.nif'; b=bytearray(p.read_bytes()); b[-1]^=1; p.write_bytes(b)
        log=io.StringIO()
        with patch.object(test_assets,'ROOT',dest):
            falsified=unittest.TextTestRunner(stream=log).run(unittest.TestSuite([test_assets.ExportAcceptance('test_exported_artifacts_meet_contract')]))
        if falsified.wasSuccessful() or len(falsified.failures)!=1 or falsified.errors: raise RuntimeError('Tampered artifact was not reliably rejected')
    (ROOT/'reports/falsification.json').write_text(json.dumps({'tampered_final_nif_rejected':True,'production_files_modified':False},indent=2))
    build=json.loads((ROOT/'reports/plugin_build.json').read_text())
    if sha(ROOT/'mod/AstraAsedio.esp')!=build['sha256']: raise RuntimeError('ESP changed after validation')
    if not build['structural_valid'] or not build['navmesh_clearance_verified'] or build['navmesh_components']!=1: raise RuntimeError('Plugin geometry checks are not passing')
    status={'revision':REVISION,'parent_revision':'v09','release_stage':'alpha_for_interactive_validation','file_tests_passed':result.testsRun,'assets':assets['checks'],'visual_triangles':assets['visual_triangles_total'],'collision_triangles':assets['collision_triangles_total'],'papyrus_compile':True,'papyrus_final_pex_disassembly_checked':True,'observed_v01_none_to_array_cast_removed':True,'user_runtime_evidence':{'v01':'reports/runtime_diagnostic/evidence.json','v02':'reports/user_evidence_v02.json'},'input_event_handler':True,'exit_independent_of_aim_update':True,'v02_input_polling_failure_exact_cause_proven':False,'binding_count':bindings['binding_count'],'bindings_reimport_verified':True,'mechanism_revision':'reports/mechanism_revision.json','limb_ties_revision':'reports/limb_ties_revision.json','test_room':build['test_room'],'activation':build['activation'],'esp_binary_contract_checks':True,'xedit_check_for_errors':False,'ck_navmesh_finalized':False,'ck_navmesh_surface_adjustment_pending':True,'skyrim_in_game_cases_executed':0,'skyrim_case_count_scope':'v10 only; the user played v08 and v09 on 2026-10-05 (reports/user_evidence_v08.json, user_evidence_v09.json); v10 unexecuted','native_ui_available':False,'runtime_target':'1.6.1170 + SKSE64 2.2.8 + Address Library','qa_profile':profile['profile'],'previous_selected_profile':profile['previous_selected_profile'],'previous_profile_files_unchanged':profile['previous_profile_files_unchanged'],'sha256':current_mod_hashes}
    status.update({'input_contract_tests_passed':behavior['test_count'],'control_lease_contract_tests_passed':lease_behavior['test_count'],'post_preflight_cancellation_checked':True,'acquisition_cleanup_rollback_checked':True,'controls_released_before_visual_cleanup':True,'native_ammo_launch_atomicity_claimed':False})
    status.update({'camera_contract_tests_passed':camera['test_count'],'first_person_mouse_aim':True,'yaw_degrees':360,'pitch_limits_degrees':[-5,80],'mount_raise_units':20,'high_elevation_nif_verified':True,'user_v03_evidence':'reports/user_evidence_v03.json','camera_runtime_verified':False})
    status.update({'native_sight_contract_tests_passed':sight['test_count'],'native_core_assertions_passed':native_checks['assertions_passed'],'native_dll_sha256':sha(dll),'native_pe_verified':True,'direct_activate_to_sight':True,'camera_node':'AstraSightCameraNode','camera_local_units':anchor['local_position_units'],'native_hooks_in_game_verified':False,'sight_preview_is_engine_proof':False,'address_library_dependency_enabled':True})
    status.update({'independent_reviews_closed':True,'final_review_receipt_sha256':sha(ROOT/'reports/v10_final_review.json')})
    status.update({'runtime_binding_regression_tests_passed':runtime_binding['test_count'],'own_camera_state_api':3,'session_api_tasklet_callable':True,'v05_user_confirmed_camera_and_mouse':True,'v09_fps_measured':False,'v08_firing_in_game_verified':'user: firing and explosion work (2026-10-05)','runtime_diagnosis':'reports/fire_runtime_diagnosis.json'})
    status.update({'user_runtime_v06_baseline':'reports/v07_runtime_baseline.json','v06_user_tested':True,'v07_shot_contract':'reports/v07_firing_behavior.json','v07_camera_wiring_contract':'reports/v07_camera_wiring_behavior.json','post_camera_hook':'installed since v07; never ran in the v09 log (0 writes, 0 skips); the camera comes from the first-person getters','v08_sight_zero_functions':'legacy since v10, not on the camera path (sightPose replaced them)','continuous_fire_hold_attack':True,'initial_fire_mode':'single','fire_mode_toggle':'Sprint (mapped)','fire_seconds':.3,'release_seconds':.1,'reset_seconds':1.2,'nominal_cycle_seconds':1.5,'native_settle_tick_seconds':.05,'engine_latency_v08_measured':False})
    # v08 backlog (docs/superpowers/specs/2026-10-04-v08-backlog-p0-p1.md); every value is a record or build fact, none an engine measurement.
    body=json.loads((ROOT/'reports/projectile_body.json').read_text())
    rustic=json.loads((ROOT/'reports/rustico.json').read_text())
    status.update({'v10_camera':'tail camera on the rear-sight/zero line, slides forward with elevation (reports/sight_path_verified.json)','v10_iron_sights':'rear ring + front post moved natively for the 75 m zero',
        'v10_pedestal_collision_height':json.loads((ROOT/'config.json').read_text())['sight']['pedestal_collision_height_units'],'v10_root_cause':'reports/user_evidence_v09.json camera_pull_in',
        'sight_path_min_sweep_clearance':sight_path['min_head_to_camera_collision_clearance'],'user_evidence_v09':'reports/user_evidence_v09.json','camera_180_in_game_verified':False})
    status.update({'v09_fixes':['stuck burst (release serial)','first entry yaw 360.0','menu: native sight suspension','operator message'],'v09_camera_180':'root cause found from the v09 log; fixed in v10 by geometry, pending in-game confirmation',
        'user_evidence_v08':'reports/user_evidence_v08.json','native_plugin_version':'3.3.0','v09_input_contract':'reports/v09_input_fixes_behavior.json',
        'tower':'straight rustic stair (Escalera_Directa design + rustico.py)','rustic_pieces':rustic['count'],'rustic_max_displacement_m':rustic['max_displacement_m'],
        'stair_route':'reports/stair_route_verified.json','walk_test_in_game':False})
    status.update({'v08_backlog_applied':['B1','B2','B3','B4','B6','B7'],'b5_operator_sweep_deferred':True,'b12_lod_not_applicable':True,
        'v08_shot_sound_contract':'reports/v08_shot_sound_behavior.json','v08_sight_zero_contract':'reports/v08_sight_zero_behavior.json',
        'sight_zero_native':True,'sight_zero_meters':json.loads((ROOT/'config.json').read_text())['sight_zero_meters'],'native_plugin_version':'3.3.0',
        'shot_sound_papyrus':True,'siege_damage_records':build['siege'],'projectile_pickable':False,'ammo_playable':False,
        'projectile_body':{k:body[k] for k in ('mass','restitution','half_extents_units','box_coverage','inertia_axis_aligned')},
        'siege_damage_in_game_verified':False,'drop_model_in_game_verified':False})
    manifest=json.loads((ROOT/'reports/source_manifest.json').read_text())
    if sha(ROOT/'source/Torre_Ballesta_lowpoly_v04.blend')!=manifest['sha256']:
        raise RuntimeError('The preserved source copy was changed')
    original=Path(manifest['source_original'])
    if original.exists() and sha(original)!=manifest['sha256']:
        raise RuntimeError('The original Blender source was changed')
    status['original_source_sha256']=manifest['sha256']
    status['source_copy_matches_original_manifest']=True
    (ROOT/'reports/delivery_status.json').write_text(json.dumps(status,indent=2))
    from release_notes_v10 import make_validation
    text=make_validation(ROOT, assets, result.testsRun, profile, camera, elevation, build)
    (ROOT/'VALIDACION.md').write_text(text,encoding='utf-8')
    docs=['README.md','PRUEBAS_EN_JUEGO.md','VALIDACION.md']
    (ROOT/'dist').mkdir(exist_ok=True)
    runtime=ROOT/f'dist/AstraAsedio_{REVISION}_MO2.zip'
    with zipfile.ZipFile(runtime,'w',zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=False) as z:
        for p in sorted((ROOT/'mod').rglob('*')):
            if p.is_file(): z.write(p,p.relative_to(ROOT/'mod'))
        for name in docs: z.write(ROOT/name,'Docs/AstraAsedio/'+name)
        z.write(ROOT/'reports/delivery_status.json','Docs/AstraAsedio/delivery_status.json')
    sources=ROOT/f'dist/AstraAsedio_{REVISION}_Fuentes.zip'
    legacy_exclusions={ROOT/'reports/clear_test_patch.json',ROOT/'scripts/build_clear_test_patch.py',ROOT/'reports/runtime_diagnostic/vanilla_records.json'}
    with zipfile.ZipFile(sources,'w',zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=False) as z:
        for directory in ('source','scripts','tests','reports','mod/scripts/source','docs','native'):
            for p in sorted((ROOT/directory).rglob('*')):
                if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.blend1','.blend2') and p != ROOT/'reports/package.json' and p not in legacy_exclusions:
                    z.write(p,p.relative_to(ROOT))
        for name in docs+['config.json']: z.write(ROOT/name,name)
        for name in renders['images']: z.write(ROOT/name,name)
        # v10: the tail sight renders come from verify_sight_path.py (same NIF hashes, gated above).
        for name in sight_path.get('renders',[]): z.write(ROOT/name,name.replace(chr(92),'/'))
        fixture=ROOT/'build/Dawnguard.esm.donors.json'
        if fixture.exists(): z.write(fixture,'build/Dawnguard.esm.donors.json')
        # Keep the xEdit script, never the staged ESM copies or executables.
        check=ROOT/'build/xedit/AstraCheck.ssepas'
        if check.exists(): z.write(check,'build/xedit/AstraCheck.ssepas')
    for archive in (runtime,sources):
        with zipfile.ZipFile(archive) as z:
            if z.testzip(): raise RuntimeError('ZIP integrity failed')
            if any(p.lower().endswith(('.dds','.esm')) for p in z.namelist()): raise RuntimeError('Unexpected vanilla resource in delivery')
    with zipfile.ZipFile(runtime) as z:
        for name,digest in current_mod_hashes.items():
            if hashlib.sha256(z.read(name.replace('\\','/'))).hexdigest()!=digest: raise RuntimeError('Packaged runtime differs from verified artifact: '+name)
    with zipfile.ZipFile(sources) as z:
        for name in z.namelist():
            disk=ROOT/Path(name)
            if not disk.is_file() or hashlib.sha256(z.read(name)).hexdigest()!=sha(disk):raise RuntimeError('Source ZIP differs from project: '+name)
        if any(name.startswith('build/native/') for name in z.namelist()):raise RuntimeError('Native dependency/build inputs must not be distributed')
    baseline=json.loads((ROOT/'reports/v10_baseline.json').read_text())
    for name,digest in baseline['parent_archives'].items():
        if sha(Path(baseline['parent_project'])/'dist'/name)!=digest:raise RuntimeError('Parent v09 delivery changed')
    for name,digest in baseline['parent_sha256'].items():
        if sha(Path(baseline['parent_project'])/name)!=digest:raise RuntimeError('Parent v09 input changed '+name)
    receipt={'revision':REVISION,'archives':[{ 'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in (runtime,sources)],'zip_integrity_verified':True,'runtime_entries_match_verified_hashes':True,'source_entries_match_project':True,'parent_v09_inputs_preserved':True,'parent_v09_archives_preserved':bool(baseline['parent_archives']),'vanilla_dds_or_esm_included':False,'legacy_dates_clamped_in_zip_only':True}
    (ROOT/'reports/package.json').write_text(json.dumps(receipt,indent=2)); print(json.dumps(receipt,indent=2))
if __name__=='__main__': main()
