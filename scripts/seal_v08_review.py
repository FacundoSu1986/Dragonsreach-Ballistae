"""Verify the independent review and snapshot release inputs before packaging.
This snapshot is root's release seal, not an additional independent review.
"""
from pathlib import Path
import json, hashlib, datetime
ROOT=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    review_path=ROOT/'reports/v08_code_review.json'
    review=json.loads(review_path.read_text())
    if review['findings']:
        raise RuntimeError('Code review has unresolved findings')
    for item in review['inputs']:
        p=Path(item['path'])
        if not p.is_absolute(): p=ROOT/p
        if sha(p)!=item['sha256']:
            raise RuntimeError('Code review input changed: '+str(p))
    for name in ('runtime_bindings_behavior','native_artifacts_verified','native_sight_behavior','camera_aim_behavior','plugin_compile','v08_shot_sound_behavior','v08_sight_zero_behavior'):
        if not json.loads((ROOT/f'reports/{name}.json').read_text())['success']:
            raise RuntimeError('Verification not passing: '+name)
    parent=json.loads((ROOT/'reports/v08_baseline.json').read_text())
    for name,digest in parent['parent_archives'].items():
        if sha(Path(parent['parent_project'])/'dist'/name)!=digest:
            raise RuntimeError('Parent delivery changed')
    for name,digest in parent['parent_sha256'].items():
        if sha(Path(parent['parent_project'])/name)!=digest:
            raise RuntimeError('Parent v07 input changed '+name)
    # These files are generated only after checking this receipt during packaging.
    derived={'v08_final_review.json','package.json','delivery_status.json','tests.log','falsification.json'}
    files={}
    for name in ('native','scripts','tests','mod','source','docs','reports','renders'):
        for p in (ROOT/name).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and not (name=='reports' and p.name in derived):
                files[str(p.relative_to(ROOT))]=sha(p)
    for name in ('README.md','PRUEBAS_EN_JUEGO.md','config.json'):
        files[name]=sha(ROOT/name)
    receipt={'revision':'v08','success':True,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope':'Independent review of changed code plus root SHA snapshot of current release inputs. Generated validation and archive receipts are derived afterwards; no FPS or engine execution claimed.',
        'reviews':{'code_review':{'reviewer':review['reviewer'],'status':'PASS','receipt':'reports/v08_code_review.json','sha256':sha(review_path),'scope':review['scope']}},
        'open_findings':[],'files_sha256':files,'engine_tests_executed':0,
        'v07_user_tested':False,'v08_engine_verified':False}
    (ROOT/'reports/v08_final_review.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    print('v08 independent review inputs unchanged; release snapshot:',len(files),'files')

if __name__=='__main__':main()
