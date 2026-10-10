"""Exercise the actual guard PSC handoff; source fixtures do not emulate Skyrim."""
import pytest
from types import SimpleNamespace
from test_v13_guard import GuardFixture, ActorFixture, rotation_z


def station():
    f = GuardFixture()
    assert "ReservePlayerLease" in f.vm.bodies, "city guard lacks player takeover"
    f.vm.state.update({"AllowPlayerTakeover": True,
                       "Standby": ActorFixture((180., 260., 0.))})
    f.native_free = True
    f.vm.state["AstraSightNative"] = SimpleNamespace(IsEffectsQuiescent=lambda *args: f.native_free,
                                                   ResetIdleScene=lambda *args: f.native_free)
    f.vm.state["SKSE"].GetPluginVersion = lambda name: 0x03050040
    f.load()
    return f


def test_city_certified_pitch_range_accepts_ground_targets():
    f=station();f.vm.state['PitchMax']=80.0
    lease=f.run('ReservePlayerLease');assert f.run('PreparePlayerLease',lease)
    f.run('ReleasePlayerLease',lease);f.tick(.2)
    assert f.run('SampleTarget',f.enemy,f.vm.state['generation'],f.vm.state['token'])


def test_reservation_invalidates_guard_before_player_pose():
    f = station()
    old_generation, old_token = f.vm.state["generation"], f.vm.state["token"]
    lease = f.run("ReservePlayerLease")
    assert lease > 0
    assert not f.run("Current", old_generation, old_token)
    assert not f.vm.state["running"]
    assert f.run("PreparePlayerLease", lease)
    assert f.guard.pos == f.vm.state["Standby"].pos
    assert f.guard.pinned
    for _ in range(5):
        f.tick(1.)
    assert f.shots == []


@pytest.mark.parametrize("slot", ["pinBusy", "sceneBusy"])
def test_player_waits_for_guard_inflight_effect(slot):
    f = station()
    f.vm.state[slot] = True
    lease = f.run("ReservePlayerLease")
    before_moves = len(f.guard.moves)
    assert not f.run("PreparePlayerLease", lease)
    assert len(f.guard.moves) == before_moves
    f.vm.state[slot] = False
    assert f.run("PreparePlayerLease", lease)


def test_second_reservation_cannot_overtake_first():
    f = station()
    lease = f.run("ReservePlayerLease")
    assert f.run("ReservePlayerLease") < 0
    assert not f.run("ReleasePlayerLease", lease + 1)
    assert f.run("PreparePlayerLease", lease)


def test_release_returns_guard_and_late_release_cannot_unpin_new_lease():
    f = station()
    lease = f.run("ReservePlayerLease")
    assert f.run("PreparePlayerLease", lease)
    assert f.run("ReleasePlayerLease", lease)
    assert f.guard.pos == f.marker.pos
    assert f.guard.pinned and f.vm.state["running"]
    newer = f.run("ReservePlayerLease")
    assert newer > lease and f.run("PreparePlayerLease", newer)
    assert not f.run("ReleasePlayerLease", lease)
    assert f.guard.pinned and f.guard.pos == f.vm.state["Standby"].pos


def test_takeover_resets_shared_controls_to_known_rest():
    f = station()
    f.node_local["CTRL_GIRO_360"] = rotation_z(30)
    f.node_local["CTRL_ELEVACION"] = rotation_z(12)
    lease = f.run("ReservePlayerLease")
    assert f.run("PreparePlayerLease", lease)
    assert f.node_local["CTRL_GIRO_360"] == rotation_z(0)
    assert f.node_local["CTRL_ELEVACION"] == rotation_z(0)


@pytest.mark.parametrize("failure", ["dead", "disabled", "missing"])
def test_dead_or_missing_guard_does_not_block_player(failure):
    f = station()
    f.run("Shutdown")
    if failure == "missing":
        f.vm.state["Artillero"] = None
    else:
        setattr(f.guard, failure, True)
    lease = f.run("ReservePlayerLease")
    assert lease > 0 and f.run("PreparePlayerLease", lease)
    assert not f.guard.pinned


def test_disabled_takeover_preserves_old_guard_only_station():
    f = station()
    f.vm.state["AllowPlayerTakeover"] = False
    assert f.run("ReservePlayerLease") < 0
    assert f.vm.state["running"] and f.guard.pinned


def test_reload_invalidates_saved_player_reservation():
    f = station()
    lease = f.run("ReservePlayerLease")
    assert f.run("PreparePlayerLease", lease)
    f.load()
    assert not f.run("ReleasePlayerLease", lease)
    assert f.vm.state["running"] and f.guard.pos == f.marker.pos


def test_missing_standby_rejects_without_stopping_guard():
    f = station()
    f.vm.state["Standby"] = None
    assert f.run("ReservePlayerLease") < 0
    assert f.guard.pinned and f.vm.state["running"]


def test_cancel_during_standby_pin_compensates_before_recovery():
    f = station()
    lease = f.run("ReservePlayerLease")
    original = f.guard.SetDontMove
    def interrupted(value=True):
        original(value)
        if value and f.vm.state["playerReserved"]:
            f.run("ReleasePlayerLease", lease)
    f.guard.SetDontMove = interrupted
    assert not f.run("PreparePlayerLease", lease)
    f.guard.SetDontMove = original
    f.tick()
    assert f.vm.state["running"] and f.guard.pos == f.marker.pos
    assert f.guard.pinned


def test_player_actor_can_never_be_moved_as_guard():
    f = station()
    f.vm.state["Artillero"] = f.player
    assert f.run("ReservePlayerLease") < 0
    assert f.player.moves == [] and not f.player.pinned


def test_native_owner_or_cleanup_defers_guard_load_recovery():
    f = station()
    f.native_free = False
    moves, animations = len(f.guard.moves), len(f.animations)
    f.load()
    assert not f.vm.state["running"]
    assert len(f.guard.moves) == moves and len(f.animations) == animations
    f.native_free = True
    f.tick()
    assert f.vm.state["running"] and f.guard.pinned


def test_native_owner_blocks_even_old_scene_compensation():
    f = station()
    f.native_free = False
    animations = len(f.animations)
    f.run("Shutdown")
    assert len(f.animations) == animations


def test_player_preparation_waits_for_previous_native_cleanup():
    f = station()
    lease = f.run("ReservePlayerLease")
    f.native_free = False
    assert not f.run("PreparePlayerLease", lease)
    f.native_free = True
    assert f.run("PreparePlayerLease", lease)


@pytest.mark.parametrize("effect_order", ["before", "after"])
def test_reload_defers_new_recovery_until_old_move_returns(effect_order):
    f = station()
    f.guard.pos = [900., 900., 0.]
    original = f.guard.MoveTo
    observed = []

    def interrupted(point):
        f.guard.MoveTo = original
        if effect_order == "after":
            original(point)
        f.load()
        observed.append((f.vm.state["pinBusy"], f.vm.state["running"],
                         f.vm.state["recoveryRequested"]))
        if effect_order == "before":
            original(point)

    f.guard.MoveTo = interrupted
    f.run("BeginRecovery")
    assert observed == [(True, False, True)]
    assert not f.vm.state["pinBusy"]
    f.guard.MoveTo = original
    f.tick()
    assert f.vm.state["running"] and f.guard.pinned
    assert f.guard.pos == f.marker.pos
