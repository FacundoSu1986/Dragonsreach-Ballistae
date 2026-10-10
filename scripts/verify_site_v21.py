"""Whole-site navigation/landing bounds; all results explicitly remain proxies."""
import json,sys,math,hashlib,struct
from pathlib import Path
import numpy as np
from shapely.geometry import Polygon
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
import v11_layout as L
import patch_plugin_v12 as P
from parser_esm import Plugin
from build_modular_v13 import subs
from nav_clearance_v21 import check

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def box_triangles(bounds,m):
    a,b=bounds[:3],bounds[3:]
    v=np.array([L.apply(m,(x,y,z)) for x in (a[0],b[0]) for y in (a[1],b[1]) for z in (a[2],b[2])])
    faces=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]
    return np.array([v[list(t)] for f in faces for t in ((f[0],f[1],f[2]),(f[0],f[2],f[3]))])

def main():
    ctx=json.loads((ROOT/'reports/site_audit_v21.json').read_text())
    fit=json.loads((ROOT/'reports/atalaya_context_v21.json').read_text())
    s=fit['site'];m=L.transform_matrix((s['x'],s['y'],s['z']),(0,0,s['rot_z_deg']),1,*L.engine_convention())
    a=np.load(ROOT/'reports/atalaya_written_v21.npz')
    nav=np.concatenate([np.array(mesh['vertices'])[np.array(mesh['triangles'])[:,:3]] for mesh in ctx['navmeshes'].values()])
    c=a['C'][a['CT']]@np.array(m['r']).T+np.array(m['t'])
    tower_hits=check(c,nav,radius=24,height=144)
    core=P.record_map(Plugin(str(ROOT/'mod/AstraAsedio.esp')))
    records=P.record_map(Plugin(str(ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp')))
    own_hull=Polygon((a['V']@np.array(m['r']).T+np.array(m['t']))[:,:2]).convex_hull
    other=[]
    for fid,raw in records.items():
        if raw[:4]!=b'REFR' or fid==0x04000A01:continue
        f=subs(raw);base=struct.unpack('<I',f['NAME'])[0];pos=struct.unpack('<6f',f['DATA'])
        rm=L.transform_matrix(pos[:3],[math.degrees(v) for v in pos[3:]],1,*L.engine_convention())
        bound=struct.unpack('<6h',subs(core[base])['OBND'])
        triangles=box_triangles(bound,rm)
        hits=check(triangles,nav,radius=24,height=144)
        other.append({'form':f'{fid:08X}','conservative_bound_obstructions':len(hits)})
        own_hull=own_hull.union(Polygon(triangles.reshape(-1,3)[:,:2]).convex_hull).convex_hull
    # Read actual winning base-object bounds rather than a guessed point radius.
    master=Plugin(r'G:\Modding\Skyrim_Runtime_1.6.1170\Data\Skyrim.esm');crash_bounds=None
    for typ,o,n,d in master.recorrer():
        if typ!='STAT':continue
        f=dict(master.subrecords(master.datos(o)))
        if f.get('EDID')==b'DragonMarkerCrashStrip\0':crash_bounds=struct.unpack('<6h',f['OBND']);break
    assert crash_bounds
    landing=[]
    for ref in ctx['refs']:
        if ref['definition'].get('edid')!='DragonMarkerCrashStrip':continue
        rm=L.transform_matrix(ref['data'][:3],[math.degrees(v) for v in ref['data'][3:]],ref['scale'],*L.engine_convention())
        strip=Polygon(box_triangles(crash_bounds,rm).reshape(-1,3)[:,:2]).convex_hull
        landing.append({'reference':ref['id'],'edid':ref['edid'],'editor_bound_separation':own_hull.distance(strip),'intersects_256_unit_buffer':own_hull.intersects(strip.buffer(256))})
    success=not tower_hits and not any(o['conservative_bound_obstructions'] for o in other) and not any(l['intersects_256_unit_buffer'] for l in landing)
    inputs=['config.json','scripts/nav_clearance_v21.py','scripts/verify_site_v21.py','reports/site_audit_v21.json','reports/atalaya_written_v21.npz','reports/atalaya_context_v21.json','mod/AstraAsedio.esp','addons/Atalaya/AstraAsedio_Atalaya.esp','addons/Atalaya/meshes/AstraAsedio/torre_atalaya_v21.nif']
    result={'success':success,'site':{k:v for k,v in s.items() if k!='heightmaps'},'navigation_triangles':len(nav),'radius':24,'height':144,'tower_obstructions':len(tower_hits),'samples':tower_hits[:20],'other_owned_refs':other,'landing_strip_bounds':landing,'watchtower_center_distance':math.dist((s['x'],s['y']),(1614.48,-14313.38)),'inputs_sha256':{n:sha(ROOT/n) for n in inputs},'game_tested':False,'scope':'Actual tower Havok, conservative OBND for other owned refs, and known crash-strip editor bounds; continuous NPC-space proxy. No engine AI, dynamic dragon body, quest playthrough, save migration, or other load orders.'}
    (ROOT/'reports/site_verified_v21.json').write_text(json.dumps(result,indent=2))
    print('SITE_CHECK',success,'tower',len(tower_hits),'other',sum(o['conservative_bound_obstructions'] for o in other),'landing',[round(l['editor_bound_separation']) for l in landing])
    assert success,result

if __name__=='__main__':main()
