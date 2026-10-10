"""Execute the guard's actual PSC branches with deterministic native fixtures.

This source evaluator is not the Papyrus VM. It tests the source arithmetic and
specified interruptions; engine event delivery, NPC animation and damage remain
in-game checks.
"""
import math
import re
from pathlib import Path
from types import SimpleNamespace

import pytest

from test_control_lease import SessionSourceEvaluator

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "mod/scripts/source/AstraAsedioGuard.psc"


def rotation_z(degrees):
    c, s = math.cos(math.radians(degrees)), math.sin(math.radians(degrees))
    return [c, -s, 0., s, c, 0., 0., 0., 1.]


def matmul(a, b):
    return [sum(a[3*r+k]*b[3*k+c] for k in range(3)) for r in range(3) for c in range(3)]


class ActorFixture:
    def __init__(self, pos=(0., 0., 0.)):
        self.pos = list(pos)
        self.dead = self.disabled = self.teammate = False
        self.loaded = self.hostile = self.los = True
        self.combat = 1
        self.target = None
        self.height = 128.
        self.pinned = False
        self.moves = []
        self.headings = []

    def IsDead(self): return self.dead
    def IsDisabled(self): return self.disabled
    def Is3DLoaded(self): return self.loaded
    def IsPlayerTeammate(self): return self.teammate
    def IsHostileToActor(self, other): return self.hostile
    def GetCombatState(self): return self.combat
    def GetCombatTarget(self): return self.target
    def HasLOS(self, other): return self.los
    def GetPositionX(self): return self.pos[0]
    def GetPositionY(self): return self.pos[1]
    def GetPositionZ(self): return self.pos[2]
    def GetHeight(self): return self.height
    def GetDistance(self, other): return math.dist(self.pos, other.pos)
    def SetDontMove(self, value=True): self.pinned = value
    def MoveTo(self, other): self.moves.append(other); self.pos = other.pos[:]
    def SetAngle(self, x, y, z): self.headings.append(z)


