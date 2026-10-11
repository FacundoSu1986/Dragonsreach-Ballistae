"""Hornea los dos clips del guardia con las MUNECAS a la altura nueva.

Es una copia de Ballesta_Astra_Animacion_Guardia_v01/scripts/build_guard.py
(sha256 5b5c3df84b85d1cbc60138e69b194392bfe03bd8eabc958c8a1aeb893adced43) con
los cambios MINIMOS que siguen. Todo lo demas -- la IK, el balanceo de
respiracion, el golpe del disparo, la postura de pies, el retargeting al
skeleton.hkx vanilla -- es identico, para que el resultado sea comparable con el
clip que ya funciona.

Por que hay que rehornear y no alcanza con bajar el NIF
------------------------------------------------------
build_guard.py:19-20 fija los objetivos de muneca en el espacio LOCAL de la
ballesta:

    LEFT_WRIST  = Vector(( 33.6, 143.8, 136.5))
    RIGHT_WRIST = Vector((-33.6, 143.8, 136.5))

y solve_arm() los alcanza con IK analitica de dos huesos. O sea: la altura de
las manos NO se deduce de la ballesta, esta ESCRITA en el clip. Bajando solo el
NIF, el guardia seguiria estirando los brazos 36 u mas arriba, hacia donde ya no
hay empunadura. Los dos clips tienen que bajar lo mismo que bajo el NIF.

Los cambios, uno por uno
------------------------
1. LEFT_WRIST / RIGHT_WRIST: z 136.5 -> 100.5  (delta = -36.0, la misma bajada
   del NIF). La x y la y NO cambian: medido en el NIF, las empunaduras se
   movieron con dx = 0 y dy = 0 exactos, solo en z.
2. ORIGEN: las entradas (rig NickNak, ballesta de referencia, skeleton de
   referencia) y el conversor HKX se leen del proyecto de animacion original en
   modo SOLO LECTURA. Ese proyecto no se toca: se verifico su sha256 antes y
   despues. El conversor ademas no se puede redistribuir, asi que se referencia
   en su lugar y nunca se copia a un paquete.
3. Las salidas (XML, HKX, .blend de autoria, informe) van a esta carpeta, no a
   la del proyecto original.
4. contact_points del informe: z 137.67 -> 101.67 (solo documentacion; la IK usa
   las munecas, que estan 1.17 u por debajo de la empunadura).
"""
import bpy
import math
import json
import sys
import subprocess
import hashlib
from pathlib import Path
from mathutils import Matrix, Vector, Quaternion

ROOT = Path(__file__).resolve().parents[1]
ORIGEN = Path(r"E:\Sectores\Sector_Modelado_3D"
              r"\Ballesta_Astra_Animacion_Guardia_v01")
sys.path.insert(0, str(ORIGEN / 'tools'))
from ixml import DocumentInterface, ReferenceFrame          # noqa: E402

FPS = 30
ACTOR_FOOT = Vector((0.0, 151.0, 0.0))
ACTOR_HEADING = math.pi
ACTOR_REST = Matrix.Translation(ACTOR_FOOT) @ Matrix.Rotation(ACTOR_HEADING, 4, 'Z')

# --- CAMBIO 1: la bajada de 36 u -------------------------------------------
BAJADA = 36.0
WRIST_Z_ANTES = 136.5
WRIST_Z = WRIST_Z_ANTES - BAJADA                          # 100.5
GRIP_Z_ANTES = 137.67
GRIP_Z = GRIP_Z_ANTES - BAJADA                            # 101.67
LEFT_WRIST = Vector((33.6, 143.8, WRIST_Z))
RIGHT_WRIST = Vector((-33.6, 143.8, WRIST_Z))


def rgba(hex_color):
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4)) + (1,)


def mat(name, color, metallic=0.0, roughness=0.6):
    m = bpy.data.materials.new(name)
    m.diffuse_color = rgba(color)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = rgba(color)
    p.inputs['Metallic'].default_value = metallic
    p.inputs['Roughness'].default_value = roughness
    return m


def all_curves(action):
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                yield from bag.fcurves


def pose_matrix(rotation, position):
    m = rotation.to_4x4()
    m.translation = position
    return m


