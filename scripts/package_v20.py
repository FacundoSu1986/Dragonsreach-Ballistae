"""Installable QA update, with only own Atalaya NIF and preserved core assets."""
from pathlib import Path
import json,hashlib,datetime
from package_v19 import archive,SUFFIXES
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    verified=json.loads((ROOT/'reports/verification_v20.json').read_text());assert verified['success']
    for rel,h in verified['files_sha256'].items():assert sha(ROOT/rel)==h,('Changed verified input',rel)
    core={p.relative_to(ROOT/'mod').as_posix():p for p in (ROOT/'mod').rglob('*') if p.is_file() and p.suffix.lower() in SUFFIXES}
    atalaya={p.relative_to(ROOT/'addons/Atalaya').as_posix():p for p in (ROOT/'addons/Atalaya').rglob('*') if p.is_file() and p.suffix.lower() in ('.esp','.nif')}
    assert set(atalaya)=={'AstraAsedio_Atalaya.esp','meshes/AstraAsedio/torre_atalaya_v20.nif'}
    docs={'Docs/AstraAsedio/README_v20.md':ROOT/'docs/README_v20.md'}
    docs.update({'Docs/AstraAsedio/Licenses/'+p.name:p for p in (ROOT/'native/licenses').iterdir() if p.is_file()})
    full=archive('AstraAsedio_QA_v20_MO2.zip',{**core,**atalaya,**docs})
    addon=archive('AstraAsedio_Atalaya_QA_v20_MO2.zip',{**atalaya,'Docs/AstraAsedio/README_v20.md':ROOT/'docs/README_v20.md'})
    result={'revision':20,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verification_report_sha256':sha(ROOT/'reports/verification_v20.json'),'qa':[full,addon],'public':[],'nexus_uploaded':False,'in_game_verified':False,'WhiterunTorres_update_required':False,'core_payload_changed':False,'native_payload_changed':False,'shipping_vanilla_geometry':False}
    (ROOT/'reports/package_v20.json').write_text(json.dumps(result,indent=2));(ROOT/'dist/MANIFEST_v20.json').write_text(json.dumps(result,indent=2))
    for p in result['qa']:print('PACKAGE_OK',p['path'],p['bytes'],p['sha256'])
if __name__=='__main__':main()
