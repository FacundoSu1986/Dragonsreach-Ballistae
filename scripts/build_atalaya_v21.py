"""Export only own site-fitted tower; core NIF and firing assets stay untouched."""
import sys,json,hashlib,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
import bpy,bmesh,addon_utils
from collections import defaultdict
import build_assets as A
import build_tower_v12 as T
import tower_v12_geometry as G
import atalaya_v21_geometry as N
import nif_nodos,nif_fisica

def main():
    addon_utils.enable('io_scene_nifly',default_set=True)
    (ROOT/'build').mkdir(exist_ok=True)
    names=A.materials();names.update(T.stockade_materials())
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'source/Torre_Ballesta_lowpoly_v04.blend'),use_scripts=False)
    bpy.context.scene.frame_set(1)
    for lib in ('donor_materials.blend','donor_materials_v11.blend'):
        with bpy.data.libraries.load(str(ROOT/'build'/lib),link=False) as (src,dst):dst.materials=[n for n in names.values() if n in src.materials]
    mats={k:bpy.data.materials[v] for k,v in names.items()}
    barriers,floorboxes,walk=T.measure_invariants()
    keep=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.split('.')[0] in T.KEEP]
    assert len(keep)>0
    for o in keep:o.location.z+=G.LOWER_DELTA/A.S
    for o in list(bpy.data.objects):
        if o not in keep:bpy.data.objects.remove(o,do_unlink=True)
    out=N.build();coll=bpy.data.collections.new('Atalaya_propia_v21');bpy.context.scene.collection.children.link(coll)
    for p in out['parts']:T.part_object(p,mats,coll)
    disks=defaultdict(list)
    for o in keep:
        keys=[A.material_key(m.name) for m in o.data.materials]
        if o.name.startswith('Plataforma_giratoria'):
            T.disk_planks_uv(o);disks['stockade_planks'].append((o,'stockade_planks',list(range(len(keys)))))
        else:
            A.remap_uv(o,keys)
            for k in sorted(set(keys)):disks[k].append((o,k,[i for i,v in enumerate(keys) if v==k]))
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'source/Atalaya_v21.blend'))
    root=A.empty('AstraAtalayaTerreno',root=True);bpy.context.view_layer.update()
    obs=[T.merge_own(out['parts'],key,'Atalaya_'+key,mats[key],root) for key in ('stockade_wood','stockade_extra','stockade_planks','rope')]
    obs += [A.merge_parts(parts,root,'Atalaya_disco_'+key,mats[key]) for key,parts in sorted(disks.items())]
    e=out['entry'];ramps=[(G.SX0,G.SX1,e['y0'],G.SY1,e['z0'],140)]
    # Preserve existing clipped edge barriers along the upper stair, add the
    # lower extension below the firing envelope.
    rails=[]
    for a,b in ((G.SX0-2.1,G.SX0+4.9),(G.SX1-4.9,G.SX1+2.1)):
        cap=G.box_firing_cap([a,G.SY1,0],[b,G.SY1,0]);h=min(73.5,cap-140)
        rails.append((a,b,G.SY0,G.SY1,h,140+h,h))
        rails.append((a,b,e['y0'],G.SY0,e['z0']+73.5,73.5,73.5))
    boxes=[([v*A.S for v in lo],[v*A.S for v in hi]) for lo,hi in barriers+floorboxes]+[(b['min'],b['max']) for b in out['boxes']]
    # An inset plate backs the centre of the turntable. Havok chunk quantization
    # can leave a tiny crack on the disk fan's central diagonal; this plate's
    # diagonal misses the operator's centre and stays inside the visible disk.
    boxes.append(([-60.,-55.,139.65],[65.,75.,148.75]))
    col=A.add_collision(root,boxes,ramps+rails)
    bm=bmesh.new();bm.from_mesh(col.data)
    r0=[bm.verts.new((150.5*math.cos(j*math.tau/24),150.5*math.sin(j*math.tau/24),139.65)) for j in range(24)]
    r1=[bm.verts.new((v.co.x,v.co.y,148.75)) for v in r0]
    bm.faces.new(tuple(reversed(r0)));bm.faces.new(tuple(r1))
    for j in range(24):bm.faces.new((r0[j],r0[(j+1)%24],r1[(j+1)%24],r1[j]))
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bmesh.ops.triangulate(bm,faces=bm.faces);bm.to_mesh(col.data);bm.free()
    flags=A.empty('BSXFlags:Atalaya',root);flags['BSXFlags_Name']='BSX';flags['BSXFlags_Value']='HAVOC | COMPLEX'
    path=ROOT/'addons/Atalaya/meshes/AstraAsedio/torre_atalaya_v21.nif';path.parent.mkdir(parents=True,exist_ok=True)
    A.select(obs+[root,col,flags],root)
    bpy.ops.export_scene.pynifly(filepath=str(path),target_game='SKYRIMSE',blender_xf=False,intuit_defaults=False,export_animations=False,preserve_hierarchy=True,export_modifiers=False,export_colors=True)
    lo,hi=nif_fisica.caja_visual(nif_nodos.leer(str(path)))
    receipt={'nif':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bbox':{'min':lo,'max':hi},'source':'source/Atalaya_v21.blend','parts':len(out['parts']),'collision_boxes':len(boxes),'entry':e,'supports':out['support_checks'],'stair_ground_max_overlap':out['stair_ground_max_overlap'],'game_tested':False,'source_geometry':'own generated parts and own v04 turntable; no vanilla geometry exported'}
    (ROOT/'reports/atalaya_build_v21.json').write_text(json.dumps(receipt,indent=2));print('ATALAYA_EXPORTED',path.stat().st_size,len(out['parts']),flush=True)
if __name__=='__main__':main()