def solve_arm(rig, side, wrist, hand_rotation, bend_hint, kind='arm'):
    prefix = 'NPC '+side+' '
    names = (['UpperArm ['+side+'Uar]', 'Forearm ['+side+'Lar]', 'Hand ['+side+'Hnd]']
             if kind == 'arm'
             else ['Thigh ['+side+'Thg]', 'Calf ['+side+'Clf]', 'Foot ['+side+'ft ]'])
    upper, fore, hand = (rig.pose.bones[prefix+n] for n in names)
    bpy.context.view_layer.update()
    shoulder = upper.matrix.translation.copy()
    upper_rest = fore.bone.head_local - upper.bone.head_local
    fore_rest = hand.bone.head_local - fore.bone.head_local
    a, b = upper_rest.length, fore_rest.length
    delta = wrist - shoulder
    distance = delta.length
    if not abs(a-b)+0.05 < distance < a+b-0.05:
        raise RuntimeError(f'{side}: wrist unreachable ({distance:.3f}, arm {a+b:.3f})')
    direction = delta.normalized()
    pole = bend_hint - direction*direction.dot(bend_hint)
    pole.normalize()
    along = (a*a-b*b+distance*distance)/(2*distance)
    radius = math.sqrt(max(0, a*a-along*along))
    elbow = shoulder + direction*along + pole*radius
    upper_q = upper_rest.normalized().rotation_difference((elbow-shoulder).normalized())
    fore_q = fore_rest.normalized().rotation_difference((wrist-elbow).normalized())
    upper.matrix = pose_matrix(upper_q.to_matrix() @ upper.bone.matrix_local.to_3x3(), shoulder)
    bpy.context.view_layer.update()
    fore.matrix = pose_matrix(fore_q.to_matrix() @ fore.bone.matrix_local.to_3x3(), elbow)
    bpy.context.view_layer.update()
    hand.matrix = pose_matrix(hand_rotation @ hand.bone.matrix_local.to_3x3(), wrist)
    bpy.context.view_layer.update()
    return {'reach_ratio': distance/(a+b),
            'wrist_error': (hand.matrix.translation-wrist).length}


def hand_alignment(rig, side, forward, thumb_side):
    wrist = rig.data.bones[f'NPC {side} Hand [{side}Hnd]'].head_local
    mid = rig.data.bones[f'NPC {side} Finger20 [{side}F20]'].head_local
    thumb = rig.data.bones[f'NPC {side} Finger00 [{side}F00]'].head_local
    y = (mid-wrist).normalized()
    x = thumb-wrist
    x = (x-y*y.dot(x)).normalized()
    z = x.cross(y).normalized()
    original = Matrix((x, y, z)).transposed()
    y2 = Vector(forward).normalized()
    x2 = Vector(thumb_side)
    x2 = (x2-y2*y2.dot(x2)).normalized()
    z2 = x2.cross(y2).normalized()
    return Matrix((x2, y2, z2)).transposed() @ original.inverted()


