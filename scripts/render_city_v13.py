"""Static preview of actual city reference transforms and unmodified terrain."""
import json,sys,math,hashlib
from pathlib import Path
import bpy,addon_utils
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
import v11_layout as L
from render_v12 import import_nif,place

def mesh_tree(objs):
    vs=[];ts=[]
    for o in objs:
        if o.type!='MESH' or o.name.startswith('bhk'):continue
        o.data.calc_loop_triangles();base=len(vs);vs.extend(o.matrix_world@v.co for v in o.data.vertices)
        ts.extend(tuple(base+j for j in t.vertices) for t in o.data.loop_triangles)
    return BVHTree.FromPolygons(vs,ts,all_triangles=True) if vs else None

def collision_tree():
    vs=[];ts=[]
    for o in bpy.data.objects:
        if o.type!='MESH':continue
        # Walking geometry is Havok for own tower/gun and visual conservative
        # envelopes for vanilla scenery; decorative shields also join this check.
        if o.get('own_visual'):continue
        o.data.calc_loop_triangles();base=len(vs)
        vs.extend(o.matrix_world@v.co for v in o.data.vertices)
        ts.extend(tuple(base+j for j in t.vertices) for t in o.data.loop_triangles)
    return BVHTree.FromPolygons(vs,ts,all_triangles=True)

