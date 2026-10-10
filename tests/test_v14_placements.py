"""Validate the actual v14 mounted references, not the former freestanding site."""
import json,math,struct,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v13')
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import build_plugin as B
from inspect_towers_v14 import nav_surface

def records():
    path=ROOT/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp'
    assert path.exists(),'New two-tower plugin has not been built'
    p=Plugin(str(path))
    return p,{p.form_id(o):(t,dict(p.subrecords(p.datos(o))),struct.unpack_from('<I',p.d,o+8)[0])
              for t,o,n,d in p.recorrer() if t!='GRUP'}

def test_two_owned_stations_and_only_measured_patrol_destination_overrides():
    p,r=records()
    sites=json.loads((ROOT/'reports/towers_v14.json').read_text())['sites']
    patrol_ids={int(s['patrol_marker_adjustment']['id'],16) for s in sites if s.get('patrol_marker_adjustment')}
    assert patrol_ids<={0x78784,0x7878a}
    assert {fid for fid,(t,ss,flags) in r.items() if t=='NPC_'}=={0x04000B00,0x04000B01}
    assert {fid for fid,(t,ss,flags) in r.items() if t in ('REFR','ACHR')}=={0x04000B40,0x04000B41,0x04000B42,0x04000B50,0x04000B51,0x04000B52}|patrol_ids
    assert not any(t in ('LAND','NAVM','NAVI','PACK','STAT') for t,ss,flags in r.values())
    assert {fid for fid,(t,ss,flags) in r.items() if fid and fid>>24<4}=={0x3c,0xd74}|patrol_ids
    assert all(flags&0x400 for fid,(t,ss,flags) in r.items() if t in ('REFR','ACHR'))
    masters=[v.rstrip(b'\0').decode() for k,v in p.subrecords(p.datos(0)) if k=='MAST']
    assert masters==['Skyrim.esm','Update.esm','Dawnguard.esm','AstraAsedio.esp']
    from build_modular_v13 import vanilla_records,subs
    original=vanilla_records(patrol_ids) if patrol_ids else {}
    for s in sites:
        m=s.get('patrol_marker_adjustment')
        if not m:continue
        fid=int(m['id'],16);before=subs(original[fid]);after=r[fid][1]
        assert {k:v for k,v in before.items() if k!='DATA'}=={k:v for k,v in after.items() if k!='DATA'}
        assert struct.unpack('<6f',after['DATA'])[:3]==pytest.approx(m['pos'],abs=.001)
        assert after['DATA'][12:]==before['DATA'][12:]

@pytest.mark.parametrize('i,prefix,grid,cell',[(0,0x04000B40,(4,-3),'0000961B'),(1,0x04000B50,(3,-3),'0000961C')])
def test_measured_transforms_and_independent_vmad(i,prefix,grid,cell):
    p,r=records();report=json.loads((ROOT/'reports/towers_v14.json').read_text());s=report['sites'][i]
    assert s['cell']==cell
    gun=r[prefix][1];actor=r[prefix+1][1];marker=r[prefix+2][1]
    xyz=struct.unpack('<6f',gun['DATA'])
    assert xyz[:3]==pytest.approx(s['gun_pos'],abs=.001)
    assert xyz[5]==pytest.approx(math.radians(s['yaw_deg']),abs=1e-6)
    assert struct.unpack('<f',gun.get('XSCL',struct.pack('<f',1.)))[0]==pytest.approx(s.get('scale',1.),abs=1e-6)
    assert tuple(math.floor(v/4096) for v in xyz[:2])==grid
    assert struct.unpack('<I',gun['NAME'])[0]==0x03000B02
    assert struct.unpack('<I',actor['NAME'])[0]==0x04000B00+i
    assert struct.unpack('<6f',actor['DATA'])[:3]==pytest.approx(s['guard_pos'],abs=.001)
    assert marker['DATA']==actor['DATA']
    vm=B.read_vmad(gun['VMAD'])['scripts'];assert len(vm)==1 and vm[0]['name']=='AstraAsedioGuard'
    props=vm[0]['properties']
    assert props['Artillero']['value']['form_id']==prefix+1 and props['Puesto']['value']['form_id']==prefix+2
    for n,val in [('FireSeconds',.2),('ReleaseSeconds',1/15),('ResetSeconds',.8),('CadenceSeconds',2.5),
                  ('PitchMin',s['pitch_min']),('PitchMax',s['pitch_max'])]:
        assert props[n]['type']==4 and props[n]['value']==pytest.approx(val,abs=1e-6)
    assert 'Session' not in props
    assert props.get('YawHalfSector',{'value':60.})['value']==pytest.approx(s.get('yaw_half_sector',60.),abs=1e-6)
    assert props.get('YawCenter',{'value':0.})['value']==pytest.approx(s.get('yaw_center',0.),abs=1e-6)
    nav=json.loads((ROOT/'reports/tower_context_v14.json').read_text())['navmeshes']
    assert any(abs(n['z']-s['guard_pos'][2])<8 for n in nav_surface(nav,*s['guard_pos'][:2]))

def test_core_preserves_every_record_except_player_timing_vmad_and_atalaya():
    def allrecords(path):
        p=Plugin(str(path));return {p.form_id(o):(t,p.datos(o)) for t,o,n,d in p.recorrer() if t not in ('GRUP','TES4')}
    old=allrecords(BASE/'mod/AstraAsedio.esp');new=allrecords(ROOT/'mod/AstraAsedio.esp')
    assert new.keys()==old.keys()
    for fid in old:
        if fid!=B.IDS['ballesta']:assert new[fid]==old[fid],f'{fid:08X}'
    vm=B.read_vmad(dict(Plugin.subrecords(new[B.IDS['ballesta']][1]))['VMAD'])['scripts'][0]['properties']
    for n,val in [('FireSeconds',.2),('ReleaseSeconds',1/15),('ResetSeconds',.8),('CycleSeconds',1.)]:
        assert vm[n]['value']==pytest.approx(val,abs=1e-6)
    assert (ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp').read_bytes()==(BASE/'addons/Atalaya/AstraAsedio_Atalaya.esp').read_bytes()
