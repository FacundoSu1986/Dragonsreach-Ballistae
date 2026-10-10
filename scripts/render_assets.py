"""Render actual exported NIFs with the extracted vanilla textures."""
import bpy, addon_utils, json, math, hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/'config.json').read_text())
addon_utils.enable('io_scene_nifly',default_set=True)
bpy.context.preferences.addons['io_scene_nifly'].preferences.sky_texture_path_1=str(Path(CFG['extracted'])/'textures')
for o in list(bpy.data.objects): bpy.data.objects.remove(o,do_unlink=True)
scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.samples=48
scene.render.resolution_x=1400; scene.render.resolution_y=1400; scene.render.resolution_percentage=100
scene.world.color=(.32,.32,.32)
scene.render.image_settings.file_format='PNG'
scene.view_settings.view_transform='AgX'
scene.view_settings.look='AgX - Medium High Contrast'
scene.view_settings.exposure=.75
visual=[]
for name in ('torre','ballesta'):
    old=set(bpy.data.objects)
    bpy.context.view_layer.objects.active=None
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.import_scene.pynifly(filepath=str(ROOT/'mod/meshes/AstraAsedio'/f'{name}.nif'),blender_xf=False,import_animations=False,import_collisions=False,create_bones=False)
    new=set(bpy.data.objects)-old
    if name=='ballesta':
        root=next(o for o in new if o.get('pynRoot'))
        root.location.z=465.5
    visual.extend(o for o in new if o.type=='MESH' and not o.name.startswith('bhk'))
bpy.context.view_layer.update()
def camera(name,position,target,lens):
    data=bpy.data.cameras.new(name); o=bpy.data.objects.new(name,data); scene.collection.objects.link(o)
    o.location=position; o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler(); data.type='ORTHO'; data.ortho_scale=lens; data.clip_end=5000; scene.camera=o
    return o
def area(name,pos,power,size):
    data=bpy.data.lights.new(name,'AREA'); data.energy=power; data.shape='DISK'; data.size=size
    o=bpy.data.objects.new(name,data); scene.collection.objects.link(o); o.location=pos; o.rotation_euler=(Vector((0,0,260))-o.location).to_track_quat('-Z','Y').to_euler()
area('Key',(-450,-750,1100),7000000,650); area('Fill',(800,-350,600),3500000,500); area('Rim',(200,650,1000),5000000,600)
bpy.ops.mesh.primitive_plane_add(size=2400,location=(0,0,-15)); ground=bpy.context.object
mat=bpy.data.materials.new('Studio_floor'); mat.diffuse_color=(.11,.13,.15,1); ground.data.materials.append(mat)
camera('Overview',(1000,-1350,1050),(25,0,275),880)
scene.render.filepath=str(ROOT/'renders/Astra_overview.png'); bpy.ops.render.render(write_still=True)
camera('Mechanism',(520,-720,840),(0,-40,575),490)
scene.render.filepath=str(ROOT/'renders/Astra_mechanism.png'); bpy.ops.render.render(write_still=True)
camera('Ratchet',(-180,260,660),(-42,124,604),115)
scene.render.filepath=str(ROOT/'renders/Astra_trinquete_v05.png'); bpy.ops.render.render(write_still=True)
camera('BowBindings',(-285,-425,875),(0,-110,610),350)
scene.render.filepath=str(ROOT/'renders/Astra_amarres_v05.png'); bpy.ops.render.render(write_still=True)
# v09: straight rustic stair tower, whole view from the stair side and a log-corner close-up.
camera('TorreRustica',(1100,-1500,1120),(40,-130,285),1260)
scene.render.filepath=str(ROOT/'renders/Astra_torre_rustica_v09.png'); bpy.ops.render.render(write_still=True)
camera('EsquinaRustica',(-700,-760,620),(-150,-150,330),520)
scene.render.filepath=str(ROOT/'renders/Astra_esquina_rustica_v09.png'); bpy.ops.render.render(write_still=True)
from mathutils import Matrix
# Mathematical preview from the actual exported anchor; this is not a Skyrim capture.
anchor=bpy.data.objects[CFG['camera_node']]
data=bpy.data.cameras.new('SightPreview'); o=bpy.data.objects.new('SightPreview',data); scene.collection.objects.link(o)
o.matrix_world=anchor.matrix_world @ Matrix.Rotation(math.pi/2,4,'X')
data.type='PERSP'; data.angle=math.radians(75); data.clip_start=8; data.clip_end=5000; scene.camera=o
scene.render.resolution_x=1600; scene.render.resolution_y=900
scene.render.filepath=str(ROOT/'renders/Astra_mira_v05.png'); bpy.ops.render.render(write_still=True)
scene.render.resolution_x=1400; scene.render.resolution_y=1400
node=bpy.data.objects['CTRL_ELEVACION'];base=node.matrix_local.copy()
pose=Matrix.Rotation(math.radians(-80),4,'X')@base;pose.translation=base.translation;node.matrix_local=pose
bpy.context.view_layer.update()
camera('DragonElevation',(480,450,785),(0,0,610),570)
scene.render.filepath=str(ROOT/'renders/Astra_elevacion_80_v05.png'); bpy.ops.render.render(write_still=True)
(ROOT/'reports/renders.json').write_text(json.dumps({'renderer':'Blender 4.4 Cycles','frames':'four rest views, sight anchor preview and +80 degree elevation view','in_game':False,'sight_preview_fov_degrees':75,'sight_preview_is_engine_camera_proof':False,'nifs':{name:hashlib.sha256((ROOT/'mod/meshes/AstraAsedio'/f'{name}.nif').read_bytes()).hexdigest() for name in ('torre','ballesta')},'images':['renders/Astra_overview.png','renders/Astra_mechanism.png','renders/Astra_trinquete_v05.png','renders/Astra_amarres_v05.png','renders/Astra_torre_rustica_v09.png','renders/Astra_esquina_rustica_v09.png','renders/Astra_mira_v05.png','renders/Astra_elevacion_80_v05.png']},indent=2))
print('ASTRA_RENDERS_OK')
