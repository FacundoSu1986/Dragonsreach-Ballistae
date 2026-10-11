# AstraSight 3.5.9 / v28 current runtime

The station main-thread pump now consumes the OAR observation and applies the
bounded feet/grip solve before aim/Fire decisions. Character::Update is telemetry
only (atomic counters; no scene, physics or slot writes). Each clip request
invalidates grip. A 1.5s watchdog rejects unavailable pose samples instead of
waiting indefinitely for an unobserved Character callback. The v27 log has six
acquisitions, seven OAR holds and zero grip confirmations; the exact thread or
cadence of the old Character callback was not measured. Main-thread execution
and fresh OAR data do not certify post-animation render ordering. v28 must be
checked in Skyrim, including subsequent-frame hand errors from the bounded log.

Papyrus retries once after the scheduled 5s/30s backoff; its persistent wait flag
prevents an infinite self-rescheduling loop. Consecutive faults reset only after
healthy native status, not merely an accepted asynchronous BeginOperation.

Earlier release notes (historical descriptions of the old callback follow):

# AstraSight 3.5.8 â€” API 4

3.5.7 separates assigned station AI from the temporary running idle. Only a
previously acquired operator may retain an override identified as our own idle 802;
foreign packages, drawn weapons and worn shields revoke the lease. Each context
failure records its exact clause and assigned/running/run-once/idle identities.
Papyrus prepares only the two owned operators: unequip their shield, retain it
in inventory, yield to the next pump and re-query before acquiring a native lease.
OAR and grip confirmation are still required before Fire and launch. The v25
live log demonstrated 134 acquisitions followed by 134 generic context cancellations;
the exact failed clause was not available. The idle-override repair is based on
CommonLib engine field semantics, and v26 playback still needs Skyrim validation.

3.5.8 (v27) corrects the admission predicate using the measured v26 session
log: on 1.6.1170, PlayIdle permanently replaces the running package with its
run-once wrapper and never populates high->currentProcessIdle (93 measured
cycles, idle=00000000), so the v26 clause (running||ownIdle once acquired) was
unsatisfiable. Post-acquisition now requires only the assigned station package
and sheathed hands; owned-idle identity is arbitrated by the OAR
clip-observation hook (project, submod, exact path, duration, weight), with the
bounded no-observation cancel retained. install() logs whether
OpenAnimationReplacer.dll was loaded separately from API acquisition. On the
Papyrus side, the pump traces once when the Torres operator references cannot
resolve, and after a faulted acquisition (status -2) it backs off for 5s, then
30s onwards, instead of re-beginning every second (that 1-second churn also
re-issued IdleForceDefaultState and stomped in-flight OAR evaluation). All
other fail-closed clauses remain unchanged; Skyrim playback is still
uncertified.

The earlier 3.5.6 fixed the measured v24 rejection of naturally 1.03-height Nord guards.
Reference scale must remain 1, while effective scale must match TESNPC::GetHeight
and remain stable during the lease. The controller reaffirms the mounted position
every tick and after the actor update. Small arm IK corrections require the actual
expected canonical OAR replacement; a recent confirmed grip is required for Fire
and Launch. Non-hostile Whiterun residents/guards are excluded from visual targets.
Player API 4 and NPC API 1 remain compatible. Runtime playback is not certified
outside Skyrim.

Target: Steam Skyrim SE 1.6.1170.0, SKSE 2.2.8 and matching Address Library. Runtime checks reject other game versions. SKSE 2.2.6 exposes the interfaces used here, but is untested with this DLL and below the supported minimum. Use the appropriate older Steam build from the official SKSE Nexus files page.

Native code owns player sight, the Fire/Release/Reset cycle and projectile launch. Reference handles and loaded scene identity are validated each update; effects serialize against teardown. Projectile speed is normalized to ShotAmmo's projectile record. A successful projectile handle is required before ammunition cost is committed. No FOV setting changes.

3.5.4 adds ResetIdleScene, a main-thread-only Papyrus binding. It rejects ownership, pending cleanup, missing nodes and scene replacement, and settles the existing Reset sequence at its final phase without replaying the legacy whole-reference animation. Guard handoff waits for native restoration. API remains 4; check DLL version 3.5.4 before calling this additive binding.

