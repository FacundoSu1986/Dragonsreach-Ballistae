"""Create a disposable project and test reconstruction from config/source."""
from pathlib import Path
import json,shutil,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1];TEMP=ROOT/'build/rebuild-v07'
def main():
    TEMP.mkdir(parents=True,exist_ok=True)
    for name in ['reports','source','mod/meshes/AstraAsedio','build']:(TEMP/name).mkdir(parents=True,exist_ok=True)
    shutil.copytree(ROOT/'scripts',TEMP/'scripts',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    cfg=json.loads((ROOT/'config.json').read_text());cfg['source']=str(ROOT/'source/Torre_Ballesta_lowpoly_v04.blend')
    (TEMP/'config.json').write_text(json.dumps(cfg))
    blender=r'C:\Program Files\Blender Foundation\Blender 4.4\blender.exe'
    commands=[]
    for name in ['build_assets.py','verify_assets.py']:
        with (TEMP/'build'/f'{name}.log').open('w',encoding='utf-8') as log:
            result=subprocess.run([blender,'-b','--factory-startup','--python',str(TEMP/'scripts'/name)],stdout=log,stderr=subprocess.STDOUT)
        assert result.returncode==0,name
        commands.append(name)
    report=json.loads((TEMP/'reports/assets_verified.json').read_text())
    assert report['ok']
    (ROOT/'reports/rebuild_v07.json').write_text(json.dumps({'success':True,'scope':'Disposable rebuild from preserved v04 with config v07; Blender export/reimport, not game execution.','commands':commands,'config_sha256':hashlib.sha256((ROOT/'config.json').read_bytes()).hexdigest(),'builder_sha256':hashlib.sha256((ROOT/'scripts/build_assets.py').read_bytes()).hexdigest(),'assets_checks':report['checks'],'sequences':report['files']['ballesta']['sequence_details'],'rope_max_gap':report['rope_reimport_max_gap'],'rope_outer_max_error':report['rope_outer_attachment_max_error'],'visual_triangles':report['visual_triangles_total'],'collision_triangles':report['collision_triangles_total']},indent=2))
    print('v07 reconstruction verified in disposable build project')
if __name__=='__main__':main()
