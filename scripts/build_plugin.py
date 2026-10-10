"""Read vanilla donors and write the isolated regular SE ESP. No runtime writes.
Navmesh bytes follow TES5Edit wbDefinitionsTES5.pas (NVNM/NVMI, version 12).
NAVI is the engine singleton 00012FB4; only this mod's map entry is serialized.
"""
import argparse,collections,hashlib,json,math,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/vendor'))
import escritor_plugin as W
from parser_esm import Plugin
sys.path.insert(0,str(ROOT/'scripts'))
import v11_layout as L
# v11: the vanilla pieces of config.json -> tower_v11 as references, after the v10 forms (last 0x933).
VANILLA_FIRST=0x03000940
LAST_NAVMESH=None
MASTERS=['Skyrim.esm','Update.esm','Dawnguard.esm']
IDS={'tower':0x03000800,'ballesta':0x03000801,'projectile':0x03000802,'ammo':0x03000803,'launcher':0x03000804,'launcher_stat':0x03000805,'session':0x03000806,'cell':0x03000807,'container':0x03000808,'navmesh':0x03000809,'tower_ref':0x03000900,'ballesta_ref':0x03000901,'container_ref':0x03000902,'spawn_ref':0x03000903}
IDS.update(light_fill=0x0300080A,light_target=0x0300080B)
IDS.update(explosion=0x0300080C,shot_sound=0x0300080D)
IDS.update(ocupada=0x0300080E,guardia=0x0300080F,guardia_ref=0x03000940)
# v08 siege records (docs/revision B1/B2/B6): one table for the build, the validator and the tests.
# Damage follows the vanilla object-fired ballista: TrapDweBallistaBolt keeps WEAP/AMMO at 0 and
# deals 80-250 through its explosion; impact force 50 is that projectile's own value.
V08={'weapon_damage':35,'weapon_stagger':1.0,'impact_force':50.0,
     'explosion_force':20.0,'explosion_damage':150.0,'explosion_radius':128.0,
     'proj_flag_pickup':0x40,'proj_flag_explosion':0x02,'ammo_flag_nonplayable':0x02,
     'names':{'projectile':'Proyectil de asedio Astra','ammo':'Virote de asedio Astra','launcher':'Lanzavirotes de asedio Astra'}}
U=lambda i:struct.pack('<I',i)
def find_records(path,edids):
 p=Plugin(path);out={}
 for t,o,n,d in p.recorrer():
  if t=='GRUP':continue
  ss=p.subrecords(p.datos(o));ed=next((v.rstrip(b'\0').decode('cp1252') for k,v in ss if k=='EDID'),'')
  if ed in edids:out[ed]={'type':t,'fid':p.form_id(o),'subs':ss,'flags':struct.unpack_from('<I',p.d,o+8)[0]}
 if set(edids)-out.keys():raise ValueError('Missing donors '+str(set(edids)-out.keys()))
 return out

def replace_clone(donor,edid,updates,drop=()):
 ss=[];seen=set()
 for k,v in donor['subs']:
  if k in drop:continue
  if k in updates:v=updates[k];seen.add(k)
  if k=='EDID':v=W.zstr(edid)
  ss.append(W.sub(k,v))
 for k,v in updates.items():
  if k not in seen:ss.append(W.sub(k,v))
 return ss

def find_guard_npc(path,candidates):
 p=Plugin(path)
 for t,o,n,d in p.recorrer():
  if t=='NPC_':
   ss=p.subrecords(p.datos(o))
   ed=next((v.rstrip(b'\0').decode('cp1252') for k,v in ss if k=='EDID'),'')
   if ed in candidates:
    return {'edid':ed,'type':t,'fid':p.form_id(o),'subs':ss,'flags':struct.unpack_from('<I',p.d,o+8)[0]}
 raise ValueError('Guard NPC donor not found among %s: abri xEdit, buscá el EDID de un guardia de ciudad (NPC_) y agregalo a config.json guardia.donores_npc'%candidates)

def lenstr(s):
 b=s.encode('utf8');return struct.pack('<H',len(b))+b

def script(name,props):
 b=lenstr(name)+b'\0'+struct.pack('<H',len(props))
 for name,(kind,value) in props.items():
  b+=lenstr(name)+bytes([kind,1])
  if kind==1:b+=struct.pack('<HhI',0,-1,value)
  elif kind==2:b+=lenstr(value)
  elif kind==3:b+=struct.pack('<i',value)
  elif kind==4:b+=struct.pack('<f',value)
  elif kind==5:b+=bytes([bool(value)])
  else:raise ValueError(kind)
 return b

def vmad(name,props):return vmad_multi([(name,props)])
def vmad_multi(scripts):
 b=struct.pack('<HHH',5,2,len(scripts))
 for name,props in scripts:b+=script(name,props)
 return b

def quest_vmad():
 b=vmad('AstraAsedioSession',{})
 b+=struct.pack('<BHHH',2,0,0,1) # bind version, fragment count, empty filename, alias count
 b+=struct.pack('<HhIHHH',0,0,IDS['session'],5,2,1)
 b+=script('AstraAsedioPlayerAlias',{'Session':(1,IDS['session'])})
 return b

def read_vmad(data,quest=False):
 """Read the SSE VMAD layout independently of the writer; fail on trailing bytes.
 Layout checked against xEdit definitions and vanilla quest alias payloads.
 """
 off=0
 def take(fmt):
  nonlocal off
  result=struct.unpack_from('<'+fmt,data,off);off+=struct.calcsize('<'+fmt)
  return result[0] if len(result)==1 else result
 def string():
  nonlocal off
  n=take('H');value=data[off:off+n];off+=n
  if len(value)!=n:raise ValueError('truncated VMAD string')
  return value.decode('utf-8')
 def object_(fmt):
  if fmt==2:unused,alias,fid=take('HhI')
  elif fmt==1:fid,alias,unused=take('IhH')
  else:raise ValueError('unsupported VMAD object format')
  if unused:raise ValueError('nonzero VMAD object reserved bytes')
  return {'form_id':fid,'alias':alias}
 def value(kind,fmt):
  if kind==1:return object_(fmt)
  if kind==2:return string()
  if kind==3:return take('i')
  if kind==4:
   v=take('f')
   if not math.isfinite(v):raise ValueError('nonfinite VMAD float')
   return v
  if kind==5:return bool(take('B'))
  if 11<=kind<=15:
   count=take('I')
   if count>128:raise ValueError('unexpected VMAD array size')
   return [value(kind-10,fmt) for _ in range(count)]
  raise ValueError('unsupported VMAD property type '+str(kind))
 def scripts(fmt,count):
  result=[]
  for _ in range(count):
   name=string();status=take('B');props={}
   for _ in range(take('H')):
    prop=string();kind,status_=take('BB')
    if prop.lower() in {p.lower() for p in props}:raise ValueError('duplicate VMAD property')
    props[prop]={'type':kind,'status':status_,'value':value(kind,fmt)}
   result.append({'name':name,'status':status,'properties':props})
  return result
 version,fmt,count=take('HHH');result={'version':version,'object_format':fmt,'scripts':scripts(fmt,count),'aliases':[]}
 if quest and off<len(data):
  result['bind_version']=take('B');count=take('H');result['fragment_file']=string();result['fragments']=[]
  for _ in range(count):
   stage,log,unknown=take('IIB');result['fragments'].append({'stage':stage,'log':log,'unknown':unknown,'script':string(),'function':string()})
  for _ in range(take('H')):
   alias=object_(fmt);version_,fmt_,count=take('HHH')
   result['aliases'].append({**alias,'version':version_,'object_format':fmt_,'scripts':scripts(fmt_,count)})
 if off!=len(data):raise ValueError('VMAD tail mismatch')
 return result

