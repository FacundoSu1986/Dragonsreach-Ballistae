"""Read AstraSight.log and say which guard-pose hypothesis the evidence supports.

Usage: python scripts/analyze_guard_log.py [path/to/AstraSight.log] [--expect 3.6.3]
Default path: Documents/My Games/Skyrim Special Edition/SKSE/AstraSight.log

Reads the lines written by AstraSight 3.6.x (`guard v26 acquired`, `guard v29 pose`,
`guard v29.1 ...`). It only reads a text file: it does not touch the game or the repo.
Hypotheses are defined in docs/superpowers/specs/2026-10-12-guardia-pose-fixes.md.
"""
import argparse
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HELD_UNITS = 12.0          # GuardHeldHandError in native/include/Astra/GuardPolicy.h
EXPECTED_VERSION = '3.6.3'
DEFAULT_LOG = Path.home()/'Documents/My Games/Skyrim Special Edition/SKSE/AstraSight.log'
LINE = re.compile(r'^\[[^\]]*\] \[AstraSight\] \[(?P<level>\w+)\] (?P<msg>.*)$')
KEY = re.compile(r'(\w+)=(\S+)')


def fields(message):
    """name=value tokens of one log line (values without spaces)."""
    return dict(KEY.findall(message))


def analyze(text, expect=EXPECTED_VERSION):
    r = {'version': None, 'oar': None, 'acquired': 0, 'holding': 0, 'projectiles': 0, 'cancels': Counter(), 'rejects': Counter(),
         'play_idle': Counter(), 're_requests': defaultdict(int), 'unresolved': 0, 'unexpected': [], 'poses': defaultdict(list),
         'refused': Counter(), 'hunted': [], 'launches': [],
         'lines': 0, 'expect': expect}
    for raw in text.splitlines():
        m = LINE.match(raw.strip())
        if not m:
            continue
        r['lines'] += 1
        msg = m['msg']
        v = re.match(r'AstraSight (\d+\.\d+\.\d+) API', msg)
        if v and r['version'] is None:
            r['version'] = v[1]
        o = re.search(r'OAR Animations V1=(\w+) \(module loaded=(\w+)\)', msg)
        if o:
            r['oar'] = (o[1] == 'True', o[2] == 'True')
        if msg.startswith('guard v26 acquired'):
            r['acquired'] += 1
        elif msg.startswith('guard v29 holding'):
            r['holding'] += 1
        elif msg.startswith('guard real projectile'):
            r['projectiles'] += 1
            f = fields(msg)
            try:
                r['launches'].append({'pitch': float(f['pitch']), 'solved': float(f['solvedPitch']), 'vz': float(f['velocityZ']),
                                      'ez': float(f['expectedZ']), 'player': f.get('player') == 'true'})
            except (KeyError, ValueError):
                pass
        elif msg.startswith('guard v29.2 shot refused'):
            r['refused'][msg.split(' reason=', 1)[1] if ' reason=' in msg else '?'] += 1
        elif msg.startswith('guard v29.2 player-hostile'):
            r['hunted'].append(fields(msg).get('hunted') == 'true')
        elif msg.startswith('guard cancel'):
            reason = msg.split(' reason=', 1)[1] if ' reason=' in msg else '?'
            r['cancels'][reason] += 1
        elif msg.startswith('guard v26 reject') or msg.startswith('guard v26 context'):
            clause = re.search(r'clause=(.*?) (?:acquired|actorXYZ)=', msg)
            r['rejects'][clause[1] if clause else '?'] += 1
        elif msg.startswith('guard v29.1 PlayIdle'):
            r['play_idle'][fields(msg).get('accepted', '?')] += 1
        elif msg.startswith('guard v29 hold re-request'):
            r['re_requests'][fields(msg).get('gun', '?')] += 1
        elif msg.startswith('guard v29.1 hold unresolved'):
            r['unresolved'] += 1
        elif msg.startswith('guard v29.1 unexpected clip'):
            q = dict(re.findall(r"(\w+)='([^']*)'", msg))
            r['unexpected'].append(q)
        elif msg.startswith('guard v29 pose'):
            f = fields(msg)
            try:
                r['poses'][f['gun']].append({
                    'status': int(f['status']), 'target': int(f['target'], 16), 'clip': int(f['clip']),
                    'left': float(f['handErrorL']), 'right': float(f['handErrorR']),
                    'writes_pos': int(f.get('writesPos', -1)), 'writes_rot': int(f.get('writesRot', -1)),
                    'pitch': float(f.get('pitch', 'nan')), 'desired_pitch': float(f.get('desiredPitch', 'nan')),
                    'drift': float(f.get('maxDrift', -1)), 'refused': f.get('moveRefused', 'none')})
            except (KeyError, ValueError):
                pass
    r['verdicts'] = verdicts(r)
    return r


