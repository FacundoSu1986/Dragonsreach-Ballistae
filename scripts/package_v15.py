"""Package only current v15 payload/docs and verify every archived byte."""
from pathlib import Path
import datetime
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_SUFFIXES = {'.esp', '.dll', '.pex', '.psc', '.seq', '.nif'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def zip_package(filename, entries):
    path = ROOT / 'dist' / filename
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9,
                         strict_timestamps=False) as archive:
        for name, source in sorted(entries.items()):
            assert not name.startswith('/') and '..' not in Path(name).parts
            archive.write(source, name)
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        assert archive.testzip() is None
        assert len(names) == len(set(names)) and set(names) == set(entries)
        for name, source in entries.items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == sha(source), name
    return {'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha(path),
            'entries': len(entries), 'crc_and_hashes_verified': True}


def main():
    review = json.loads((ROOT / 'reports/review_v15.json').read_text())
    assert review['approved_for_offline_qa'] and review['in_game_verified'] is False
    for name, expected in review['files_sha256'].items():
        assert sha(ROOT / name) == expected, ('Changed reviewed file', name)
    verified = json.loads((ROOT / 'reports/verification_v15.json').read_text())
    assert verified['success']
    assert sha(ROOT / 'reports/verification_v15.json') == review['verification_report_sha256']
    core = {p.relative_to(ROOT / 'mod').as_posix(): p for p in (ROOT / 'mod').rglob('*')
            if p.is_file() and p.suffix.lower() in PAYLOAD_SUFFIXES}
    core['AstraAsedio_Atalaya.esp'] = ROOT / 'addons/Atalaya/AstraAsedio_Atalaya.esp'
    city = {p.relative_to(ROOT / 'addons/WhiterunTorres').as_posix(): p
            for p in (ROOT / 'addons/WhiterunTorres').rglob('*')
            if p.is_file() and p.suffix.lower() in {'.esp', '.nif'}}
    assert {n for n in core if n.endswith('.esp')} == {'AstraAsedio.esp', 'AstraAsedio_Atalaya.esp'}
    assert set(city) == {'AstraAsedio_WhiterunTorres.esp',
                         'meshes/AstraAsedio/voladizo_este.nif',
                         'meshes/AstraAsedio/voladizo_oeste.nif'}
    for source in [*core.values(), *city.values()]:
        name = str(source.relative_to(ROOT))
        assert sha(source) == verified['files_sha256'][name], ('Unverified archive payload', name)
    staging = ROOT / 'build/package_v15'
    staging.mkdir(parents=True, exist_ok=True)
    (ROOT / 'dist').mkdir(exist_ok=True)
    docs = {}
    mapping = [('docs/README_v15.md', 'README.md'),
               ('docs/PRUEBAS_v15.md', 'PRUEBAS_EN_JUEGO.md'),
               ('docs/VALIDACION_v15.md', 'VALIDACION_v15.md'),
               ('reports/modular_v15.json', 'COMPATIBILIDAD_v15.json'),
               ('reports/platforms_v15.json', 'PLATAFORMAS_v15.json'),
               ('reports/verification_v15.json', 'VERIFICACION_v15.json'),
               ('reports/review_v15.json', 'REVISION_v15.json'),
               ('reports/v15_city_quality_closure.md', 'CIERRE_CALIDAD_v15.md')]
    for source, name in mapping:
        target = staging / name
        target.write_bytes((ROOT / source).read_bytes())
        docs['Docs/AstraAsedio/' + name] = target
    for source in (ROOT / 'native/licenses').iterdir():
        if source.is_file():
            docs['Docs/AstraAsedio/Licenses/' + source.name] = source
    for source in (ROOT / 'renders').glob('v15_voladizo_*.png'):
        docs['Docs/AstraAsedio/Preview/' + source.name] = source
    receipt = {
        'revision': 'QA v15', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'in_game_verified': False, 'game_tested': False, 'runtime': '1.6.1170',
        'native_dll_version': '3.5.0', 'native_api_version': 4, 'new_native_build': True,
        'native_release_seconds': 1 / 15, 'engine_latency_measured': False,
        'timing_scope': 'release after successful Fire preparation plus engine frame scheduling',
        'player_minimum_nominal_reload_seconds': 1., 'guard_minimum_cadence_seconds': 2.5,
        'pitch_degrees': [-20, 80], 'city_yaw_degrees': [-60, 60],
        'city_navmesh_added': False, 'existing_patrol_overrides': False,
        'requires_new_test_save': True, 'independent_city_final_quality_approval': False,
        'closure': 'root; independent review finding fixed and global gate passed',
        'verification_report_sha256': sha(ROOT / 'reports/verification_v15.json'),
        'review_report_sha256': sha(ROOT / 'reports/review_v15.json'),
        'core_payload_sha256': {n: sha(p) for n, p in sorted(core.items())},
        'city_payload_sha256': {n: sha(p) for n, p in sorted(city.items())},
    }
    target = staging / 'RECIBO_v15.json'
    target.write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    docs['Docs/AstraAsedio/RECIBO_v15.json'] = target
    packages = [zip_package('AstraAsedio_QA_v15_MO2.zip', {**core, **docs}),
                zip_package('AstraAsedio_WhiterunTorres_QA_v15_MO2.zip', {**city, **docs})]
    report = {**receipt, 'packages': packages, 'zip_crc_and_hashes_verified': True,
              'archive_inventory_sha256': {
                  packages[0]['path']: {n: sha(p) for n, p in sorted({**core, **docs}.items())},
                  packages[1]['path']: {n: sha(p) for n, p in sorted({**city, **docs}.items())}}}
    (ROOT / 'reports/package_qa_v15.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    (ROOT / 'README.md').write_bytes((ROOT / 'docs/README_v15.md').read_bytes())
    for package in packages:
        print('V15_PACKAGE_OK', package['path'], package['bytes'], package['sha256'])


if __name__ == '__main__':
    main()
