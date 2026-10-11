"""Package the v27 candidate, preserving the previously delivered v23-v26 ZIPs."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from package_v19 import archive


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    subprocess.run([sys.executable,'scripts/verify_v27_release.py'],cwd=ROOT,check=True)
    verification=json.loads((ROOT/'reports/verification_v27.json').read_text())
    assert verification['success'] and verification['revision']==27
    entries={}
    for folder,suffixes in [('mod',{'.esp','.dll','.psc','.pex','.seq','.nif'}),
            ('addons/WhiterunTorres',{'.esp','.nif'}),('addons/Atalaya',{'.esp','.nif'}),
            ('addons/GuardAnim',{'.esp','.seq','.json','.hkx'})]:
        base=ROOT/folder
        for path in base.rglob('*'):
            if not path.is_file() or path.suffix.lower() not in suffixes:continue
            name=path.relative_to(base).as_posix()
            assert name not in entries and name.casefold() not in {n.casefold() for n in entries},name
            assert verification['files_sha256'][path.relative_to(ROOT).as_posix()]==sha(path),name
            entries[name]=path
    assert {n for n in entries if n.endswith('.esp')}=={
        'AstraAsedio.esp','AstraAsedio_WhiterunTorres.esp','AstraAsedio_Atalaya.esp','AstraAsedio_GuardAnim.esp'}
    for name in ('README_v27.md','QA_v27.md'):
        entries['Docs/AstraAsedio/'+name]=ROOT/'docs'/name
    for path in (ROOT/'native/licenses').iterdir():
        if path.is_file():entries['Docs/AstraAsedio/Licenses/'+path.name]=path
    manifest={'revision':27,'game_tested':False,
              'previous_v26_context_failure_confirmed':True,
              'exact_v26_context_clause_measured':True,
              'v26_diagnosis_report_sha256':sha(ROOT/'reports/diagnosis_v26_context.json'),
              'v25_diagnosis_report_sha256':sha(ROOT/'reports/diagnosis_v25_context.json'),
              'files_sha256':{n:sha(p) for n,p in sorted(entries.items())},
              'verification_report_sha256':sha(ROOT/'reports/verification_v27.json'),
              'native_build_receipt_sha256':sha(ROOT/'reports/native_build_receipt.json'),
              'review_report_sha256':sha(ROOT/'reports/review_v27.json'),
              'editable_blend_sha256':sha(ROOT/'source/astra_guard_v23.blend'),
              'preview_mp4_sha256':sha(ROOT/'previews/v23/Astra_Guardia_v23_Giro_Disparo.mp4')}
    manifest_path=ROOT/'dist/MANIFEST_v27.json'
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    entries['Docs/AstraAsedio/MANIFEST_v27.json']=manifest_path
    filename='AstraAsedio_QA_v27_Unificado_MO2.zip'
    report=archive(filename,entries,stamp=(1980,1,1,0,0,0))
    again=archive(filename,entries,stamp=(1980,1,1,0,0,0))
    assert report['sha256']==again['sha256'] and report['inventory_sha256']==again['inventory_sha256']
    report.update(reproducible=True,revision=27,game_tested=False,
                  verification_report_sha256=manifest['verification_report_sha256'])
    (ROOT/'reports/package_v27.json').write_text(json.dumps(report,indent=2)+'\n')
    (ROOT/'dist/SHA256_v27.txt').write_text(report['sha256']+'  '+filename+'\n')
    print('PACKAGE_V27_OK',report['path'],report['bytes'],report['sha256'])


if __name__=='__main__':main()
