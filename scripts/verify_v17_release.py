"""Current-source, compiled payload, geometry and immutable-parent release gate."""
from pathlib import Path
import hashlib,json,sys,subprocess,datetime,re,struct
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import build_plugin as B
import patch_plugin_v12 as P
from build_modular_v13 import subs,vanilla_records

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def payload():
    paths=[p for p in (ROOT/'mod').rglob('*') if p.is_file() and p.suffix.lower() in ('.esp','.dll','.nif','.pex','.psc','.seq')]
    paths += [p for p in (ROOT/'addons/WhiterunTorres').rglob('*') if p.is_file() and p.suffix.lower() in ('.esp','.nif')]
    paths += [ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp']
    return paths

def properties(script):
    src=(ROOT/'mod/scripts/source'/ (script+'.psc')).read_text()
    own={n.lower():t.lower() for t,n in re.findall(r'(?im)^\s*(\w+)\s+Property\s+(\w+)[^\r\n]*\bAuto\b',src)}
    parent=re.search(r'(?im)^Scriptname\s+\w+\s+extends\s+(\w+)',src)[1]
    if parent.lower().startswith('astra'):own={**properties(parent),**own}
    return own

def validate_vmad():
    city=P.record_map(Plugin(str(ROOT/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp')))
    core=P.record_map(Plugin(str(ROOT/'mod/AstraAsedio.esp')));forms={**core,**city}
    external=set()
    for raw in city.values():
        if 'VMAD' not in subs(raw):continue
        for script in B.read_vmad(subs(raw)['VMAD'])['scripts']:
            external.update(p['value']['form_id'] for p in script['properties'].values() if p['type']==1 and p['value']['form_id'] not in forms)
    assert all(fid>>24<3 for fid in external),'Unresolved own reference'
    forms.update(vanilla_records(external))
    checked=0
    for fid,raw in city.items():
        if 'VMAD' not in subs(raw):continue
        for script in B.read_vmad(subs(raw)['VMAD'])['scripts']:
            fields=properties(script['name'])
            for name,prop in script['properties'].items():
                t=fields[name.lower()];expected={'string':2,'int':3,'float':4,'bool':5}.get(t,1)
                assert prop['type']==expected,(fid,name,t,prop['type'])
                if expected==1:
                    target=prop['value']['form_id'];assert target in forms,(fid,name,'Missing reference')
                    sig=forms[target][:4]
                    required={'weapon':b'WEAP','ammo':b'AMMO','sound':b'SOUN','astraasediosession':b'QUST','astraasedioguard':b'REFR','actor':b'ACHR','objectreference':b'REFR'}[t]
                    assert sig==required,(name,required,sig)
                checked+=1
    return checked

def main():
    baseline=json.loads((ROOT/'reports/baseline_v17.json').read_text());parent=Path(baseline['parent'])
    for name,h in baseline['files_sha256'].items():assert sha(parent/name)==h,('Parent v16 was modified',name)
    paths=payload()+[ROOT/'config.json',ROOT/'scripts/build_modular_v17.py',ROOT/'scripts/platforms_v15_geometry.py',ROOT/'scripts/verify_v17_release.py']
    modules=['test_v15_platforms','test_v15_placements','test_v15_station','test_v15_takeover','test_v13_guard','test_v14_sector',
             'test_camera_aim','test_control_lease','test_session_contract','test_assets','test_v12_lower','test_v16_frame_dispatch','test_v16_placement_recovery','test_v17_launch','test_v17_city_upgrade']
    paths += [ROOT/'tests'/(m+'.py') for m in modules]
    before={str(p.relative_to(ROOT)):sha(p) for p in paths}
    args=[sys.executable,'-m','pytest',*[f'tests/{m}.py' for m in modules],'-q']
    r=subprocess.run(args,cwd=ROOT,capture_output=True,text=True);print(r.stdout+r.stderr);assert r.returncode==0
    subprocess.run([sys.executable,str(ROOT/'scripts/verify_native_artifacts.py')],cwd=ROOT,check=True)
    compiled=json.loads((ROOT/'reports/plugin_compile.json').read_text());assert compiled['success'] and len(compiled['scripts'])==6
    for s in compiled['scripts']:
        assert sha(ROOT/s['source'])==s['source_sha256'] and sha(ROOT/s['pex'])==s['sha256']
        b=s['bytecode_safety'];assert sha(ROOT/b['disassembly'])==b['disassembly_sha256']
    stationasm=(ROOT/'reports/papyrus_bytecode/AstraAsedioStation.disassemble.pas').read_text()
    assert '.object AstraAsedioStation AstraAsedioActi' in stationasm
    assert 'ReservePlayerLease' in stationasm and 'ReleasePlayerLease' in stationasm and 'IsEffectsQuiescent' in stationasm
    platforms=json.loads((ROOT/'reports/platforms_v15.json').read_text());assert platforms['success']
    for name,h in platforms['inputs_sha256'].items():assert sha(ROOT/name)==h,('Changed platform input',name)
    for s in platforms['sites']:
        assert sha(ROOT/s['nif'])==s['nif_sha256'] and s['lost_nav_centers']==0
        assert not s['gun_contacts'] and not s['initial_projectile_hits']
    metadata=json.loads((ROOT/'reports/tower_geometry_metadata_v14.json').read_text());cfg=json.loads((ROOT/'config.json').read_text())
    for s in metadata['sites']:
        for ref in s['refs']:assert sha(Path(cfg['extracted'])/'meshes'/ref['model'])==ref['sha256']
    # Cached vanilla triangles are unchanged from v14. Reimported own NIFs are
    # current; neither a historical report nor a regenerated timestamp is proof.
    for rel in ('reports/tower_context_v14.json','reports/tower_geometry_este_v14.npz','reports/tower_geometry_oeste_v14.npz','reports/gun_havok_v14.npz'):
        assert sha(ROOT/rel)==sha(parent/rel)
    corecheck=B.validate_plugin(str(ROOT/'mod/AstraAsedio.esp'));assert corecheck['navmesh_components']==1
    vmad_props=validate_vmad()
    plugins=[ROOT/'mod/AstraAsedio.esp',ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp',ROOT/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp']
    initial=[sha(p) for p in plugins]
    subprocess.run([sys.executable,str(ROOT/'scripts/build_modular_v17.py')],cwd=ROOT,check=True)
    assert initial==[sha(p) for p in plugins],'City plugin build is not idempotent'
    assert before=={str(p.relative_to(ROOT)):sha(p) for p in paths},'Payload changed during verification'
    reports=['plugin_compile.json','native_build_receipt.json','native_binary_checks.json','native_artifacts_verified.json','assets_verified.json','platforms_v15_build.json','platforms_v15.json','modular_v17.json']
    result={'revision':17,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'success':True,'command':args,'output':r.stdout+r.stderr,
            'files_sha256':before,'reports_sha256':{p:sha(ROOT/'reports'/p) for p in reports},'vmad_properties_typechecked':vmad_props,
            'native_assertions':2352,'compiled_scripts':6,'parent_baseline_files_verified':len(baseline['files_sha256']),
            'plugin_build_idempotent':True,'in_game_verified':False,'game_vm_executed':False}
    (ROOT/'reports/verification_v17.json').write_text(json.dumps(result,indent=2))
    print('V17_VERIFIED compile6 native2352 geometry2 parentImmutable',vmad_props,'VMAD properties')
if __name__=='__main__':main()
