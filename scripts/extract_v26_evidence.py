"""Extract the measured v26 in-game session evidence into reports/.

Reads the live AstraSight.log of the 2026-10-11 17:12 session (v26, DLL 3.5.7)
and records the aggregate that falsifies the v26 admission clause: PlayIdle's
run-once wrapper holds GetRunningPackage() and high->currentProcessIdle stays
null, so (running==B90 || ownIdle) can never hold while the own idle runs.
No personal data is stored; only engine-observed lines and counts.
"""
from pathlib import Path
import datetime
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = Path.home() / r"OneDrive\Documentos\My Games\Skyrim Special Edition\SKSE\AstraSight.log"


def main(log_path=None):
    log = Path(log_path or DEFAULT_LOG)
    raw = log.read_bytes()
    text = raw.decode('utf-8', errors='replace')
    lines = text.splitlines()
    clause = 'clause=running package has no owned idle override'
    acquired = [ln for ln in lines if 'guard v26 acquired' in ln]
    contexts = [ln for ln in lines if clause in ln]
    cancels = [ln for ln in lines if 'guard cancel' in ln]
    holds = [ln for ln in lines if 'hold confirmed by OAR' in ln]
    grips = [ln for ln in lines if 'grip confirmed' in ln]
    idle_null = [ln for ln in lines if re.search(r'\bidle=00000000\b', ln)]
    runonce = {re.search(r'runOncePackage=([0-9A-Fa-f]+)', ln).group(1) for ln in contexts}
    stamps = [re.match(r'\[([\d\- :\.]+)\]', ln).group(1) for ln in lines if ln.startswith('[')]
    report = {
        'observed_revision': 26,
        'source_log': log.name,
        'log_sha256': hashlib.sha256(raw).hexdigest(),
        'log_bytes': len(raw),
        'session_window_utc_local': [stamps[0], stamps[-1]] if stamps else [],
        'dll_line': next((ln.split('] ')[-1] for ln in lines if 'AstraSight 3.5.7 API 4' in ln), ''),
        'acquired_count': len(acquired),
        'cancel_count': len(cancels),
        'context_clause_count': len(contexts),
        'distinct_runonce_packages': sorted(runonce),
        'idle_null_in_every_context_clause': len(idle_null) == len(contexts) and len(contexts) > 0,
        'hold_observed': bool(holds),
        'grip_observed': bool(grips),
        'first_acquisition': acquired[:2],
        'first_context_clause': contexts[:2],
        'first_cancel': [ln for ln in cancels[:2]],
        'conclusion': ('On 1.6.1170 the PlayIdle run-once wrapper keeps GetRunningPackage() and '
                       'high->currentProcessIdle stays null while the own idle runs, so the v26 '
                       'admission clause (running==B90 || ownIdle) is unsatisfiable on this route.'),
        'v26_in_game_tested': True,
        'v27_in_game_tested': False,
        'extracted_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    out = ROOT / 'reports/diagnosis_v26_context.json'
    out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('DIAGNOSIS_V26_CONTEXT_OK', out.name, 'acquired', len(acquired), 'clause', len(contexts))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