class GuardFixture:
    def __init__(self):
        assert SOURCE.exists(), "missing NPC controller"
        self.source = SOURCE.read_text(encoding="utf-8-sig")
        self.vm = SessionSourceEvaluator(self.source)
        self.time = 20.
        self.menu = False
        self.loaded = True
        self.player = ActorFixture((1000., 0., 0.))
        self.guard = ActorFixture((0., 240., 0.))
        self.marker = ActorFixture((0., 240., 0.))
        self.enemy = ActorFixture((0., -1600., 0.))
        self.guard.target = self.enemy
        self.root_rotation = rotation_z(0)
        self.root_pos = [0., 0., 0.]
        self.node_local = {"CTRL_GIRO_360": rotation_z(0), "CTRL_ELEVACION": rotation_z(0)}
        self.animations = []
        self.shots = []
        self.sounds = []
        self.visual = 1.
        self.updates = []
        self.hooks = {}
        self.bad_pose = False
        self.animation_ok = True
        self.vm.state.update({
            "Self": self, "Artillero": self.guard, "Puesto": self.marker,
            "Launcher": SimpleNamespace(Fire=self.fire), "ShotAmmo": object(),
            "ShotSound": SimpleNamespace(Play=lambda ref: self.sounds.append(ref)),
            "Game": SimpleNamespace(GetPlayer=lambda: self.player, GetFormFromFile=lambda *args: None),
            "Utility": SimpleNamespace(GetCurrentRealTime=lambda: self.time, IsInMenuMode=lambda: self.menu),
            "SKSE": SimpleNamespace(GetVersion=lambda: 2),
            "Math": SimpleNamespace(Abs=abs, Sqrt=math.sqrt,
                Sin=lambda x: math.sin(math.radians(x)), Cos=lambda x: math.cos(math.radians(x)),
                ACos=lambda x: math.degrees(math.acos(x)), ASin=lambda x: math.degrees(math.asin(x))),
            "NetImmerse": SimpleNamespace(HasNode=lambda *args: True,
                GetNodeWorldRotationMatrix=self.read_rotation, GetNodeWorldPosition=self.read_position,
                SetNodeLocalRotationMatrix=self.write_rotation, SetNodeScale=self.scale),
        })
        self.vm.native.update({
            "Is3DLoaded": lambda: self.loaded, "IsDisabled": lambda: False,
            "BlockActivation": lambda blocked: None,
            "RegisterForSingleUpdate": self.updates.append, "UnregisterForUpdate": lambda: self.updates.clear(),
            "PlayGamebryoAnimation": self.animate,
        })

    def interrupt(self, boundary):
        callback = self.hooks.pop(boundary, None)
        if callback: callback()

    def read_rotation(self, ref, node, out, first):
        if node == "": result = self.root_rotation
        else:
            pitch = self.node_local["CTRL_ELEVACION"]
            yaw = self.node_local["CTRL_GIRO_360"]
            result = matmul(matmul(matmul(self.root_rotation, yaw), pitch), rotation_z(180))
        out[:] = result
        if self.bad_pose and node: out[4] *= -1
        self.interrupt("rotation")
        return True

    def read_position(self, ref, node, out, first):
        if not node: result = self.root_pos
        else:
            yaw = self.node_local["CTRL_GIRO_360"]
            pitch = self.node_local["CTRL_ELEVACION"]
            local = [sum(pitch[3*r+k]*[0., -224., 19.6][k] for k in range(3)) for r in range(3)]
            local[2] += 153.
            matrix = matmul(self.root_rotation, yaw)
            result = [self.root_pos[r]+sum(matrix[3*r+k]*local[k] for k in range(3)) for r in range(3)]
        out[:] = result
        self.interrupt("position")
        return True

    def write_rotation(self, ref, node, value, first):
        self.node_local[node] = value[:]
        self.interrupt("write_rotation")
        return True

    def scale(self, ref, node, value, first): self.visual = value
    def animate(self, name, restart):
        self.animations.append(name)
        self.interrupt("animation:"+name)
        return self.animation_ok
    def fire(self, ref, ammo): self.shots.append((self.time, ref, ammo))
    def run(self, name, *args): return self.vm.run(name, *args)
    def load(self): self.run("OnLoad")
    def tick(self, seconds=.2): self.time += seconds; self.run("OnUpdate")
    def acquire_and_aim(self):
        self.load()
        for _ in range(30):
            self.tick()
            if self.vm.state["phase"] == 1: return
        raise AssertionError("guard did not prepare a valid shot")


def test_guard_exists_and_uses_independent_reference_properties():
    f = GuardFixture()
    assert f.vm.state["ProjectileSpeed"] == 5400.
    assert f.vm.state["ProjectileGravity"] == pytest.approx(240.345)
    assert (f.vm.state["PitchMin"], f.vm.state["PitchMax"]) == (-20., 45.)
    for forbidden in ("Session", "DisablePlayerControls", "ForceFirstPerson", "RegisterForKey"):
        assert not re.search(r"\b"+forbidden+r"\b", f.source)
    # v15 shared stations only query per-gun effects ownership; the guard
    # still cannot begin/end a sight, aim the player's camera or handle input.
    assert set(re.findall(r"AstraSightNative\.(\w+)\(", f.source)) == {"IsEffectsQuiescent", "ResetIdleScene"}


@pytest.mark.parametrize("failure", ["player", "teammate", "dead", "disabled", "unloaded", "friendly", "peace", "guard_peace", "los", "none"])
def test_unsafe_combat_targets_never_launch(failure):
    f = GuardFixture()
    if failure == "player": f.guard.target = f.player
    elif failure == "none": f.guard.target = None
    elif failure == "guard_peace": f.guard.combat = 0
    elif failure == "los": f.guard.los = False
    elif failure == "friendly": f.enemy.hostile = False
    elif failure == "peace": f.enemy.combat = 0
    else: setattr(f.enemy, {"unloaded": "loaded"}.get(failure, failure), failure != "unloaded")
    f.load()
    for _ in range(30): f.tick()
    assert not f.shots
    assert f.vm.state["phase"] == 0


