"""Compare original mechanism vertices with the final v01 NIF, in game units."""
import bpy, addon_utils, json, math
from pathlib import Path
from mathutils import Vector
from mathutils.kdtree import KDTree

ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/'config.json').read_text())
names=['Manivela_torno','Mango_torno','Rueda_trinquete','Una_trinquete','Muelle_una',
       'Palanca_gatillo','Eje_torno','Volante_torno','Cubo_volante']
addon_utils.enable('io_scene_nifly',default_set=True)
bpy.ops.wm.open_mainfile(filepath=CFG['source'],use_scripts=False)
bpy.context.scene.frame_set(1);bpy.context.view_layer.update()
dep=bpy.context.evaluated_depsgraph_get()
original={};points={}
for name in names:
    obj=bpy.data.objects[name];evaluated=obj.evaluated_get(dep);mesh=evaluated.to_mesh()
    pp=[obj.matrix_world@v.co for v in mesh.vertices]
    points[name]=[(v-Vector((0,0,6.65)))*70 for v in pp]
    original[name]={'bbox_world_m':{'min':[min(v[i] for v in pp) for i in range(3)],'max':[max(v[i] for v in pp) for i in range(3)]},
                    'matrix_world':[list(row) for row in obj.matrix_world],
                    'vertices':len(pp),'rotation_euler':list(obj.rotation_euler),'location':list(obj.location)}
    evaluated.to_mesh_clear()
for obj in list(bpy.data.objects):bpy.data.objects.remove(obj,do_unlink=True)
for action in list(bpy.data.actions):bpy.data.actions.remove(action)
bpy.context.view_layer.objects.active=None
bpy.ops.import_scene.pynifly(filepath=str(ROOT/'mod/meshes/AstraAsedio/ballesta.nif'),blender_xf=False,import_animations=False,import_collisions=False,create_bones=False)
bpy.context.scene.frame_set(1);bpy.context.view_layer.update()
vv=[obj.matrix_world@v.co for obj in bpy.data.objects if obj.type=='MESH' for v in obj.data.vertices]
tree=KDTree(len(vv))
for i,p in enumerate(vv):tree.insert(p,i)
tree.balance()
for name,pp in points.items():
    original[name]['max_source_vertex_distance_to_nif_units']=max(tree.find(p)[2] for p in pp)
report={'comparison':'v04 source rest pose -> exported v01 rest pose','parts':original}
(ROOT/'reports/mechanism_diagnosis.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
