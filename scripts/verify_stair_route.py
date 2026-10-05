"""v09: check the reimported torre.nif collision and explicit feet samples in the written NAVM (Blender).

From Ballesta_Astra_Escalera_Directa_v01, adapted: the rustic pass bends body/roof pieces on purpose,
so their vertices are bounded instead of identical, and the collision layout must equal the frozen
square-stair reference.
"""
import bpy,addon_utils,json,sys,math,struct,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/vendor'))
from parser_esm import Plugin
cfg=json.loads((ROOT/'config.json').read_text());s=cfg['meters_to_units']
DRIFT_LIMIT_M=.22   # v09 amplitudes: log ends up to 0.13 m plus thickness and lean
addon_utils.enable('io_scene_nifly',default_set=True)
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
bpy.context.view_layer.objects.active=None
bpy.ops.import_scene.pynifly(filepath=str(ROOT/'mod/meshes/AstraAsedio/torre.nif'),blender_xf=False,create_bones=False,import_animations=False,import_collisions=True)
bpy.context.view_layer.update()
vertices=[];triangles=[]
for o in bpy.data.objects:
    if o.type!='MESH' or not o.name.startswith('bhk'):continue
    o.data.calc_loop_triangles();base=len(vertices)
    vertices.extend(o.matrix_world@v.co for v in o.data.vertices)
    triangles.extend(tuple(base+i for i in t.vertices) for t in o.data.loop_triangles)
assert vertices
bvh=BVHTree.FromPolygons(vertices,triangles,all_triangles=True)
walk=json.loads((ROOT/'reports/collision_walkable.json').read_text());r=walk['ramps'][0]
reference=json.loads((ROOT/'reports/reference_collision_escalera_directa.json').read_text())
# v10: the ballista pedestal box is lowered on purpose (camera pull-in, reports/user_evidence_v09.json);
# every stair/tower key must still equal the square-stair reference.
stair_keys=[k for k in reference if k!='ballesta_fixed_box_units']
assert {k:walk[k] for k in stair_keys}=={k:reference[k] for k in stair_keys},'Collision layout differs from the square stair reference'
pedestal=walk['ballesta_fixed_box_units'];ref_pedestal=reference['ballesta_fixed_box_units']
# Same footprint and base as the reference; only the top is lowered.
assert pedestal['min']==ref_pedestal['min'] and pedestal['max'][:2]==ref_pedestal['max'][:2],('pedestal footprint differs from the reference',pedestal,ref_pedestal)
assert abs(pedestal['max'][2]-pedestal['min'][2]-cfg['sight']['pedestal_collision_height_units'])<1e-3,('pedestal collision height',pedestal)
x=sum(r['x'])/2;y0,y1=r['y'];z0,z1=r['z']
route=[(x,y0-42,0)]
route.extend((x,y0+(y1-y0)*i/100,z0+(z1-z0)*i/100) for i in range(101))
route.extend((x,y1+(238-y1)*i/10,z1) for i in range(1,11))
route.extend((x+(238-x)*i/15,238,z1) for i in range(1,16))
errors=[];body_hits=[];rail_hits=[];floor_samples=[];edge_probe_recoveries=[]
for k,p in enumerate(route[1:]):
    loc,normal,index,distance=bvh.ray_cast(Vector((p[0],p[1],p[2]+20)),Vector((0,0,-1)),40)
    # A ray on a triangulation diagonal can miss both top triangles in BVH.
    # Probe within 0.02 unit (0.29 mm); retain the original miss in evidence.
    if loc is None or abs(loc.z-p[2])>.03:
        edge_probe_recoveries.append({'sample':k,'exact_ray_hit':list(loc) if loc is not None else None})
        candidates=[bvh.ray_cast(Vector((p[0]+dx,p[1]+dy,p[2]+20)),Vector((0,0,-1)),40) for dx,dy in ((.02,0),(-.02,0),(0,.02),(0,-.02))]
        candidates=[h for h in candidates if h[0] is not None]
        if candidates:loc,normal,index,distance=min(candidates,key=lambda h:abs(h[0].z-p[2]))
    assert loc is not None,('Missing floor',k,p)
    errors.append(abs(loc.z-p[2]))
    floor_samples.append({'sample':k,'expected':p,'hit':list(loc),'normal':list(normal),'triangle':index,'error':errors[-1]})
    for h in (25,64,112):
        origin=Vector((p[0],p[1],p[2]+h))
        for j in range(8):
            direction=Vector((math.cos(j*math.tau/8),math.sin(j*math.tau/8),0))
            hit=bvh.ray_cast(origin,direction,18)
            if hit[0] is not None:body_hits.append({'sample':k,'height':h,'distance':hit[3]})
    if 1<k<99:
        for sign in (-1,1):
            hit=bvh.ray_cast(Vector((p[0],p[1],p[2]+.53*s)),Vector((sign,0,0)),.65*s)
            assert hit[0] is not None,('Missing side protection',k,sign)
            rail_hits.append(hit[3])
