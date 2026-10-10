"""Create a new MO2 QA package with fresh evidence and baseline preservation checks."""
import json
import hashlib
import zipfile
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v11')

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    mod=ROOT/'mod'; esp=mod/'AstraAsedio.esp'
    original_sha=sha(esp)
    subprocess.run([sys.executable,str(ROOT/'scripts/patch_plugin_v12.py')],check=True,cwd=ROOT)
    if sha(esp)!=original_sha:raise ValueError('Plugin patch is not idempotent')
    preserved={}
    for path in (BASE/'mod').rglob('*'):
        if not path.is_file():continue
        rel=path.relative_to(BASE/'mod').as_posix()
        if rel.startswith('Docs/') or rel in ('AstraAsedio.esp','meshes/AstraAsedio/torre.nif'):continue
        if sha(path)!=sha(mod/rel):raise ValueError('Proven v11 resource changed: '+rel)
        preserved[rel]=sha(path)
    for name,key in [('plugin_v12.json','land_and_vanilla_overrides_preserved'),
                     ('route_v12.json','ok'),('shot_clearance_v12.json','ok')]:
        report=json.loads((ROOT/'reports'/name).read_text())
        if report.get(key) is not True:raise ValueError('Required evidence did not pass: '+name)
    for name in ('shields_v12.json','route_v12.json'):
        report=json.loads((ROOT/'reports'/name).read_text())
        if report.get('torre_sha256')!=sha(mod/'meshes/AstraAsedio/torre.nif'):
            raise ValueError('Evidence belongs to another tower: '+name)
    route=json.loads((ROOT/'reports/route_v12.json').read_text())
    if route['esp_sha256']!=sha(esp):raise ValueError('Route evidence is for another plugin')
    for src,dst in [('README_v12.md','README.md'),('PRUEBAS_v12.md','PRUEBAS_EN_JUEGO.md'),
                    ('VALIDACION_v12.md','VALIDACION.md')]:
        data=(ROOT/'docs'/src).read_bytes()
        (ROOT/dst).write_bytes(data)
        (mod/'Docs/AstraAsedio'/dst).write_bytes(data)
    (mod/'Docs/AstraAsedio/INSTALACION_ATALAYA.md').write_bytes((ROOT/'docs/README_v12.md').read_bytes())
    hashes={p.relative_to(mod).as_posix():sha(p) for p in mod.rglob('*') if p.is_file() and p.suffix.lower() in ('.esp','.dll','.pex','.psc','.seq','.nif')}
    receipt={'revision':'QA v12 baja','deck_meters':2.0,'shields_per_tower':12,
             'game_tested':False,'proven_v11_files_preserved':preserved,
             'plugin_patch_idempotent':True,'sha256_payload':hashes}
    (mod/'Docs/AstraAsedio/RECIBO_v12.json').write_text(json.dumps(receipt,indent=2))
    out=ROOT/'dist/AstraAsedio_QA_v12_Baja_MO2.zip'
    entries={}
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=False) as z:
        for p in sorted(mod.rglob('*')):
            if p.is_file():
                rel=p.relative_to(mod).as_posix(); z.write(p,rel); entries[rel]=sha(p)
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None,'Corrupt ZIP'
        assert len(z.namelist())==len(set(z.namelist())),'Duplicate entry'
        assert set(z.namelist())==set(entries),'Missing payload'
        assert not any(n.lower().endswith(('.dds','.esm','.esl','.blend')) for n in z.namelist()),'Vanilla/source payload'
        for rel,digest in entries.items():assert hashlib.sha256(z.read(rel)).hexdigest()==digest,rel
    receipt.update({'zip':str(out),'bytes':out.stat().st_size,'zip_sha256':sha(out),
                    'zip_entries':len(entries),'zip_crc_and_hashes_verified':True,
                    'sha256_all_entries':entries})
    (ROOT/'reports/package_qa_v12.json').write_text(json.dumps(receipt,indent=2))
    print('V12_PACKAGE_OK',out,'bytes',out.stat().st_size,'files',len(entries),'sha256',sha(out))

if __name__=='__main__':main()
