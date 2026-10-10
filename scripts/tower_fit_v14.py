"""Measure a stock ballista against winning vanilla tower geometry.

All writes stay in scripts/reports/renders. NIFs and masters are read only.
Blender --python this_file -- dump imports the written Havok and visual meshes.
Python this_file search consumes that geometry; Blender render consumes selection.
"""
import hashlib,json,math,sys,struct
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
import v11_layout as L
from inspect_towers_v14 import nav_surface
from verify_shot_clearance_v12 import Aim,seg_tri,node_matrices,rz,rx,box_triangles
BASE=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v13')
REPORTS=ROOT/'reports'
GUN=ROOT/'mod/meshes/AstraAsedio/ballesta.nif'

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def mesh_arrays(objs):
    vs=[];ts=[]
    for o in objs:
        if o.type!='MESH':continue
        o.data.calc_loop_triangles();base=len(vs)
        vs.extend(tuple(o.matrix_world@v.co) for v in o.data.vertices)
        ts.extend(tuple(base+i for i in t.vertices) for t in o.data.loop_triangles)
    return np.array(vs).reshape(-1,3),np.array(ts,dtype=np.int32).reshape(-1,3)

def context_import(req,cfg,context):
    import bpy
    from probe_towers_v14 import load
    origin=req['requested'];visual=[];coll=[];metadata=[]
    for ref in context['refs']:
        if ref['deleted']:continue
        model=ref['donor'].get('model','')
        if not model.lower().startswith(('architecture\\','landscape\\rocks\\','clutter\\')):continue
        path=Path(cfg['extracted'])/'meshes'/model
        if not path.exists():continue
        # Include the entire collected 950-u reference set: large wall pieces
        # can extend across the target even when their origins are farther away.
        m=L.transform_matrix([a-b for a,b in zip(ref['data'][:3],origin)],
                             [math.degrees(a) for a in ref['data'][3:]],ref['scale'],*L.engine_convention())
        objs=load(path,m);v=[o for o in objs if o.type=='MESH' and not o.name.startswith('bhk')]
        c=[o for o in objs if o.type=='MESH' and o.name.startswith('bhk')]
        for o in objs:o['vanilla_reference']=ref['id']
        visual+=v;coll+=c
        V,T=mesh_arrays(v+c)
        metadata.append({'ref':ref['id'],'model':model,'sha256':sha(path),
                         'visual_meshes':len(v),'havok_meshes':len(c),
                         'bounds_min':V.min(0).tolist() if len(V) else None,
                         'bounds_max':V.max(0).tolist() if len(V) else None})
    return visual,coll,metadata

def gun_arrays():
    import nif_nodos,nif_fisica
    nif=nif_nodos.leer(str(GUN));d=nif['datos'];nodes=nif['nodos']
    parents={child:i for i,n in nodes.items() for child in n['hijos']}
    world=nif_fisica._mundo_padre(nif)
    out=[]
    for i,name,o,local,sh,a,desc,nv,datos in nif_fisica._shapes(nif):
        nt=struct.unpack_from('<H',d,datos-8)[0];stride=(desc&15)*4
        m=np.array(nif_fisica._mul(world(i),local))
        V=np.array([struct.unpack_from('<3f',d,datos+k*stride) for k in range(nv)])
        V=V@m[:,:3].T+m[:,3]
        T=np.array([struct.unpack_from('<3H',d,datos+nv*stride+k*6) for k in range(nt)],dtype=np.int32)
        chain=[];p=parents.get(i)
        while p is not None:chain.append(nodes[p]['nombre']);p=parents.get(p)
        out.append({'name':name,'V':V,'T':T,'pitch':'CTRL_ELEVACION' in chain,'yaw':'CTRL_GIRO_360' in chain})
    return out

def gun_pose(shapes,yaw,pitch):
    verts=[];tris=[]
    for sh in shapes:
        V=sh['V'].copy()
        if sh['pitch']:V=(V-np.array([0,0,153]))@rx(-math.radians(pitch))[:3,:3].T+np.array([0,0,153])
        if sh['yaw']:V=(V-np.array([0,0,135.5]))@rz(math.radians(yaw))[:3,:3].T+np.array([0,0,135.5])
        tris.append(sh['T']+sum(len(v) for v in verts));verts.append(V)
    return np.concatenate(verts),np.concatenate(tris)

def dump():
    import bpy,addon_utils
    from probe_towers_v14 import load
    cfg=json.loads((BASE/'config.json').read_text());context=json.loads((REPORTS/'tower_context_v14.json').read_text())
    addon_utils.enable('io_scene_nifly',default_set=True)
    bpy.context.preferences.addons['io_scene_nifly'].preferences.sky_texture_path_1=str(Path(cfg['extracted'])/'textures')
    metadata=[]
    for req in context['requests']:
        for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
        visual,coll,refs=context_import(req,cfg,context)
        V,T=mesh_arrays(visual);C,CT=mesh_arrays(coll)
        # keep imported collider winding, but floor detection also accepts
        # either face orientation by checking an unsigned normal.
        np.savez_compressed(REPORTS/f'tower_geometry_{req["name"]}_v14.npz',V=V,T=T,C=C,CT=CT)
        metadata.append({'name':req['name'],'visual_triangles':len(T),'havok_triangles':len(CT),'refs':refs})
        print('DUMPED',req['name'],V.shape,T.shape,C.shape,CT.shape,flush=True)
    for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
    gun=load(GUN,L.transform_matrix((0,0,0),(0,0,0),1,*L.engine_convention()))
    C,CT=mesh_arrays([o for o in gun if o.type=='MESH' and o.name.startswith('bhk')])
    np.savez_compressed(REPORTS/'gun_havok_v14.npz',C=C,CT=CT)
    shapes=gun_arrays();V,T=gun_pose(shapes,0,0)
    (REPORTS/'tower_geometry_metadata_v14.json').write_text(json.dumps({'inputs_sha256':{'gun':sha(GUN),'context':sha(REPORTS/'tower_context_v14.json'),'script':sha(__file__)},'sites':metadata,
      'gun_shapes':[{'name':s['name'],'yaw':s['yaw'],'pitch':s['pitch'],'bounds_min':s['V'].min(0).tolist(),'bounds_max':s['V'].max(0).tolist(),'vertices':len(s['V']),'triangles':len(s['T'])} for s in shapes],
      'gun_visual_min':V.min(0).tolist(),'gun_visual_max':V.max(0).tolist(),'gun_havok_min':C.min(0).tolist(),'gun_havok_max':C.max(0).tolist()},indent=2))

