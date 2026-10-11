"""Allowlisted QA/public candidates; verify archived bytes and PEX metadata."""
from pathlib import Path
import hashlib,json,zipfile,re,datetime
from pex_metadata import metadata
ROOT=Path(__file__).resolve().parents[1]
SUFFIXES={'.esp','.dll','.pex','.psc','.seq','.nif'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def archive(filename,entries,public=False,stamp=None):
    """Empaqueta `entries` en dist/<filename>.

    `stamp` es un date_time de zip (year,month,day,hour,min,sec). Si se pasa, todas las
    entradas lo usan y el ZIP queda **reproducible**: el mismo contenido da el mismo sha.
    Sin `stamp` se conserva el comportamiento historico (`z.write`, que guarda el mtime
    del archivo) y el sha cambia cada vez que se reescribe una fuente.
    """
    path=ROOT/'dist'/filename;path.parent.mkdir(parents=True,exist_ok=True)
    assert len(entries)==len({n.casefold() for n in entries})
    for n,p in entries.items():
        assert not n.startswith('/') and '..' not in Path(n).parts
        if public:
            assert p.suffix.lower() not in ('.blend','.log','.exe','.pdb','.obj','.esm','.ini')
            if p.suffix.lower() in ('.md','.json','.psc','.txt','.cpp','.h','.py'):
                data=p.read_text(encoding='utf-8-sig')
                assert not re.search(r'[A-Z]:[\\/]|Facu2|DESKTOP-DF3S14S',data),n
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=False) as z:
        for n,p in sorted(entries.items()):
            if stamp is None:z.write(p,n)
            else:
                info=zipfile.ZipInfo(n,date_time=stamp)
                info.compress_type=zipfile.ZIP_DEFLATED
                info.external_attr=0o644<<16
                z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None and set(z.namelist())==set(entries)
        for n,p in entries.items():
            data=z.read(n);assert hashlib.sha256(data).hexdigest()==sha(p),n
            if n.lower().endswith('.pex'):
                head,_=metadata(data)
                assert head['user']=='AstraAsedio' and head['computer']=='Build'
                assert '/' not in head['source'] and '\\' not in head['source']
    return {'path':str(path.relative_to(ROOT)),'bytes':path.stat().st_size,'sha256':sha(path),'entries':len(entries),'crc_and_hashes_verified':True,'inventory_sha256':{n:sha(p) for n,p in sorted(entries.items())}}

def main():
    v=json.loads((ROOT/'reports/verification_v19.json').read_text());assert v['success']
    for n,h in v['files_sha256'].items():assert sha(ROOT/n)==h,('Changed verified file',n)
    native=json.loads((ROOT/'reports/native_build_receipt.json').read_text())
    for n,h in native['files_sha256'].items():assert sha(ROOT/n)==h,('Changed native source',n)
    core={p.relative_to(ROOT/'mod').as_posix():p for p in (ROOT/'mod').rglob('*') if p.is_file() and p.suffix.lower() in SUFFIXES}
    city={p.relative_to(ROOT/'addons/WhiterunTorres').as_posix():p for p in (ROOT/'addons/WhiterunTorres').rglob('*') if p.is_file() and p.suffix.lower() in ('.esp','.nif')}
    for p in [*core.values(),*city.values()]:assert sha(p)==v['files_sha256'][str(p.relative_to(ROOT))]
    assert {n for n in core if n.endswith('.esp')}=={'AstraAsedio.esp'}
    assert len(city)==3 and len([n for n in core if n.endswith('.pex')])==6
    docs={'Docs/AstraAsedio/'+p.name:p for p in (ROOT/'docs/nexus').iterdir() if p.is_file()}
    licenses={'Docs/AstraAsedio/Licenses/'+p.name:p for p in (ROOT/'native/licenses').iterdir() if p.is_file()}
    assert len(licenses)==4
    docs.update(licenses)
    qdocs={'Docs/AstraAsedio/README_v19.md':ROOT/'docs/README_v19.md',**licenses}
    qcore={**core,'AstraAsedio_Atalaya.esp':ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp'}
    qa=[archive('AstraAsedio_QA_v19_MO2.zip',{**qcore,**qdocs}),archive('AstraAsedio_WhiterunTorres_QA_v19_MO2.zip',{**city,**qdocs})]
    public=[archive('nexus/AstraAsedio_Core_0.19.0-rc1.zip',{**core,**docs},True),archive('nexus/AstraAsedio_WhiterunTorres_0.19.0-rc1.zip',{**city,**docs},True)]
    source={'native/CMakeLists.txt':ROOT/'native/CMakeLists.txt','native/README.md':ROOT/'native/README.md'}
    for folder in ('include','src','tests','licenses'):
        for p in (ROOT/'native'/folder).rglob('*'):
            if p.is_file():source[p.relative_to(ROOT).as_posix()]=p
    for p in (ROOT/'mod/scripts/source').glob('*.psc'):source['scripts/source/'+p.name]=p
    source.update({'README.md':ROOT/'native/README.md','RELEASE_STATUS.md':ROOT/'docs/nexus/RELEASE_STATUS.md'})
    public.append(archive('nexus/AstraAsedio_Source_0.19.0-rc1.zip',source,True))
    report={'revision':19,'version':'0.19.0-rc.1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verification_report_sha256':sha(ROOT/'reports/verification_v19.json'),'qa':qa,'public':public,'public_contains_atalaya':False,'game_tested_v19':False,'nexus_uploaded':False,'native_version':'3.5.4','pex_metadata_anonymized':True,'public_source_scope':'native C++ and PSC only; not full ESP/NIF regeneration'}
    (ROOT/'reports/package_v19.json').write_text(json.dumps(report,indent=2))
    manifest={k:v for k,v in report.items() if k not in ('qa','verification_report_sha256')}
    manifest['public']=[{k:v for k,v in p.items() if k!='inventory_sha256'} for p in public]
    (ROOT/'dist/nexus/MANIFEST.json').write_text(json.dumps(manifest,indent=2))
    for p in qa+public:print('PACKAGE_OK',p['path'],p['bytes'],p['sha256'])
if __name__=='__main__':main()
