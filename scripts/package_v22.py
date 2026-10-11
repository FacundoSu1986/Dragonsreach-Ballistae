"""Un paquete QA v22 completo: core de dos torretas, WhiterunTorres, Atalaya y GuardAnim.

Exige el sello `scripts/verify_v22_release.py` antes de archivar. Escribe
`reports/package_v22.json` y `dist/MANIFEST_v22.json`.
"""
import hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from package_v19 import archive

SUFFIXES = {'.esp', '.dll', '.pex', '.psc', '.seq', '.nif'}
GUARD_SUFFIXES = {'.esp', '.hkx', '.json'}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    subprocess.run([sys.executable, str(ROOT / 'scripts/verify_v22_release.py')], cwd=ROOT, check=True)
    verified = json.loads((ROOT / 'reports/verification_v22.json').read_text())
    assert verified['success'], 'el sello de v22 no paso; no se empaqueta'

    core = {p.relative_to(ROOT / 'mod').as_posix(): p
            for p in (ROOT / 'mod').rglob('*') if p.is_file() and p.suffix.lower() in SUFFIXES}
    city = {p.relative_to(ROOT / 'addons/WhiterunTorres').as_posix(): p
            for p in (ROOT / 'addons/WhiterunTorres').rglob('*')
            if p.is_file() and p.suffix.lower() in ('.esp', '.nif')}
    guard = {p.relative_to(ROOT / 'addons/GuardAnim').as_posix(): p
             for p in (ROOT / 'addons/GuardAnim').rglob('*')
             if p.is_file() and p.suffix.lower() in GUARD_SUFFIXES}
    atalaya = {'AstraAsedio_Atalaya.esp': ROOT / 'addons/Atalaya/AstraAsedio_Atalaya.esp',
               'meshes/AstraAsedio/torre_atalaya_v20.nif':
                   ROOT / 'addons/Atalaya/meshes/AstraAsedio/torre_atalaya_v20.nif'}
    docs = {'Docs/AstraAsedio/README_v22.md': ROOT / 'docs/README_v22.md'}
    docs.update({'Docs/AstraAsedio/Licenses/' + p.name: p
                 for p in (ROOT / 'native/licenses').iterdir() if p.is_file()})
    assert len(docs) == 5

    grupos = {'core': core, 'city': city, 'atalaya': atalaya, 'guard': guard}
    for a, ga in grupos.items():
        for b, gb in grupos.items():
            if a < b:
                assert set(ga).isdisjoint(gb), (a, b)

    entries = {**core, **city, **atalaya, **guard, **docs}
    assert {n for n in entries if n.endswith('.esp')} == {
        'AstraAsedio.esp', 'AstraAsedio_WhiterunTorres.esp',
        'AstraAsedio_Atalaya.esp', 'AstraAsedio_GuardAnim.esp'}
    package = archive('AstraAsedio_QA_v22_Completo_MO2.zip', entries)

    report = {k: v for k, v in verified.items() if k != 'inputs_sha256'}
    report['package'] = {k: v for k, v in package.items() if k != 'inventory_sha256'}
    report['inventory_sha256'] = package['inventory_sha256']
    report['payload_counts'] = {k: len(g) for k, g in grupos.items()}
    (ROOT / 'reports/package_v22.json').write_text(json.dumps(report, indent=2))
    (ROOT / 'dist/MANIFEST_v22.json').write_text(json.dumps(report, indent=2))
    print('PACKAGE_OK', package['path'], package['bytes'], package['sha256'], package['entries'])


if __name__ == '__main__':
    main()