(ROOT/'reports/route_diagnostics.json').write_text(json.dumps({'floors':floor_samples,'body_hits':body_hits},indent=2))
assert max(errors)<.03, sorted(floor_samples,key=lambda p:p['error'],reverse=True)[:3]
assert not body_hits,body_hits[:10]
removed_checks={}
for name,p in [('frontal',(0,-180,230)),('izquierdo',(-180,0,230)),('trasero',(0,180,230))]:
    removed_checks[name]=bvh.ray_cast(Vector(p),Vector((0,0,-1)),25)[0] is None
assert all(removed_checks.values()),removed_checks
plugin=Plugin(str(ROOT/'mod/AstraAsedio.esp'))
nv=next(dict(plugin.subrecords(plugin.datos(o)))['NVNM'] for t,o,n,d in plugin.recorrer() if t=='NAVM')
vc=struct.unpack_from('<I',nv,16)[0];vs=[struct.unpack_from('<3f',nv,20+12*i) for i in range(vc)]
off=20+12*vc;tc=struct.unpack_from('<I',nv,off)[0];off+=4
ts=[struct.unpack_from('<3H3hHH',nv,off+16*i) for i in range(tc)]
def contains(foot,t):
    a,b,c=[vs[j] for j in t[:3]]
    dx=foot[0]-a[0];dy=foot[1]-a[1]
    den=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    u=(dx*(c[1]-a[1])-dy*(c[0]-a[0]))/den
    v=((b[0]-a[0])*dy-(b[1]-a[1])*dx)/den
    z=a[2]+u*(b[2]-a[2])+v*(c[2]-a[2])
    return min(u,v,1-u-v)>=-.0001 and abs(z-foot[2]-2)<.03
uncovered=[(k,p) for k,p in enumerate(route) if not any(contains(p,t) for t in ts)]
assert not uncovered,uncovered[:10]
# The rustic pass bends body/roof pieces on purpose: same pieces, bounded drift.
def snapshot(path):
    bpy.ops.wm.open_mainfile(filepath=str(path),use_scripts=False)
    bpy.context.scene.frame_set(1);bpy.context.view_layer.update()
    result={}
    for o in bpy.context.scene.objects:
        if o.type=='MESH' and any(c.name in ('01_Torre','03_Plataforma') for c in o.users_collection):
            result[o.name]=[[round(x,6) for x in o.matrix_world@v.co] for v in o.data.vertices]
    return result
original=snapshot(ROOT/'source/Torre_Ballesta_lowpoly_v04.blend')
editable=snapshot(ROOT/'source/Torre_escalera_rustica.blend')
assert set(original)==set(editable),'Body/roof pieces added or removed'
def box(vs):return [min(v[j] for v in vs) for j in range(3)]+[max(v[j] for v in vs) for j in range(3)]
drift=max(abs(a-b) for n in original for a,b in zip(box(original[n]),box(editable[n])))
changed=sum(1 for n in original if box(original[n])!=box(editable[n]))
assert drift<=DRIFT_LIMIT_M,('Body/roof drift too large',drift)
assert changed>=100,('Rustic pass did not reach the body/roof pieces',changed)
# Walk surfaces (treads, roof planks, landing) are generated or bent before export; their measured
# vertical drift is bound to this exact torre.nif and must stay within the floor limit.
rustic=json.loads((ROOT/'reports/rustico.json').read_text())
assert rustic['torre_nif_sha256']==hashlib.sha256((ROOT/'mod/meshes/AstraAsedio/torre.nif').read_bytes()).hexdigest(),'rustico.json is for another torre.nif'
assert rustic['floor_pieces']>=80,('floor pieces missing from the rustic report',rustic['floor_pieces'])
assert rustic['floor_vertical_measured_m']<=rustic['floor_vertical_limit_m']+1e-6,('floor pieces moved vertically',rustic['floor_vertical_measured_m'])
report={'success':True,'collision_mesh_triangles':len(triangles),'route_samples':len(route),'max_floor_error_units':max(errors),
    'diagonal_edge_probe_recoveries':edge_probe_recoveries,'edge_probe_max_offset_units':.02,
    'clearance_sample_rays':len(route[1:])*3*8,'body_clearance_blocking_hits':body_hits,'side_barrier_rays':len(rail_hits),
    'old_balcony_collision_absent':removed_checks,'navmesh_covered_route_samples':len(route),'uncovered_navmesh_samples':uncovered,
    'collision_layout_equal_to_reference':True,'reference':'reports/reference_collision_escalera_directa.json',
    'body_and_roof_pieces':len(original),'floor_pieces':rustic['floor_pieces'],'floor_vertical_measured_m':rustic['floor_vertical_measured_m'],'body_and_roof_pieces_bent':changed,'body_and_roof_max_bbox_drift_m':drift,'drift_limit_m':DRIFT_LIMIT_M,
    'nif_sha256':hashlib.sha256((ROOT/'mod/meshes/AstraAsedio/torre.nif').read_bytes()).hexdigest(),
    'esp_sha256':hashlib.sha256((ROOT/'mod/AstraAsedio.esp').read_bytes()).hexdigest(),
    'engine_movement_tested':False,'scope':'Static geometric samples of reimported Havok and NAVM; not an engine actor simulation.'}
(ROOT/'reports/stair_route_verified.json').write_text(json.dumps(report,indent=2))
print('STAIR_ROUTE_VERIFIED',len(route),'samples;',changed,'of',len(original),'body/roof pieces bent; drift',round(drift,3))
