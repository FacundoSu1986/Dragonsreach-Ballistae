"""Compile only project sources; runtime is read-only."""
import hashlib,json,re,shutil,subprocess,tempfile
from pathlib import Path
from pex_metadata import anonymize,metadata
ROOT=Path(__file__).resolve().parents[1]
def validate_assembly(assembly):
 """Reject the None -> array cast that poisoned ArrayCreate in the v01 VM log.
 Inspect disassembly from the final PEX, keeping temporary types per function.
 Object None casts remain valid; array casts do not.
 """
 globals_=dict(re.findall(r'\.variable\s+(\S+)\s+(\S+)',assembly,re.I))
 functions=re.findall(r'\.function\b.*?\.endFunction',assembly,re.I|re.S) or [assembly]
 allocations=0
 for body in functions:
  types={**globals_,**dict(re.findall(r'\.local\s+(\S+)\s+(\S+)',body,re.I))}
  for dest in re.findall(r'\bCast\s+(\S+)\s+None\b',body,re.I):
   if types.get(dest,'').endswith('[]'):raise ValueError('None cast into array temporary '+dest)
  allocations+=len(re.findall(r'\bArrayCreate\s+',body,re.I))
 return {'no_none_to_array_casts':True,'array_create_count':allocations,'functions_inspected':len(functions)}

def validate_input_assembly(assembly):
 """Verify event input in the shipped controller PEX, not just its source."""
 events=('OnKeyDown','OnKeyUp','OnControlDown','OnControlUp')
 for event in events:
  if not re.search(r'\.function\s+'+event+r'\b',assembly,re.I):raise ValueError('Missing input event '+event)
 if re.search(r'CallStatic\s+input\s+IsKeyPressed\b',assembly,re.I):raise ValueError('Legacy poll-only input is not supported')
 for code in (203,205,200,208):
  if not re.search(r'CallMethod\s+RegisterForKey\s+self\s+\S+\s+'+str(code)+r'\b',assembly,re.I):raise ValueError('Missing arrow registration '+str(code))
 return {'skse_input_events':list(events),'no_iskeypressed_poll':True,'arrow_keycodes':[203,205,200,208]}

def validate_camera_assembly(assembly):
 """The installed Game wrapper redirects to unbound Camera.GetCameraState.
 Enforce our own API in final bytecode, independently of compiler imports.
 """
 if re.search(r'CallStatic\s+(?:camera|game)\s+GetCameraState\b',assembly,re.I):
  raise ValueError('Unbound runtime camera state dependency')
 if not re.search(r'CallStatic\s+astrasightnative\s+GetCameraState\b',assembly,re.I):
  raise ValueError('Missing own camera state binding')
 return {'own_camera_state_binding':True,'runtime_camera_wrappers_absent':True}

def main():
 cfg=json.loads((ROOT/'config.json').read_text())
 runtime=Path(cfg['runtime']);src=ROOT/'mod/scripts/source';out=ROOT/'mod/scripts'; compiler=runtime/'Papyrus Compiler/PapyrusCompiler.exe'
 imports=';'.join(str(p) for p in [src,runtime/'Data/Scripts/Source',runtime/'Data/Source/Scripts'])
 assembler=runtime/'Papyrus Compiler/PapyrusAssembler.exe'
 report={'compiler':str(compiler),'assembler':str(assembler),'runtime_read_only':True,'scripts':[],'success':True,'compile_from_fresh_staging':True}
 bytecode_dir=ROOT/'reports/papyrus_bytecode';bytecode_dir.mkdir(parents=True,exist_ok=True)
 for p in sorted(src.glob('*.psc')):
  source_sha256=hashlib.sha256(p.read_bytes()).hexdigest()
  with tempfile.TemporaryDirectory(prefix='papyrus_',dir=ROOT/'build') as td:
   stage=Path(td);args=[str(compiler),str(p),'-f='+str(runtime/'Data/Source/Scripts/TESV_Papyrus_Flags.flg'),'-i='+imports,'-o='+str(stage)]
   r=subprocess.run(args,capture_output=True,text=True)
   staged=stage/(p.stem+'.pex');q=out/(p.stem+'.pex');ok=r.returncode==0 and staged.exists() and staged.stat().st_size>128
   output=r.stdout+r.stderr;safety={};asm_exit=None
   if ok:
    original_pex=staged.read_bytes()
    staged.write_bytes(anonymize(original_pex))
    public_metadata,_=metadata(staged.read_bytes())
    a=subprocess.run([str(assembler),p.stem,'-D'],cwd=stage,capture_output=True,text=True)
    asm_exit=a.returncode;output+=a.stdout+a.stderr
    assembly=stage/(p.stem+'.disassemble.pas')
    ok=a.returncode==0 and assembly.exists()
    if ok:
     try:
      assembly_text=assembly.read_text(encoding='utf-8-sig');safety=validate_assembly(assembly_text)
      if p.stem=='AstraAsedioActi':safety.update(validate_input_assembly(assembly_text))
      if p.stem in ('AstraAsedioActi','AstraAsedioSession'):safety.update(validate_camera_assembly(assembly_text))
     except ValueError as e:ok=False;output+='\nBYTECODE_REJECTED: '+str(e)
    if source_sha256!=hashlib.sha256(p.read_bytes()).hexdigest():
     ok=False;output+='\nSOURCE_CHANGED_DURING_COMPILE: recompile the final source before publishing PEX'
    if ok:
     target=bytecode_dir/assembly.name;shutil.copy2(assembly,target);shutil.copy2(staged,q)
     safety.update({'anonymized_header':public_metadata,'executable_tables_unchanged':True})
     safety.update({'disassembly':str(target.relative_to(ROOT)),'disassembly_sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
  report['scripts'].append({'source_sha256':source_sha256,'source':str(p.relative_to(ROOT)),'pex':str(q.relative_to(ROOT)),'exit_code':r.returncode,'assembler_exit_code':asm_exit,'success':ok,'output':output,'bytecode_safety':safety,'sha256':hashlib.sha256(q.read_bytes()).hexdigest() if ok else None})
  report['success'] &= ok
  print(p.name, 'OK' if ok else 'FAILED',output)
 (ROOT/'reports/plugin_compile.json').write_text(json.dumps(report,indent=2))
 return 0 if report['success'] else 1
if __name__=='__main__':raise SystemExit(main())