def measured(sample):
    return sample['left'] >= 0 and sample['right'] >= 0


def verdicts(r):
    out = []
    if r['version'] is None:
        return [('NO-DATA', 'No "AstraSight x.y.z" line: wrong file, empty log or the DLL did not load.')]
    if r['version'] != r['expect']:
        out.append(('DLL', f"Loaded AstraSight {r['version']}, this analysis expects {r['expect']}. In MO2 check that no other mod overrides SKSE/Plugins/AstraSight.dll."))
    if r['oar'] is not None and not all(r['oar']):
        out.append(('OAR', f"OAR Animations V1={r['oar'][0]} module loaded={r['oar'][1]}: the guard runtime is disabled without OAR; nothing can animate."))
    if r['oar'] is None:
        out.append(('OAR', 'No "OAR Animations V1=" line (log from before v27, or the runtime did not install).'))
    if r['acquired'] == 0:
        clauses = ', '.join(f'{c} x{n}' for c, n in r['rejects'].most_common(3)) or 'no reject/context clause logged'
        out.append(('NEVER-ACQUIRED', f'No operator was acquired ({clauses}). Fix that first; no pose hypothesis applies.'))
        return out
    samples = [s for lst in r['poses'].values() for s in lst]
    if not samples:
        out.append(('NO-POSE-LOG', 'Acquired but no "guard v29 pose" line: the lease ended before 2 s or tick() stopped. See cancels: '
                    + (', '.join(f'{c} x{n}' for c, n in r['cancels'].most_common(3)) or 'none')))
        return out
    got = [s for s in samples if measured(s)]
    held = [s for s in got if s['left'] <= HELD_UNITS and s['right'] <= HELD_UNITS]
    # H3: wrists far from the grips although the hold was entered.
    if got and len(held) < len(got) / 2:
        worst = statistics.median([max(s['left'], s['right']) for s in got])
        out.append(('H3-HANDS-FAR', f'Wrists are on the grips in only {len(held)}/{len(got)} samples (median worst hand {worst:.0f} u, held <= {HELD_UNITS:.0f} u). '
                    'Clip plays but geometry/skeleton/scale does not match the grips.'))
    if not got:
        out.append(('H3-NOT-MEASURED', 'Hand nodes could not be measured in any sample (handError = -1): 3D not loaded or skeleton node names differ.'))
    # H1: still writing the transform every frame while nothing is being tracked.
    still = [s for s in samples if s['target'] == 0 and s['status'] >= 1 and s['writes_pos'] >= 0]
    if still and statistics.mean(s['writes_pos'] + s['writes_rot'] for s in still) > 10:
        out.append(('H1-WRITING-EVERY-FRAME', 'With no target the pose still writes position/rotation many times per 2 s: the per-frame write is not gone (old DLL, or something moves the actor).'))
    elif still:
        out.append(('H1-OK', f'Still hold writes {statistics.mean(s["writes_pos"] + s["writes_rot"] for s in still):.1f} transforms per 2 s on average (expected ~0).'))
    # H2: the idle keeps being re-requested.
    again = sum(r['re_requests'].values())
    if again >= 2 or r['unresolved']:
        out.append(('H2-RE-REQUEST-CYCLE', f'{again} hold re-requests, {r["unresolved"]} "hold unresolved": OAR samples are not seen and the wrists are not on the grips. '
                    'Look at "unexpected clip" lines for what is really playing.'))
    if r['play_idle'].get('false'):
        out.append(('PLAYIDLE-REJECTED', f'PlayIdle was rejected {r["play_idle"]["false"]} times: the engine refused the owned idle (package/graph state).'))
    # H4: another owner of the animation.
    if r['unexpected']:
        names = Counter((u.get('mod') or '(none)', u.get('submod') or '(none)', u.get('animation') or '(no replacement: vanilla clip)') for u in r['unexpected'])
        top = '; '.join(f'mod={m} submod={s} anim={a} x{n}' for (m, s, a), n in names.most_common(3))
        out.append(('H4-OTHER-CLIP', f'Clips that are not ours play on the operator: {top}. Open OAR (Shift+O) on the guard to see which submod wins.'))
    # v29.2: elevation tracking and shooting.
    tracked = [s for s in samples if s['target'] != 0 and s['desired_pitch'] == s['desired_pitch'] and s['pitch'] == s['pitch']]
    if tracked:
        off = [s for s in tracked if abs(s['desired_pitch']-s['pitch']) > 1.0]
        if len(off) > len(tracked)/2:
            out.append(('PITCH-NOT-TRACKING', f'With a target, the elevation is more than 1 deg from the wanted one in {len(off)}/{len(tracked)} samples '
                        f'(median |error| {statistics.median(abs(s["desired_pitch"]-s["pitch"]) for s in off):.1f} deg): the mount cannot reach it (limits +-30 deg, 25 deg/s) or pose() refuses the move.'))
        else:
            out.append(('PITCH-OK', f'Elevation follows the target in {len(tracked)-len(off)}/{len(tracked)} samples.'))
    if r['refused']:
        out.append(('SHOT-REFUSED', 'shoot() declined: ' + '; '.join(f'{c} x{n}' for c, n in r['refused'].most_common(4))))
    if r['hunted']:
        out.append(('PLAYER-HUNTED', f'The runtime saw the town guards fight the player {sum(r["hunted"])} time(s) '
                    f'({len(r["hunted"])} state changes); the player is a valid target only then.'))
    bad = [l for l in r['launches'] if abs(l['vz']-l['ez']) > max(25., .02*abs(l['ez']))]
    if bad:
        out.append(('LAUNCH-VELOCITY-MISMATCH', f'{len(bad)}/{len(r["launches"])} launches report a vertical velocity that differs from the bore '
                    f'(first: velocityZ={bad[0]["vz"]:.0f} expected {bad[0]["ez"]:.0f}): the engine did not keep the elevated velocity.'))
    if r['projectiles']:
        out.append(('FIRE', f'{r["projectiles"]} real projectiles launched'
                    + (f' ({sum(1 for l in r["launches"] if l["player"])} at the player, {sum(1 for l in r["launches"] if abs(l["pitch"]) > 1)} elevated by more than 1 deg).' if r['launches'] else '.')))
    if not any(not k.endswith('-OK') and k not in ('FIRE', 'PLAYER-HUNTED') for k, _ in out):
        out.append(('LOOKS-HEALTHY', 'No hypothesis is supported by this log; if the pose still looks wrong in game, the cause is not in these signals.'))
    return out


