"""Copy read-only build caches and seal the inherited v07 baseline."""
from pathlib import Path
import json, hashlib, shutil
ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.with_name('Ballesta_Astra_Vanilla_SE_v07')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
baseline = {str(p.relative_to(OLD)): sha(p) for folder in ['native','mod','source','dist'] for p in (OLD/folder).rglob('*') if p.is_file()}
for name in ['CommonLibSSE-NG','spdlog','rapidcsv','windows_sdk','python']:
    src = OLD/'build/native'/name
    dst = ROOT/'build/native'/name
    if src.exists() and not dst.exists(): shutil.copytree(src,dst)
# v07 reached its QA profile but was never packaged: its dist/ is empty, so there are no parent archives to pin.
(ROOT/'reports/v08_baseline.json').write_text(json.dumps({'parent':str(OLD),'parent_project':str(OLD),'parent_sha256':baseline,'parent_archives':{p.name:sha(p) for p in (OLD/'dist').glob('*.zip')},'parent_review':'docs/revision/2026-10-04-revision-tecnica-astra-v07.md','v07_packaged':any((OLD/'dist').glob('*.zip')),'user_confirmed_v07':None,'v07_in_game_verified':False,'scope':'v08 applies the P0/P1 backlog of the v07 technical review; v07 stays untouched.'},indent=2),encoding='utf-8')
print('v07 baseline sealed; local pinned caches copied')
