"""Identify the textured front face of the vanilla target without guessing rotation."""
import bpy,addon_utils,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/'config.json').read_text())
addon_utils.enable('io_scene_nifly',default_set=True)
bpy.context.preferences.addons['io_scene_nifly'].preferences.sky_texture_path_1=str(Path(CFG['extracted'])/'textures')
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
bpy.context.view_layer.objects.active=None
for name in ('archerytarget01','archerytargettripod01'):
    bpy.ops.import_scene.pynifly(filepath=str(Path(CFG['extracted'])/'meshes/clutter/common'/f'{name}.nif'),blender_xf=False,import_animations=False,import_collisions=False,create_bones=False)
    bpy.ops.object.select_all(action='DESELECT');bpy.context.view_layer.objects.active=None
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=12
scene.render.resolution_x=700;scene.render.resolution_y=700;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.world.color=(.3,.3,.3)
for i,x in enumerate((-250,250)):
    data=bpy.data.lights.new('fill'+str(i),'AREA');data.energy=900000;data.size=180
    obj=bpy.data.objects.new(data.name,data);scene.collection.objects.link(obj)
    obj.location=(x,-150,200);obj.rotation_euler=(Vector((-30,0,60))-obj.location).to_track_quat('-Z','Y').to_euler()
data=bpy.data.cameras.new('camera');obj=bpy.data.objects.new('camera',data);scene.collection.objects.link(obj)
data.type='ORTHO';data.ortho_scale=170;data.clip_end=5000;scene.camera=obj
for side,x in [('positive_x',250),('negative_x',-300)]:
    obj.location=(x,0,100);obj.rotation_euler=(Vector((-30,0,60))-obj.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(ROOT/'renders'/('Target_'+side+'.png'));bpy.ops.render.render(write_still=True)
