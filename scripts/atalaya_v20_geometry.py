"""Own site-specific supports and longer stairs; no terrain/navmesh mutation."""
import json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
import v11_layout as L
import tower_v12_geometry as G
from select_whiterun_site_v13 import height

class Surface:
    def __init__(self):
        self.ctx=json.loads((ROOT/'reports/atalaya_context_v20.json').read_text())
        self.site=self.ctx['site'];self.m=L.transform_matrix((self.site['x'],self.site['y'],self.site['z']),(0,0,self.site['rot_z_deg']),1,*L.engine_convention())
        self.lands={tuple(map(int,k.split(','))):(0,0,'',v) for k,v in self.site['heightmaps'].items()}
        rocks=np.load(ROOT/'reports/atalaya_rocks_v20.npz')['triangles']
        rocks=(rocks-np.array(self.m['t']))@np.array(self.m['r'])
        existing=np.load(ROOT/'reports/atalaya_existing_havok_v20.npz')['triangles']
        receipt=json.loads((ROOT/'reports/atalaya_environment_v20.json').read_text())
        assert all(self.site[k]==v for k,v in receipt['site'].items()),'Stale environment frame'
        self.tris=np.concatenate([rocks,existing])
    def z(self,x,y):
        wx,wy,_=L.apply(self.m,(x,y,0));top=height(self.lands,wx,wy)-self.site['z']
        if len(self.tris):
            a,b,c=self.tris[:,0],self.tris[:,1],self.tris[:,2]
            den=(b[:,0]-a[:,0])*(c[:,1]-a[:,1])-(b[:,1]-a[:,1])*(c[:,0]-a[:,0]);ok=np.abs(den)>1e-8;safe=np.where(ok,den,1)
            u=((x-a[:,0])*(c[:,1]-a[:,1])-(y-a[:,1])*(c[:,0]-a[:,0]))/safe
            v=((b[:,0]-a[:,0])*(y-a[:,1])-(b[:,1]-a[:,1])*(x-a[:,0]))/safe
            mask=ok&(u>=-1e-6)&(v>=-1e-6)&(u+v<=1+1e-6)
            if mask.any():top=max(top,float((a[:,2]+u*(b[:,2]-a[:,2])+v*(c[:,2]-a[:,2]))[mask].max()))
        return top

def build():
    surface=Surface();cfg=L.load_cfg();site=dict(surface.site)
    feet=[(x,y) for x in cfg['tower_v11']['platform']['grid'] for y in cfg['tower_v11']['platform']['grid']]
    feet += [(x,G.SY0+t*(G.SY1-G.SY0)) for x in G.STRINGER_X for t in (.45,.75)]
    site['support_foot_overrides']={'%.6f,%.6f'%(x,y):min(surface.z(x+dx,y+dy) for dx in (-10,0,10) for dy in (-10,0,10))-16 for x,y in feet}
    cfg['city_site']=site
    out=G.build(cfg)
    # Continue the existing straight stair slope to the local terrain. Find the
    # first contact, rather than flattening the LAND or leaving a floating entry.
    def difference(y):
        return max(surface.z(x,y) for x in np.linspace(G.SX0,G.SX1,9))-G.SLOPE*(y-G.SY0)
    upper=G.SY0;lower=upper
    while difference(lower)<1.0:
        lower-=4
        if lower<G.SY0-400:raise ValueError('No safe stair entrance within 400 units')
    for i in range(30):
        mid=(lower+upper)/2
        if difference(mid)>=1:lower=mid
        else:upper=mid
    y0=(lower+upper)/2;z0=G.SLOPE*(y0-G.SY0)
    entry=G.Tower(cfg);rise=-z0;count=math.ceil(rise/G.RISE);tread=(G.SY0-y0)/count
    for i in range(count):
        y=y0+(i+.5)*tread;z=G.SLOPE*(y-G.SY0)
        entry.plank(f'Atalaya_entrada_peldano_{i:02d}',((G.SX0+G.SX1)/2,y,z),(1,0,0),(0,0,1),G.SX1-G.SX0,tread*.97,G.TREAD_T,kind='tread',twist=0)
    for x,tag in zip(G.STRINGER_X,('int','ext')):
        entry.log('Atalaya_entrada_zanca_'+tag,(x,y0,z0-30),(x,G.SY0+8,5-30),10,sides=9,bend=(.002,.004),box=True)
        entry.log('Atalaya_entrada_pasamanos_'+tag,(x,y0,z0+G.HANDRAIL_ABOVE_RAMP),(x,G.SY0+8,5+G.HANDRAIL_ABOVE_RAMP),4.5,sides=7,bend=(.002,.004))
        for k,t in enumerate((.15,.65)):
            y=y0+t*(G.SY0-y0);z=G.SLOPE*(y-G.SY0)
            bottom=surface.z(x,y)-16
            entry.log(f'Atalaya_entrada_pilote_{tag}_{k}',(x,y,bottom),(x,y,z-18),10,sides=9,bend=(.002,.004),box=True)
            entry.log(f'Atalaya_entrada_baranda_{tag}_{k}',(x,y,z-18),(x,y,z+G.HANDRAIL_ABOVE_RAMP),4.5,sides=7,bend=(.002,.004))
    out['parts']+=entry.parts;out['boxes']+=entry.boxes
    out['entry']={'y0':y0,'z0':z0,'y1':G.SY0,'z1':0,'added_steps':count,'rise':rise/count,'tread':tread}
    supports=[]
    for b in out['boxes']:
        if not (b['name'].startswith('Pilote_') or 'entrada_pilote_' in b['name']):continue
        lo,hi=b['min'],b['max'];samples=[surface.z(x,y) for x in np.linspace(lo[0],hi[0],3) for y in np.linspace(lo[1],hi[1],3)]
        assert lo[2]<min(samples),(b['name'],'floating',lo[2],min(samples))
        # Some stair support ends are underground by design at the entrance.
        supports.append({'name':b['name'],'bottom':lo[2],'top':hi[2],'ground_min':min(samples),'ground_max':max(samples),'bottom_below_ground':min(samples)-lo[2]})
    samples=[]
    for y in np.linspace(y0,G.SY1,201):
        z=G.SLOPE*(y-G.SY0)
        for x in np.linspace(G.SX0,G.SX1,9):samples.append(surface.z(x,y)-z)
    assert max(samples)<2,('Stair buried by terrain',max(samples))
    out['site']=site;out['support_checks']=supports;out['stair_ground_max_overlap']=max(samples)
    return out

def probe():
    s=Surface()
    for x,y in [(a,b) for a in (-262,262) for b in (-262,262)]+[(323.4,y) for y in (G.SY0,-100,-200,-300,0,196)]:
        print('SURFACE',x,y,s.z(x,y),'ramp',G.SLOPE*(y-G.SY0))
    for r in s.ctx['refs']:print('NEAR',r['id'],r['donor'],r['data'][:3])
if __name__=='__main__':
    out=build();print('ATALAYA_FIT',out['entry'],'supports',len(out['support_checks']),'stair_overlap',out['stair_ground_max_overlap'])
    (ROOT/'reports/atalaya_geometry_v20.json').write_text(json.dumps({k:v for k,v in out.items() if k in ('entry','site','support_checks','stair_ground_max_overlap')},indent=2))
