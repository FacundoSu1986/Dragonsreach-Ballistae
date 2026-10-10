"""Read masters only; seal terrain, nearby objects and NAVM at the new site."""
import sys,json,struct,math,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import nivelar_terreno as T
import v11_layout as L
import numpy as np

def main():
    cfg=L.load_cfg(); masters=['Skyrim.esm','Update.esm','Dawnguard.esm']
    site={'x':4665.54,'y':-14922.81,'z':-5217.81,'rot_z_deg':187.63,'cell':'0000963D','grid':[1,-4]}
    refs={};models={};nav={};land={};sources={}
    for master in masters:
        p=Plugin(str(Path(cfg['runtime'])/'Data'/master));stack=[]
        sources[master]=hashlib.sha256(p.d).hexdigest()
        for typ,o,n,depth in p.recorrer():
            if typ=='GRUP':stack[depth:]=[struct.unpack_from('<Ii',p.d,o+8)];continue
            if typ not in ('STAT','TREE','FLOR','ACTI','REFR','NAVM','LAND'):continue
            fid=p.form_id(o);world=next((f for f,t in stack[:depth] if t==1),0)
            cell=next((f for f,t in reversed(stack[:depth]) if t==6),0)
            if typ in ('REFR','NAVM','LAND') and (world!=0x3c or cell!=0x963d):continue
            ss=dict(p.subrecords(p.datos(o)));flags=struct.unpack_from('<I',p.d,o+8)[0]
            if typ in ('STAT','TREE','FLOR','ACTI'):
                if 'MODL' in ss:models[fid]={'model':L.zstr(ss['MODL']),'edid':L.zstr(ss.get('EDID',b''))}
            elif typ=='REFR' and 'DATA' in ss:
                pos=struct.unpack('<6f',ss['DATA'])
                if math.dist(pos[:2],(site['x'],site['y']))<1500:
                    refs[fid]={'id':f'{fid:08X}','base':struct.unpack('<I',ss['NAME'])[0],'data':pos,'scale':struct.unpack('<f',ss['XSCL'])[0] if 'XSCL' in ss else 1,'flags':flags}
            elif typ=='LAND':land={'id':f'{fid:08X}','master':master,'heights':T.decodificar_vhgt(ss['VHGT'])[1]}
            elif typ=='NAVM':
                if flags&0x20:nav.pop(fid,None);continue
                nv=ss['NVNM'];count=struct.unpack_from('<I',nv,16)[0]
                verts=[struct.unpack_from('<3f',nv,20+12*i) for i in range(count)]
                cur=20+12*count;nt=struct.unpack_from('<I',nv,cur)[0];cur+=4
                tris=[struct.unpack_from('<3H3hHH',nv,cur+16*i) for i in range(nt)]
                nav[fid]={'id':f'{fid:08X}','cell':'0000963D','vertices':verts,'triangles':[t[:3]+t[6:] for t in tris],'nvnm_sha256':hashlib.sha256(nv).hexdigest(),'master':master}
    for r in refs.values():r['donor']=models.get(r['base'],{})
    site['heightmaps']={'1,-4':land['heights']}
    # Highest projected visible rock surface. Only read geometry, never export it.
    rocks=[]
    for r in refs.values():
        model=r['donor'].get('model','')
        if not model.lower().startswith('landscape\\rocks\\') or r['flags']&(0x20|0x800):continue
        v,t=L.nif_triangles(Path(cfg['extracted'])/'meshes'/model)
        m=L.transform_matrix(r['data'][:3],[math.degrees(a) for a in r['data'][3:]],r['scale'],*L.engine_convention())
        vv=v@(np.array(m['r'])*m['s']).T+np.array(m['t']);rocks.append((r['id'],vv[t]))
    # Seal relevant triangles as a non-shipping research cache.
    np.savez_compressed(ROOT/'reports/atalaya_rocks_v20.npz',triangles=np.concatenate([t for f,t in rocks]) if rocks else np.empty((0,3,3)))
    result={'site':site,'land':{k:v for k,v in land.items() if k!='heights'},'refs':list(refs.values()),'navmeshes':list(nav.values()),'sources':sources,'read_only':True}
    (ROOT/'reports/atalaya_context_v20.json').write_text(json.dumps(result,indent=2))
    print('ATALAYA_CONTEXT',len(refs),'refs',len(rocks),'rocks',len(nav),'navmeshes')
if __name__=='__main__':main()