def animate_pose(rig, name, seconds, rest, hand_rotations):
    action = bpy.data.actions.new(name)
    action.use_fake_user = True
    rig.animation_data_create()
    rig.animation_data.action = action
    samples = []
    inv = ACTOR_REST.inverted()
    actor_rotation = ACTOR_REST.to_3x3().inverted()
    for frame in range(round(seconds*FPS)+1):
        t = frame/FPS
        bpy.context.scene.frame_set(frame)
        for pb in rig.pose.bones:
            pb.matrix_basis = Matrix.Identity(4)
        # Fixed stance: put both boots behind the raised turntable, on the deck.
        # A 3-unit static hip bend provides knee room without stretching legs.
        com = rig.pose.bones['NPC COM [COM ]']
        lowered = rest[com.name].copy()
        lowered.translation.z -= 3
        com.matrix = lowered
        bpy.context.view_layer.update()
        for side in ('L', 'R'):
            foot = rig.pose.bones[f'NPC {side} Foot [{side}ft ]']
            solve_arm(rig, side, rest[foot.name].translation+Vector((0, -12, 0)),
                      Matrix.Identity(3), Vector((0, 1, 0)), kind='leg')
        # Breathing is rotation-only; feet, COM and root do not move vertically.
        breath = 0.24*math.sin(t*math.tau/2) if name.endswith('operate') else 0.0
        impulse = 0.0
        if name.endswith('fire'):
            points = [(0, 0), (2/FPS, 1), (4/FPS, .7), (.2, .35), (.45, 0), (1, 0)]
            for (ta, va), (tb, vb) in zip(points, points[1:]):
                if ta <= t <= tb:
                    u = (t-ta)/(tb-ta)
                    u = u*u*(3-2*u)
                    impulse = va+(vb-va)*u
                    break
        # A slight forward lean and raised clavicles accommodate the real mount.
        spine = rig.pose.bones['NPC Spine2 [Spn2]']
        forward_q = Quaternion(Vector((1, 0, 0)), math.radians(-3.0+breath+1.1*impulse))
        spine.matrix = pose_matrix(forward_q.to_matrix() @ rest[spine.name].to_3x3(),
                                   rest[spine.name].translation-Vector((0, 0, 3)))
        bpy.context.view_layer.update()
        for side, sign in [('L', 1), ('R', -1)]:
            clav = rig.pose.bones[f'NPC {side} Clavicle [{side}Clv]']
            base = clav.matrix.copy()
            q = Quaternion(Vector((0, 1, 0)), math.radians(sign*18))
            clav.matrix = pose_matrix(q.to_matrix() @ base.to_3x3(), base.translation)
        bpy.context.view_layer.update()
        targets = {'L': inv @ LEFT_WRIST,
                   'R': inv @ (RIGHT_WRIST+Vector((0, -.75*impulse, -.8*impulse)))}
        reach = {}
        for side, sign in [('L', -1), ('R', 1)]:
            reach[side] = solve_arm(rig, side, targets[side], hand_rotations[side],
                                    Vector((sign, .10, -.60)))
            # Curl the four fingers around the handle; thumb closes from the side.
            for finger in range(5):
                for joint in range(3):
                    bname = f'NPC {side} Finger{finger}{joint} [{side}F{finger}{joint}]'
                    pb = rig.pose.bones.get(bname)
                    if pb is None:
                        continue
                    angle = ([18, 36, 32][joint] if finger == 0
                             else [40, 54, 42][joint])
                    if side == 'R' and finger == 1:
                        angle += 5*impulse
                    pb.rotation_mode = 'QUATERNION'
                    pb.rotation_quaternion = Quaternion(Vector((0, 0, 1)),
                                                        math.radians(sign*angle))
        bpy.context.view_layer.update()
        for pb in rig.pose.bones:
            pb.rotation_mode = 'QUATERNION'
            pb.keyframe_insert(data_path='location', frame=frame, group=pb.name)
            pb.keyframe_insert(data_path='rotation_quaternion', frame=frame, group=pb.name)
            # No stretch: explicitly remove tiny numeric errors from decomposition.
            if max(abs(v-1) for v in pb.scale) > .001:
                raise RuntimeError(f'Non-rigid scale in {pb.name}: {tuple(pb.scale)}')
            pb.scale = (1, 1, 1)
            pb.keyframe_insert(data_path='scale', frame=frame, group=pb.name)
        samples.append({'frame': frame, 'reach': reach, 'trigger_pull': impulse})
    for curve in all_curves(action):
        for key in curve.keyframe_points:
            key.interpolation = 'LINEAR'
    if name.endswith('fire'):
        marker = action.pose_markers.new('AstraGuardReleaseVisual')
        marker.frame = 2
    return action, samples


def export_clip(rig, action, frames, rest, skeleton):
    rig.animation_data.action = action
    doc = DocumentInterface.create()
    doc.set_frames(frames)
    doc.set_framerate(FPS)
    doc.set_additive(False)
    anim = doc.add_animation('0')
    anim.set_skeleton_name('skeleton.hkx')
    anim.set_reference_frame(ReferenceFrame.OBJECT)
    tracks = {b['name']: anim.add_transform_track(b['name']) for b in skeleton['bones']}
    # Use per-bone reference frames; NickNak rest axes differ from the HKX axes.
    corrections = {b['name']: rest[b['name']].inverted() @ Matrix(b['object_matrix'])
                   for b in skeleton['bones'] if b['name'] in rest}
    for frame in range(frames):
        bpy.context.scene.frame_set(frame)
        bpy.context.view_layer.update()
        for bone in skeleton['bones']:
            n = bone['name']
            if n in corrections:
                matrix = rig.pose.bones[n].matrix @ corrections[n]
            else:
                matrix = Matrix(bone['object_matrix'])
            loc, rotation, scale = matrix.decompose()
            tracks[n].add_key(frame).set_value(loc, rotation, Vector((1, 1, 1)))
    if action.name.endswith('fire'):
        # Converter annotations are one-based sample indices, not seconds.
        anim.add_annotation(3, 'AstraGuardReleaseVisual')
    xml_path = ROOT/'animations'/f'{action.name}.xml'
    hkx_path = xml_path.with_suffix('.hkx')
    doc.save(str(xml_path))
    exe = str(ORIGEN/'tools/blender-hkx.exe')
    skeleton_hkx = str(ORIGEN/'tools/skeleton.hkx')
    command = [exe, 'pack', '30', 'AMD64', str(xml_path), str(hkx_path), skeleton_hkx]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        # The bundled converter predates the addon's new FPS command argument.
        command = [exe, 'pack', 'AMD64', str(xml_path), str(hkx_path), skeleton_hkx]
        result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode or not hkx_path.is_file() or hkx_path.stat().st_size < 1000:
        raise RuntimeError('HKX conversion failed: '+result.stdout+result.stderr)
    return {'file': hkx_path.name,
            'sha256': hashlib.sha256(hkx_path.read_bytes()).hexdigest(),
            'frames': frames, 'duration': (frames-1)/FPS,
            'converter_command': command,
            'converter_output': result.stdout+result.stderr}


