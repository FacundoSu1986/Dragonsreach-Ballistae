"""Seal current root-reviewed v16 offline QA evidence without engine claims."""
from pathlib import Path
import hashlib,json,datetime
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    verified=json.loads((ROOT/'reports/verification_v16.json').read_text())
    assert verified['success'] and not verified['in_game_verified']
    native=json.loads((ROOT/'reports/native_build_receipt.json').read_text())
    assert native['plugin_version_string']=='3.5.1' and native['api_version']==4
    files={**verified['files_sha256'],**native['files_sha256']}
    for n,h in files.items():assert sha(ROOT/n)==h,('Changed verified input',n)
    for n,h in verified['reports_sha256'].items():
        assert sha(ROOT/'reports'/n)==h,('Changed verification evidence',n)
        files['reports/'+n]=h
    parent=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v15')
    for rel in ['mod/AstraAsedio.esp','addons/Atalaya/AstraAsedio_Atalaya.esp',
                'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp',
                'addons/WhiterunTorres/meshes/AstraAsedio/voladizo_este.nif',
                'addons/WhiterunTorres/meshes/AstraAsedio/voladizo_oeste.nif']:
        assert sha(ROOT/rel)==sha(parent/rel),(rel,'Unrequested plugin/geometry change')
    modular=json.loads((ROOT/'reports/modular_v15.json').read_text())
    modular['revision']=16
    modular['core_and_city_esp_unchanged_from_v15']=True
    modular['native_dll_version']='3.5.1'
    modular['placement_recovery']={'scope':'known own city refs B40/B50, their own markers, existing platform anchors',
                                   'runs':'guard recovery or player preparation, only when scene is quiescent',
                                   'new_saved_properties_required':False,'engine_verified':False}
    modular['compatibility']['city_save_migration_supported']=False
    modular['compatibility']['new_test_save_required']=False
    modular['compatibility']['placement_recovery_from_v15_implemented']=True
    modular['compatibility']['full_saved_script_migration_guaranteed']=False
    (ROOT/'reports/modular_v16.json').write_text(json.dumps(modular,indent=2),encoding='utf-8')
    additions=['reports/v16_root_review.md','reports/verification_v16.json','reports/modular_v16.json',
               'docs/README_v16.md','docs/PRUEBAS_v16.md','docs/VALIDACION_v16.md',
               'scripts/package_v16.py','scripts/seal_review_v16.py']
    for rel in additions:files[rel]=sha(ROOT/rel)
    for p in (ROOT/'native/licenses').iterdir():
        if p.is_file():files[p.relative_to(ROOT).as_posix()]=sha(p)
    review={'revision':16,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'approved_for_offline_qa':True,'closing_reviewer':'root','new_independent_review':False,
            'in_game_verified':False,'verification_report_sha256':sha(ROOT/'reports/verification_v16.json'),
            'review_notes':'reports/v16_root_review.md','files_sha256':files,
            'limits':['Actual hooks/latency and persisted VM callbacks require Skyrim',
                      'Position persistence is inferred; no ESS was modified or parsed',
                      'Unchanged v15 geometry certificate retained for identical NIF bytes']}
    (ROOT/'reports/review_v16.json').write_text(json.dumps(review,indent=2),encoding='utf-8')
    print('V16_OFFLINE_REVIEW_SEALED',len(files),'files')
if __name__=='__main__':main()
