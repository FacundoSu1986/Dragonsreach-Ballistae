"""Check fitted binding paths against reimported final NIF wood, metal and rope."""
import bpy,addon_utils,json,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
addon_utils.enable('io_scene_nifly',default_set=True)
for obj in list(bpy.data.objects):bpy.data.objects.remove(obj,do_unlink=True)
bpy.context.view_layer.objects.active=None
path=ROOT/'mod/meshes/AstraAsedio/ballesta.nif'
bpy.ops.import_scene.pynifly(filepath=str(path),blender_xf=False,import_animations=False,import_collisions=False,create_bones=False)
bpy.context.view_layer.update()
def surface(parent,rope):
    objs=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(parent+'_') and ('rope' in o.name)==rope]
    if not objs:raise RuntimeError('Missing reimported limb shapes: '+parent+' rope='+str(rope))
    vertices=[];triangles=[]
    for obj in objs:
        off=len(vertices);vertices.extend(obj.matrix_world@v.co for v in obj.data.vertices)
        obj.data.calc_loop_triangles();triangles.extend(tuple(off+i for i in t.vertices) for t in obj.data.loop_triangles)
    return BVHTree.FromPolygons(vertices,triangles,all_triangles=True),[o.name for o in objs]
revision=json.loads((ROOT/'reports/limb_ties_revision.json').read_text())
lift=Vector((0,0,json.loads((ROOT/'config.json').read_text()).get('mount_raise_units',0.0)))
results=[]
for part in revision['parts']:
    wood,names=surface(part['parent'],False);rope,rope_names=surface(part['parent'],True)
    frame=Matrix(part['source_world_frame'])
    centers=[(frame@Vector(p)-Vector((0,0,6.65)))*70+lift for p in part['path_local']]
    gaps=[wood.find_nearest(p)[3]-revision['rope_radius_m']*70 for p in centers]
    tube_dist=[rope.find_nearest(p)[3] for p in centers]
    if min(gaps)<0 or max(gaps)>0.15:raise RuntimeError('Final binding loose or penetrating: '+part['name'])
    if min(tube_dist)<0.3 or max(tube_dist)>1.05:raise RuntimeError('Fitted path not covered by exported rope: '+part['name'])
    results.append({'name':part['name'],'parent':part['parent'],'samples':len(centers),'limb_shapes':names,'rope_shapes':rope_names,
                    'clearance_min_units':min(gaps),'clearance_max_units':max(gaps),'center_to_rope_surface_min_units':min(tube_dist),
                    'center_to_rope_surface_max_units':max(tube_dist)})
report={'ok':True,'in_game_verified':False,'nif_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'parts':results,'both_limbs_verified':True,'binding_count':len(results),'clearance_tolerance_units':0.15}
(ROOT/'reports/limb_ties_verified.json').write_text(json.dumps(report,indent=2))
print('ASTRA_BINDINGS_REIMPORTED_OK',len(results),max(r['clearance_max_units'] for r in results))
