"""Run official xEdit scripting checks on isolated copies, never runtime files."""
from pathlib import Path
import subprocess,shutil,json,hashlib,re,datetime
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'build/xedit_v19'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

SCRIPT='''unit AstraReadOnly;
var failures: Integer;
procedure Scan(e: IInterface);
var i: Integer; error: string;
begin
  error := Check(e);
  if error <> '' then begin
    Inc(failures);
    AddMessage('ASTRA_ERROR ' + Name(e) + ' -> ' + error);
  end;
  for i := 0 to ElementCount(e)-1 do Scan(ElementByIndex(e,i));
end;
function Initialize: Integer;
var i: Integer; f: IInterface; n: string;
begin
  failures := 0;
  AddMessage('ASTRA_CHECK_BEGIN');
  for i := 0 to FileCount-1 do begin
    f := FileByIndex(i); n := GetFileName(f);
    if Pos('AstraAsedio',n)=1 then begin
      AddMessage('ASTRA_FILE ' + n);
      Scan(f);
    end;
  end;
  AddMessage('ASTRA_CHECK_END errors=' + IntToStr(failures));
end;
function Process(e: IInterface): Integer;
begin
end;
end.
'''

def main():
    cfg=json.loads((ROOT/'config.json').read_text());runtime=Path(cfg['runtime'])
    folders={n:WORK/n for n in ('Data','Scripts','Cache','Backups','Temp','Ini','Saves')}
    for p in folders.values():p.mkdir(parents=True,exist_ok=True)
    originals=[runtime/'Data'/n for n in ('Skyrim.esm','Update.esm','Dawnguard.esm','HearthFires.esm','Dragonborn.esm')]
    originals += [ROOT/'mod/AstraAsedio.esp',ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp',ROOT/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp']
    hashes={str(p):sha(p) for p in originals}
    for p in originals:
        target=folders['Data']/p.name
        if not target.exists() or sha(target)!=hashes[str(p)]:shutil.copy2(p,target)
    exe=WORK/'SSEEdit.exe'
    shutil.copy2(Path(r'G:\Modding\SSEDIT\SSEEdit 4.1.5f\SSEEdit.exe'),exe)
    script=folders['Scripts']/'AstraReadOnly.ssepas';script.write_text(SCRIPT)
    plugins=WORK/'plugins.txt';plugins.write_text('\n'.join('*'+p.name for p in originals)+'\n')
    (folders['Ini']/'Skyrim.ini').write_text('[General]\nsLanguage=ENGLISH\n')
    log=WORK/'check.log'
    args=[str(exe),'-SSE','-autoload','-autoexit','-NoAutoMarkModified',f'-script:{script}',f'-P:{plugins}',f'-R:{log}']
    args += [f'-{flag}:{folders[n]}\\' for flag,n in [('D','Data'),('S','Scripts'),('C','Cache'),('B','Backups'),('T','Temp'),('M','Ini'),('G','Saves')]]
    args += [f'-I:{folders["Ini"] / "Skyrim.ini"}']
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'attempted':True,'read_only_script':True,'isolated_copies':True,'command':args}
    try:
        p=subprocess.run(args,cwd=WORK,startupinfo=startup,timeout=55,capture_output=True,text=True)
        result['exit_code']=p.returncode
    except subprocess.TimeoutExpired:
        result.update(timed_out=True,limitation='Script execution did not finish within the bounded noninteractive run')
    raw=log.read_text(encoding='utf-8-sig',errors='replace') if log.exists() else ''
    end=re.search(r'ASTRA_CHECK_END errors=(\d+)',raw)
    result.update(completed=bool(end),errors=int(end[1]) if end else None,files_checked=re.findall(r'ASTRA_FILE (AstraAsedio[^\r\n]+)',raw),log=str(log.relative_to(ROOT)),log_sha256=sha(log) if log.exists() else None)
    assert all(sha(p)==hashes[str(p)] for p in originals),'Original input modified'
    result.update(originals_unchanged=True,input_sha256=hashes,success=bool(end) and int(end[1])==0 and len(result['files_checked'])==3)
    (ROOT/'reports/xedit_v19.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ('command','input_sha256')},indent=2))
    print('\n'.join(raw.splitlines()[-22:]))
if __name__=='__main__':main()
