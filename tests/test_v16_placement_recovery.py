"""Real Guard PSC recovery with stored v14 position and native interruptions."""
from types import SimpleNamespace
from pathlib import Path
import json
import pytest
from test_v13_guard import GuardFixture, ActorFixture, rotation_z


def mounted(site):
    f=GuardFixture(); f.native_free=True; f.site=site; f.placement_moves=[]
    f.root_pos=[0.,0.,0.]; f.root_angle=[0.,0.,180.]
    f.root_rotation=rotation_z(180)
    f.anchor=ActorFixture((0.,0.,0.)); f.wait=ActorFixture((180.,260.,0.))
    f.vm.state.update(AllowPlayerTakeover=True, Standby=f.wait,
                     AstraSightNative=SimpleNamespace(IsEffectsQuiescent=lambda *args:f.native_free,
                                                      ResetIdleScene=lambda *args:f.native_free))
    f.vm.state['SKSE'].GetPluginVersion=lambda name: 0x03050040
    for item in (f.anchor,f.marker,f.wait):
        item.angles=[0.,0.,0.]
        item.GetAngleX=lambda item=item:item.angles[0]
        item.GetAngleY=lambda item=item:item.angles[1]
        item.GetAngleZ=lambda item=item:item.angles[2]
        def move(anchor, x=0., y=0., z=0., match=True, item=item):
            f.placement_moves.append(item)
            item.pos=[anchor.pos[0]+x,anchor.pos[1]+y,anchor.pos[2]+z]
            if match:item.angles=anchor.angles[:]
        item.MoveTo=move
        item.SetAngle=lambda x,y,z,item=item:setattr(item,'angles',[x,y,z])
    for i,axis in enumerate('XYZ'):
        setattr(f,'GetPosition'+axis,lambda i=i:f.root_pos[i])
        setattr(f,'GetAngle'+axis,lambda i=i:f.root_angle[i])
    def move_root(anchor,x=0.,y=0.,z=0.,match=True):
        f.placement_moves.append(f);f.root_pos=[anchor.pos[0]+x,anchor.pos[1]+y,anchor.pos[2]+z]
        if match:f.root_angle=anchor.angles[:]
        f.root_rotation=rotation_z(f.root_angle[2])
    f.MoveTo=move_root
    def angle_root(x,y,z):
        f.root_angle=[x,y,z];f.root_rotation=rotation_z(z)
    f.SetAngle=angle_root
    gun=0xB70 if site=='este' else 0xB80
    f.vm.state['Game'].GetFormFromFile=lambda form,filename: {
        gun:f,gun+2:f.marker,gun+3:f.wait,gun+4:f.anchor}.get(form) if filename=='AstraAsedio_WhiterunTorres.esp' else None
    certificate=json.loads((Path(__file__).resolve().parents[1]/'reports/platforms_v15.json').read_text())
    measured=next(s for s in certificate['sites'] if s['name']==site)
    f.gun_y=measured['gun_local_pos'][1]
    f.deck=measured['deck_local_z']
    f.wait_y=measured['standby_local_foot'][1]
    return f


def assert_placed(f):
    assert f.root_pos==pytest.approx([0.,f.gun_y,f.deck])
    assert f.root_angle==[0.,0.,0.]
    assert f.marker.pos==pytest.approx([124.,f.gun_y+144,f.deck])
    assert f.wait.pos==pytest.approx([-210.,f.wait_y,f.deck])
    assert f.marker.angles==[0.,0.,180.] and f.wait.angles==[0.,0.,180.]


@pytest.mark.parametrize('site',['este','oeste'])
def test_load_relocates_saved_gun_and_owned_markers_onto_existing_extension(site):
    f=mounted(site);f.load();assert_placed(f)
    assert f.vm.state['running'] and f.guard.pinned and f.guard.pos==f.marker.pos
    moves=len(f.placement_moves);f.load();assert_placed(f)
    assert len(f.placement_moves)==moves, 'An already correct loaded placement must not teleport again'


@pytest.mark.parametrize('site',['este','oeste'])
def test_prepare_repairs_saved_placement_before_admitting_player(site):
    f=mounted(site);lease=f.run('ReservePlayerLease')
    assert f.run('PreparePlayerLease',lease);assert_placed(f)
    assert f.vm.state['playerReady'] and f.guard.pos==f.wait.pos and f.guard.pinned
    f.run('ReleasePlayerLease',lease)
    assert f.vm.state['running'] and f.guard.pos==f.marker.pos


@pytest.mark.parametrize('order',['before','after'])
@pytest.mark.parametrize('cancel',['takeover','load','unload'])
@pytest.mark.parametrize('target',['gun','post','standby'])
@pytest.mark.parametrize('operation',['MoveTo','SetAngle'])
def test_old_placement_effect_cannot_cross_new_guard_or_player_ownership(order,cancel,target,operation):
    f=mounted('oeste');item={'gun':f,'post':f.marker,'standby':f.wait}[target]
    original=getattr(item,operation);observed=[];lease=[]
    def interrupted(*args):
        setattr(item,operation,original)
        if order=='after':original(*args)
        if cancel=='takeover':
            lease.append(f.run('ReservePlayerLease'))
            assert not f.run('PreparePlayerLease',lease[0])
        elif cancel=='load':f.load()
        else:f.run('OnUnload')
        observed.append((f.vm.state['pinBusy'],f.vm.state['sceneBusy'],f.vm.state['playerReady'],f.vm.state['running']))
        if order=='before':original(*args)
    setattr(item,operation,interrupted);f.load()
    assert observed==[(True,True,False,False)]
    assert not f.vm.state['pinBusy'] and not f.vm.state['sceneBusy']
    if cancel=='takeover':
        assert f.run('PreparePlayerLease',lease[0]);assert_placed(f)
        assert f.guard.pos==f.wait.pos and f.guard.pinned
    else:
        f.load();assert_placed(f)
        assert f.vm.state['running'] and f.guard.pinned


def test_pending_native_owner_blocks_all_placement_writes():
    f=mounted('este');f.native_free=False;f.load()
    assert f.placement_moves==[] and not f.vm.state['running']
    lease=f.run('ReservePlayerLease');assert not f.run('PreparePlayerLease',lease)
    assert f.placement_moves==[]
    f.native_free=True;assert f.run('PreparePlayerLease',lease);assert_placed(f)


def test_missing_owned_anchor_fails_closed_without_moving_other_references():
    f=mounted('este')
    f.vm.state['Game'].GetFormFromFile=lambda form,filename:f if form==0xB70 else None
    lease=f.run('ReservePlayerLease')
    assert not f.run('PreparePlayerLease',lease)
    assert f.placement_moves==[] and not f.vm.state['playerReady']
