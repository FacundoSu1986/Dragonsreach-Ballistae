"""Patch the tested v11 ESP without rebuilding weapon, scripts or world/terrain.

Always read the immutable v11 baseline. Preserve reference identities in both cells.
Only structure, shield DATA, ballista Z, and laboratory NAVM/NAVI may change.

v22 — este script es el dueno de `mod/AstraAsedio.esp` y el que lo valida, asi que tiene que
dejar el plugin COMPLETO: `validate_plugin` exige los dos scripts del ACTI, el GLOB, el NPC_
del guardia y los XLKR reciprocos. Por eso el guardia autonomo entra aca y no en un stage
posterior. Ademas refresca las properties que manda `config.json`: el baseline v11 es
inmutable y conserva los tiempos de su epoca (Fire 0.3, Release 0.1, Reset 1.2, Cycle 1.5,
PitchMin -5, PitchPivotHeight 153), y el pivote tiene que seguir la bajada de 36 u del NIF.

`build_modular_v13.py` corre despues y solo agrega las formas modulares 0x03000B00-03 que
los tres addons referencian como master 03.
"""
import json
import hashlib
import math
import struct
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.with_name('Ballesta_Astra_Vanilla_SE_v11')
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]
import colocar_escudos as C
import build_plugin as B
import mundo_v11 as M
from parser_esm import Plugin
import escritor_plugin as W

def modify_subs(raw, updates):
    body = b''.join(W.sub(k, updates.get(k, v)) for k, v in Plugin.subrecords(raw[24:]))
    return raw[:4] + struct.pack('<I', len(body)) + raw[8:24] + body

def record_map(p):
    return {p.form_id(o): p.d[o:o+24+n] for t, o, n, dep in p.recorrer() if t not in ('GRUP', 'TES4')}

def transform_groups(group, changes, removed, added):
    label, typ = C.etiqueta(group)
    children = []
    for off, size, raw in C.hijos(group):
        if raw[:4] == b'GRUP':
            children.append(transform_groups(raw, changes, removed, added))
        else:
            fid = struct.unpack_from('<I', raw, 12)[0]
            if fid not in removed: children.append(changes.get(fid, raw))
    # `added` va por (label, tipo de grupo): 8 = persistentes de la celda, 9 = temporales.
    # El guardia es persistente (como la ballesta a la que se enlaza), los escudos temporales.
    if typ in (8, 9): children.extend(added.get((label, typ), []))
    return C.rearmar(group, children)

def add_group(groups, label, records):
    """Agrega records al grupo de nivel superior `label`, o lo crea si no existe."""
    key = struct.unpack('<I', label.encode())[0]
    for i, g in enumerate(groups):
        if C.etiqueta(g) == (key, 0):
            groups[i] = C.rearmar(g, [r for o, n, r in C.hijos(g)] + list(records))
            return
    groups.append(W.grupo(label, list(records)))

def update_header(raw, count, next_id):
    body = []
    for k, v in Plugin.subrecords(raw[24:]):
        if k == 'HEDR': v = v[:4] + struct.pack('<II', count, next_id)
        body.append(W.sub(k, v))
    body = b''.join(body)
    return raw[:4] + struct.pack('<I', len(body)) + raw[8:24] + body

def auto_props(cfg, gcfg):
    """Las 23 properties Auto sin default de `AstraGuardiaAuto.psc`.

    Los tres nombres de nodo (`YawNode`/`PitchNode`/`VisualBoltNode`) son strings CON default
    en el PSC, asi que no viajan en el VMAD. `PitchMin`/`PitchMax`/`YawSpeed`/`PitchSpeed`/
    `ReleaseSegundos` los espeja `validate_plugin` contra el config de nivel superior, igual
    que el script del jugador: la torreta no puede tener limites distintos de la maquina."""
    return {'Launcher': (1, B.IDS['launcher']), 'ShotAmmo': (1, B.IDS['ammo']),
            'ShotSound': (1, B.IDS['shot_sound']), 'OcupadaGuardia': (1, B.IDS['ocupada']),
            'VelocidadProyectil': (4, gcfg['velocidad_proyectil']),
            'GravedadProyectil': (4, gcfg['gravedad_proyectil']),
            'MuzzleAlto': (4, gcfg['muzzle_alto']), 'MuzzleAdelante': (4, gcfg['muzzle_adelante']),
            'YawSpeed': (4, cfg['yaw_speed']), 'PitchSpeed': (4, cfg['pitch_speed']),
            'PitchMin': (4, cfg['pitch_min']), 'PitchMax': (4, cfg['pitch_max']),
            'ArcMax': (4, gcfg['arc_max']), 'AlcanceMin': (4, gcfg['alcance_min']),
            'AlcanceMax': (4, gcfg['alcance_max']), 'MargenLinea': (4, gcfg['margen_linea']),
            'MargenImpacto': (4, gcfg['margen_impacto']), 'MaxRafaga': (3, gcfg['max_rafaga']),
            'Enfriamiento': (4, gcfg['enfriamiento']), 'Anticipacion': (4, gcfg['anticipacion']),
            'ReleaseSegundos': (4, cfg['release_seconds']),
            'TickSegundos': (4, gcfg['tick_segundos']), 'QALog': (5, gcfg['qa_log'])}

