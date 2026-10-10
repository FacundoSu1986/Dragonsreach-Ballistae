# AstraSight 3.5.4 — API 4

Target: Steam Skyrim SE 1.6.1170.0, SKSE 2.2.8 and matching Address Library. Runtime checks reject other game versions. SKSE 2.2.6 exposes the interfaces used here, but is untested with this DLL and below the supported minimum. Use the appropriate older Steam build from the official SKSE Nexus files page.

Native code owns player sight, the Fire/Release/Reset cycle and projectile launch. Reference handles and loaded scene identity are validated each update; effects serialize against teardown. Projectile speed is normalized to ShotAmmo's projectile record. A successful projectile handle is required before ammunition cost is committed. No FOV setting changes.

3.5.4 adds ResetIdleScene, a main-thread-only Papyrus binding. It rejects ownership, pending cleanup, missing nodes and scene replacement, and settles the existing Reset sequence at its final phase without replaying the legacy whole-reference animation. Guard handoff waits for restoration and any pending guard Launcher.Fire. API remains 4; check DLL version 3.5.4 before calling this additive binding.

Guard firing uses a separate Papyrus Weapon.Fire path. Player flight measurements do not establish NPC ballistics. Player sight and flight were confirmed with 3.5.3; the 3.5.4 handoff change requires game testing. Portable tests establish math and ordering, not Skyrim rendering or VM scheduling.

## Source build

The source archive includes native C++ and six PSC files. It excludes Bethesda files, SDKs, dependency source trees and the historical ESP/NIF/Blender pipeline. Use an x64 MSVC developer shell, CMake 3.26+, Ninja and C++23. Release toolchain: MSVC 14.51.36231, Windows SDK 10.0.26100.0. Other toolchains are uncertified.

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

CMake detects the compiler language by default. Only if its include-prefix detection fails, set ASTRA_SHOWINCLUDES_PREFIX to the exact compiler diagnostic prefix. Install out/AstraSight.dll into Data/SKSE/Plugins. For pure tests without Skyrim headers use -DASTRA_BUILD_PLUGIN=OFF. Nine targets cover 2,376 assertions.

Compile PSC files with the Skyrim Creation Kit Papyrus compiler and matching SKSE source imports. Binary PEX was disassembled after anonymizing compiler user/host fields; executable tables remain byte-identical. Changing PSC alone does not update installed PEX. The local build_native.py helper is machine-specific and excluded from the public source archive.

## Notices and limits

Third-party notices, including spdlog's embedded fmt, are in licenses. The DLL links Windows and Microsoft C++ runtime libraries and retains a few compiler diagnostic paths into the SDK checkout. Public packages exclude logs, profiles and machine configuration. The source archive grants no additional game-asset or original-asset rights; publisher permissions apply.

Tests do not establish engine hooks, NPC ballistics, damage, navigation or camera-mod compatibility. Camera transactions retain the existing Session mutex discipline; concurrent engine reentrancy remains a game verification topic.

API evidence: [FirstPersonState](https://github.com/CharmedBaryon/CommonLibSSE-NG/blob/b93280e832f263dbef44e44cbe2936622a02f91a/include/RE/F/FirstPersonState.h), [native marshalling](https://github.com/CharmedBaryon/CommonLibSSE-NG/blob/b93280e832f263dbef44e44cbe2936622a02f91a/include/RE/N/NativeFunction.h), [handle resolution](https://github.com/CharmedBaryon/CommonLibSSE-NG/blob/b93280e832f263dbef44e44cbe2936622a02f91a/include/RE/B/BSPointerHandle.h).
