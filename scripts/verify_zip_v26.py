"""Read the final ZIP independently; certify inventory, bytes and old archives."""
from pathlib import Path
import hashlib
import json
import sys
import struct
import zipfile

ROOT=Path(__file__).resolve().parents[1]
OLD={23:'b09b815fa27e11ec9cb15016331c0dd3d338fd160eeb2632b186538e6edc27dd',
     24:'6304b3a525c25219e73a27ae98efe5fc39fd720827526b73cfb6810ecfd8111f',
     25:'b1f524268cf0a3165cf1ac6c6644b20a272a76429de3a8877fab7ffba278db02'}


def digest(data):return hashlib.sha256(data).hexdigest()


def main():
    path=ROOT/'dist/AstraAsedio_QA_v26_Unificado_MO2.zip'
    old_paths={revision:ROOT/f'dist/AstraAsedio_QA_v{revision}_Unificado_MO2.zip' for revision in OLD}
    for revision,old in old_paths.items():assert digest(old.read_bytes())==OLD[revision]
    with zipfile.ZipFile(path) as z,zipfile.ZipFile(old_paths[25]) as baseline:
        assert z.testzip() is None
        names=z.namelist();assert len(names)==len(set(names))==len({n.casefold() for n in names})
        assert all(not n.startswith('/') and '..' not in Path(n).parts for n in names)
        manifest_name='Docs/AstraAsedio/MANIFEST_v26.json'
        manifest=json.loads(z.read(manifest_name));assert manifest['revision']==26 and not manifest['game_tested']
        assert set(manifest['files_sha256'])==set(names)-{manifest_name}
        for name,expected in manifest['files_sha256'].items():assert digest(z.read(name))==expected,name
        assert manifest['verification_report_sha256']==digest((ROOT/'reports/verification_v26.json').read_bytes())
        assert manifest['native_build_receipt_sha256']==digest((ROOT/'reports/native_build_receipt.json').read_bytes())
        assert manifest['review_report_sha256']==digest((ROOT/'reports/review_v26.json').read_bytes())
        assert manifest['exact_v25_context_clause_measured'] is False
        assert manifest['editable_blend_sha256']==digest((ROOT/'source/astra_guard_v23.blend').read_bytes())
        assert manifest['preview_mp4_sha256']==digest((ROOT/'previews/v23/Astra_Guardia_v23_Giro_Disparo.mp4').read_bytes())
        assert manifest['diagnosis_report_sha256']==digest((ROOT/'reports/diagnosis_v25_context.json').read_bytes())
        plugins={n for n in names if n.endswith('.esp')}
        assert plugins=={'AstraAsedio.esp','AstraAsedio_WhiterunTorres.esp','AstraAsedio_Atalaya.esp','AstraAsedio_GuardAnim.esp'}
        pex=[n for n in names if n.endswith('.pex')];hkx=[n for n in names if n.endswith('.hkx')]
        assert len(pex)==10 and len(hkx)==12
        preserved=[n for n in names if n.endswith(('.esp','.hkx','.nif','.seq','.json')) and not n.startswith('Docs/')]
        for name in preserved:assert z.read(name)==baseline.read(name),name+' differs from approved v25 resource'
        old_manifest=json.loads(baseline.read('Docs/AstraAsedio/MANIFEST_v25.json'))
        for field in ('editable_blend_sha256','preview_mp4_sha256'):assert manifest[field]==old_manifest[field]
        receipt=json.loads((ROOT/'reports/native_build_receipt.json').read_text())
        sys.path.insert(0,str(Path(receipt['vendor_dir'])/'python'))
        import pefile
        receipt_hashes={name.replace('\\','/'):value for name,value in receipt['files_sha256'].items()}
        dll=z.read('SKSE/Plugins/AstraSight.dll');assert digest(dll)==receipt_hashes['mod/SKSE/Plugins/AstraSight.dll']
        pe=pefile.PE(data=dll);assert pe.FILE_HEADER.Machine==0x8664
        version=next(e.address for e in pe.DIRECTORY_ENTRY_EXPORT.symbols if e.name==b'SKSEPlugin_Version')
        assert struct.unpack('<I',pe.get_data(version+4,4))[0]==0x03050070
        report={'revision':26,'success':True,'game_tested':False,'entries':len(names),
                'sha256':digest(path.read_bytes()),'bytes':path.stat().st_size,'crc_ok':True,
                'complete_manifest_ok':True,'four_plugins':True,'ten_pex':True,'twelve_hkx':True,
                'preserved_v25_resources':preserved,'previous_v23_v24_v25_zip_unchanged':True,
                'editable_and_preview_unchanged':True,'archived_dll_metadata_3_5_7':True}
    (ROOT/'reports/zip_independent_v26.json').write_text(json.dumps(report,indent=2)+'\n')
    print('ZIP_V26_INDEPENDENT_OK',report['entries'],report['bytes'],report['sha256'])


if __name__=='__main__':main()
