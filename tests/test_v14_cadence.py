"""v14 cadence: evaluate actual PSC branches, never claim engine timing.

The fixtures execute controller source with explicit native delays. Papyrus
scheduling, TickSeconds preparation, rendering and damage still need game QA.
"""
import importlib.util
import json
import math
from pathlib import Path
import struct
import sys

import pytest

from tests.test_native_sight import NativeSightFixture
from test_v13_guard import GuardFixture

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.with_name("Ballesta_Astra_Vanilla_SE_v13")
sys.path.insert(0, str(ROOT / "scripts"))
from retime_v07 import retime, transform_times, nif_nodos

PLAYER_NAMES = ("FireSeconds", "ReleaseSeconds", "ResetSeconds", "CycleSeconds")
PLAYER_TIMES = (.2, 1 / 15, .8, 1.)
GUARD_NAMES = ("FireSeconds", "ReleaseSeconds", "ResetSeconds", "CadenceSeconds")
GUARD_TIMES = (.2, 1 / 15, .8, 2.5)


def player():
    f = NativeSightFixture()
    f.active()
    f.vm.state["AstraSightNative"].ValidateShot = lambda *args: True
    return f


def values(f, names):
    return [f.vm.state[name] for name in names]


def test_configuration_and_source_defaults_agree_on_moderate_cadence():
    cfg = json.loads((ROOT / "config.json").read_text())
    assert [cfg[k] for k in ("fire_seconds", "release_seconds", "reset_seconds", "cycle_seconds")] == pytest.approx(PLAYER_TIMES)
    assert values(player(), PLAYER_NAMES) == pytest.approx(PLAYER_TIMES, abs=1e-7)
    assert values(GuardFixture(), GUARD_NAMES) == pytest.approx(GUARD_TIMES, abs=1e-7)


@pytest.mark.parametrize("controller", ["player", "guard"])
def test_saved_v13_defaults_migrate_idempotently_on_load(controller):
    f = player() if controller == "player" else GuardFixture()
    names = PLAYER_NAMES if controller == "player" else GUARD_NAMES
    old = (.3000000119, .1000000015, 1.2000000477, 1.5 if controller == "player" else 4.)
    f.vm.state.update(dict(zip(names, old)))
    f.vm.run("OnLoad")
    assert values(f, names) == pytest.approx(PLAYER_TIMES if controller == "player" else GUARD_TIMES, abs=1e-7)
    first = values(f, names)
    f.vm.run("OnLoad")
    assert values(f, names) == first
    if controller == "player":
        assert f.vm.state["PitchMin"] == -20.


@pytest.mark.parametrize("controller", ["player", "guard"])
def test_valid_custom_timing_is_preserved_and_recovery_uses_custom_cadence(controller):
    f = player() if controller == "player" else GuardFixture()
    names = PLAYER_NAMES if controller == "player" else GUARD_NAMES
    custom = (.4, .15, 1.1, 1.75 if controller == "player" else 6.)
    f.vm.state.update(dict(zip(names, custom)))
    f.vm.run("OnLoad")
    assert values(f, names) == list(custom)
    if controller == "guard":
        assert f.vm.state["nextShotAt"] == pytest.approx(f.time + 6.)


@pytest.mark.parametrize("controller", ["player", "guard"])
@pytest.mark.parametrize("invalid", [float("nan"), float("inf"), -1., 0., 1000.])
def test_invalid_saved_timing_is_bounded_before_new_cycle(controller, invalid):
    f = player() if controller == "player" else GuardFixture()
    names = PLAYER_NAMES if controller == "player" else GUARD_NAMES
    f.vm.state.update(dict.fromkeys(names, invalid))
    f.vm.run("OnLoad")
    assert values(f, names) == pytest.approx(PLAYER_TIMES if controller == "player" else GUARD_TIMES, abs=1e-7)
    assert all(math.isfinite(v) for v in values(f, names))


def test_player_request_normalizes_timings_before_preparing_a_new_cycle():
    f = player()
    f.vm.state.update(dict(zip(PLAYER_NAMES, (.3, .1, 1.2, 1.5))))
    f.vm.run("RequestShot")
    assert f.vm.state["phase"] == 1
    assert values(f, PLAYER_NAMES) == pytest.approx(PLAYER_TIMES, abs=1e-7)


