"""Read-only camera placement probe against the reimported final meshes."""
from pathlib import Path
import bpy, addon_utils, json, hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[1]
addon_utils.enable('io_scene_nifly',default_set=True)
for o in list(bpy.data.objects): bpy.data.objects.remove(o,do_unlink=True)
path=ROOT/'mod/meshes/AstraAsedio/ballesta.nif'
bpy.ops.import_scene.pynifly(filepath=str(path),blender_xf=False,import_animations=False,import_collisions=False,create_bones=False)
bpy.context.view_layer.update()
pitch=bpy.data.objects['CTRL_ELEVACION']
meshes=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith('bhk')]
trees=[]
for o in meshes:
    o.data.calc_loop_triangles()
    verts=[o.matrix_world@v.co for v in o.data.vertices]
    trees.append((o.name,BVHTree.FromPolygons(verts,[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)))
rows=[]
for y in (95,110,125,145):
    for z in (32,40,48):
        p=pitch.matrix_world@Vector((0,y,z))
        nearest=min((tree.find_nearest(p)[3],name) for name,tree in trees)
        hits=[]
        for name,tree in trees:
            hit=tree.ray_cast(p,Vector((0,-1,0)),3000)
            if hit[0] is not None: hits.append((hit[3],name))
        rows.append({'local':[0,y,z],'nearest_mesh_units':nearest[0],'nearest_mesh':nearest[1],'centre_ray_hits':sorted(hits)})
report={'nif_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'read_only':True,'rest_candidates':rows,'limits':'Ray/distance probes do not prove visibility, near-plane, or inside/outside classification in Skyrim.'}
(ROOT/'reports/sight_candidates.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
