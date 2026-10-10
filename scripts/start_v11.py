"""Copy read-only build caches and seal the inherited v10 baseline."""
from pathlib import Path
import json, hashlib, shutil
ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.with_name('Ballesta_Astra_Vanilla_SE_v10')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
baseline = {str(p.relative_to(OLD)): sha(p) for folder in ['native','mod','source','dist'] for p in (OLD/folder).rglob('*') if p.is_file()}
for name in ['CommonLibSSE-NG','spdlog','rapidcsv','windows_sdk','python']:
    src = OLD/'build/native'/name
    dst = ROOT/'build/native'/name
    if src.exists() and not dst.exists(): shutil.copytree(src,dst)
# Files the user tested in game with v10; v11 must keep them byte-identical.
mod = ROOT/'mod'
invariant = [mod/'meshes/AstraAsedio/ballesta.nif', mod/'meshes/AstraAsedio/virote.nif', mod/'SKSE/Plugins/AstraSight.dll']
invariant += sorted(mod.rglob('*.psc')) + sorted(mod.rglob('*.pex'))
missing = [str(p) for p in invariant if not p.exists()]
if missing: raise SystemExit('missing invariant files: %s' % missing)
(ROOT/'reports/v11_baseline.json').write_text(json.dumps({'parent':str(OLD),'parent_project':str(OLD),'parent_sha256':baseline,
    'parent_archives':{p.name:sha(p) for p in (OLD/'dist').glob('*.zip')},'v10_packaged':any((OLD/'dist').glob('*.zip')),
    'user_tested_v10':True,'user_evidence':'reports/user_evidence_v10/referencia_torre_usuario.webp',
    'invariant_sha256':{str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in invariant},
    'scope':'v11 reemplaza la torre por una torre rústica mixta (geometría propia + piezas vanilla colocadas desde el ESP, puerta vanilla que se abre); ballesta, cámara, mira y scripts quedan iguales a v10, que no se toca.'},indent=2,ensure_ascii=False),encoding='utf-8')
# The copied config still opens v10's source blend; every build of v11 must read its own copy.
cfg_path = ROOT/'config.json'
cfg = json.loads(cfg_path.read_text(encoding='utf-8'))
cfg['source'] = str(ROOT/'source/Torre_Ballesta_lowpoly_v04.blend')
if not Path(cfg['source']).is_file(): raise SystemExit('missing v11 source copy: %s' % cfg['source'])
cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print('v10 baseline sealed; %d invariant files; local pinned caches copied; config source -> v11' % len(invariant))
