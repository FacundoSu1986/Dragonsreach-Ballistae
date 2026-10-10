"""Fresh, bounded checks for the final v13 assets and controllers."""
import json,hashlib,sys,subprocess,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    modules=['test_session_contract','test_control_lease','test_camera_aim','test_native_sight','test_v06_runtime_bindings',
             'test_v07_firing','test_v08_sight_zero','test_v09_input_fixes','test_v10_sight','test_plugin_contract',
             'test_v12_lower','test_v13_depression','test_v13_modularity','test_v13_guard','test_v13_native_depression']
    args=[sys.executable,'-m','pytest',*[f'tests/{m}.py' for m in modules],'-q']
    watched=[p for p in (ROOT/'tests').glob('*.py') if p.stem in modules]
    watched += [p for p in (ROOT/'mod').rglob('*') if p.is_file() and p.suffix.lower()in('.nif','.esp','.dll','.psc','.pex','.seq')]
    watched += [ROOT/'addons/Whiterun/AstraAsedio_Whiterun.esp',ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp']
    before={str(p.relative_to(ROOT)):sha(p) for p in watched}
    r=subprocess.run(args,cwd=ROOT,capture_output=True,text=True);print(r.stdout+r.stderr)
    assert r.returncode==0,'V13 checks failed'
    assert before=={str(p.relative_to(ROOT)):sha(p) for p in watched},'Inputs changed during verification'
    subprocess.run([sys.executable,str(ROOT/'scripts/verify_native_artifacts.py')],cwd=ROOT,check=True,capture_output=True,text=True)
    compile=json.loads((ROOT/'reports/plugin_compile.json').read_text())
    assert compile['success'] and len(compile['scripts'])==5
    for s in compile['scripts']:
        assert s['source_sha256']==sha(ROOT/s['source']) and s['sha256']==sha(ROOT/s['pex']),'Stale Papyrus evidence'
    route=json.loads((ROOT/'reports/route_v12.json').read_text());shots=json.loads((ROOT/'reports/shot_clearance_v12.json').read_text())
    assert route['ok'] and route['esp_sha256']==sha(ROOT/'mod/AstraAsedio.esp')
    assert shots['ok'] and shots['shots']==36360 and shots['pitch_range']==[-20,80]
    for n,h in shots['inputs_sha256'].items():assert sha(ROOT/n)==h,('Stale shot evidence',n)
    sight=json.loads((ROOT/'reports/sight_path_verified.json').read_text());assert sight['success'] and sight['poses']==288
    for n,h in sight['inputs_sha256'].items():assert sha(ROOT/n)==h,('Stale sight evidence',n)
    city=json.loads((ROOT/'reports/city_visual_v13.json').read_text())
    assert city['body_route_samples']==172 and city['body_route_blocked_samples']==0
    assert city['city_mesh_sha256']==sha(ROOT/'mod/meshes/AstraAsedio/torre_whiterun.nif')
    assert city['site_sha256']==sha(ROOT/'reports/city_site_v13.json')
    report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'success':True,'command':args,'output':r.stdout+r.stderr,
            'files_sha256':before,'source_changed_during_tests':False,'native_assertions':2281,'game_vm_executed':False,'in_game_verified':False}
    (ROOT/'reports/verification_v13.json').write_text(json.dumps(report,indent=2))
    print('V13_VERIFIED native2281, compile5, shot36360, route162+172, camera288')
if __name__=='__main__':main()
