# v06: repair firing-time camera bindings and native scheduling

User confirmed v05 mounted camera and mouse aiming in Skyrim. Firing becomes slow and buggy. Preserve the working camera transform, models, ammo, animation timelines, control ownership and v05 archives. Do not modify runtime Game/Camera scripts, saves, the selected MO2 profile or vanilla assets.

Evidence: copied Papyrus.0.log reports repeated unbound Camera.GetCameraState calls in CanOperate, SampleSightAimResult and firing preflight. Disassembled installed Game.pex also forwards GetCameraState to Camera, so merely changing the PSC namespace would keep the defect. SKSE registers the getter on Game and makes it NoWait. v05 Astra native registrations use default tasklet scheduling although session operations are mutex protected and scene writes occur only in FP Update.

1. Reproduce the unbound getter/default-zero camera acceptance in actual PSC fixtures; retain all previous lifecycle, cancellation and single-ammo regressions.
2. Add Astra's own API-v2 camera getter, unknown state -1, matching SKSE's pointer-identity lookup. Guard new calls against absent/older DLLs, including cleanup on saved sessions. Keep external Game/Camera PEX files unchanged.
3. Mark the session-only native APIs callable from tasklets, including explicit flag on custom CaptureAim. Confirm official handle/array NoWait precedents and review synchronization; do not move scene work to VM threads.
4. Compile the DLL and four PSC, disassemble final PEX and prohibit Camera/GetCameraState imports. Keep sparse firing diagnostics for a next game run; no per-frame log flood. Preserve five-second reload.
5. Independently review source/interop/cleanup, run applicable tests and compare installed/packaged files. Prepare separate AstraAsedio_QA_v06 with Address Library, preserving selected v05/other profiles. Seal v06 MO2/source ZIPs and describe proof limits.

FPS or full-resolution firing behavior is not measured by source tests. User clarification is pending; v06 game acceptance remains pending until another real run.
