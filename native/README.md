# AstraSight native controller

Target: SkyrimSE 1.6.1170.0, SKSE64 2.2.8, existing Address Library `versionlib-1-6-1170-0.bin`. Runtime metadata and Load/Query gates reject other runtimes. Plugin name is `AstraSight`, version 1. No FOV or global control settings are changed.

Build from the project root with Python 3.11:

```powershell
& 'C:\Users\Facu2\AppData\Local\Programs\Python\Python311\python.exe' scripts/build_native.py
```

`build_native.py` pins CommonLibSSE-NG, spdlog and rapidcsv under `build/native`, builds with installed x64 MSVC and bundled Ninja/CMake, runs CTest, then copies the DLL to `mod/SKSE/Plugins`. Installed UCRT headers on this machine contained all-zero bytes. `prepare_local_sdk.py` performs administrative extraction of the already cached official SDK packages to `build/native/windows_sdk`; it neither repairs nor installs the global SDK. SDK inputs and executable runtime files are build inputs only and must be excluded from distribution.

Dependency revisions and license copies are in the build receipt and `native/licenses`. spdlog includes fmt 12.0.0; its embedded license is retained too. CommonLib is linked statically. The resulting DLL uses the usual installed Windows/MSVC runtime DLLs listed in `native_binary_checks.json`.

## Ownership and ordering

Papyrus owns the operator lease, controls, inventory and firing. `BeginSight` records reference handle age/index plus token and initial degrees; it does not touch scene data. `IsSightReady` becomes true only after a successful FP game-update transaction. VM callbacks read or modify only protected requests/snapshots. `CaptureAim` has a dedicated float-array dispatcher: unavailable results preserve the `kFloatArray` type even when the VM represents a zero-length array with a null array pointer.

The game thread resolves the reference handle each update using CommonLib's `LookupReferenceByHandle`, retaining no reference pointer between updates. A scene cache retains NiPointers plus loaded3D identity and internal epoch. CameraRoot and its parent identities are checked too. Acquisition strips the existing initial yaw/pitch rotations from the cached rest bases once. Only local rotations of CTRL_GIRO_360 and CTRL_ELEVACION are changed; translations, pivots and scales are retained.

Per-frame validation failures invalidate only the ticket's matching key and epoch under the session mutex. An old frame cannot cancel a newer lease accepted between its ticket read and validation. Global FP End/load/revert cleanup still invalidates the active session unconditionally.

FP Update, GetRotation, GetTranslation and End slots 3, 4, 5 and 2 are hooked. The original Update/getters/End are called outside the session mutex. Getters read a single coherent snapshot and check its FP state identity; they never apply scene data. FP End, SKSE pre/post load, new game and revert clear readiness and the override. Update also rejects death, missing reference/3D/nodes, changed 3D identity and ineligible camera.

Applying rotations, recursively calling transform-only UpdateWorldData, validating ProjectileNode/anchor, and publishing yaw/pitch/camera occurs inside one mutex transaction shared with CaptureAim(freeze), SetFrozen and EndSight. A prepared mouse sample cannot bypass a later freeze. EndSight waits for any in-flight transaction; after it returns no update from that epoch can write the lease's transforms. No transform restoration occurs natively; Papyrus can restore after EndSight returns.

Mouse aim consumes changes in player's logical look transformed through root transpose. After a valid applied pose, Update reconciles player's logical X/Z look angles to the same world direction and rebases its sample to applied yaw/pitch inside the transaction. This discards over-limit motion and avoids local-Euler folding for tilted roots. Player position is never changed. During freeze or pause the sample is rebased too; transition out of freeze and menu-open/close events discard the first unsampled movement. Overshoot at either limit is discarded, so reversing starts immediately. Yaw wraps continuously; pitch clamps to -5..80 degrees.

## Camera convention and remaining engine verification

The NIF camera anchor is a logical +Y-forward/+Z-up basis; it is not copied to the FP quaternion. At acquisition, the original FP quaternion is normalized, mapped to a rotation basis and compared with player logical look to derive an optical-axis adapter. With an identity cameraRoot parent, local and world spaces coincide. With a nonidentity parent, original getter pose is compared to cameraRoot local/world poses; ambiguous or distant calibration rejects readiness. Position is divided by parent scale when returning local translation, and rotation is composed with parent inverse when returning local orientation. Adapter and selected spaces are logged to AstraSight.log. Camera and ProjectileNode +Y forwards must match the root-relative gun -Y direction after the same world update.

`inspect_camera_runtime.py` reads the existing executable and Address Library only. Static vtable pointers can be resolved, but the installed Steam executable's text bytes are packed/encrypted; the recorded disassembly is not evidence of frame order or getter consumer semantics. Those are still pending visual verification in Skyrim. CTest checks portable math and lease ordering; PE checks establish architecture, exports and metadata only. No native UI or game launch was used.

Required in-game checks: rigid camera across 360 yaw and -5..80 pitch, direct reversal after overshoot, menus and freeze/reload resuming without jumps, near/far projectile parallax, entry from first/third person, death/load/camera transition cleanup, and restored camera after E exit. Other camera-mod hook conflicts and actual camera consumer timing also require that game test.

Primary API evidence: [CommonLib FirstPersonState](https://github.com/CharmedBaryon/CommonLibSSE-NG/blob/b93280e832f263dbef44e44cbe2936622a02f91a/include/RE/F/FirstPersonState.h), [TESCamera](https://github.com/CharmedBaryon/CommonLibSSE-NG/blob/b93280e832f263dbef44e44cbe2936622a02f91a/include/RE/T/TESCamera.h), [NativeFunction marshalling](https://github.com/CharmedBaryon/CommonLibSSE-NG/blob/b93280e832f263dbef44e44cbe2936622a02f91a/include/RE/N/NativeFunction.h), [handle resolution](https://github.com/CharmedBaryon/CommonLibSSE-NG/blob/b93280e832f263dbef44e44cbe2936622a02f91a/include/RE/B/BSPointerHandle.h).
