"""Seal the current local review; this does not assert in-game verification."""
from pathlib import Path
import hashlib,json,datetime
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    verified=json.loads((ROOT/'reports/verification_v18.json').read_text())
    assert verified['success'] and not verified['in_game_verified']
    native=json.loads((ROOT/'reports/native_build_receipt.json').read_text())
    assert native['plugin_version_string']=='3.5.3' and native['plugin_version']==0x03050030 and native['api_version']==4
    files={**verified['files_sha256'],**native['files_sha256']}
    for n,h in files.items():assert sha(ROOT/n)==h,('Changed verified input',n)
    for n,h in verified['reports_sha256'].items():
        assert sha(ROOT/'reports'/n)==h,('Changed verification evidence',n)
        files['reports/'+n]=h
    parent=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v17')
    for rel in ['mod/AstraAsedio.esp','addons/Atalaya/AstraAsedio_Atalaya.esp',
                'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp',
                'mod/meshes/AstraAsedio/ballesta.nif','mod/meshes/AstraAsedio/torre.nif',
                'addons/WhiterunTorres/meshes/AstraAsedio/voladizo_este.nif',
                'addons/WhiterunTorres/meshes/AstraAsedio/voladizo_oeste.nif']:
        assert sha(ROOT/rel)==sha(parent/rel),(rel,'Unrequested geometry/core change')
    old_modular=json.loads((ROOT/'reports/modular_v17.json').read_text())
    old_modular.update(revision=18, plugin_source_revision=17, placements_unchanged_from_v17=True, runtime_station_relocation=False)
    (ROOT/'reports/modular_v18.json').write_text(json.dumps(old_modular,indent=2),encoding='utf-8')
    evidence=json.loads((ROOT/'reports/runtime_evidence_v18/receipt.json').read_text())
    for name,h in evidence['files_sha256'].items():
        assert sha(ROOT/'reports/runtime_evidence_v18'/name)==h
    for rel in ['reports/v18_root_review.md','reports/verification_v18.json',
                'docs/README_v18.md','docs/PRUEBAS_v18.md','docs/VALIDACION_v18.md',
                'scripts/package_v18.py','scripts/seal_review_v18.py',
                'reports/modular_v18.json','reports/baseline_v18.json',
                'reports/runtime_evidence_v18/receipt.json','reports/runtime_evidence_v18/AstraSight.log',
                'reports/runtime_evidence_v18/Papyrus.0.log',
                'reports/v18_regression_red.log','reports/v18_cpp_red.log','reports/v18_focused_green.log',
                'reports/v18_native_build.log','reports/v18_papyrus_compile.log','reports/v18_release_gate.log']:
        files[rel]=sha(ROOT/rel)
    for p in (ROOT/'native/licenses').iterdir():
        if p.is_file():files[p.relative_to(ROOT).as_posix()]=sha(p)
    review={'revision':18,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'approved_for_offline_qa':True,'closing_reviewer':'root','new_independent_review':False,
            'in_game_verified':False,'verification_report_sha256':sha(ROOT/'reports/verification_v18.json'),
            'review_notes':'reports/v18_root_review.md','files_sha256':files,
            'limits':['V18 projectile movement/trajectory, collisions and damage require Skyrim',
                      'Static city handoff, lifecycle and camera require Skyrim',
                      'V17 speed mismatch is measured; exact city lifecycle trigger is inferred']}
    (ROOT/'reports/review_v18.json').write_text(json.dumps(review,indent=2),encoding='utf-8')
    print('V18_OFFLINE_REVIEW_SEALED',len(files),'files')
if __name__=='__main__':main()
