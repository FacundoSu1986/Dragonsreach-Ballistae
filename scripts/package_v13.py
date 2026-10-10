"""Package only v13 payload and current documentation; historical v12 docs excluded."""
import json,hashlib,zipfile,sys,subprocess,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def zip_package(name,entries):
    path=ROOT/'dist'/name
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=False) as z:
        for name,p in sorted(entries.items()):z.write(p,name)
    with zipfile.ZipFile(path) as z:
        assert z.testzip()is None and len(z.namelist())==len(set(z.namelist()))
        assert set(z.namelist())==set(entries)
        for n,p in entries.items():assert hashlib.sha256(z.read(n)).hexdigest()==sha(p),n
    return {'path':str(path),'bytes':path.stat().st_size,'sha256':sha(path),'entries':len(entries),'crc_and_hashes_verified':True}
def main():
    reviewed=json.loads((ROOT/'reports/review_v13.json').read_text());assert reviewed['approved'],'Review pending'
    for n,h in reviewed['files_sha256'].items():assert sha(ROOT/n)==h,('Reviewed file changed',n)
    verification=json.loads((ROOT/'reports/verification_v13.json').read_text());assert verification['success']
    for n,h in verification['files_sha256'].items():assert sha(ROOT/n)==h,('Unverified payload changed',n)
    plugins=[ROOT/'mod/AstraAsedio.esp',ROOT/'addons/Whiterun/AstraAsedio_Whiterun.esp',ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp']
    before=[sha(p) for p in plugins]
    subprocess.run([sys.executable,str(ROOT/'scripts/build_modular_v13.py')],cwd=ROOT,check=True)
    assert before==[sha(p) for p in plugins],'Plugins are not idempotent'
    staging=ROOT/'build/package_v13';staging.mkdir(exist_ok=True)
    docs={}
    for src,dst in [('README_v13.md','README.md'),('PRUEBAS_v13.md','PRUEBAS_EN_JUEGO.md'),('VALIDACION_v13.md','VALIDACION_v13.md')]:
        target=staging/dst;target.write_bytes((ROOT/'docs'/src).read_bytes());docs['Docs/AstraAsedio/'+dst]=target
    manifest=staging/'COMPATIBILIDAD_v13.json';manifest.write_bytes((ROOT/'reports/modular_v13.json').read_bytes());docs['Docs/AstraAsedio/COMPATIBILIDAD_v13.json']=manifest
    for license_path in (ROOT/'native/licenses').iterdir():
        if license_path.is_file():docs['Docs/AstraAsedio/Licenses/'+license_path.name]=license_path
    core={p.relative_to(ROOT/'mod').as_posix():p for p in (ROOT/'mod').rglob('*') if p.is_file() and p.suffix.lower()in('.esp','.dll','.pex','.psc','.seq','.nif')}
    core['AstraAsedio_Atalaya.esp']=plugins[2]
    # Compare immutable v11 assets and installation inputs before writing ZIPs.
    base=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v11')
    v11_archive=base/'dist/AstraAsedio_QA_v11_MO2.zip'
    preserved={}
    for n in ('meshes/AstraAsedio/ballesta.nif','meshes/AstraAsedio/virote.nif','seq/AstraAsedio.seq'):
        assert sha(ROOT/'mod'/n)==sha(base/'mod'/n),n;preserved[n]=sha(base/'mod'/n)
    receipt={'revision':'QA v13','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'game_tested':False,
             'pitch_player':[-20,80],'shields_per_tower':12,'guard_animation':'neutral prototype, no custom human operation animation',
             'plugin_patch_idempotent':True,'native_dll_version':'3.4.0','preserved_v11_payload':preserved,
             'v11_archive_sha256':sha(v11_archive),'sha256_payload':{n:sha(p) for n,p in core.items()},
             'verification_report_sha256':sha(ROOT/'reports/verification_v13.json'),'review_report_sha256':sha(ROOT/'reports/review_v13.json')}
    rp=staging/'RECIBO_v13.json';rp.write_text(json.dumps(receipt,indent=2));docs['Docs/AstraAsedio/RECIBO_v13.json']=rp
    core.update(docs)
    city={'AstraAsedio_Whiterun.esp':plugins[1],**docs}
    packages=[zip_package('AstraAsedio_QA_v13_MO2.zip',core),zip_package('AstraAsedio_Whiterun_QA_v13_MO2.zip',city)]
    receipt.update({'packages':packages,'zip_crc_and_hashes_verified':True})
    (ROOT/'reports/package_qa_v13.json').write_text(json.dumps(receipt,indent=2))
    (ROOT/'README.md').write_bytes((ROOT/'docs/README_v13.md').read_bytes())
    for p in packages:print('V13_PACKAGE_OK',p['path'],p['bytes'],p['sha256'])
if __name__=='__main__':main()
