"""Recreate the sealed site inputs from the recorded MO2 survey and current config."""
import sys,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
import v11_layout as L

def main():
    cfg=L.load_cfg();audit=json.loads((ROOT/'reports/site_audit_v21.json').read_text())
    site=dict(cfg['tower_v11']['mundo'])
    site['heightmaps']={','.join(map(str,v['grid'])):v['heights'] for v in audit['land'].values() if 'heights' in v}
    refs=[];rocks=[]
    for ref in audit['refs']:
        if ref['source'].startswith('Astra') or math.dist(ref['data'][:2],(site['x'],site['y']))>=1400:continue
        r={**{k:ref[k] for k in ['id','data','scale','flags']},'donor':ref['definition']};refs.append(r)
        model=r['donor'].get('model','')
        if r['flags']&(0x20|0x800) or not model.lower().startswith(('landscape\\rocks\\','landscape\\tundra\\')):continue
        v,t=L.nif_triangles(Path(cfg['extracted'])/'meshes'/model)
        m=L.transform_matrix(r['data'][:3],[math.degrees(a) for a in r['data'][3:]],r['scale'],*L.engine_convention())
        rocks.extend((v@np.array(m['r']).T*m['s']+np.array(m['t']))[t])
    ctx={'site':site,'refs':refs,'sources':audit['sources'],'navmeshes':audit['navmeshes'],'read_only':True}
    (ROOT/'reports/atalaya_context_v21.json').write_text(json.dumps(ctx,indent=2))
    np.savez_compressed(ROOT/'reports/atalaya_rocks_v21.npz',triangles=np.array(rocks).reshape(-1,3,3))
    print('SITE_INPUTS',len(refs),'refs',len(rocks),'visual rock triangles')

if __name__=='__main__':main()
