# Release status — 0.19.0-rc.1

Candidate, not a stable release. No Nexus upload has been performed.

Offline verification covers current C++ tests, interpreted PSC lifecycle regressions, fresh compiled/disassembled PEX, VMAD types and references, archive integrity and immutable-parent hashes. These checks do not execute Skyrim's VM, renderer or Creation Kit finalization.

Before publishing as stable:

1. Confirm that guard/player transfer has no whole-weapon disappearance on entry, exit, unload/reload and repeated takeover, including a guard shot pending at activation.
2. Check both Whiterun towers with a fresh test save and a copied v18 save: sight, bolt velocity, ammunition, damage, collision, guard return, menus, death and loading.
3. Verify NPC projectile behavior in combat separately from native player shots.
4. Complete Creation Kit finalization/checks for any playable custom navmesh. Atalaya stays excluded until its altered exterior LAND and NAVM agree.
5. Complete xEdit Check for Errors and supported parent cleanup, then reload and verify all placed-reference IDs and data. Two bounded isolated xEdit scripting attempts did not complete, so there is no xEdit pass. Current Tamriel WRLD 0000003C and persistent CELL 00000D74 headers retain vanilla settings and can affect other mods; placement patches still require testing.
6. Establish redistributable requirements on a clean machine, confirm the official SKSE 2.2.8 download and test representative camera/Whiterun overhauls before claiming compatibility.

This archive contains no test saves, Papyrus runtime logs, build artifacts other than the DLL/PEX, or machine-specific configuration. PEX compiler user/computer names are anonymized. A few SDK diagnostic paths remain inside the DLL; they are disclosed rather than described as absent.
