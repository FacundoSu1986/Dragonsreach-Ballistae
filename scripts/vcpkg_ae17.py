"""Install the dependencies of the 1.7.104 CommonLibSSE-NG fork with the Visual Studio bundled vcpkg, using the same
compiler/SDK environment as scripts/build_native.py (local Windows SDK copy) and an overlay triplet that does not load
vcvars. Output: build/native-ae17/vcpkg_installed."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_native as B  # noqa: E402

VENDOR = ROOT / 'build/native-ae17'
VCPKG = B.VS / 'VC/vcpkg/vcpkg.exe'
TRIPLET = 'x64-windows-static-md-astra'


def main():
    env = B.environment(ROOT / 'build/native')
    args = [str(VCPKG), 'install', f'--x-manifest-root={VENDOR / "CommonLibSSE-NG"}',
            f'--x-install-root={VENDOR / "vcpkg_installed"}', f'--overlay-triplets={VENDOR / "triplets"}',
            f'--triplet={TRIPLET}', f'--host-triplet={TRIPLET}', '--x-no-default-features']
    r = subprocess.run(args, cwd=ROOT, env=env)
    sys.exit(r.returncode)


if __name__ == '__main__':
    main()
