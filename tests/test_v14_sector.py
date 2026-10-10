"""Measured tower sectors reject unreachable targets instead of clamping them."""
import math
import pytest
from test_v13_guard import GuardFixture

def aimed(yaw):
    f=GuardFixture();f.load();f.vm.state['ProjectileGravity']=0.
    f.enemy.pos=[math.sin(math.radians(yaw))*1600.,-224.-math.cos(math.radians(yaw))*1600.,172.6-60.]
    return f

def test_existing_default_sector_preserved():
    assert GuardFixture().vm.state.get('YawHalfSector')==60.

@pytest.mark.parametrize('angle,accepted',[(0.,True),(19.,True),(-19.,True),(21.,False),(-21.,False),(59.,False)])
def test_measured_narrow_sector(angle,accepted):
    f=aimed(angle);f.vm.state['YawHalfSector']=20.
    assert f.run('SampleTarget',f.enemy,f.vm.state['generation'],f.vm.state['token']) is accepted

@pytest.mark.parametrize('bad',[float('nan'),float('inf'),-1.,0.,61.])
def test_invalid_sector_fails_closed(bad):
    f=aimed(0.);f.vm.state['YawHalfSector']=bad
    assert not f.run('SampleTarget',f.enemy,f.vm.state['generation'],f.vm.state['token'])

@pytest.mark.parametrize('angle,accepted',[(-9.,True),(-1.,True),(-11.,False),(1.,False)])
def test_asymmetric_measured_sector(angle,accepted):
    f=aimed(angle);f.vm.state['YawHalfSector']=5.;f.vm.state['YawCenter']=-5.
    assert f.run('SampleTarget',f.enemy,f.vm.state['generation'],f.vm.state['token']) is accepted

@pytest.mark.parametrize('center',[float('nan'),float('inf'),-56.,56.])
def test_shifted_sector_cannot_exceed_legacy_limits(center):
    f=aimed(0.);f.vm.state['YawHalfSector']=5.;f.vm.state['YawCenter']=center
    assert not f.run('SampleTarget',f.enemy,f.vm.state['generation'],f.vm.state['token'])

@pytest.mark.parametrize('reference_scale',[.75,.85])
def test_scaled_reference_uses_world_muzzle_and_unscaled_rotation(reference_scale):
    f=GuardFixture();f.root_pos=[17801.74,-8324.61,-3616.]
    original=f.read_position
    def scaled_world(ref,node,out,first):
        original(ref,node,out,first)
        if node:out[:]=[f.root_pos[i]+reference_scale*(out[i]-f.root_pos[i]) for i in range(3)]
        return True
    f.vm.state['NetImmerse'].GetNodeWorldPosition=scaled_world
    f.enemy.pos=[f.root_pos[0],f.root_pos[1]-1600.,f.root_pos[2]]
    f.load()
    assert f.run('SampleTarget',f.enemy,f.vm.state['generation'],f.vm.state['token'])
    s=f.vm.state;m=s['muzzlePosition'];v=s['ProjectileSpeed']
    assert m==pytest.approx([f.root_pos[0],f.root_pos[1]-224.*reference_scale,f.root_pos[2]+172.6*reference_scale])
    time=math.hypot(f.enemy.pos[0]-m[0],f.enemy.pos[1]-m[1])/(v*math.hypot(s['aimX'],s['aimY']))
    actual=[m[0]+s['aimX']*v*time,m[1]+s['aimY']*v*time,m[2]+s['aimZ']*v*time-.5*s['ProjectileGravity']*time*time]
    assert actual==pytest.approx([*f.enemy.pos[:2],f.enemy.pos[2]+60.],abs=1e-6)
