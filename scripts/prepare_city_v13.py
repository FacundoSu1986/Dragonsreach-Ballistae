"""Seal a placement off the approach road and fit the own pilings to vanilla heights."""
import json,sys,math
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
import v11_layout as L
import tower_v12_geometry as G
from select_whiterun_site_v13 import load_terrain,height

def main():
    cells,lands=load_terrain();x,y,angle=18400.0,-6300.0,45.0
    m=L.transform_matrix((x,y,0),(0,0,angle),1,*L.engine_convention())
    feet=[L.apply(m,(sx,G.SY0,0)) for sx in (G.SX0,G.SX1)]
    datum=max(height(lands,wx,wy) for wx,wy,_ in feet)-1.0
    grid=(math.floor(x/4096),math.floor(y/4096));cell=lands[grid][0]
    site={'x':x,'y':y,'z':datum,'rot_z_deg':angle,'cell':f'{cell:08X}','grid':list(grid),
          'world':'0000003C','guard_local':[73.5,132.0,140],'gun_local':[0,0,151.55],
          'forward_world':[-math.sqrt(.5),-math.sqrt(.5),0],
          'heightmaps':{f'{gx},{gy}':v[3] for (gx,gy),v in lands.items() if (gx,gy)==grid},
          'chain':cells[cell][3],'game_tested':False,'LAND_edits':0,'NAVM_edits':0,'vanilla_refs_edited':0,
          'gate_reference':'0001B1F1','gate_distance_units':math.hypot(x-19312,y+7424),
          'notes':'Puesto de madera al lado norte del acceso exterior, orientado hacia el camino/llanura. Pilotes ajustados al LAND vanilla; guardia aparece en el puesto, sin ruta nueva.'}
    cfg=L.load_cfg();cfg['city_site']=site
    # Pillar feet may seat on a visible vanilla rock instead of cutting through it
    # down to the underlying LAND. Only the own pillar endpoints change.
    rocks=[]
    for r in json.loads((ROOT/'reports/gate_models_v13.json').read_text()):
        model=r['donor'].get('model','')
        if not model.lower().startswith('landscape\\rocks\\'):continue
        if math.hypot(r['data'][0]-x,r['data'][1]-y)>900:continue
        v,t=L.nif_triangles(Path(cfg['extracted'])/'meshes'/model)
        rm=L.transform_matrix(r['data'][:3],[math.degrees(a) for a in r['data'][3:]],r.get('scale',1),*L.engine_convention())
        vv=v@(np.array(rm['r'])*rm['s']).T+np.array(rm['t']);rocks.append((r['id'],vv[t]))
    def rock_top(wx,wy):
        top=-math.inf
        for fid,tris in rocks:
            a,b,c=tris[:,0],tris[:,1],tris[:,2];den=(b[:,0]-a[:,0])*(c[:,1]-a[:,1])-(b[:,1]-a[:,1])*(c[:,0]-a[:,0])
            ok=np.abs(den)>1e-8;safe=np.where(ok,den,1)
            u=((wx-a[:,0])*(c[:,1]-a[:,1])-(wy-a[:,1])*(c[:,0]-a[:,0]))/safe
            v=((b[:,0]-a[:,0])*(wy-a[:,1])-(b[:,1]-a[:,1])*(wx-a[:,0]))/safe
            mask=ok&(u>=-1e-6)&(v>=-1e-6)&(u+v<=1+1e-6)
            if mask.any():top=max(top,float((a[:,2]+u*(b[:,2]-a[:,2])+v*(c[:,2]-a[:,2]))[mask].max()))
        return top
    feet_xy=[(sx,sy) for sx in cfg['tower_v11']['platform']['grid'] for sy in cfg['tower_v11']['platform']['grid']]
    feet_xy += [(sx,G.SY0+t*(G.SY1-G.SY0)) for sx in G.STRINGER_X for t in (.45,.75)]
    overrides={}
    for sx,sy in feet_xy:
        wx,wy,_=L.apply(m,(sx,sy,0));stone=max(rock_top(wx+dx,wy+dy) for dx in (-9,0,9) for dy in (-9,0,9))
        ground=height(lands,wx,wy)
        if math.isfinite(stone) and stone>ground:
            overrides['%.6f,%.6f'%(sx,sy)]=stone-datum-6.0
    site['support_foot_overrides']=overrides
    geometry=G.build(cfg)
    supports=[]
    for box in geometry['boxes']:
        if not box['name'].startswith('Pilote_'):continue
        a,b=box['min'],box['max'];cx=(a[0]+b[0])/2;cy=(a[1]+b[1])/2
        samples=[];stone_samples=[]
        for lx in (a[0],cx,b[0]):
            for ly in (a[1],cy,b[1]):
                wx,wy,_=L.apply(m,(lx,ly,0));samples.append(height(lands,wx,wy)-datum)
                st=rock_top(wx,wy)
                if math.isfinite(st):stone_samples.append(st-datum)
        surface=max(min(samples),max(stone_samples) if stone_samples else -math.inf)
        assert a[2]<=surface, ('Floating support',box,surface)
        assert b[2]>=max(samples)+10, ('Buried support top',box,max(samples))
        supports.append({'name':box['name'],'bottom':a[2],'top':b[2],'ground_min':min(samples),'ground_max':max(samples),'support_surface_max':surface})
    stair=[]
    for t in range(101):
        ly=G.SY0+(G.SY1-G.SY0)*t/100;z=140*t/100
        for lx in (G.SX0,(G.SX0+G.SX1)/2,G.SX1):
            wx,wy,_=L.apply(m,(lx,ly,0));ground=height(lands,wx,wy)-datum
            stair.append({'t':t,'x':lx,'ramp_z':z,'ground_z':ground})
    site['support_checks']=supports
    site['stair_terrain_max_overlap_units']=max(p['ground_z']-p['ramp_z'] for p in stair)
    assert site['stair_terrain_max_overlap_units']<2,site['stair_terrain_max_overlap_units']
    (ROOT/'reports/city_site_v13.json').write_text(json.dumps(site,ensure_ascii=False,indent=2))
    print('CITY_SITE',site['cell'],site['grid'],datum,'pilings',len(supports),'stair_overlap',site['stair_terrain_max_overlap_units'])
if __name__=='__main__':main()
