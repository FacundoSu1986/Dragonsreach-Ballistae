import sys,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import build_plugin as B
def records(path):
    p=Plugin(str(path))
    return p,{p.form_id(o):(t,dict(p.subrecords(p.datos(o)))) for t,o,n,d in p.recorrer() if t not in ('GRUP','TES4')}
def test_core_has_no_world_placements_or_terrain():
    p,r=records(ROOT/'mod/AstraAsedio.esp')
    assert not any(t in ('WRLD','LAND','ACHR','NPC_') for t,ss in r.values())
    assert not any(t=='CELL' and 'XCLC' in ss for t,ss in r.values())
    vm=B.read_vmad(r[0x03000801][1]['VMAD'])
    assert vm['scripts'][0]['properties']['PitchMin']['value']==-20
def test_city_own_references_only():
    p,r=records(ROOT/'addons/Whiterun/AstraAsedio_Whiterun.esp')
    assert not any(t in ('LAND','NAVM','NAVI','PACK') for t,ss in r.values())
    assert all(fid>>24==4 for fid,(t,ss) in r.items() if t in ('REFR','ACHR','NPC_'))
    actors=[fid for fid,(t,ss) in r.items() if t=='ACHR']
    assert len(actors)==1
    gun=next(ss for fid,(t,ss) in r.items() if t=='REFR' and 'VMAD'in ss)
    props=B.read_vmad(gun['VMAD'])['scripts'][0]['properties']
    assert props['Artillero']['value']['form_id']==actors[0]
    assert props['ShotAmmo']['value']['form_id']==0x03000B01
def test_guard_projectile_nonexplosive():
    p,r=records(ROOT/'mod/AstraAsedio.esp')
    data=r[0x03000B00][1]['DATA']
    assert not struct.unpack_from('<H',data)[0]&2
    assert struct.unpack_from('<I',data,36)[0]==0
    assert abs(struct.unpack_from('<f',data,4)[0]-.35)<1e-6
    assert struct.unpack_from('<f',data,8)[0]==5400

def test_world_container_has_no_master_offset_tables_or_localized_full():
    p,r=records(ROOT/'addons/Whiterun/AstraAsedio_Whiterun.esp')
    ss=r[0x3C][1]
    assert ss['FULL']==b'Skyrim\0'
    assert 'OFST' not in ss and 'RNAM' not in ss
    npc=next(ss for typ,ss in r.values() if typ=='NPC_')
    assert 'RNAM' in npc
