"""Verify current build inputs, portable tests and PE metadata; never load the game DLL."""
from pathlib import Path
import hashlib,json,subprocess,sys,re
ROOT=Path(__file__).resolve().parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    build=json.loads((ROOT/'reports/native_build_receipt.json').read_text())
    for name,digest in build['files_sha256'].items():
        if sha(ROOT/name)!=digest:raise RuntimeError('Native build evidence is stale: '+name)
    vendor=build.get('vendor_manifest')
    if vendor and (not vendor['immutable'] or sha(ROOT/vendor['report'])!=vendor['sha256']):
        raise RuntimeError('Read-only vendor manifest evidence is stale')
    subprocess.run([sys.executable,str(ROOT/'native/verify_binary.py')],check=True,capture_output=True,text=True)
    output='';total=0;executables={}
    for name in ['AstraCoreTests.exe','AstraV07Tests.exe','AstraV08Tests.exe','AstraV09Tests.exe','AstraV10Tests.exe','AstraV15Tests.exe','AstraV17Tests.exe','AstraV18Tests.exe','AstraV19Tests.exe']:
        executable=ROOT/build.get('build_dir','build/native/release-verified')/name
        run=subprocess.run([str(executable)],capture_output=True,text=True)
        current=run.stdout+run.stderr;output+=current
        assertions=re.search(r'(\d+) (?:v(?:0[789]|10|15|17|18|19) )?assertions.*?(\d+) failures',current)
        if run.returncode!=0 or not assertions or int(assertions[2])!=0:raise RuntimeError('Portable native tests failed: '+name)
        total+=int(assertions[1]);executables[name]=sha(executable)
    print(output)
    report={'success':True,'assertions_passed':total,'failures':0,'output':output,'test_executables_sha256':executables,'dll_sha256':sha(ROOT/'mod/SKSE/Plugins/AstraSight.dll'),'native_build_receipt_sha256':sha(ROOT/'reports/native_build_receipt.json'),'verification_script_sha256':sha(Path(__file__)),'engine_dll_loaded':False,'in_game_verified':False,'scope':'Current PE/input hash checks and portable C++ tests; no Skyrim hooks or Papyrus VM execution.'}
    (ROOT/'reports/native_artifacts_verified.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
if __name__=='__main__':main()