def test_incompatible_player_release_and_cycle_are_repaired_without_erasing_custom_fire_reset():
    f = player()
    f.vm.state.update(FireSeconds=.4, ReleaseSeconds=.5, ResetSeconds=1.1, CycleSeconds=1.)
    f.vm.run("OnLoad")
    assert values(f, PLAYER_NAMES) == pytest.approx((.4, 1 / 15, 1.1, 1.5), abs=1e-7)


@pytest.mark.parametrize("controller", ["player", "guard"])
def test_migration_does_not_rewrite_deliberately_restored_legacy_custom_values(controller):
    f = player() if controller == "player" else GuardFixture()
    names = PLAYER_NAMES if controller == "player" else GUARD_NAMES
    f.vm.run("OnLoad")
    custom = (.3, .1, 1.2, 1.5 if controller == "player" else 4.)
    f.vm.state.update(dict(zip(names, custom)))
    f.vm.run("OnLoad")
    assert values(f, names) == list(custom)


def test_guard_release_cannot_outlast_its_fire_animation():
    f = GuardFixture(); f.vm.state.update(FireSeconds=.4, ReleaseSeconds=.5, ResetSeconds=1.1)
    f.load()
    assert values(f, GUARD_NAMES) == pytest.approx((.4, 1 / 15, 1.1, 2.5), abs=1e-7)


def test_saved_player_shot_callback_cannot_launch_after_load_migration():
    f = player(); f.vm.run("RequestShot")
    f.vm.now += .05; f.vm.run("OnUpdate")
    old = (f.vm.state["generation"], f.vm.state["token"])
    assert f.vm.state["phase"] == 2
    f.vm.state.update(dict(zip(PLAYER_NAMES, (.3, .1, 1.2, 1.5))))
    f.vm.state["timingRevision"] = 0  # Restored v13 has no v14 migration marker.
    f.vm.run("OnLoad")
    assert (f.vm.state["generation"], f.vm.state["token"]) != old
    f.vm.run("CommitShot", old[0]); f.vm.run("OnUpdate")
    assert f.launches == 0
    assert values(f, PLAYER_NAMES) == pytest.approx(PLAYER_TIMES, abs=1e-7)


def test_player_nominal_one_second_cycle_includes_a_preparation_tick():
    f = player(); f.vm.state.update(ContinuousFire=True, repeatFire=True)
    launched = []
    f.vm.state["Launcher"].Fire = lambda *args: launched.append(f.vm.now)
    f.vm.run("RequestShot")
    for _ in range(80):
        f.vm.now += .05; f.vm.run("OnUpdate")
        if len(launched) == 2: break
    assert len(launched) == 2
    interval = launched[1] - launched[0]
    assert 1.05 - 1e-9 <= interval <= 1.2 + 1e-9


def test_player_valid_custom_cycle_is_respected_in_continuous_fire():
    f = player(); f.vm.run("OnLoad"); f.active()
    f.vm.state.update(FireSeconds=.4, ReleaseSeconds=.15, ResetSeconds=1.1,
                      CycleSeconds=1.75, ContinuousFire=True, repeatFire=True)
    launched = []
    f.vm.state["Launcher"].Fire = lambda *args: launched.append(f.vm.now)
    f.vm.run("RequestShot")
    for _ in range(100):
        f.vm.now += .05; f.vm.run("OnUpdate")
        if len(launched) == 2: break
    assert len(launched) == 2
    assert 1.8 - 1e-9 <= launched[1] - launched[0] <= 1.95


def test_guard_recovery_waits_validated_two_and_a_half_seconds():
    f = GuardFixture(); f.load()
    assert f.vm.state["nextShotAt"] == pytest.approx(f.time + 2.5)
    for _ in range(12): f.tick(.2)
    assert not f.shots and f.vm.state["phase"] == 0
    f.tick(f.vm.state["nextShotAt"] - f.time + .00001)
    assert f.vm.state["phase"] == 1
    f.tick(1 / 15 + .00001); assert len(f.shots) == 1