@pytest.mark.parametrize("yaw,pitch", [(61., 0.), (-61., 0.), (0., -21.), (0., 46.), (180., 0.)])
def test_target_outside_guard_sector_rejected(yaw, pitch):
    f = GuardFixture()
    f.vm.state["ProjectileGravity"] = 0.
    r = 1600.
    f.enemy.pos = [math.sin(math.radians(yaw))*math.cos(math.radians(pitch))*r,
        -math.cos(math.radians(yaw))*math.cos(math.radians(pitch))*r,
        172.6 + math.sin(math.radians(pitch))*r - 60.]
    f.load()
    assert not f.run("SampleTarget", f.enemy, f.vm.state["generation"], f.vm.state["token"])
    assert not f.shots


def test_low_arc_solution_hits_target_using_projectile_data():
    f = GuardFixture(); f.load()
    assert f.run("SampleTarget", f.enemy, f.vm.state["generation"], f.vm.state["token"])
    s = f.vm.state
    muzzle = s["muzzlePosition"]
    dx, dy = f.enemy.pos[0]-muzzle[0], f.enemy.pos[1]-muzzle[1]
    h = math.hypot(dx, dy)
    t = h/(s["ProjectileSpeed"]*math.hypot(s["aimX"], s["aimY"]))
    actual = [muzzle[0]+s["aimX"]*s["ProjectileSpeed"]*t,
        muzzle[1]+s["aimY"]*s["ProjectileSpeed"]*t,
        muzzle[2]+s["aimZ"]*s["ProjectileSpeed"]*t-.5*s["ProjectileGravity"]*t*t]
    assert actual == pytest.approx([*f.enemy.pos[:2], f.enemy.pos[2]+60.], abs=1e-6)
    assert s["desiredPitch"] < 0.  # Target below the elevated muzzle.


def test_root_transpose_and_native_bore_follow_rotated_reference():
    f = GuardFixture()
    f.root_rotation = rotation_z(90.)
    f.enemy.pos = [1600., 0., 0.]
    f.player.pos = [0., 1000., 0.]
    f.acquire_and_aim(); f.tick(.1)
    assert len(f.shots) == 1
    assert abs(f.vm.state["yaw"]) < .05


def test_turn_rate_is_bounded_and_shot_waits_for_alignment():
    f = GuardFixture()
    f.enemy.pos = [1000., -1400., 0.]
    f.load(); f.tick()
    assert 0. < f.vm.state["yaw"] <= 6.00001
    assert not f.shots
    f.tick(100.)  # A stalled VM tick cannot snap the mount through the sector.
    assert f.vm.state["yaw"] <= 18.00001
    assert not f.shots


def test_fire_release_reset_and_two_and_a_half_second_cadence():
    f = GuardFixture(); f.acquire_and_aim()
    assert f.animations[-1] == "Fire" and not f.shots
    f.tick(.1)
    assert len(f.shots) == 1 and f.visual == 0.
    fired_at = f.shots[0][0]
    f.tick(.200001)
    assert f.animations[-1] == "Reset"
    f.tick(.800001)
    assert f.visual == 1. and f.vm.state["phase"] == 0
    while f.time < fired_at+2.5: f.tick(.2)
    f.tick(.1)
    assert len(f.shots) == 2
    assert f.shots[1][0]-fired_at >= 2.5
    assert len(f.sounds) == 2


@pytest.mark.parametrize("change", ["dead", "los", "different", "unloaded", "pose", "menu"])
def test_release_revalidates_target_and_current_muzzle(change):
    f = GuardFixture(); f.acquire_and_aim()
    if change == "dead": f.enemy.dead = True
    elif change == "los": f.guard.los = False
    elif change == "different": f.guard.target = ActorFixture((0., -1500., 0.))
    elif change == "unloaded": f.enemy.loaded = False
    elif change == "pose": f.bad_pose = True
    else: f.menu = True
    f.tick(.1)
    assert not f.shots
    assert f.animations[-1] == "Reset"


@pytest.mark.parametrize("boundary", ["animation:Fire", "rotation", "position"])
def test_unload_cancels_suspended_native_boundaries(boundary):
    f = GuardFixture()
    if boundary == "animation:Fire":
        f.hooks[boundary] = lambda: (setattr(f, "loaded", False), f.run("OnUnload"))
        f.load()
        for _ in range(30): f.tick()
    else:
        f.acquire_and_aim()
        f.hooks[boundary] = lambda: (setattr(f, "loaded", False), f.run("OnUnload"))
        f.tick(.1)
    assert not f.shots and not f.guard.pinned
    assert f.vm.state["token"] == -1


