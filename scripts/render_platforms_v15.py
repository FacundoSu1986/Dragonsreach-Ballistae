"""Static Blender previews of exported assets and read-only vanilla context."""
import sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
import bpy,addon_utils,numpy as np
from mathutils import Vector
import tower_fit_v14 as F
from probe_towers_v14 import load
import v11_layout as L

def main():
    cfg=json.loads((ROOT/'config.json').read_text());ctx=json.loads((ROOT/'reports/tower_context_v14.json').read_text())
    addon_utils.enable('io_scene_nifly',default_set=True)
    bpy.context.preferences.addons['io_scene_nifly'].preferences.sky_texture_path_1=str(Path(cfg['extracted'])/'textures')
    report=json.loads((ROOT/'reports/platforms_v15.json').read_text())
    for s in report['sites']:
        for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
        req=next(r for r in ctx['requests'] if r['name']==s['name'])
        # Limit render-only imports by cached measured bounds, preserving every
        # complete visible tower/wall donor. Never export these vanilla models.
        near={'requests':ctx['requests'],'refs':[r for r in ctx['refs'] if math.dist(r['data'][:2],req['requested'][:2])<750]}
        F.context_import(req,cfg,near)
        load(ROOT/s['nif'],L.transform_matrix((0,0,0),(0,0,0),1,*L.engine_convention()))
        load(ROOT/'mod/meshes/AstraAsedio/ballesta.nif',L.transform_matrix(s['gun_local_pos'],(0,0,0),1,*L.engine_convention()))
        scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=12
        scene.render.resolution_x=1400;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
        scene.world.color=(.18,.18,.18)
        sun=bpy.data.objects.new('PreviewSun',bpy.data.lights.new('PreviewSun','SUN'));scene.collection.objects.link(sun)
        sun.rotation_euler=(.45,-.5,-.7);sun.data.energy=2.5
        cam=bpy.data.objects.new('PreviewCamera',bpy.data.cameras.new('PreviewCamera'));scene.collection.objects.link(cam)
        cam.location=(850,-1150,640);target=Vector((0,-325,-60))
        cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=1050
        cam.data.clip_start=1;cam.data.clip_end=10000
        scene.camera=cam;scene.render.image_settings.file_format='PNG'
        scene.render.filepath=str(ROOT/'renders'/('v15_voladizo_'+s['name']+'.png'));bpy.ops.render.render(write_still=True)
        print('PREVIEW_RENDERED',s['name'],flush=True)
if __name__=='__main__':main()
