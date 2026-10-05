"""Create a disposable project and test reconstruction from config/source."""
from pathlib import Path
import json,shutil,subprocess,hashlib,struct,sys
ROOT=Path(__file__).resolve().parents[1];TEMP=ROOT/'build/rebuild-v08'
sys.path.insert(0,str(ROOT/'scripts/vendor'))
import nif_nodos

def palette(nif,offset,size):
    """NiDefaultAVObjectPalette entries as a set: PyNifly writes them in hash-seed order."""
    d=nif['datos'];_scene,count=struct.unpack_from('<iI',d,offset);pos=offset+8;entries=set()
    for _ in range(count):
        length=struct.unpack_from('<I',d,pos)[0];name=d[pos+4:pos+4+length];pos+=4+length
        entries.add((name,struct.unpack_from('<i',d,pos)[0]));pos+=4
    assert pos==offset+size
    return entries

def equivalent(a_path,b_path):
    """Same blocks byte for byte, except the object palette compared as a set."""
    a=nif_nodos.leer(str(a_path));b=nif_nodos.leer(str(b_path))
    if [t for t,o,s in a['bloques']]!=[t for t,o,s in b['bloques']] or a['strings']!=b['strings']:return False
    for (t,oa,sa),(_t,ob,sb) in zip(a['bloques'],b['bloques']):
        if t=='NiDefaultAVObjectPalette':
            if palette(a,oa,sa)!=palette(b,ob,sb):return False
        elif a['datos'][oa:oa+sa]!=b['datos'][ob:ob+sb]:return False
    return True
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
            # Without --python-exit-code Blender exits 0 even when the script raises.
            result=subprocess.run([blender,'-b','--factory-startup','--python-exit-code','1','--python',str(TEMP/'scripts'/name)],stdout=log,stderr=subprocess.STDOUT)
        assert result.returncode==0,name
        commands.append(name)
    report=json.loads((TEMP/'reports/assets_verified.json').read_text())
    assert report['ok']
    # The disposable build must also reproduce the v08 projectile body and the alpha-free floors.
    assert report['checks']['projectile_box'] and report['checks']['no_alpha_properties']
    rebuilt={n:hashlib.sha256((TEMP/'mod/meshes/AstraAsedio'/f'{n}.nif').read_bytes()).hexdigest() for n in ('torre','ballesta','virote')}
    shipped={n:hashlib.sha256((ROOT/'mod/meshes/AstraAsedio'/f'{n}.nif').read_bytes()).hexdigest() for n in ('torre','ballesta','virote')}
    same={n:equivalent(TEMP/'mod/meshes/AstraAsedio'/f'{n}.nif',ROOT/'mod/meshes/AstraAsedio'/f'{n}.nif') for n in ('torre','ballesta','virote')}
    assert all(same.values()),same
    # Every script the disposable build imports, so packaging can refuse stale evidence.
    inputs={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ('config.json','scripts/build_assets.py','scripts/verify_assets.py','scripts/nif_fisica.py','scripts/vendor/nif_nodos.py','scripts/mechanism_source_fixes.py','scripts/limb_tie_fixes.py','scripts/retime_v07.py')}
    (ROOT/'reports/rebuild_v08.json').write_text(json.dumps({'success':True,'inputs_sha256':inputs,'scope':'Disposable rebuild from preserved v04 with config v08; Blender export/reimport, not game execution.','commands':commands,'config_sha256':hashlib.sha256((ROOT/'config.json').read_bytes()).hexdigest(),'builder_sha256':hashlib.sha256((ROOT/'scripts/build_assets.py').read_bytes()).hexdigest(),'assets_checks':report['checks'],'sequences':report['files']['ballesta']['sequence_details'],'rope_max_gap':report['rope_reimport_max_gap'],'rope_outer_max_error':report['rope_outer_attachment_max_error'],'visual_triangles':report['visual_triangles_total'],'collision_triangles':report['collision_triangles_total'],'projectile_physics':report['projectile_physics_verified'],'rebuilt_nif_sha256':rebuilt,'shipped_nif_sha256':shipped,'byte_identical_to_shipped':rebuilt==shipped,'equivalent_to_shipped':same,'equivalence_rule':'every block byte-identical except NiDefaultAVObjectPalette, compared as a name->block set (PyNifly writes it in hash-seed order)'},indent=2))
    print('v08 reconstruction verified in disposable build project; equivalent:',same,'byte-identical:',rebuilt==shipped)
if __name__=='__main__':main()
