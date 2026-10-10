"""Seal concrete review and final archive bytes; no engine approval is implied."""
from pathlib import Path
import json,hashlib,zipfile,datetime
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    v=json.loads((ROOT/'reports/verification_v19.json').read_text());assert v['success']
    n=json.loads((ROOT/'reports/native_build_receipt.json').read_text());assert n['plugin_version_string']=='3.5.4' and n['api_version']==4
    files={**v['files_sha256'],**n['files_sha256']}
    for name,h in files.items():assert sha(ROOT/name)==h,('Changed verification input',name)
    for name,h in v['reports_sha256'].items():
        assert sha(ROOT/'reports'/name)==h,('Changed report',name)
        files['reports/'+name]=h
    baseline=json.loads((ROOT/'reports/baseline_v19.json').read_text())
    for name,h in baseline['files_sha256'].items():assert sha(Path(baseline['parent'])/name)==h
    packaged=json.loads((ROOT/'reports/package_v19.json').read_text())
    for p in packaged['qa']+packaged['public']:
        path=ROOT/p['path'];assert sha(path)==p['sha256']
        with zipfile.ZipFile(path) as z:
            assert z.testzip() is None
            assert {name:hashlib.sha256(z.read(name)).hexdigest() for name in z.namelist()}==p['inventory_sha256']
        files[p['path']]=p['sha256']
    for name in ('reports/v19_root_review.md','reports/package_v19.json','reports/xedit_v19.json','reports/verification_v19.json','reports/baseline_v19.json','dist/nexus/MANIFEST.json','docs/NEXUS_PUBLICACION_v19.md','scripts/package_v19.py','scripts/seal_review_v19.py','scripts/write_docs_v19.py','scripts/run_xedit_v19.py'):
        files[name]=sha(ROOT/name)
    for p in [*(ROOT/'docs/nexus').glob('*'),*(ROOT/'reports').glob('adversarial_*_v19.md'),*(ROOT/'reports').glob('v19_*.log')]:
        if p.is_file():files[str(p.relative_to(ROOT))]=sha(p)
    evidence=ROOT/'reports/runtime_evidence_v19'
    ev=json.loads((evidence/'receipt.json').read_text())
    for name,h in ev['files_sha256'].items():
        assert sha(evidence/name)==h;files[str((evidence/name).relative_to(ROOT))]=h
    files[str((evidence/'receipt.json').relative_to(ROOT))]=sha(evidence/'receipt.json')
    report={'revision':19,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'approved_for_offline_qa':True,'approved_for_stable_nexus':False,'in_game_verified':False,'independent_reviewers':3,'review_mode':'single round with accepted findings fixed and disposition recorded','verification_report_sha256':sha(ROOT/'reports/verification_v19.json'),'files_sha256':files,'remaining_release_gates':['v19 handoff/game validation','supported xEdit parent cleanup and Check for Errors','CK NAVM finalization for playable custom navigation','clean install/runtime dependency and compatibility tests'],'nexus_uploaded':False}
    (ROOT/'reports/review_v19.json').write_text(json.dumps(report,indent=2))
    print('V19_REVIEW_SEALED',len(files),'files; QA approved; stable Nexus pending')
if __name__=='__main__':main()
