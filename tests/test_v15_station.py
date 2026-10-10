"""Execute the real Station/Acti/Guard PSC under specified native interruptions.

The scalar evaluator does not establish Papyrus scheduling or Skyrim latency.
Native effects, scene persistence, city collision and event delivery need game QA.
"""
import re
from pathlib import Path
from types import SimpleNamespace

import pytest

from test_control_lease import SessionSourceEvaluator
from test_v15_takeover import station as guard_station
from tests.test_camera_aim import AimFixture

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "mod/scripts/source/AstraAsedioStation.psc"


class StationFixture:
    def __init__(self):
        assert SOURCE.exists(), "shared station controller is missing"
        self.source = SOURCE.read_text(encoding="utf-8-sig")
        self.vm = SessionSourceEvaluator(self.source)
        self.guard = guard_station()
        self.parent = AimFixture()
        self.player = self.parent.vm.state["player"]
        self.loaded = True
        self.native_free = True
        self.updates = []
        self.hooks = {}
        self.calls = []
        self.coordinator = SimpleNamespace(**{
            name: self.guard_call(name) for name in
            ("ReservePlayerLease", "PreparePlayerLease", "ReleasePlayerLease")
        })
        self.parent.vm.state["UseSightCamera"] = True
        self.parent.self_ref.UseSightCamera = True
        self.parent.vm.state["SKSE"].GetPluginVersion = lambda name: 0x03050040
        self.parent.vm.state["AstraSightNative"] = SimpleNamespace(
            GetAPIVersion=lambda: 4, IsAvailable=lambda: True,
            GetCameraState=self.parent.lease.camera_state,
            IsEffectsQuiescent=self.quiet,
            EndSight=lambda *args: self.boundary("native_end"),
            BeginFastSight=lambda *args: True, IsFastSightReady=lambda *args: True,
            IsSightReady=lambda *args: True, GetFireMode=lambda *args: 0,
            CaptureAim=lambda *args: [0., 0.],
        )
        self.parent.vm.state["Utility"].WaitMenuMode = lambda seconds: None
        self.parent.lease.vm.state["SKSE"] = self.parent.vm.state["SKSE"]
        self.parent.lease.vm.state["AstraSightNative"] = self.parent.vm.state["AstraSightNative"]
        self.parent.lease.vm.state["Utility"].WaitMenuMode = lambda seconds: None
        self.guard.vm.state["AstraSightNative"].IsEffectsQuiescent = self.quiet
        self.parent.vm.native["EndSession"] = lambda: self.run("EndSession")
        self.parent.self_ref.EndSession = lambda: self.run("EndSession")
        self.parent.vm.native["RegisterForSingleUpdate"] = self.updates.append
        self.parent.vm.native["UnregisterForUpdate"] = self.updates.clear
        self.parent.vm.native["RejectActivation"] = lambda reason: self.calls.append(("reject", reason))
        parent_methods = {name: self.parent_call(name) for name in self.parent.vm.bodies}
        self.vm.state.update(
            Self=self.parent.self_ref, Guard=self.coordinator, Parent=SimpleNamespace(**parent_methods),
            Game=self.parent.vm.state["Game"], Utility=self.parent.vm.state["Utility"],
            SKSE=self.parent.vm.state["SKSE"],
            AstraSightNative=self.parent.vm.state["AstraSightNative"],
        )
        self.vm.native.update(Is3DLoaded=lambda: self.loaded, BlockActivation=lambda *args: None,
                              RegisterForSingleUpdate=self.updates.append)

    def boundary(self, name):
        self.calls.append((name,))
        callback = self.hooks.pop(name, None)
        if callback:
            callback()

    def parent_call(self, name):
        def call(*args):
            self.boundary("parent:" + name)
            # A Parent call bypasses the child's override; internal calls dispatch it.
            override = self.parent.vm.native.pop(name, None)
            try:
                result = self.parent.vm.run(name, *args)
                self.boundary("parent:" + name + ":after")
                return result
            finally:
                if override is not None:
                    self.parent.vm.native[name] = override
        return call

    def guard_call(self, name):
        def call(*args):
            self.boundary("guard:" + name)
            result = self.guard.run(name, *args)
            self.boundary("guard:" + name + ":after")
            return result
        return call

    def quiet(self, ref, token):
        self.boundary("quiet:" + str(token))
        return token > 0 or (self.native_free and not self.parent.vm.state["operating"]
                             and not self.parent.vm.state["endingSession"])

    def run(self, name, *args):
        return self.vm.run(name, *args)

    def enter(self):
        self.run("OnActivate", self.player)

    def tick(self, seconds=.05):
        self.parent.vm.now += seconds
        self.run("OnUpdate")