def guard_records(cfg, gcfg):
    """GLOB arbitro + NPC_ clon del guardia. Devuelve (glob, npc, donante, paquete).

    Misma logica que `build_plugin.guard_records`: el donante es una PRIORIDAD de
    `guardia.donores_npc`, y hay que borrar los templateFlags que gobiernan lo que se hereda
    del TPLT, o el nombre del config se ignora y el guardia se va caminando a su ciudad."""
    data = Path(cfg['runtime']) / 'Data'
    donor = B.find_guard_npc(data / 'Skyrim.esm', gcfg['donores_npc'])
    pack = None
    if gcfg.get('paquete_torre'):
        pack = B.find_records(data / 'Skyrim.esm', [gcfg['paquete_torre']])[gcfg['paquete_torre']]
        if pack['type'] != 'PACK':
            raise ValueError('guardia.paquete_torre debe ser un PACK, no ' + pack['type'])
        pldts = [v for k, v in pack['subs'] if k == 'PLDT']
        if not pldts or any(struct.unpack_from('<I', v, 0)[0] != 3 for v in pldts):
            raise ValueError('guardia.paquete_torre %s debe anclarse a la ubicacion del editor (PLDT type=3)' % gcfg['paquete_torre'])
        if any(k == 'CTDA' for k, _ in pack['subs']):
            raise ValueError('guardia.paquete_torre %s debe ser incondicional (sin CTDA)' % gcfg['paquete_torre'])
    drop = 0x0080 | (0x0020 if pack else 0)
    subs = []; pkid = False; full = False
    for k, v in donor['subs']:
        if k == 'EDID':
            subs.append(W.sub('EDID', W.zstr('AstraGuardiaNPC')))
            subs.append(W.sub('VMAD', B.vmad('AstraGuardiaNPC', {})))
        elif k == 'VMAD':
            continue
        elif k == 'FULL':
            subs.append(W.sub('FULL', W.zstr(gcfg['nombre']))); full = True
        elif k == 'PKID' and pack:
            if not pkid:
                subs.append(W.sub('PKID', struct.pack('<I', pack['fid']))); pkid = True
        elif k == 'ACBS':
            acbs = bytearray(v)
            struct.pack_into('<H', acbs, 18, struct.unpack_from('<H', acbs, 18)[0] & ~drop)
            subs.append(W.sub('ACBS', bytes(acbs)))
        else:
            subs.append(W.sub(k, v))
    if pack and not pkid:
        at = next((i for i, s in enumerate(subs) if s[:4] == b'AIDT'), len(subs) - 1)
        subs.insert(at + 1, W.sub('PKID', struct.pack('<I', pack['fid'])))
    if not full:
        at = next((i for i, s in enumerate(subs) if s[:4] == b'CNAM'), len(subs) - 1)
        subs.insert(at + 1, W.sub('FULL', W.zstr(gcfg['nombre'])))
    npc = W.record('NPC_', B.IDS['guardia'], subs)
    glob = W.record('GLOB', B.IDS['ocupada'], [W.sub('EDID', W.zstr('AstraGuardiaOcupada')),
                                                W.sub('FNAM', b's\0'),
                                                W.sub('FLTV', struct.pack('<f', 0.0))])
    return glob, npc, donor, pack

def ballesta_ref_with_link(raw, delta, guard_ref):
    """DATA con la Z de la bajada v12 + XLKR reciproco hacia el guardia.

    `modify_subs` solo reemplaza subrecords que YA existen, y el REFR del baseline v11 no
    tiene XLKR, asi que hay que insertarlo a mano (despues de NAME, como pide el orden de
    REFR en TES5)."""
    subs = []
    for k, v in Plugin.subrecords(raw[24:]):
        if k == 'DATA':
            xyz = list(struct.unpack('<6f', v)); xyz[2] += delta
            subs.append(W.sub('DATA', struct.pack('<6f', *xyz)))
        else:
            subs.append(W.sub(k, v))
        if k == 'NAME' and guard_ref:
            subs.append(W.sub('XLKR', struct.pack('<II', guard_ref, 0)))
    return W.record('REFR', struct.unpack_from('<I', raw, 12)[0], subs,
                    struct.unpack_from('<I', raw, 8)[0])