def neutral_cell_lighting(original):
 if len(original)!=92:raise ValueError('unexpected XCLL layout')
 lighting=bytearray(original)
 lighting[0:4]=bytes((112,112,112,0));lighting[4:8]=bytes((80,80,80,0));lighting[8:12]=bytes((64,64,64,0))
 for i in range(6):lighting[40+i*4:44+i*4]=bytes((112,112,112,0))
 lighting[64:68]=bytes((112,112,112,0));lighting[72:76]=bytes((64,64,64,0))
 struct.pack_into('<2f',lighting,12,100000.,200000.)
 struct.pack_into('<f',lighting,36,1.);struct.pack_into('<f',lighting,76,0.);struct.pack_into('<I',lighting,88,0)
 return bytes(lighting)

def neutral_light(donor,edid,radius):
 data=bytearray(dict(donor['subs'])['DATA'])
 if len(data)!=48 or struct.unpack_from('<I',data,12)[0]!=0:raise ValueError('light donor must be nonshadowed and constant')
 struct.pack_into('<I',data,4,radius);data[8:12]=bytes((220,220,220,0))
 return replace_clone(donor,edid,{'DATA':bytes(data),'FNAM':struct.pack('<f',1.)})

def bound(asset,default):
 a=ROOT/'reports/assets.json';coords=default
 if a.exists():
  obj=json.loads(a.read_text());entry=obj.get('assets',{}).get(asset,obj.get(asset,{}))
  bbox=entry.get('bbox_units') or entry.get('bbox')
  if isinstance(bbox,dict) and 'min' in bbox:coords=bbox['min']+bbox['max']
  elif isinstance(bbox,list) and len(bbox)==2:coords=bbox[0]+bbox[1]
 vals=[math.floor(x) if i<3 else math.ceil(x) for i,x in enumerate(coords)]
 if any(x<-32768 or x>32767 for x in vals):raise ValueError('OBND overflow')
 return struct.pack('<6h',*vals)

def projectile_radius():
 """PROJ collision radius = shaft half-width of the patched virote Havok box, in units."""
 import nif_fisica,nif_nodos
 box=nif_fisica.cuerpos_caja(nif_nodos.leer(str(ROOT/'mod/meshes/AstraAsedio/virote.nif')))[0]
 return round(min(box['semiejes_hk'][0],box['semiejes_hk'][2])*nif_fisica.HK,3)

def stat(edid,model,obnd):
 return [W.sub('EDID',W.zstr(edid)),W.sub('OBND',obnd),W.sub('MODL',W.zstr(model)),W.sub('MODT',bytes.fromhex('020000000000000000000000')),W.sub('DNAM',struct.pack('<fI',90.0,0))]

def reference(fid,base,pos,angle=0.0,edid=None,persistent=False,rot=None,scale=1.0,link=0,tipo='REFR'):
 """rot: X/Y/Z radians as stored in DATA (v11_layout.engine_convention says how the engine reads them).
 tipo: 'REFR' para objetos, 'ACHR' para referencias de NPC (el engine solo
 instancia actores desde ACHR; un REFR con base NPC_ es ignorado)."""
 ss=[]
 if edid:ss.append(W.sub('EDID',W.zstr(edid)))
 ss.append(W.sub('NAME',U(base)))
 # Skyrim.esm order for scaled references: ... NAME, XSCL, DATA last.
 if abs(scale-1.0)>1e-9:ss.append(W.sub('XSCL',struct.pack('<f',scale)))
 ss.append(W.sub('DATA',struct.pack('<6f',*pos,*(rot if rot is not None else (0,0,angle)))))
 if link:ss.append(W.sub('XLKR',struct.pack('<II',link,0)))
 return W.record(tipo,fid,ss,banderas=0x400 if persistent else 0)

def _contains(tri,x,y):
 (ax,ay,_a),(bx,by,_b),(cx,cy,_c)=tri;d=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
 if abs(d)<1e-9:return False
 l1=((by-cy)*(x-cx)+(cx-bx)*(y-cy))/d;l2=((cy-ay)*(x-cx)+(ax-cx)*(y-cy))/d
 return min(l1,l2,1-l1-l2)>=-1e-6

def band_obstacles(cfg):
 """What stands where an actor walks (0-128 u): the vanilla pieces and the tower's own boxes."""
 z0,z1=cfg['tower_v11']['spawn_marker']['band']
 out=L.band_boxes(cfg['tower_v11']['pieces'],z0,z1,cfg=cfg)
 for b in collision_boxes():
  if b['min'][2]<z1 and b['max'][2]>z0:out.append({'min':b['min'],'max':b['max'],'name':'torre'})
 return out

def spawn_marker(cfg,vertices,triangles):
 """v10's COC marker stays put unless something stands within min_clearance of it in the actor
 band; then it moves to the nearest free point of a 16 u grid, outside the room, on the navmesh."""
 spec=cfg['tower_v11']['spawn_marker'];x0,y0,z0=spec['pos'];need=spec['min_clearance']
 room=cfg['tower_v11']['room'];(rcx,rcy),(sx,sy)=room['center'],room['size']
 obstacles=band_obstacles(cfg)
 ground=[[vertices[j] for j in t] for t in triangles if max(vertices[j][2] for j in t)<=10]
 def clearance(x,y):return min(math.hypot(max(b['min'][0]-x,0,x-b['max'][0]),max(b['min'][1]-y,0,y-b['max'][1])) for b in obstacles)
 for x,y in sorted(((x0+16*i,y0+16*j) for i in range(-40,41) for j in range(-40,41)),key=lambda p:(math.hypot(p[0]-x0,p[1]-y0),p)):
  if abs(x-rcx)<sx/2 and abs(y-rcy)<sy/2:continue
  c=clearance(x,y)
  if c>=need and any(_contains(tri,x,y) for tri in ground):
   return {'pos':[x,y,z0],'moved':(x,y)!=(x0,y0),'clearance':c,'original':[x0,y0,z0],'rule':'>= %g u from anything in the %s u band, outside the room, on the navmesh'%(need,spec['band'])}
 raise ValueError('no free spawn point near the configured marker')

def collision_boxes():
 data=json.loads((ROOT/'reports/collision_walkable.json').read_text())
 boxes=[dict(b, nav_step_units=16.0) if b.get('name','').startswith(('Vigueta_', 'Viga_borde_')) else b for b in data['solid_boxes_units']]
 # v12: the floor is also a ceiling below the low platform. It blocks ground navigation,
 # while a 16 u step envelope lets actors finish the ramp onto its leading edge.
 boxes.extend(dict(b,nav_step_units=16.0) for b in data['floors_units'])
 for b in data.get('stair_edge_barriers_units',[]):
  ramp=next(r for r in data['ramps'] if abs(r['y'][0]-b['min'][1])<.01 and abs(r['y'][1]-b['max'][1])<.01)
  slope=(ramp['z'][1]-ramp['z'][0])/(ramp['y'][1]-ramp['y'][0])
  boxes.append(dict(b,slope_y=slope,z_intercept=ramp['z'][0]-slope*ramp['y'][0],rail_height=b['max'][2]-ramp['z'][1]))
 pedestal=data['ballesta_fixed_box_units'];z=json.loads((ROOT/'config.json').read_text())['tower_top_units']
 boxes.append({'min':[pedestal['min'][0],pedestal['min'][1],pedestal['min'][2]+z],'max':[pedestal['max'][0],pedestal['max'][1],pedestal['max'][2]+z]})
 return boxes

def triangle_blocked(triangle,box,clearance=18.0,actor_height=128.0):
 """Clip the actor-foot triangle against the obstruction's expanded 3D box.
 Expanded XY is conservative for a capsule. Z expansion below accounts for
 the actor above its feet. Boundary-only contact at the clearance is allowed.
 """
 if 'slope_y' in box:
  slope=box['slope_y'];triangle=[(p[0],p[1],p[2]-slope*p[1]) for p in triangle]
  box={'min':[box['min'][0],box['min'][1],box['z_intercept']-abs(slope)*clearance],'max':[box['max'][0],box['max'][1],box['z_intercept']+box['rail_height']+abs(slope)*clearance]}
 eps=.01
 lo=[box['min'][0]-clearance+eps,box['min'][1]-clearance+eps,box['min'][2]-actor_height+eps]
 hi=[box['max'][0]+clearance-eps,box['max'][1]+clearance-eps,box['max'][2]-box.get('nav_step_units',0.0)-eps]
 if any(max(p[i] for p in triangle)<lo[i] or min(p[i] for p in triangle)>hi[i] for i in range(3)):return False
 polygon=[tuple(p) for p in triangle]
 for axis in range(3):
  for limit,sign in [(lo[axis],1.0),(hi[axis],-1.0)]:
   out=[]
   for a,b in zip(polygon,polygon[1:]+polygon[:1]):
    da=(a[axis]-limit)*sign;db=(b[axis]-limit)*sign
    if da>=0:out.append(a)
    if (da>=0)!=(db>=0):
     t=da/(da-db);out.append(tuple(a[j]+t*(b[j]-a[j]) for j in range(3)))
   polygon=out
   if not polygon:return False
 return True

