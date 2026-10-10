"""Prove reuse of v13's verified native binary without claiming a new build."""
from pathlib import Path
import hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v13')
EXES=['AstraCoreTests.exe','AstraV07Tests.exe','AstraV08Tests.exe','AstraV09Tests.exe','AstraV10Tests.exe']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    receipt_path=BASE/'reports/native_build_receipt.json'
    receipt=json.loads(receipt_path.read_text())
    unchanged={};separate={}
    for name,digest in receipt['files_sha256'].items():
        assert sha(BASE/name)==digest,'v13 build receipt mismatch: '+name
        if name=='mod\\scripts\\source\\AstraAsedioActi.psc':
            separate[name]={'v13':digest,'v14':sha(ROOT/name),'verified_by':'fresh Papyrus compile receipt, not native build reuse'}
        else:
            assert sha(ROOT/name)==digest,'Native reuse input changed: '+name
            unchanged[name]=digest
    vendor=receipt['vendor_manifest']
    assert vendor['immutable'] and sha(BASE/vendor['report'])==vendor['sha256']
    assert sha(ROOT/vendor['report'])==vendor['sha256']
    subprocess.run([sys.executable,str(ROOT/'native/verify_binary.py')],check=True,capture_output=True,text=True)
    results=[];total=0
    for name in EXES:
        path=ROOT/receipt['build_dir']/name
        assert sha(path)==sha(BASE/receipt['build_dir']/name),'Portable binary changed: '+name
        run=subprocess.run([str(path)],capture_output=True,text=True)
        output=run.stdout+run.stderr
        match=re.search(r'(\d+) (?:v(?:0[789]|10) )?assertions.*?(\d+) failures',output)
        assert run.returncode==0 and match and int(match[2])==0,output
        total+=int(match[1]);results.append({'name':name,'sha256':sha(path),'assertions':int(match[1]),'output':output})
    report={'success':True,'new_native_build':False,'reused_verified_build':'v13',
            'v13_build_receipt_sha256':sha(receipt_path),'unchanged_native_inputs':unchanged,
            'papyrus_checked_separately':separate,'dll_sha256':sha(ROOT/'mod/SKSE/Plugins/AstraSight.dll'),
            'binary_checks_sha256':sha(ROOT/'reports/native_binary_checks.json'),
            'assertions_passed':total,'failures':0,'tests':results,
            'verification_script_sha256':sha(Path(__file__)),'engine_dll_loaded':False,'in_game_verified':False}
    (ROOT/'reports/native_reuse_v14.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('NATIVE_V13_REUSE_VERIFIED',total,'assertions; no new native build')
if __name__=='__main__':main()
