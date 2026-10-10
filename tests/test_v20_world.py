"""Actual payload regressions for terrain-safe relocation."""
from pathlib import Path
import json,sys,struct,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
import nif_nodos,nif_fisica
from parser_esm import Plugin
import patch_plugin_v12 as P
from build_modular_v13 import subs

def test_atalaya_uses_user_position_and_keeps_owned_reference_ids():
    r=P.record_map(Plugin(str(ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp')))
    p=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v19')
    old=P.record_map(Plugin(str(p/'addons/Atalaya/AstraAsedio_Atalaya.esp')))
    oldrefs={fid for fid,raw in old.items() if fid>>24==4 and raw[:4]==b'REFR'}
    assert oldrefs<={fid for fid,raw in r.items() if raw[:4]==b'REFR'}
    tower=struct.unpack('<6f',subs(r[0x04000A01])['DATA'])
    assert max(abs(a-b) for a,b in zip(tower[:3],(4665.54,-14922.81,-5217.81)))<.003
    assert abs(math.degrees(tower[5])%360-187.63)<.001
    gun=struct.unpack('<6f',subs(r[0x04000A00])['DATA'])
    assert abs(gun[2]-tower[2]-151.55)<.003

def test_atalaya_keeps_navigation_and_quests_and_only_opens_the_stair():
    r=P.record_map(Plugin(str(ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp')))
    assert not any(raw[:4] in (b'NAVM',b'NAVI',b'PACK',b'QUST') for raw in r.values())
    assert {fid for fid in r if fid>>24<4}=={0x3c,0x963d,0xa63d,0xe4396,0xe4397}

def test_core_firing_and_city_station_payloads_unchanged():
    parent=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v19')
    for path in (ROOT/'mod').rglob('*'):
        if path.is_file():assert path.read_bytes()==(parent/path.relative_to(ROOT)).read_bytes()
    for path in (ROOT/'addons/WhiterunTorres').rglob('*'):
        if path.is_file():assert path.read_bytes()==(parent/path.relative_to(ROOT)).read_bytes()

def test_shields_follow_the_tower_and_chest_seats_on_existing_terrain():
    import mundo_v11 as M
    from atalaya_v20_geometry import Surface
    r=P.record_map(Plugin(str(ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp')))
    cfg=json.loads((ROOT/'config.json').read_text());site=cfg['tower_v11']['mundo']
    for i,item in enumerate(cfg['tower_v11']['escudos']['items']):
        fid=0x04000A43+i
        pos,rot=M.llevar({'pos':item['pos'],'rot_deg':item['rot_deg'],'scale':1},site)
        data=struct.unpack('<6f',subs(r[fid])['DATA'])
        assert max(abs(a-b) for a,b in zip(pos,data[:3]))<.003
        a=M.L.transform_matrix((0,0,0),rot,1,*M.L.engine_convention())['r']
        b=M.L.transform_matrix((0,0,0),[math.degrees(v) for v in data[3:]],1,*M.L.engine_convention())['r']
        assert np.max(abs(np.array(a)-np.array(b)))<1e-6
    s=Surface();data=struct.unpack('<6f',subs(r[0x04000A02])['DATA']);local=np.array(s.m['r']).T@(np.array(data[:3])-np.array(s.m['t']))
    assert abs(local[2]-s.z(local[0],local[1])-2)<.003

def test_site_specific_model_is_resolved_and_in_cell():
    import v11_layout as L
    r=P.record_map(Plugin(str(ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp')))
    assert struct.unpack('<I',subs(r[0x04000A01])['NAME'])[0]==0x04000A50
    model=subs(r[0x04000A50])['MODL'].rstrip(b'\0').decode()
    path=ROOT/'addons/Atalaya/meshes'/model
    assert path.exists()
    n=nif_nodos.leer(str(path));assert n['bloques'][0][0]=='BSFadeNode'
    box=struct.unpack('<6h',subs(r[0x04000A50])['OBND']);lo,hi=nif_fisica.caja_visual(n)
    assert all(a<=b for a,b in zip(box[:3],lo)) and all(a>=b for a,b in zip(box[3:],hi))
    for raw in r.values():
        if raw[:4]==b'REFR':
            data=struct.unpack('<6f',subs(raw)['DATA'])
            assert math.floor(data[0]/4096)==1 and math.floor(data[1]/4096)==-4

def test_written_model_verified_against_current_inputs():
    import hashlib
    report=json.loads((ROOT/'reports/atalaya_verified_v20.json').read_text())
    assert report['success'] and report['walk_samples']==244 and report['static_aim_poses']==1512
    assert not report['capsule_blocked'] and not report['vanilla_access_blocked']
    assert not report['gun_contacts'] and not report['initial_shot_hits']
    assert report['stair_ground_max_overlap']<2
    for rel,h in report['inputs_sha256'].items():
        if rel=='config.json':
            site=json.loads((ROOT/'config.json').read_text())['tower_v11']['mundo']
            assert [site['x'],site['y'],site['z'],site['rot_z_deg'],site['cell']]==[4665.54,-14922.81,-5217.81,187.63,'0000963D']
            continue
        assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel
