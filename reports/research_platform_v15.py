"""Read-only v15 platform research. All outputs are reports; input assets unchanged."""
import sys,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import tower_fit_v14 as F
from verify_shot_clearance_v12 import seg_tri, Aim
from mathutils import Vector
from mathutils.bvhtree import BVHTree

def zhits(T,x,y):
    A,B,C=T[:,0],T[:,1],T[:,2]
    den=(B[:,1]-C[:,1])*(A[:,0]-C[:,0])+(C[:,0]-B[:,0])*(A[:,1]-C[:,1])
    valid=abs(den)>1e-8
    d=np.where(valid,den,1)
    u=((B[:,1]-C[:,1])*(x-C[:,0])+(C[:,0]-B[:,0])*(y-C[:,1]))/d
    v=((C[:,1]-A[:,1])*(x-C[:,0])+(A[:,0]-C[:,0])*(y-C[:,1]))/d
    keep=valid&(u>=-1e-6)&(v>=-1e-6)&(u+v<=1+1e-6)
    z=u*A[:,2]+v*B[:,2]+(1-u-v)*C[:,2]
    return sorted(set(round(float(a),3) for a in z[keep]))

def navtops(ctx,origin):
    out=[]
    for m in ctx['navmeshes']:
        if m.get('deleted'):continue
        for i,t in enumerate(m['triangles']):
            pts=np.array([m['vertices'][k] for k in t[:3]])-origin
            if (abs(pts[:,:2])<350).all() and (abs(pts[:,2])<20).all():
                out.append({'mesh':m['id'],'index':i,'vertices':pts.tolist()})
    return out

