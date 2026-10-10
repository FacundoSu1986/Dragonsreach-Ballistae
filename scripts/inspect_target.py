import bpy, addon_utils, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/'config.json').read_text())
addon_utils.enable('io_scene_nifly',default_set=True)
report={}
for name in ('archerytarget01','archerytargettripod01'):
    for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
    bpy.context.view_layer.objects.active=None
    bpy.ops.import_scene.pynifly(filepath=str(Path(CFG['extracted'])/'meshes/clutter/common'/f'{name}.nif'),blender_xf=False,import_animations=False,import_collisions=False,create_bones=False)
    bpy.context.view_layer.update()
    rows=[]
    for o in bpy.data.objects:
        if o.type!='MESH':continue
        o.data.calc_loop_triangles()
        for p in sorted(o.data.polygons,key=lambda p:p.area,reverse=True)[:12]:
            norm=o.matrix_world.to_3x3()@p.normal;center=o.matrix_world@p.center
            rows.append({'shape':o.name,'area':p.area,'normal':list(norm),'center':list(center),
                         'diffuse':o.data.materials[p.material_index].get('BSShaderTextureSet_Diffuse')})
    report[name]=rows
(ROOT/'reports/target_facing.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