def render(r):
    lines = [f"AstraSight {r['version'] or '?'}  (log lines parsed: {r['lines']})",
             f"acquired={r['acquired']} holding={r['holding']} projectiles={r['projectiles']} re-requests={sum(r['re_requests'].values())} unresolved={r['unresolved']}"]
    if r['cancels']:
        lines.append('cancels: ' + '; '.join(f'{c} x{n}' for c, n in r['cancels'].most_common(5)))
    for gun, lst in sorted(r['poses'].items()):
        got = [s for s in lst if measured(s)]
        if got:
            lines.append(f'gun {gun}: {len(lst)} pose samples, worst-hand median {statistics.median(max(s["left"], s["right"]) for s in got):.1f} u, '
                         f'held {sum(1 for s in got if max(s["left"], s["right"]) <= HELD_UNITS)}/{len(got)}')
    lines.append('')
    lines += [f'[{key}] {text}' for key, text in r['verdicts']]
    return '\n'.join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('log', nargs='?', type=Path, default=DEFAULT_LOG)
    ap.add_argument('--expect', default=EXPECTED_VERSION, help='AstraSight version the log should come from')
    args = ap.parse_args(argv)
    try:
        text = args.log.read_text(encoding='utf-8', errors='replace')
    except OSError as error:
        print(f'cannot read {args.log}: {error}', file=sys.stderr)
        return 2
    print(render(analyze(text, args.expect)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
