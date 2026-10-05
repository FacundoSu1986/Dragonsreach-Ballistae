"""Build pinned local dependencies and the x64 SKSE DLL without global installs."""
from pathlib import Path
import argparse, os, subprocess, shutil, hashlib, json, datetime, sys
ROOT = Path(__file__).resolve().parents[1]
VS = Path(r'C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools')
MSVC = VS / 'VC/Tools/MSVC/14.51.36231'
SDK = Path(r'C:\Program Files (x86)\Windows Kits\10')
SDK_VERSION = '10.0.26100.0'
LOCAL_SDK = ROOT/'build/native/windows_sdk/Windows Kits/10'
CMAKE = VS/'Common7/IDE/CommonExtensions/Microsoft/CMake/CMake/bin/cmake.exe'
CTEST = CMAKE.with_name('ctest.exe')
NINJA = VS/'Common7/IDE/CommonExtensions/Microsoft/CMake/Ninja/ninja.exe'
PINS = {
 'CommonLibSSE-NG': ('https://github.com/CharmedBaryon/CommonLibSSE-NG.git','b93280e832f263dbef44e44cbe2936622a02f91a'),
 'spdlog': ('https://github.com/gabime/spdlog.git','486b55554f11c9cccc913e11a87085b2a91f706f'),
 'rapidcsv': ('https://github.com/d99kris/rapidcsv.git','03133b59e17ca92ecf886b611d87a03ad2bb2a8f'),
}
def environment():
 env=os.environ.copy()
 env['PATH']=str(MSVC/'bin/Hostx64/x64')+';'+str(SDK/'bin'/SDK_VERSION/'x64')+';'+env['PATH']
 sdk=LOCAL_SDK if LOCAL_SDK.exists() else SDK
 env['INCLUDE']=';'.join(str(p) for p in [MSVC/'include',*[sdk/'Include'/SDK_VERSION/n for n in ['ucrt','shared','um','winrt']],*[SDK/'Include'/SDK_VERSION/n for n in ['shared','um','winrt']]])
 env['LIB']=';'.join(str(p) for p in [MSVC/'lib/x64',sdk/'Lib'/SDK_VERSION/'ucrt/x64',SDK/'Lib'/SDK_VERSION/'um/x64'])
 env['VSLANG']='1033'
 return env
def run(args,env):
 print(' '.join(map(str,args)),flush=True)
 subprocess.run(list(map(str,args)),cwd=ROOT,env=env,check=True)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--core-only',action='store_true');parser.add_argument('--build-dir',default='build/native/release-verified');parser.add_argument('--no-receipt',action='store_true');args=parser.parse_args()
 if not LOCAL_SDK.exists() and not any((SDK/'Include'/SDK_VERSION/'ucrt/stdlib.h').read_bytes()):
  subprocess.run([sys.executable,str(ROOT/'native/prepare_local_sdk.py')],check=True)
 env=environment();build=ROOT/args.build_dir
 if not args.core_only:
  for name,(url,revision) in PINS.items():
   target=ROOT/'build/native'/name
   if not target.exists():
    run(['git','clone',url,target],env);run(['git','-C',target,'checkout','--detach',revision],env)
   actual=subprocess.check_output(['git','-C',str(target),'rev-parse','HEAD'],text=True).strip()
   if actual!=revision: raise RuntimeError(f'{name}: revision {actual} differs from pin {revision}')
 run([CMAKE,'-S',ROOT/'native','-B',build,'-G','Ninja',f'-DCMAKE_MAKE_PROGRAM={NINJA}','-DCMAKE_BUILD_TYPE=Release',f'-DASTRA_BUILD_PLUGIN={"OFF" if args.core_only else "ON"}'],env)
 run([CMAKE,'--build',build,'--parallel','4'],env)
 run([CTEST,'--test-dir',build,'--output-on-failure'],env)
 if not args.core_only:
  destination=ROOT/'mod/SKSE/Plugins/AstraSight.dll';destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(build/'AstraSight.dll',destination)
  if not args.no_receipt:
   files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['native'] for p in (ROOT/folder).rglob('*') if p.is_file()}
   for p in [ROOT/'scripts/build_native.py',ROOT/'mod/scripts/source/AstraSightNative.psc']:
    files[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
   files[str(destination.relative_to(ROOT))]=hashlib.sha256(destination.read_bytes()).hexdigest()
   result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runtime':'1.6.1170.0','skse_minimum':'2.2.8','architecture':'AMD64','plugin_name':'AstraSight','plugin_version':50528256,'api_version':3,'tasklet_callable_session_api':True,'dependencies':PINS,'files_sha256':files,'in_game_verified':False}
   (ROOT/'reports/native_build_receipt.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
if __name__=='__main__':main()