def bvh_from_triangles(T):
    from mathutils.bvhtree import BVHTree
    return BVHTree.FromPolygons(T.reshape(-1,3).tolist(),np.arange(len(T)*3).reshape(-1,3).tolist(),all_triangles=True)

def floor_at(bvh,x,y,z):
    from mathutils import Vector
    hit=bvh.ray_cast(Vector((x,y,z+30)),Vector((0,0,-1)),60)
    if hit[0] is None or abs(hit[1].z)<.8:return None
    return float(hit[0].z)

def capsule_margin(p,T,bounds=None):
    # An 82-u window contains every triangle closer than radius18 + margin64
    # to the capsule axis. Outside triangles are provably farther than82;
    # reported positive values are capped at a conservative64-u lower bound.
    lo=np.array(p)+np.array([-82,-82,-64]);hi=np.array(p)+np.array([82,82,192])
    tri_lo,tri_hi=bounds if bounds is not None else (T.min(1),T.max(1))
    k=(tri_hi>=lo).all(1)&(tri_lo<=hi).all(1)
    subset=T[k]
    # Floor triangles are allowed to touch the bottom of the capsule.
    if not len(subset):return 64.
    return float(min(64.,seg_tri(np.array(p)+[0,0,18],np.array(p)+[0,0,110],subset).min()-18))

def world_transform(V,pos,yaw):
    R=np.array(L.transform_matrix((0,0,0),(0,0,yaw),1,*L.engine_convention())['r'])
    return V@R.T+np.array(pos)

