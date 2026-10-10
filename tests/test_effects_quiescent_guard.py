"""IsEffectsQuiescent exists only on AstraSight 3.5.0 or newer.

The expected maps are handwritten. A new call site has to be added here on
purpose: either it stays behind GetPluginVersion("AstraSight") compared with
50659328, or a missing/older DLL loops the caller. A wait on a live native
also needs the 5s clock and the 500-poll cap. Deriving the maps from the
tree would stay green when the next call forgets the gate.
"""
import re
from pathlib import Path
from types import SimpleNamespace

from test_control_lease import NativeControlFixture, SOURCE
from test_v15_station import StationFixture
from test_v15_takeover import station
from test_v17_city_upgrade import alias
from tests.test_camera_aim import AimFixture

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "mod" / "scripts" / "source"
EFFECTS_VERSION = 0x03050000

# Counts, not names alone. A second call in a function already listed is the
# likely next hole, and a set of function names would let it through.
QUIESCENT_CALLS = {
    "AstraAsedioActi.psc": {"EndSession": 2},
    "AstraAsedioGuard.psc": {"StationSceneAvailable": 1},
    "AstraAsedioPlayerAlias.psc": {"RetireLegacyCity": 1},
    "AstraAsedioSession.psc": {"RestoreControls": 2},
    "AstraAsedioStation.psc": {"PollStationRelease": 1},
}
# The second Acti/Session call is the sample after WaitMenuMode, inside the
# same gate and the same spin cap. It is not a second wait.
BOUNDED_WAITS = {
    "AstraAsedioActi.psc": {"EndSession": 1},
    "AstraAsedioSession.psc": {"RestoreControls": 1},
}
FUNCTION = re.compile(
    r"^(?:bool |int |float |string )?(?:Function|Event) (\w+)\(([^\n]*)\)\n(.*?)^End(?:Function|Event)",
    re.M | re.S,
)


def functions(path):
    text = path.read_text(encoding="utf-8-sig")
    return {name: body for name, _params, body in FUNCTION.findall(text)}


def while_loops(body):
    """Papyrus loops only. A nearby while that does not call the native is not a wait."""
    lines = body.splitlines()
    loops = []
    index = 0
    while index < len(lines):
        if lines[index].strip().startswith("while "):
            start = index
            depth = 1
            index += 1
            while depth and index < len(lines):
                nxt = lines[index].strip()
                depth += nxt.startswith("while ") - (nxt == "endwhile")
                index += 1
            loops.append("\n".join(lines[start:index]))
            continue
        index += 1
    return loops


def test_effects_query_version_packs_as_3_5_0():
    assert EFFECTS_VERSION == 50659328


def test_every_effects_query_is_behind_the_3_5_0_gate():
    found = {}
    for path in sorted(SCRIPTS.glob("*.psc")):
        counts = {}
        for name, body in functions(path).items():
            count = body.count("AstraSightNative.IsEffectsQuiescent")
            if not count:
                continue
            start = 0
            seen = 0
            while True:
                call = body.find("AstraSightNative.IsEffectsQuiescent", start)
                if call < 0:
                    break
                assert body.rfind("50659328", 0, call) != -1, path.name + " " + name
                assert body.rfind('GetPluginVersion("AstraSight")', 0, call) != -1, path.name + " " + name
                seen += 1
                start = call + 1
            assert seen == count
            counts[name] = count
        if counts:
            found[path.name] = counts
    assert found == QUIESCENT_CALLS


def test_every_effects_wait_has_a_five_second_and_spin_bound():
    found = {}
    for path in sorted(SCRIPTS.glob("*.psc")):
        counts = {}
        for name, body in functions(path).items():
            waits = [loop for loop in while_loops(body) if "IsEffectsQuiescent" in loop]
            if not waits:
                continue
            for loop in waits:
                assert "spins < 500" in loop, name
                assert "started + 5.0" in loop, name
            counts[name] = len(waits)
        if counts:
            found[path.name] = counts
    assert found == BOUNDED_WAITS


def test_station_release_poll_is_bounded_without_a_busy_wait():
    body = functions(SCRIPTS / "AstraAsedioStation.psc")["PollStationRelease"]
    assert [loop for loop in while_loops(body) if "IsEffectsQuiescent" in loop] == []
    assert "stationReleaseDeadline" in body
    assert "now + 5.0" in body
    assert "50659328" in body


def _unbound(*_args):
    raise AssertionError("unregistered IsEffectsQuiescent")


def test_old_dll_starts_the_guard_without_querying_effects():
    gun = station()
    gun.vm.state["SKSE"].GetPluginVersion = lambda name: EFFECTS_VERSION - 1
    gun.vm.state["AstraSightNative"].IsEffectsQuiescent = _unbound
    gun.load()
    assert gun.vm.state["running"]
    assert not gun.vm.state["recoveryRequested"]


def test_exact_3_5_0_still_defers_recovery_while_effects_are_live():
    gun = station()
    gun.native_free = False
    gun.vm.state["SKSE"].GetPluginVersion = lambda name: EFFECTS_VERSION
    seen = []
    gun.vm.state["AstraSightNative"].IsEffectsQuiescent = lambda *args: seen.append(args) or False
    gun.load()
    assert seen
    assert not gun.vm.state["running"]
    assert gun.vm.state["recoveryRequested"]
    assert 0.2 in gun.updates