def count(f, name):
    return sum(call[0] == name for call in f.calls)


@pytest.mark.parametrize("effect_order", ["before", "after"])
def test_recovery_move_finishes_before_player_can_take_over(effect_order):
    f = StationFixture()
    f.guard.guard.pos = [900., 900., 0.]
    original = f.guard.guard.MoveTo
    observed = []

    def interrupted(point):
        if point is f.guard.marker:
            if effect_order == "after":
                original(point)
            f.enter()
            observed.append((f.guard.vm.state["pinBusy"],
                             f.guard.vm.state["playerReady"],
                             f.parent.vm.state["operating"]))
            if effect_order == "before":
                original(point)
        else:
            original(point)

    f.guard.guard.MoveTo = interrupted
    f.guard.run("BeginRecovery")
    assert observed == [(True, False, False)]
    assert not f.guard.vm.state["pinBusy"]
    f.tick()
    assert f.parent.vm.state["operating"] and f.guard.vm.state["playerReady"]
    assert f.guard.guard.pinned
    assert f.guard.guard.pos == f.guard.vm.state["Standby"].pos


def test_station_reserves_then_prepares_before_parent_can_disable_controls():
    f = StationFixture()
    f.guard.vm.state["sceneBusy"] = True
    f.enter()
    assert f.guard.vm.state["playerReserved"] and f.parent.lease.calls == []
    assert count(f, "parent:OnActivate") == 0
    f.guard.vm.state["sceneBusy"] = False
    f.tick()
    assert f.parent.vm.state["operating"]
    assert f.calls.index(("guard:PreparePlayerLease:after",)) < f.calls.index(("parent:ResetStationAim",))
    assert f.calls.index(("parent:ResetStationAim",)) < f.calls.index(("parent:OnActivate",))
    assert f.guard.guard.pinned and f.guard.guard.pos == f.guard.vm.state["Standby"].pos


def test_reentrant_activation_and_duplicate_updates_are_single_flight():
    f = StationFixture()
    f.hooks["guard:ReservePlayerLease"] = f.enter
    f.hooks["guard:PreparePlayerLease"] = lambda: (f.enter(), f.tick())
    f.enter()
    assert count(f, "guard:ReservePlayerLease") == 1
    assert count(f, "parent:OnActivate") == 1


def test_parent_end_and_controls_restore_precede_coordinator_release():
    f = StationFixture(); f.enter()
    observed = []
    f.parent.lease.hooks[("enable", "after")] = lambda: observed.append(
        (f.guard.vm.state["playerReserved"], f.parent.vm.state["endingSession"]))
    f.run("EndSession")
    assert observed == [(True, True)]
    assert f.parent.lease.controls == [True] * 8
    assert not f.guard.vm.state["playerReserved"]
    assert count(f, "guard:ReleasePlayerLease") == 1


def test_native_wildcard_barrier_holds_guard_after_parent_cleanup():
    f = StationFixture(); f.enter(); f.native_free = False
    f.run("EndSession")
    assert not f.parent.vm.state["operating"] and not f.parent.vm.state["endingSession"]
    assert f.guard.vm.state["playerReserved"]
    assert count(f, "guard:ReleasePlayerLease") == 0
    f.tick(); assert f.guard.vm.state["playerReserved"]
    f.native_free = True; f.tick()
    assert not f.guard.vm.state["playerReserved"]


@pytest.mark.parametrize("reason", ["timeout", "menu", "dead", "unloaded", "rewind", "invalid_clock"])
def test_failed_wait_never_enters_parent_and_returns_guard(reason):
    f = StationFixture(); f.guard.vm.state["sceneBusy"] = True; f.enter()
    if reason == "timeout": f.parent.vm.now += 10.01
    elif reason == "menu": f.parent.vm.menu = True
    elif reason == "dead": f.parent.lease.dead = True
    elif reason == "unloaded": f.loaded = False
    elif reason == "rewind": f.parent.vm.now = 1.
    else: f.parent.vm.now = float("nan")
    f.guard.vm.state["sceneBusy"] = False
    f.tick()
    assert count(f, "parent:OnActivate") == 0
    assert f.parent.lease.controls == [True] * 8
    assert not f.guard.vm.state["playerReserved"]


@pytest.mark.parametrize("event,args", [("OnUnload", ()), ("OnCellDetach", ()),
    ("OnDestructionStageChanged", (0, 1)), ("OnLoad", ())])
@pytest.mark.parametrize("boundary", ["guard:ReservePlayerLease:after", "guard:PreparePlayerLease:after",
    "parent:ResetStationAim", "parent:OnActivate"])