v23 adds a separate AstraGuardNative API1 for the two low NPC stations. It launches a real engine projectile with the operator, launcher and ammunition through Projectile::LaunchData. Player API4 and its sight/shot policy remain compatible. The v23 DLL is identified by SHA256 in reports/native_build_receipt.json. Portable tests establish math and adapter contracts; v23 has not been verified in Skyrim.

## AstraGuardNative API1

IsAvailable and GetAPIVersion report the installed pump/OAR interface. BeginOperation(gun, guard, token, launcher, ammo, shotSound) acquires only AstraAsedio_WhiterunTorres.esp B70/B71 or B80/B81 with core ACTI B04. High stations remain player-only. GetStatus returns -1 absent, 0 acquiring, 1 observed Hold ready, 2 turning, 3 body Fire, 4 cleanup or -2 fault. EndOperation returns true only after effects and cleanup drain; completion is absent (-1), with a fault tombstone (-2) cleared by EndOperation. NotifyCombat is advisory; native selection independently scans loaded actors.

The camera-independent pump chains PlayerCharacter::Update (vfunc0xAD). Character::Update reaffirms the supported pose and applies lower-skeleton and arm IK after the original actor update only with a recent expected canonical OAR observation. The hkbClipGenerator::Generate hook preserves all five ABI arguments from OAR's primary implementation; observations follow original generation and reject future timeOffset sampling. OAR identity must match AstraAsedio Guard / Astra Guard Operate, Fire, TurnLeft or TurnRight and the physical IdleHandsBehindBack[\_Enter].hkx path under animations/OpenAnimationReplacer/AstraAsedioGuard/{Operate,Fire,TurnLeft,TurnRight}. Canonical astra_guard_*.hkx delivery copies are not runtime OAR replacements.

The actor's physical 151u orbit determines initial yaw, including a saved nonzero yaw. Acquisition requires upright reference scale1, a supported floor offset within eight units of gun root Z, and a certified natural human height (0.9 to 1.1). The free NPC heading is set during acquisition. It does not teleport to neutral. Yaw stays within Â±60Â°, pitch is horizontal, and the gun's identity rest rotations are verified against the delivered low NIF. Cleanup neutralizes gun aim; a subsequent lease derives yaw from the actor rather than accumulating the previous scene rotation. Moving the actor calls SetPosition with Havok enabled and checks the live controller's displacement. Floor and fenced clearance rays use that controller's full collision filter; a residual own-actor hit cannot certify floor.

Hold lasts 2s, body Fire 1s and a turn 0.8s for at most 12Â°. The authored clips contain 25 samples at 30fps with root floor 0; linear yaw advances at most 15Â°/s. Native IK preserves the planted world foot targets for partial turns. Arm IK rotates upper-arm/forearm bones while preserving hand world rotation and bone scale. Wrists follow the approved gun-local targets (+/-33.6,143.8,100.5), with the authored right-hand trigger curve during Fire. Corrections above 16 units or residual hand error above one unit cancel the lease; transitional/vanilla poses are never pulled onto the handles. Grip samples older than two frames cannot authorize Fire or Launch. Actual body Fire time sets the authoritative game clock, the mechanical Fire duration is 0.2s, release occurs at 2/30s, Reset lasts 0.8s and cadence is 2.5s. The runtime requests no corporal reload. Unobservable replacements, phase jumps, death/stagger, menus, load/unload or unknown physical state cancel and restore original private-faction ranks, movement and head-tracking flags. Legitimate Hold interruption recovery is bounded.

Visible player/visitor targets are limited to 2100u. Non-hostile members of Skyrim.esm TownWhiterunFaction (28172) or GuardFactionWhiterun (2BE39) are ignored; the player remains eligible and enemies retain priority. Both owned operators are excluded and protected. Nearby enemies may be visually followed above/below the firing line, but firing always requires a reachable horizontal trajectory. Only reachable enemies in combat can extend selection to 6000u. Cached targets remain stable within their priority class. Target selection and shot validation use the live controller shape AABB transformed into world units, including scaled creatures. Protected actors use conservative enclosing cylinders with margin; missing bounds, excessive scan counts, missing impact, blocked path or unknown explosion state prevents launch. Horizontal speed 5400/gravity 240.345 is checked against the live projectile record. Every predicted Havok segment through actual target impact is tested; the live PROJ explosion radius protects allies, neutrals and the player. Final main-thread lease, actor, target, muzzle, phase and visibility checks immediately precede the real launch. Auto aim and origin redirection are disabled; speed normalization follows the existing player runtime.