def test_saved_cycle_recovery_invalidates_old_generation_and_token():
    f = GuardFixture(); f.acquire_and_aim()
    old = (f.vm.state["generation"], f.vm.state["token"])
    f.load()
    assert not f.run("Current", *old)
    assert f.vm.state["phase"] == 0 and f.visual == 1.
    assert not f.shots
    f.run("CommitShot", f.enemy, *old)
    assert not f.shots


def test_real_time_rewind_recovers_a_restored_pending_cycle():
    f = GuardFixture(); f.acquire_and_aim()
    old = f.vm.state["generation"]
    f.time = 1.; f.run("OnUpdate")
    assert f.vm.state["generation"] > old
    assert f.vm.state["phase"] == 0 and not f.shots


@pytest.mark.parametrize("event,args", [("OnUnload", ()), ("OnCellDetach", ()), ("OnDestructionStageChanged", (0, 1))])
def test_lifecycle_releases_only_dedicated_guard(event, args):
    f = GuardFixture(); f.load()
    assert f.guard.pinned
    f.run(event, *args)
    assert not f.guard.pinned and not f.player.pinned
    assert f.vm.state["token"] == -1


def test_guard_death_releases_without_resurrect_or_teleport():
    f = GuardFixture(); f.load(); f.guard.dead = True; f.tick()
    assert not f.guard.pinned and not f.shots and not f.guard.moves
    assert "Resurrect" not in f.source


def test_move_to_station_only_during_recovery_if_far():
    f = GuardFixture(); f.guard.pos = [0., 600., 0.]; f.load()
    assert f.guard.moves == [f.marker]
    f.guard.pos = [0., 400., 0.]
    for _ in range(20): f.tick()
    assert f.guard.moves == [f.marker]
    assert not f.shots  # Pin displaced beyond station tolerance.


@pytest.mark.parametrize("height,z", [(128., 0.), (128., 110.), (128., 180.), (256., 270.)])
def test_player_body_crossing_blocks_fire(height, z):
    f = GuardFixture(); f.acquire_and_aim()
    # Place the player so the measured trajectory passes through feet, torso or
    # head, including the extra 64-unit animation allowance above measured height.
    s = f.vm.state
    muzzle = s["muzzlePosition"]
    t = .1
    bx, by, bz = s["muzzleWorldMatrix"][1], s["muzzleWorldMatrix"][4], s["muzzleWorldMatrix"][7]
    f.player.height = height
    f.player.pos = [muzzle[0]+bx*5400*t, muzzle[1]+by*5400*t,
        muzzle[2]+bz*5400*t-.5*240.345*t*t-z]
    f.tick(.1)
    assert not f.shots


def test_player_clear_of_trajectory_can_fire():
    f = GuardFixture(); f.acquire_and_aim(); f.player.pos = [300., -750., 0.]
    f.tick(.1)
    assert len(f.shots) == 1


@pytest.mark.parametrize("speed,gravity", [(0., 240.345), (-1., 240.345), (float("nan"), 240.345), (5400., float("nan")), (100., 240.345)])
def test_invalid_or_unreachable_ballistics_fail_closed(speed, gravity):
    f = GuardFixture(); f.vm.state.update(ProjectileSpeed=speed, ProjectileGravity=gravity)
    f.load()
    for _ in range(30): f.tick()
    assert not f.shots


def test_animation_failure_aborts_without_loop_or_launch():
    f = GuardFixture(); f.animation_ok = False; f.load()
    for _ in range(30): f.tick()
    assert not f.shots
    assert f.vm.state["phase"] in (0, 3)
    assert len(f.animations) <= 6


def test_target_change_during_final_los_check_aborts_commit():
    f = GuardFixture(); f.acquire_and_aim()
    calls = 0
    def los(target):
        nonlocal calls
        calls += 1
        if calls == 2:
            f.guard.target = None
        return True
    f.guard.HasLOS = los
    f.tick(.1)
    assert calls == 2 and not f.shots
    assert f.vm.state["phase"] == 3


