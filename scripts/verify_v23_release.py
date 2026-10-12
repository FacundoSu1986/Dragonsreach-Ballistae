"""Read-only release gates on current v23 artifacts; no archived builders run."""
from pathlib import Path
import collections
import datetime
import hashlib
import json
import re
import struct
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import build_plugin as B
import build_native as N

PLUGINS = ['mod/AstraAsedio.esp','addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp',
           'addons/Atalaya/AstraAsedio_Atalaya.esp','addons/GuardAnim/AstraAsedio_GuardAnim.esp']
BASEZIP = ROOT.with_name('Ballesta_Astra_Vanilla_SE_v21')/'dist/AstraAsedio_QA_v22_Completo_MO2.zip'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def plugin_checks():
    catalog = {}
    for name in PLUGINS:
        p = Plugin(ROOT/name)
        masters = [v.rstrip(b'\0').decode() for k,v in p.subrecords(p.datos(0)) if k=='MAST']
        records = {}
        ids = []
        for typ,off,n,depth in p.recorrer():
            if typ in ('TES4','GRUP'):continue
            fid = p.form_id(off)
            ids.append(fid)
            subs = p.subrecords(p.datos(off))
            records[fid] = (typ,subs)
        assert len(ids)==len(set(ids)),name+' duplicate FormID'
        catalog[Path(name).name] = (masters,records)
    def exists(owner,fid):
        if not fid:return True
        masters,records = catalog[owner]
        index = fid>>24
        if index == len(masters):return fid in records
        assert index < len(masters),(owner,hex(fid),'master index')
        master = masters[index]
        if master not in catalog:
            assert master in ('Skyrim.esm','Update.esm','Dawnguard.esm'),master
            return True
        own_index = len(catalog[master][0])
        return ((own_index<<24)|(fid&0xFFFFFF)) in catalog[master][1]
    counts = {}
    for owner,(masters,records) in catalog.items():
        counts[owner] = len(records)
        for fid,(typ,subs) in records.items():
            for key,value in subs:
                if key in ('NAME','ALFR','PKID','ALPC') and len(value)==4:
                    ref = struct.unpack('<I',value)[0]
                    assert exists(owner,ref),(owner,hex(fid),key,hex(ref))
                    if key in ('PKID','ALPC'):
                        index=ref>>24
                        target_owner=owner if index==len(masters) else masters[index]
                        if target_owner in catalog:
                            target_id=(len(catalog[target_owner][0])<<24)|(ref&0xFFFFFF)
                            assert catalog[target_owner][1][target_id][0]=='PACK',(owner,key,'expected PACK')
                if key=='VMAD':
                    vm = B.read_vmad(value,quest=typ=='QUST')
                    scripts = vm['scripts']+[s for a in vm['aliases'] for s in a['scripts']]
                    for script in scripts:
                        source = ROOT/'mod/scripts/source'/(script['name']+'.psc')
                        assert source.is_file(),script['name']
                        text = source.read_text()
                        parent_source = source
                        parents = set()
                        while True:
                            parent = re.search(r'\bScriptname\s+\w+\s+extends\s+(\w+)',parent_source.read_text(),re.I)
                            if not parent or parent[1].casefold() in parents:break
                            parents.add(parent[1].casefold())
                            parent_source = source.with_name(parent[1]+'.psc')
                            if not parent_source.is_file():break
                            text += '\n'+parent_source.read_text()
                        for prop in script['properties']:
                            item = script['properties'][prop]
                            assert re.search(r'\bProperty\s+'+re.escape(prop)+r'\b',text,re.I),(script['name'],prop)
                            if item['type']==1:assert exists(owner,item['value']['form_id']),(owner,script['name'],prop)
    core = catalog['AstraAsedio.esp'][1]
    player = B.read_vmad(dict(core[0x03000801][1])['VMAD'])['scripts']
    assert [s['name'] for s in player]==['AstraAsedioActi']
    with zipfile.ZipFile(BASEZIP) as z:
        assert z.testzip() is None
        baseline_core = ROOT/'build/guard-v23/compare_core.esp'
        baseline_core.write_bytes(z.read('AstraAsedio.esp'))
        old = Plugin(baseline_core)
        oldvm = next(B.read_vmad(dict(old.subrecords(old.datos(o)))['VMAD']) for t,o,n,d in old.recorrer()
                     if t=='ACTI' and old.form_id(o)==0x03000801)
        assert player[0]==oldvm['scripts'][0],'player properties changed'
        for zipname,path in [('AstraAsedio_Atalaya.esp',ROOT/PLUGINS[2]),
                ('meshes/AstraAsedio/ballesta.nif',ROOT/'mod/meshes/AstraAsedio/ballesta.nif'),
                ('meshes/AstraAsedio/ballesta_guardia.nif',ROOT/'mod/meshes/AstraAsedio/ballesta_guardia.nif'),
                ('meshes/AstraAsedio/torre_atalaya_v20.nif',ROOT/'addons/Atalaya/meshes/AstraAsedio/torre_atalaya_v20.nif')]:
            assert z.read(zipname)==path.read_bytes(),zipname+' changed from v22'
    return {'records':counts,'vmad_aliases_and_object_properties_resolve':True,
            'player_properties_and_high_meshes_match_v22':True,'vanilla_master_reference_integrity':'structural; no xEdit engine check'}


