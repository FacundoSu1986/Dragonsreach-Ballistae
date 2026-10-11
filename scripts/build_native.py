"""Build pinned local dependencies and the x64 SKSE DLL without global installs."""
from pathlib import Path
import argparse, os, subprocess, shutil, hashlib, json, datetime, sys
ROOT = Path(__file__).resolve().parents[1]
VS = Path(r'C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools')
MSVC = VS / 'VC/Tools/MSVC/14.51.36231'
SDK = Path(r'C:\Program Files (x86)\Windows Kits\10')
SDK_VERSION = '10.0.26100.0'
DEFAULT_VENDOR = ROOT/'build/native'
CMAKE = VS/'Common7/IDE/CommonExtensions/Microsoft/CMake/CMake/bin/cmake.exe'
CTEST = CMAKE.with_name('ctest.exe')
NINJA = VS/'Common7/IDE/CommonExtensions/Microsoft/CMake/Ninja/ninja.exe'
PINS = {
 'CommonLibSSE-NG': ('https://github.com/CharmedBaryon/CommonLibSSE-NG.git','b93280e832f263dbef44e44cbe2936622a02f91a'),
 'spdlog': ('https://github.com/gabime/spdlog.git','486b55554f11c9cccc913e11a87085b2a91f706f'),
 'rapidcsv': ('https://github.com/d99kris/rapidcsv.git','03133b59e17ca92ecf886b611d87a03ad2bb2a8f'),
}
def environment(vendor=DEFAULT_VENDOR):
 env=os.environ.copy()
 env['PATH']=str(MSVC/'bin/Hostx64/x64')+';'+str(SDK/'bin'/SDK_VERSION/'x64')+';'+env['PATH']
 local_sdk=vendor/'windows_sdk/Windows Kits/10'
 sdk=local_sdk if local_sdk.exists() else SDK
 env['INCLUDE']=';'.join(str(p) for p in [MSVC/'include',*[sdk/'Include'/SDK_VERSION/n for n in ['ucrt','shared','um','winrt']],*[SDK/'Include'/SDK_VERSION/n for n in ['shared','um','winrt']]])
 env['LIB']=';'.join(str(p) for p in [MSVC/'lib/x64',sdk/'Lib'/SDK_VERSION/'ucrt/x64',SDK/'Lib'/SDK_VERSION/'um/x64'])
 env['VSLANG']='1033'
 return env
def run(args,env):
 print(' '.join(map(str,args)),flush=True)
 subprocess.run(list(map(str,args)),cwd=ROOT,env=env,check=True)

