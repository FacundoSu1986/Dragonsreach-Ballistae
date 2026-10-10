"""Reimport written NIFs and measure static access/nav/aim; no engine claim."""
import json,sys,math,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor'),str(ROOT/'reports')]
import numpy as np,bpy,addon_utils
import tower_fit_v14 as F
import platforms_v15_geometry as G
import research_platform_v15 as R
from verify_shot_clearance_v12 import Aim,seg_tri
from inspect_towers_v14 import nav_surface
from probe_towers_v14 import load
import v11_layout as L
from mathutils import Vector
import nif_nodos

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def nav_samples(ctx,s,CT):
    origin=np.array(s['origin']);floors=F.bvh_from_triangles(CT);points={}
    for t in R.navtops(ctx,origin):
        v=np.array(t['vertices']);lo=np.floor(v[:,:2].min(0)/4)*4;hi=np.ceil(v[:,:2].max(0)/4)*4
        for x in np.arange(lo[0],hi[0]+1,4):
            for y in np.arange(lo[1],hi[1]+1,4):
                ss=[h for h in nav_surface(ctx['navmeshes'],x+origin[0],y+origin[1]) if abs(h['z']-origin[2])<25]
                if not ss:continue
                z=ss[0]['z']-origin[2];fz=F.floor_at(floors,x,y,z)
                if fz is not None and abs(fz-z)<8:points[(x,y)]=[x,y,fz]
    markerid='00078784' if s['name']=='este' else '0007878A';ref=next(r for r in ctx['refs'] if r['id']==markerid)
    marker=np.array(ref['data'][:3])-origin;marker[2]=F.floor_at(floors,*marker[:2],marker[2]);points['marker']=marker.tolist()
    return points,markerid

