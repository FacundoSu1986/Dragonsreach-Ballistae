"""Find open vanilla geometry near the gate before selecting a placement."""
import sys,json,math
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
import v11_layout as L
from select_whiterun_site_v13 import load_terrain,height
import tower_v12_geometry as G

def main():
    cfg=L.load_cfg();cells,land=load_terrain();trees=[]
    for r in json.loads((ROOT/'reports/gate_models_v13.json').read_text()):
        model=r['donor'].get('model','');low=model.lower()
        if not low.startswith(('architecture\\','landscape\\rocks\\','landscape\\roads\\')):continue
        if r['donor']['type']not in ('STAT','DOOR'):continue
        path=Path(cfg['extracted'])/'meshes'/model
        if not path.exists():continue
        v,t=L.nif_triangles(path)
        m=L.transform_matrix(r['data'][:3],[math.degrees(a) for a in r['data'][3:]],r.get('scale',1),*L.engine_convention())
        v=v@(np.array(m['r'])*m['s']).T+np.array(m['t'])
        trees.append((r['id'],BVHTree.FromPolygons([Vector(p) for p in v],t.tolist(),all_triangles=True)))
    v,t=L.nif_triangles(ROOT/'mod/meshes/AstraAsedio/torre.nif');m=L.transform_matrix((0,0,0),(0,0,45),1,*L.engine_convention())
    v=v@np.array(m['r']).T;site=[]
    for x in range(16900,18801,100):
        for y in range(-9600,-5599,100):
            grid=(math.floor(x/4096),math.floor(y/4096))
            # Keep the whole support/decoration footprint in one cell.
            if min(x%4096,4096-x%4096,y%4096,4096-y%4096)<510:continue
            feet=[L.apply(m,(sx,G.SY0,0)) for sx in (G.SX0,G.SX1)]
            z=max(height(land,x+px,y+py) for px,py,_ in feet)-1
            vv=v+np.array((x,y,z));tree=BVHTree.FromPolygons([Vector(p) for p in vv],t.tolist(),all_triangles=True)
            overlaps=[fid for fid,bvh in trees if tree.overlap(bvh)]
            if overlaps:continue
            ground=[height(land,x+dx,y+dy)-z for dx in (-380,0,380) for dy in (-380,0,380)]
            if max(ground)>90:continue
            distance=math.hypot(x-19312,y+7424)
            site.append({'x':x,'y':y,'z':z,'distance':distance,'span':max(ground)-min(ground),'max_ground':max(ground)})
    site.sort(key=lambda s:s['distance']+.1*s['span'])
    (ROOT/'reports/city_open_sites_v13.json').write_text(json.dumps(site,indent=2))
    print('OPEN_SITES',len(site),json.dumps(site[:12]))
if __name__=='__main__':main()