def test_reload_during_commit_keeps_new_token_and_cancels_old_shot():
    f = GuardFixture(); f.acquire_and_aim()
    old = (f.vm.state["generation"], f.vm.state["token"])
    f.hooks["rotation"] = f.load
    f.tick(.1)
    assert not f.shots
    assert not f.run("Current", *old)
    assert f.guard.pinned and f.vm.state["phase"] == 0 and f.visual == 1.


def test_unload_during_player_body_query_cancels_commit():
    f = GuardFixture(); f.acquire_and_aim()
    def height():
        f.loaded = False
        f.run("OnUnload")
        return 128.
    f.player.GetHeight = height
    f.tick(.1)
    assert not f.shots and not f.guard.pinned


def test_operator_property_cannot_pin_player():
    f = GuardFixture(); f.vm.state["Artillero"] = f.player; f.load()
    assert not f.player.pinned and not f.shots
    assert f.vm.state["token"] == -1


@pytest.mark.parametrize("matrix", [[0.]*9, [1.,0.,0.,0.,1.,0.,0.,0.,-1.], [float("nan")]+[0.]*8])
def test_invalid_root_matrix_blocks_target_sampling(matrix):
    f = GuardFixture(); f.root_rotation = matrix; f.load()
    assert not f.run("SampleTarget", f.enemy, f.vm.state["generation"], f.vm.state["token"])
    assert not f.shots


def test_unloaded_operator_releases_then_recovers_on_bounded_idle_tick():
    f = GuardFixture(); f.load(); f.guard.loaded = False; f.tick()
    assert not f.guard.pinned and f.vm.state["token"] == -1
    assert f.updates == [1.]
    f.guard.loaded = True; f.tick(1.)
    assert f.guard.pinned and f.vm.state["token"] > 0
    assert not f.shots


@pytest.mark.parametrize("minimum,maximum", [(-21., 45.), (-20., 46.), (30., -10.), (float("nan"), 45.)])
def test_pitch_properties_outside_physical_limits_fail_closed(minimum, maximum):
    f = GuardFixture(); f.vm.state.update(PitchMin=minimum, PitchMax=maximum); f.load()
    assert not f.run("SampleTarget", f.enemy, f.vm.state["generation"], f.vm.state["token"])


def test_narrowed_pitch_properties_reject_target_instead_of_clamping():
    f = GuardFixture(); f.vm.state.update(PitchMin=0., PitchMax=20.); f.load()
    assert not f.run("SampleTarget", f.enemy, f.vm.state["generation"], f.vm.state["token"])


def test_enemy_death_during_commit_clock_boundary_aborts_release():
    f = GuardFixture(); f.acquire_and_aim()
    def clock():
        f.enemy.dead = True
        return f.time
    f.vm.state["Utility"].GetCurrentRealTime = clock
    f.run("CommitShot", f.enemy, f.vm.state["generation"], f.vm.state["token"])
    assert not f.shots
    assert f.vm.state["phase"] == 3


def test_unload_before_pending_pin_native_effect_compensates_acquisition():
    f = GuardFixture()
    interrupted = False
    def pin(value=True):
        nonlocal interrupted
        if value and not interrupted:
            interrupted = True
            f.loaded = False
            f.run("OnUnload")
        # Native effect can occur after the event that cancelled acquisition.
        f.guard.pinned = value
    f.guard.SetDontMove = pin
    f.load()
    assert not f.guard.pinned
    assert f.vm.state["token"] == -1 and f.vm.state["ownedGuard"] is None


def test_reload_during_pending_pin_defers_new_owner_until_compensation():
    f = GuardFixture()
    interrupted = False
    effects = []
    def pin(value=True):
        nonlocal interrupted
        if value and not interrupted:
            interrupted = True
            f.loaded = False; f.run("OnUnload")
            f.loaded = True; f.load()
        f.guard.pinned = value
        effects.append(value)
    f.guard.SetDontMove = pin
    f.load()
    # The next loaded generation may acquire only after the old True effect has
    # completed and its matching compensation has released it.
    assert effects == [True, False]
    assert not f.guard.pinned and f.vm.state["token"] == -1
    f.tick(.2)
    assert effects == [True, False, True]
    assert f.guard.pinned and f.vm.state["token"] > 0


