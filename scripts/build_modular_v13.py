"""Separate core assets from exterior placements; stable master-local identities.

Whiterun adds only owned references and one owned actor base. CELL/WRLD are
containers copied from the winning vanilla master. No terrain/navmesh/object edits.
"""
import json,struct,math,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import escritor_plugin as W
import colocar_escudos as C
import patch_plugin_v12 as P
import build_plugin as B
import mundo_v11 as M

NEW={'proj':0x03000B00,'ammo':0x03000B01,'acti':0x03000B02,'tower':0x03000B03}
CITY={'npc':0x04000B00,'gun':0x04000B10,'guard':0x04000B11,'marker':0x04000B12,'tower':0x04000B13}

def subs(raw):return dict(Plugin.subrecords(raw[24:]))
def add_group(groups,label,record):
    key=struct.unpack('<I',label.encode())[0]
    for i,g in enumerate(groups):
        if C.etiqueta(g)==(key,0):groups[i]=C.rearmar(g,[r for o,n,r in C.hijos(g)]+[record]);return
    groups.append(W.grupo(label,[record]))

def save_plugin(path,groups,masters,nextid):
    body=b''.join(groups);header=W.tes4(masters,C.bloques_totales(body,0),nextid,'Astra',False,'QA v13: tiro bajo y colocaciones modulares')
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(header+body)
    p=Plugin(str(path));items=list(p.recorrer());ids=[p.form_id(o) for t,o,n,d in items if t not in ('GRUP','TES4')]
    assert len(ids)==len(set(ids)),('Duplicate FormID',path)
    assert struct.unpack_from('<I',subs(p.d[:p.inicio_datos])['HEDR'],4)[0]==len(items)-1
    return {'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,'records':len(ids),'masters':masters}

def clone(raw,fid,updates,drop=()):
    return W.record(raw[:4],fid,[W.sub(k,updates.get(k,v)) for k,v in Plugin.subrecords(raw[24:]) if k not in drop],struct.unpack_from('<I',raw,8)[0])

def vanilla_records(wanted):
    result={};cfg=json.loads((ROOT/'config.json').read_text())
    for master in B.MASTERS:
        p=Plugin(str(Path(cfg['runtime'])/'Data'/master))
        for t,o,n,d in p.recorrer():
            if t=='GRUP' or p.form_id(o) not in wanted:continue
            # Re-serialize decompressed donors; preserve all repeated subrecords.
            fid=p.form_id(o);flags=struct.unpack_from('<I',p.d,o+8)[0]&~0x40000
            raw=W.record(t,fid,[W.sub(k,v) for k,v in Plugin.subrecords(p.datos(o))],flags)
            result[fid]=raw
    assert result.keys()==wanted,('Missing vanilla records',wanted-result.keys())
    return result

def ref(fid,base,pos,rot,edid,kind='REFR',persistent=False,vmad=None):
    ss=[W.sub('EDID',W.zstr(edid))]
    if vmad:ss.append(W.sub('VMAD',vmad))
    ss.extend([W.sub('NAME',struct.pack('<I',base)),W.sub('DATA',struct.pack('<6f',*pos,*(math.radians(v) for v in rot)))])
    return W.record(kind,fid,ss,0x400 if persistent else 0)

def main():
    P.main()  # Rebuild allowed geometry edits from immutable v11, never an in-place cumulative patch.
    cfg=json.loads((ROOT/'config.json').read_text());path=ROOT/'mod/AstraAsedio.esp';p=Plugin(str(path));r=P.record_map(p)
    groups=[];world=None
    off=p.inicio_datos
    while off<len(p.d):
        size=struct.unpack_from('<I',p.d,off+4)[0];g=p.d[off:off+size]
        if C.etiqueta(g)==(struct.unpack('<I',b'WRLD')[0],0):world=g
        else:groups.append(g)
        off+=size
    assert world is not None
    vm=B.read_vmad(subs(r[B.IDS['ballesta']])['VMAD'])['scripts'][0]
    props={k:(v['type'],v['value']['form_id'] if v['type']==1 else v['value']) for k,v in vm['properties'].items()}
    props['PitchMin']=(4,-20.0)
    change=P.modify_subs(r[B.IDS['ballesta']],{'VMAD':B.vmad('AstraAsedioActi',props)})
    groups=[P.transform_groups(g,{B.IDS['ballesta']:change},set(),{}) for g in groups]
    proj=bytearray(subs(r[B.IDS['projectile']])['DATA'])
    struct.pack_into('<H',proj,0,struct.unpack_from('<H',proj)[0]&~2)
    struct.pack_into('<I',proj,36,0)
    add_group(groups,'PROJ',clone(r[B.IDS['projectile']],NEW['proj'],{'EDID':W.zstr('AstraGuardProjectile'),'FULL':W.zstr('Virote del artillero Astra'),'DATA':bytes(proj)}))
    ammo=bytearray(subs(r[B.IDS['ammo']])['DATA']);struct.pack_into('<I',ammo,0,NEW['proj'])
    add_group(groups,'AMMO',clone(r[B.IDS['ammo']],NEW['ammo'],{'EDID':W.zstr('AstraGuardAmmo'),'FULL':W.zstr('Virote del artillero Astra'),'DATA':bytes(ammo)}))
    add_group(groups,'ACTI',clone(r[B.IDS['ballesta']],NEW['acti'],{'EDID':W.zstr('AstraGuardBallista'),'FULL':W.zstr('Ballesta del artillero Astra')},('VMAD',)))
    box=json.loads((ROOT/'reports/assets.json').read_text())['torre_whiterun']['bbox_units']
    obnd=[math.floor(x) for x in box['min']]+[math.ceil(x) for x in box['max']]
    add_group(groups,'STAT',clone(r[B.IDS['tower']],NEW['tower'],{'EDID':W.zstr('AstraTowerWhiterun'),'OBND':struct.pack('<6h',*obnd),'MODL':W.zstr('AstraAsedio\\torre_whiterun.nif')}))
    core=save_plugin(path,groups,B.MASTERS,0xB04)
    B.validate_plugin(str(path))
    # Former exterior is optional. Only new owned REFR headers change namespace;
    # NAME/VMAD dependencies continue to resolve to the core master at index03.
    def legacy(g):
        children=[]
        for o,n,raw in C.hijos(g):
            if raw[:4]==b'GRUP':raw=legacy(raw)
            else:
                fid=struct.unpack_from('<I',raw,12)[0]
                if fid>>24==3:raw=raw[:12]+struct.pack('<I',(fid&0xFFFFFF)|0x04000000)+raw[16:]
            children.append(raw)
        return C.rearmar(g,children)
    masters=B.MASTERS+['AstraAsedio.esp']
    old=save_plugin(ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp',[legacy(world)],masters,0xA4F)
    site=json.loads((ROOT/'reports/city_site_v13.json').read_text());cell=int(site['cell'],16)
    vanilla=vanilla_records({0x3C,cell,0xD74,0x001000EC})
    guard_ss=subs(vanilla[0x001000EC]);acbs=bytearray(guard_ss['ACBS'])
    # Do not inherit AI packages or scripts from the template; own guard alone is stationed.
    struct.pack_into('<H',acbs,18,struct.unpack_from('<H',acbs,18)[0]&~(0x20|0x200))
    npc=clone(vanilla[0x001000EC],CITY['npc'],{'EDID':W.zstr('AstraWhiterunArtillero'),'FULL':W.zstr('Artillero de Carrera Blanca'),'ACBS':bytes(acbs)},('PKID','VMAD'))
    citygroups=[W.grupo('NPC_',[npc])]
    posrot=lambda pos:M.llevar({'pos':pos,'rot_deg':[0,0,0],'scale':1},site)
    gunpos,rot=posrot(site['gun_local']);guardpos,_=posrot(site['guard_local']);markerpos=guardpos
    guardprops={'Artillero':(1,CITY['guard']),'Puesto':(1,CITY['marker']),
                'Launcher':(1,B.IDS['launcher']),'ShotAmmo':(1,NEW['ammo']),'ShotSound':(1,B.IDS['shot_sound']),
                'PitchMin':(4,-20.),'PitchMax':(4,45.),'ProjectileSpeed':(4,5400.),'ProjectileGravity':(4,240.345)}
    gun=ref(CITY['gun'],NEW['acti'],gunpos,rot,'AstraWhiterunBallesta',persistent=True,vmad=B.vmad('AstraAsedioGuard',guardprops))
    actor=ref(CITY['guard'],CITY['npc'],guardpos,(0,0,225),'AstraWhiterunArtilleroRef','ACHR',True)
    marker=ref(CITY['marker'],0x34,markerpos,(0,0,225),'AstraWhiterunPuesto',persistent=True)
    towerpos,trot=posrot([0,0,0]);temporary=[ref(CITY['tower'],NEW['tower'],towerpos,trot,'AstraWhiterunTorre')]
    for i,item in enumerate(cfg['tower_v11']['escudos']['items']):
        pp,rr=M.llevar({'pos':item['pos'],'rot_deg':item['rot_deg'],'scale':1},site)
        temporary.append(ref(0x04000B20+i,C.STAT_ESCUDO,pp,rr,'AstraWhiterunEscudo'+item['nombre']))
    persistent=W.grupo(struct.pack('<I',0xD74),[W.grupo(struct.pack('<I',0xD74),[gun,actor,marker],8)],6)
    cellchildren=W.grupo(struct.pack('<I',cell),[W.grupo(struct.pack('<I',cell),temporary,9)],6)
    chain=site['chain'];label4=next(label for label,typ in chain if typ==4);label5=next(label for label,typ in chain if typ==5)
    ext=W.grupo(struct.pack('<I',label4),[W.grupo(struct.pack('<I',label5),[vanilla[cell],cellchildren],5)],4)
    # The output ESP is not localized. FULL in Skyrim.esm is a STRINGS ID;
    # OFST/RNAM here are master-sized world tables, not transferable cell data.
    worldrecord=clone(vanilla[0x3C],0x3C,{'FULL':W.zstr('Skyrim')},('OFST','RNAM'))
    worldgroup=W.grupo('WRLD',[worldrecord,W.grupo(struct.pack('<I',0x3C),[vanilla[0xD74],persistent,ext],1)])
    citygroups.append(worldgroup)
    city=save_plugin(ROOT/'addons/Whiterun/AstraAsedio_Whiterun.esp',citygroups,masters,0xB2C)
    manifests={'core':core,'whiterun':city,'atalaya':old,'site':{k:v for k,v in site.items() if k!='heightmaps'},
               'forms_core':{k:f'{v:08X}' for k,v in NEW.items()},'forms_city':{k:f'{v:08X}' for k,v in CITY.items()},
               'compatibility':{'core_world_overrides':0,'city_cells':['00000D74',site['cell']],
                                 'city_LAND':0,'city_NAVM':0,'city_vanilla_REF_overrides':0,
                                 'atalaya_keeps_v11_terrain_edits':True,'patches_for_other_mods':'deferred','game_tested':False}}
    (ROOT/'reports/modular_v13.json').write_text(json.dumps(manifests,ensure_ascii=False,indent=2))
    print('MODULAR_BUILT',core['records'],city['records'],old['records'])
if __name__=='__main__':main()
