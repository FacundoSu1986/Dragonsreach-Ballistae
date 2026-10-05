"""Install only into our own MO2 mod/profile; do not select or launch it."""
from pathlib import Path
import json, shutil, configparser, hashlib, re
ROOT=Path(__file__).resolve().parents[1]
MO2=Path('G:/Modding/MO2/SkyrimSE')
NAME='AstraAsedio_QA_v10'
DEPENDENCY='Address Library All in One'
mo2_ini=Path('C:/Users/Facu2/AppData/Local/ModOrganizer/Skyrim Special Edition/ModOrganizer.ini')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def selected_profile():
    match=re.search(r'^selected_profile=@ByteArray\(([^\r\n)]*)\)',mo2_ini.read_text(encoding='utf-8-sig'),re.M)
    if not match: raise RuntimeError('Cannot verify the saved MO2 profile selection')
    return match.group(1)
previous_selection=selected_profile()
if previous_selection==NAME:
    raise RuntimeError('The managed profile is currently selected; preserve it until Skyrim is closed and a different profile is selected')
address_library=MO2/'mods'/DEPENDENCY/'SKSE/Plugins/versionlib-1-6-1170-0.bin'
if not address_library.is_file():
    raise RuntimeError('Required existing 1.6.1170 Address Library is unavailable')
ini_before=sha(mo2_ini)
previous_profile=MO2/'profiles'/previous_selection
previous_files={p.name:sha(p) for p in previous_profile.iterdir() if p.is_file()}
mod=MO2/'mods'/NAME; profile=MO2/'profiles'/NAME
for destination in (mod,profile):
    if destination.exists():
        marker=destination/'astra_managed.json'
        if not marker.is_file() or json.loads(marker.read_text()).get('project')!=str(ROOT):
            raise RuntimeError('Destination is not owned by this build: '+str(destination))
    destination.mkdir(parents=True,exist_ok=True)
    (destination/'astra_managed.json').write_text(json.dumps({'project':str(ROOT),'purpose':'independent test profile'}))
shutil.copytree(ROOT/'mod',mod,dirs_exist_ok=True)
(mod/'meta.ini').write_text('[General]\ngameName=Skyrim Special Edition\nname=Ballesta Astra de asedio v10 QA\nversion=0.10.0-alpha\n',encoding='utf-8')
default=MO2/'profiles/Default'
for name in ('skyrim.ini','skyrimprefs.ini','archives.txt'):
    shutil.copy2(default/name,profile/name)
ini=configparser.ConfigParser(strict=False); ini.optionxform=str; ini.read(profile/'skyrim.ini',encoding='utf-8-sig')
for section in ('General','Papyrus','Actor'):
    if not ini.has_section(section): ini.add_section(section)
for key,val in [('bEnableLogging','1'),('bEnableTrace','1'),('bLoadDebugInformation','1')]: ini['Papyrus'][key]=val
ini['Actor']['bUseNavMeshForMovement']='1'
with (profile/'skyrim.ini').open('w',encoding='utf-8') as f: ini.write(f)
(profile/'settings.ini').write_text('[General]\nLocalSaves=true\nLocalSettings=true\nAutomaticArchiveInvalidation=true\n')
(profile/'saves').mkdir(exist_ok=True)
(profile/'modlist.txt').write_text('# Managed Astra independent QA profile\n'+''.join(('+' if p.name in (NAME,DEPENDENCY) else '-')+p.name+'\n' for p in sorted((MO2/'mods').iterdir()) if p.is_dir()),encoding='utf-8')
order=['Skyrim.esm','Update.esm','Dawnguard.esm','HearthFires.esm','Dragonborn.esm','AstraAsedio.esp']
(profile/'loadorder.txt').write_text('\n'.join(order)+'\n',encoding='utf-8')
(profile/'plugins.txt').write_text('*AstraAsedio.esp\n',encoding='utf-8')
for name in ('lockedorder.txt','initweaks.ini','skyrimcustom.ini'):
    if not (profile/name).exists(): (profile/name).write_text('')
selection_unchanged=selected_profile()==previous_selection
previous_files_unchanged=previous_files=={p.name:sha(p) for p in previous_profile.iterdir() if p.is_file()}
if not selection_unchanged or not previous_files_unchanged or sha(mo2_ini)!=ini_before:
    raise RuntimeError('The previous MO2 configuration changed during preparation; inspect before continuing')
installed_hashes={str(p.relative_to(mod)):sha(p) for p in mod.rglob('*') if p.is_file() and p.name not in ('meta.ini','astra_managed.json')}
source_hashes={str(p.relative_to(ROOT/'mod')):sha(p) for p in (ROOT/'mod').rglob('*') if p.is_file()}
if installed_hashes!=source_hashes: raise RuntimeError('The installed QA mod does not match the verified project files')
report={'mod':str(mod),'profile':str(profile),'profile_selected':False,'game_launched':False,'enabled_mo2_mods':[NAME,DEPENDENCY],'address_library':str(address_library),'address_library_sha256':sha(address_library),'local_saves':True,'local_ini':True,'runtime':'G:/Modding/Skyrim_Runtime_1.6.1170','esp_sha256':sha(mod/'AstraAsedio.esp'),'previous_selected_profile':previous_selection,'previous_profile_files_unchanged':previous_files_unchanged,'mo2_ini_unchanged':True,'installed_files_match_project':True,'installed_sha256':installed_hashes}
(ROOT/'reports/test_profile.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