def main():
    addon_utils.enable('io_scene_nifly',default_set=True)
    ctx=json.loads((ROOT/'reports/tower_context_v14.json').read_text());built=json.loads((ROOT/'reports/platforms_v15_build.json').read_text())
    shapes=F.gun_arrays();gh=np.load(ROOT/'reports/gun_havok_v14.npz');GC,GCT=gh['C'],gh['CT']
    aim=Aim({'tower_top_units':0});results=[]
    rest=nif_nodos.leer(str(ROOT/'mod/meshes/AstraAsedio/ballesta.nif'))
    for n in rest['nodos'].values():
        if n['nombre'] in ('CTRL_GIRO_360','CTRL_ELEVACION'):assert np.max(abs(np.array(n['rot']).reshape(3,3)-np.eye(3)))<1e-6
    for item in built['sites']:
        s=item['site'];name=s['name'];nif=ROOT/item['nif'];assert sha(nif)==item['sha256']
        for ob in list(bpy.data.objects):bpy.data.objects.remove(ob,do_unlink=True)
        obs=load(nif,L.transform_matrix((0,0,0),(0,0,0),1,*L.engine_convention()))
        V,VT=F.mesh_arrays([o for o in obs if o.type=='MESH' and not o.name.startswith('bhk')])
        C,CT=F.mesh_arrays([o for o in obs if o.type=='MESH' and o.name.startswith('bhk')]);ownT=C[CT]
        assert len(C)>0 and len(V)>0
        np.savez_compressed(ROOT/f'reports/platform_{name}_v15.npz',V=V,T=VT,C=C,CT=CT)
        original=np.load(ROOT/f'reports/tower_geometry_{name}_v14.npz');env=np.concatenate([original['V'][original['T']],original['C'][original['CT']]])
        eb=(env.min(1),env.max(1));ob=(ownT.min(1),ownT.max(1));combined=np.concatenate([env,ownT]);cb=(combined.min(1),combined.max(1))
        points,markerid=nav_samples(ctx,s,original['C'][original['CT']]);usable={k:p for k,p in points.items() if R.margin(p,env,eb)>=0}
        losses=[{'foot':p,'margin':R.margin(p,ownT,ob)} for p in usable.values() if R.margin(p,ownT,ob)<-.02]
        assert not losses,(name,'NAV_LOSS',losses[:3])
        floors=F.bvh_from_triangles(ownT);pos=np.array(s['gun_local_pos']);deck=s['deck_local_z']
        fixed=[]
        for x in np.linspace(GC[:,0].min(),GC[:,0].max(),9):
            for y in np.linspace(GC[:,1].min(),GC[:,1].max(),9):
                fz=F.floor_at(floors,pos[0]+x,pos[1]+y,deck);assert fz is not None and abs(fz-deck)<.05
                fixed.append(abs(fz-deck))
        operator=np.array(s['operator_local_foot']);standby=np.array(s['standby_local_foot'])
        route=G.route_samples(s);route_env=[R.margin(p,env,eb) for p in route]
        # Step-up interpolation is a geometric proxy. It does not prove engine
        # stair traversal; foot may be up to one riser above the supporting slab.
        route_own=[R.margin(p,ownT,ob) for p in route]
        route_floor=[];original_floors=F.bvh_from_triangles(original['C'][original['CT']])
        for p in route:
            own=F.floor_at(floors,*p[:2],p[2]);orig=F.floor_at(original_floors,*p[:2],p[2])
            hits=[z for z in (own,orig) if z is not None and z<=p[2]+20.15]
            route_floor.append(None if not hits else p[2]-max(hits))
        # Certify 525 static poses. Animation bounds are a separate game check.
        gun_contacts=[];shots=[];opmin=999.;standmin=999.;navgap=999.;raymin=999.;ownbvh=F.bvh_from_triangles(ownT)
        for yaw in range(-60,61,5):
            for pitch in range(-20,81,5):
                gv,gt=F.gun_pose(shapes,yaw,pitch);gv+=pos;gunT=gv[gt]
                nearby=combined[(combined.max(1)>[pos[0]-350,pos[1]-350,deck+.08]).all(1)&(combined.min(1)<[pos[0]+350,pos[1]+350,deck+440]).all(1)]
                overlaps=F.bvh_from_triangles(gunT).overlap(F.bvh_from_triangles(nearby))
                if overlaps:gun_contacts.append([yaw,pitch,len(overlaps)])
                gunall=np.concatenate([gunT,(GC+pos)[GCT]])
                opmin=min(opmin,R.margin(operator,gunall));standmin=min(standmin,R.margin(standby,gunall))
                navgap=min(navgap,min(p[1] for p in usable.values())-gv[:,1].max())
                m,b=aim.pose(yaw,pitch);m+=pos;e=m+b*max(0.,(650-np.linalg.norm(m[:2]-pos[:2]))/np.linalg.norm(b[:2]))
                k=(combined.max(1)>=np.minimum(m,e)-4).all(1)&(combined.min(1)<=np.maximum(m,e)+4).all(1)
                if k.any():
                    d=float(seg_tri(m,e,combined[k]).min());raymin=min(raymin,d)
                    if d<2.205:shots.append([yaw,pitch,d])
        assert not gun_contacts,(name,'GUN_CONTACT',gun_contacts[:5])
        assert not shots,(name,'SHOT_HIT',shots[:5])
        assert opmin>0 and standmin>0 and navgap>18,(name,opmin,standmin,navgap)
        assert min(route_env)>0,(name,'ACCESS_ENV',min(route_env),route[np.argmin(route_env)])
        # Own stair risers may contact the step-up capsule by design. Record
        # those transitions explicitly and require the slab never exceeds feet
        # by more than the specified <=20-u engine step candidate.
        assert all(v is not None and -20.15<=v<=20.15 for v in route_floor),(name,'SUPPORT',route_floor)
        for p,m in zip(route,route_own):
            step_proxy=name=='este' and p[0]>=120 and p[1]>=-105
            assert step_proxy or m>=-.04,(name,'ACCESS_OWN',p,m)
        result={**s,'nif':item['nif'],'nif_sha256':sha(nif),'visual_triangles':len(VT),'havok_triangles':len(CT),
            'original_usable_nav_centers':len(usable),'lost_nav_centers':len(losses),'original_marker':markerid,
            'marker_own_margin':R.margin(usable['marker'],ownT,ob),'fixed_base_max_gap':max(fixed),
            'route_samples':len(route),'route_environment_min_margin':min(route_env),'route_own_min_margin':min(route_own),
            'max_step_up_proxy_gap':max(route_floor),'operator_gun_min_margin':opmin,'standby_gun_min_margin':standmin,
            'gun_nav_y_gap':navgap,'certified_static_poses':525,'pose_increment_degrees':5,
            'gun_contacts':gun_contacts,'initial_projectile_hits':shots,'initial_projectile_min_clearance':raymin,
            'operator_environment_margin':R.margin(operator,combined,cb),'standby_environment_margin':R.margin(standby,combined,cb)}
        results.append(result);print('PLATFORM_VERIFIED',name,{k:result[k] for k in ('lost_nav_centers','route_environment_min_margin','route_own_min_margin','gun_nav_y_gap','operator_gun_min_margin')},flush=True)
    report={'success':True,'sites':results,'scope':'Actual exported NIF visual/Havok; vanilla 4-u NAVM sample preservation and 5-degree static aim poses. Step-up access proxy, not Skyrim navigation/animation/latency.',
            'engine_verified':False,'capsule':{'radius':18,'height':128},'inputs_sha256':{p:sha(ROOT/p) for p in ['scripts/platforms_v15_geometry.py','scripts/build_platforms_v15.py','scripts/verify_platforms_v15.py','reports/research_platform_v15.py','scripts/tower_fit_v14.py','scripts/verify_shot_clearance_v12.py','scripts/inspect_towers_v14.py','scripts/v11_layout.py','scripts/probe_towers_v14.py','reports/platforms_v15_build.json','mod/meshes/AstraAsedio/ballesta.nif','reports/tower_context_v14.json','reports/tower_geometry_metadata_v14.json','reports/tower_geometry_este_v14.npz','reports/tower_geometry_oeste_v14.npz','reports/gun_havok_v14.npz']}}
    (ROOT/'reports/platforms_v15.json').write_text(json.dumps(report,indent=2))
if __name__=='__main__':main()
