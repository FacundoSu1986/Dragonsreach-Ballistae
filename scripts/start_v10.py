"""Copy read-only build caches and seal the inherited v09 baseline."""
from pathlib import Path
import json, hashlib, shutil
ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.with_name('Ballesta_Astra_Vanilla_SE_v09')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
baseline = {str(p.relative_to(OLD)): sha(p) for folder in ['native','mod','source','dist'] for p in (OLD/folder).rglob('*') if p.is_file()}
for name in ['CommonLibSSE-NG','spdlog','rapidcsv','windows_sdk','python']:
    src = OLD/'build/native'/name
    dst = ROOT/'build/native'/name
    if src.exists() and not dst.exists(): shutil.copytree(src,dst)
# The v09 MO2 profile was tested by the user on 2026-10-05: everything worked except the camera.
(ROOT/'reports/v10_baseline.json').write_text(json.dumps({'parent':str(OLD),'parent_project':str(OLD),'parent_sha256':baseline,
    'parent_archives':{p.name:sha(p) for p in (OLD/'dist').glob('*.zip')},'v09_packaged':any((OLD/'dist').glob('*.zip')),
    'user_tested_v09':True,'user_evidence':'reports/user_evidence_v09.json',
    'scope':'v10 fixes the camera pull-in found with the v09 camera recorder (pedestal collision between the eye and the sight), moves the camera to the tail on the rear-sight/front-post line, and adds a fixed iron sight; v09 stays untouched.'},indent=2),encoding='utf-8')
print('v09 baseline sealed; local pinned caches copied')
