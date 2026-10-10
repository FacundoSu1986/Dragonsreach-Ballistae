"""Read winning vanilla references and NAVM geometry around Facu's two towers."""
import hashlib,json,math,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v13')
sys.path.insert(0,str(ROOT/'scripts/vendor'))
from parser_esm import Plugin
MASTERS=['Skyrim.esm','Update.esm','Dawnguard.esm']
REQUESTS=[{'name':'este','requested':[17801.74,-8324.61,-3615.66],'tower_ref':'000684EC'},
          {'name':'oeste','requested':[15225.56,-8306.52,-4127.66],'tower_ref':'00063FD0'}]

def nav_surface(nav,x,y,max_delta=900):
    hits=[]
    for mesh in nav:
        if mesh.get('deleted'):continue
        v=mesh['vertices']
        for i,t in enumerate(mesh['triangles']):
            a,b,c=[v[k] for k in t[:3]]
            den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
            if abs(den)<1e-8:continue
            u=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(y-c[1]))/den
            w=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(y-c[1]))/den
            if min(u,w,1-u-w)>=-1e-5:
                hits.append({'navmesh':mesh['id'],'triangle':i,'z':u*a[2]+w*b[2]+(1-u-w)*c[2],
                             'triangle_flags':t[3:],'cell':mesh['cell']})
    return hits

def main():
    cfg=json.loads((BASE/'config.json').read_text());refs={};models={};cells={};nav={};sources={}
    for master in MASTERS:
        p=Plugin(str(Path(cfg['runtime'])/'Data'/master))
        names=[v.rstrip(b'\0').decode('cp1252') for k,v in p.subrecords(p.datos(0)) if k=='MAST']+[master]
        def canon(fid):
            if not fid:return 0
            idx=fid>>24
            assert idx<len(names),(master,f'{fid:08X}',names)
            return (MASTERS.index(names[idx])<<24)|(fid&0xffffff)
        stack=[]
        for typ,off,n,depth in p.recorrer():
            if typ=='GRUP':
                label,kind=struct.unpack_from('<Ii',p.d,off+8)
                if kind in (1,6,8,9,10):label=canon(label)
                stack[depth:]=[(label,kind)]
                continue
            if typ not in ('REFR','ACHR','CELL','STAT','ACTI','DOOR','NAVM'):continue
            fid=canon(p.form_id(off));key=f'{fid:08X}';ss=dict(p.subrecords(p.datos(off)))
            flags=struct.unpack_from('<I',p.d,off+8)[0];deleted=bool(flags&0x20)
            if typ=='CELL':
                if fid in (0xd74,0x961b,0x961c):
                    cells[key]={'id':key,'edid':ss.get('EDID',b'').rstrip(b'\0').decode('cp1252'),
                                'grid':list(struct.unpack_from('<2i',ss['XCLC'])) if 'XCLC' in ss else None,
                                'chain':stack[:depth],'source':master}
            elif typ in ('STAT','ACTI','DOOR'):
                models[key]={'type':typ,'edid':ss.get('EDID',b'').rstrip(b'\0').decode('cp1252'),
                             'model':ss.get('MODL',b'').rstrip(b'\0').decode('cp1252'),'source':master}
            elif typ in ('REFR','ACHR'):
                world=next((label for label,kind in stack[:depth] if kind==1),0)
                if world!=0x3c and key not in refs:continue
                if 'DATA' not in ss or len(ss['DATA'])!=24:continue
                data=list(struct.unpack('<6f',ss['DATA']))
                near=any(math.dist(data[:2],q['requested'][:2])<950 for q in REQUESTS)
                if not near and key not in refs:continue
                cell=next((label for label,kind in reversed(stack[:depth]) if kind==6),0)
                refs[key]={'id':key,'type':typ,'cell':f'{cell:08X}','world':f'{world:08X}',
                           'base':f'{canon(struct.unpack("<I",ss["NAME"])[0]):08X}',
                           'edid':ss.get('EDID',b'').rstrip(b'\0').decode('cp1252'),'data':data,
                           'scale':struct.unpack('<f',ss['XSCL'])[0] if 'XSCL' in ss else 1.,
                           'source':master,'deleted':deleted,'flags':flags}
            elif typ=='NAVM':
                cell=next((label for label,kind in reversed(stack[:depth]) if kind==6),0)
                if cell not in (0x961b,0x961c):continue
                if deleted:nav[key]={'id':key,'deleted':True,'cell':f'{cell:08X}'};continue
                nv=ss['NVNM'];version,crc,world,position,count=struct.unpack_from('<5I',nv)
                assert version==12 and canon(world)==0x3c,(key,version,world)
                ygrid,xgrid=struct.unpack_from('<2h',nv,12)
                verts=[list(struct.unpack_from('<3f',nv,20+12*i)) for i in range(count)]
                cursor=20+12*count;tri_count=struct.unpack_from('<I',nv,cursor)[0];cursor+=4
                assert cursor+16*tri_count<=len(nv)
                triangles=[]
                for i in range(tri_count):
                    t=struct.unpack_from('<3H3hHH',nv,cursor+16*i)
                    assert max(t[:3])<count,(key,i,t)
                    triangles.append(list(t[:3]+t[6:]))
                nav[key]={'id':key,'cell':f'{cell:08X}','grid':[xgrid,ygrid],'source':master,'version':version,
                          'nvnm_sha256':hashlib.sha256(nv).hexdigest(),'vertices':verts,'triangles':triangles}
        sources[master]={'bytes':len(p.d),'sha256':hashlib.sha256(p.d).hexdigest()}
    for r in refs.values():r['donor']=models.get(r['base'],{})
    requests=[]
    for q in REQUESTS:
        r=refs[q['tower_ref']]
        requests.append({**q,'tower':r,'requested_nav_surfaces':nav_surface(list(nav.values()),*q['requested'][:2])})
    out={'runtime_read_only':True,'sources':sources,'requests':requests,'cells':cells,
         'refs':list(refs.values()),'navmeshes':list(nav.values()),
         'scope':'Winning vanilla geometry only; NAVM presence is not an engine path test.'}
    (ROOT/'reports/tower_context_v14.json').write_text(json.dumps(out,indent=2))
    for q in requests:print(q['name'],q['tower']['donor']['model'],q['tower']['cell'],q['requested_nav_surfaces'])
    print('TOWER_CONTEXT',len(refs),'refs',len(nav),'NAVM records')
if __name__=='__main__':main()
