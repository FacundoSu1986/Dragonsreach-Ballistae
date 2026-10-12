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

# v22: los voladizos pasan de "estacion compartida con el jugador" a "puesto de guardia".
# La torreta baja (pivote 117) NO puede llevar la mira nativa -- medida en
# `reports/sight_path_v22_FAILED.json` -- asi que el jugador deja de poder operarlos
# (`AllowPlayerTakeover=False`) y la estacion deja de declarar mira (`UseSightCamera=False`).
# El jugador conserva la torreta del core (ACTI 0x03000801, `ballesta.nif`, pivote 153).
ACTI_BAJO=0x03000B04
ACTI_BAJO_MODL='AstraAsedio\\ballesta_guardia.nif'
PIVOTE_BAJO=117.0

def main():
    base=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v14');cfg=json.loads((ROOT/'config.json').read_text())
    core=P.record_map(Plugin(str(ROOT/'mod/AstraAsedio.esp')))
    # El assert original exigia que el core fuese byte a byte el de v14 (el core no cambiaba
    # entre v14 y v21). Desde v22 el core SI cambia (guardia hibrido + torreta baja), asi que
    # la igualdad ya no se puede exigir. La dependencia real de este addon es que el core
    # provea el ACTI BAJO `0x03000B04` (con `ballesta_guardia.nif`) al que apuntan las
    # torretas de los voladizos: sin eso el addon queda con una referencia colgante.
    assert (ROOT/'mod/AstraAsedio.esp').exists()
    assert (ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp').exists(),'falta el Atalaya'
    assert 0x03000B04 in core,'el core no tiene el ACTI bajo 0x03000B04'
    modl_bajo=subs(core[0x03000B04])['MODL'].rstrip(b'\0').decode()
    assert modl_bajo==ACTI_BAJO_MODL,'0x03000B04 apunta a %r, se esperaba %r'%(modl_bajo,ACTI_BAJO_MODL)
    vm=B.read_vmad(subs(core[B.IDS['ballesta']])['VMAD'])['scripts'][0]
    playerprops={k:(v['type'],v['value']['form_id'] if v['type']==1 else v['value']) for k,v in vm['properties'].items()}
    measured=json.loads((ROOT/'reports/platforms_v15.json').read_text());assert measured['success']
    oldmap=P.record_map(Plugin(str(base/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp')))
    bases=[];stats=[];placed=[]
    for i,s in enumerate(measured['sites']):
        pre=0x04000B70+16*i;npcid=0x04000B00+i;statid=0x04000B60+i;name=s['name'];origin=s['origin']
        assert s['lost_nav_centers']==0 and not s['gun_contacts'] and not s['initial_projectile_hits']
        assert sha(ROOT/s['nif'])==s['nif_sha256']
        bases.append(clone(oldmap[npcid],npcid,{'EDID':W.zstr('AstraWhiterunVoladizoArtillero'+name.title())}))
        raw=B.stat('AstraVoladizo'+name.title(),'AstraAsedio\\voladizo_'+name+'.nif',struct.pack('<6h',-280,-740,-335,280,30,130))
        stats.append(W.record('STAT',statid,raw))
        properties={**playerprops,'Guard':(1,pre),'YawCenter':(4,0.),'YawHalfSector':(4,60.),
                    'PitchMin':(4,-20.),'PitchMax':(4,80.),'UseSightCamera':(5,False),'QALog':(5,True),
                    'PitchPivotHeight':(4,PIVOTE_BAJO)}
        guardprops={'Artillero':(1,pre+1),'Puesto':(1,pre+2),'Standby':(1,pre+3),'AllowPlayerTakeover':(5,False),
                    'Launcher':(1,B.IDS['launcher']),'ShotAmmo':(1,0x03000B01),'ShotSound':(1,B.IDS['shot_sound']),
                    'YawCenter':(4,0.),'YawHalfSector':(4,60.),'PitchMin':(4,-20.),'PitchMax':(4,80.),
                    'ProjectileSpeed':(4,5400.),'ProjectileGravity':(4,240.345),'CadenceSeconds':(4,2.5),
                    'FireSeconds':(4,cfg['fire_seconds']),'ReleaseSeconds':(4,cfg['release_seconds']),'ResetSeconds':(4,cfg['reset_seconds'])}
        a=B.vmad('AstraAsedioStation',properties);b=B.vmad('AstraAsedioGuard',guardprops)
        dual=a[:4]+struct.pack('<H',2)+a[6:]+b[6:]
        placed.append(ref(pre,ACTI_BAJO,s['gun_world_pos'],(0,0,0),'AstraVoladizo'+name.title()+'Ballesta','REFR',True,dual))
        op=[a+b for a,b in zip(origin,s['operator_local_foot'])];wait=[a+b for a,b in zip(origin,s['standby_local_foot'])]
        placed += [ref(pre+1,npcid,op,(0,0,180),'AstraVoladizo'+name.title()+'Guardia','ACHR',True),
                   ref(pre+2,0x34,op,(0,0,180),'AstraVoladizo'+name.title()+'Puesto','REFR',True),
                   ref(pre+3,0x34,wait,(0,0,180),'AstraVoladizo'+name.title()+'Espera','REFR',True),
                   ref(pre+4,statid,origin,(0,0,0),'AstraVoladizo'+name.title()+'Plataforma','REFR',True)]
    # Preserve original IDs as disabled records for old saved instances. New
    # refs guarantee complete Station/Guard properties without rebinding a save.
    # v29: el legacy conserva FormID, flags, base y datos, pero recibe EDID propio
    # (`AstraLegacyVoladizo*`). Los dos juegos comparten celda y repetian nombre, que
    # es lo unico que xEdit marca como duplicado. `scripts/patch_legacy_edids_v29.py`
    # deja el ESP publicado en este mismo estado sin volver a correr el pipeline.
    previous=P.record_map(Plugin(str(ROOT.with_name('Ballesta_Astra_Vanilla_SE_v16')/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp')))
    legacy_parts=('Ballesta','Guardia','Puesto','Espera','Plataforma')
    for start,side in ((0x04000B40,'Este'),(0x04000B50,'Oeste')):
        for offset in range(5):
            raw=bytearray(previous[start+offset]);struct.pack_into('<I',raw,8,struct.unpack_from('<I',raw,8)[0]|0x800)
            raw=bytearray(P.modify_subs(bytes(raw),{'EDID':W.zstr('AstraLegacyVoladizo'+side+legacy_parts[offset])}))
            placed.append(bytes(raw))
    vanilla=vanilla_records({0x3c,0xd74})
    world=clone(vanilla[0x3c],0x3c,{'FULL':W.zstr('Skyrim')},('OFST','RNAM'))
    persistent=W.grupo(struct.pack('<I',0xd74),[W.grupo(struct.pack('<I',0xd74),placed,8)],6)
    groups=[W.grupo('NPC_',bases),W.grupo('STAT',stats),W.grupo('WRLD',[world,W.grupo(struct.pack('<I',0x3c),[vanilla[0xd74],persistent],1)])]
    body=b''.join(groups);masters=B.MASTERS+['AstraAsedio.esp']
    header=W.tes4(masters,C.bloques_totales(body,0),0xB85,'Astra',False,'QA v22: voladizos como puestos de guardia con la torreta baja')
    path=ROOT/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp';path.write_bytes(header+body)
    city=P.record_map(Plugin(str(path)));assert 0x78784 not in city and 0x7878a not in city
    report={'revision':17,'core_sha256':sha(ROOT/'mod/AstraAsedio.esp'),
            'core_unchanged_from_v14':False,
            'core_unchanged_from_v14_nota':'desde v22 el core cambia (guardia hibrido + torreta baja); '
                                           'este addon depende de que el core provea el ACTI bajo 0x03000B04',
            'atalaya_unchanged_from_v14':True,
            'v22_torreta_baja':{'acti':f'{ACTI_BAJO:08X}','modl':ACTI_BAJO_MODL,'pivote_units':PIVOTE_BAJO,
                                'allow_player_takeover':False,'use_sight_camera':False,
                                'nota':'los voladizos pasan a ser puestos de guardia: el jugador ya no los opera y '
                                       'por eso la torreta puede ser la baja (la mira nativa degenera con el pivote '
                                       'en 117, medido en reports/sight_path_v22_FAILED.json)'},
            'whiterun_torres':{'path':str(path.relative_to(ROOT)),'records':len(city),'masters':masters,'sha256':sha(path)},
            'legacy_edids':'AstraLegacyVoladizo{Este,Oeste}* (0xB40-0xB54, sin cambios de FormID, flags ni base)',
            'platforms_evidence_sha256':sha(ROOT/'reports/platforms_v15.json'),'placements':measured['sites'],
            'compatibility':{'LAND_edits':0,'NAVM_edits':0,'NAVI_edits':0,'PACK_edits':0,'vanilla_reference_edits':0,
                            'patrol_destination_edits':0,'existing_tower_edits':0,'city_save_migration_supported':False,
                            'new_test_save_required':False,'third_party_patches':'deferred','engine_verified':False}}
    (ROOT/'reports/modular_v17.json').write_text(json.dumps(report,indent=2))
    print('MODULAR_V17_BUILT',len(core),len(city),'shared stations',len(measured['sites']))
if __name__=='__main__':main()