def search(scale=1.,refine=False,scope='all'):
    """Rank fully supported static placements before certifying moving sectors."""
    from mathutils import Vector
    context=json.loads((REPORTS/'tower_context_v14.json').read_text());metadata=json.loads((REPORTS/'tower_geometry_metadata_v14.json').read_text())
    shapes=gun_arrays();GV,GT=gun_pose(shapes,0,0);GV*=scale
    gh=np.load(REPORTS/'gun_havok_v14.npz');GC,GCT=gh['C']*scale,gh['CT']
    base_min=float(min(GV[:,2].min(),GC[:,2].min()))
    feet=GC[GC[:,2]<=base_min+.001];feet=np.unique(feet,axis=0)
    # Interior support samples prevent a bridge over a stairwell or deck gap.
    support=np.array([[x,y,base_min] for x in np.linspace(GC[:,0].min(),GC[:,0].max(),9)
                       for y in np.linspace(GC[:,1].min(),GC[:,1].max(),9)])
    aim=Aim({'tower_top_units':0});results=[]
    for req in context['requests']:
        if scope!='all' and req['name']!=scope:continue
        geom=np.load(REPORTS/f'tower_geometry_{req["name"]}_v14.npz');origin=np.array(req['requested'])
        VT=geom['V'][geom['T']];CT=geom['C'][geom['CT']];allT=np.concatenate([VT,CT])
        floors=bvh_from_triangles(CT);fz=floor_at(floors,0,0,0)
        # Full visual and written collision within the mounting envelope.
        keep=(allT.max(1)>[-520,-520,fz+.08]).all(1)&(allT.min(1)<[520,520,fz+520]).all(1)
        near=allT[keep];near_bounds=(near.min(1),near.max(1));obstacles=bvh_from_triangles(near)
        candidates=[];counts={};rejections={};examples=[];operator_failures=[]
        for yaw in ((0,) if scope!='all' else (0,15,345,30,330,45,315) if refine else (0,45,315,90,270,135,225,180)):
            count=0;rejected={'floor':0,'support':0,'gun_static':0,'operator':0}
            for dx in range(-136,137,8):
                for dy in range(-136,137,8):
                    z=floor_at(floors,dx,dy,fz)
                    if z is None or abs(z-fz)>1:rejected['floor']+=1;continue
                    pos=np.array([dx,dy,z-base_min]);W=world_transform(support,pos,yaw)
                    footW=world_transform(feet,pos,yaw)
                    cornerz=[floor_at(floors,p[0],p[1],z) for p in footW]
                    if any(v is None or abs(v-z)>2. for v in cornerz):rejected['support']+=1;continue
                    zs=[floor_at(floors,p[0],p[1],z) for p in W]
                    if any(v is None or abs(v-z)>2. for v in zs):
                        rejected['support']+=1
                        if dx==0 and dy==0:print('SUPPORT_CENTER',req['name'],yaw,z,[(W[i].round(2).tolist(),v) for i,v in enumerate(zs) if v is None or abs(v-z)>.25][:8],flush=True)
                        continue
                    # A small raised rim is allowed within the measured 2-u
                    # floor tolerance, with every base corner's gap disclosed.
                    support_z=max(zs);pos[2]=support_z-base_min
                    WG=world_transform(GV,pos,yaw);guntree=bvh_from_triangles(WG[GT])
                    overlap=guntree.overlap(obstacles)
                    if overlap:
                        rejected['gun_static']+=1
                        if len(examples)<20:
                            examples.append({'offset':pos.tolist(),'yaw':yaw,'overlap_pairs':len(overlap),'gun_triangle':world_transform(GV,pos,yaw)[GT[overlap[0][0]]].tolist(),'obstacle_triangle':near[overlap[0][1]].tolist()})
                        continue
                    worldgun=WG[GT];gc=world_transform(GC,pos,yaw)[GCT]
                    combined_gun=np.concatenate([worldgun,gc]);gun_bounds=(combined_gun.min(1),combined_gun.max(1))
                    operators=[]
                    local_options=[(73.5,132),(73.5,144),(91.5,126),(91.5,144),(108,120),(108,144),(55.5,150),(108,102),(120,84),(126,64),(108,64),(126,102),(73.5,64),(-73.5,132),(-91.5,144)]
                    if refine:local_options+=[(x,y) for x in range(100,173,8) for y in range(24,161,8)
                                             if math.hypot(x-73.5,y-101.5)*scale<=70]
                    debug=[]
                    for local in local_options:
                        p=world_transform(np.array([[*local,0.]])*scale,pos,yaw)[0]
                        gz=floor_at(floors,p[0],p[1],z)
                        if gz is None or abs(gz-z)>2.:continue
                        p[2]=gz
                        ns=[n for n in nav_surface(context['navmeshes'],*(p[:2]+origin[:2])) if abs(n['z']-(gz+origin[2]))<=8]
                        if not ns:continue
                        # Bare minimum center plus surrounding capsule footprint.
                        if any(floor_at(floors,p[0]+18*math.cos(a),p[1]+18*math.sin(a),gz) is None for a in np.linspace(0,math.tau,17)[:-1]):continue
                        envmargin=capsule_margin(p,near,near_bounds);gunmargin=capsule_margin(p,combined_gun,gun_bounds)
                        debug.append({'local':local,'env':envmargin,'gun':gunmargin,'nav':ns})
                        if min(envmargin,gunmargin)<.05:continue
                        crank=world_transform(np.array([[73.5,101.5,0]])*scale,pos,yaw)[0]
                        distance=float(np.linalg.norm(p[:2]-crank[:2]))
                        if distance>70:continue
                        operators.append({'local':list(local),'local_scaled':(np.array(local)*scale).tolist(),'local_pos':p.tolist(),'world_pos':(p+origin).tolist(),'nav':ns,
                                          'body_margin':envmargin,'gun_margin':gunmargin,'crank_xy_distance':distance})
                    if not operators:
                        rejected['operator']+=1
                        if len(operator_failures)<20:operator_failures.append({'offset':pos.tolist(),'yaw':yaw,'body_margins':debug})
                        continue
                    count+=1
                    # neutral and boundary shot probes expose roof/parapet restrictions.
                    R=np.array(L.transform_matrix((0,0,0),(0,0,yaw),1,*L.engine_convention())['r']);shot_hits=0;minimum=1000.
                    for y in (-60,-30,0,30,60):
                        for pitch in (-20,0,20,45):
                            muzzle,bore=aim.pose(y,pitch);muzzle=R@(muzzle*scale)+pos;bore=R@bore
                            end=muzzle+bore*max(0,(600-np.linalg.norm(muzzle[:2]-pos[:2]))/np.linalg.norm(bore[:2]))
                            low=np.minimum(muzzle,end)-3;high=np.maximum(muzzle,end)+3
                            k=(near.max(1)>=low).all(1)&(near.min(1)<=high).all(1)
                            if k.any():
                                d=float(seg_tri(muzzle,end,near[k]).min());minimum=min(minimum,d)
                                shot_hits+=d<2.205
                    candidates.append({'offset':pos.tolist(),'gun_pos':(pos+origin).tolist(),'yaw_deg':yaw,'scale':scale,'floor_z':support_z+origin[2],'center_floor_z':z+origin[2],
                      'base_min_z':base_min,'support_variation':max(zs)-min(zs),'support_samples':len(zs),'operators':operators,
                      'corner_floor_z':[q+origin[2] for q in cornerz],'base_corner_gaps':[support_z-q for q in cornerz],
                      'coarse_shot_hits':shot_hits,'coarse_minimum':minimum,'rest_overlap_pairs':len(overlap),
                      'score':shot_hits*1000+math.hypot(dx,dy)+min(o['crank_xy_distance'] for o in operators)})
            counts[str(yaw)]=count;rejections[str(yaw)]=rejected;print('SEARCH',req['name'],yaw,count,rejected,flush=True)
        candidates.sort(key=lambda v:v['score'])
        results.append({'name':req['name'],'requested':req['requested'],'floor_z':fz+origin[2],
                        'static_candidates_by_yaw':counts,'rejections':rejections,'center_overlap_examples':examples,'operator_failures':operator_failures,'candidates':candidates})
        print('BEST',req['name'],[(c['offset'],c['yaw_deg'],c['coarse_shot_hits']) for c in candidates[:5]],flush=True)
    (REPORTS/(f'tower_refine_{scope}_{scale:.2f}_v14.json' if scope!='all' else f'tower_refine_scale_{scale:.2f}_v14.json' if refine else 'tower_search_v14.json' if scale==1 else f'tower_search_scale_{scale:.2f}_v14.json')).write_text(json.dumps({'sites':results,'scale':scale,'scope':'Static geometry and support search; selected sector certificate follows.'},indent=2))

def floor_map():
    from mathutils import Vector
    context=json.loads((REPORTS/'tower_context_v14.json').read_text());out={}
    for req in context['requests']:
        geom=np.load(REPORTS/f'tower_geometry_{req["name"]}_v14.npz');bvh=bvh_from_triangles(geom['C'][geom['CT']])
        xs=list(range(-240,241,4));ys=list(range(-240,241,4));zs=[]
        for y in ys:zs.append([floor_at(bvh,x,y,0) for x in xs])
        out[req['name']]={'xs':xs,'ys':ys,'zs':zs}
    (REPORTS/'tower_floor_map_v14.json').write_text(json.dumps(out))

