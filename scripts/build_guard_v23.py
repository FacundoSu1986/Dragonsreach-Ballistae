"""Author v23 contact poses and synchronized short steps with Blender 5.2.

External NickNak rig, reference skeleton and converter are read in place.
Only own animation outputs are copied to source/anim. No tool/rig redistribution.
"""
import bpy
import hashlib
import json
import math
import shutil
import sys
from pathlib import Path
from mathutils import Matrix, Quaternion, Vector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import build_guard_bajada as B

STAGE = ROOT/'build/guard-v23'
STEP_SECONDS = .8
STEP_DEGREES = 12.
SAMPLES = {}
original_animate = B.animate_pose


def material(name, color, metallic=0., roughness=.6):
    value = B.rgba(color)
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = value
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    shader = nodes.new('ShaderNodeBsdfPrincipled')
    output = nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(shader.outputs['BSDF'],output.inputs['Surface'])
    shader.inputs['Base Color'].default_value = value
    shader.inputs['Metallic'].default_value = metallic
    shader.inputs['Roughness'].default_value = roughness
    return mat


def smooth(t):
    t = max(0., min(1., t))
    return t*t*(3.-2.*t)


def animate(rig, name, seconds, rest, hand_rotations):
    action, samples = original_animate(rig, name, seconds, rest, hand_rotations)
    inv = B.ACTOR_REST.inverted()
    turning = name.endswith(('turn_left', 'turn_right'))
    sign = 1 if name.endswith('turn_left') else -1
    delta = math.radians(sign*STEP_DEGREES)
    endpoint = Matrix.Rotation(delta, 4, 'Z') @ B.ACTOR_REST
    lead = 'L' if sign > 0 else 'R'
    feet = {s: rest[f'NPC {s} Foot [{s}ft ]'].translation + Vector((0,-12,0))
            for s in ('L','R')}
    for frame, sample in enumerate(samples):
        bpy.context.scene.frame_set(frame)
        bpy.context.view_layer.update()
        if turning:
            u = frame/(seconds*B.FPS)
            com = rig.pose.bones['NPC COM [COM ]']
            matrix = com.matrix.copy()
            matrix.translation.z -= 2*math.sin(math.pi*u)
            com.matrix = matrix
            bpy.context.view_layer.update()
        # Less clavicle elevation: wrists sit below shoulders on the low gun.
        for side, side_sign in (('L',1),('R',-1)):
            clav = rig.pose.bones[f'NPC {side} Clavicle [{side}Clv]']
            base = clav.matrix.copy()
            q = Quaternion(Vector((0,1,0)), math.radians(side_sign*(4-18)))
            clav.matrix = B.pose_matrix(q.to_matrix() @ base.to_3x3(), base.translation)
        bpy.context.view_layer.update()
        impulse = sample['trigger_pull']
        targets = {'L': inv @ B.LEFT_WRIST,
                   'R': inv @ (B.RIGHT_WRIST+Vector((0,-.75*impulse,-.8*impulse)))}
        for side, pole_sign in (('L',-1),('R',1)):
            sample['reach'][side] = B.solve_arm(rig, side, targets[side],
                hand_rotations[side], Vector((pole_sign,.10,-.60)))
        sample['feet'] = {}
        if turning:
            u = frame/(seconds*B.FPS)
            placement = Matrix.Rotation(delta*u,4,'Z') @ B.ACTOR_REST
            sample['yaw_fraction'] = u
            for side in ('L','R'):
                phase = 2*u if side == lead else 2*u-1
                blend = smooth(phase)
                lift = 4.*math.sin(math.pi*phase) if 0 < phase < 1 else 0.
                start, end = B.ACTOR_REST @ feet[side], endpoint @ feet[side]
                world = start.lerp(end,blend) + Vector((0,0,lift))
                local = placement.inverted() @ world
                # Bone orientation stays fixed in world during planted phases.
                rotation = Matrix.Rotation(delta*(blend-u),3,'Z')
                reach = B.solve_arm(rig, side, local, rotation,
                                    Vector((0,1,0)),kind='leg')
                actual = placement @ rig.pose.bones[f'NPC {side} Foot [{side}ft ]'].matrix.translation
                sample['feet'][side] = {'world':list(actual),'expected_world':list(world),
                    'planted': phase <= 0 or phase >= 1,
                    'position_error':(actual-world).length,'reach_ratio':reach['reach_ratio']}
        for pb in rig.pose.bones:
            for field in ('location','rotation_quaternion','scale'):
                pb.keyframe_insert(data_path=field,frame=frame,group=pb.name)
        bpy.context.view_layer.update()
    for curve in B.all_curves(action):
        for key in curve.keyframe_points:
            key.interpolation = 'LINEAR'
    SAMPLES[name] = samples
    return action, samples


