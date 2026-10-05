# Native v05 verification

Final DLL: `mod/SKSE/Plugins/AstraSight.dll`, AMD64, 599552 bytes.
SHA256: `38327cec801fbfa7b6b7515e94adf482627249f620ae50401207027dc975daef`.

Fresh `scripts/build_native.py` exited 0. CTest passed 1/1. Direct `AstraCoreTests.exe` reported 113 assertions, 0 failures. Tests cover rotated-root transforms, 360 wrap, -5..80 limits and immediate reversal, optical adapter composition, cameraRoot parent scale, lease/token/epoch invalidation, freeze and End waiting for in-flight apply, stale prepared samples, menus/freeze drift, missing scene and nonfinite input. The final reconciled path restores player's logical look to applied world direction and rebases its sample, with no player position, FOV or control writes.

RED evidence: first runnable math suite failed 16 adapter-basis assertions (`native_core_toolchain.log`), caught the incorrect cross-product sign, then passed (`native_core_green.log`). Deliberately removing CaptureAim freeze produced seven expected failures (`native_freeze_red.log`), including prepared-frame and published-snapshot tests; source was restored. The reconciliation regression failed once before its rebase was implemented (`native_reconcile_red.log`, 107 assertions/1 failure) and passes in the final build.

PE parse confirms exactly SKSEPlugin_Load/Query/Version exports; plugin name AstraSight; version 1.0.0; compatibility only 1.6.1170.0; Address Library and post629 struct flags; minimum SKSE 2.2.8. The DLL was never loaded by this verification. Details: `native_binary_checks.json`.

Pinned primary dependencies: CommonLibSSE-NG b93280e832f263dbef44e44cbe2936622a02f91a (MIT); spdlog 486b55554f11c9cccc913e11a87085b2a91f706f (MIT, bundled fmt 12.0.0 MIT); rapidcsv 03133b59e17ca92ecf886b611d87a03ad2bb2a8f (BSD3). Exact license notices are in native/licenses and need inclusion in the runtime distribution. Build inputs under build/native must not be packaged, including SDK extraction and vendor checkouts. Source/DLL/PSC/build-helper SHA receipts: `native_build_receipt.json`; official cached SDK extraction: `native_sdk_receipt.json`.

Toolchain findings fixed locally: installed UCRT headers/props contained zero bytes; official cached SDK MSI/CABs were administratively extracted only inside build/native/windows_sdk. CMake's misdecoded Spanish include prefix prevented header dependency tracking; native/CMakeLists corrects that prefix and final build uses a fresh verified directory. No global installs/repair, runtime modifications, native UI or game launch occurred.

Pending in Skyrim: actual FP hook timing, original quaternion convention/calibration and getter consumer-space observations, visual rigid attachment, frame order under animation, parallax/impacts, camera-mod conflicts, and game death/load/E restoration. The Steam executable's packed text makes recorded static disassembly unsuitable for proving those properties. CaptureAim preserves float[] type (including a typed null zero-array representation if VM allocation fails), but VM empty-array behavior still needs engine verification. No compiled/file check proves that visual/frame acceptance.


Review P2 fix: per-frame failure invalidation now checks both ticket key and epoch under the session mutex. RED reproduced five failures in 113 assertions (native_invalidation_red.log) using the former unconditional behavior: stale A invalidation cancelled B readiness/snapshot, wrong key at the same epoch cancelled the lease, and a stale epoch cancelled a renewed identical key. GREEN passes all 113 assertions and also verifies that matching-frame failure invalidates its own lease. The three early FP validation branches use the guarded invalidation; camera End/load/revert remain global. NIF, exact six-function PSC API and build helper were unchanged.


