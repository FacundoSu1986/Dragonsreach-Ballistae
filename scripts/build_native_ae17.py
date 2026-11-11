"""Build the Skyrim 1.7.104 variant of AstraSight.dll (experimental; untested in game).

Dependencies: build/native-ae17/CommonLibSSE-NG (alandtse fork, pinned below, GPL-3.0-or-later with exceptions) and
build/native-ae17/vcpkg_installed (scripts/vcpkg_ae17.py). Output: build/native/ae17/AstraSight.dll; the 1.6.1170 DLL
in mod/SKSE/Plugins is not touched.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_native as B  # noqa: E402

COMMONLIB = ('https://github.com/alandtse/CommonLibSSE-NG.git', '67b201b6fe45241ac5c1e4630ecf847523775b66')
VENDOR = ROOT / 'build/native-ae17'
BUILD = ROOT / 'build/native/ae17'
TRIPLET = 'x64-windows-static-md-astra'


def main():
    head = subprocess.check_output(['git', '-C', str(VENDOR / 'CommonLibSSE-NG'), 'rev-parse', 'HEAD'], text=True).strip()
    if head != COMMONLIB[1]:
        raise SystemExit(f'CommonLibSSE-NG at {head}, pin is {COMMONLIB[1]}')
    env = B.environment(ROOT / 'build/native')
    sdk = ROOT / 'build/native/windows_sdk/Windows Kits/10'
    ucrt_inc = (sdk / 'Include/10.0.26100.0/ucrt').as_posix()
    toolchain = B.VS / 'VC/vcpkg/scripts/buildsystems/vcpkg.cmake'
    B.run([B.CMAKE, '-S', ROOT / 'native', '-B', BUILD, '-G', 'Ninja', f'-DCMAKE_MAKE_PROGRAM={B.NINJA}',
           '-DCMAKE_BUILD_TYPE=Release', '-DASTRA_AE17=ON', f'-DASTRA_VENDOR={VENDOR}',
           f'-DCMAKE_TOOLCHAIN_FILE={toolchain}', f'-DVCPKG_INSTALLED_DIR={VENDOR / "vcpkg_installed"}',
           f'-DVCPKG_TARGET_TRIPLET={TRIPLET}', f'-DVCPKG_OVERLAY_TRIPLETS={VENDOR / "triplets"}', '-DVCPKG_MANIFEST_MODE=OFF',
           f'-DCMAKE_CXX_STANDARD_INCLUDE_DIRECTORIES={ucrt_inc}', f'-DCMAKE_C_STANDARD_INCLUDE_DIRECTORIES={ucrt_inc}',
           '-DASTRA_SHOWINCLUDES_PREFIX=Nota: inclusiÃƒÂ³n del archivo: '], env)
    B.run([B.CMAKE, '--build', BUILD, '--parallel', '4', '--target', 'AstraSight'], env)
    print('AE17_DLL', BUILD / 'AstraSight.dll')


if __name__ == '__main__':
    main()
