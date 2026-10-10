"""Inspect the exported sight anchor in reimported poses, never the source model."""
from pathlib import Path
import bpy,addon_utils,json,hashlib,math
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[1]
addon_utils.enable('io_scene_nifly',default_set=True)
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
path=ROOT/'mod/meshes/AstraAsedio/ballesta.nif'
bpy.ops.import_scene.pynifly(filepath=str(path),blender_xf=False,import_animations=False,import_collisions=False,create_bones=False)
pitch=bpy.data.objects['CTRL_ELEVACION'];root=pitch.parent.parent
camera=bpy.data.objects['AstraSightCameraNode'];projectile=bpy.data.objects['ProjectileNode']
assert camera.parent==pitch
base=pitch.matrix_local.copy()
floor=json.loads((ROOT/'reports/collision_walkable.json').read_text())['walkable_disk_units']['top_z']-json.loads((ROOT/'config.json').read_text())['tower_top_units']
# v10: the anchor is the rear sight centre (the ring surrounds it by design); the tail camera itself is
# checked by verify_sight_path.py. Exclude the iron-sight meshes from this anchor clearance.
meshes=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith('bhk') and 'alza' not in o.name and 'guion' not in o.name]
poses=[]
for root_yaw in (0,47,180):
    root.rotation_euler.z=math.radians(root_yaw)
    for elevation in (-5,0,35,45,60,70,75,80):
        pose=Matrix.Rotation(math.radians(-elevation),4,'X')@base
        pose.translation=base.translation;pitch.matrix_local=pose
        bpy.context.view_layer.update()
        eye=camera.matrix_world.translation.copy()
        forward=(camera.matrix_world.to_3x3()@Vector((0,1,0))).normalized()
        muzzle_forward=(projectile.matrix_world.to_3x3()@Vector((0,1,0))).normalized()
        nearest=[];hits=[]
        for o in meshes:
            o.data.calc_loop_triangles()
            tree=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
            nearest.append(tree.find_nearest(eye)[3])
            hit=tree.ray_cast(eye,forward,3000)
            if hit[0] is not None:hits.append({'shape':o.name,'distance':hit[3]})
        local_eye=root.matrix_world.inverted()@eye
        row={'root_yaw':root_yaw,'pitch':elevation,'world_eye':list(eye),'logical_forward':list(forward),'muzzle_forward_dot':forward.dot(muzzle_forward),'floor_clearance_root_local':local_eye.z-floor,'nearest_mesh_distance':min(nearest),'centre_ray_hits':hits}
        assert not hits,row
        assert row['muzzle_forward_dot']>.99999,row
        assert row['floor_clearance_root_local']>5,row
        assert row['nearest_mesh_distance']>10,row
        poses.append(row)
report={'ok':True,'nif_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'poses':poses,'minimum_floor_clearance':min(p['floor_clearance_root_local'] for p in poses),'minimum_mesh_distance':min(p['nearest_mesh_distance'] for p in poses),'minimum_direction_dot':min(p['muzzle_forward_dot'] for p in poses),'local_position_units':list(camera.location),'logical_basis':'NIF +Y forward and +Z up; native adapter handles FP convention.','in_game_camera_verified':False,'scope':'Rest-pose ballesta meshes and floor plane; not camera near-plane, frame composition, full animation, operator or scene visibility in Skyrim.'}
(ROOT/'reports/sight_anchor_verified.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='poses'},indent=2))