def navmesh_geometry(vanilla_obstacles=True):
 # Coarse flat ground grid avoids the tower's blocking footprint.
 global LAST_NAVMESH
 vertices=[];triangles=[];vertex_ids={}
 def vert(p):
  key=tuple(round(c,4) for c in p)
  if key not in vertex_ids:vertex_ids[key]=len(vertices);vertices.append(key)
  return vertex_ids[key]
 def quad(a,b,c,d):
  ia,ib,ic,id=[vert(p) for p in [a,b,c,d]];triangles.extend([(ia,ib,ic),(ia,ic,id)])
 walkfile=ROOT/'reports/collision_walkable.json'
 if not walkfile.exists():raise ValueError('Collision walking surfaces required before navmesh build')
 data=json.loads(walkfile.read_text());walk_source=str(walkfile.relative_to(ROOT))
 floors=data['floors_units'];ramps=data['ramps'];boxes=collision_boxes()
 # v11: the room under the platform replaces v10's log cabin (+-140), and the vanilla stilts,
 # braces, walls and door block the ground where they stand in the actor band (0-128 u) only:
 # a cross brace does not close its whole bay, and pieces under the stair or the deck do not
 # touch the navmesh laid on them (spec §3).
 cfg=json.loads((ROOT/'config.json').read_text());room=cfg['tower_v11']['room']
 (rcx,rcy),(rsx,rsy)=room['center'],room['size']
 band=L.band_boxes(cfg['tower_v11']['pieces'],cfg=cfg) if vanilla_obstacles else []
 # A shared 2D subdivision gives matching edges at every landing and corner.
 xs=set(range(-2048,2049,512));ys=set(range(-2560,1537,512))
 xs.update([rcx-rsx/2,rcx+rsx/2]);ys.update([rcy-rsy/2,rcy+rsy/2])
 for box in band:
  xs.update(round(v,3) for v in [box['min'][0]-18,box['max'][0]+18]);ys.update(round(v,3) for v in [box['min'][1]-18,box['max'][1]+18])
 for f in floors:
  xs.update(round(v,3) for v in [f['min'][0],f['max'][0]])
  ys.update(round(v,3) for v in [f['min'][1],f['max'][1]])
 for r in ramps:
  xs.update(round(v,3) for v in r['x']);ys.update(round(v,3) for v in r['y'])
 for box in boxes:
  xs.update(round(v,3) for v in [box['min'][0]-18,box['max'][0]+18]);ys.update(round(v,3) for v in [box['min'][1]-18,box['max'][1]+18])
 xs=sorted(xs);ys=sorted(ys)
 emitted=set();plane_cells=collections.defaultdict(set)
 xi={v:i for i,v in enumerate(xs)};yi={v:i for i,v in enumerate(ys)}
 def emit(x0,x1,y0,y1,zfunc,ground=False):
  corners=[(x0,y0,zfunc(y0)),(x1,y0,zfunc(y0)),(x1,y1,zfunc(y1)),(x0,y1,zfunc(y1))]
  signature=tuple(tuple(round(v,3) for v in q) for q in corners)
  if signature not in emitted:
   if any(triangle_blocked([signature[0],signature[1],signature[2]],box) or triangle_blocked([signature[0],signature[2],signature[3]],box) for box in (boxes+band if ground else boxes)):return
   emitted.add(signature)
   slope=(zfunc(y1)-zfunc(y0))/(y1-y0);key=(round(slope,8),round(zfunc(y0)-slope*y0,5))
   plane_cells[key].add((xi[x0],yi[y0]))
 for x0,x1 in zip(xs,xs[1:]):
  for y0,y1 in zip(ys,ys[1:]):
   mx=(x0+x1)/2;my=(y0+y1)/2
   in_room=abs(mx-rcx)<rsx/2 and abs(my-rcy)<rsy/2
   lower=ramps[0];under_stair=lower['x'][0]<mx<lower['x'][1] and lower['y'][0]<my<lower['y'][1]
   if not in_room and not under_stair:emit(x0,x1,y0,y1,lambda y:2.0,ground=True)
   for f in floors:
    if f['min'][0]-.001<mx<f['max'][0]+.001 and f['min'][1]-.001<my<f['max'][1]+.001:
     z=round(f['max'][2],3)+2.0;emit(x0,x1,y0,y1,lambda y,z=z:z)
   for r in ramps:
    if r['x'][0]-.001<mx<r['x'][1]+.001 and r['y'][0]-.001<my<r['y'][1]+.001:
     ry0,ry1=[round(v,3) for v in r['y']];rz0,rz1=[round(v,3) for v in r['z']]
     emit(x0,x1,y0,y1,lambda y,a=ry0,b=ry1,c=rz0,d=rz1:c+(d-c)*(y-a)/(b-a)+2.0)
 # Merge free planar grid cells into rectangles before triangulating.
 # Boundary fans include adjacent rectangle corners, eliminating T junctions.
 rectangles=[]
 for (slope,intercept),cells in plane_cells.items():
  remaining=set(cells)
  while remaining:
   ix,iy=min(remaining,key=lambda q:(q[1],q[0]));endx=ix+1
   while (endx,iy) in remaining:endx+=1
   endy=iy+1
   while all((cx,endy) in remaining for cx in range(ix,endx)):endy+=1
   for cy in range(iy,endy):
    for cx in range(ix,endx):remaining.remove((cx,cy))
   x0,x1,y0,y1=xs[ix],xs[endx],ys[iy],ys[endy]
   rectangles.append([(x0,y0,round(slope*y0+intercept,3)),(x1,y0,round(slope*y0+intercept,3)),(x1,y1,round(slope*y1+intercept,3)),(x0,y1,round(slope*y1+intercept,3))])
 corners=sorted(set(tuple(round(v,3) for v in p) for rect in rectangles for p in rect))
 for rect in rectangles:
  center=tuple(sum(p[j] for p in rect)/4 for j in range(3));ci=vert(center)
  boundary=[]
  for a,b in zip(rect,rect[1:]+rect[:1]):
   delta=[b[j]-a[j] for j in range(3)];length=sum(v*v for v in delta);points=[]
   for c in corners:
    t=sum((c[j]-a[j])*delta[j] for j in range(3))/length
    if -.00001<=t<.99999:
     err=sum((c[j]-(a[j]+t*delta[j]))**2 for j in range(3))
     if err<.00001:points.append((t,c))
   boundary.extend(c for t,c in sorted(points))
  ids=[vert(p) for p in boundary]
  for a,b in zip(ids,ids[1:]+ids[:1]):triangles.append((ci,a,b))
 if len(triangles)>32767:raise ValueError('Navmesh needs splitting: '+str(len(triangles)))
 edges={};adj=[[-1,-1,-1] for _ in triangles]
 for ti,t in enumerate(triangles):
  for e in range(3):
   k=tuple(sorted((t[e],t[(e+1)%3])))
   if k in edges:
    oi,oe=edges[k];adj[ti][e]=oi;adj[oi][oe]=ti
   else:edges[k]=(ti,e)
 vmin=[min(p[i] for p in vertices) for i in range(3)];vmax=[max(p[i] for p in vertices) for i in range(3)]
 nv=struct.pack('<IIII',12,0xA5E9A03C,0,IDS['cell'])+U(len(vertices))
 nv+=b''.join(struct.pack('<3f',*v) for v in vertices)+U(len(triangles))
 nv+=b''.join(struct.pack('<3H3hHH',*t,*adj[i],0,0) for i,t in enumerate(triangles))
 nv+=struct.pack('<III',0,0,0) # edge links, doors, cover triangles
 divisor=8;gx=(vmax[0]-vmin[0])/divisor;gy=(vmax[1]-vmin[1])/divisor
 nv+=struct.pack('<I8f',divisor,gx,gy,*vmin,*vmax)
 for cy in range(divisor):
  for cx in range(divisor):
   # Conservative triangle AABB overlaps; never omit a candidate triangle.
   left=vmin[0]+cx*gx;right=left+gx;bottom=vmin[1]+cy*gy;top=bottom+gy
   ts=[i for i,t in enumerate(triangles) if max(vertices[j][0] for j in t)>=left and min(vertices[j][0] for j in t)<=right and max(vertices[j][1] for j in t)>=bottom and min(vertices[j][1] for j in t)<=top]
   nv+=U(len(ts))+b''.join(struct.pack('<h',i) for i in ts)
 # Map infos use only our island, with complete geometry. Isolated cell has no doors.
 center=[sum(p[i] for p in vertices)/len(vertices) for i in range(3)]
 mi=struct.pack('<II4fIII',IDS['navmesh'],32,*center,0.0,0,0,0)+b'\1'
 mi+=struct.pack('<6f',*vmin,*vmax)+U(len(triangles))+b''.join(struct.pack('<3H',*t) for t in triangles)
 mi+=U(len(vertices))+b''.join(struct.pack('<3f',*p) for p in vertices)+struct.pack('<III',0xA5E9A03C,0,IDS['cell'])
 LAST_NAVMESH=(vertices,triangles)
 return nv,mi,{'vanilla_band_obstacles':len(band),'room_footprint':[rcx-rsx/2,rcy-rsy/2,rcx+rsx/2,rcy+rsy/2],'vertices':len(vertices),'triangles':len(triangles),'walk_source':walk_source,'bounds':[vmin,vmax],'capsule_clearance_xy':18.0,'actor_height':128.0,'solid_box_count':len(boxes),'merged_rectangles':len(rectangles),'sloped_barrier_count':len(data.get('stair_edge_barriers_units',[])),'clearance_model':'18-unit conservative horizontal capsule envelope and 128-unit actor height; solid AABBs plus sloped stair-rail prisms. Triangle polygon clipping, reciprocal adjacency, one component required.','walkable_disk_units':data.get('walkable_disk_units')}

