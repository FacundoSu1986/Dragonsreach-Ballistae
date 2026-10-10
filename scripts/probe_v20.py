"""Read-only placement and rendering facts for v20 diagnosis."""
import sys,json,struct,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
import nif_nodos, nif_fisica, numpy as np
from parser_esm import Plugin
import patch_plugin_v12 as P

def main():
    result={'meshes':[],'atalaya':[]}
    for name in ('voladizo_este','voladizo_oeste'):
        n=nif_nodos.leer(str(ROOT/f'addons/WhiterunTorres/meshes/AstraAsedio/{name}.nif'))
        shapes=[]
        for i,t,o,m,sh,al,desc,nv,data in nif_fisica._shapes(n):
            p=o+4; ne,=struct.unpack_from('<I',n['datos'],p); p+=4+ne*4+4
            flags,=struct.unpack_from('<I',n['datos'],p); p+=4+12+36+4+4
            bound=struct.unpack_from('<4f',n['datos'],p)
            vv=np.array([struct.unpack_from('<3f',n['datos'],data+k*(desc&15)*4) for k in range(nv)])
            maxrad=float(np.linalg.norm(vv-np.array(bound[:3]),axis=1).max())
            shapes.append({'block':i,'flags':flags,'bound':bound,'vertices':nv,'required_radius':maxrad})
        result['meshes'].append({'name':name,'nodes':n['nodos'],'shapes':shapes,'visual_bounds':nif_fisica.caja_visual(n)})
    p=Plugin(str(ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp'))
    for fid,raw in P.record_map(p).items():
        ss=dict(Plugin.subrecords(raw[24:]));r={'id':f'{fid:08X}','type':raw[:4].decode(),'flags':hex(struct.unpack_from('<I',raw,8)[0])}
        for k in ('EDID','MODL'):
            if k in ss:r[k]=ss[k].rstrip(b'\0').decode('cp1252')
        if raw[:4] in (b'REFR',b'ACHR'):
            r['NAME']=f"{struct.unpack('<I',ss['NAME'])[0]:08X}";r['DATA']=struct.unpack('<6f',ss['DATA'])
        result['atalaya'].append(r)
    (ROOT/'reports/probe_v20.json').write_text(json.dumps(result,indent=2))
    for mesh in result['meshes']:print(mesh['name'],mesh['shapes'])
    for path in (ROOT/'mod/meshes/AstraAsedio/torre.nif',ROOT/'addons/WhiterunTorres/meshes/AstraAsedio/voladizo_este.nif'):
        n=nif_nodos.leer(str(path));typ,o,size=n['bloques'][0];p=o+4;ne=struct.unpack_from('<I',n['datos'],p)[0];p+=4+ne*4+4;flags=struct.unpack_from('<I',n['datos'],p)[0];p+=4+52+4;nc=struct.unpack_from('<I',n['datos'],p)[0];p+=4+4*nc
        print('ROOT_LAYOUT',path.name,typ,size,'flags',hex(flags),'tail',n['datos'][p:o+size].hex())
if __name__=='__main__':main()
