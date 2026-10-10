"""Copy read-only build caches and seal the inherited v08 baseline."""
from pathlib import Path
import json, hashlib, shutil
ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.with_name('Ballesta_Astra_Vanilla_SE_v08')
STAIRS = ROOT.with_name('Ballesta_Astra_Escalera_Rustica_v01')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
baseline = {str(p.relative_to(OLD)): sha(p) for folder in ['native','mod','source','dist'] for p in (OLD/folder).rglob('*') if p.is_file()}
for name in ['CommonLibSSE-NG','spdlog','rapidcsv','windows_sdk','python']:
    src = OLD/'build/native'/name
    dst = ROOT/'build/native'/name
    if src.exists() and not dst.exists(): shutil.copytree(src,dst)
# The v08 MO2 profile was tested by the user on 2026-10-05; its logs and screenshots are evidence for v09.
stairs = {str(p.relative_to(STAIRS)): sha(p) for p in (STAIRS/'scripts').glob('*.py')}
(ROOT/'reports/v09_baseline.json').write_text(json.dumps({'parent':str(OLD),'parent_project':str(OLD),'parent_sha256':baseline,
    'parent_archives':{p.name:sha(p) for p in (OLD/'dist').glob('*.zip')},'v08_packaged':any((OLD/'dist').glob('*.zip')),
    'user_tested_v08':True,'user_evidence':'reports/user_evidence_v08.json','stairs_source_project':str(STAIRS),'stairs_scripts_sha256':stairs,
    'scope':'v09 fixes the v08 in-game findings (stuck burst, menu exit, first-entry sample, misleading operator message), records the 180-degree camera fault natively, and adopts the straight rustic stair tower; v08 stays untouched.'},indent=2),encoding='utf-8')
print('v08 baseline sealed; local pinned caches copied')