def lower_reference():
    # Same transform and pedestal affinity as the canonical byte-patched NIF.
    aim = bpy.data.objects['CTRL_GIRO_360']
    aim.location.z -= 36.
    k = (137.6-20.-36.)/(137.6-20.)
    for name in ('AstraBallesta_floor','AstraBallesta_metal','AstraBallesta_wood'):
        obj = bpy.data.objects.get(name)
        if obj is None or obj.type != 'MESH':
            raise RuntimeError('Missing canonical reference pedestal '+name)
        world = obj.matrix_world.copy()
        inv = world.inverted()
        for vertex in obj.data.vertices:
            point = world @ vertex.co
            if point.z > 20:
                point.z = 20 + (point.z-20)*k
                vertex.co = inv @ point
        obj.data.update()
    bpy.context.view_layer.update()


def platform_reference():
    from platforms_v15_geometry import site
    site_data = site('este')
    offset = Vector(site_data['gun_local_pos'])
    material = B.mat('Plataforma Astra v23','#574534')
    for box in site_data['collision_boxes']:
        lo, hi = Vector(box['lo'])-offset, Vector(box['hi'])-offset
        bpy.ops.mesh.primitive_cube_add(size=1,location=(lo+hi)/2)
        obj = bpy.context.object
        obj.name = 'Preview_Platform_'+box['name']
        obj.scale = hi-lo
        obj.data.materials.append(material)


def main():
    if bpy.app.version[:3] != (5,2,2):
        raise RuntimeError('Authoring requires the configured Blender5.2.2')
    for folder in ('animations','source','reports'):
        (STAGE/folder).mkdir(parents=True,exist_ok=True)
    B.ROOT = STAGE
    B.animate_pose = animate
    B.mat = material
    B.main()
    rig = bpy.data.objects['Deform Rig']
    rest = {bone.name:bone.matrix_local.copy() for bone in rig.data.bones}
    rotation = B.ACTOR_REST.to_3x3().inverted()
    hand_rotations = {s:B.hand_alignment(rig,s,rotation@Vector((0,-1,0)),
        rotation@Vector((1 if s=='L' else -1,0,0))) for s in ('L','R')}
    skeleton = json.loads((B.ORIGEN/'reports/vanilla_skeleton_reference.json').read_text())
    receipts = json.loads((STAGE/'reports/authoring_bajada.json').read_text())['clips']
    for side in ('left','right'):
        action, _ = animate(rig,'astra_guard_turn_'+side,STEP_SECONDS,rest,hand_rotations)
        receipts.append(B.export_clip(rig,action,25,rest,skeleton))
    destination = ROOT/'source/anim'
    destination.mkdir(parents=True,exist_ok=True)
    for receipt in receipts:
        shutil.copy2(STAGE/'animations'/receipt['file'],destination/receipt['file'])
    lower_reference()
    platform_reference()
    rig.animation_data.action = bpy.data.actions['astra_guard_operate']
    scene = bpy.context.scene
    scene.frame_start, scene.frame_end = 0,60
    scene.frame_set(0)
    scene['v23_turn_seconds'] = STEP_SECONDS
    scene['v23_turn_degrees'] = STEP_DEGREES
    scene['v23_yaw_fraction'] = 'linear normalized clip local time'
    source = ROOT/'source/astra_guard_v23.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(source))
    report = {'success':True,'blender':bpy.app.version_string,
        'source':str(source.relative_to(ROOT)),
        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'root_motion':False,'scale':1,'pitch':0,'yaw_limits':[-60,60],
        'clavicle_raise_degrees':4,'wrists_gun_local_z':100.5,
        'operator_foot_gun_local':[0,151,0],'turn_seconds':STEP_SECONDS,
        'turn_degrees':STEP_DEGREES,'yaw_fraction':'linear',
        'turn_lift_units':4,'release_seconds':2/30,'clips':receipts,'samples':SAMPLES,
        'turn_hip_lower_max_units':2,
        'game_tested':False}
    max_error = max(s['reach'][side]['wrist_error'] for v in SAMPLES.values()
                    for s in v for side in ('L','R'))
    max_foot = max(f['position_error'] for v in SAMPLES.values()
                   for s in v for f in s['feet'].values())
    assert max_error < .01 and max_foot < .01, (max_error,max_foot)
    report['max_wrist_error_units'], report['max_step_foot_error_units'] = max_error,max_foot
    (ROOT/'reports/authoring_v23.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('GUARD_V23_AUTHORED',max_error,max_foot)


if __name__ == '__main__':
    main()
