"""Measure the existing NIF's moving envelope at upward aim angles, read-only."""
from pathlib import Path
import json, math, hashlib
import bpy, addon_utils
from mathutils import Matrix, Vector
ROOT=Path(__file__).resolve().parents[1]
addon_utils.enable('io_scene_nifly',default_set=True)
for obj in list(bpy.data.objects): bpy.data.objects.remove(obj,do_unlink=True)
path=ROOT/'mod/meshes/AstraAsedio/ballesta.nif'
cfg=json.loads((ROOT/'config.json').read_text())
bpy.ops.import_scene.pynifly(filepath=str(path),blender_xf=False,import_animations=False,import_collisions=False,create_bones=False)
node=bpy.data.objects['CTRL_ELEVACION']
base=node.matrix_local.copy()
moving=[]
for obj in bpy.data.objects:
    parent=obj.parent
    while parent and parent!=node: parent=parent.parent
    if parent==node and obj.type=='MESH':moving.append(obj)
samples=[]
muzzle=bpy.data.objects['ProjectileNode']
for pitch in (-5,0,35,45,60,70,75,80):
    pose=Matrix.Rotation(math.radians(-pitch),4,'X')@base
    pose.translation=base.translation
    node.matrix_local=pose
    bpy.context.view_layer.update()
    values=[(obj.name,obj.matrix_world@vert.co) for obj in moving for vert in obj.data.vertices]
    lowest=min(values,key=lambda value:value[1].z)
    c=math.cos(math.radians(pitch));s=math.sin(math.radians(pitch))
    expected=Vector((0,-224*c+19.6*s,cfg['pitch_pivot_units']+224*s+19.6*c))
    direction=muzzle.matrix_world.to_3x3()@Vector((0,1,0))
    error=(muzzle.matrix_world.translation-expected).length
    dot=direction.dot(Vector((0,-c,s)))
    if error>.01 or dot<.99999:raise RuntimeError('Muzzle transform does not match requested elevation')
    samples.append({'pitch':pitch,'moving_min_z_relative_to_roof':lowest[1].z,'lowest_shape':lowest[0],'muzzle_position_error':error,'muzzle_direction_dot':dot})
node.matrix_local=base
floor=json.loads((ROOT/'reports/collision_walkable.json').read_text())['walkable_disk_units']['top_z']-cfg['tower_top_units']
report={'nif_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'samples':samples,'source_read_only':True,'geometry_modified':False,'sample_height_reference':'ballista root/base, conservatively above the real floor','floor_relative_z':floor,'floor_minimum_clearance':min(value['moving_min_z_relative_to_roof'] for value in samples)-floor,'muzzle_transforms_verified':True}
(ROOT/'reports/elevation_diagnosis.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