def validate_plugin(path):
 p=Plugin(path);r={};counts=collections.Counter()
 for t,o,n,d in p.recorrer():
  if t=='GRUP':continue
  fid=p.form_id(o);ss=dict(p.subrecords(p.datos(o)));r[fid]=(t,ss);counts[t]+=1
  if struct.unpack_from('<H',p.d,o+20)[0]!=44:raise ValueError('wrong formVersion')
  if fid>>24>3:raise ValueError('bad master index')
 if struct.unpack_from('<I',p.d,8)[0]!=0:raise ValueError('ESP must be regular')
 if r[IDS['cell']][1]['EDID']!=b'AstraAsedioTest\0':raise ValueError('missing test cell')
 ammo=r[IDS['ammo']][1];projref=struct.unpack_from('<I',ammo['DATA'])[0]
 if projref not in r or r[projref][0]!='PROJ':raise ValueError('ammo projectile unresolved')
 weap=r[IDS['launcher']][1]
 if len(weap['DATA'])!=10 or len(weap['DNAM'])!=100:raise ValueError('bad WEAP data')
 if weap['NNAM']!=b'ProjectileNode\0':raise ValueError('bad native muzzle node')
 if r[struct.unpack('<I',weap['WNAM'])[0]][0]!='STAT':raise ValueError('bad launcher STAT')
 # v08: siege-only projectile and ammo, siege damage through the weapon and its explosion.
 pdata=r[IDS['projectile']][1]['DATA'];pflags=struct.unpack_from('<H',pdata)[0]
 if pflags&V08['proj_flag_pickup'] or not pflags&V08['proj_flag_explosion']:raise ValueError('siege projectile must be non-pickable and explode')
 expl=struct.unpack_from('<I',pdata,36)[0]
 if expl not in r or r[expl][0]!='EXPL':raise ValueError('siege projectile explosion unresolved')
 if struct.unpack_from('<3f',r[expl][1]['DATA'],24)!=(V08['explosion_force'],V08['explosion_damage'],V08['explosion_radius']):raise ValueError('bad siege explosion')
 if struct.unpack_from('<f',pdata,52)[0]!=V08['impact_force'] or not 0<struct.unpack_from('<f',pdata,72)[0]<10:raise ValueError('bad siege projectile impact or radius')
 if not struct.unpack_from('<I',ammo['DATA'],4)[0]&V08['ammo_flag_nonplayable']:raise ValueError('siege ammo must be non-playable')
 if struct.unpack('<IfH',weap['DATA'])[2]!=V08['weapon_damage'] or struct.unpack_from('<f',weap['DNAM'],96)[0]!=V08['weapon_stagger']:raise ValueError('bad siege weapon damage or stagger')
 if 'SNAM' in weap or 'XNAM' in weap:raise ValueError('weapon attack sound would double the Papyrus shot sound')
 # Plan task 4: the same checks as the tests. The 39-era donor MODT must not survive,
 # the radius is the shaft half-width, and every donor byte not listed in V08 is untouched.
 if r[expl][1].get('MODT')!=bytes.fromhex('020000000000000000000000'):raise ValueError('siege explosion MODT must be the empty formVersion 44 header')
 if abs(struct.unpack_from('<f',pdata,72)[0]-projectile_radius())>1e-4:raise ValueError('siege projectile radius must be the virote shaft half-width')
 donors=json.loads((ROOT/'build/Dawnguard.esm.donors.json').read_text())
 def donor_sub(edid,sub):return bytes.fromhex(next(v for k,v in donors[edid]['subs'] if k==sub))
 def same_except(a,b,ranges):
  if len(a)!=len(b):return False
  keep=[i for i in range(len(a)) if not any(lo<=i<hi for lo,hi in ranges)]
  return all(a[i]==b[i] for i in keep)
 dpdata=donor_sub('DLC1BoltSteelProjectile','DATA')
 changed_flags=V08['proj_flag_pickup']|V08['proj_flag_explosion']
 if struct.unpack_from('<H',pdata)[0]&~changed_flags!=struct.unpack_from('<H',dpdata)[0]&~changed_flags or not same_except(pdata,dpdata,[(0,2),(36,40),(52,56),(72,76)]):
  raise ValueError('siege projectile ballistics (gravity, speed, range) must stay those of the donor')
 if not same_except(weap['DATA'],donor_sub('DLC1TrapCrossbowWeapon01','DATA'),[(8,10)]) or not same_except(weap['DNAM'],donor_sub('DLC1TrapCrossbowWeapon01','DNAM'),[(96,100)]):
  raise ValueError('siege weapon may change only damage and stagger from the donor')
 av=read_vmad(r[IDS['ballesta']][1]['VMAD']);qv=read_vmad(r[IDS['session']][1]['VMAD'],quest=True)
 if (av['version'],av['object_format'])!=(5,2) or av['scripts'][0]['name']!='AstraAsedioActi':raise ValueError('bad activator VMAD')
 props=av['scripts'][0]['properties']
 sight=props.get('UseSightCamera')
 expected_sight=json.loads((ROOT/'config.json').read_text())['use_sight_camera']
 if type(expected_sight) is not bool or not sight or sight['type']!=5 or sight['value'] is not expected_sight:raise ValueError('bad VMAD property UseSightCamera: must match explicit configured mode')
 cfg=json.loads((ROOT/'config.json').read_text())
 for key,name in {'FireSeconds':'fire_seconds','ReleaseSeconds':'release_seconds','ResetSeconds':'reset_seconds','CycleSeconds':'cycle_seconds'}.items():
  if key not in props or props[key]['type']!=4 or abs(props[key]['value']-cfg[name])>.00001:raise ValueError('bad VMAD timing '+key)
 if props.get('ContinuousFire',{}).get('value') is not cfg['continuous_fire']:raise ValueError('bad VMAD ContinuousFire')
 for name,target,typ in [('Session',IDS['session'],'QUST'),('Launcher',IDS['launcher'],'WEAP'),('ShotAmmo',IDS['ammo'],'AMMO')]:
  prop=props.get(name)
  if not prop or prop['type']!=1 or prop['value']!={'form_id':target,'alias':-1} or r[target][0]!=typ:raise ValueError('bad VMAD property '+name)
 steel=props.get('SteelBolt')
 steel_donor=json.loads((ROOT/'build/Dawnguard.esm.donors.json').read_text())['DLC1BoltSteel']
 if not steel or steel['type']!=1 or steel['value']['form_id']!=steel_donor['fid'] or steel['value']['alias']!=-1 or steel_donor['type']!='AMMO':raise ValueError('bad VMAD property SteelBolt')
 sound=props.get('ShotSound')
 if not sound or sound['type']!=1 or sound['value']!={'form_id':IDS['shot_sound'],'alias':-1} or r.get(IDS['shot_sound'],('',))[0]!='SOUN':raise ValueError('bad VMAD property ShotSound')
 fire=json.loads((ROOT/'build/Dawnguard.esm.donors.json').read_text())['WPNCrossbowFire']
 if fire['type']!='SNDR' or r[IDS['shot_sound']][1].get('SDSC')!=U(fire['fid']):raise ValueError('ShotSound must play Dawnguard WPNCrossbowFire')
 # v-guardia: dos scripts en la ballesta (sesión + torre autónoma) y sus forms.
 gcfg=json.loads((ROOT/'config.json').read_text()).get('guardia')
 if gcfg:
  if len(av['scripts'])!=2 or av['scripts'][1]['name']!='AstraGuardiaAuto':raise ValueError('bad auto VMAD')
  ap=av['scripts'][1]['properties']
  for name,target in [('Launcher',IDS['launcher']),('ShotAmmo',IDS['ammo']),('ShotSound',IDS['shot_sound']),('OcupadaGuardia',IDS['ocupada'])]:
   pr=ap.get(name)
   if not pr or pr['type']!=1 or pr['value']!={'form_id':target,'alias':-1}:raise ValueError('bad auto VMAD property '+name)
  for key,ck in {'VelocidadProyectil':'velocidad_proyectil','GravedadProyectil':'gravedad_proyectil','ArcMax':'arc_max','AlcanceMin':'alcance_min','AlcanceMax':'alcance_max','MargenLinea':'margen_linea','MargenImpacto':'margen_impacto','Enfriamiento':'enfriamiento','Anticipacion':'anticipacion','TickSegundos':'tick_segundos'}.items():
   if key not in ap or ap[key]['type']!=4 or abs(ap[key]['value']-gcfg[ck])>1e-4:raise ValueError('bad auto VMAD '+key)
  if ap['MaxRafaga']['type']!=3 or ap['MaxRafaga']['value']!=gcfg['max_rafaga']:raise ValueError('bad auto VMAD MaxRafaga')
  for key,ck in [('YawSpeed','yaw_speed'),('PitchSpeed','pitch_speed'),('PitchMin','pitch_min'),('PitchMax','pitch_max'),('ReleaseSegundos','release_seconds')]:
   if abs(ap[key]['value']-json.loads((ROOT/'config.json').read_text())[ck])>1e-4:raise ValueError('bad auto VMAD mirror '+key)
  if r[IDS['ocupada']][0]!='GLOB':raise ValueError('bad guardia GLOB type')
  gs_=r[IDS['ocupada']][1]
  if gs_['FNAM']!=b's\0' or struct.unpack('<f',gs_['FLTV'])[0]!=0.:raise ValueError('bad guardia GLOB payload')
  if r[IDS['guardia']][0]!='NPC_':raise ValueError('bad guardia NPC type')
  nv=read_vmad(r[IDS['guardia']][1]['VMAD'])
  if nv['scripts'][0]['name']!='AstraGuardiaNPC' or nv['scripts'][0]['properties']:raise ValueError('bad guardia NPC VMAD')
  def link_de(fid):
   v=r[fid][1].get('XLKR')
   return struct.unpack('<II',v)[0] if v else 0
  if link_de(IDS['ballesta_ref'])!=IDS['guardia_ref'] or link_de(IDS['guardia_ref'])!=IDS['ballesta_ref']:raise ValueError('bad guardia XLKR links')
  if r[IDS['guardia_ref']][0]!='ACHR':raise ValueError('guardia ref must be ACHR (REFR with NPC base is never instantiated)')
  if struct.unpack('<I',r[IDS['guardia_ref']][1]['NAME'])[0]!=IDS['guardia']:raise ValueError('guardia ref does not point at the NPC')
 if (qv['version'],qv['object_format'])!=(5,2) or qv['scripts'][0]['name']!='AstraAsedioSession':raise ValueError('bad quest VMAD')
 if len(qv['aliases'])!=1:raise ValueError('bad player alias count')
 alias=qv['aliases'][0]
 if (alias['form_id'],alias['alias'])!=(IDS['session'],0) or alias['scripts'][0]['name']!='AstraAsedioPlayerAlias':raise ValueError('bad player alias VMAD binding')
 if alias['scripts'][0]['properties']['Session']['value']!={'form_id':IDS['session'],'alias':-1}:raise ValueError('bad player alias Session property')
 qs=r[IDS['session']][1]
 if struct.unpack_from('<H',qs['DNAM'])[0]&0x101!=0x101 or qs['ALST']!=U(0) or qs['ALFR']!=U(0x14):raise ValueError('bad start-enabled quest bootstrap')
 for fid,(t,ss) in r.items():
  if t in ('REFR','ACHR'):
   target=struct.unpack('<I',ss['NAME'])[0]
   if target>>24==3 and target not in r:raise ValueError('unresolved '+t)
 nv=r[IDS['navmesh']][1]['NVNM'];off=16
 if struct.unpack_from('<I',nv,12)[0]!=IDS['cell']:raise ValueError('wrong nav parent')
 vc=struct.unpack_from('<I',nv,off)[0];off+=4
 vs=[struct.unpack_from('<3f',nv,off+12*i) for i in range(vc)];off+=vc*12
 tc=struct.unpack_from('<I',nv,off)[0];off+=4
 ts=[struct.unpack_from('<3H3hHH',nv,off+16*i) for i in range(tc)];off+=tc*16
 for i,t in enumerate(ts):
  if len(set(t[:3]))!=3 or max(t[:3])>=vc:raise ValueError('bad nav vertices')
  a,b,c=[vs[j] for j in t[:3]]
  area=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
  if abs(area)<.01:raise ValueError('degenerate nav triangle')
  for e,j in enumerate(t[3:6]):
   if j>=tc or j<-1:raise ValueError('bad nav adjacency')
   if j>=0 and i not in ts[j][3:6]:raise ValueError('nonreciprocal nav edge')
 for _ in range(3):
  if struct.unpack_from('<I',nv,off)[0]!=0:raise ValueError('unexpected nav link')
  off+=4
 div=struct.unpack_from('<I',nv,off)[0];off+=36
 for _ in range(div*div):
  n=struct.unpack_from('<I',nv,off)[0];off+=4
  if n:
   if max(struct.unpack_from('<'+str(n)+'h',nv,off))>=tc:raise ValueError('invalid grid')
  off+=n*2
 if off!=len(nv):raise ValueError('navmesh tail mismatch')
 boxes=collision_boxes()
 for i,t in enumerate(ts):
  if any(triangle_blocked([vs[j] for j in t[:3]],box) for box in boxes):raise ValueError('Navmesh triangle intersects expanded collision: '+str(i))
 # v11: the ground must also clear every vanilla piece where an actor walks.
 cfg=json.loads((ROOT/'config.json').read_text());pieces=L.resolve_pieces(cfg)
 band=L.band_boxes(cfg['tower_v11']['pieces'],cfg=cfg)
 for i,t in enumerate(ts):
  tri=[vs[j] for j in t[:3]]
  if max(v[2] for v in tri)<=10 and any(triangle_blocked(tri,b) for b in band):raise ValueError('Ground navmesh triangle intersects a vanilla piece: '+str(i))
 placed=collections.Counter(struct.unpack('<I',ss['NAME'])[0] for fid,(t,ss) in r.items() if t=='REFR' and VANILLA_FIRST<=fid<VANILLA_FIRST+len(pieces))
 if placed!=collections.Counter(p['formid'] for p in pieces):raise ValueError('vanilla references do not match the tower_v11 layout')
 if any('XTEL' in ss for fid,(t,ss) in r.items() if t=='REFR' and struct.unpack('<I',ss['NAME'])[0]==0x000C78A3):raise ValueError('the room door must not teleport')
 mi=r[0x12FB4][1]['NVMI']
 if struct.unpack_from('<I',mi)[0]!=IDS['navmesh'] or struct.unpack_from('<I',mi,len(mi)-4)[0]!=IDS['cell']:raise ValueError('bad map parent')
 unseen=set(range(tc));components=0
 while unseen:
  components+=1;todo=[unseen.pop()]
  while todo:
   ti=todo.pop()
   for j in ts[ti][3:6]:
    if j in unseen:unseen.remove(j);todo.append(j)
 return {'vmad_bindings_verified':True,'player_alias_bootstrap_structurally_verified':True,'navmesh_clearance_verified':True,'navmesh_components':components,'navmesh_max_z':max(v[2] for v in vs),'structural_valid':True,'record_types':dict(counts),'navmesh_vertices':vc,'navmesh_triangles':tc,'ck_finalized_verified':False,'in_game_verified':False,'sha256':hashlib.sha256(p.d).hexdigest(),'size':len(p.d)}

