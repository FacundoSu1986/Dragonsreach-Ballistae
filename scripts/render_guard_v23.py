"""Render authored v23 geometry/actions; preview is not a Skyrim test."""
import bpy
import math
import sys
from pathlib import Path
from mathutils import Vector, Matrix

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'previews/v23'
OUT.mkdir(parents=True,exist_ok=True)
args = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
MODE = args[0] if args else 'poses'
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'source/astra_guard_v23.blend'),use_scripts=False)
scene = bpy.context.scene
rig = bpy.data.objects['Deform Rig']
placement = bpy.data.objects['Preview_OperatorPlacement']
aim = bpy.data.objects['CTRL_GIRO_360']
actor_rest = Matrix.Translation((0,151,0))@Matrix.Rotation(math.pi,4,'Z')

world = bpy.data.worlds.new('Preview studio')
nodes = world.node_tree.nodes
bg = nodes.new('ShaderNodeBackground')
bg.inputs['Color'].default_value = (.045,.060,.075,1)
bg.inputs['Strength'].default_value = .65
output = nodes.new('ShaderNodeOutputWorld')
world.node_tree.links.new(bg.outputs['Background'],output.inputs['Surface'])
scene.world = world
scene.render.engine = 'CYCLES'
scene.cycles.samples = 12
scene.cycles.use_denoising = True
scene.render.resolution_x,scene.render.resolution_y = 960,600
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.view_settings.view_transform = 'AgX'


def light(name,pos,energy,size,color):
    data = bpy.data.lights.new(name,'AREA')
    data.energy,data.size,data.color = energy,size,color
    obj = bpy.data.objects.new(name,data)
    scene.collection.objects.link(obj)
    obj.location = pos
    obj.rotation_euler = (Vector((0,50,85))-obj.location).to_track_quat('-Z','Y').to_euler()


light('Key',(200,260,400),5500000,280,(1,.82,.65))
light('Fill',(-260,100,250),3200000,260,(.62,.78,1))
light('Rim',(10,-320,380),6000000,180,(.72,.89,1))


def camera(name,pos,target,scale):
    data = bpy.data.cameras.new(name)
    data.type,data.ortho_scale,data.clip_end = 'ORTHO',scale,5000
    obj = bpy.data.objects.new(name,data)
    scene.collection.objects.link(obj)
    obj.location = pos
    obj.rotation_euler = (Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
    return obj


wide = camera('Full arc',(480,640,440),(0,5,65),650)
close = camera('Grip',(230,290,220),(0,130,92),190)
scene.camera = wide


def set_yaw(degrees):
    rotation = Matrix.Rotation(math.radians(degrees),4,'Z')
    aim.rotation_euler.z = math.radians(degrees)
    placement.matrix_world = rotation@actor_rest


def pose(frame,yaw,clip):
    rig.animation_data.action = bpy.data.actions[clip]
    scene.frame_set(frame)
    set_yaw(yaw)
    bpy.context.view_layer.update()


if MODE == 'poses':
    for yaw in (-60,0,60):
        pose(0,yaw,'astra_guard_operate')
        scene.camera = wide
        scene.render.filepath = str(OUT/f'guard_yaw_{yaw:+03d}.png')
        bpy.ops.render.render(write_still=True)
    pose(2,0,'astra_guard_fire')
    scene.camera = close
    scene.render.filepath = str(OUT/'guard_grip_fire.png')
    bpy.ops.render.render(write_still=True)
    print('V23_POSES_RENDERED')
else:
    sequence = bpy.data.actions.new('PREVIEW_ONLY full arc and fire')
    sequence.use_fake_user = True
    for frame in range(331):
        if frame < 30:
            clip,local,yaw = 'astra_guard_operate',frame,-60.
        elif frame < 270:
            step,local = divmod(frame-30,24)
            clip,yaw = 'astra_guard_turn_left',-60.+step*12+local*.5
        elif frame <= 300:
            clip,local,yaw = 'astra_guard_fire',frame-270,60.
        else:
            clip,local,yaw = 'astra_guard_operate',frame-301,60.
        pose(local,yaw,clip)
        matrices = {pb.name:pb.matrix_basis.copy() for pb in rig.pose.bones}
        rig.animation_data.action = sequence
        scene.frame_set(frame)
        for pb in rig.pose.bones:
            pb.matrix_basis = matrices[pb.name]
            for field in ('location','rotation_quaternion','scale'):
                pb.keyframe_insert(data_path=field,frame=frame,group=pb.name)
        set_yaw(yaw)
        aim.keyframe_insert(data_path='rotation_euler',frame=frame)
        for field in ('location','rotation_euler'):
            placement.keyframe_insert(data_path=field,frame=frame)
    # Reference mechanism only; sourced motion stays inside this preview file.
    reference = Path('E:/Sectores/Sector_Modelado_3D/Ballesta_Astra_Animacion_Guardia_v01/inputs/ballesta_reference.blend')
    with bpy.data.libraries.load(str(reference),link=False) as (src,dst):
        dst.actions = ['Fire','Reset']
    fire,reset = dst.actions
    for slot in fire.slots:
        obj = bpy.data.objects[slot.identifier[2:]]
        action = bpy.data.actions.new('PREVIEW_ONLY mechanism '+obj.name)
        obj.animation_data_create()
        obj.animation_data.action = action
        for frame in range(331):
            t = (frame-270)/30
            native = fire if t <= .2 else reset
            nt = max(0,min(.2,t)) if native == fire else min(.8,t-.2)
            native_slot = next(s for s in native.slots if s.identifier == slot.identifier)
            fields = set()
            for layer in native.layers:
                for strip in layer.strips:
                    for fc in strip.channelbag(native_slot).fcurves:
                        getattr(obj,fc.data_path)[fc.array_index] = fc.evaluate(1+nt*24)
                        fields.add(fc.data_path)
            for field in fields:obj.keyframe_insert(data_path=field,frame=frame)
    bolt = bpy.data.objects['VIROTE_VISUAL']
    for frame,scale in ((0,1),(271,1),(272,.001),(300,.001),(301,1),(330,1)):
        bolt.scale = (scale,)*3
        bolt.keyframe_insert(data_path='scale',frame=frame)
    for obj in (rig,aim,placement,*[bpy.data.objects[s.identifier[2:]] for s in fire.slots]):
        for layer in obj.animation_data.action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for curve in bag.fcurves:
                        for key in curve.keyframe_points:
                            key.interpolation = 'CONSTANT' if obj == bolt and curve.data_path == 'scale' else 'LINEAR'
    scene.frame_start,scene.frame_end = 0,330
    scene.frame_set(150)
    scene.camera = wide
    scene['preview_is_skyrim_test'] = False
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'astra_guard_preview_v23.blend'))
    scene.cycles.samples = 6
    scene.render.resolution_x,scene.render.resolution_y = 640,400
    (OUT/'frames').mkdir(exist_ok=True)
    scene.render.filepath = str(OUT/'frames/frame_')
    bpy.ops.render.render(animation=True)
    print('V23_MOVIE_FRAMES_RENDERED')