def test_lifecycle_cancels_suspended_entry_without_disabling_controls(event, args, boundary):
    f = StationFixture()
    f.hooks[boundary] = lambda: f.run(event, *args)
    f.enter()
    assert not f.parent.vm.state["operating"]
    assert f.parent.lease.controls == [True] * 8
    assert not f.guard.vm.state["playerReserved"]
    assert not f.vm.state["stationBusy"]


def test_unload_inside_actual_session_acquire_compensates_disabled_controls():
    f = StationFixture()
    f.parent.lease.hooks[("disable", "before")] = lambda: f.run("OnUnload")
    f.enter()
    assert not f.parent.vm.state["operating"]
    assert f.parent.lease.controls == [True] * 8
    assert not f.guard.vm.state["playerReserved"]


def test_failed_parent_validation_releases_the_reservation():
    f = StationFixture(); f.parent.vm.state["Launcher"] = None; f.enter()
    assert not f.parent.vm.state["operating"]
    assert not f.guard.vm.state["playerReserved"]
    assert f.parent.lease.calls == []


@pytest.mark.parametrize("reason", ["timeout", "menu", "dead", "unloaded"])
def test_prepare_return_revalidates_deadline_and_player_context(reason):
    f = StationFixture()
    def changed():
        if reason == "timeout": f.parent.vm.now += 10.01
        elif reason == "menu": f.parent.vm.menu = True
        elif reason == "dead": f.parent.lease.dead = True
        else: f.loaded = False
    f.hooks["guard:PreparePlayerLease:after"] = changed
    f.enter()
    assert count(f, "parent:OnActivate") == 0
    assert not f.guard.vm.state["playerReserved"]
    assert f.parent.lease.controls == [True] * 8


def test_parent_update_query_holds_single_flight_slot_until_snapshot_returns():
    f = StationFixture(); f.enter()
    f.parent.vm.state["operating"] = False
    def query_returns_late():
        f.run("EndSession")
        f.parent.vm.now += .4
        f.enter()
    f.hooks["parent:IsPlayerOperating:after"] = query_returns_late
    f.tick()
    assert count(f, "guard:ReservePlayerLease") == 1
    assert not f.parent.vm.state["operating"]
    assert not f.guard.vm.state["playerReserved"]


def test_normal_update_delegates_to_actual_parent_while_lease_stays_reserved():
    f = StationFixture(); f.enter(); f.tick()
    assert count(f, "parent:OnUpdate") == 1
    assert f.parent.vm.state["operating"]
    assert not f.parent.vm.state["cameraEntryPending"]
    assert f.guard.vm.state["playerReserved"]


def test_update_delivered_before_entry_stack_returns_does_not_lose_only_tick():
    f = StationFixture()
    def delivered():
        f.updates.clear()  # The scheduled callback is now being delivered.
        f.run("OnUpdate")
    f.hooks["parent:OnActivate:after"] = delivered
    f.enter()
    assert f.parent.vm.state["operating"]
    assert f.updates, "single-flight entry consumed the only parent update"


def test_menu_during_camera_entry_drains_the_actual_parent_and_guard_lease():
    f = StationFixture(); f.enter(); f.parent.vm.menu = True
    f.run("OnMenuOpen", "InventoryMenu")
    assert not f.parent.vm.state["operating"]
    assert f.parent.lease.controls == [True] * 8
    assert not f.guard.vm.state["playerReserved"]


def test_player_alias_emergency_cleanup_reaches_child_release_on_death():
    f = StationFixture(); f.enter(); f.parent.lease.dead = True
    f.parent.lease.vm.run("EmergencyCleanup")
    assert not f.parent.vm.state["operating"]
    assert f.parent.lease.controls == [True] * 8
    assert not f.guard.vm.state["playerReserved"]


def test_onload_recovers_saved_parent_cleanup_without_scene_writes():
    f = StationFixture(); f.enter()
    f.parent.vm.state.update(endingSession=True, operating=False, token=-1)
    f.parent.vm.native["CaptureMatrices"] = lambda: pytest.fail("Station load captured guard pose")
    f.parent.vm.native["ApplyAim"] = lambda: pytest.fail("Station load wrote guard pose")
    f.run("OnLoad")
    assert not f.parent.vm.state["endingSession"]
    assert f.parent.lease.controls == [True] * 8
    assert not f.guard.vm.state["playerReserved"]
    assert count(f, "parent:NormalizeTimingProperties") == 1


def test_load_recovery_cannot_accept_a_reentrant_activation():
    f = StationFixture()
    f.hooks["parent:RecoverStationLoad"] = f.enter
    f.run("OnLoad")
    assert count(f, "guard:ReservePlayerLease") == 0
    assert not f.vm.state["stationBusy"]


