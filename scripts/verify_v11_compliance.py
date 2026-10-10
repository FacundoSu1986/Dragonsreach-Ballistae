"""Plan task 12: no vanilla geometry in v11 (spec §4 'Cumplimiento'; THIRD_PARTY_POLICY.md). Blender, read-only.

  - no shape of torre.nif repeats the vertices of a vanilla mesh the layout or the builds use, in its
    own frame or where the layout places it;
  - no object of a .blend in source/ repeats them either (the builds import vanilla donors only to
    copy materials or a collision recipe);
  - the folder holds no other NIF, DDS, ESM, BSA or BA2 than the three own NIFs (build/ excluded:
    caches that are never shipped);
  - no report holds vertex lists.
Falsified: a shape made of a vanilla mesh's vertices must be caught. Vanilla meshes are read from
config.extracted into memory only.
"""
import bpy, json, sys, hashlib
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]
import v11_layout as L

CFG = L.load_cfg()
DONORS = ('architecture/farmhouse/lumbermill01.nif', 'clutter/civilwar/catapult/civilwarcatapult01.nif',
          'dlc01/traps/crossbowtraps/plaincrossbow/plaincrossbowtrap01.nif', 'dlc01/weapons/crossbow/boltprojectile.nif',
          'clutter/stockade/stockadewoodbeam01.nif', 'clutter/stockade/stockadescaffoldtop0sided01.nif')
MATCH = 8              # shared vertices (to 0.01 u) that count as a copy
OWN_NIFS = {'mod/meshes/AstraAsedio/torre.nif', 'mod/meshes/AstraAsedio/ballesta.nif', 'mod/meshes/AstraAsedio/virote.nif'}

def key_set(V, scale=1.0): return {tuple(np.round(np.asarray(v)*scale, 2)) for v in V}

def vanilla_sets():
    out = {}
    models = {p['modl'].replace('\\', '/').lower() for p in CFG['tower_v11']['pieces']} | set(DONORS)
    for m in sorted(models):
        V, _T = L.nif_triangles(Path(CFG['extracted'])/'meshes'/m)
        if len(V): out[m] = key_set(V)
    for p in CFG['tower_v11']['pieces']:
        V, _T = L.piece_mesh(p, CFG); out['placed:' + p['name']] = key_set(V)
    return out

def copies(V, sets, scale=1.0):
    k = key_set(V, scale); return {name: n for name, s in sets.items() if (n := len(k & s)) >= MATCH}

def main():
    sets = vanilla_sets(); report = {'match_threshold': MATCH, 'vanilla_sets': len(sets)}
    # 1. torre.nif, shape by shape
    import nif_nodos, nif_fisica, struct
    nif = nif_nodos.leer(str(ROOT/'mod/meshes/AstraAsedio/torre.nif')); d = nif['datos']; mp = nif_fisica._mundo_padre(nif)
    torre = {}
    for i, name, _o, local, _s, _a, desc, nv, datos in nif_fisica._shapes(nif):
        m = nif_fisica._mul(mp(i), local); paso = (desc & 0xF)*4
        V = [nif_fisica._aplicar(m, struct.unpack_from('<3f', d, datos + k*paso)) for k in range(nv)]
        hit = copies(V, sets)
        if hit: torre[name] = hit
    report['torre_nif_copies'] = torre
    # 2. source .blend files, object by object (local and world coordinates; scenes are in metres or units)
    blends = {}; collision_objects = {}
    for path in sorted((ROOT/'source').glob('*.blend')):
        bpy.ops.wm.open_mainfile(filepath=str(path), use_scripts=False, load_ui=False); found = {}
        # For the record: Havok shape objects kept in the scene (own collision, or a donor's box recipe).
        collision_objects[path.name] = sorted('%s (%d vertices)' % (o.name, len(o.data.vertices)) for o in bpy.data.objects
                                              if o.type == 'MESH' and o.name.startswith('bhk'))
        for o in bpy.data.objects:
            if o.type != 'MESH' or not len(o.data.vertices): continue
            local = [tuple(v.co) for v in o.data.vertices]; world = [tuple(o.matrix_world @ v.co) for v in o.data.vertices]
            hit = {}
            for V in (local, world):
                for scale in (1.0, 70.0): hit.update(copies(V, sets, scale))
            if hit: found[o.name] = hit
        blends[path.name] = found
    report['blend_copies'] = blends; report['blend_collision_objects'] = collision_objects
    # 3. files
    stray = sorted(str(p.relative_to(ROOT)).replace('\\', '/') for p in ROOT.rglob('*')
                   if p.is_file() and p.suffix.lower() in ('.nif', '.dds', '.esm', '.bsa', '.ba2') and 'build' not in p.relative_to(ROOT).parts
                   and str(p.relative_to(ROOT)).replace('\\', '/') not in OWN_NIFS)
    report['stray_files'] = stray
    # 4. reports: no list of points that repeats a vanilla mesh. Measured 2026-10-06: the inherited
    # point lists are own ballista pieces (limb_ties_*) and bounding-box corners (projectile_donor).
    def point_lists(x):
        if isinstance(x, list):
            if len(x) >= MATCH and all(isinstance(t, list) and len(t) == 3 and all(isinstance(c, (int, float)) for c in t) for t in x):
                yield x; return
            for y in x: yield from point_lists(y)
        elif isinstance(x, dict):
            for y in x.values(): yield from point_lists(y)
    flagged = {}
    for p in sorted((ROOT/'reports').glob('*.json')):
        for pts in point_lists(json.loads(p.read_text(encoding='utf-8'))):
            hit = {}
            for scale in (1.0, 70.0): hit.update(copies(pts, sets, scale))
            if hit: flagged.setdefault(p.name, []).append(hit)
    report['reports_with_vertex_lists'] = flagged
    # Falsification: a shape that is a vanilla mesh must be caught.
    fake_V, _T = L.nif_triangles(Path(CFG['extracted'])/'meshes'/'clutter/stockade/stockadewoodbeam01.nif')
    report['falsified'] = bool(copies(fake_V, sets))
    report['ok'] = (not torre and not any(blends.values()) and not stray and not report['reports_with_vertex_lists'] and report['falsified'])
    report['torre_nif_sha256'] = hashlib.sha256((ROOT/'mod/meshes/AstraAsedio/torre.nif').read_bytes()).hexdigest()
    (ROOT/'reports/v11_compliance.json').write_text(json.dumps(report, indent=2))
    print('V11_COMPLIANCE', 'ok' if report['ok'] else 'FAILED', {k: report[k] for k in ('torre_nif_copies', 'blend_copies', 'stray_files', 'reports_with_vertex_lists', 'falsified')})
    if not report['ok']: raise SystemExit('compliance failed')

main()
