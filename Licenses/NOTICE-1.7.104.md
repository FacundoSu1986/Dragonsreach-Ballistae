# License notice — AstraSight.dll, Skyrim 1.7.104 build (experimental)

This variant of the SKSE plugin is built against the maintained fork of CommonLibSSE-NG by alandtse,
https://github.com/alandtse/CommonLibSSE-NG at commit `67b201b6fe45241ac5c1e4630ecf847523775b66` (version 12.2.0),
which is licensed **GPL-3.0-or-later** with the *Modding Exception* and the *GPL-3.0 Linking Exception*
(`CommonLibSSE-NG-alandtse-COPYING.txt`, `CommonLibSSE-NG-alandtse-EXCEPTIONS.md`).

* The AstraSight C++ source (`native/` in the source archive) is offered under **GPL-3.0-or-later** for this build.
  The 1.6.1170 build links the MIT-licensed CommonLibSSE-NG commit `b93280e` (CharmedBaryon) and is not affected
  by this notice.
* **Corresponding Source**: `DragonsreachBallistae-1.0.0-source-AE1.7.104-GPL.zip`, published next to this file on the
  mod page. It holds the AstraSight source and build scripts, the exact CommonLibSSE-NG source at the commit above and
  the source of the libraries linked into the DLL (fmt, spdlog, DirectXTK, DirectXMath, nlohmann-json, rapidcsv,
  SimpleIni, toml11, xbyak), each with its own license text (also copied here as `*-LICENSE`).
* Skyrim itself is the "Modded Code" covered by the Modding Exception; Papyrus scripts, plugins and meshes of the mod
  are separate works and not covered by the GPL.

There is NO WARRANTY, to the extent permitted by law (GPL-3.0 sections 15 and 16).