def test_load_preserves_suspended_entry_slot_until_matching_stack_returns():
    f = StationFixture(); f.guard.vm.state["sceneBusy"] = True; f.enter()
    saved_revision = f.vm.state["stationRevision"]
    f.vm.state.update(stationBusy=True, stationBusyRevision=saved_revision)
    f.run("OnLoad")
    assert f.vm.state["stationBusy"] and f.guard.vm.state["playerReserved"]
    assert not f.run("StationCurrent", saved_revision, f.coordinator, f.vm.state["stationLease"])
    f.run("FinishStationCall", saved_revision)
    f.guard.vm.state["sceneBusy"] = False
    f.tick()
    assert not f.guard.vm.state["playerReserved"] and not f.vm.state["stationBusy"]


def test_property_change_cannot_redirect_release_to_another_coordinator():
    f = StationFixture(); f.enter()
    other = SimpleNamespace(ReleasePlayerLease=lambda lease: pytest.fail("released replacement guard"))
    f.vm.state["Guard"] = other
    f.run("EndSession")
    assert not f.guard.vm.state["playerReserved"]


def test_old_station_release_cannot_unpin_new_guard_lease_after_guard_load():
    f = StationFixture(); f.enter()
    old = f.vm.state["stationLease"]
    f.guard.load()
    newer = f.guard.run("ReservePlayerLease")
    assert newer > old
    f.hooks["guard:ReleasePlayerLease"] = lambda: f.guard.run("PreparePlayerLease", newer)
    f.run("EndSession")
    assert f.guard.vm.state["playerLease"] == newer
    assert f.guard.vm.state["playerReady"] and f.guard.guard.pinned
    assert f.guard.guard.pos == f.guard.vm.state["Standby"].pos


@pytest.mark.parametrize("failure", ["skse", "plugin", "api", "unavailable"])
def test_native_prerequisite_failure_never_reserves_guard_or_controls(failure):
    f = StationFixture()
    if failure == "skse": f.parent.vm.state["SKSE"].GetVersion = lambda: 1
    elif failure == "plugin": f.parent.vm.state["SKSE"].GetPluginVersion = lambda name: 0x03040000
    elif failure == "api": f.vm.state["AstraSightNative"].GetAPIVersion = lambda: 3
    else: f.vm.state["AstraSightNative"].IsAvailable = lambda: False
    f.enter()
    assert count(f, "guard:ReservePlayerLease") == 0
    assert count(f, "quiet:0") == 0
    assert not f.parent.lease.calls
    assert count(f, "parent:RejectActivation") == 1


def test_reentrant_release_cannot_enter_new_owner_before_old_recovery_returns():
    f = StationFixture(); f.enter()
    f.hooks["guard:ReleasePlayerLease"] = f.enter
    f.run("EndSession")
    assert count(f, "guard:ReservePlayerLease") == 1
    f.parent.vm.now += .4; f.enter()
    assert count(f, "guard:ReservePlayerLease") == 2
    assert f.parent.vm.state["operating"]


def test_release_query_callback_invalidates_old_revision_before_guard_release():
    f = StationFixture(); f.enter(); f.native_free = False; f.run("EndSession")
    f.native_free = True
    f.hooks["quiet:0"] = lambda: f.run("OnUnload")
    f.tick()
    assert f.guard.vm.state["playerReserved"]
    assert count(f, "guard:ReleasePlayerLease") == 0
    f.tick(); assert not f.guard.vm.state["playerReserved"]


def test_nonplayer_and_missing_guard_never_acquire_controls():
    f = StationFixture(); f.run("OnActivate", object())
    assert count(f, "guard:ReservePlayerLease") == 0
    f.vm.state["Guard"] = None; f.enter()
    assert not f.parent.vm.state["operating"] and not f.parent.lease.calls


def test_lifecycle_source_never_calls_parent_load_or_writes_shared_scene():
    f = StationFixture()
    assert re.search(r"Scriptname AstraAsedioStation extends AstraAsedioActi", f.source)
    assert "AstraAsedioGuard Property Guard Auto" in f.source
    assert "Parent.OnLoad(" not in f.source
    assert not re.search(r"(?:CaptureMatrices|ApplyAim|SetNode\w*|MoveTo|SetDontMove)\(", f.source)
    assert "RecoverStationLoad" in f.parent.vm.bodies
    helper = f.parent.vm.bodies["RecoverStationLoad"][1]
    assert "EmergencyCleanup" in helper
    assert "CaptureMatrices" not in helper and "ApplyAim" not in helper
