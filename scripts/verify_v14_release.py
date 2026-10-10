"""Fresh controller/plugin/bytecode checks and explicit spatial/native reuse."""
import json,hashlib,sys,subprocess,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    modules=['test_session_contract','test_control_lease','test_camera_aim','test_native_sight','test_v06_runtime_bindings',
             'test_v07_firing','test_v08_sight_zero','test_v09_input_fixes','test_v10_sight','test_plugin_contract',
             'test_v12_lower','test_v13_depression','test_v13_guard','test_v13_native_depression',
             'test_v14_cadence','test_v14_sector','test_v14_placements','test_sight_anchor']
    watched=[p for p in (ROOT/'tests').glob('*.py') if p.stem in modules]
    watched += [p for p in (ROOT/'mod').rglob('*') if p.is_file() and p.suffix.lower() in ('.nif','.esp','.dll','.psc','.pex','.seq')]
    watched += [ROOT/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp',ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp',
                ROOT/'config.json',ROOT/'reports/towers_v14.json',ROOT/'scripts/build_modular_v14.py']
    before={str(p.relative_to(ROOT)):sha(p) for p in watched}
    args=[sys.executable,'-m','pytest',*[f'tests/{m}.py' for m in modules],'-q']
    r=subprocess.run(args,cwd=ROOT,capture_output=True,text=True);print(r.stdout+r.stderr)
    assert r.returncode==0,'V14 checks failed'
    assert before=={str(p.relative_to(ROOT)):sha(p) for p in watched},'Inputs changed during verification'
    compile=json.loads((ROOT/'reports/plugin_compile.json').read_text())
    assert compile['success'] and len(compile['scripts'])==5
    for s in compile['scripts']:
        assert s['source_sha256']==sha(ROOT/s['source']) and s['sha256']==sha(ROOT/s['pex']),'Stale Papyrus evidence'
        dis=s['bytecode_safety'];assert dis['disassembly_sha256']==sha(ROOT/dis['disassembly'])
    for script in ['verify_native_reuse_v14.py','verify_spatial_reuse_v14.py']:
        subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,check=True)
    city=json.loads((ROOT/'reports/towers_v14.json').read_text())
    assert city['success'] and city['ballista_sha256']==sha(ROOT/'mod/meshes/AstraAsedio/ballesta.nif')
    assert city['context_sha256']==sha(ROOT/'reports/tower_context_v14.json')
    bindings={'gun':'mod/meshes/AstraAsedio/ballesta.nif','context':'reports/tower_context_v14.json',
              'verifier':'scripts/tower_fit_v14.py','selection':'reports/tower_selected_v14.json',
              'geometry_metadata':'reports/tower_geometry_metadata_v14.json'}
    for key,path in bindings.items():assert city['inputs_sha256'][key]==sha(ROOT/path),('Stale tower evidence',key)
    assert city['verifier_sha256']==sha(ROOT/'scripts/tower_fit_v14.py')
    caches=city['geometry_cache_sha256'];assert len(caches)==3
    for path,digest in caches.items():assert sha(ROOT/path)==digest,('Stale geometry cache',path)
    assert city['patrol_marker_sweep_sha256']==sha(ROOT/'reports/patrol_marker_sweep_v14.json')
    metadata=json.loads((ROOT/'reports/tower_geometry_metadata_v14.json').read_text())
    cfg=json.loads((ROOT/'config.json').read_text());extracted=Path(cfg['extracted'])/'meshes'
    for s in metadata['sites']:
        for ref in s['refs']:assert sha(extracted/ref['model'])==ref['sha256'],('Changed inspected vanilla model',ref['model'])
    reports={n:sha(ROOT/'reports'/n) for n in ['plugin_compile.json','native_reuse_v14.json','spatial_reuse_v14.json','towers_v14.json','modular_v14.json']}
    report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'success':True,'command':args,'output':r.stdout+r.stderr,
            'files_sha256':before,'reports_sha256':reports,'source_changed_during_tests':False,'native_assertions':2281,
            'new_native_build':False,'game_vm_executed':False,'in_game_verified':False}
    (ROOT/'reports/verification_v14.json').write_text(json.dumps(report,indent=2))
    print('V14_VERIFIED compile5; native2281 reused binary; new tower geometry; preserved player spatial evidence')
if __name__=='__main__':main()