def vendor_manifest(vendor):
 files={}
 for path in sorted(vendor.rglob('*')):
  if path.is_file():
   with path.open('rb') as source: digest=hashlib.file_digest(source,'sha256').hexdigest()
   files[path.relative_to(vendor).as_posix()]={'bytes':path.stat().st_size,'sha256':digest}
 return files
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--core-only',action='store_true');parser.add_argument('--build-dir',default='build/native/release-verified');parser.add_argument('--vendor-dir',type=Path,help='Reuse existing pinned dependencies and local SDK without modifying them');parser.add_argument('--no-receipt',action='store_true');args=parser.parse_args()
 vendor=(args.vendor_dir or DEFAULT_VENDOR).resolve();build=(ROOT/args.build_dir).resolve()
 if not build.is_relative_to(ROOT) or build==ROOT:
  raise RuntimeError('Build output must stay inside this project')
 if args.vendor_dir and build.is_relative_to(vendor):
  raise RuntimeError('Build output cannot write into the external vendor directory')
 local_sdk=vendor/'windows_sdk/Windows Kits/10'
 global_header=SDK/'Include'/SDK_VERSION/'ucrt/stdlib.h'
 if not local_sdk.exists() and (not global_header.is_file() or not any(global_header.read_bytes())):
  if args.vendor_dir:
   raise RuntimeError('External vendor SDK is unavailable; refusing to write into its directory')
  subprocess.run([sys.executable,str(ROOT/'native/prepare_local_sdk.py')],check=True)
 env=environment(vendor)
 vendor_before=vendor_manifest(vendor) if args.vendor_dir else None
 if not args.core_only:
  for name,(url,revision) in PINS.items():
   target=vendor/name
   if not target.exists():
    if args.vendor_dir: raise RuntimeError(f'Existing pinned dependency missing: {target}')
    run(['git','clone',url,target],env);run(['git','-C',target,'checkout','--detach',revision],env)
   actual=subprocess.check_output(['git','-C',str(target),'rev-parse','HEAD'],text=True).strip()
   if actual!=revision: raise RuntimeError(f'{name}: revision {actual} differs from pin {revision}')
 run([CMAKE,'-S',ROOT/'native','-B',build,'-G','Ninja',f'-DCMAKE_MAKE_PROGRAM={NINJA}','-DCMAKE_BUILD_TYPE=Release','-DASTRA_SHOWINCLUDES_PREFIX=Nota: inclusiÃƒÂ³n del archivo: ',f'-DASTRA_BUILD_PLUGIN={"OFF" if args.core_only else "ON"}',f'-DASTRA_VENDOR={vendor}'],env)
 run([CMAKE,'--build',build,'--parallel','4'],env)
 run([CTEST,'--test-dir',build,'--output-on-failure'],env)
 vendor_evidence=None
 if vendor_before is not None:
  vendor_after=vendor_manifest(vendor)
  changed=[name for name in vendor_before.keys()|vendor_after.keys() if vendor_before.get(name)!=vendor_after.get(name)]
  if changed: raise RuntimeError('Read-only vendor inputs changed: '+', '.join(sorted(changed)))
  manifest_path=ROOT/'reports/native_vendor_manifest.json'
  vendor_evidence={'vendor_dir':str(vendor),'immutable':True,'comparison':'Full SHA256/byte-length file manifest before and after pin checks, CMake, build and CTest','file_count':len(vendor_before),'total_bytes':sum(item['bytes'] for item in vendor_before.values()),'files':vendor_before}
  manifest_path.write_text(json.dumps(vendor_evidence,indent=2),encoding='utf-8')
  vendor_evidence={'report':str(manifest_path.relative_to(ROOT)),'sha256':hashlib.sha256(manifest_path.read_bytes()).hexdigest(),'immutable':True,'file_count':vendor_evidence['file_count'],'total_bytes':vendor_evidence['total_bytes']}
 if not args.core_only:
  destination=ROOT/'mod/SKSE/Plugins/AstraSight.dll';destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(build/'AstraSight.dll',destination)
  if not args.no_receipt:
   files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['native'] for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
   for p in [ROOT/'scripts/build_native.py',ROOT/'mod/scripts/source/AstraSightNative.psc',ROOT/'mod/scripts/source/AstraAsedioActi.psc',ROOT/'mod/scripts/source/AstraGuardNative.psc']:
    files[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
   files[str(destination.relative_to(ROOT))]=hashlib.sha256(destination.read_bytes()).hexdigest()
   result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'project_root':str(ROOT),'build_dir':str(build.relative_to(ROOT)),'vendor_dir':str(vendor),'external_vendor_read_only':bool(args.vendor_dir),'vendor_manifest':vendor_evidence,'runtime':'1.6.1170.0','skse_minimum':'2.2.8','architecture':'AMD64','plugin_name':'AstraSight','plugin_version':50659472,'plugin_version_string':'3.5.9','api_version':4,'pitch_limits_degrees':[-20.0,80.0],'per_session_aim_limits':True,'native_release_seconds':1/15,'nominal_cycle_seconds':1.0,'projectile_critical_path':'native input, game-thread effects, no VM tick','engine_latency_measured':False,'tasklet_callable_session_api':True,'dependencies':PINS,'files_sha256':files,'in_game_verified':False}
   result.update({'npc_api_version':1,'npc_clip_seconds':{'hold':2.0,'body_fire':1.0,'turn_left':0.8,'turn_right':0.8},'npc_yaw_limits_degrees':[-60.0,60.0],'npc_pitch_degrees':0.0,'npc_visual_radius_units':2100.0,'npc_fire_range_units':6000.0,'npc_maximum_turn_degrees_per_second':15.0,'npc_projectile_speed':5400.0,'npc_gravity_units':240.345,'npc_frame_pump':'PlayerCharacter::Update vfunc0xAD, independent of FirstPersonState/camera','npc_post_ik_order_in_game_verified':False,'npc_reference_scale':1.0,'npc_natural_height_range':[0.9,1.1],'npc_grip_max_correction_units':16.0,'npc_grip_required_before_fire_and_launch':True,'npc_resident_factions':{'Skyrim.esm':[0x28172,0x2BE39]},'npc_pose_reaffirmed_each_update':True,'npc_assigned_package_and_oar_authority':True,'npc_pose_consumed_on_main_pump':True,'npc_character_update_telemetry_only':True,'npc_shield_veto_acquire_and_context':True,'npc_context_failures_log_exact_clause':True})
   (ROOT/'reports/native_build_receipt.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
   sdk=local_sdk if local_sdk.exists() else SDK
   sdk_header=sdk/'Include'/SDK_VERSION/'ucrt/stdlib.h'
   sdk_result={'utc':result['utc'],'project_root':str(ROOT),'sdk_root':str(sdk),'sdk_version':SDK_VERSION,'operation':'Reuse existing SDK inputs in place; no extraction or installation','external_vendor_read_only':bool(args.vendor_dir),'stdlib_header_sha256':hashlib.sha256(sdk_header.read_bytes()).hexdigest()}
   (ROOT/'reports/native_sdk_receipt.json').write_text(json.dumps(sdk_result,indent=2),encoding='utf-8')
if __name__=='__main__':main()
