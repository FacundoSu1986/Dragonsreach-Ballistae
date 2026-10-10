"""Copy read-only build caches and seal the inherited v06 baseline."""
from pathlib import Path
import json, hashlib, shutil
ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.with_name('Ballesta_Astra_Vanilla_SE_v06')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
baseline = {str(p.relative_to(OLD)): sha(p) for folder in ['native','mod','source','dist'] for p in (OLD/folder).rglob('*') if p.is_file()}
for name in ['CommonLibSSE-NG','spdlog','rapidcsv','windows_sdk','python']:
    src = OLD/'build/native'/name
    dst = ROOT/'build/native'/name
    if src.exists() and not dst.exists(): shutil.copytree(src,dst)
logs = Path(r'C:\Users\Facu2\OneDrive\Documentos\My Games\Skyrim Special Edition')
for file in ['SKSE/AstraSight.log','Logs/Script/Papyrus.0.log','SKSE/skse64.log']:
    src = logs/file
    if src.exists():
        dst = ROOT/'reports/baseline_v06_runtime'/file
        dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
(ROOT/'reports/v07_baseline.json').write_text(json.dumps({'parent':str(OLD),'parent_sha256':baseline,'user_confirmed_v06':'Camera aligned and mouse working; drift beyond 180 and slow shot/reload reported.','v07_in_game_verified':False},indent=2),encoding='utf-8')
print('v06 baseline sealed; local pinned caches copied')
