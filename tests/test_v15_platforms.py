import sys,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))

def test_full_size_guns_outside_original_walkways():
    import platforms_v15_geometry as G
    for name in ('este','oeste'):
        s=G.site(name)
        assert s['scale']==1 and s['gun_local_pos'][1]<-400
        assert s['yaw_range']==[-60,60] and s['pitch_range']==[-20,80]
        assert s['operator_local_foot'][1]+18<-230
        assert s['standby_local_foot'][1]+18<-180

def test_access_steps_keep_original_nav_capsule_buffer():
    import platforms_v15_geometry as G
    east=G.site('este')
    risers=[b for b in east['floor_boxes'] if b['kind']=='step']
    assert len(risers)==4
    assert [round(b['hi'][2]-east['floor_local_z']) for b in risers]==[20,40,60,72]
    assert all(b['lo'][0]>=145 for b in risers)
    assert max(east['step_rises'])<=20
    west=G.site('oeste')
    assert west['step_rises']==[]
    assert G.floor_z(west,0,-150)==west['deck_local_z']

def test_deck_supports_every_fixed_gun_base_sample():
    import platforms_v15_geometry as G
    h=np.load(ROOT/'reports/gun_havok_v14.npz')['C']
    for name in ('este','oeste'):
        s=G.site(name);pos=np.array(s['gun_local_pos'])
        for x in np.linspace(h[:,0].min(),h[:,0].max(),9):
            for y in np.linspace(h[:,1].min(),h[:,1].max(),9):
                z=G.floor_z(s,pos[0]+x,pos[1]+y)
                assert z is not None and abs(z-(pos[2]+h[:,2].min()))<.01
        for key in ('operator_local_foot','standby_local_foot'):
            p=s[key];assert abs(G.floor_z(s,*p[:2])-p[2])<.01

def test_braces_join_real_wall_anchors_and_outer_beams():
    import platforms_v15_geometry as G
    for name in ('este','oeste'):
        s=G.site(name)
        assert len(s['braces'])==2
        for b in s['braces']:
            assert b['a'][2]==-280 and b['b'][1]<=-580
            assert b['b'][2]==s['deck_local_z']-26
            assert abs(b['a'][0])==96 and b['a'][0]==b['b'][0]
        assert s['original_reference_overrides']==[]

def test_walking_route_is_supported_and_bounded_step_changes():
    import platforms_v15_geometry as G
    for name in ('este','oeste'):
        s=G.site(name)
        for p in G.route_samples(s):
            if p[0]<=137 and name=='este':continue
            if name=='oeste' and p[1]>-126:continue
            z=G.floor_z(s,*p[:2]);assert z is not None
            assert abs(z-p[2])<=20.01
        assert all(math.isfinite(q) for b in s['collision_boxes'] for k in ('lo','hi') for q in b[k])

def test_own_visuals_have_uvs_and_solid_collider():
    import platforms_v15_geometry as G
    cfg=json.loads((ROOT/'config.json').read_text())
    for name in ('este','oeste'):
        s,parts=G.build(name,cfg)
        assert len(parts)>50
        for p in parts:
            assert len(p['mats'])==len(p['faces'])
            assert len(p['uvs'])==len(p['verts'])
            assert all(math.isfinite(v) for pt in p['verts'] for v in pt)
        assert all(b['hi'][2]>b['lo'][2] for b in s['collision_boxes'])