def certificate_grid(filename='tower_search_scale_0.75_v14.json',west_only=False):
    """Coarse pose envelope; exact one-degree certification is a later stage."""
    searchdata=json.loads((REPORTS/filename).read_text());context=json.loads((REPORTS/'tower_context_v14.json').read_text())
    shapes=gun_arrays();aim=Aim({'tower_top_units':0});reports=[]
    for site in searchdata['sites']:
        if west_only and site['name']!='oeste':continue
        if not site['candidates']:continue
        req=next(q for q in context['requests'] if q['name']==site['name']);origin=np.array(req['requested'])
        geom=np.load(REPORTS/f'tower_geometry_{site["name"]}_v14.npz');T=np.concatenate([geom['V'][geom['T']],geom['C'][geom['CT']]])
        # Prefer south where it has an operator. Keep north diagnostic otherwise.
        options=sorted(site['candidates'],key=lambda c:(min(c['yaw_deg'],360-c['yaw_deg'])>60,c['score']))[:3]
        for candidate in options:
            pos=np.array(candidate['offset']);scale=candidate['scale'];yaw=candidate['yaw_deg']
            R=np.array(L.transform_matrix((0,0,0),(0,0,yaw),1,*L.engine_convention())['r'])
            keep=(T.max(1)>[pos[0]-430,pos[1]-430,pos[2]+.08]).all(1)&(T.min(1)<[pos[0]+430,pos[1]+430,pos[2]+420]).all(1)
            near=T[keep];obstacles=bvh_from_triangles(near)
            operators=sorted(candidate['operators'],key=lambda o:(min(abs(n['z']-o['world_pos'][2]) for n in o['nav'])>1,-min(o['body_margin'],o['gun_margin']),o['crank_xy_distance']))
            operator=operators[0];p=np.array(operator['local_pos']);grid=[]
            for y in range(-60,61,5):
                for pitch in range(-20,46,5):
                    V,GT=gun_pose(shapes,y,pitch);V=(V*scale)@R.T+pos;gunT=V[GT]
                    pairs=bvh_from_triangles(gunT).overlap(obstacles)
                    body=capsule_margin(p,gunT)
                    muzzle,bore=aim.pose(y,pitch);muzzle=R@(muzzle*scale)+pos;bore=R@bore
                    end=muzzle+bore*max(0,(600-np.linalg.norm(muzzle[:2]-pos[:2]))/np.linalg.norm(bore[:2]))
                    lo=np.minimum(muzzle,end)-3;hi=np.maximum(muzzle,end)+3;k=(T.max(1)>=lo).all(1)&(T.min(1)<=hi).all(1)
                    distance=float(seg_tri(muzzle,end,T[k]).min()) if k.any() else 1000.
                    grid.append({'yaw':y,'pitch':pitch,'gun_overlap_pairs':len(pairs),'operator_margin':body,'shot_distance':distance,
                                 'ok':not pairs and body>=0 and distance>2.205})
                print('CERT_GRID',site['name'],yaw,pos.tolist(),y,sum(g['ok'] for g in grid if g['yaw']==y),flush=True)
            reports.append({'name':site['name'],'candidate':candidate,'operator':operator,'grid':grid})
    outname='tower_grid_'+Path(filename).stem+'.json'
    (REPORTS/outname).write_text(json.dumps({'sites':reports},indent=2))

def provisional():
    data=json.loads((REPORTS/'tower_refine_scale_0.75_v14.json').read_text());sites=[]
    for site in data['sites']:
        if site['name']=='oeste':
            compact=json.loads((REPORTS/'tower_local_west_south_0.65_v14.json').read_text())
            c=next(c for c in compact['candidates'] if c['offset'][:2]==[-24,-32])
            operators=sorted(c['operators'],key=lambda o:(min(abs(n['z']-o['world_pos'][2]) for n in o['nav'])>1,-min(o['body_margin'],o['gun_margin']),o['crank_xy_distance']))
            sites.append({'name':site['name'],'candidate':c,'operator':operators[0]});continue
        offset=[-24,16] if site['name']=='este' else [0,-8]
        c=next(c for c in site['candidates'] if c['offset'][:2]==offset and c['yaw_deg']==(0 if site['name']=='este' else 345))
        operators=sorted(c['operators'],key=lambda o:(min(abs(n['z']-o['world_pos'][2]) for n in o['nav'])>1,-min(o['body_margin'],o['gun_margin']),o['crank_xy_distance']))
        operator=next((o for o in operators if o['local']==[124,64]),operators[0])
        sites.append({'name':site['name'],'candidate':c,'operator':operator})
    (REPORTS/'tower_selected_v14.json').write_text(json.dumps({'sites':sites,'provisional':True},indent=2))

def certify():
    """One-degree STATIC REST angular sweep, not Fire/Reset animation or engine QA."""
    data=json.loads((REPORTS/'tower_selected_v14.json').read_text());context=json.loads((REPORTS/'tower_context_v14.json').read_text())
    shapes=gun_arrays();aim=Aim({'tower_top_units':0});gh=np.load(REPORTS/'gun_havok_v14.npz');gc,gct=gh['C'],gh['CT'];sites=[]
    for selected in data['sites']:
        name=selected['name'];c=selected['candidate'];op=selected['operator'];pos=np.array(c['offset']);scale=c['scale'];yaw=c['yaw_deg']
        req=next(q for q in context['requests'] if q['name']==name);origin=np.array(req['requested'])
        geom=np.load(REPORTS/f'tower_geometry_{name}_v14.npz');T=np.concatenate([geom['V'][geom['T']],geom['C'][geom['CT']]])
        R=np.array(L.transform_matrix((0,0,0),(0,0,yaw),1,*L.engine_convention())['r'])
        floor_local=c['floor_z']-origin[2]
        keep=(T.max(1)>[pos[0]-430,pos[1]-430,floor_local+.02]).all(1)&(T.min(1)<[pos[0]+430,pos[1]+430,pos[2]+420]).all(1)
        near=T[keep];near_bounds=(near.min(1),near.max(1));obstacles=bvh_from_triangles(near)
        world_gc=(gc*scale)@R.T+pos;gcT=world_gc[gct]
        sector=(-10,10) if name=='este' else (-10,2);pitches=(-20,20) if name=='este' else (-20,0)
        rows=[];fails=[];minimum={'distance':math.inf};minimum_body=math.inf;minpose=None
        p=np.array(op['local_pos']);tested=0
        for y in range(sector[0],sector[1]+1):
            for pitch in range(pitches[0],pitches[1]+1):
                V,GT=gun_pose(shapes,y,pitch);V=(V*scale)@R.T+pos;gunT=V[GT]
                combined=np.concatenate([gunT,gcT]);pairs=bvh_from_triangles(combined).overlap(obstacles)
                body=capsule_margin(p,combined)
                if body<minimum_body:minimum_body=body;minpose=[y,pitch]
                muzzle,bore=aim.pose(y,pitch);muzzle=R@(muzzle*scale)+pos;bore=R@bore
                end=muzzle+bore*max(0,(600-np.linalg.norm(muzzle[:2]-pos[:2]))/np.linalg.norm(bore[:2]))
                # Outside the32-u expanded segment AABB all triangles are
                # farther than32u; cap the computed distance at that bound.
                lo=np.minimum(muzzle,end)-32.;hi=np.maximum(muzzle,end)+32.
                k=(T.max(1)>=lo).all(1)&(T.min(1)<=hi).all(1)
                distances=seg_tri(muzzle,end,T[k]) if k.any() else np.array([32.])
                distance=float(min(32.,distances.min()));tested+=int(k.sum())
                if distance<minimum['distance']:minimum={'distance':distance,'yaw':y,'pitch':pitch,'ray_start':(muzzle+origin).tolist(),'ray_end':(end+origin).tolist()}
                row={'yaw':y,'pitch':pitch,'visual_and_havok_overlap_pairs':len(pairs),'operator_margin':body,'projectile_distance':distance}
                rows.append(row)
                if pairs or body<0 or distance<=2.205:
                    if len(fails)<20:fails.append(row)
            print('CERTIFIED_ROW',name,y,len(rows),'failures',len(fails),flush=True)
        restV,restGT=gun_pose(shapes,0,0);restV=(restV*scale)@R.T+pos
        rest_pairs=bvh_from_triangles(np.concatenate([restV[restGT],gcT])).overlap(obstacles)
        # Deliberately put an artificial post across a central shot. The same
        # exact segment/triangle routine must identify zero clearance.
        m,b=aim.pose((sector[0]+sector[1])/2,(pitches[0]+pitches[1])/2);m=R@(m*scale)+pos;b=R@b;block=m+b*80
        false_distance=float(seg_tri(m,m+b*160,box_triangles(block-[6,6,6],block+[6,6,6])).min())
        capsule_env=capsule_margin(p,near,near_bounds)
        axisnav=[n for n in nav_surface(context['navmeshes'],*c['gun_pos'][:2]) if abs(n['z']-c['center_floor_z'])<=8]
        # Support traces come from the written Havok, with each corner gap.
        floors=bvh_from_triangles(geom['C'][geom['CT']]);base_min=float(gc[:,2].min());feet=gc[gc[:,2]<=base_min+.001]
        feet_world=(feet*scale)@R.T+pos+origin;feet_reports=[]
        for foot in feet_world:
            f=floor_at(floors,foot[0]-origin[0],foot[1]-origin[1],floor_local)
            feet_reports.append({'world':foot.tolist(),'support_z':f+origin[2] if f is not None else None,
                                 'gap_units':float(foot[2]-(f+origin[2])) if f is not None else None})
        allTworld=geom['C'][geom['CT']]+origin
        refs=[]
        for ref in json.loads((REPORTS/'tower_geometry_metadata_v14.json').read_text())['sites'][0 if name=='este' else 1]['refs']:
            if ref['havok_meshes'] and ref['bounds_min'] and ref['bounds_min'][2]<=floor_local<=ref['bounds_max'][2] and ref['bounds_min'][0]<=pos[0]<=ref['bounds_max'][0] and ref['bounds_min'][1]<=pos[1]<=ref['bounds_max'][1]:refs.append(ref['ref'])
        patrol_id='00078784' if name=='este' else '0007878A';patrol=next((r for r in context['refs'] if r['id']==patrol_id),None)
        patrol_result=None
        patrol_adjustment=None
        if patrol:
            pp=np.array(patrol['data'][:3])-origin
            patrol_result={'ref':patrol_id,'world_pos':patrol['data'][:3],
                           'capsule_margin_against_gun_rest':capsule_margin(pp,np.concatenate([restV[restGT],gcT])),
                           'modified':False,'scope':'Marker retained; a negative margin means its old destination overlaps the new gun. No engine path guarantee.'}
            if patrol_result['capsule_margin_against_gun_rest']<0:
                choices=[];restgun=np.concatenate([restV[restGT],gcT]);restbounds=(restgun.min(1),restgun.max(1))
                for mx in range(16,97,4):
                    for my in range(-24,25,8):
                        q=pp.copy();q[0]+=mx;q[1]+=my;qz=floor_at(floors,q[0],q[1],floor_local)
                        if qz is None:continue
                        q[2]=qz;nav=[n for n in nav_surface(context['navmeshes'],*(q[:2]+origin[:2])) if abs(n['z']-(qz+origin[2]))<=8]
                        if not nav:continue
                        supports=[floor_at(floors,q[0]+18*math.cos(a),q[1]+18*math.sin(a),qz) for a in np.linspace(0,math.tau,17)[:-1]]
                        if any(v is None or abs(v-qz)>2 for v in supports):continue
                        em=capsule_margin(q,near,near_bounds);gm=capsule_margin(q,restgun,restbounds)
                        separation=float(np.linalg.norm(q[:2]-p[:2]))
                        if min(em,gm)<2 or separation<40:continue
                        choices.append({'id':patrol_id,'pos':(q+origin).tolist(),'old_pos':patrol['data'][:3],
                             'rot_rad':patrol['data'][3:],'nav':nav,'nav_delta_z':min(abs(n['z']-(qz+origin[2])) for n in nav),
                             'capsule_radius':18,'capsule_height':128,'vanilla_margin_lower_bound':em,'gun_rest_margin_lower_bound':gm,
                             'guard_xy_separation':separation,'move_xy_units':math.hypot(mx,my),
                             'floor_foot_z':qz+origin[2],'footprint_floor_variation':max(supports)-min(supports),
                             'scope':'Measured destination support and standing capsule only; original rotation preserved, no Skyrim pathfinding test.'})
                if choices:patrol_adjustment=min(choices,key=lambda a:(a['move_xy_units'],-min(a['vanilla_margin_lower_bound'],a['gun_rest_margin_lower_bound'])))
        navdelta=min(abs(n['z']-op['world_pos'][2]) for n in op['nav'])
        nav_ok=navdelta<=8
        support_ok=all(f['gap_units'] is not None and -.02<=f['gap_units']<=2. for f in feet_reports)
        marker_ok=patrol is None or patrol_result['capsule_margin_against_gun_rest']>=0 or patrol_adjustment is not None
        ok=not fails and not rest_pairs and minimum_body>=0 and capsule_env>=0 and false_distance==0 and nav_ok and support_ok and marker_ok
        site={'name':name,'user_requested':req['requested'],'gun_pos':c['gun_pos'],'guard_pos':op['world_pos'],'guard_local_unscaled':op['local'],
          'guard_local_scaled':op['local_scaled'],'yaw_deg':yaw,'scale':scale,'floor_z':c['floor_z'],'center_floor_z':c['center_floor_z'],
          'base_min_z':c['base_min_z'],'base_min_z_unscaled':base_min,'base_contact_world_z':c['gun_pos'][2]+c['base_min_z'],
          'cell':req['tower']['cell'],'world':'0000003C','tower_ref':req['tower_ref'],'support_refs_bounds_match':refs,
          'navmesh':{'guard':op['nav'],'guard_delta_z':navdelta,'gun_axis':axisnav,'scope':'Geometric NAVM triangle presence; no Skyrim pathfinding or reachability test.'},
          'support':{'ok':support_ok,'floor_source':'all nearby written vanilla Havok','corners':feet_reports,'samples':c['support_samples'],
                     'max_gap_units':max(f['gap_units'] for f in feet_reports),'tolerance_units':2.,'interior_height_variation':c['support_variation']},
          'body':{'radius':18,'height':128,'vanilla_min_margin':capsule_env,'gun_rest_min_margin':capsule_margin(p,np.concatenate([restV[restGT],gcT])),
                  'gun_sweep_min_margin':minimum_body,'gun_sweep_worst_pose':minpose,'crank_xy_distance':op['crank_xy_distance'],
                  'scope':'Fixed operator capsule against visual triangles and written Havok; intentional foot-floor contact excluded. Margins capped at64u are conservative lower bounds.'},
          'route':{'guard_on_existing_navmesh':nav_ok,'crank_reach_xy_units':op['crank_xy_distance'],
                   'tested':'Spawn/standing volume and NAVM support only; no route to the tower or live-engine path test.'},
          'pitch_min':pitches[0],'pitch_max':pitches[1],'yaw_center':sum(sector)/2,'yaw_half_sector':(sector[1]-sector[0])/2,
          'yaw_min':sector[0],'yaw_max':sector[1],'angular_certificate':{'ok':ok,'sampling_yaw_deg':1,'sampling_pitch_deg':1,
             'poses':len(rows),'rest_overlap_pairs':len(rest_pairs),'failed_pose_examples':fails,'projectile_radius':2.205,
             'minimum_projectile_distance':minimum,'projectile_distance_capped_lower_bound_at_units':32.,'projectile_margin_lower_bound':minimum['distance']-2.205,'distance_pairs_tested':tested,
             'artificial_post_falsification_distance':false_distance,'triangles_visual':len(geom['T']),'triangles_havok':len(geom['CT']),
             'scope':'Static REST angular samples only. Fire/Reset keyframe envelope, between-sample continuous motion, animations of surrounding world objects and Skyrim engine behavior were not measured.'},
          'existing_patrol_marker':patrol_result,'engine_verified':False,'success':ok}
        if patrol_adjustment:site['patrol_marker_adjustment']=patrol_adjustment
        (REPORTS/f'tower_angular_samples_{name}_v14.json').write_text(json.dumps({'rows':rows,'site':site},indent=2))
        sites.append(site);print('SITE_FINAL',name,ok,minimum,'body',minimum_body,flush=True)
    cache_paths=[f'reports/tower_geometry_{name}_v14.npz' for name in ('este','oeste')]+['reports/gun_havok_v14.npz']
    report={'success':all(s['success'] for s in sites) and len(sites)==2,'ballista_sha256':sha(GUN),'context_sha256':sha(REPORTS/'tower_context_v14.json'),
      'geometry_cache_sha256':{name:sha(ROOT/name) for name in cache_paths},
      'verifier_sha256':sha(__file__),'inputs_sha256':{'gun':sha(GUN),'context':sha(REPORTS/'tower_context_v14.json'),'verifier':sha(__file__),
      'selection':sha(REPORTS/'tower_selected_v14.json'),'geometry_metadata':sha(REPORTS/'tower_geometry_metadata_v14.json')},
      'sites':sites,'engine_verified':False,'scope':'Measured static-rest placement and 1-degree angular samples of two scaled NPC references on existing vanilla towers. Player NIF and vanilla masters remain unmodified.'}
    (REPORTS/'towers_v14.json').write_text(json.dumps(report,indent=2,allow_nan=False))
    print('TOWERS_FINAL',report['success'],flush=True)

