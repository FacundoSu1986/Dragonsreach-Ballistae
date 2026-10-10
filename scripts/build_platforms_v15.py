"""Blender export of two own meshes; shaders reference vanilla texture paths."""
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
import bpy,addon_utils
import build_assets as A
import build_tower_v12 as T
import platforms_v15_geometry as G
from mathutils import Vector

def main():
    addon_utils.enable('io_scene_nifly',default_set=True)
    cfg=json.loads((ROOT/'config.json').read_text())
    mats=T.stockade_materials()
    sources=[]
    for name in ('este','oeste'):
        A.clear();s,parts=G.build(name,cfg)
        root=A.empty('AstraVoladizo_'+name)
        objects=[T.merge_own(parts,key,'Astra_'+name+'_'+key,bpy.data.materials[value],root) for key,value in mats.items()]
        boxes=[(b['lo'],b['hi']) for b in s['collision_boxes']]
        # Visual supporting beams/braces below the walking surface have matching
        # solid Havok. Their local AABBs cannot intrude into the original top path.
        for p in parts:
            if p['kind']!='log' or any(k in p['name'] for k in ('Rail','Rear')):continue
            lo=[min(v[i] for v in p['verts']) for i in range(3)];hi=[max(v[i] for v in p['verts']) for i in range(3)]
            boxes.append((lo,hi))
        col=A.add_collision(root,boxes)
        flags=A.empty('BSXFlags:'+name,root);flags['BSXFlags_Name']='BSX';flags['BSXFlags_Value']='HAVOC | COMPLEX'
        target=ROOT/'addons/WhiterunTorres/meshes/AstraAsedio'/('voladizo_'+name+'.nif');target.parent.mkdir(parents=True,exist_ok=True)
        A.select(objects+[root,col,flags],root)
        bpy.ops.export_scene.pynifly(filepath=str(target),target_game='SKYRIMSE',blender_xf=False,intuit_defaults=False,
                                   export_animations=False,preserve_hierarchy=True,export_modifiers=False,export_colors=True)
        # Separate editable scene keeps only own geometry, no donor model.
        source=ROOT/'source'/('Voladizo_v15_'+name+'.blend')
        bpy.ops.wm.save_as_mainfile(filepath=str(source))
        sources.append({'name':name,'nif':str(target.relative_to(ROOT)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
                        'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                        'parts':len(parts),'collision_boxes':len(boxes),'site':s})
        print('PLATFORM_EXPORTED',name,len(parts),len(boxes),target.stat().st_size,flush=True)
    (ROOT/'reports/platforms_v15_build.json').write_text(json.dumps({'sites':sources,'source_geometry':'own generated parts',
                'textures':'vanilla references only','engine_verified':False},indent=2))
if __name__=='__main__':main()
