"""Two owned, shared-control cantilever stations; no vanilla patrol/nav edits."""
import sys,json,struct,hashlib,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import build_plugin as B
import patch_plugin_v12 as P
import escritor_plugin as W
import colocar_escudos as C
from build_modular_v13 import clone,subs,ref,vanilla_records

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    base=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v14');cfg=json.loads((ROOT/'config.json').read_text())
    for rel in ('mod/AstraAsedio.esp','addons/Atalaya/AstraAsedio_Atalaya.esp'):
        assert (ROOT/rel).read_bytes()==(base/rel).read_bytes()
    core=P.record_map(Plugin(str(ROOT/'mod/AstraAsedio.esp')))
    vm=B.read_vmad(subs(core[B.IDS['ballesta']])['VMAD'])['scripts'][0]
    playerprops={k:(v['type'],v['value']['form_id'] if v['type']==1 else v['value']) for k,v in vm['properties'].items()}
    measured=json.loads((ROOT/'reports/platforms_v15.json').read_text());assert measured['success']
    oldmap=P.record_map(Plugin(str(base/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp')))
    bases=[];stats=[];placed=[]
    for i,s in enumerate(measured['sites']):
        pre=0x04000B40+16*i;npcid=0x04000B00+i;statid=0x04000B60+i;name=s['name'];origin=s['origin']
        assert s['lost_nav_centers']==0 and not s['gun_contacts'] and not s['initial_projectile_hits']
        assert sha(ROOT/s['nif'])==s['nif_sha256']
        bases.append(clone(oldmap[npcid],npcid,{'EDID':W.zstr('AstraWhiterunVoladizoArtillero'+name.title())}))
        raw=B.stat('AstraVoladizo'+name.title(),'AstraAsedio\\voladizo_'+name+'.nif',struct.pack('<6h',-280,-740,-335,280,30,130))
        stats.append(W.record('STAT',statid,raw))
        properties={**playerprops,'Guard':(1,pre),'YawCenter':(4,0.),'YawHalfSector':(4,60.),
                    'PitchMin':(4,-20.),'PitchMax':(4,80.),'UseSightCamera':(5,True),'QALog':(5,True)}
        guardprops={'Artillero':(1,pre+1),'Puesto':(1,pre+2),'Standby':(1,pre+3),'AllowPlayerTakeover':(5,True),
                    'Launcher':(1,B.IDS['launcher']),'ShotAmmo':(1,0x03000B01),'ShotSound':(1,B.IDS['shot_sound']),
                    'YawCenter':(4,0.),'YawHalfSector':(4,60.),'PitchMin':(4,-20.),'PitchMax':(4,80.),
                    'ProjectileSpeed':(4,5400.),'ProjectileGravity':(4,240.345),'CadenceSeconds':(4,2.5),
                    'FireSeconds':(4,cfg['fire_seconds']),'ReleaseSeconds':(4,cfg['release_seconds']),'ResetSeconds':(4,cfg['reset_seconds'])}
        a=B.vmad('AstraAsedioStation',properties);b=B.vmad('AstraAsedioGuard',guardprops)
        dual=a[:4]+struct.pack('<H',2)+a[6:]+b[6:]
        placed.append(ref(pre,0x03000B02,s['gun_world_pos'],(0,0,0),'AstraVoladizo'+name.title()+'Ballesta','REFR',True,dual))
        op=[a+b for a,b in zip(origin,s['operator_local_foot'])];wait=[a+b for a,b in zip(origin,s['standby_local_foot'])]
        placed += [ref(pre+1,npcid,op,(0,0,180),'AstraVoladizo'+name.title()+'Guardia','ACHR',True),
                   ref(pre+2,0x34,op,(0,0,180),'AstraVoladizo'+name.title()+'Puesto','REFR',True),
                   ref(pre+3,0x34,wait,(0,0,180),'AstraVoladizo'+name.title()+'Espera','REFR',True),
                   ref(pre+4,statid,origin,(0,0,0),'AstraVoladizo'+name.title()+'Plataforma','REFR',True)]
    vanilla=vanilla_records({0x3c,0xd74})
    world=clone(vanilla[0x3c],0x3c,{'FULL':W.zstr('Skyrim')},('OFST','RNAM'))
    persistent=W.grupo(struct.pack('<I',0xd74),[W.grupo(struct.pack('<I',0xd74),placed,8)],6)
    groups=[W.grupo('NPC_',bases),W.grupo('STAT',stats),W.grupo('WRLD',[world,W.grupo(struct.pack('<I',0x3c),[vanilla[0xd74],persistent],1)])]
    body=b''.join(groups);masters=B.MASTERS+['AstraAsedio.esp']
    header=W.tes4(masters,C.bloques_totales(body,0),0xB62,'Astra',False,'QA v15: plataformas voladizas y control compartido')
    path=ROOT/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp';path.write_bytes(header+body)
    city=P.record_map(Plugin(str(path)));assert 0x78784 not in city and 0x7878a not in city
    report={'revision':15,'core_sha256':sha(ROOT/'mod/AstraAsedio.esp'),'core_unchanged_from_v14':True,
            'atalaya_unchanged_from_v14':True,'whiterun_torres':{'path':str(path.relative_to(ROOT)),'records':len(city),'masters':masters,'sha256':sha(path)},
            'platforms_evidence_sha256':sha(ROOT/'reports/platforms_v15.json'),'placements':measured['sites'],
            'compatibility':{'LAND_edits':0,'NAVM_edits':0,'NAVI_edits':0,'PACK_edits':0,'vanilla_reference_edits':0,
                            'patrol_destination_edits':0,'existing_tower_edits':0,'city_save_migration_supported':False,
                            'new_test_save_required':True,'third_party_patches':'deferred','engine_verified':False}}
    (ROOT/'reports/modular_v15.json').write_text(json.dumps(report,indent=2))
    print('MODULAR_V15_BUILT',len(core),len(city),'shared stations',len(measured['sites']))
if __name__=='__main__':main()