def marker_sweep():
    """Verify moved patrol destinations against every accepted static-rest pose."""
    context=json.loads((REPORTS/'tower_context_v14.json').read_text());report=json.loads((REPORTS/'towers_v14.json').read_text())
    assert sha(GUN)==report['ballista_sha256'] and sha(REPORTS/'tower_context_v14.json')==report['context_sha256']
    assert all(sha(ROOT/name)==value for name,value in report['geometry_cache_sha256'].items())
    shapes=gun_arrays();gh=np.load(REPORTS/'gun_havok_v14.npz');results=[]
    for site in report['sites']:
        if 'patrol_marker_adjustment' not in site:continue
        request=next(q for q in context['requests'] if q['name']==site['name']);origin=np.array(request['requested'])
        p=np.array(site['patrol_marker_adjustment']['pos'])-origin;pos=np.array(site['gun_pos'])-origin;scale=site['scale'];yaw=site['yaw_deg']
        R=np.array(L.transform_matrix((0,0,0),(0,0,yaw),1,*L.engine_convention())['r']);gc=(gh['C']*scale)@R.T+pos;gcT=gc[gh['CT']]
        minimum=64.;worst=None;count=0
        for y in range(int(site['yaw_min']),int(site['yaw_max'])+1):
            for pitch in range(int(site['pitch_min']),int(site['pitch_max'])+1):
                V,T=gun_pose(shapes,y,pitch);V=(V*scale)@R.T+pos
                margin=capsule_margin(p,np.concatenate([V[T],gcT]));count+=1
                if margin<minimum:minimum=margin;worst=[y,pitch]
        item={'name':site['name'],'marker':site['patrol_marker_adjustment']['id'],'pos':site['patrol_marker_adjustment']['pos'],
              'poses':count,'gun_sweep_capsule_margin_lower_bound':minimum,'worst_pose':worst,'ok':minimum>=0}
        results.append(item);site['patrol_marker_adjustment']['angular_rest_sweep']=item
        print('MARKER_SWEEP',item,flush=True)
    output={'success':all(s['ok'] for s in results),'sites':results,'ballista_sha256':sha(GUN),'verifier_sha256':sha(__file__),
      'geometry_cache_sha256':report['geometry_cache_sha256'],
      'scope':'Fixed moved patrol-destination capsules sampled against the static-rest angular gun sweep at 1 degree; no actor animation, continuous motion or Skyrim pathfinding verification.'}
    (REPORTS/'patrol_marker_sweep_v14.json').write_text(json.dumps(output,indent=2))
    report['patrol_marker_sweep_sha256']=sha(REPORTS/'patrol_marker_sweep_v14.json')
    report['success']=report['success'] and output['success']
    (REPORTS/'towers_v14.json').write_text(json.dumps(report,indent=2,allow_nan=False))

