"""Read nearby vanilla Havok in the new tower frame; cache is not shipped."""
import sys,json,math,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
import bpy,addon_utils,numpy as np
import v11_layout as L
from probe_towers_v14 import load,capsule_clear
import tower_fit_v14 as F

def main():
    addon_utils.enable('io_scene_nifly',default_set=True)
    cfg=L.load_cfg();ctx=json.loads((ROOT/'reports/atalaya_context_v21.json').read_text());s=ctx['site'];m=L.transform_matrix((s['x'],s['y'],s['z']),(0,0,s['rot_z_deg']),1,*L.engine_convention());rd=np.array(m['r']);origin=np.array(m['t'])
    env=[];meta=[]
    for ref in ctx['refs']:
        model=ref['donor'].get('model','')
        if ref['flags']&(0x20|0x800) or not model.lower().startswith(('landscape\\rocks\\','landscape\\roads\\','landscape\\tundra\\','dungeons\\')):continue
        nif=Path(cfg['extracted'])/'meshes'/model
        rm=L.transform_matrix(ref['data'][:3],[math.degrees(a) for a in ref['data'][3:]],ref['scale'],*L.engine_convention())
        local={'r':(rd.T@np.array(rm['r'])).tolist(),'t':(rd.T@(np.array(rm['t'])-origin)).tolist(),'s':rm['s']}
        objs=load(nif,local);a,b=F.mesh_arrays([o for o in objs if o.type=='MESH' and o.name.startswith('bhk')]);env.extend(a[b])
        item={'reference':ref['id'],'model':model,'sha256':hashlib.sha256(nif.read_bytes()).hexdigest(),'havok_triangles':len(b),'min':a.min(0).tolist() if len(a) else None,'max':a.max(0).tolist() if len(a) else None}
        if len(b):
            bvh=F.bvh_from_triangles(a[b]);item['blocks_initial_entrance']=not capsule_clear(bvh,(323.4,-197.36,-103.96))
        meta.append(item)
        print('ENVIRONMENT',item,flush=True)
    np.savez_compressed(ROOT/'reports/atalaya_existing_havok_v21.npz',triangles=np.array(env).reshape(-1,3,3))
    (ROOT/'reports/atalaya_environment_v21.json').write_text(json.dumps({'site':{k:v for k,v in s.items() if k!='heightmaps'},'inputs':meta,'scope':'Read-only vanilla Havok in the tower local frame; research cache never shipped'},indent=2))
if __name__=='__main__':main()
