import bpy, addon_utils, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
C=json.loads((ROOT/'config.json').read_text())
addon_utils.enable('io_scene_nifly',default_set=True)
for o in list(bpy.data.objects): bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.import_scene.pynifly(filepath=str(Path(C['extracted'])/'meshes/dlc01/weapons/crossbow/BoltProjectile.nif'),blender_xf=False,import_animations=False,create_bones=False)
report=[]
for o in bpy.data.objects:
    record={'name':o.name,'type':o.type,'parent':o.parent.name if o.parent else None,'matrix':[list(row) for row in o.matrix_world],'props':{k:str(v) for k,v in o.items()}}
    if o.rigid_body: record['rigidbody']={k:getattr(o.rigid_body,k) for k in ('mass','type','collision_shape','friction','restitution','linear_damping','angular_damping','collision_margin')}
    if o.type=='MESH': record['bounds']=[list(v) for v in o.bound_box]
    report.append(record)
(ROOT/'reports/projectile_donor.json').write_text(json.dumps(report,indent=2))
print(json.dumps([r for r in report if 'rigidbody' in r],indent=2))
