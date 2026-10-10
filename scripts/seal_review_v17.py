"""Seal the current local review; this does not assert in-game verification."""
from pathlib import Path
import hashlib,json,datetime
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    verified=json.loads((ROOT/'reports/verification_v17.json').read_text())
    assert verified['success'] and not verified['in_game_verified']
    native=json.loads((ROOT/'reports/native_build_receipt.json').read_text())
    assert native['plugin_version_string']=='3.5.2' and native['plugin_version']==0x03050020 and native['api_version']==4
    files={**verified['files_sha256'],**native['files_sha256']}
    for n,h in files.items():assert sha(ROOT/n)==h,('Changed verified input',n)
    for n,h in verified['reports_sha256'].items():
        assert sha(ROOT/'reports'/n)==h,('Changed verification evidence',n)
        files['reports/'+n]=h
    parent=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v16')
    for rel in ['mod/AstraAsedio.esp','addons/Atalaya/AstraAsedio_Atalaya.esp',
                'mod/meshes/AstraAsedio/ballesta.nif','mod/meshes/AstraAsedio/torre.nif',
                'addons/WhiterunTorres/meshes/AstraAsedio/voladizo_este.nif',
                'addons/WhiterunTorres/meshes/AstraAsedio/voladizo_oeste.nif']:
        assert sha(ROOT/rel)==sha(parent/rel),(rel,'Unrequested geometry/core change')
    for rel in ['reports/v17_root_review.md','reports/verification_v17.json',
                'docs/README_v17.md','docs/PRUEBAS_v17.md','docs/VALIDACION_v17.md',
                'scripts/package_v17.py','scripts/seal_review_v17.py']:
        files[rel]=sha(ROOT/rel)
    for p in (ROOT/'native/licenses').iterdir():
        if p.is_file():files[p.relative_to(ROOT).as_posix()]=sha(p)
    review={'revision':17,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'approved_for_offline_qa':True,'closing_reviewer':'root','new_independent_review':False,
            'in_game_verified':False,'verification_report_sha256':sha(ROOT/'reports/verification_v17.json'),
            'review_notes':'reports/v17_root_review.md','files_sha256':files,
            'limits':['Actual launch velocity/trajectory and damage require Skyrim',
                      'Fresh city script binding, retirement and E require Skyrim',
                      'No recent save was parsed; saved binding issue remains a hypothesis']}
    (ROOT/'reports/review_v17.json').write_text(json.dumps(review,indent=2),encoding='utf-8')
    print('V17_OFFLINE_REVIEW_SEALED',len(files),'files')
if __name__=='__main__':main()
