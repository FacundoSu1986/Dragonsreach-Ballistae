# Documentation and publication review — v19

Open documentation/developer-experience findings: none in the final candidate artifacts reviewed. This closes the single publication review; it is not approval of the pending engine or plugin release gates.

Resolved findings:

1. `native/README.md:1` now identifies AstraSight 3.5.4/API4, explains the additive main-thread ResetIdleScene binding, and separates the measured v18 player-flight evidence from the unverified v19 handoff change. The archived Source README matches this current file byte-for-byte.
2. `native/README.md:13` now supplies a source-archive CMake/Ninja recipe from an x64 MSVC developer shell with exact dependency pins/toolchain versions. Private Python/vendor paths and the machine-specific helper are excluded. The source scope explicitly excludes the historical ESP/NIF/Blender pipeline.
3. `scripts/pex_metadata.py:23` anonymizes only non-executable compiler identity fields, and `scripts/compile_papyrus.py` disassembles the sanitized final PEX. All six PEX inside the archived Core payload have user `AstraAsedio` and computer `Build`; no former username/hostname remains in those headers.
4. `native/CMakeLists.txt:5` leaves include-prefix autodetection enabled by default and makes the local MSVC prefix an explicit optional override. The Source archive contains that corrected configuration and instructions.

Final archived-byte checks:

- Core: 25 entries, SHA256 `8d7ea6a571bdb19162d90f476129dd05ee3ccd3ddc0be3d069afab0d822b4818`.
- Whiterun Towers: 9 entries, SHA256 `0c4e9c299c7effc874eaf4626c601def1049f8c191609b687e81bf4f5cef8c7f`.
- Source: 30 entries, SHA256 `d49121c29451f7d72dfe88d08e37faebcd3e54d25f9cf481f609ed463d738101`.

Each actual ZIP passed CRC, duplicate-name, exact inventory and per-entry SHA256 checks against `reports/package_v19.json`. Shipped README and RELEASE_STATUS bytes match their current sources. All three contain the four dependency notices, including embedded fmt. The source archive excludes dependency trees, SDKs, pipeline configuration, Blender assets and runtime logs. Public text/source files contain no former workstation identity or private C:/E:/G: paths; the remaining DLL SDK diagnostic paths are explicitly disclosed. Atalaya is absent from all three public archives.

Current release gates are disclosed in `docs/nexus/RELEASE_STATUS.md:7`: v19 visibility/handoff engine verification, independent NPC ballistics and damage checks, save/update and camera-mod tests, custom navigation finalization, formal xEdit checks and supported WRLD/CELL parent cleanup, and a clean-machine dependency test. Two isolated xEdit attempts timed out; the documentation makes no pass or stable-release claim. The public README names the specific Tamriel WRLD/persistent CELL conflict instead of claiming broad mod compatibility.

Publication notes accurately distinguish custom modeling from Bethesda record/material/physics donors, retain upstream notices, leave original-asset permission choices to the publisher, and require AI-Generated Content and AI Media disclosure under the current Nexus rules. Keyboard/mouse-only fast firing, held-repeat controls, steel-bolt cost, explosive damage records, optional-addon dependency and uninstall-by-preinstallation-save guidance are present.
