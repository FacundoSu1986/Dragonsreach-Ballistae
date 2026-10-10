# Native v13 verification

AstraSight 3.4.0 / API 3 supports pitch -20..80 degrees. Session::begin and Session::update use the same limits; player AstraAsedioActi.psc defaults to PitchMin -20 and requires packed DLL version 50593792 (0x03040000). Runtime remains SkyrimSE 1.6.1170.0, minimum SKSE64 2.2.8. Camera, lease and API 3 functions retain their existing interface.

Final DLL: mod/SKSE/Plugins/AstraSight.dll, AMD64, 635904 bytes.
SHA256: 7cf962b1b16c14033ae62e36261b75a26a1212d4f7e0c692d24131e364cffb2d.

Real build command, exit 0:

```powershell
python scripts/build_native.py --vendor-dir E:\Sectores\Sector_Modelado_3D\Ballesta_Astra_Vanilla_SE_v11\build\native --build-dir build/native/release-verified
```

CMake generated dependency files, objects, test binaries and the DLL only inside v13/build/native/release-verified. Pinned CommonLibSSE-NG, spdlog, rapidcsv and extracted SDK inputs were reused in place from v11. The before/after file inventory found 6012 files both times and zero changes to byte lengths or nanosecond last-write times. The isolation guard separately rejected a requested build output outside v13 before creating it. No dependency source was copied or regenerated into v11. A second build receipt refresh also compared the full SHA256 and byte-length manifest of all 6,012 vendor files (665,641,140 bytes) before and after CMake, build and CTest; every digest remained identical. The immutable manifest is reports/native_vendor_manifest.json, sealed by SHA256 inside native_build_receipt.json.

CTest passed 5/5. Fresh scripts/verify_native_artifacts.py exited 0 and direct test executables reported 2281 assertions and zero failures: Core 147, v07 302, v08 86, v09 51, v10 1695. These cover initial pitch clamping, incremental lower overshoot, immediate reversal at -20 with and without player-look reconciliation, tilted/scaled-root muzzle validation at -20, existing freeze/token/epoch ordering and camera/post/zero collinearity at -20..80 over six yaw samples and scales 1/2.

TDD red evidence: new native tests built against the previous -5 implementation; Core reported six failures and v07 six failures, with the other three CTest suites passing (reports/v13_native_red.log). The three new player depression/version-gate tests also failed against the previous source (reports/v13_player_depression_red.log). Following implementation, all 138 selected player/controller regression tests passed (reports/v13_player_native_green.log). Those Python fixtures evaluate the actual PSC arithmetic and branches, with explicit native boundaries; they are not a Papyrus game VM.

PE parsing confirms AMD64, exactly SKSEPlugin_Load / SKSEPlugin_Query / SKSEPlugin_Version exports, packed plugin version 50593792, Address Library and post629 flags, compatibility only 1.6.1170.0 and minimum SKSE 2.2.8. Source/DLL/PSC/build-helper SHA receipt is reports/native_build_receipt.json; current SDK reuse receipt is reports/native_sdk_receipt.json; PE and executable evidence is reports/native_binary_checks.json and reports/native_artifacts_verified.json.

Evidence logs: reports/v13_native_build.log (also reports/native_build.log), reports/v13_native_build_receipt_refresh.log, reports/v13_native_verified.log, reports/v13_native_red.log, reports/v13_player_depression_red.log and reports/v13_player_native_green.log. Read-only vendor comparison is reports/v13_native_vendor_readonly.json.

The DLL was not loaded and Skyrim was not launched. Portable tests and PE checks do not prove FP hook timing, camera consumer-space semantics, animation/frame order, actual projectile impacts, camera-mod interactions or death/load/E restoration in the game. Bethesda PEX compilation belongs to the complete v13 build; this native verification does not execute Papyrus in Skyrim.