def contact_probe():
    data=json.loads((REPORTS/'tower_selected_v14.json').read_text());shapes=gun_arrays();gh=np.load(REPORTS/'gun_havok_v14.npz');out=[]
    for sel in data['sites']:
        c=sel['candidate'];pos=np.array(c['offset']);scale=c['scale'];R=np.array(L.transform_matrix((0,0,0),(0,0,c['yaw_deg']),1,*L.engine_convention())['r'])
        geom=np.load(REPORTS/f'tower_geometry_{sel["name"]}_v14.npz');T=np.concatenate([geom['V'][geom['T']],geom['C'][geom['CT']]])
        floor_local=pos[2]+c['base_min_z'];keep=(T.max(1)>[pos[0]-430,pos[1]-430,floor_local+.02]).all(1)&(T.min(1)<[pos[0]+430,pos[1]+430,pos[2]+420]).all(1);near=T[keep]
        V,GT=gun_pose(shapes,0,0);V=(V*scale)@R.T+pos;gc=(gh['C']*scale)@R.T+pos;gunT=np.concatenate([V[GT],gc[gh['CT']]])
        pairs=bvh_from_triangles(gunT).overlap(bvh_from_triangles(near));examples=[]
        for a,b in pairs[:24]:examples.append({'gun_triangle_index':a,'gun_is_havok':a>=len(GT),'gun_triangle':gunT[a].tolist(),'world_triangle':near[b].tolist(),'world_triangle_min':near[b].min(0).tolist(),'world_triangle_max':near[b].max(0).tolist()})
        floors=bvh_from_triangles(geom['C'][geom['CT']]);samples=[]
        for x in np.linspace(gh['C'][:,0].min()*scale,gh['C'][:,0].max()*scale,41):
            for y in np.linspace(gh['C'][:,1].min()*scale,gh['C'][:,1].max()*scale,41):
                p=R@np.array([x,y,0])+pos;f=floor_at(floors,p[0],p[1],floor_local)
                samples.append({'xy':p[:2].tolist(),'floor_z':f})
        out.append({'name':sel['name'],'rest_pairs':len(pairs),'examples':examples,'footprint_samples':samples,'floor_root':floor_local})
    (REPORTS/'tower_contacts_v14.json').write_text(json.dumps({'sites':out},indent=2))
    print('CONTACTS',[(s['name'],s['rest_pairs']) for s in out])

def local_west(south=False,scale=.75):
    """Resolve the identified collider/post contact around the viable SSE bay."""
    context=json.loads((REPORTS/'tower_context_v14.json').read_text());req=context['requests'][1];origin=np.array(req['requested']);shapes=gun_arrays()
    V,GT=gun_pose(shapes,0,0);gh=np.load(REPORTS/'gun_havok_v14.npz');GC,GCT=gh['C'],gh['CT'];V*=scale;GC*=scale
    geom=np.load(REPORTS/'tower_geometry_oeste_v14.npz');allT=np.concatenate([geom['V'][geom['T']],geom['C'][geom['CT']]])
    floors=bvh_from_triangles(geom['C'][geom['CT']]);fz=floor_at(floors,0,0,0);near=allT[(allT.max(1)>[-430,-430,fz+.08]).all(1)&(allT.min(1)<[430,430,420]).all(1)]
    support=np.array([[x,y,0] for x in np.linspace(GC[:,0].min(),GC[:,0].max(),13) for y in np.linspace(GC[:,1].min(),GC[:,1].max(),13)])
    results=[];rejected=[]
    for yaw in ((0,) if south else (345,340,350)):
        R=np.array(L.transform_matrix((0,0,0),(0,0,yaw),1,*L.engine_convention())['r'])
        for dx in (range(-24,-7,4) if scale<.75 else range(-40,41,4) if south else range(-8,33,4)):
            for dy in (range(-44,-27,4) if scale<.75 else range(-64,-23,4) if south else range(-20,5,4)):
                z=floor_at(floors,dx,dy,fz)
                if z is None or abs(z-fz)>2:continue
                pos=np.array([dx,dy,z-float(GC[:,2].min())]);W=support@R.T+pos;zs=[floor_at(floors,p[0],p[1],z) for p in W]
                if any(v is None or abs(v-z)>2 for v in zs):continue
                support_z=max(zs);pos[2]=support_z-float(GC[:,2].min())
                obstacle=near[near.max(1)[:,2]>support_z+.02];ob=bvh_from_triangles(obstacle)
                gunT=np.concatenate([(V@R.T+pos)[GT],(GC@R.T+pos)[GCT]])
                overlaps=bvh_from_triangles(gunT).overlap(ob)
                if overlaps:
                    rejected.append({'xy':[dx,dy],'yaw':yaw,'overlaps':len(overlaps),'havok_pairs':sum(a>=len(GT) for a,b in overlaps)});continue
                operators=[];crank=R@(np.array([73.5,101.5,0])*scale)+pos
                gunbounds=(gunT.min(1),gunT.max(1));obbounds=(obstacle.min(1),obstacle.max(1))
                for x in range(108,181,8):
                    for y in range(16,153,8):
                        reach=math.hypot(x-73.5,y-101.5)*scale
                        if reach>100:continue
                        p=R@(np.array([x,y,0])*scale)+pos;gz=floor_at(floors,p[0],p[1],fz)
                        if gz is None or abs(gz-fz)>16:continue
                        p[2]=gz;nav=[n for n in nav_surface(context['navmeshes'],*(p[:2]+origin[:2])) if abs(n['z']-(gz+origin[2]))<=8]
                        if not nav:continue
                        if any(floor_at(floors,p[0]+18*math.cos(a),p[1]+18*math.sin(a),gz) is None for a in np.linspace(0,math.tau,17)[:-1]):continue
                        env=capsule_margin(p,obstacle,obbounds);gm=capsule_margin(p,gunT,gunbounds)
                        if min(env,gm)<.05:continue
                        operators.append({'local':[x,y],'local_scaled':[x*scale,y*scale],'local_pos':p.tolist(),'world_pos':(p+origin).tolist(),
                                          'nav':nav,'body_margin':env,'gun_margin':gm,'crank_xy_distance':reach})
                results.append({'offset':pos.tolist(),'gun_pos':(pos+origin).tolist(),'yaw_deg':yaw,'scale':scale,'floor_z':support_z+origin[2],
                                'center_floor_z':z+origin[2],'base_min_z':float(GC[:,2].min()),'support_variation':max(zs)-min(zs),'support_samples':len(zs),
                                'operators':operators,'rest_overlap_pairs':0,'score':math.hypot(dx,dy)})
        print('LOCAL_WEST',yaw,'clean rest candidates',len(results),'with operator',sum(bool(c['operators']) for c in results),flush=True)
    (REPORTS/(f'tower_local_west_south_{scale:.2f}_v14.json' if scale<.75 else 'tower_local_west_south_v14.json' if south else 'tower_local_west_v14.json')).write_text(json.dumps({'candidates':results,'rejected':rejected},indent=2))

