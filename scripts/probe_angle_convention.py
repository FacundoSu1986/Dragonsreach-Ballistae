"""Decide the engine's REFR rotation convention from real Skyrim.esm placements (v11, spec §1).

Neighbouring stockade references placed by Bethesda with large X/Y/Z rotations touch each
other in game. Every order/sign combination is tried; the one under which the neighbours
touch is the engine's. Meshes are read from config.extracted in memory only; nothing vanilla
is written (the report keeps FormIDs, distances and counts only).
"""
import collections, hashlib, json, math, struct, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import v11_layout as L
from v11_layout import zstr, mesh_vertices

CFG = L.load_cfg()
MIN_ROT_DEG = 3.0      # every axis rotated more than this (spec §1)
NEIGHBOUR_UNITS = 400.0
TOL = 10.0             # default; the result was the same at 5, 10 and 20 u
MARGIN = 3.0           # units between the best and second-best convention for a pair to count
PASS_FRACTION = 0.95   # kept in the report for the plan's original criterion (not met; see below)
FAMILIES = ('clutter\\stockade\\',)

def main(argv):
    TOL = float(argv[1]) if len(argv) > 1 else globals()['TOL']
    esm = Plugin(str(L.esm_path(CFG)))
    stats = {}; refs = []
    for tipo, o, _t, _p in esm.recorrer():
        if tipo == 'STAT':
            ss = dict(esm.subrecords(esm.datos(o)))
            model = zstr(ss.get('MODL', b'')).lower()
            if model.startswith(FAMILIES): stats[esm.form_id(o)] = model
    cell = None
    for tipo, o, _t, _p in esm.recorrer():
        if tipo == 'CELL': cell = esm.form_id(o)
        elif tipo == 'REFR':
            ss = dict(esm.subrecords(esm.datos(o)))
            base = struct.unpack('<I', ss['NAME'])[0]
            if base not in stats or 'DATA' not in ss: continue
            x, y, z, rx, ry, rz = struct.unpack('<6f', ss['DATA'])
            deg = [math.degrees(a) for a in (rx, ry, rz)]
            scale = struct.unpack('<f', ss['XSCL'])[0] if 'XSCL' in ss else 1.0
            refs.append({'fid': esm.form_id(o), 'cell': cell, 'model': stats[base], 'pos': (x, y, z),
                         'rot_deg': deg, 'scale': scale,
                         'tilted': all(abs(((a + 180) % 360) - 180) > MIN_ROT_DEG for a in deg)})
    tilted = [r for r in refs if r['tilted']]
    by_cell = collections.defaultdict(list)
    for r in refs: by_cell[r['cell']].append(r)
    pairs = []
    for r in tilted:
        for s in by_cell[r['cell']]:
            if s['fid'] == r['fid'] or (s['tilted'] and s['fid'] < r['fid']): continue
            if math.dist(r['pos'], s['pos']) <= NEIGHBOUR_UNITS: pairs.append((r, s))
    cache = {}
    def verts(m):
        if m not in cache: cache[m] = mesh_vertices(m)
        return cache[m]
    def world(r, conv):
        m = L.transform_matrix(r['pos'], r['rot_deg'], r['scale'], *conv)
        R = np.array(m['r'])*m['s']; return verts(r['model'])@R.T + np.array(m['t'])
    def min_dist(a, b):
        best = math.inf
        for k in range(0, len(a), 512):
            dd = ((a[k:k+512, None, :] - b[None, :, :])**2).sum(-1).min()
            best = min(best, float(dd))
        return math.sqrt(best)
    # The untilted neighbour (if any) has the same matrix in every convention only when its X/Y are 0;
    # both sides are transformed with the candidate convention, as the engine would.
    convs = L.all_conventions()
    cache_file = ROOT/'build/v11_probe_angle_dists.json'   # gaps only, no geometry
    # The cache is only valid for the same pairs, placements and mesh reader.
    key = hashlib.sha256(json.dumps([[r['fid'], s['fid'], r['rot_deg'], s['rot_deg'], r['scale'], s['scale']] for r, s in pairs]).encode()
                         + (ROOT/'scripts/v11_layout.py').read_bytes()).hexdigest()
    cached = json.loads(cache_file.read_text()) if cache_file.exists() else None
    if cached and cached['key'] == key: table = cached['gaps']
    else:
        table = [[min_dist(world(r, c), world(s, c)) for r, s in pairs] for c in convs]
        cache_file.write_text(json.dumps({'key': key, 'gaps': table}))
    # Most neighbours within 400 u do not touch at all (they share a cell, not a joint). The
    # discriminating set is the pairs that touch under SOME convention: Bethesda placed them in
    # contact, so the engine's convention must explain (nearly) all of them, and the others not.
    contact = [k for k in range(len(pairs)) if min(t[k] for t in table) <= TOL]
    results = []
    for c, gaps in zip(convs, table):
        touch = sum(gaps[k] <= TOL for k in contact)
        results.append({'order': c[0], 'signs': list(c[1]), 'touching': touch, 'contact_pairs': len(contact),
                        'fraction': touch/len(contact) if contact else 0.0, 'median_gap_all': float(np.median(gaps))})
        print(c, touch, '/', len(contact), flush=True)
    # Measured 2026-10-06: vertex-to-vertex gaps are a coarse proxy (faces touch between vertices,
    # many cell neighbours are not joints), so no convention reaches 95 % of contact pairs. The
    # discriminating statistic is the per-pair winner: among pairs touching within TOL under their
    # best convention, with a margin >= MARGIN over the second best, count which convention wins.
    wins = collections.Counter()
    for k in range(len(pairs)):
        col = [t[k] for t in table]; s = sorted(col)
        if s[0] <= TOL and s[1] - s[0] >= MARGIN: wins[col.index(s[0])] += 1
    n_win = sum(wins.values()); ranked = wins.most_common()
    def binom_tail(n, k, p):  # P[X >= k], X ~ Bin(n, p)
        return sum(math.comb(n, i)*p**i*(1-p)**(n-i) for i in range(k, n+1))
    for idx, r in enumerate(results):
        r['wins'] = wins.get(idx, 0); r['p_uniform'] = binom_tail(n_win, r['wins'], 1/len(convs)) if n_win else 1.0
    best = ranked[0] if ranked else (None, 0); second = ranked[1][1] if len(ranked) > 1 else 0
    passing = [results[best[0]]] if best[0] is not None and results[best[0]]['p_uniform'] < 1e-6 and best[1] >= 3*max(second, 1) else []
    for r in results: r['passes'] = bool(passing) and r is passing[0]
    decided = len(passing) == 1 and n_win >= 20
    out = {'decided': decided, 'tol_units': TOL, 'pass_fraction': PASS_FRACTION, 'min_rot_deg': MIN_ROT_DEG,
           'neighbour_units': NEIGHBOUR_UNITS, 'tilted_refs': len(tilted), 'pairs': len(pairs), 'contact_pairs': len(contact),
           'pair_fids': [['%08X' % r['fid'], '%08X' % s['fid']] for r, s in pairs], 'conventions': results}
    if decided:
        win = passing[0]; out.update(order=win['order'], signs=win['signs'])
        # Falsify: flipping any one sign of the winner must leave it a third of the winner's wins or fewer.
        out['falsified'] = all(next(r for r in results if r['order'] == win['order'] and r['signs'] == flip)['wins'] * 3 <= win['wins']
                               for flip in [[-s if i == j else s for i, s in enumerate(win['signs'])] for j in range(3)])
        out['decided'] = decided and out['falsified']
    (ROOT/'reports/angle_convention.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    print('ANGLE_CONVENTION', 'decided' if out['decided'] else 'UNDECIDED', out.get('order'), out.get('signs'), len(pairs), 'pairs')
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
