"""Final city VMAD and owned records; no engine activation claims."""
from pathlib import Path
import sys,struct,json
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import build_plugin as B
import patch_plugin_v12 as P
from build_modular_v13 import subs

def records():
    p=Plugin(str(ROOT/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp'))
    return P.record_map(p)

def test_only_own_placements_no_vanilla_patrol_or_nav_edits():
    r=records()
    assert not any(raw[:4] in (b'LAND',b'NAVM',b'NAVI',b'PACK') for raw in r.values())
    assert {fid for fid in r if fid and fid>>24<4}=={0x3c,0xd74}
    assert 0x78784 not in r and 0x7878a not in r
    assert sum(raw[:4]==b'STAT' for raw in r.values())==2
    assert sum(raw[:4]==b'ACHR' for raw in r.values())==4
    assert sum(raw[:4]==b'ACHR' and not struct.unpack_from('<I',raw,8)[0]&0x800 for raw in r.values())==2

def test_each_gun_uses_coordinated_player_and_guard_scripts():
    r=records();core=P.record_map(Plugin(str(ROOT/'mod/AstraAsedio.esp')))
    coreprops=B.read_vmad(subs(core[B.IDS['ballesta']])['VMAD'])['scripts'][0]['properties']
    for prefix in (0x04000B70,0x04000B80):
        scripts=B.read_vmad(subs(r[prefix])['VMAD'])['scripts']
        assert [s['name'] for s in scripts]==['AstraAsedioStation','AstraAsedioGuard']
        player,guard=[s['properties'] for s in scripts]
        assert player['Guard']['value']['form_id']==prefix
        assert guard['AllowPlayerTakeover']['value'] is True
        assert guard['Standby']['value']['form_id']==prefix+3
        assert guard['Artillero']['value']['form_id']==prefix+1
        assert guard['Puesto']['value']['form_id']==prefix+2
        for name in ('Session','Launcher','ShotAmmo','SteelBolt','ShotSound'):
            assert player[name]==coreprops[name]
        for props in (player,guard):
            assert props['YawHalfSector']['value']==60
            assert props['YawCenter']['value']==0
            assert props['PitchMin']['value']==-20 and props['PitchMax']['value']==80
        assert player['UseSightCamera']['value'] is True
        assert player['CycleSeconds']['value']==1
        assert guard['CadenceSeconds']['value']==2.5

def test_actual_refs_match_written_platform_measurements():
    r=records();report=json.loads((ROOT/'reports/platforms_v15.json').read_text())
    for i,s in enumerate(report['sites']):
        pre=0x04000B70+16*i;origin=s['origin']
        expected={pre:s['gun_world_pos'],pre+1:[a+b for a,b in zip(origin,s['operator_local_foot'])],
                  pre+2:[a+b for a,b in zip(origin,s['operator_local_foot'])],
                  pre+3:[a+b for a,b in zip(origin,s['standby_local_foot'])],pre+4:origin}
        for fid,pos in expected.items():
            ss=subs(r[fid]);data=struct.unpack('<6f',ss['DATA'])
            assert max(abs(a-b) for a,b in zip(data[:3],pos))<.003
            assert struct.unpack_from('<I',r[fid],8)[0]&0x400
        model=subs(r[0x04000B60+i])['MODL'].rstrip(b'\0').decode()
        assert model=='AstraAsedio\\voladizo_'+s['name']+'.nif'
        assert (ROOT/'addons/WhiterunTorres/meshes'/model).exists()

def test_core_and_low_tower_preserved_from_v14():
    base=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v14')
    # v20 relocates the optional Atalaya. Core and Whiterun retain the measured
    # v14/v19 geometry; the new exterior contract is in test_v20_world.
    for rel in ('mod/AstraAsedio.esp','mod/meshes/AstraAsedio/ballesta.nif','mod/meshes/AstraAsedio/torre.nif'):
        assert (ROOT/rel).read_bytes()==(base/rel).read_bytes()
