"""Read-only installation/log evidence. Saves only Astra-related log excerpts."""
from pathlib import Path
import datetime,hashlib,json,re,sys

ROOT=Path(__file__).resolve().parents[2]
V01=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v01')
MO2=Path('G:/Modding/MO2/SkyrimSE')
PROFILE=MO2/'profiles/PruebaEmpaquetado'
DOCS=Path(sys.argv[1])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

modlist=PROFILE/'modlist.txt'
enabled=[s[1:].strip() for s in modlist.read_text(encoding='utf-8-sig').splitlines() if s.startswith('+')]
plugins=PROFILE/'plugins.txt'
plugin_lines=plugins.read_text(encoding='utf-8-sig').splitlines()
artifacts=['AstraAsedio.esp','AstraAsedio_Despejado.esp','scripts/AstraAsedioActi.pex','scripts/AstraAsedioSession.pex','scripts/AstraAsedioPlayerAlias.pex','seq/AstraAsedio.seq']
installed=[]
for artifact in artifacts:
 candidates=[MO2/'mods'/m/artifact for m in enabled if (MO2/'mods'/m/artifact).exists()]
 override=MO2/'overwrite'/artifact
 if override.exists():candidates.insert(0,override)
 installed.append({'artifact':artifact,'enabled_mod_candidates':[{'path':str(p),'sha256':sha(p),'matches_v01':(V01/'mod'/artifact).exists() and sha(p)==sha(V01/'mod'/artifact),'matches_v02':(ROOT/'mod'/artifact).exists() and sha(p)==sha(ROOT/'mod'/artifact)} for p in candidates],'unambiguous_effective_file':len(candidates)==1})

logs=[];errors=[]
for p in sorted((DOCS/'My Games/Skyrim Special Edition/Logs/Script').glob('Papyrus.*.log')):
 lines=p.read_text(encoding='utf-8',errors='replace').splitlines()
 matches=[]
 for i,line in enumerate(lines):
  if 'error:' not in line:continue
  block=[line]
  for following in lines[i+1:i+8]:
   if following.startswith('['):break
   block.append(following)
  if any('AstraAsedio' in s for s in block):
   matches.append({'line':i+1,'excerpt':'\n'.join(block)})
 if matches:
  counts={}
  for m in matches:
   error=m['excerpt'].split('error:',1)[1].splitlines()[0].strip();counts[error]=counts.get(error,0)+1
  # Preserve one observed example for each failure type and caller, never other-mod log contents.
  examples={}
  for m in matches:
   error=m['excerpt'].split('error:',1)[1].splitlines()[0].strip()
   caller='OnActivate' if '.OnActivate()' in m['excerpt'] else 'OnLoad'
   examples.setdefault((error,caller),m)
  logs.append({'path':str(p),'sha256':sha(p),'modified':datetime.datetime.fromtimestamp(p.stat().st_mtime).isoformat(),'astra_error_counts':counts,'examples':list(examples.values())})

report={'collected_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'documents_resolved_by':'[Environment]::GetFolderPath(MyDocuments)','documents':str(DOCS),'profile_read_only':str(PROFILE),'profile_modlist_sha256':sha(modlist),'profile_plugins_sha256':sha(plugins),'enabled_astra_plugins':[s for s in plugin_lines if s.lstrip('*').lower().startswith('astra')],'installed_files':installed,'astra_only_log_evidence':logs,'runtime_or_mo2_written':False,'saved_games_read_or_written':False,'native_apps_started':False,'in_game_fix_verified':False}
(ROOT/'reports/runtime_diagnostic/evidence.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'installed':[(i['artifact'],[(c['matches_v01'],c['matches_v02']) for c in i['enabled_mod_candidates']]) for i in installed],'logs':[(i['path'],i['astra_error_counts']) for i in logs]},indent=2))
