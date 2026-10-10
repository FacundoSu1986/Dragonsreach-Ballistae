"""Gate only the Atalaya update; unchanged v19 core/city remain immutable."""
from pathlib import Path
import sys,json,hashlib,subprocess,struct,datetime
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import patch_plugin_v12 as P
import colocar_escudos as C
from build_modular_v13 import subs

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
MODULES=['test_v20_world','test_v15_platforms','test_v15_placements','test_v15_station','test_v15_takeover','test_v13_guard','test_v14_sector','test_camera_aim','test_control_lease','test_session_contract','test_assets','test_v12_lower','test_v16_frame_dispatch','test_v17_launch','test_v17_city_upgrade','test_v18_runtime','test_v19_handoff','test_v19_pex_privacy']

def main():
    baseline=json.loads((ROOT/'reports/baseline_v20.json').read_text());parent=Path(baseline['parent'])
    for rel,h in baseline['files_sha256'].items():assert sha(parent/rel)==h,('Parent mutated',rel)
    preserved=[]
    for folder in ('mod','addons/WhiterunTorres','native'):
        for p in (parent/folder).rglob('*'):
            if p.is_file():
                rel=p.relative_to(parent);assert sha(ROOT/rel)==sha(p),('Unexpected core/city/native change',str(rel));preserved.append(str(rel))
    report=json.loads((ROOT/'reports/atalaya_verified_v20.json').read_text());assert report['success']
    for rel,h in report['inputs_sha256'].items():assert sha(ROOT/rel)==h,('Stale scene verification',rel)
    cfg=json.loads((ROOT/'config.json').read_text())
    for donor in report['nearby_vanilla']:assert sha(Path(cfg['extracted'])/'meshes'/donor['model'])==donor['sha256']
    compiled=json.loads((ROOT/'reports/plugin_compile.json').read_text());assert compiled['success']
    for item in compiled['scripts']:
        assert sha(ROOT/item['source'])==item['source_sha256'] and sha(ROOT/item['pex'])==item['sha256']
    # Native sources/DLL and the prior receipt are preserved, not rebuilt or
    # described as freshly re-tested by this placement-only gate.
    native=json.loads((ROOT/'reports/native_build_receipt.json').read_text())
    for rel,h in native['files_sha256'].items():assert sha(ROOT/rel)==h,('Native receipt mismatch',rel)
    rel='addons/Atalaya/AstraAsedio_Atalaya.esp';initial=sha(ROOT/rel);configsha=sha(ROOT/'config.json')
    rebuilt=subprocess.run([sys.executable,'scripts/place_atalaya_v20.py'],cwd=ROOT,capture_output=True,text=True)
    assert rebuilt.returncode==0,rebuilt.stdout+rebuilt.stderr
    assert sha(ROOT/rel)==initial and sha(ROOT/'config.json')==configsha,'Placement build is not idempotent'
    plugin=Plugin(str(ROOT/rel));records=P.record_map(plugin);core=P.record_map(Plugin(str(ROOT/'mod/AstraAsedio.esp')))
    assert struct.unpack_from('<I',subs(plugin.d[:plugin.inicio_datos])['HEDR'],4)[0]==len(list(plugin.recorrer()))-1
    assert struct.unpack_from('<I',subs(plugin.d[:plugin.inicio_datos])['HEDR'],8)[0]>max(fid&0xffffff for fid in records if fid>>24==4)
    for fid,raw in records.items():
        if raw[:4]==b'REFR':assert struct.unpack('<I',subs(raw)['NAME'])[0] in records.keys()|core.keys()
    payload=[p for folder in ('mod','addons/WhiterunTorres','addons/Atalaya') for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix.lower() in ('.esp','.dll','.nif','.pex','.psc','.seq')]
    tracked=payload+[ROOT/'config.json',ROOT/'docs/README_v20.md']+[ROOT/'scripts'/n for n in ('verify_v20_release.py','place_atalaya_v20.py','build_atalaya_v20.py','atalaya_v20_geometry.py','verify_atalaya_v20.py','research_atalaya_v20.py','research_havok_atalaya_v20.py','package_v20.py')]+[ROOT/'tests'/(m+'.py') for m in MODULES]
    before={p.relative_to(ROOT).as_posix():sha(p) for p in tracked}
    cmd=[sys.executable,'-m','pytest',*[f'tests/{m}.py' for m in MODULES],'-q']
    result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);print(result.stdout+result.stderr);assert result.returncode==0
    assert before=={p.relative_to(ROOT).as_posix():sha(p) for p in tracked}
    output={'revision':20,'success':True,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Atalaya relocation only; core/city/native preserved byte for byte from v19','command':cmd,'test_output':result.stdout+result.stderr,'geometry_report_sha256':sha(ROOT/'reports/atalaya_verified_v20.json'),'files_sha256':before,'parent_immutable_files':len(baseline['files_sha256']),'preserved_core_city_native_files':len(preserved),'plugin_build_idempotent':True,'LAND_edits':0,'NAVM_edits':0,'vanilla_REF_overrides':0,'native_version':'3.5.4/API4 unchanged','native_rebuilt':False,'papyrus_recompiled':False,'guard_body_animation_changed':False,'in_game_verified':False,'quest_MQ104_verified':False,'npc_routes_verified':False,'formal_xedit_ck_validated':False,'nexus_stable_approved':False}
    (ROOT/'reports/verification_v20.json').write_text(json.dumps(output,indent=2));print('V20_GATE_OK',len(preserved),'preserved files',len(baseline['files_sha256']),'immutable parent files')
if __name__=='__main__':main()
