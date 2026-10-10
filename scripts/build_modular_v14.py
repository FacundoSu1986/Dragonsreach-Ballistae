"""Patch only core timing VMAD; place two persistent mounted guard stations."""
import json,struct,sys,math,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v13')
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import build_plugin as B
import colocar_escudos as C
import escritor_plugin as W
import patch_plugin_v12 as P
from build_modular_v13 import save_plugin,clone,subs,ref,vanilla_records

def main():
    cfg=json.loads((ROOT/'config.json').read_text());path=BASE/'mod/AstraAsedio.esp';p=Plugin(str(path))
    original=P.record_map(p);ballesta=original[B.IDS['ballesta']]
    vm=B.read_vmad(subs(ballesta)['VMAD'])['scripts'][0]
    props={k:(v['type'],v['value']['form_id'] if v['type']==1 else v['value']) for k,v in vm['properties'].items()}
    for prop,key in [('FireSeconds','fire_seconds'),('ReleaseSeconds','release_seconds'),('ResetSeconds','reset_seconds'),('CycleSeconds','cycle_seconds')]:
        props[prop]=(4,cfg[key])
    change=P.modify_subs(ballesta,{'VMAD':B.vmad('AstraAsedioActi',props)})
    raw=p.d;start=p.inicio_datos;groups=[]
    while start<len(raw):
        size=struct.unpack_from('<I',raw,start+4)[0]
        groups.append(P.transform_groups(raw[start:start+size],{B.IDS['ballesta']:change},set(),{}));start+=size
    header=raw[:p.inicio_datos];out=ROOT/'mod/AstraAsedio.esp';out.write_bytes(header+b''.join(groups))
    after=P.record_map(Plugin(str(out)))
    assert after.keys()==original.keys()
    assert all(after[k]==v for k,v in original.items() if k!=B.IDS['ballesta'])
    B.validate_plugin(str(out))
    assert (ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp').read_bytes()==(BASE/'addons/Atalaya/AstraAsedio_Atalaya.esp').read_bytes()
    measured=json.loads((ROOT/'reports/towers_v14.json').read_text());assert measured['success'] and len(measured['sites'])==2
    assert measured['ballista_sha256']==hashlib.sha256((ROOT/'mod/meshes/AstraAsedio/ballesta.nif').read_bytes()).hexdigest()
    old=Plugin(str(BASE/'addons/Whiterun/AstraAsedio_Whiterun.esp'));oldmap=P.record_map(old)
    bases=[];placed=[];source=ROOT/'mod/scripts/source/AstraAsedioGuard.psc'
    for i,s in enumerate(measured['sites']):
        base=0x04000B00+i;prefix=0x04000B40+0x10*i
        npc=clone(oldmap[0x04000B00],base,{'EDID':W.zstr('AstraWhiterunArtilleroTorres'+str(i+1)),
                  'FULL':W.zstr('Artillero de la torre '+s['name'])})
        bases.append(npc)
        guardprops={'Artillero':(1,prefix+1),'Puesto':(1,prefix+2),'Launcher':(1,B.IDS['launcher']),
                    'ShotAmmo':(1,0x03000B01),'ShotSound':(1,B.IDS['shot_sound']),
                    'PitchMin':(4,s['pitch_min']),'PitchMax':(4,s['pitch_max']),
                    'ProjectileSpeed':(4,5400.),'ProjectileGravity':(4,240.345),'CadenceSeconds':(4,2.5),
                    'FireSeconds':(4,cfg['fire_seconds']),'ReleaseSeconds':(4,cfg['release_seconds']),'ResetSeconds':(4,cfg['reset_seconds'])}
        if s.get('yaw_half_sector',60)!=60:
            assert 'Property YawHalfSector' in source.read_text(),'Measured sector requires a script property'
            guardprops['YawHalfSector']=(4,s['yaw_half_sector'])
        if s.get('yaw_center',0)!=0:
            guardprops['YawCenter']=(4,s['yaw_center'])
        gun=ref(prefix,0x03000B02,s['gun_pos'],(0,0,s['yaw_deg']),'AstraWhiterunTorre'+s['name'].title()+'Ballesta',
                kind='REFR',persistent=True,vmad=B.vmad('AstraAsedioGuard',guardprops))
        scale=float(s.get('scale',1.))
        assert math.isfinite(scale) and .65<=scale<=1.,'Measured reference scale outside approved range'
        if scale!=1.:
            gun=W.record('REFR',prefix,[W.sub(k,v) for k,v in Plugin.subrecords(gun[24:])]+[W.sub('XSCL',struct.pack('<f',scale))],banderas=0x400)
        placed.append(gun)
        heading=(s['yaw_deg']+180)%360
        placed.append(ref(prefix+1,base,s['guard_pos'],(0,0,heading),'AstraWhiterunTorre'+s['name'].title()+'Guardia','ACHR',True))
        placed.append(ref(prefix+2,0x34,s['guard_pos'],(0,0,heading),'AstraWhiterunTorre'+s['name'].title()+'Puesto','REFR',True))
    marker_changes=[s['patrol_marker_adjustment'] for s in measured['sites'] if s.get('patrol_marker_adjustment')]
    marker_ids={int(m['id'],16) for m in marker_changes}
    assert marker_ids<={0x78784,0x7878a},'Only the two existing tower patrol destinations may move'
    vanilla=vanilla_records({0x3c,0xd74}|marker_ids)
    for m in marker_changes:
        fid=int(m['id'],16);original_marker=vanilla[fid]
        assert original_marker[:4]==b'REFR' and struct.unpack_from('<I',original_marker,8)[0]&0x400
        old_data=struct.unpack('<6f',subs(original_marker)['DATA'])
        assert all(math.isfinite(v) for v in m['pos']) and len(m['pos'])==3
        placed.append(P.modify_subs(original_marker,{'DATA':struct.pack('<6f',*m['pos'],*old_data[3:])}))
    world=clone(vanilla[0x3c],0x3c,{'FULL':W.zstr('Skyrim')},('OFST','RNAM'))
    persistent=W.grupo(struct.pack('<I',0xd74),[W.grupo(struct.pack('<I',0xd74),placed,8)],6)
    groups=[W.grupo('NPC_',bases),W.grupo('WRLD',[world,W.grupo(struct.pack('<I',0x3c),[vanilla[0xd74],persistent],1)])]
    city=save_plugin(ROOT/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp',groups,B.MASTERS+['AstraAsedio.esp'],0xB53)
    core={'path':str(out.relative_to(ROOT)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'records':len(after),'masters':B.MASTERS}
    atal=ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp'
    manifest={'core':core,'whiterun_torres':city,'atalaya':{'path':str(atal.relative_to(ROOT)),'sha256':hashlib.sha256(atal.read_bytes()).hexdigest(),'unchanged_from_v13':True},
              'placements':measured['sites'],'towers_evidence_sha256':hashlib.sha256((ROOT/'reports/towers_v14.json').read_bytes()).hexdigest(),
              'compatibility':{'world':'0000003C','container_cells':['00000D74'],'physical_cells':['0000961B','0000961C'],
                 'LAND_edits':0,'NAVM_edits':0,'NAVI_edits':0,'vanilla_reference_edits':len(marker_ids),'patrol_destination_edits':marker_changes,'existing_tower_edits':0,
                 'replace_old_plugin':'AstraAsedio_Whiterun.esp (disable)','city_save_migration_supported':False,'new_test_save_required':True,
                 'third_party_patches':'deferred','engine_verified':False}}
    (ROOT/'reports/modular_v14.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    print('MODULAR_V14_BUILT',core['records'],city['records'],'mounted guard stations',len(measured['sites']))
if __name__=='__main__':main()