def test_reload_before_pending_release_effect_cannot_unpin_new_owner():
    f = GuardFixture(); f.load()
    interrupted = False
    effects = []
    def pin(value=True):
        nonlocal interrupted
        if not value and not interrupted:
            interrupted = True
            f.loaded = True; f.load()
        f.guard.pinned = value
        effects.append(value)
    f.guard.SetDontMove = pin
    f.run("OnUnload")
    assert effects == [False]
    assert not f.guard.pinned and f.vm.state["token"] == -1
    f.tick(.2)
    assert effects == [False, True]
    assert f.guard.pinned and f.vm.state["token"] > 0


def test_old_hide_effect_after_load_is_compensated_before_new_owner():
    f = GuardFixture(); f.acquire_and_aim()
    interrupted = False
    def scale(ref, node, value, first):
        nonlocal interrupted
        if value == 0. and not interrupted:
            interrupted = True
            f.load()
        f.visual = value
    f.vm.state["NetImmerse"].SetNodeScale = scale
    f.tick(.1)
    assert f.visual == 1.
    assert f.vm.state["token"] == -1
    f.tick(.2)
    assert f.vm.state["token"] > 0 and f.vm.state["phase"] == 0 and f.visual == 1.
    f.guard.target = None
    for _ in range(20): f.tick(1.)
    assert f.visual == 1.


def test_old_aim_matrix_effect_cannot_overwrite_recovered_pose():
    f = GuardFixture(); f.load()
    f.enemy.pos = [1000., -1400., 0.]
    interrupted = False
    def write(ref, node, value, first):
        nonlocal interrupted
        if node == "CTRL_GIRO_360" and not interrupted:
            interrupted = True
            f.load()
        return f.write_rotation(ref, node, value, first)
    f.vm.state["NetImmerse"].SetNodeLocalRotationMatrix = write
    f.tick(.2)
    assert f.vm.state["token"] == -1
    f.tick(.2)
    assert f.vm.state["token"] > 0
    assert f.node_local["CTRL_GIRO_360"] == pytest.approx(rotation_z(0.))
    assert f.node_local["CTRL_ELEVACION"] == pytest.approx(rotation_z(0.))


def test_old_fire_animation_effect_after_load_resets_before_new_owner():
    f = GuardFixture(); f.load()
    interrupted = False
    f.active_animation = "Reset"
    def animate(name, restart):
        nonlocal interrupted
        if name == "Fire" and not interrupted:
            interrupted = True
            f.load()
        f.active_animation = name
        return True
    f.vm.native["PlayGamebryoAnimation"] = animate
    for _ in range(30):
        f.tick(.2)
        if interrupted: break
    assert interrupted
    assert f.active_animation == "Reset" and not f.shots
    assert f.vm.state["token"] == -1
    f.tick(.2)
    assert f.vm.state["token"] > 0 and f.vm.state["phase"] == 0
    assert f.active_animation == "Reset" and f.visual == 1.


def test_delayed_release_preserves_two_and_a_half_seconds_between_actual_launches():
    f = GuardFixture(); f.acquire_and_aim()
    f.tick(3.)
    assert len(f.shots) == 1
    for _ in range(70):
        f.tick(.1)
        if len(f.shots) >= 2: break
    assert len(f.shots) == 2
    assert f.shots[1][0]-f.shots[0][0] >= 2.5-1e-9


def test_suspended_final_preflight_reserves_cadence_from_post_launch_clock():
    f = GuardFixture(); f.acquire_and_aim()
    f.hooks["rotation"] = lambda: setattr(f, "time", f.time+2.)
    f.tick(.1)
    assert len(f.shots) == 1
    for _ in range(70):
        f.tick(.1)
        if len(f.shots) >= 2: break
    assert len(f.shots) == 2
    assert f.shots[1][0]-f.shots[0][0] >= 2.5-1e-9

