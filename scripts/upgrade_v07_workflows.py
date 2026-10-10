"""Upgrade copied release workflows, retaining their verification gates."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=ROOT/'scripts/prepare_test_profile.py';s=p.read_text().replace('v06','v07').replace('0.6.0-alpha','0.7.0-alpha');p.write_text(s)
    p=ROOT/'scripts/verify_input_contracts.py';s=p.read_text().replace("'revision']='v06'","'revision']='v07'").replace("'revision': 'v06'","'revision': 'v07'").replace('three settle ticks and original transform preflight retained.','one native settle tick and cached native preflight; legacy three ticks retained.')
    point="    from tests.test_session_contract import InputBehaviorContract"
    insert="""    run_contract('tests.test_v07_firing', 'v07_firing_behavior.json', 'AstraAsedioActi.psc', 'controller_source_sha256', (
        ROOT/'tests/test_native_sight.py', ROOT/'tests/test_control_lease.py',ROOT/'tests/test_camera_aim.py',
        ROOT/'mod/scripts/source/AstraSightNative.psc', ROOT/'native/src/Plugin.cpp', ROOT/'config.json',
    ))
    run_contract('tests.test_v07_camera_contract', 'v07_camera_wiring_behavior.json', 'AstraAsedioActi.psc', 'controller_source_sha256', (
        ROOT/'native/src/Plugin.cpp', ROOT/'scripts/retime_v07.py',ROOT/'scripts/build_plugin.py',ROOT/'config.json',ROOT/'mod/AstraAsedio.esp',
    ))
"""
    if "run_contract('tests.test_v07_firing'" not in s:s=s.replace(point,insert+point)
    p.write_text(s)
    p=ROOT/'scripts/package_release.py';s=p.read_text().replace("REVISION='v06'","REVISION='v07'").replace('v06_final_review','v07_final_review').replace('AstraAsedio_QA_v06','AstraAsedio_QA_v07').replace('33554432','50331648').replace('release_notes_v06','release_notes_v07').replace("'parent_revision':'v05'","'parent_revision':'v06'").replace("'own_camera_state_api':2","'own_camera_state_api':3").replace('v06_fps_measured','v07_fps_measured').replace('v06_firing_in_game_verified','v07_firing_in_game_verified').replace('v06 only; user confirmed v05 camera/mouse but not v06 firing','v07 only; user tested v06 and requested camera/cadence fixes; v07 unexecuted').replace('v06_baseline.json','v07_baseline.json').replace('Parent v05 delivery changed','Parent v06 delivery changed').replace('parent_v05_archives_preserved','parent_v06_archives_preserved')
    gate="    anchor=json.loads((ROOT/'reports/sight_anchor_verified.json').read_text())"
    if 'v07_firing_behavior' not in s:
        s=s.replace(gate,"""    for report in ('v07_firing_behavior','v07_camera_wiring_behavior'):
        evidence=json.loads((ROOT/f'reports/{report}.json').read_text())
        if not evidence['success'] or evidence['controller_source_sha256']!=sha(ROOT/'mod/scripts/source/AstraAsedioActi.psc'):raise RuntimeError('Stale v07 contract')
        for name,digest in evidence['dependency_sha256'].items():
            if sha(ROOT/name)!=digest:raise RuntimeError('Stale v07 dependency '+name)
    rebuild=json.loads((ROOT/'reports/rebuild_v07.json').read_text())
    if not rebuild['success'] or rebuild['builder_sha256']!=sha(ROOT/'scripts/build_assets.py') or rebuild['config_sha256']!=sha(ROOT/'config.json'):raise RuntimeError('Stale rebuild evidence')
"""+gate)
    s=s.replace("    receipt={'revision':REVISION", "    for name,digest in baseline['parent_sha256'].items():\n        if sha(Path(baseline['parent_project'])/name)!=digest:raise RuntimeError('Parent v06 input changed '+name)\n    receipt={'revision':REVISION")
    p.write_text(s)
    p=ROOT/'scripts/seal_v06_review.py';s=p.read_text().replace('v06','v07').replace("'v05_camera_mouse_user_confirmed':True","'v06_camera_mouse_user_confirmed':True");(ROOT/'scripts/seal_v07_review.py').write_text(s)
    p=ROOT/'reports/v07_baseline.json';d=json.loads(p.read_text());parent=Path(d['parent']);d['parent_project']=str(parent);d['parent_archives']={p.name:sha(p) for p in (parent/'dist').glob('*.zip')};p.write_text(json.dumps(d,indent=2))
    p=ROOT/'reports/source_manifest.json';d=json.loads(p.read_text());d['source_copy']=str(ROOT/'source/Torre_Ballesta_lowpoly_v04.blend');p.write_text(json.dumps(d,indent=2))
    p=ROOT/'reports/renders.json';d=json.loads(p.read_text());d['parent_nif_hashes']=d['nifs'].copy();d['nifs']={n:sha(ROOT/f'mod/meshes/AstraAsedio/{n}.nif') for n in d['nifs']};d['reuse_scope']='v06 static rest/elevation renders retained. Retime changes only temporal floats; spatial/material/collision bytes identical. No v07 camera/render engine execution.';d['reuse_evidence']='reports/animation_retime.json';d['image_sha256']={n:sha(ROOT/n) for n in d['images']};p.write_text(json.dumps(d,indent=2))
    print('v07 release workflows upgraded; no checks removed')
if __name__=='__main__':main()