def render_selection():
    import bpy,addon_utils
    from mathutils import Vector
    from probe_towers_v14 import load
    cfg=json.loads((BASE/'config.json').read_text());context=json.loads((REPORTS/'tower_context_v14.json').read_text())
    selection=json.loads((REPORTS/'tower_selected_v14.json').read_text())
    addon_utils.enable('io_scene_nifly',default_set=True)
    bpy.context.preferences.addons['io_scene_nifly'].preferences.sky_texture_path_1=str(Path(cfg['extracted'])/'textures')
    previews=[]
    for sel in selection['sites']:
        for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
        req=next(q for q in context['requests'] if q['name']==sel['name']);context_import(req,cfg,context)
        c=sel['candidate'];load(GUN,L.transform_matrix(c['offset'],(0,0,c['yaw_deg']),c['scale'],*L.engine_convention()))
        p=sel['operator']['local_pos'];mat=bpy.data.materials.new('Diagnostic operator capsule - not an actor')
        mat.diffuse_color=(.03,.5,.85,1);mat.use_nodes=True
        bsdf=mat.node_tree.nodes.get('Principled BSDF');bsdf.inputs['Base Color'].default_value=(.03,.5,.85,1);bsdf.inputs['Roughness'].default_value=.45
        for height in (18,110):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=18,location=(p[0],p[1],p[2]+height))
            bpy.context.object.data.materials.append(mat);bpy.context.object.name='OperatorEnvelope128_R18'
        bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=18,depth=92,location=(p[0],p[1],p[2]+64));bpy.context.object.data.materials.append(mat)
        sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=24
        sc.render.resolution_x=1400;sc.render.resolution_y=1100;sc.render.resolution_percentage=100
        sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.32,.34,.37,1);sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
        sun=bpy.data.lights.new('Daylight','SUN');sun.energy=3.2;so=bpy.data.objects.new('Daylight',sun);sc.collection.objects.link(so);so.rotation_euler=(.5,-.4,-.7)
        area=bpy.data.lights.new('Fill','AREA');area.energy=700000;area.shape='DISK';area.size=500;ao=bpy.data.objects.new('Fill',area);sc.collection.objects.link(ao);ao.location=(300,-450,250);ao.rotation_euler=(Vector((0,0,100))-ao.location).to_track_quat('-Z','Y').to_euler()
        camera=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));sc.collection.objects.link(camera);sc.camera=camera
        for view,loc,target,lens in (('encaje',(480,-630,270),(0,0,90),48),('contexto',(800,-950,720),(0,0,-70),42)):
            camera.location=loc;camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.lens=lens;camera.data.clip_end=20000
            path=ROOT/'renders'/f'v14_torre_{sel["name"]}_{view}.png';sc.render.filepath=str(path);bpy.ops.render.render(write_still=True)
            previews.append({'name':sel['name'],'view':view,'path':str(path),'sha256':sha(path),'gun_scale':c['scale'],'camera_local':loc,
                             'caption':'Blender geometric reconstruction from vanilla masters; cyan capsule is an operator envelope (128 u height / 18 u radius), not a real actor or Skyrim capture.'})
    (REPORTS/'tower_render_metadata_v14.json').write_text(json.dumps({'renders':previews,'engine_verified':False},indent=2))

if __name__=='__main__':
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
    if args[0]=='dump':dump()
    elif args[0]=='search':search(float(args[1]) if len(args)>1 else 1.)
    elif args[0]=='refine':search(float(args[1]),True)
    elif args[0]=='focused':search(float(args[1]),True,args[2])
    elif args[0]=='floor_map':floor_map()
    elif args[0]=='grid':certificate_grid(args[1] if len(args)>1 else 'tower_search_scale_0.75_v14.json',len(args)>2 and args[2]=='west')
    elif args[0]=='provisional':provisional()
    elif args[0]=='certify':certify()
    elif args[0]=='marker_sweep':marker_sweep()
    elif args[0]=='contacts':contact_probe()
    elif args[0]=='local_west':local_west()
    elif args[0]=='local_south':local_west(True)
    elif args[0]=='compact':local_west(True,float(args[1]))
    elif args[0]=='render':render_selection()