def test_guard_nominal_launch_interval_is_moderate():
    f = GuardFixture(); f.acquire_and_aim(); f.tick(.1)
    for _ in range(70):
        f.tick(.1)
        if len(f.shots) == 2: break
    assert len(f.shots) == 2
    assert 2.5 - 1e-9 <= f.shots[1][0] - f.shots[0][0] <= 2.8


@pytest.mark.parametrize("preflight_delay,fire_delay", [(2., 0.), (0., 3.), (2., 3.)])
def test_guard_cadence_includes_final_preflight_and_weapon_fire_delays(preflight_delay, fire_delay):
    f = GuardFixture(); f.acquire_and_aim()
    if preflight_delay:
        f.hooks["rotation"] = lambda: setattr(f, "time", f.time + preflight_delay)
    returns = []
    def delayed_fire(ref, ammo):
        f.shots.append((f.time, ref, ammo))
        if len(f.shots) == 1: f.time += fire_delay
        returns.append(f.time)
    f.vm.state["Launcher"].Fire = delayed_fire
    f.tick(.1)
    assert len(f.shots) == 1
    assert f.vm.state["nextShotAt"] >= returns[0] + 2.5 - 1e-9
    for _ in range(100):
        f.tick(.1)
        if len(f.shots) == 2: break
    assert len(f.shots) == 2
    assert f.shots[1][0] - f.shots[0][0] >= 2.5 - 1e-9
    assert f.shots[1][0] - returns[0] >= 2.5 - 1e-9


@pytest.mark.parametrize("slot", ["pinBusy", "sceneBusy", "updating", "recovering"])
def test_guard_busy_slots_do_not_schedule_a_fast_loop(slot):
    f = GuardFixture(); f.load(); f.updates.clear()
    f.vm.state[slot] = True
    for _ in range(10): f.tick(.01)
    assert not f.shots and not f.updates


@pytest.mark.parametrize("clock", [float("nan"), float("inf"), -1.])
def test_guard_begin_shot_rejects_invalid_clock(clock):
    f = GuardFixture(); f.load()
    f.time = clock
    f.run("BeginShot", f.enemy, f.vm.state["generation"], f.vm.state["token"])
    assert f.vm.state["phase"] != 1 and not f.shots


def timing_offsets(binary):
    raw = binary["datos"]; offsets = set()
    for kind, off, size in binary["bloques"]:
        if kind != "NiControllerSequence": continue
        count = struct.unpack_from("<I", raw, off + 4)[0]
        offsets.add(off + 12 + count * 29 + 20)
        for i in range(count):
            interp = struct.unpack_from("<i", raw, off + 12 + i * 29)[0]
            _, io, _ = binary["bloques"][interp]
            data = struct.unpack_from("<i", raw, io + 32)[0]
            _, do, ds = binary["bloques"][data]
            offsets.update(transform_times(raw, do, ds))
    return offsets


def test_written_nif_retimes_v13_and_changes_only_registered_time_floats():
    parent = BASE / "mod/meshes/AstraAsedio/ballesta.nif"
    binary = nif_nodos.leer(str(parent))
    assert binary["version"] == "0x14020007" and binary["bs"] == 100
    expected, report = retime(parent, {"Fire": .2, "Reset": .8})
    actual = (ROOT / "mod/meshes/AstraAsedio/ballesta.nif").read_bytes()
    assert actual == expected
    masked = bytearray(actual)
    for off in timing_offsets(binary): masked[off:off + 4] = binary["datos"][off:off + 4]
    assert masked == binary["datos"]
    assert report["timing_floats"] == len(timing_offsets(binary))


def test_v14_retimer_measures_parent_before_reusing_validated_byte_retimer():
    script = ROOT / "scripts/retime_v14.py"
    assert script.exists(), "v14 retimer is not implemented"
    spec = importlib.util.spec_from_file_location("retime_v14", script)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    output, report = module.retime_parent(BASE / "mod/meshes/AstraAsedio/ballesta.nif", {"Fire": .2, "Reset": .8})
    assert report["baseline_measurement"]["version"] == "0x14020007"
    assert report["baseline_measurement"]["bs"] == 100
    assert report["baseline_measurement"]["sequences"] == pytest.approx({"Fire": .3, "Reset": 1.2}, abs=1e-6)
    assert output == (ROOT / "mod/meshes/AstraAsedio/ballesta.nif").read_bytes()