def main():
    cfg=L.load_cfg();site=json.loads((ROOT/'reports/city_site_v13.json').read_text())
    addon_utils.enable('io_scene_nifly',default_set=True)
    bpy.context.preferences.addons['io_scene_nifly'].preferences.sky_texture_path_1=str(Path(cfg['extracted'])/'textures')
    for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
    origin=(site['x'],site['y'],site['z']);rotation=(0,0,site['rot_z_deg'])
    roots,tower=import_nif(ROOT/'mod/meshes/AstraAsedio/torre_whiterun.nif')
    place(roots,L.transform_matrix((0,0,0),rotation,1,*L.engine_convention()))
    for o in tower:
        if o.type=='MESH':o['own_visual']=True
    roots,_=import_nif(ROOT/'mod/meshes/AstraAsedio/ballesta.nif')
    place(roots,L.transform_matrix((0,0,cfg['tower_top_units']),rotation,1,*L.engine_convention()))
    for o in bpy.data.objects:
        if o.type=='MESH' and not o.name.startswith('bhk'):o['own_visual']=True
    # Import own written Havok in addition to visual meshes for route/body checks.
    for name,offset in (('torre_whiterun',0),('ballesta',cfg['tower_top_units'])):
        old=set(bpy.data.objects);bpy.context.view_layer.objects.active=None
        bpy.ops.import_scene.pynifly(filepath=str(ROOT/'mod/meshes/AstraAsedio'/f'{name}.nif'),blender_xf=False,import_animations=False,import_collisions=True,create_bones=False)
        new=set(bpy.data.objects)-old
        for o in new:
            if o.type=='MESH' and o.name.startswith('bhk'):
                o.parent=None
                place([o],L.transform_matrix((0,0,offset),rotation,1,*L.engine_convention()))
                o.hide_render=True
            elif o.type=='MESH':o['own_visual']=True;o.hide_render=True
    for item in cfg['tower_v11']['escudos']['items']:
        import mundo_v11 as M
        pp,rr=M.llevar({'pos':item['pos'],'rot_deg':item['rot_deg'],'scale':1},site)
        roots,_=import_nif(Path(cfg['extracted'])/'meshes'/cfg['tower_v11']['escudos']['modl'])
        place(roots,L.transform_matrix([p-o for p,o in zip(pp,origin)],rr,1,*L.engine_convention()))
    bpy.context.view_layer.update();own_tree=mesh_tree(tower);overlaps=[];models=[]
    for ref in json.loads((ROOT/'reports/gate_models_v13.json').read_text()):
        model=ref['donor'].get('model','');lower=model.lower()
        if not lower.startswith(('architecture\\','landscape\\rocks\\','landscape\\roads\\')):continue
        if ref['donor']['type'] not in ('STAT','DOOR'):continue
        path=Path(cfg['extracted'])/'meshes'/model
        if not path.exists():continue
        roots,objs=import_nif(path)
        place(roots,L.transform_matrix([p-o for p,o in zip(ref['data'][:3],origin)],
                                      [math.degrees(a) for a in ref['data'][3:]],ref.get('scale',1),*L.engine_convention()))
        bpy.context.view_layer.update();other=mesh_tree(objs)
        if other and own_tree.overlap(other):overlaps.append({'id':ref['id'],'model':model})
        models.append(ref['id'])
    # LAND as triangles: preview only. No write to vanilla resources or plugin LAND.
    vs=[];fs=[]
    for key,h in site['heightmaps'].items():
        gx,gy=map(int,key.split(','));base=len(vs)
        vs.extend((gx*4096+128*x-origin[0],gy*4096+128*y-origin[1],h[y][x]-origin[2]) for y in range(33) for x in range(33))
        for y in range(32):
            for x in range(32):
                a=base+y*33+x;fs.extend(((a,a+1,a+34),(a,a+34,a+33)))
    me=bpy.data.meshes.new('LAND_vanilla');me.from_pydata(vs,[],fs);me.update()
    ob=bpy.data.objects.new('LAND_vanilla',me);bpy.context.scene.collection.objects.link(ob)
    mat=bpy.data.materials.new('Tundra_preview');mat.diffuse_color=(.24,.20,.12,1);ob.data.materials.append(mat)
    bpy.context.view_layer.update();body=collision_tree()
    import tower_v12_geometry as G
    route=[((G.SX0+G.SX1)/2,G.SY0+(G.SY1-G.SY0)*i/100,140*i/100) for i in range(101)]
    route += [((G.SX0+G.SX1)/2,238,140)]
    route += [((G.SX0+G.SX1)/2*(1-i/30),238,140) for i in range(1,31)]
    route += [(0,238+(132-238)*i/20,140) for i in range(1,21)]
    route += [(73.5*i/20,132,140) for i in range(1,21)]
    m=L.transform_matrix((0,0,0),rotation,1,*L.engine_convention());blocks=[]
    for k,p in enumerate(route):
        worldp=Vector(L.apply(m,p))
        for height in (18,25,64,112,128):
            for j in range(16):
                a=j*math.tau/16;hit=body.ray_cast(worldp+Vector((0,0,height)),Vector((math.cos(a),math.sin(a),0)),18)
                if hit[0] is not None:blocks.append({'sample':k,'height':height,'hit':list(hit[0])})
    assert not blocks,('City body route obstructed',blocks[:10])
    sun=bpy.data.lights.new('sol','SUN');sun.energy=3.5;o=bpy.data.objects.new('sol',sun);bpy.context.scene.collection.objects.link(o);o.rotation_euler=(.8,.2,2.2)
    world=bpy.data.worlds.new('mundo');bpy.context.scene.world=world;world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.36,.38,.42,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
    sc=bpy.context.scene;sc.render.engine='BLENDER_EEVEE_NEXT';sc.render.resolution_x=1600;sc.render.resolution_y=1000;sc.render.resolution_percentage=100
    cam=bpy.data.cameras.new('cam');cam.lens=32;cam.clip_start=5;cam.clip_end=20000
    ob=bpy.data.objects.new('cam',cam);sc.collection.objects.link(ob);sc.camera=ob
    ob.location=(-1700,-1800,1350);ob.rotation_euler=(Vector((600,-200,200))-ob.location).to_track_quat('-Z','Y').to_euler()
    sc.render.filepath=str(ROOT/'renders/v13_whiterun.png');bpy.ops.render.render(write_still=True)
    report={'game_capture':False,'static_preview':True,'models':models,'tower_intersections_with_vanilla_visual_meshes':overlaps,
            'body_route_samples':len(route),'body_route_blocked_samples':len(blocks),'guard_local':site['guard_local'],
            'rock_seating':'Own pillar endpoints seated 6u into vanilla rock surfaces; contact is expected below the deck.',
            'city_mesh_sha256':hashlib.sha256((ROOT/'mod/meshes/AstraAsedio/torre_whiterun.nif').read_bytes()).hexdigest(),
            'site_sha256':hashlib.sha256((ROOT/'reports/city_site_v13.json').read_bytes()).hexdigest()}
    (ROOT/'reports/city_visual_v13.json').write_text(json.dumps(report,indent=2))
    assert all(r['model'].lower().startswith('landscape\\rocks\\') for r in overlaps),overlaps
    print('CITY_PREVIEW_OK',len(models),'vanilla models, only expected rock footing contacts, body route',len(route))
if __name__=='__main__':main()