def scan():
    ctx=json.loads((ROOT/'reports/tower_context_v14.json').read_text());out={}
    for req in ctx['requests']:
        g=np.load(ROOT/f'reports/tower_geometry_{req["name"]}_v14.npz')
        VT=g['V'][g['T']];CT=g['C'][g['CT']];T=np.concatenate([VT,CT]);origin=np.array(req['requested'])
        k=(T.max(1)>[-550,-700,-30]).all(1)&(T.min(1)<[550,400,650]).all(1);T=T[k]
        samples={}
        for x in (-160,-120,-80,-40,0,40,80,120,160):
            samples[str(x)]=[[y,zhits(T,x,y)] for y in range(-320,141,20)]
        out[req['name']]={'origin':origin.tolist(),'nav':navtops(ctx,origin),'south_vertical_samples':samples}
    (ROOT/'reports/v15_platform_profiles.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

def route_points(nodes,spacing=4):
    out=[]
    for a,b in zip(nodes[:-1],nodes[1:]):
        a=np.array(a,dtype=float);b=np.array(b,dtype=float)
        for t in np.linspace(0,1,max(2,int(math.ceil(np.linalg.norm(b-a)/spacing))+1)):
            out.append(a+(b-a)*t)
    return out

def margin(p,T,bounds=None):
    # Existing floors and solids lying completely below the foot do not block
    # the actor. All upper/side triangles remain in the swept capsule check.
    lo,hi=bounds if bounds is not None else (T.min(1),T.max(1))
    k=(hi>np.array(p)+[-80,-80,.05]).all(1)&(lo<np.array(p)+[80,80,130]).all(1)
    if not k.any():return 62.
    return min(62.,float(seg_tri(np.array(p)+[0,0,18],np.array(p)+[0,0,110],T[k]).min()-18))

def routes_only():
    g=np.load(ROOT/'reports/tower_geometry_este_v14.npz');T=np.concatenate([g['V'][g['T']],g['C'][g['CT']]])
    bounds=(T.min(1),T.max(1));floor=-.354012;deck=floor+72;options=[]
    for sy in (-50,):
        route=route_points([[110,sy,floor],[122,sy,floor]])
        for i in range(3):
            z=floor+(i+1)*20
            route+=route_points([[145+i*10,sy,z],[150+i*10,sy,z]])
        route+=route_points([[170,sy,floor+60],[174,-78,floor+60]])
        route+=route_points([[174,-78,deck],[174,-102,deck]])
        route+=route_points([[174,-102,deck],[174,-150,deck],[96,-150,deck],[96,-240,deck],[210,-300,deck],[124,-356,deck]])
        mm=[margin(p,T,bounds) for p in route];wi=int(np.argmin(mm))
        wp=route[wi];k=(bounds[1]>wp+[-80,-80,.05]).all(1)&(bounds[0]<wp+[80,80,130]).all(1)
        dd=seg_tri(wp+[0,0,18],wp+[0,0,110],T[k]);tri=T[k][np.argmin(dd)]
        options.append({'y':sy,'margin':min(mm),'worst':wp.tolist(),'triangle':tri.tolist(),'vertical_hits':zhits(T,wp[0],wp[1]),'points':len(route)})
    print(json.dumps(options,indent=2),flush=True)
    (ROOT/'reports/v15_platform_access_options.json').write_text(json.dumps(options,indent=2))

def support_refs():
    import bpy,addon_utils
    from probe_towers_v14 import load
    import v11_layout as L
    addon_utils.enable('io_scene_nifly',default_set=True)
    cfg=json.loads((ROOT/'config.json').read_text());ctx=json.loads((ROOT/'reports/tower_context_v14.json').read_text());out=[]
    for name,fid,z in [('este','00089F3F',-280),('oeste','00042516',-280)]:
        req=next(q for q in ctx['requests'] if q['name']==name);ref=next(r for r in ctx['refs'] if r['id']==fid)
        for ob in list(bpy.data.objects):bpy.data.objects.remove(ob,do_unlink=True)
        model=Path(cfg['extracted'])/'meshes'/ref['donor']['model']
        tr=L.transform_matrix([a-b for a,b in zip(ref['data'][:3],req['requested'])],[math.degrees(a) for a in ref['data'][3:]],ref['scale'],*L.engine_convention())
        obs=load(model,tr);C,CT=F.mesh_arrays([o for o in obs if o.type=='MESH' and o.name.startswith('bhk')]);bvh=F.bvh_from_triangles(C[CT]);hits=[]
        for x in (-120,-96,96,120):
            hit=bvh.ray_cast(Vector((x,-700,z)),Vector((0,1,0)),750)
            hits.append({'x':x,'point':list(hit[0]) if hit[0] is not None else None,'normal':list(hit[1]) if hit[1] is not None else None})
        out.append({'name':name,'ref':fid,'model':ref['donor']['model'],'z':z,'hits':hits})
    (ROOT/'reports/v15_platform_support_refs.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2),flush=True)

def nav_check():
    from verify_shot_clearance_v12 import box_triangles
    from inspect_towers_v14 import nav_surface
    ctx=json.loads((ROOT/'reports/tower_context_v14.json').read_text());out=[]
    for req in ctx['requests']:
        name=req['name'];origin=np.array(req['requested']);g=np.load(ROOT/f'reports/tower_geometry_{name}_v14.npz');T=np.concatenate([g['V'][g['T']],g['C'][g['CT']]])
        bd=(T.min(1),T.max(1));floors=F.bvh_from_triangles(g['C'][g['CT']]);nav=navtops(ctx,origin);pts={}
        for tri in nav:
            v=np.array(tri['vertices']);lo=np.floor(v[:,:2].min(0)/4)*4;hi=np.ceil(v[:,:2].max(0)/4)*4
            for x in np.arange(lo[0],hi[0]+1,4):
                for y in np.arange(lo[1],hi[1]+1,4):
                    ss=nav_surface(ctx['navmeshes'],x+origin[0],y+origin[1]);on=[s for s in ss if abs(s['z']-origin[2])<25]
                    if not on:continue
                    nz=on[0]['z']-origin[2];fz=F.floor_at(floors,x,y,nz)
                    if fz is None or abs(fz-nz)>8:continue
                    p=np.array([x,y,fz]);em=margin(p,T,bd)
                    if em>=0:pts[(x,y)]={'foot':p.tolist(),'margin':em}
        markerid='00078784' if name=='este' else '0007878A';mr=next(r for r in ctx['refs'] if r['id']==markerid);marker=np.array(mr['data'][:3])-origin
        mf=F.floor_at(floors,*marker[:2],marker[2]);marker[2]=mf if mf is not None else marker[2]
        points=list(pts.values())+[{'foot':marker.tolist(),'margin':margin(marker,T,bd),'marker':markerid}]
        floor=-.354012
        variants={}
        if name=='este':
            for sx in (145,146,148):
                boxes=[([128,-78,floor-12],[sx,-22,floor]),([sx,-78,floor-12],[sx+16,-22,floor+20]),([sx+16,-78,floor-12],[sx+32,-22,floor+40])]
                # Main south flight/crosswalk lies outside original top NAVM.
                for i in range(2):boxes.append(([146,-50-(i+1)*24,floor-12],[202,-50-i*24,floor+56+i*16]))
                boxes += [([146,-150,floor+60],[202,-98,floor+72]),([68,-178,floor+60],[174,-122,floor+72]),([68,-240,floor+60],[124,-150,floor+72])]
                variants[str(sx)]=boxes
        else:variants['flat']=[([-36,-180,floor-12],[36,-126,floor]),([-260,-630,floor-12],[260,-180,floor])]
        findings={}
        for key,boxes in variants.items():
            NT=np.concatenate([box_triangles(a,b) for a,b in boxes]);NB=(NT.min(1),NT.max(1));loss=[];remain=[];markercheck=None
            for sp in points:
                nm=margin(sp['foot'],NT,NB)
                if sp.get('marker'):markercheck={'foot':sp['foot'],'old_margin':sp['margin'],'new_margin':nm}
                if nm<0:loss.append({'foot':sp['foot'],'old_margin':sp['margin'],'new_margin':nm})
                else:remain.append({'foot':sp['foot'],'new_margin':nm})
            findings[key]={'lost_centers':len(loss),'first_lost':loss[:15],'loss_bounds':None if not loss else [np.min([p['foot'] for p in loss],axis=0).tolist(),np.max([p['foot'] for p in loss],axis=0).tolist()],'remaining':len(remain),'marker':markercheck,'boxes':[[a,b] for a,b in boxes]}
        profile=[[x,[z for z in zhits(T,x,-50) if -5<z<100]] for x in range(120,181,2)] if name=='este' else []
        out.append({'name':name,'usable_original_centers':len(points),'findings':findings,'entry_side_surface_profile_y_minus50':profile})
        print(name,len(points),[(k,v['lost_centers'],v['marker']) for k,v in findings.items()],flush=True)
    (ROOT/'reports/v15_platform_nav_buffer.json').write_text(json.dumps(out,indent=2))

def proposal():
    ctx=json.loads((ROOT/'reports/tower_context_v14.json').read_text());out=[]
    shapes=F.gun_arrays();aim=Aim({'tower_top_units':0});gh=np.load(ROOT/'reports/gun_havok_v14.npz')
    GC,GCT=gh['C'],gh['CT'];base=float(GC[:,2].min())
    for req in ctx['requests']:
        name=req['name'];origin=np.array(req['requested']);g=np.load(ROOT/f'reports/tower_geometry_{name}_v14.npz')
        T=np.concatenate([g['V'][g['T']],g['C'][g['CT']]])
        floor=-.354012
        if name=='este':
            deck=floor+72;pos=np.array([0.,-500.,deck-base]);poly=[[-260,-710],[260,-710],[260,-240],[-260,-240]]
            path=[[110,0,floor],[160,0,floor],[160,-50,floor]]
            # Stairs have six 12-u rises /18-u runs, all x>=132 beyond NAVM.
            step_points=[]
            for i in range(6):
                z=floor+(i+1)*12
                step_points+=route_points([[160,-50-i*18,z],[160,-50-(i+1)*18,z]])
            step_points+=route_points([[160,-158,deck],[160,-280,deck],[210,-300,deck],[124,-356,deck]])
            standby=np.array([-210.,-280.,deck]);gangway={'bounds_xy':[132,-240,188,-158],'connector':[128,-50,188,20],'step_bounds':[132,-158,188,-50],'rises':6,'rise':12,'run':18}
        else:
            deck=floor;pos=np.array([0.,-420.,deck-base]);poly=[[-260,-630],[260,-630],[260,-180],[-260,-180]]
            path=[[0,-100,floor],[0,-126,floor],[0,-180,floor],[210,-180,floor],[210,-250,floor],[124,-276,floor]];step_points=[]
            standby=np.array([-210.,-210.,deck]);gangway={'bounds_xy':[-36,-180,36,-126],'flat':True}
        route=route_points(path)+step_points
        op=pos+np.array([124.,144.,base])
        envroutes=[margin(p,T) for p in route]
        worsti=int(np.argmin(envroutes))
        envop=margin(op,T);envstand=margin(standby,T)
        # Test static collision, all upper visual geometry and the actor against
        # the actual gun at 5-degree increments; dense certification follows.
        keep=(T.max(1)>[pos[0]-350,pos[1]-350,deck+.08]).all(1)&(T.min(1)<[pos[0]+350,pos[1]+350,deck+440]).all(1)
        near=T[keep];envbvh=F.bvh_from_triangles(near);static_havok=GC+pos;static_tri=static_havok[GCT]
        contacts=[];opworst={'margin':999.};standworst={'margin':999.};bboxlo=np.array([math.inf]*3);bboxhi=-bboxlo
        shots=[];shotworst={'clearance':999.};routegunworst={'margin':999.}
        for y in range(-60,61,5):
            for p in range(-20,81,5):
                V,GT=F.gun_pose(shapes,y,p);V+=pos;gunT=V[GT];gunb=F.bvh_from_triangles(gunT)
                ov=gunb.overlap(envbvh)
                if ov:contacts.append({'yaw':y,'pitch':p,'pairs':len(ov)})
                bboxlo=np.minimum(bboxlo,V.min(0));bboxhi=np.maximum(bboxhi,V.max(0))
                combined=np.concatenate([gunT,static_tri]);om=margin(op,combined);sm=margin(standby,combined)
                if om<opworst['margin']:opworst={'margin':om,'yaw':y,'pitch':p}
                if sm<standworst['margin']:standworst={'margin':sm,'yaw':y,'pitch':p}
                # Access points within 300u of the axis; neutral guard can be
                # tracked from original approach through the outer corridor.
                for rp in route:
                    if np.linalg.norm(np.array(rp[:2])-pos[:2])>300:continue
                    rm=margin(rp,combined)
                    if rm<routegunworst['margin']:routegunworst={'margin':rm,'point':rp.tolist(),'yaw':y,'pitch':p}
                m,b=aim.pose(y,p);m+=pos;e=m+b*max(0.,(600.-np.linalg.norm(m[:2]-pos[:2]))/np.linalg.norm(b[:2]))
                k=(T.max(1)>=np.minimum(m,e)-4).all(1)&(T.min(1)<=np.maximum(m,e)+4).all(1)
                if k.any():
                    d=float(seg_tri(m,e,T[k]).min())
                    if d<shotworst['clearance']:shotworst={'clearance':d,'yaw':y,'pitch':p}
                    if d<2.205:shots.append({'yaw':y,'pitch':p,'clearance':d})
        nav=navtops(ctx,origin);NP=np.concatenate([np.array(n['vertices']) for n in nav]);navmin=NP.min(0);navmax=NP.max(0)
        # Written-Havok horizontal rays find the south facing support surface.
        envfull=F.bvh_from_triangles(g['C'][g['CT']]);anchors=[]
        for x in (-120,-96,-80,80,96,120):
            for z in (-64,-120,-200,-280):
                hit=envfull.ray_cast(Vector((x,-700,z)),Vector((0,1,0)),750)
                if hit[0] is not None:anchors.append({'point':[round(float(q),3) for q in hit[0]],'normal':[round(float(q),3) for q in hit[1]],'probe_x':x,'probe_z':z})
        data={'name':name,'origin':origin.tolist(),'floor_local_z':floor,'deck_local_z':deck,'main_deck_polygon':poly,'access':gangway,'gun_local_pos':pos.tolist(),'gun_world_pos':(pos+origin).tolist(),'scale':1.,'yaw_deg':0.,'yaw_range':[-60,60],'pitch_range':[-20,80],'operator_local_foot':op.tolist(),'operator_world_foot':(op+origin).tolist(),'standby_local_foot':standby.tolist(),'standby_world_foot':(standby+origin).tolist(),'crank_distance_xy':float(np.linalg.norm(np.array([124,144])-np.array([73.5,101.5]))),'route':path,'route_samples':len(route),'route_environment_worst':{'margin':min(envroutes),'point':route[worsti].tolist()},'operator_env_margin':envop,'standby_env_margin':envstand,'coarse_poses':25*21,'gun_environment_contacts':contacts,'operator_gun_worst':opworst,'standby_gun_worst':standworst,'route_gun_worst':routegunworst,'shot_hits':shots,'shot_worst':shotworst,'gun_envelope_min':bboxlo.tolist(),'gun_envelope_max':bboxhi.tolist(),'original_nav_min':navmin.tolist(),'original_nav_max':navmax.tolist(),'gun_nav_y_gap':float(navmin[1]-bboxhi[1]),'operator_capsule_nav_y_gap':float(navmin[1]-(op[1]+18)),'standby_capsule_nav_y_gap':float(navmin[1]-(standby[1]+18)),'support_surface_probes':anchors,'engine_verified':False}
        out.append(data);print(name,'routeEnv',data['route_environment_worst'],'opGun',opworst,'routeGun',routegunworst,'overlap',len(contacts),'navgap',data['gun_nav_y_gap'],flush=True)
    (ROOT/'reports/v15_platform_proposal.json').write_text(json.dumps({'sites':out,'capsule':{'radius':18,'height':128},'pose_sampling_deg':5,'scope':'Numerical proposal; does not prove Skyrim pathing, final collision, animation bounds or structural strength.'},indent=2))

if __name__=='__main__':
    if 'proposal' in sys.argv:proposal()
    elif 'routes' in sys.argv:routes_only()
    elif 'supports' in sys.argv:support_refs()
    elif 'nav' in sys.argv:nav_check()
    else:scan()
