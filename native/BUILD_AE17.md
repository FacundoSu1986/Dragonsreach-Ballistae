# Building AstraSight.dll for Skyrim 1.7.104

Requirements: Visual Studio 2022+ Build Tools (MSVC, C++23), CMake 3.26+, Ninja, vcpkg, Windows 10 SDK.

Layout of this archive:

* `native/` — AstraSight source (`CMakeLists.txt`, `src/`, `include/`).
* `third_party/CommonLibSSE-NG/` — alandtse fork at commit `67b201b6fe45241ac5c1e4630ecf847523775b66`.
* `third_party/vcpkg-sources/<port>/` — sources of the vcpkg ports linked into the DLL (versions in `VERSIONS.txt`).

Steps (from the archive root):

```
vcpkg install --x-manifest-root=third_party/CommonLibSSE-NG --x-install-root=vcpkg_installed --triplet=x64-windows-static-md
cmake -S native -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DASTRA_AE17=ON -DASTRA_VENDOR=<archive root>/third_party
      -DCMAKE_TOOLCHAIN_FILE=<vcpkg>/scripts/buildsystems/vcpkg.cmake -DVCPKG_INSTALLED_DIR=vcpkg_installed
      -DVCPKG_TARGET_TRIPLET=x64-windows-static-md -DVCPKG_MANIFEST_MODE=OFF
cmake --build build --target AstraSight
```

`ASTRA_VENDOR` must be the folder that contains `CommonLibSSE-NG`. The release DLL was built this way with the
Visual Studio bundled vcpkg (the author's machine used an overlay triplet only to point at a local copy of the
Windows SDK; it changes no compiler or library option). `build_native_ae17.py` and `vcpkg_ae17.py` are the author's
wrappers, included for reference.