def build():
 cfg=json.loads((ROOT/'config.json').read_text());data=Path(cfg['runtime'])/'Data'
 dg=find_records(data/'Dawnguard.esm',['DLC1TrapCrossbowWeapon01','DLC1BoltSteel','DLC1BoltSteelProjectile','WPNCrossbowFire'])
 sk=find_records(data/'Skyrim.esm',['QASmoke','WRIntFloorSTMid01Large','ArcheryTarget','ArcheryTargetTripod','TreasChestSmallEMPTYNoRespawn','DefaultImageSpace','MagicVoiceDragonRendProjectileLight','TrapBallistaBoltExplosion02'])
 if dg['WPNCrossbowFire']['type']!='SNDR' or sk['TrapBallistaBoltExplosion02']['type']!='EXPL':raise ValueError('v08 sound/explosion donors changed type')
 if sk['DefaultImageSpace']['fid']!=0x167 or struct.unpack('<4f',dict(sk['DefaultImageSpace']['subs'])['TNAM'])!=(0.,1.,1.,1.):raise ValueError('neutral vanilla ImageSpace changed')
 gcfg=cfg.get('guardia')
 guard_donor=None
 if gcfg:
  guard_donor=find_guard_npc(data/'Skyrim.esm',gcfg['donores_npc'])
 (ROOT/'build/Dawnguard.esm.donors.json').write_text(json.dumps({k:{**{q:v for q,v in d.items() if q!='subs'},'subs':[[k,v.hex()] for k,v in d['subs']]} for k,d in dg.items()},indent=2))
 groups=[];new=[]
 def add(t,fid,ss,flags=0):
  new.append(fid);return W.record(t,fid,ss,banderas=flags)
 groups.append(W.grupo('STAT',[add('STAT',IDS['tower'],stat('AstraAsedioTower','AstraAsedio\\torre.nif',bound('torre',[-420,-420,0,420,420,700]))),add('STAT',IDS['launcher_stat'],stat('AstraAsedioLauncherModel','AstraAsedio\\ballesta.nif',bound('ballesta',[-350,-300,0,350,300,250])))]))
 props={'Session':(1,IDS['session']),'Launcher':(1,IDS['launcher']),'ShotAmmo':(1,IDS['ammo']),'SteelBolt':(1,dg['DLC1BoltSteel']['fid']),'ShotSound':(1,IDS['shot_sound'])}
 for k,v in {'FireSeconds':'fire_seconds','ReleaseSeconds':'release_seconds','ResetSeconds':'reset_seconds','CycleSeconds':'cycle_seconds','YawSpeed':'yaw_speed','PitchSpeed':'pitch_speed','PitchMin':'pitch_min','PitchMax':'pitch_max','OperatorDistance':'operator_distance'}.items():props[k]=(4,cfg[v])
 props['TickSeconds']=(4,1/cfg['controller_hz']);props['PitchSign']=(4,-1.0)
 props['UseMouseAim']=(5,cfg['mouse_aim']);props['PitchPivotHeight']=(4,cfg['pitch_pivot_units'])
 props['UseSightCamera']=(5,cfg['use_sight_camera'])
 props['ContinuousFire']=(5,cfg['continuous_fire'])
 props['OperatorHeight']=(4,119.);props['OperatorVerticalTolerance']=(4,64.)
 props['OcupadaGuardia']=(1,IDS['ocupada'])
 auto_props=None
 if gcfg:
  auto_props={'Launcher':(1,IDS['launcher']),'ShotAmmo':(1,IDS['ammo']),'ShotSound':(1,IDS['shot_sound']),'OcupadaGuardia':(1,IDS['ocupada']),
   'VelocidadProyectil':(4,gcfg['velocidad_proyectil']),'GravedadProyectil':(4,gcfg['gravedad_proyectil']),
   'MuzzleAlto':(4,gcfg['muzzle_alto']),'MuzzleAdelante':(4,gcfg['muzzle_adelante']),
   'ArcMax':(4,gcfg['arc_max']),'AlcanceMin':(4,gcfg['alcance_min']),'AlcanceMax':(4,gcfg['alcance_max']),
   'MargenLinea':(4,gcfg['margen_linea']),'MargenImpacto':(4,gcfg['margen_impacto']),
   'MaxRafaga':(3,gcfg['max_rafaga']),'Enfriamiento':(4,gcfg['enfriamiento']),'Anticipacion':(4,gcfg['anticipacion']),
   'TickSegundos':(4,gcfg['tick_segundos']),'QALog':(5,gcfg['qa_log']),
   'YawSpeed':(4,cfg['yaw_speed']),'PitchSpeed':(4,cfg['pitch_speed']),
   'PitchMin':(4,cfg['pitch_min']),'PitchMax':(4,cfg['pitch_max']),'ReleaseSegundos':(4,cfg['release_seconds'])}
 acti_scripts=[('AstraAsedioActi',props)]+([('AstraGuardiaAuto',auto_props)] if auto_props else [])
 acti=[W.sub('EDID',W.zstr('AstraAsedioBallesta')),W.sub('VMAD',vmad_multi(acti_scripts)),W.sub('OBND',bound('ballesta',[-350,-300,0,350,300,250])),W.sub('FULL',W.zstr('Ballesta de asedio Astra')),W.sub('MODL',W.zstr('AstraAsedio\\ballesta.nif')),W.sub('MODT',bytes.fromhex('020000000000000000000000')),W.sub('FNAM',struct.pack('<H',0))]
 groups.append(W.grupo('ACTI',[add('ACTI',IDS['ballesta'],acti)]))
 # v-guardia: flag compartido sesión/demo <-> torre autónoma
 groups.append(W.grupo('GLOB',[add('GLOB',IDS['ocupada'],[W.sub('EDID',W.zstr('AstraGuardiaOcupada')),W.sub('FNAM',b's\0'),W.sub('FLTV',struct.pack('<f',0.0))])]))
 if guard_donor:
  # Clon de un guardia vanilla: paquetes/facciones/combate del donante (sandbox
  # anclado a la ubicación del editor = la torre). El VMAD del sensor va justo
  # después de EDID, como exige el orden de subrecords de NPC_.
  gsubs=[]
  for k,v in guard_donor['subs']:
   if k=='EDID':
    gsubs.append(W.sub('EDID',W.zstr('AstraGuardiaNPC')))
    gsubs.append(W.sub('VMAD',vmad('AstraGuardiaNPC',{})))
   elif k=='VMAD':
    continue
   elif k=='FULL':
    gsubs.append(W.sub('FULL',W.zstr(gcfg['nombre'])))
   else:
    gsubs.append(W.sub(k,v))
  groups.append(W.grupo('NPC_',[add('NPC_',IDS['guardia'],gsubs)]))
 light_donor=sk['MagicVoiceDragonRendProjectileLight']
 groups.append(W.grupo('LIGH',[add('LIGH',IDS['light_fill'],neutral_light(light_donor,'AstraAsedioNeutralFill',1450)),add('LIGH',IDS['light_target'],neutral_light(light_donor,'AstraAsedioNeutralTargetLight',900))]))
 # v08 B1/B2: donor ballistics (gravity, speed, range) unchanged; only pickup, explosion, impact and radius move.
 proj_data=bytearray(dict(dg['DLC1BoltSteelProjectile']['subs'])['DATA'])
 if len(proj_data)!=92:raise ValueError('unexpected PROJ DATA layout')
 flags=struct.unpack_from('<H',proj_data)[0]
 struct.pack_into('<H',proj_data,0,(flags&~V08['proj_flag_pickup'])|V08['proj_flag_explosion'])
 struct.pack_into('<I',proj_data,36,IDS['explosion']);struct.pack_into('<f',proj_data,52,V08['impact_force'])
 radius=projectile_radius();struct.pack_into('<f',proj_data,72,radius)
 updates={'FULL':W.zstr(V08['names']['projectile']),'MODL':W.zstr('AstraAsedio\\virote.nif'),'MODT':bytes.fromhex('020000000000000000000000'),'OBND':bound('virote',[-8,-180,-8,8,8,8]),'DATA':bytes(proj_data)}
 groups.append(W.grupo('PROJ',[add('PROJ',IDS['projectile'],replace_clone(dg['DLC1BoltSteelProjectile'],'AstraAsedioProjectile',updates))]))
 # Same layout as the vanilla ballista ammo (DLC2DwarvenBallistaBolt, flags 0x7): never playable.
 ammo_data=bytearray(dict(dg['DLC1BoltSteel']['subs'])['DATA']);struct.pack_into('<I',ammo_data,0,IDS['projectile'])
 struct.pack_into('<I',ammo_data,4,struct.unpack_from('<I',ammo_data,4)[0]|V08['ammo_flag_nonplayable'])
 groups.append(W.grupo('AMMO',[add('AMMO',IDS['ammo'],replace_clone(dg['DLC1BoltSteel'],'AstraAsedioNativeBolt',{'FULL':W.zstr(V08['names']['ammo']),'DESC':b'\0','DATA':bytes(ammo_data),'MODL':W.zstr('AstraAsedio\\virote.nif')}))]))
 weap_subs=dict(dg['DLC1TrapCrossbowWeapon01']['subs'])
 weap_data=bytearray(weap_subs['DATA']);struct.pack_into('<H',weap_data,8,V08['weapon_damage'])
 weap_dnam=bytearray(weap_subs['DNAM']);struct.pack_into('<f',weap_dnam,96,V08['weapon_stagger'])
 groups.append(W.grupo('WEAP',[add('WEAP',IDS['launcher'],replace_clone(dg['DLC1TrapCrossbowWeapon01'],'AstraAsedioNativeLauncher',{'FULL':W.zstr(V08['names']['launcher']),'DESC':b'\0','NNAM':W.zstr('ProjectileNode'),'WNAM':U(IDS['launcher_stat']),'DATA':bytes(weap_data),'DNAM':bytes(weap_dnam)}))]))
 # The donor EXPL is formVersion 39: its MODT triples are misread under 44 (skill trap 26), so ship the empty 44 header.
 expl_data=bytearray(dict(sk['TrapBallistaBoltExplosion02']['subs'])['DATA'])
 if len(expl_data)!=52:raise ValueError('unexpected EXPL DATA layout')
 struct.pack_into('<3f',expl_data,24,V08['explosion_force'],V08['explosion_damage'],V08['explosion_radius'])
 groups.append(W.grupo('EXPL',[add('EXPL',IDS['explosion'],replace_clone(sk['TrapBallistaBoltExplosion02'],'AstraAsedioImpactoEXPL',{'MODT':bytes.fromhex('020000000000000000000000'),'DATA':bytes(expl_data)}))]))
 # Weapon.Fire from an object has no attack sound; Papyrus plays this once per launched bolt.
 groups.append(W.grupo('SOUN',[add('SOUN',IDS['shot_sound'],[W.sub('EDID',W.zstr('AstraAsedioDisparoSOUN')),W.sub('OBND',bytes(12)),W.sub('SDSC',U(dg['WPNCrossbowFire']['fid']))])]))
 cont=replace_clone(sk['TreasChestSmallEMPTYNoRespawn'],'AstraAsedioBoltChest',{'FULL':W.zstr('Suministro de virotes de acero Astra')},drop=['CNTO','COCT','VMAD'])
 # Inventory count precedes CNTO and DATA as required by CONT layout.
 at=next(i for i,s in enumerate(cont) if s[:4]==b'DATA');cont[at:at]=[W.sub('COCT',U(1)),W.sub('CNTO',struct.pack('<Ii',dg['DLC1BoltSteel']['fid'],200))]
 groups.append(W.grupo('CONT',[add('CONT',IDS['container'],cont)]))
 quest=[W.sub('EDID',W.zstr('AstraAsedioSessionQuest')),W.sub('VMAD',quest_vmad()),W.sub('DNAM',struct.pack('<HBBII',0x101,50,0,0,0)),W.sub('NEXT',b''),W.sub('ANAM',U(1)),W.sub('ALST',U(0)),W.sub('ALID',W.zstr('Player')),W.sub('FNAM',U(4)),W.sub('ALFR',U(0x14)),W.sub('ALED',b'')]
 groups.append(W.grupo('QUST',[add('QUST',IDS['session'],quest)]))
 cellss=replace_clone(sk['QASmoke'],'AstraAsedioTest',{'FULL':W.zstr('Sala de pruebas de asedio Astra'),'XCLL':neutral_cell_lighting(dict(sk['QASmoke']['subs'])['XCLL']),'XCIM':U(sk['DefaultImageSpace']['fid'])})
 cell=add('CELL',IDS['cell'],cellss)
 # The navmesh first: the spawn marker must land on it (v11 spec §1).
 nv,mi,nreport=navmesh_geometry();marker=spawn_marker(cfg,*LAST_NAVMESH)
 persistent=[reference(IDS['ballesta_ref'],IDS['ballesta'],(0,0,cfg['tower_top_units']),edid='AstraAsedioBallestaREF',persistent=True,link=IDS['guardia_ref'] if guard_donor else 0),reference(IDS['spawn_ref'],0x34,tuple(marker['pos']),math.pi,edid='AstraAsedioCOCMarker',persistent=True)]
 new.extend([IDS['ballesta_ref'],IDS['spawn_ref']])
 refs=[reference(IDS['tower_ref'],IDS['tower'],(0,0,0),edid='AstraAsedioTowerREF'),reference(IDS['container_ref'],IDS['container'],(400,380,2),edid='AstraAsedioBoltChestREF')];new.extend([IDS['tower_ref'],IDS['container_ref']])
 if guard_donor:
  gx,gy,gz=gcfg['posicion'];gangle=math.atan2(-gx,-gy)
  refs.append(reference(IDS['guardia_ref'],IDS['guardia'],(gx,gy,gz),gangle,edid='AstraGuardiaREF',link=IDS['ballesta_ref'],tipo='ACHR'));new.append(IDS['guardia_ref'])
 nextid=0x03000910
 for x in [-1536,-512,512,1536]:
  for y in [-2048,-1024,0,1024]:
   refs.append(reference(nextid,sk['WRIntFloorSTMid01Large']['fid'],(x,y,0)));new.append(nextid);nextid+=1
 muzzle=(0.0,-224.0,cfg['tower_top_units']+cfg['pitch_pivot_units']+19.6)
 target_z=muzzle[2]-65.0
 for dist in [700,2100]:
  # Measured vanilla bullseye faces local -X. Skyrim heading is clockwise:
  # +90 degrees rotates that front to +Y, toward the muzzle at the origin.
  # NiMatrix3::SetEulerAnglesXYZ uses [cosZ,sinZ; -sinZ,cosZ].
  refs.append(reference(nextid,sk['ArcheryTargetTripod']['fid'],(0,muzzle[1]-dist,target_z),math.pi/2,edid='AstraAsedioTarget'+str(dist)));new.append(nextid);nextid+=1
  refs.append(reference(nextid,sk['ArcheryTarget']['fid'],(0,muzzle[1]-dist,target_z),math.pi/2));new.append(nextid);nextid+=1
  # Native floor under elevated static target, with Havok collision.
  refs.append(reference(nextid,sk['WRIntFloorSTMid01Large']['fid'],(0,muzzle[1]-dist,target_z-2.0)));new.append(nextid);nextid+=1
 for fid,base,pos in [(0x03000930,IDS['light_fill'],(-650,300,850)),(0x03000931,IDS['light_fill'],(650,-350,850)),(0x03000932,IDS['light_target'],(0,-924,900)),(0x03000933,IDS['light_target'],(0,-2324,900))]:
  refs.append(reference(fid,base,pos));new.append(fid)
 # v11: stilts, braces, room walls and ceiling, and the room door, as references to Skyrim.esm.
 pieces=L.resolve_pieces(cfg);vanilla_refs=[]
 for k,p in enumerate(pieces):
  fid=VANILLA_FIRST+k
  if fid&0xFFF>=0xFFF:raise ValueError('vanilla references must stay below 0xFFF (ESL range)')
  refs.append(reference(fid,p['formid'],tuple(p['pos']),rot=tuple(math.radians(a) for a in p['rot_deg']),scale=p['scale']));new.append(fid)
  vanilla_refs.append({'name':p['name'],'form_id':f'{fid:08X}','base':f'{p["formid"]:08X}','edid':p['edid'],'role':p['role'],'scale':p['scale']})
 refs.append(add('NAVM',IDS['navmesh'],[W.sub('NVNM',nv)]))
 children=W.grupo(U(IDS['cell']),[W.grupo(U(IDS['cell']),persistent,8),W.grupo(U(IDS['cell']),refs,9)],6)
 local_cell=IDS['cell']&0xffffff;subblock=W.grupo(struct.pack('<i',(local_cell//10)%10),[cell,children],3);block=W.grupo(struct.pack('<i',local_cell%10),[subblock],2)
 groups.append(W.grupo('CELL',[block]))
 groups.append(W.grupo('NAVI',[W.record('NAVI',0x12FB4,[W.sub('NVER',U(12)),W.sub('NVMI',mi),W.sub('NVPP',struct.pack('<II',0,0))])]))
 esp=ROOT/'mod/AstraAsedio.esp';W.escribir(esp,MASTERS,groups,new,autor='Astra',esl=False,descripcion='Stationary siege crossbow. Isolated test cell. Requires SKSE64.')
 # xEdit GenerateSEQFileForFile writes start-enabled quests as FixedFormID uint32s.
 # Keep file-relative master index 03; the runtime resolves the plugin's load order.
 seq=ROOT/'mod/seq/AstraAsedio.seq';seq.parent.mkdir(parents=True,exist_ok=True);seq.write_bytes(U(IDS['session']))
 report=validate_plugin(esp);report.update({'masters':MASTERS,'forms':{k:f'{v:08X}' for k,v in IDS.items()},'muzzle_rest_world':muzzle,'targets':{'10m':[0,muzzle[1]-700,muzzle[2]],'30m':[0,muzzle[1]-2100,muzzle[2]]},'navmesh':nreport,'donors':{k:f'{v["fid"]:08X}' for k,v in dg.items()},'NAVI':'Singleton 00012FB4 with only own NVMI; master files unchanged','limitations':['CK finalization not run','Native shooter attribution and in-game damage not verified','Navmesh avoids expanded collision boxes; CK path tests are pending']})
 report['test_room']={'neutral_imagespace':'00000167 DefaultImageSpace','ambient_rgb':[112,112,112],'directional_rgb':[80,80,80],'fog_max':0.,'native_light_count':4,'shadow_light_count':0,'light_donor':f'{light_donor["fid"]:08X} MagicVoiceDragonRendProjectileLight','light_radii_units':[1450,1450,900,900],'archery_target_form_id':f'{sk["ArcheryTarget"]["fid"]:08X}','target_heading_degrees':90.,'target_front_world_approx':[0.,.94,.34],'heading_source':'https://raw.githubusercontent.com/powerof3/CommonLibSSE/dev/src/RE/N/NiMatrix3.cpp','visual_in_game_verified':False}
 report['siege']={'weapon_damage':V08['weapon_damage'],'ammo_damage':struct.unpack_from('<f',ammo_data,8)[0],'explosion_damage':V08['explosion_damage'],'explosion_radius':V08['explosion_radius'],'explosion_force':V08['explosion_force'],'explosion_donor':'Skyrim.esm TrapBallistaBoltExplosion02','impact_force':V08['impact_force'],'weapon_stagger':V08['weapon_stagger'],'projectile_collision_radius':radius,'projectile_pickable':False,'ammo_playable':False,'shot_sound':'Dawnguard.esm WPNCrossbowFire via Papyrus SOUN','damage_composition_in_game_verified':False}
 report['vanilla_references']=vanilla_refs
 report['spawn_marker']=marker
 report['door']={'base':'000C78A3 FarmhouseAnimDoor01','teleport':False,'opens':cfg['tower_v11']['room']['door_opens'],'swing_verified_in_game':False}
 report['angle_convention']={k:v for k,v in json.loads((ROOT/'reports/angle_convention.json').read_text()).items() if k in ('decided','order','signs','falsified')}
 report['guardia']={'donante_npc':(guard_donor or {}).get('edid'),'donante_fid':('%08X'%guard_donor['fid']) if guard_donor else None,
  'nombre':gcfg['nombre'] if gcfg else None,'posicion':gcfg['posicion'] if gcfg else None,
  'glob_ocupada':'%08X'%IDS['ocupada'],'auto_script':'AstraGuardiaAuto en la ballesta (segundo VMAD)',
  'balistica':{'velocidad':gcfg['velocidad_proyectil'],'gravedad':gcfg['gravedad_proyectil'],'fuente':'native/src/Core.cpp v08 sight zero (5400 u/s, 0.35*9.81*70)'},
  'reglas':{'arc_max':gcfg['arc_max'],'alcance_min':gcfg['alcance_min'],'alcance_max':gcfg['alcance_max'],'max_rafaga':gcfg['max_rafaga'],'enfriamiento':gcfg['enfriamiento'],'margen_linea':gcfg['margen_linea']},
  'sensor':'combate vanilla del NPC (OnCombatStateChanged) + IsDetectedBy como LOS',
  'prioridad':'GlobalVariable AstraGuardiaOcupada: sesión y demo del jugador siempre ganan',
  'in_game_verified':False}
 report['activation']={'operator_distance_xy':cfg['operator_distance'],'operator_height_from_root':119.,'operator_vertical_tolerance':64.,'new_interaction_form':False,'rejection_notifications':True}
 report['seq']={'path':str(seq.relative_to(ROOT)), 'sha256':hashlib.sha256(seq.read_bytes()).hexdigest(), 'quest_fixed_form_id':f'{IDS["session"]:08X}', 'format_reference':'https://github.com/TES5Edit/TES5Edit/blob/dev-4.1.6/xEdit/xeMainForm.pas'}
 (ROOT/'reports/plugin_build.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
 return report
if __name__=='__main__':build()

