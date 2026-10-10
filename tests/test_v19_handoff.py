"""Guard handoff effects from the actual PSC; not Skyrim rendering emulation."""
from test_v15_takeover import station
import pytest


def test_handoff_restores_pose_without_replaying_legacy_animation():
    f=station()
    f.native_resets=[]
    f.vm.state['AstraSightNative'].ResetIdleScene=lambda ref: f.native_resets.append(ref) or True
    f.vm.state['SKSE'].GetPluginVersion=lambda name: 0x03050040
    # The existing native sight already controls these sequences directly.
    # Handoff must not start a second full Reset through the legacy ref API.
    before=len(f.animations)
    lease=f.run('ReservePlayerLease')
    assert f.run('PreparePlayerLease',lease)
    assert len(f.animations)==before, 'Handoff still restarts a legacy Reset'
    assert f.native_resets and f.vm.state['playerReady']


def test_pending_native_reset_cannot_mark_player_ready_or_move_guard():
    f=station()
    f.vm.state['SKSE'].GetPluginVersion=lambda name: 0x03050040
    f.vm.state['AstraSightNative'].ResetIdleScene=lambda ref: False
    lease=f.run('ReservePlayerLease');before=len(f.guard.moves)
    assert not f.run('PreparePlayerLease',lease)
    assert not f.vm.state['playerReady'] and len(f.guard.moves)==before
    f.vm.state['AstraSightNative'].ResetIdleScene=lambda ref: True
    assert f.run('PreparePlayerLease',lease)


def test_cancel_during_native_reset_cannot_finish_old_handoff():
    f=station()
    f.vm.state['SKSE'].GetPluginVersion=lambda name: 0x03050040
    lease=f.run('ReservePlayerLease');before=len(f.guard.moves)
    def cancelled(ref):
        f.run('OnUnload')
        return True
    f.vm.state['AstraSightNative'].ResetIdleScene=cancelled
    assert not f.run('PreparePlayerLease',lease)
    assert not f.vm.state['playerReady'] and len(f.guard.moves)==before


def test_old_dll_never_calls_unbound_idle_reset():
    f=station();f.vm.state['SKSE'].GetPluginVersion=lambda name: 0x03050030
    def unbound(ref):
        raise AssertionError('Old DLL has no ResetIdleScene binding')
    f.vm.state['AstraSightNative'].ResetIdleScene=unbound
    lease=f.run('ReservePlayerLease')
    assert not f.run('PreparePlayerLease',lease)


def test_pending_guard_launch_drains_before_player_handoff():
    f=station();lease=[];observed=[]
    for _ in range(30):
        f.tick(.2)
        if f.vm.state['phase']==1:break
    assert f.vm.state['phase']==1
    def pending_fire(ref,ammo):
        lease.append(f.run('ReservePlayerLease'))
        observed.append(f.run('PreparePlayerLease',lease[0]))
        f.fire(ref,ammo)
    f.vm.state['Launcher'].Fire=pending_fire
    f.tick(.2)
    assert observed==[False], 'Player became ready before the previous guard Fire returned'
    assert len(f.shots)==1 and not f.vm.state['sceneBusy']
    assert f.run('PreparePlayerLease',lease[0])


@pytest.mark.parametrize('event', ['OnLoad', 'OnUnload'])
def test_load_interruption_during_guard_fire_does_not_reuse_old_lease(event):
    f=station();leases=[];ready=[]
    for _ in range(30):
        f.tick(.2)
        if f.vm.state['phase']==1:break
    assert f.vm.state['phase']==1
    def interrupted_fire(ref,ammo):
        leases.append(f.run('ReservePlayerLease'))
        f.run(event)
        ready.append(f.run('PreparePlayerLease',leases[0]))
        f.fire(ref,ammo)
    f.vm.state['Launcher'].Fire=interrupted_fire
    f.tick(.2)
    assert ready==[False] and not f.vm.state['playerReady']
    assert not f.vm.state['sceneBusy']
    assert not f.run('PreparePlayerLease',leases[0])
    assert not f.run('ReleasePlayerLease',leases[0])
