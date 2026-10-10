"""Bind offline QA closure to the current files; do not invent engine approval."""
from pathlib import Path
import datetime
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    verification = json.loads((ROOT / 'reports/verification_v15.json').read_text())
    assert verification['success'] and verification['in_game_verified'] is False
    native = json.loads((ROOT / 'reports/native_build_receipt.json').read_text())
    files = {**verification['files_sha256'], **native['files_sha256']}
    for name, expected in files.items():
        assert sha(ROOT / name) == expected, ('Changed verified source/payload', name)
    for name, expected in verification['reports_sha256'].items():
        assert sha(ROOT / 'reports' / name) == expected, ('Changed verification report', name)
        files['reports/' + name] = expected
    reviews = ['v15_native_spec_review.md', 'v15_station_spec_review.md',
               'v15_city_spec_review.md', 'v15_native_quality_review.md']
    for name in reviews:
        text = (ROOT / 'reports' / name).read_text(encoding='utf-8')
        assert 'APROBADO' in text, ('Missing prior independent scope approval', name)
    # The completed native quality review still binds the delivered code/DLL.
    # Papyrus artifacts were recompiled after the later city correction; their
    # current identity is established by the global verification and root close.
    quality = (ROOT / 'reports/v15_native_quality_review.md').read_text()
    pairs = re.findall(r'\| (native/[^|]+?) \| ([0-9a-f]{64}) \|', quality)
    assert len(pairs) >= 5
    for name, expected in pairs:
        assert sha(ROOT / name.strip()) == expected, ('Native reviewed code changed', name)
    assert sha(ROOT / 'mod/SKSE/Plugins/AstraSight.dll') in quality
    additions = [ROOT / 'reports' / name for name in reviews]
    additions += [ROOT / 'reports/v15_city_quality_closure.md',
                  ROOT / 'reports/verification_v15.json',
                  ROOT / 'scripts/package_v15.py', ROOT / 'scripts/verify_v15_release.py', Path(__file__)]
    additions += [ROOT / 'docs' / name for name in
                  ('README_v15.md', 'PRUEBAS_v15.md', 'VALIDACION_v15.md')]
    additions += list((ROOT / 'native/licenses').iterdir())
    additions += list((ROOT / 'renders').glob('v15_voladizo_*.png'))
    for path in additions:
        assert path.is_file()
        files[path.relative_to(ROOT).as_posix()] = sha(path)
    result = {
        'revision': 15, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'approved_for_offline_qa': True, 'closing_reviewer': 'root',
        'in_game_verified': False,
        'independent_review_scopes': reviews,
        'city_final_independent_quality_approval': False,
        'city_quality_interruption': 'usage limit after reporting recovery MoveTo race',
        'city_fix_root_closure': 'reports/v15_city_quality_closure.md',
        'closed_finding': 'Recovery MoveTo retains pinBusy until return and cancellation validation',
        'limits': ['Skyrim activation/latency/AI/animation/save-load untested',
                   'East step-up is a contact-tolerant geometric proposal, not free capsule proof',
                   'Prior Station/city hashes superseded by fresh compilation and root closure'],
        'verification_report_sha256': sha(ROOT / 'reports/verification_v15.json'),
        'files_sha256': files,
    }
    (ROOT / 'reports/review_v15.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print('V15_OFFLINE_REVIEW_SEALED', len(files), 'files; engine unverified')


if __name__ == '__main__':
    main()