def main():
    cfg = json.loads((ROOT/'config.json').read_text(encoding='utf-8'))
    p = Plugin(str(BASE/'mod/AstraAsedio.esp'))
    source = record_map(p)
    delta = cfg['revision_v12']['delta_units']
    mapping = {int(r['origen'], 16): int(r['nuevo'], 16) for r in
               json.loads((BASE/'reports/mundo_esp_v11.json').read_text())['refr_en_mundo']}
    oldcfg = json.loads((BASE/'config.json').read_text(encoding='utf-8'))
    removed_local = set(range(B.VANILLA_FIRST, B.VANILLA_FIRST + len(oldcfg['tower_v11']['pieces'])))
    removed = removed_local | {mapping[i] for i in removed_local}
    changes = {}
    # --- v22: el ACTI y el guardia autonomo -------------------------------------------------
    # El baseline v11 es inmutable y trae los tiempos de su epoca, asi que el parche tiene que
    # dejarlos en los valores que manda config.json: validate_plugin los compara y el build
    # moria con "bad VMAD timing FireSeconds". PitchPivotHeight entra tambien porque el NIF
    # bajo 36 u (v22) y la mira del ESP tiene que bajar con el.
    gcfg = cfg.get('guardia')
    guard_ref = B.IDS['guardia_ref']
    if guard_ref in source and guard_ref not in removed:
        raise ValueError('guardia_ref %08X choca con un record del baseline (esperado: una pieza '
                         'vanilla que este parche borra)' % guard_ref)
    acti_raw = source[B.IDS['ballesta']]
    vm = B.read_vmad(dict(Plugin.subrecords(acti_raw[24:]))['VMAD'])['scripts'][0]
    if vm['name'] != 'AstraAsedioActi':
        raise ValueError('el ACTI del baseline v11 no corre AstraAsedioActi: ' + vm['name'])
    props = {k: (v['type'], v['value']['form_id'] if v['type'] == 1 else v['value'])
             for k, v in vm['properties'].items()}
    for key, name in {'FireSeconds': 'fire_seconds', 'ReleaseSeconds': 'release_seconds',
                      'ResetSeconds': 'reset_seconds', 'CycleSeconds': 'cycle_seconds',
                      'YawSpeed': 'yaw_speed', 'PitchSpeed': 'pitch_speed',
                      'PitchMin': 'pitch_min', 'PitchMax': 'pitch_max',
                      'PitchPivotHeight': 'pitch_pivot_units'}.items():
        props[key] = (4, cfg[name])
    props['UseSightCamera'] = (5, cfg['use_sight_camera'])
    props['ContinuousFire'] = (5, cfg['continuous_fire'])
    acti_scripts = [('AstraAsedioActi', props)]
    top = []
    if gcfg:
        # El arbitro sesion/demo <-> torre: la torre cede siempre que el jugador opere.
        props['OcupadaGuardia'] = (1, B.IDS['ocupada'])
        glob, npc, guard_donor, guard_pack = guard_records(cfg, gcfg)
        acti_scripts.append(('AstraGuardiaAuto', auto_props(cfg, gcfg)))
        top = [('GLOB', glob), ('NPC_', npc)]
    changes[B.IDS['ballesta']] = modify_subs(acti_raw, {'VMAD': B.vmad_multi(acti_scripts)})
    # --- fin v22 ----------------------------------------------------------------------------
    bbox = json.loads((ROOT/'reports/assets.json').read_text())['torre']['bbox_units']
    obnd = [math.floor(v) for v in bbox['min']] + [math.ceil(v) for v in bbox['max']]
    changes[B.IDS['tower']] = modify_subs(source[B.IDS['tower']], {'OBND': struct.pack('<6h', *obnd)})
    # La ballesta local lleva XLKR reciproco hacia el guardia; su gemela del mundo no, porque
    # alla no hay guardia. El engine instancia actores solo desde ACHR.
    changes[B.IDS['ballesta_ref']] = ballesta_ref_with_link(source[B.IDS['ballesta_ref']], delta,
                                                            guard_ref if gcfg else 0)
    world_ballesta = mapping[B.IDS['ballesta_ref']]
    changes[world_ballesta] = ballesta_ref_with_link(source[world_ballesta], delta, 0)
    added = {(B.IDS['cell'], 9): [], (0x963D, 9): [], (B.IDS['cell'], 8): []}
    if gcfg:
        # El guardia es persistente, igual que la ballesta a la que se enlaza.
        gx, gy, gz = gcfg['posicion']
        added[(B.IDS['cell'], 8)].append(B.reference(
            guard_ref, B.IDS['guardia'], (gx, gy, gz), math.atan2(-gx, -gy),
            edid='AstraGuardiaREF', persistent=True, link=B.IDS['ballesta_ref'], tipo='ACHR'))
    for i, item in enumerate(cfg['tower_v11']['escudos']['items']):
        local_fid = C.REFR_BASE + i
        old = i < 5
        world_fid = mapping[local_fid] if old else 0x03000A48 + i - 5
        pos, rot = item['pos'], item['rot_deg']
        world_pos, world_rot = M.llevar({'pos': pos, 'rot_deg': rot, 'scale': 1.0}, cfg['tower_v11']['mundo'])
        for fid, position, rotation, cell, suffix in (
            (local_fid, pos, rot, B.IDS['cell'], ''),
            (world_fid, world_pos, world_rot, 0x963D, 'Mundo')):
            data = struct.pack('<6f', *position, *(math.radians(v) for v in rotation))
            if old:
                changes[fid] = modify_subs(source[fid], {'DATA': data})
            else:
                if fid in source: raise ValueError('New FormID already used: %08X' % fid)
                added[(cell, 9)].append(C.referencia(fid, C.STAT_ESCUDO, position,
                                   tuple(math.radians(v) for v in rotation), 'AstraEscudo'+item['nombre']+suffix))
    nv, mi, navreport = B.navmesh_geometry()
    changes[B.IDS['navmesh']] = modify_subs(source[B.IDS['navmesh']], {'NVNM': nv})
    changes[0x12FB4] = modify_subs(source[0x12FB4], {'NVMI': mi})
    original = p.d
    start = C.leer_cabecera(original)[4]
    groups = []
    off = start
    while off < len(original):
        size = struct.unpack_from('<I', original, off+4)[0]
        raw = original[off:off+size]
        groups.append(transform_groups(raw, changes, removed, added))
        off += size
    # GLOB y NPC_ no existian en el baseline v11: van en grupos de nivel superior nuevos.
    for label, record in top:
        add_group(groups, label, [record])
    body = b''.join(groups)
    count = C.bloques_totales(body, 0)
    header = update_header(original[:start], count, 0xA4F)
    out = ROOT/'mod/AstraAsedio.esp'
    out.write_bytes(header+body)
    result = record_map(Plugin(str(out)))
    for fid, raw in source.items():
        if fid not in removed and fid not in changes and result.get(fid) != raw:
            raise ValueError('Unexpected record change: %08X' % fid)
    expected_new = {struct.unpack_from('<I', r, 12)[0] for items in added.values() for r in items}
    expected_new |= {struct.unpack_from('<I', r, 12)[0] for _, r in top}
    if result.keys() != (source.keys() - removed | expected_new):
        raise ValueError('Record IDs differ from allowlist')
    checked = B.validate_plugin(str(out))
    if checked['navmesh_components'] != 1: raise ValueError('Disconnected navigation')
    report = {'source_sha256': hashlib.sha256(original).hexdigest(),
              'sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'bytes': out.stat().st_size,
              'removed_refs': ['%08X'%i for i in sorted(removed)],
              'changed_records': ['%08X'%i for i in sorted(changes)],
              'added_refs': ['%08X'%i for i in sorted(expected_new)],
              'all_other_records_preserved_byte_for_byte': True,
              'land_and_vanilla_overrides_preserved': True,
              'navmesh': navreport, 'validation': checked,
              'world_own_refs': 15, 'local_shields': 12, 'world_shields': 12,
              'guardia': ({'donante_npc': guard_donor['edid'], 'donante_fid': '%08X' % guard_donor['fid'],
                           'paquete_torre': gcfg.get('paquete_torre'),
                           'paquete_torre_fid': ('%08X' % guard_pack['fid']) if guard_pack else None,
                           'template_flags_borrados': ['BaseData (0x0080)'] + (['AIPackages (0x0020)'] if guard_pack else []),
                           'glob_ocupada': '%08X' % B.IDS['ocupada'], 'npc': '%08X' % B.IDS['guardia'],
                           'ref': '%08X' % guard_ref, 'ref_tipo': 'ACHR',
                           'xlkr_reciproco': ['%08X' % B.IDS['ballesta_ref'], '%08X' % guard_ref],
                           'auto_script': 'AstraGuardiaAuto (2.º VMAD del ACTI)'} if gcfg else None),
              'game_tested': False}
    (ROOT/'reports/plugin_v12.json').write_text(json.dumps(report, indent=2))
    print('V12_PLUGIN_PATCHED', report['bytes'], 'removed', len(removed), 'new', len(expected_new),
          'navmesh', checked['navmesh_vertices'], checked['navmesh_triangles'], 'components', checked['navmesh_components'],
          'guardia', (guard_donor['edid'] if gcfg else 'off'))

if __name__ == '__main__': main()