The on-disk hook inspection confirms Address Library vtable pointers into executable PE sections only. Steam-wrapped .text was not decoded, and no engine execution cadence, visual hand contact, collision behavior, actual projectile behavior or post-IK render ordering is claimed. Those checks remain in-game acceptance work. Unknown observations fail closed.

## Source build

The source archive includes native C++ and PSC sources. It excludes Bethesda files, SDKs, dependency source trees and the historical ESP/NIF/Blender pipeline. Use an x64 MSVC developer shell, CMake 3.26+, Ninja and C++23. Release toolchain: MSVC 14.51.36231, Windows SDK 10.0.26100.0. Other toolchains are uncertified.

Clone these into a local vendor directory at exactly these commits:

| Directory | Upstream | Commit |
| --- | --- | --- |
| CommonLibSSE-NG | https://github.com/CharmedBaryon/CommonLibSSE-NG | b93280e832f263dbef44e44cbe2936622a02f91a |
| spdlog | https://github.com/gabime/spdlog | 486b55554f11c9cccc913e11a87085b2a91f706f |
| rapidcsv | https://github.com/d99kris/rapidcsv | 03133b59e17ca92ecf886b611d87a03ad2bb2a8f |

From the source archive root:

```powershell
cmake -S native -B out -G Ninja -DCMAKE_BUILD_TYPE=Release -DASTRA_VENDOR="$PWD/vendor"
cmake --build out --parallel 4
ctest --test-dir out --output-on-failure
```

CMake detects the compiler language by default. Only if its include-prefix detection fails, set ASTRA_SHOWINCLUDES_PREFIX to the exact compiler diagnostic prefix. Install out/AstraSight.dll into Data/SKSE/Plugins. For pure tests without Skyrim headers use -DASTRA_BUILD_PLUGIN=OFF. The current CTest suite includes thirteen targets: the original nine, guard policy/lifecycle/IK/ABI tests, v25 natural-scale/grip/resident tests, v26 assigned/owned-idle admission tests, and a binding regression against the actual city/core ESPs and low NIF.

Compile PSC files with the Skyrim Creation Kit Papyrus compiler and matching SKSE source imports. Binary PEX was disassembled after anonymizing compiler user/host fields; executable tables remain byte-identical. Changing PSC alone does not update installed PEX. The local build_native.py helper is machine-specific and excluded from the public source archive.

## Notices and limits

Third-party notices, including spdlog's embedded fmt, are in licenses. The DLL links Windows and Microsoft C++ runtime libraries and retains a few compiler diagnostic paths into the SDK checkout. Public packages exclude logs, profiles and machine configuration. The source archive grants no additional game-asset or original-asset rights; publisher permissions apply.

Tests do not establish engine hooks, NPC ballistics, damage, navigation or camera-mod compatibility. Camera transactions retain the existing Session mutex discipline; concurrent engine reentrancy remains a game verification topic.

API evidence: [FirstPersonState](https://github.com/CharmedBaryon/CommonLibSSE-NG/blob/b93280e832f263dbef44e44cbe2936622a02f91a/include/RE/F/FirstPersonState.h), [native marshalling](https://github.com/CharmedBaryon/CommonLibSSE-NG/blob/b93280e832f263dbef44e44cbe2936622a02f91a/include/RE/N/NativeFunction.h), [handle resolution](https://github.com/CharmedBaryon/CommonLibSSE-NG/blob/b93280e832f263dbef44e44cbe2936622a02f91a/include/RE/B/BSPointerHandle.h), [OAR Animations API](https://github.com/ersh1/OpenAnimationReplacer/blob/main/src/API/OpenAnimationReplacerAPI-Animations.h), [Generate five-argument hook](https://github.com/ersh1/OpenAnimationReplacer/blob/main/src/Hooks.h), [controller support ray using its full filter](https://github.com/alexsylex/AnimationMotionRevolution/blob/main/source/Hooks.cpp).