def main():
    rig_file = ORIGEN/'inputs/nicknak/Blender Rigs/NickNak Rig 5.blend'
    bpy.ops.wm.open_mainfile(filepath=str(rig_file), use_scripts=False)
    rig = bpy.data.objects['Deform Rig']
    keep = {'Deform Rig', 'MinerClothes', 'MaleUnderwearBody:0', 'MaleHeadIMF',
            'HandMaleBig3rd', 'merchantboots'}
    for obj in list(bpy.data.objects):
        if obj.name not in keep:
            bpy.data.objects.remove(obj, do_unlink=True)
    collection = bpy.data.collections.new('Astra · Guardia')
    bpy.context.scene.collection.children.link(collection)
    for o in list(bpy.data.objects):
        for c in list(o.users_collection):
            c.objects.unlink(o)
        collection.objects.link(o)
        o.hide_viewport = False
        o.hide_render = False
        o.hide_set(False)
        o.animation_data_clear()
        if o.type == 'MESH' and o.data.shape_keys:
            o.data.shape_keys.animation_data_clear()
    rig.animation_data_clear()
    for pb in rig.pose.bones:
        for c in list(pb.constraints):
            pb.constraints.remove(c)
        pb.matrix_basis = Matrix.Identity(4)
        pb.bone.hide = False
        pb.custom_shape = None
    # Embedded rig UI scripts are not needed by the baked editable actions.
    for t in list(bpy.data.texts):
        bpy.data.texts.remove(t)
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.render.fps_base = 1
    scene.unit_settings.system = 'NONE'
    rest = {b.name: b.matrix_local.copy() for b in rig.data.bones}
    actor_inv_rotation = ACTOR_REST.to_3x3().inverted()
    hand_rotations = {
        'L': hand_alignment(rig, 'L', actor_inv_rotation@Vector((0, -1, 0)),
                            actor_inv_rotation@Vector((1, 0, 0))),
        'R': hand_alignment(rig, 'R', actor_inv_rotation@Vector((0, -1, 0)),
                            actor_inv_rotation@Vector((-1, 0, 0)))}
    actions, samples = {}, {}
    for name, duration in [('astra_guard_operate', 2), ('astra_guard_fire', 1)]:
        action, sample = animate_pose(rig, name, duration, rest, hand_rotations)
        actions[name], samples[name] = action, sample
    skeleton = json.loads((ORIGEN/'reports/vanilla_skeleton_reference.json').read_text())
    receipts = [export_clip(rig, actions[n], count, rest, skeleton)
                for n, count in [('astra_guard_operate', 61), ('astra_guard_fire', 31)]]
    # Reference meshes stay in their own collection and never enter HKX exports.
    with bpy.data.libraries.load(str(ORIGEN/'inputs/ballesta_reference.blend'),
                                 link=False) as (src, dst):
        dst.objects = list(src.objects)
    gun_collection = bpy.data.collections.new('Astra · Ballesta de referencia')
    scene.collection.children.link(gun_collection)
    for o in dst.objects:
        if o:
            gun_collection.objects.link(o)
            o.animation_data_clear()
            o.hide_set(False)
            o.hide_render = False
    aim = bpy.data.objects['CTRL_GIRO_360']
    pitch = bpy.data.objects['CTRL_ELEVACION']
    aim.rotation_euler = (0, 0, 0)
    pitch.rotation_euler = (0, 0, 0)
    # Rig/meshes are actor-relative. This empty models the controller's world pose.
    placement = bpy.data.objects.new('Preview_OperatorPlacement', None)
    scene.collection.objects.link(placement)
    placement.matrix_world = ACTOR_REST
    for o in list(collection.objects):
        local = o.matrix_world.copy()
        o.parent = placement
        o.matrix_parent_inverse = Matrix.Identity(4)
        o.matrix_basis = local
    rig['animation_coordinate_frame'] = 'Actor local; +Y forward; no root motion'
    rig['reference_pose_alignment'] = 'NickNak delta retargeted to vanilla skeleton.hkx'
    rig.show_in_front = True
    mats = {'skin': mat('Guardia · piel', '#a57c60'),
            'cloth': mat('Guardia · cuero', '#4b3430'),
            'steel': mat('Guardia · acero', '#5e6e76', .7, .4),
            'wood': mat('Ballesta · madera', '#805534'),
            'metal': mat('Ballesta · herrajes', '#39494c', .65, .4),
            'rope': mat('Ballesta · cuerda', '#b89967'),
            'bolt': mat('Ballesta · virote', '#a18b63')}
    for o in collection.objects:
        if o.type != 'MESH':
            continue
        color = ('skin' if o.name in ('MaleHeadIMF', 'HandMaleBig3rd',
                                      'MaleUnderwearBody:0') else 'cloth')
        o.data.materials.clear()
        o.data.materials.append(mats[color])
    for o in gun_collection.objects:
        if o.type == 'MESH':
            suffix = o.name.rsplit('_', 1)[-1]
            color = suffix if suffix in ('wood', 'rope', 'bolt') else 'metal'
            if suffix == 'floor':
                color = 'wood'
            o.data.materials.clear()
            o.data.materials.append(mats[color])
    rig.animation_data.action = actions['astra_guard_operate']
    scene.frame_start, scene.frame_end = 0, 60
    scene.frame_set(0)
    bpy.context.view_layer.update()
    for o in bpy.context.selected_objects:
        o.select_set(False)
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    (ROOT/'source').mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'source/astra_guard_bajada.blend'))

    # La razon ergonomica del cambio, medida sobre la muestra horneada.
    peor = 0.0
    for name, sample in samples.items():
        for s in sample:
            for lado in ('L', 'R'):
                peor = max(peor, s['reach'][lado]['wrist_error'])
    ratios = [s['reach'][l]['reach_ratio'] for s in samples['astra_guard_operate']
              for l in ('L', 'R')]
    report = {
        'blender': bpy.app.version_string,
        'skeleton': str(ORIGEN/'tools/skeleton.hkx'),
        'base_script': str(ORIGEN/'scripts/build_guard.py'),
        'cambio': {
            'motivo': 'bajar la ballesta 36 u para que el guardia no suba los '
                      'brazos por encima del hombro',
            'bajada_u': BAJADA,
            'muneca_z_antes': WRIST_Z_ANTES, 'muneca_z_despues': WRIST_Z,
            'empunadura_z_antes': GRIP_Z_ANTES, 'empunadura_z_despues': GRIP_Z,
            'hombro_z_guardia': 107.087,
            'muneca_menos_hombro_u': round(WRIST_Z - 107.087, 3),
        },
        'actor_foot_gun_local_units': list(ACTOR_FOOT),
        'actor_heading_radians': ACTOR_HEADING,
        'yaw_limits_degrees': [-60, 60], 'fixed_pitch_degrees': 0,
        'fixed_stance': {'hip_lower_units': 3, 'feet_gun_local_y_offset_units': 12},
        'contact_points': {'support_grip': [33.6, 137.9, GRIP_Z],
                           'fire_grip': [-33.6, 137.9, GRIP_Z]},
        'wrists': {'L': list(LEFT_WRIST), 'R': list(RIGHT_WRIST)},
        'release_seconds': 2/FPS, 'release_marker': 'AstraGuardReleaseVisual',
        'clips': receipts, 'samples': samples, 'runtime_integrated': False,
        'verificacion': {
            'peor_error_de_muneca_u': round(peor, 6),
            'alcance_min_pct': round(100*min(ratios), 1),
            'alcance_max_pct': round(100*max(ratios), 1),
        },
    }
    (ROOT/'reports').mkdir(parents=True, exist_ok=True)
    (ROOT/'reports/authoring_bajada.json').write_text(json.dumps(report, indent=2))
    print('GUARD_BUILT_BAJADA', json.dumps(receipts))
    print('VERIFICACION', json.dumps(report['verificacion']))


if __name__ == '__main__':
    main()
