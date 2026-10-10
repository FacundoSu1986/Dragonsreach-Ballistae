"""Seal the two reviewed v14 MO2 archives with current documentation only."""
import json,hashlib,zipfile,sys,subprocess,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def zip_package(name,entries):
    path=ROOT/'dist'/name
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=False) as z:
        for name,p in sorted(entries.items()):z.write(p,name)
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
        assert set(z.namelist())==set(entries)
        for n,p in entries.items():assert hashlib.sha256(z.read(n)).hexdigest()==sha(p),n
    return {'path':str(path),'bytes':path.stat().st_size,'sha256':sha(path),'entries':len(entries),'crc_and_hashes_verified':True}
def main():
    reviewed=json.loads((ROOT/'reports/review_v14.json').read_text());assert reviewed['approved'],'Review pending'
    for n,h in reviewed['files_sha256'].items():assert sha(ROOT/n)==h,('Reviewed file changed',n)
    verification=json.loads((ROOT/'reports/verification_v14.json').read_text());assert verification['success']
    for n,h in verification['files_sha256'].items():assert sha(ROOT/n)==h,('Unverified payload changed',n)
    for n,h in verification['reports_sha256'].items():assert sha(ROOT/'reports'/n)==h,('Unverified report changed',n)
    plugins=[ROOT/'mod/AstraAsedio.esp',ROOT/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp',ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp']
    before=[sha(p) for p in plugins]
    subprocess.run([sys.executable,str(ROOT/'scripts/build_modular_v14.py')],cwd=ROOT,check=True)
    assert before==[sha(p) for p in plugins],'Plugins not idempotent'
    staging=ROOT/'build/package_v14';staging.mkdir(exist_ok=True)
    docs={}
    for src,dst in [('README_v14.md','README.md'),('PRUEBAS_v14.md','PRUEBAS_EN_JUEGO.md'),('VALIDACION_v14.md','VALIDACION_v14.md')]:
        target=staging/dst;target.write_bytes((ROOT/'docs'/src).read_bytes());docs['Docs/AstraAsedio/'+dst]=target
    for report,name in [('modular_v14.json','COMPATIBILIDAD_v14.json'),('towers_v14.json','TORRES_v14.json')]:
        target=staging/name;target.write_bytes((ROOT/'reports'/report).read_bytes());docs['Docs/AstraAsedio/'+name]=target
    for p in (ROOT/'native/licenses').iterdir():
        if p.is_file():docs['Docs/AstraAsedio/Licenses/'+p.name]=p
    core={p.relative_to(ROOT/'mod').as_posix():p for p in (ROOT/'mod').rglob('*') if p.is_file() and p.suffix.lower() in ('.esp','.dll','.pex','.psc','.seq','.nif')}
    # Keep the inherited mesh: the preserved core STAT still references it,
    # even though the new mounted addon does not place that former tower.
    core['AstraAsedio_Atalaya.esp']=plugins[2]
    receipt={'revision':'QA v14','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'game_tested':False,
             'player_cycle_seconds':1.,'guard_minimum_cadence_seconds':2.5,'pitch_player':[-20,80],
             'guard_animation':'neutral prototype; no custom human operation animation','plugin_patch_idempotent':True,
             'native_dll_version':'3.4.0','new_native_build':False,'payload_sha256':{n:sha(p) for n,p in core.items()},
             'city_plugin_sha256':sha(plugins[1]),'verification_report_sha256':sha(ROOT/'reports/verification_v14.json'),
             'review_report_sha256':sha(ROOT/'reports/review_v14.json')}
    target=staging/'RECIBO_v14.json';target.write_text(json.dumps(receipt,indent=2));docs['Docs/AstraAsedio/RECIBO_v14.json']=target
    core.update(docs);city={'AstraAsedio_WhiterunTorres.esp':plugins[1],**docs}
    packages=[zip_package('AstraAsedio_QA_v14_MO2.zip',core),zip_package('AstraAsedio_WhiterunTorres_QA_v14_MO2.zip',city)]
    receipt.update({'packages':packages,'zip_crc_and_hashes_verified':True})
    (ROOT/'reports/package_qa_v14.json').write_text(json.dumps(receipt,indent=2))
    (ROOT/'README.md').write_bytes((ROOT/'docs/README_v14.md').read_bytes())
    for p in packages:print('V14_PACKAGE_OK',p['path'],p['bytes'],p['sha256'])
if __name__=='__main__':main()
