"""Choose an exterior emplacement from the unedited vanilla LAND, with a placement receipt."""
import sys,json,struct,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import nivelar_terreno as T
import v11_layout as L

def load_terrain():
    cfg=L.load_cfg(); cells={}; lands={}; current=None
    for filename in ('Skyrim.esm','Update.esm','Dawnguard.esm'):
        p=Plugin(str(Path(cfg['runtime'])/'Data'/filename));stack=[]
        for typ,o,n,depth in p.recorrer():
            if typ=='GRUP':
                stack[depth:]=[struct.unpack_from('<Ii',p.d,o+8)]
                continue
            if typ not in ('CELL','LAND'):continue
            world=next((label for label,gt in stack[:depth] if gt==1),0)
            ss=dict(p.subrecords(p.datos(o)));fid=p.form_id(o)
            if typ=='CELL':
                current=fid
                if world==0x3C and 'XCLC'in ss:
                    grid=struct.unpack('<2i',ss['XCLC'][:8]);cells[fid]=(grid,filename,ss,stack[:depth])
            elif current in cells and 'VHGT'in ss:
                lands[cells[current][0]]=(current,fid,filename,T.decodificar_vhgt(ss['VHGT'])[1])
    return cells,lands

def height(lands,x,y):
    gx,gy=math.floor(x/4096),math.floor(y/4096)
    data=lands[(gx,gy)][3]; fx=(x-gx*4096)/128;fy=(y-gy*4096)/128
    ix,iy=int(fx),int(fy);tx,ty=fx-ix,fy-iy
    # Both possible terrain triangle diagonals: average for placement, retained error bound.
    a,b,c,d=data[iy][ix],data[iy][ix+1],data[iy+1][ix],data[iy+1][ix+1]
    z=(1-tx)*(1-ty)*a+tx*(1-ty)*b+(1-tx)*ty*c+tx*ty*d
    return z

def main():
    cells,lands=load_terrain();cfg=L.load_cfg()
    candidates=[]
    for x in range(17100,18401,100):
        for y in range(-6900,-5899,100):
            pts=[height(lands,x+dx,y+dy) for dx in (-380,-250,0,250,380) for dy in (-380,-250,0,250,380)]
            candidates.append({'x':x,'y':y,'span':max(pts)-min(pts),'height':height(lands,x,y),
                               'gate_distance':math.hypot(x-19312,y+7424)})
    candidates.sort(key=lambda c:c['span']+.035*c['gate_distance'])
    report={'candidates':candidates[:30],'terrain_sources':{str(grid):{'cell':f'{v[0]:08X}','land':f'{v[1]:08X}','master':v[2]} for grid,v in lands.items() if 3<=grid[0]<=4 and -2<=grid[1]<=-1}}
    (ROOT/'reports/whiterun_sites_v13.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(candidates[:12],indent=2))
if __name__=='__main__':main()
