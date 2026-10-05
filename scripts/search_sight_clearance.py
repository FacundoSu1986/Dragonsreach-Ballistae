"""Find camera offsets that clear fixed and moving geometry at all eight pitches."""
from pathlib import Path
import bpy,addon_utils,json,math
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
addon_utils.enable('io_scene_nifly',default_set=True)
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.import_scene.pynifly(filepath=str(ROOT/'mod/meshes/AstraAsedio/ballesta.nif'),blender_xf=False,import_animations=False,import_collisions=False,create_bones=False)
pitch=bpy.data.objects['CTRL_ELEVACION'];base=pitch.matrix_local.copy()
meshes=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith('bhk')]
candidates={(y,z):{'local':[0,y,z],'min_mesh':1e10,'min_floor':1e10,'hits':0} for y in range(80,151,5) for z in range(32,73,4)}
for elevation in (-5,0,35,45,60,70,75,80):
    pose=Matrix.Rotation(math.radians(-elevation),4,'X')@base;pose.translation=base.translation;pitch.matrix_local=pose;bpy.context.view_layer.update()
    trees=[]
    for o in meshes:
        o.data.calc_loop_triangles()
        trees.append(BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True))
    forward=(pitch.matrix_world.to_3x3()@Vector((0,-1,0))).normalized()
    for (y,z),row in candidates.items():
        eye=pitch.matrix_world@Vector((0,y,z))
        row['min_floor']=min(row['min_floor'],eye.z+2.8)
        for tree in trees:
            row['min_mesh']=min(row['min_mesh'],tree.find_nearest(eye)[3])
            if tree.ray_cast(eye,forward,3000)[0] is not None:row['hits']+=1
valid=[r for r in candidates.values() if r['min_mesh']>15 and r['min_floor']>10 and r['hits']==0]
valid.sort(key=lambda r:(r['local'][2],-r['min_mesh'],r['local'][1]))
(ROOT/'reports/sight_clearance_search.json').write_text(json.dumps({'scope':'Rest mesh/floor probes, not engine camera visibility','valid':valid,'all_candidates':list(candidates.values())},indent=2))
print(json.dumps(valid[:12],indent=2))