def test_player_prepare_on_an_old_dll_does_not_call_the_unregistered_query():
    gun = station()
    gun.vm.state["SKSE"].GetPluginVersion = lambda name: -1
    gun.vm.state["AstraSightNative"].IsEffectsQuiescent = _unbound
    lease = gun.run("ReservePlayerLease")
    assert lease > 0
    assert gun.run("PreparePlayerLease", lease) is False


def test_missing_dll_retires_a_legacy_city_without_the_effects_query():
    vm, refs = alias()
    seen = []
    vm.state["SKSE"].GetPluginVersion = lambda name: -1
    vm.state["AstraSightNative"].IsEffectsQuiescent = lambda *args: seen.append(args) or False
    legacy = refs[0xB40]
    legacy.quiet = False
    assert vm.run("RetireLegacyCity", 0xB40, 0xB70) is True
    assert seen == []
    assert legacy.retired
    assert all(refs[form_id].disabled for form_id in range(0xB40, 0xB45))


def test_exact_3_5_0_still_waits_to_retire_a_live_legacy_city():
    vm, refs = alias()
    vm.state["SKSE"].GetPluginVersion = lambda name: EFFECTS_VERSION
    legacy = refs[0xB40]
    legacy.quiet = False
    assert vm.run("RetireLegacyCity", 0xB40, 0xB70) is False
    assert not legacy.retired
    assert not any(refs[form_id].disabled for form_id in range(0xB40, 0xB45))


def test_saved_release_without_the_dll_returns_the_lease():
    placed = StationFixture()
    placed.enter()
    assert placed.guard.vm.state["playerReserved"]
    placed.parent.vm.state["SKSE"].GetPluginVersion = lambda name: -1
    placed.vm.state["AstraSightNative"].IsEffectsQuiescent = _unbound
    placed.run("EndSession")
    assert not placed.guard.vm.state["playerReserved"]


def test_release_poll_waits_five_seconds_then_returns_a_live_lease():
    placed = StationFixture()
    placed.enter()
    placed.native_free = False
    traces = []
    placed.vm.state["Debug"] = SimpleNamespace(Trace=lambda message: traces.append(message))
    placed.run("EndSession")
    assert placed.guard.vm.state["playerReserved"]
    deadline = placed.vm.state["stationReleaseDeadline"]
    assert deadline == placed.parent.vm.now + 5.0
    placed.parent.vm.now = deadline
    placed.run("OnUpdate")
    assert placed.guard.vm.state["playerReserved"]
    assert traces == []
    placed.parent.vm.now = deadline + 0.01
    placed.run("OnUpdate")
    assert not placed.guard.vm.state["playerReserved"]
    assert traces and "timed out" in traces[-1]


def test_release_poll_returns_the_lease_when_the_clock_restarts_or_is_nan():
    placed = StationFixture()
    placed.enter()
    placed.native_free = False
    placed.run("EndSession")
    assert placed.vm.state["stationReleaseStarted"] == 10.0
    placed.parent.vm.now = 0.0
    placed.run("OnUpdate")
    assert not placed.guard.vm.state["playerReserved"]

    placed = StationFixture()
    placed.enter()
    placed.native_free = False
    placed.parent.vm.now = float("nan")
    placed.run("EndSession")
    assert not placed.guard.vm.state["playerReserved"]


def _aim_that_never_settles(advance):
    fixture = AimFixture()
    fixture.vm.state["UseSightCamera"] = True
    fixture.self_ref.UseSightCamera = True
    fixture.active()
    waits = []
    fixture.vm.state["AstraSightNative"].EndSight = lambda *_args: True
    fixture.vm.state["AstraSightNative"].IsEffectsQuiescent = lambda *_args: False

    def wait(seconds):
        waits.append(seconds)
        advance(fixture)

    fixture.vm.state["Utility"].WaitMenuMode = wait
    fixture.vm.run("EndSession")
    assert fixture.vm.state["endingSession"] is False
    assert fixture.vm.state["operating"] is False
    assert fixture.lease.controls[:3] == [True, True, True]
    return waits


def test_end_session_continues_when_the_effects_clock_expires():
    def advance(fixture):
        fixture.vm.now += 5.0

    assert _aim_that_never_settles(advance) == [0.01]


def test_end_session_stops_after_500_polls_when_the_clock_is_frozen():
    assert len(_aim_that_never_settles(lambda _fixture: None)) == 500


def _session_that_never_settles(advance):
    fixture = NativeControlFixture(SOURCE.read_text(encoding="utf-8-sig"))
    gun = fixture.gun()
    gun.UseSightCamera = True
    clock = {"t": 3.0}
    waits = []
    fixture.vm.state["SKSE"].GetPluginVersion = lambda name: EFFECTS_VERSION
    fixture.vm.state["Utility"].GetCurrentRealTime = lambda: clock["t"]
    fixture.vm.state["AstraSightNative"].EndSight = lambda *_args: None
    fixture.vm.state["AstraSightNative"].IsEffectsQuiescent = lambda *_args: False

    def wait(seconds):
        waits.append(seconds)
        advance(clock)

    fixture.vm.state["Utility"].WaitMenuMode = wait
    token = fixture.vm.run("Acquire", gun)
    assert token > 0
    fixture.vm.run("Release", gun, token)
    assert fixture.vm.state["releasing"] is False
    assert fixture.controls[:3] == [True, True, True]
    return waits


def test_session_release_continues_when_the_effects_clock_expires():
    assert _session_that_never_settles(lambda clock: clock.__setitem__("t", clock["t"] + 5.0)) == [0.01]


def test_session_release_stops_after_500_polls_when_the_clock_is_frozen():
    assert len(_session_that_never_settles(lambda _clock: None)) == 500
