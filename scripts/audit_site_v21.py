"""Read the active MO2 profile; retain persistent quest refs and winning navmeshes."""
import sys,struct,json,hashlib,math
from pathlib import Path
import numpy as np
from shapely.geometry import Polygon,Point,box
from shapely.ops import unary_union
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import nivelar_terreno as T

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    base=Path(r'G:\Modding\MO2\SkyrimSE');profile=base/'profiles/Prueba huevo'
    data=Path(r'G:\Modding\Skyrim_Runtime_1.6.1170/Data')
    mods=[s[1:] for s in (profile/'modlist.txt').read_text(encoding='utf-8-sig').splitlines() if s.startswith('+')]
    names=['Skyrim.esm','Update.esm','Dawnguard.esm','HearthFires.esm','Dragonborn.esm']
    names += [s[1:] for s in (profile/'plugins.txt').read_text(encoding='utf-8-sig').splitlines() if s.startswith('*')]
    sources=[];nav={};refs={};land={};models={};quest={}
    region=box(-2500,-23000,13000,-7500)
    for name in names:
        candidates=[base/'overwrite'/name]+[base/'mods'/m/name for m in mods]+[data/name]
        path=next((p for p in candidates if p.is_file()),None)
        if not path: raise FileNotFoundError(name)
        p=Plugin(str(path));sources.append({'name':name,'path':str(path),'sha256':sha(path)})
        masters=[v.rstrip(b'\0').decode('cp1252') for k,v in p.subrecords(p.datos(0)) if k=='MAST']+[name]
        def identity(fid):
            index=fid>>24
            assert index<len(masters),(name,hex(fid),masters)
            return masters[index]+':%06X'%(fid&0xffffff)
        stack=[]
        for typ,o,n,depth in p.recorrer():
            if typ=='GRUP':stack[depth:]=[struct.unpack_from('<Ii',p.d,o+8)];continue
            if typ not in ('NAVM','REFR','ACHR','LAND','CELL','STAT','TREE','FLOR','ACTI','FURN','NPC_','IDLM','QUST','PACK'):continue
            key=identity(p.form_id(o));ss=p.subrecords(p.datos(o));fields=dict(ss)
            flags=struct.unpack_from('<I',p.d,o+8)[0]
            ed=fields.get('EDID',b'').rstrip(b'\0').decode('cp1252')
            if typ in ('STAT','TREE','FLOR','ACTI','FURN','NPC_','IDLM'):
                models[key]={'edid':ed,'type':typ,'model':fields.get('MODL',b'').rstrip(b'\0').decode('cp1252')};continue
            if typ in ('QUST','PACK'):
                if 'MQ104' in ed.upper():quest[key]={'edid':ed,'type':typ,'source':name,'fields':[[k,v.hex()] for k,v in ss]}
                continue
            world=next((f for f,t in stack[:depth] if t==1),None)
            if world is None or identity(world)!='Skyrim.esm:00003C':continue
            cell=next((f for f,t in reversed(stack[:depth]) if t==6),None)
            if typ=='NAVM':
                if flags&0x20:nav.pop(key,None);continue
                nv=fields['NVNM'];count=struct.unpack_from('<I',nv,16)[0]
                verts=np.array([struct.unpack_from('<3f',nv,20+12*i) for i in range(count)])
                if not len(verts) or not region.intersects(box(*verts[:,:2].min(0),*verts[:,:2].max(0))):continue
                cur=20+12*count;nt=struct.unpack_from('<I',nv,cur)[0];cur+=4
                tris=[struct.unpack_from('<3H3hHH',nv,cur+16*i) for i in range(nt)]
                nav[key]={'source':name,'cell':identity(cell),'vertices':verts.tolist(),'triangles':tris,'sha256':hashlib.sha256(nv).hexdigest()}
            elif typ in ('REFR','ACHR') and 'DATA' in fields:
                pos=struct.unpack('<6f',fields['DATA'])
                if not region.covers(Point(*pos[:2])):continue
                refs[key]={'id':key,'type':typ,'source':name,'base':identity(struct.unpack('<I',fields['NAME'])[0]),'edid':ed,'data':pos,'flags':flags,'cell':identity(cell),'scale':struct.unpack('<f',fields['XSCL'])[0] if 'XSCL' in fields else 1,'fields':{k:v.hex() for k,v in ss if k not in ('DATA','NAME') and len(v)<200}}
            elif typ=='LAND':
                if identity(cell) in land:land[identity(cell)].update({'source':name,'heights':T.decodificar_vhgt(fields['VHGT'])[1]})
            elif typ=='CELL' and 'XCLC' in fields:
                grid=struct.unpack_from('<2i',fields['XCLC'])
                if region.intersects(box(grid[0]*4096,grid[1]*4096,(grid[0]+1)*4096,(grid[1]+1)*4096)):
                    land.setdefault(key,{})['grid']=grid
    for ref in refs.values():ref['definition']=models.get(ref['base'],{})
    polys=[]
    for mesh in nav.values():
        v=np.array(mesh['vertices'])
        for t in mesh['triangles']:
            poly=Polygon(v[list(t[:3]),:2])
            if poly.area>1e-5:polys.append(poly)
    union=unary_union(polys)
    # Package values are recorded beside the map: do not claim arbitrary buffers
    # are the actual dragon footprint. MQ104 combat location has radius 5000.
    center=Point(1614.48,-14313.38)
    markers=[r for r in refs.values() if 'MQ104' in r['edid'].upper() or 'WATCHTOWERPATROL' in r['edid'].upper() or 'DRAGON' in r['definition'].get('edid','').upper()]
    candidates=[]
    for x in range(-2000,12501,125):
        for y in range(-22500,-7999,125):
            pt=Point(x,y);distance=pt.distance(center)
            if not 5700<distance<8500:continue
            clearance=pt.distance(union)
            if clearance<500:continue
            nearest=min(pt.distance(Point(*r['data'][:2])) for r in markers)
            if nearest<1000:continue
            grid=[math.floor(x/4096),math.floor(y/4096)]
            cell=next((k for k,v in land.items() if v.get('grid')==tuple(grid) and 'heights' in v),None)
            if not cell:continue
            candidates.append({'x':x,'y':y,'grid':grid,'cell':cell,'nav_clearance':clearance,'mission_marker_clearance':nearest,'watchtower_distance':distance})
    candidates.sort(key=lambda c:(c['watchtower_distance'],-c['nav_clearance']))
    result={'sources':sources,'profile':str(profile),'navmeshes':nav,'refs':list(refs.values()),'land':land,'quest':quest,'candidates':candidates,'read_only_game_files':True,'game_tested':False}
    (ROOT/'reports/site_audit_v21.json').write_text(json.dumps(result,indent=2))
    (ROOT/'reports/nav_union_v21.wkt').write_text(union.wkt)
    print('AUDIT',len(nav),'navmeshes',len(refs),'refs',len(candidates),'candidates')
    for c in candidates[:12]:print('CANDIDATE',c)

if __name__=='__main__':main()
