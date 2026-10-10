"""Reimport written Havok and verify walking route, headroom and laboratory NAVM."""
import sys
import json
import math
import struct
import hashlib
from pathlib import Path
import bpy
import addon_utils
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
import v11_layout as L
from parser_esm import Plugin

def main():
    cfg = L.load_cfg()
    addon_utils.enable('io_scene_nifly',default_set=True)
    for o in list(bpy.data.objects): bpy.data.objects.remove(o,do_unlink=True)
    bpy.context.view_layer.objects.active = None
    bpy.ops.import_scene.pynifly(filepath=str(ROOT/'mod/meshes/AstraAsedio/torre.nif'),
        blender_xf=False,create_bones=False,import_animations=False,import_collisions=True)
    bpy.context.view_layer.update()
    verts, tris = [], []
    for o in bpy.data.objects:
        if o.type != 'MESH' or not o.name.startswith('bhk'): continue
        o.data.calc_loop_triangles(); base = len(verts)
        verts.extend(o.matrix_world @ v.co for v in o.data.vertices)
        tris.extend(tuple(base+j for j in t.vertices) for t in o.data.loop_triangles)
    assert verts, 'Missing exported collision'
    floor_tree = BVHTree.FromPolygons(verts,tris,all_triangles=True)
    # Shields are checked as physical visual obstacles to catch clipping on the stair.
    esc = cfg['tower_v11']['escudos']
    sv, st = L.nif_triangles(Path(cfg['extracted'])/'meshes'/esc['modl'])
    for it in esc['items']:
        m = L.transform_matrix(it['pos'],it['rot_deg'],1.0,*L.engine_convention())
        vv = sv @ np.array(m['r']).T + np.array(m['t']); base=len(verts)
        verts.extend(Vector(v) for v in vv)
        tris.extend(tuple(base+int(j) for j in t) for t in st)
    body_tree = BVHTree.FromPolygons(verts,tris,all_triangles=True)
    walk = json.loads((ROOT/'reports/collision_walkable.json').read_text())
    r = walk['ramps'][0]; x=sum(r['x'])/2; y0,y1=r['y']; z1=r['z'][1]
    route=[(x,y0-42,0)]
    route.extend((x,y0+(y1-y0)*i/100,z1*i/100) for i in range(101))
    route.extend((x,y1+(238-y1)*i/10,z1) for i in range(1,11))
    route.extend((x*(1-i/30),238,z1) for i in range(1,31))
    route.extend((0,238+(160-238)*i/20,z1) for i in range(1,21))
    floor_errors=[]; blocks=[]
    for k,p in enumerate(route[1:]):
        hits=[floor_tree.ray_cast(Vector((p[0]+dx,p[1]+dy,p[2]+20)),Vector((0,0,-1)),40)
              for dx,dy in ((0,0),(.02,0),(-.02,0),(0,.02),(0,-.02))]
        hits=[hit for hit in hits if hit[0] is not None]
        assert hits, ('No floor',k,p)
        error=min(abs(hit[0].z-p[2]) for hit in hits); floor_errors.append(error)
        assert error<.06, ('Floor discontinuity',k,p,error)
        for h in (18,25,64,112,128):
            for j in range(16):
                a=j*math.tau/16; direction=Vector((math.cos(a),math.sin(a),0))
                hit=body_tree.ray_cast(Vector((p[0],p[1],p[2]+h)),direction,18.0)
                if hit[0] is not None: blocks.append({'sample':k,'pos':p,'height':h,'hit':list(hit[0])})
    assert not blocks, ('Body blocked on route',blocks[:10])
    p=Plugin(str(ROOT/'mod/AstraAsedio.esp'))
    nv=next(dict(p.subrecords(p.datos(o)))['NVNM'] for t,o,n,d in p.recorrer() if t=='NAVM')
    vc=struct.unpack_from('<I',nv,16)[0]
    vs=[struct.unpack_from('<3f',nv,20+12*i) for i in range(vc)]
    off=20+12*vc; tc=struct.unpack_from('<I',nv,off)[0]
    ts=[struct.unpack_from('<3H3hHH',nv,off+4+16*i) for i in range(tc)]
    def contains(foot,t):
        a,b,c=[vs[j] for j in t[:3]]
        dx=foot[0]-a[0];dy=foot[1]-a[1]
        den=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        u=(dx*(c[1]-a[1])-dy*(c[0]-a[0]))/den
        v=((b[0]-a[0])*dy-(b[1]-a[1])*dx)/den
        z=a[2]+u*(b[2]-a[2])+v*(c[2]-a[2])
        return min(u,v,1-u-v)>=-.0001 and abs(z-foot[2]-2)<.05
    missed=[(k,p) for k,p in enumerate(route) if not any(contains(p,t) for t in ts)]
    assert not missed, ('NAVM misses route',missed[:10])
    # All NAVM triangles: torso/head at vertices, edge midpoints and centroids against
    # final reimported collision; stair feet may step over a 16 u ledge.
    nav_hits=[]
    for i,t in enumerate(ts):
        ps=[Vector(vs[j]) for j in t[:3]]
        samples=ps+[(ps[j]+ps[(j+1)%3])/2 for j in range(3)]+[sum(ps,Vector())/3]
        for q in samples:
            for h in (18,64,112,126):
                for direction in (Vector((1,0,0)),Vector((-1,0,0)),Vector((0,1,0)),Vector((0,-1,0))):
                    hit=floor_tree.ray_cast(q+Vector((0,0,h)),direction,17.95)
                    if hit[0] is not None: nav_hits.append((i,list(q),h,list(hit[0])))
    assert not nav_hits, ('NAVM body intersects actual Havok',nav_hits[:8])
    # The world keeps exactly the same rigid transform; rotation/translation preserve
    # these physical clearances. Ground datum differs from leveled LAND by <1 unit.
    world=cfg['tower_v11']['mundo']; assert abs(world['z']-round(world['z']/8)*8)<1.0
    report={'ok':True,'route_samples':len(route),'floor_error_max_units':max(floor_errors),
            'body_blocking_hits':len(blocks),'navmesh_route_uncovered':len(missed),
            'navmesh_triangle_body_hits':len(nav_hits),'actor_height_units':128,'actor_radius_units':18,
            'navmesh_triangles_checked':tc,'world_route_same_rigid_transform':True,
            'world_ground_datum_delta_units':world['z']-round(world['z']/8)*8,
            'torre_sha256':hashlib.sha256((ROOT/'mod/meshes/AstraAsedio/torre.nif').read_bytes()).hexdigest(),
            'esp_sha256':hashlib.sha256(p.d).hexdigest(),'game_tested':False}
    (ROOT/'reports/route_v12.json').write_text(json.dumps(report,indent=2))
    print('V12_ROUTE_OK',len(route),'samples',tc,'nav triangles','max floor error',max(floor_errors))

if __name__=='__main__':main()
