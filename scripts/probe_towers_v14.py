"""Measure existing tower floors/body clearance and preview mounted ballista poses."""
import json,sys,math,hashlib
from pathlib import Path
import bpy,addon_utils
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
import v11_layout as L
from render_v12 import place
from inspect_towers_v14 import nav_surface
BASE=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v13')

def tree(objs):
    vs=[];ts=[]
    for o in objs:
        if o.type!='MESH':continue
        o.data.calc_loop_triangles();base=len(vs)
        vs.extend(o.matrix_world@v.co for v in o.data.vertices)
        ts.extend(tuple(base+i for i in t.vertices) for t in o.data.loop_triangles)
    return BVHTree.FromPolygons(vs,ts,all_triangles=True) if vs else None

def load(path,m):
    before=set(bpy.data.objects);bpy.context.view_layer.objects.active=None
    bpy.ops.import_scene.pynifly(filepath=str(path),blender_xf=False,import_animations=False,import_collisions=True,create_bones=False)
    objs=set(bpy.data.objects)-before
    place([o for o in objs if o.parent is None],m)
    bpy.context.view_layer.update()
    for o in objs:
        if o.name.startswith('bhk'):o.hide_render=True
    return objs

def floor(bvh,x,y,near_z):
    hit=bvh.ray_cast(Vector((x,y,near_z+45)),Vector((0,0,-1)),100)
    if hit[0] is None or hit[1].z<.8:return None
    return hit[0].z

def capsule_clear(bvh,p,radius=18):
    for z in (18,25,64,112,128):
        for j in range(24):
            a=j*math.tau/24
            h=bvh.ray_cast(Vector(p)+Vector((0,0,z)),Vector((math.cos(a),math.sin(a),0)),radius)
            if h[0] is not None:return False
    top=bvh.ray_cast(Vector(p)+Vector((0,0,10)),Vector((0,0,1)),118)
    return top[0] is None

def render(name,origin,look):
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=16
    scene.render.resolution_x=1200;scene.render.resolution_y=900;scene.render.resolution_percentage=100
    scene.world.color=(.14,.14,.14)
    data=bpy.data.lights.new('Sol','SUN');ob=bpy.data.objects.new('Sol',data);scene.collection.objects.link(ob)
    ob.rotation_euler=(.4,-.5,-.7);data.energy=2
    cam=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));scene.collection.objects.link(cam)
    cam.location=(520,-650,490);cam.rotation_euler=(Vector(look)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=38
    scene.camera=cam;scene.render.filepath=str(ROOT/'renders'/f'v14_torre_{name}.png');bpy.ops.render.render(write_still=True)

def main():
    cfg=json.loads((BASE/'config.json').read_text());context=json.loads((ROOT/'reports/tower_context_v14.json').read_text())
    addon_utils.enable('io_scene_nifly',default_set=True)
    bpy.context.preferences.addons['io_scene_nifly'].preferences.sky_texture_path_1=str(Path(cfg['extracted'])/'textures')
    reports=[]
    for req in context['requests']:
        for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
        origin=req['requested'];visual=[];coll=[];loaded=[];own_tower_coll=[]
        for ref in context['refs']:
            if ref['deleted'] or math.dist(ref['data'][:2],origin[:2])>750:continue
            model=ref['donor'].get('model','')
            if not model.lower().startswith(('architecture\\','landscape\\rocks\\','clutter\\')):continue
            path=Path(cfg['extracted'])/'meshes'/model
            if not path.exists():continue
            m=L.transform_matrix([a-b for a,b in zip(ref['data'][:3],origin)],
                                 [math.degrees(a) for a in ref['data'][3:]],ref['scale'],*L.engine_convention())
            objs=load(path,m);v=[o for o in objs if o.type=='MESH' and not o.name.startswith('bhk')]
            c=[o for o in objs if o.type=='MESH' and o.name.startswith('bhk')]
            visual+=v;coll+=c;loaded.append({'id':ref['id'],'model':model,'collision_objects':len(c)})
            if ref['id']==req['tower_ref']:own_tower_coll=c
        # Large tower holds roof/posts; its walking floor belongs to the two
        # adjoining WRScafStr02 references. Include all nearby written Havok.
        body=tree(visual+coll);floors=tree(coll) or tree(visual)
        floor_at_request=floor(floors,0,0,0)
        assert floor_at_request is not None,('No floor at request',req['name'])
        print('REQUEST_FLOOR',req['name'],floor_at_request+origin[2],len(own_tower_coll))
        # Candidate floor disk and guard capsule. Final mount is selected from measured alternatives.
        candidates=[]
        for x in range(-96,97,24):
            for y in range(-96,97,24):
                z=floor(floors,x,y,floor_at_request)
                if z is None:continue
                nav=nav_surface(context['navmeshes'],x+origin[0],y+origin[1])
                on_nav=[n for n in nav if abs(n['z']-(z+origin[2]))<8]
                candidates.append({'local':[x,y,z],'body_clear':capsule_clear(body,(x,y,z)),
                                   'nav':on_nav})
        gun=load(ROOT/'mod/meshes/AstraAsedio/ballesta.nif',L.transform_matrix((0,0,floor_at_request+11.55),(0,0,0),1,*L.engine_convention()))
        reports.append({**req,'floor_world_z':floor_at_request+origin[2],'havok_floor_objects':len(own_tower_coll),
                        'candidates':candidates,'models':loaded,'preview_mount':[origin[0],origin[1],floor_at_request+origin[2]+11.55],
                        'scope':'Preview at supplied XY, conservative mesh/body checks; final mount selection follows.'})
        render(req['name'],origin,(0,0,70))
    output={'ballista_sha256':hashlib.sha256((ROOT/'mod/meshes/AstraAsedio/ballesta.nif').read_bytes()).hexdigest(),
            'context_sha256':hashlib.sha256((ROOT/'reports/tower_context_v14.json').read_bytes()).hexdigest(),
            'sites':reports,'engine_verified':False}
    (ROOT/'reports/tower_probe_v14.json').write_text(json.dumps(output,indent=2))
    print('TOWERS_PROBED',[(r['name'],len(r['candidates']),sum(p['body_clear'] for p in r['candidates'])) for r in reports])
if __name__=='__main__':main()
