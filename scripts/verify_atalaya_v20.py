"""Reimport the written site NIF: walk/aim/terrain proxies, not game testing."""
import sys,json,math,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
import bpy,addon_utils,numpy as np
from mathutils import Vector
import v11_layout as L
import build_assets as A
import tower_fit_v14 as F
from probe_towers_v14 import load,capsule_clear
from verify_shot_clearance_v12 import Aim,seg_tri
import atalaya_v20_geometry as G

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    addon_utils.enable('io_scene_nifly',default_set=True)
    cfg=L.load_cfg();bpy.context.preferences.addons['io_scene_nifly'].preferences.sky_texture_path_1=str(Path(cfg['extracted'])/'textures')
    A.clear();s=G.Surface();fit=G.build();path=ROOT/'addons/Atalaya/meshes/AstraAsedio/torre_atalaya_v20.nif'
    own=load(path,L.transform_matrix((0,0,0),(0,0,0),1,*L.engine_convention()))
    V,T=F.mesh_arrays([o for o in own if o.type=='MESH' and not o.name.startswith('bhk')])
    C,CT=F.mesh_arrays([o for o in own if o.type=='MESH' and o.name.startswith('bhk')])
    assert len(T)>0 and len(CT)>0
    np.savez_compressed(ROOT/'reports/atalaya_written_v20.npz',V=V,T=T,C=C,CT=CT)
    bvh=F.bvh_from_triangles(C[CT]);route=[]
    entry=fit['entry']
    for y in np.linspace(entry['y0']+2,196,161):route.append([323.4,float(y),.6201923076923077*(float(y)+29.736434108527135)])
    route += [[323.4,float(y),140] for y in np.linspace(196,230,11)]
    route += [[float(x),230,140] for x in np.linspace(323.4,0,41)]
    route += [[0,float(y),148.75 if y<150 else 140] for y in np.linspace(230,135,31)]
    floor_errors=[];badcaps=[]
    for p in route:
        z=F.floor_at(bvh,p[0],p[1],p[2]);assert z is not None,('Missing walking support',p)
        floor_errors.append(abs(z-p[2]))
        assert abs(z-p[2])<10,('Walking gap',p,z)
        if not capsule_clear(bvh,(p[0],p[1],z)):badcaps.append(p)
    assert not badcaps,('Capsule blocked',badcaps[:4])
    assert abs(F.floor_at(bvh,0,0,148.75)-148.75)<.03
    allT=np.concatenate([V[T],C[CT]]);aim=Aim(cfg);shapes=F.gun_arrays();contacts=[];hits=[];mindist=math.inf;poses=0
    render_only='--render-only' in sys.argv
    if render_only:
        approved=json.loads((ROOT/'reports/atalaya_verified_v20.json').read_text())
        assert approved['success'] and approved['nif_sha256']==sha(path)
    for yaw in ([] if render_only else range(0,360,5)):
        for pitch in range(-20,81,5):
            gv,gt=F.gun_pose(shapes,yaw,pitch);gv[:,2]+=151.55;gun=gv[gt]
            sel=(allT.max(1)>gun.min((0,1))).all(1)&(allT.min(1)<gun.max((0,1))).all(1)
            if sel.any():
                overlap=F.bvh_from_triangles(gun).overlap(F.bvh_from_triangles(allT[sel]))
                if overlap:contacts.append([yaw,pitch,len(overlap)])
            m,b=aim.pose(yaw,pitch);e=m+b*max(0,(650-np.linalg.norm(m[:2]))/np.linalg.norm(b[:2]))
            sel=(allT.max(1)>=np.minimum(m,e)-4).all(1)&(allT.min(1)<=np.maximum(m,e)+4).all(1)
            if sel.any():
                d=float(seg_tri(m,e,allT[sel]).min());mindist=min(mindist,d)
                if d<2.205:hits.append([yaw,pitch,d])
            poses+=1
    assert not contacts,('Gun intersects own tower',contacts[:5])
    assert not hits,('Own geometry blocks shot',hits[:5])
    # Nearby vanilla geometry is read only. Seal hashes and test the access
    # capsule, without exporting or redistributing any of those meshes.
    env=[];metadata=[];rd=np.array(s.m['r']);origin=np.array(s.m['t'])
    for ref in s.ctx['refs']:
        model=ref['donor'].get('model','')
        if ref['flags']&(0x20|0x800) or not model.lower().startswith(('landscape\\rocks\\','landscape\\roads\\','dungeons\\')):continue
        nif=Path(cfg['extracted'])/'meshes'/model
        rm=L.transform_matrix(ref['data'][:3],[math.degrees(a) for a in ref['data'][3:]],ref['scale'],*L.engine_convention())
        local={'r':(rd.T@np.array(rm['r'])).tolist(),'t':(rd.T@(np.array(rm['t'])-origin)).tolist(),'s':rm['s']}
        objs=load(nif,local);a,b=F.mesh_arrays([o for o in objs if o.type=='MESH' and o.name.startswith('bhk')]);env.extend(a[b])
        metadata.append({'reference':ref['id'],'model':model,'sha256':sha(nif),'havok_triangles':len(b)})
    envb=F.bvh_from_triangles(np.array(env)) if env else None
    blocked=[]
    if envb:
        for p in route:
            z=F.floor_at(bvh,p[0],p[1],p[2])
            if not capsule_clear(envb,(p[0],p[1],z)):blocked.append(p)
    assert not blocked,('Vanilla object blocks stairs/access',blocked[:4])
    result={'success':True,'nif_sha256':sha(path),'visual_triangles':len(T),'havok_triangles':len(CT),'walk_samples':len(route),'walk_max_support_gap':max(floor_errors),'capsule_blocked':badcaps,'vanilla_access_blocked':blocked,'static_aim_poses':poses,'pose_increment_degrees':5,'gun_contacts':contacts,'initial_shot_hits':hits,'initial_shot_min_clearance':mindist if math.isfinite(mindist) else None,'supports':fit['support_checks'],'stair_ground_max_overlap':fit['stair_ground_max_overlap'],'nearby_vanilla':metadata,'LAND_edits':0,'NAVM_edits':0,'game_tested':False,'scope':'Written NIF reimport; geometric walking capsule and 5-degree static rest-pose/initial-shot grid. No NPC route, animated bounds, quest, save migration, or engine test.'}
    result['inputs_sha256']={rel:sha(ROOT/rel) for rel in ('config.json','scripts/atalaya_v20_geometry.py','scripts/verify_atalaya_v20.py','scripts/tower_v12_geometry.py','scripts/tower_fit_v14.py','scripts/probe_towers_v14.py','scripts/render_v12.py','scripts/verify_shot_clearance_v12.py','scripts/v11_layout.py','reports/atalaya_context_v20.json','reports/atalaya_environment_v20.json','reports/atalaya_rocks_v20.npz','reports/atalaya_existing_havok_v20.npz','mod/meshes/AstraAsedio/ballesta.nif','addons/Atalaya/meshes/AstraAsedio/torre_atalaya_v20.nif')}
    if not render_only:
        (ROOT/'reports/atalaya_verified_v20.json').write_text(json.dumps(result,indent=2))
        print('ATALAYA_VERIFIED',len(T),len(CT),len(route),poses,'poses',flush=True)
    # Terrain preview is a diagram from the read-only height map. Vanilla
    # meshes remain in memory; no blend containing them is saved.
    heights=np.array(s.site['heightmaps']['1,-4']);vv=[];ff=[]
    for y in range(33):
        for x in range(33):vv.append(tuple(rd.T@(np.array([4096+x*128,-16384+y*128,heights[y,x]])-origin)))
    for y in range(32):
        for x in range(32):i=y*33+x;ff.extend([(i,i+1,i+34),(i,i+34,i+33)])
    me=bpy.data.meshes.new('Terrain_preview');me.from_pydata(vv,[],ff);me.update();ob=bpy.data.objects.new('Terrain_preview',me);bpy.context.scene.collection.objects.link(ob)
    mat=bpy.data.materials.new('Terrain_diagram');mat.diffuse_color=(.16,.21,.13,1);me.materials.append(mat)
    load(ROOT/'mod/meshes/AstraAsedio/ballesta.nif',L.transform_matrix((0,0,151.55),(0,0,0),1,*L.engine_convention()))
    for item in cfg['tower_v11']['escudos']['items']:
        load(Path(cfg['extracted'])/'meshes'/cfg['tower_v11']['escudos']['modl'],L.piece_matrix({'pos':item['pos'],'rot_deg':item['rot_deg'],'scale':1}))
    for mat in bpy.data.materials:
        if 'stockade' in mat.name.lower():mat.diffuse_color=(.28,.17,.08,1)
        elif 'rope' in mat.name.lower():mat.diffuse_color=(.39,.30,.17,1)
    scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH';scene.render.resolution_x=1200;scene.render.resolution_y=900;scene.render.resolution_percentage=100
    scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL';scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True
    cam=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));scene.collection.objects.link(cam);cam.location=(950,-1000,690);cam.rotation_euler=(Vector((40,0,60))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=48;cam.data.clip_start=1;cam.data.clip_end=100000;scene.camera=cam
    (ROOT/'renders').mkdir(exist_ok=True);scene.render.filepath=str(ROOT/'renders/atalaya_v20_terreno.png');bpy.ops.render.render(write_still=True)
if __name__=='__main__':main()