def main(revision=23):
    assert revision in (23,24,25,26,27,28,29)
    checks = {}
    def record(name,fn):
        try:checks[name]={'success':True,'result':fn()}
        except Exception as e:checks[name]={'success':False,'error':str(e)}
        print(name,'PASS' if checks[name]['success'] else 'FAIL')
    def run(args):
        result = subprocess.run(args,cwd=ROOT,capture_output=True,text=True)
        assert result.returncode==0,(result.stdout+result.stderr)[-5000:]
        return (result.stdout+result.stderr)[-6000:]
    record('v23_acceptance',lambda:run([sys.executable,'-m','unittest','tests.test_v23_release']))
    if revision==24:
        record('v24_exclusive_operator_ai_and_save_migration',lambda:run([sys.executable,'-m','unittest','tests.test_v24_guard_ai']))
    if revision==25:
        record('v25_exclusive_operator_ai_and_scale_diagnosis',lambda:run([sys.executable,'-m','unittest','tests.test_v25_guard_ai']))
    if revision==26:
        record('v26_owned_idle_shield_and_context_diagnosis',lambda:run([sys.executable,'-m','unittest','tests.test_v26_guard_ai']))
    if revision==27:
        record('v26_owned_idle_shield_and_context_diagnosis',lambda:run([sys.executable,'-m','unittest','tests.test_v26_guard_ai']))
        record('v27_measured_clause_correction_and_resilience',lambda:run([sys.executable,'-m','unittest','tests.test_v27_guard_resilience']))
    if revision==28:
        record('v28_pose_pump_and_retry_lifecycle',lambda:run([sys.executable,'-m','unittest','tests.test_v26_guard_ai','tests.test_v28_runtime']))
    if revision==29:
        record('v29_hold_clip_grips_rigid_mount_and_retry_lifecycle',lambda:run([sys.executable,'-m','unittest','tests.test_v26_guard_ai','tests.test_v28_runtime','tests.test_v29_guard_simple']))
    record('player_camera_input_lease_regressions',lambda:run([sys.executable,'-m','unittest',
           'tests.test_camera_aim','tests.test_control_lease','tests.test_session_contract']))
    record('hkx_independent_decode',lambda:run([sys.executable,'scripts/verify_hkx_v23.py']))
    record('plugin_bindings_and_player_preservation',plugin_checks)
    def bytecode():
        report = json.loads((ROOT/'reports/plugin_compile.json').read_text())
        assert report['success'] and report['compile_from_fresh_staging']
        for script in report['scripts']:
            assert script['success'] and sha(ROOT/script['source'])==script['source_sha256']
            assert sha(ROOT/script['pex'])==script['sha256']
            safety = script['bytecode_safety']
            assert sha(ROOT/safety['disassembly'])==safety['disassembly_sha256']
        for name in ('AstraAsedioGuard','AstraGuardiaAuto'):
            asm = (ROOT/'reports/papyrus_bytecode'/(name+'.disassemble.pas')).read_text()
            assert not re.search(r'CallMethod\s+Fire\b',asm,re.I),name+' still launches from VM'
        asm = (ROOT/'reports/papyrus_bytecode/AstraAsedioGuard.disassemble.pas').read_text()
        for native in ('BeginOperation','GetStatus','EndOperation','NotifyCombat'):
            assert re.search(r'CallStatic\s+AstraGuardNative\s+'+native+r'\b',asm,re.I),native
        if revision>=24:
            for method in ('StopCombat','SheatheWeapon','EvaluatePackage'):
                assert re.search(r'CallMethod\s+'+method+r'\b',asm,re.I),method+' absent from final PEX'
            bootstrap=(ROOT/'reports/papyrus_bytecode/AstraAsedioPlayerAlias.disassemble.pas').read_text()
            for method in ('Clear','ForceRefTo','EvaluatePackage'):
                assert re.search(r'CallMethod\s+'+method+r'\b',bootstrap,re.I),method+' absent from bootstrap PEX'
        if revision>=26:
            for method in ('GetEquippedShield','UnequipItem'):
                assert re.search(r'CallMethod\s+'+method+r'\b',asm,re.I),method+' absent from final PEX'
        return {'fresh_compiled_scripts':len(report['scripts']),'source_pex_disassembly_hashes_match':True}
    record('compiled_bytecode',bytecode)
    def native():
        report = json.loads((ROOT/'reports/native_build_receipt.json').read_text())
        assert report['architecture']=='AMD64' and report['runtime']=='1.6.1170.0'
        assert report['api_version']==4 and report['npc_api_version']==1
        for name,digest in report['files_sha256'].items():assert sha(ROOT/name)==digest,('stale DLL receipt',name)
        dll = (ROOT/'mod/SKSE/Plugins/AstraSight.dll').read_bytes()
        pe_offset = struct.unpack_from('<I',dll,0x3C)[0]
        assert dll[:2]==b'MZ' and dll[pe_offset:pe_offset+4]==b'PE\0\0'
        assert struct.unpack_from('<H',dll,pe_offset+4)[0]==0x8664
        assert b'AstraGuardNative\0' in dll and b'SKSEPlugin_Version\0' in dll
        return run([str(N.CTEST),'--test-dir',str(ROOT/report['build_dir']),'--output-on-failure'])
    record('native_build_and_ctest',native)
    record('native_pe_exports_and_skse_metadata',lambda:run([sys.executable,'native/verify_binary.py']))
    files = [p for folder in ('mod','addons/WhiterunTorres','addons/Atalaya','addons/GuardAnim')
             for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix.lower() in ('.esp','.nif','.psc','.pex','.dll','.hkx','.seq','.json')]
    report = {'revision':revision,'success':all(c['success'] for c in checks.values()),
              'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,
              'files_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in files},
              'game_tested':False,'live_installation_modified':False,'nexus_uploaded':False,
              'historical_checks':'Archived build routes are not executed; current acceptance includes preserved v23 geometry/HKX contracts'}
    (ROOT/f'reports/verification_v{revision}.json').write_text(json.dumps(report,indent=2)+'\n')
    for name,check in checks.items():
        if not check['success']:print(name,check['error'])
    return 0 if report['success'] else 1


if __name__ == '__main__':raise SystemExit(main())
