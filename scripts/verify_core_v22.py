"""Verify the v22 core ESP: guard wiring, modular forms, and addon master resolution.

Nace de un bug real de integracion: el runbook del merge mandaba regenerar el core con
`build_plugin.py`, que produce un ESP SIN las formas modulares `0x030009C0`/`0x03000B00-03`.
Los tres addons las referencian como master 03, asi que el resultado era un producto con
masters colgantes que ningun test detectaba (nadie comparaba el core contra los addons).

Uso: python scripts/verify_core_v22.py
"""
import collections, json, struct, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'scripts/vendor')]
from parser_esm import Plugin
import build_plugin as B

CORE = ROOT / 'mod/AstraAsedio.esp'
ADDONS = ['addons/Atalaya/AstraAsedio_Atalaya.esp',
          'addons/Whiterun/AstraAsedio_Whiterun.esp',
          'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp']
# Formas del core que los addons referencian por master index 03.
MODULAR = {0x030009C0: 'STAT', 0x03000B00: 'PROJ', 0x03000B01: 'AMMO',
           0x03000B02: 'ACTI', 0x03000B03: 'STAT', 0x03000B04: 'ACTI'}
REF_SUBS = ('NAME', 'TPLT', 'WNAM', 'CNAM', 'INAM', 'SCRI', 'SDSC')

# Dos torretas, mismo contrato (clone del ACTI del jugador sin VMAD) y distinto MODL.
# El alto lleva la mira nativa (pivote 153, contrato de camara de v10); el bajo (pivote
# 117, -36 u) es la ergonomia de la animacion del guardia y solo puede ir donde NO hay
# mira nativa. Ver `reports/sight_path_v22_FAILED.json` para la medicion del fallo.
MODELO_ALTO = 'AstraAsedio\\ballesta.nif'
MODELO_BAJO = 'AstraAsedio\\ballesta_guardia.nif'

fails = []


def check(cond, msg):
    print(('  OK   ' if cond else '  FAIL ') + msg)
    if not cond:
        fails.append(msg)


def records(path):
    p = Plugin(str(path))
    recs, order = {}, []
    for t, o, n, d in p.recorrer():
        if t == 'GRUP':
            continue
        fid = p.form_id(o)
        recs[fid] = (t, dict(p.subrecords(p.datos(o))))
        order.append(fid)
    return p, recs, order


def masters(plugin):
    tes4 = plugin.d[24:24 + struct.unpack_from('<I', plugin.d, 4)[0]]
    return [v.rstrip(b'\0').decode() for k, v in Plugin.subrecords(tes4) if k == 'MAST']


def main():
    if not CORE.exists():
        print('FAIL falta', CORE); return 1
    p, recs, order = records(CORE)
    cfg = json.loads((ROOT / 'config.json').read_text())
    gcfg = cfg.get('guardia')

    print('== 1) core: masters y unicidad de FormID ==')
    check(masters(p) == ['Skyrim.esm', 'Update.esm', 'Dawnguard.esm'], 'masters = Skyrim/Update/Dawnguard')
    dupes = [f for f, c in collections.Counter(order).items() if c > 1]
    check(not dupes, 'sin FormIDs duplicados' + ('' if not dupes else ' ' + str([f'{d:08X}' for d in dupes])))

    print('== 2) core: formas modulares que referencian los addons ==')
    for fid, want in sorted(MODULAR.items()):
        t, ss = recs.get(fid, ('<ausente>', {}))
        edid = ss.get('EDID', b'').rstrip(b'\0').decode('cp1252', 'replace')
        check(t == want, f'{fid:08X} {want} {edid!r}')
    check(B.IDS['guardia_ref'] not in recs or recs[B.IDS['guardia_ref']][0] == 'ACHR',
          f'{B.IDS["guardia_ref"]:08X} libre (pieza vanilla borrada) o ACHR del guardia')

    print('== 3) core: el ACTI lleva los dos scripts con las properties del config ==')
    t, ss = recs[B.IDS['ballesta']]
    vm = B.read_vmad(ss['VMAD'])
    names = [s['name'] for s in vm['scripts']]
    check(names == ['AstraAsedioActi', 'AstraGuardiaAuto'], f'scripts = {names}')
    p0 = vm['scripts'][0]['properties']
    for key, name in [('FireSeconds', 'fire_seconds'), ('ReleaseSeconds', 'release_seconds'),
                      ('ResetSeconds', 'reset_seconds'), ('CycleSeconds', 'cycle_seconds')]:
        check(abs(p0[key]['value'] - cfg[name]) < 1e-5, f'AstraAsedioActi.{key} == config.{name}')
    # El pivote tiene que seguir la bajada del NIF o la mira apunta alto.
    check(abs(p0['PitchPivotHeight']['value'] - cfg['pitch_pivot_units']) < 1e-5,
          f'PitchPivotHeight = {p0["PitchPivotHeight"]["value"]} == config.pitch_pivot_units')
    if not gcfg:
        print('  (config.guardia ausente: se saltea el resto)')
    else:
        p1 = vm['scripts'][1]['properties']
        for key, ck in [('VelocidadProyectil', 'velocidad_proyectil'), ('GravedadProyectil', 'gravedad_proyectil'),
                        ('MuzzleAlto', 'muzzle_alto'), ('MuzzleAdelante', 'muzzle_adelante'),
                        ('ArcMax', 'arc_max'), ('AlcanceMin', 'alcance_min'), ('AlcanceMax', 'alcance_max'),
                        ('MargenLinea', 'margen_linea'), ('MargenImpacto', 'margen_impacto'),
                        ('Enfriamiento', 'enfriamiento'), ('Anticipacion', 'anticipacion'),
                        ('TickSegundos', 'tick_segundos')]:
            check(abs(p1[key]['value'] - gcfg[ck]) < 1e-4, f'AstraGuardiaAuto.{key} == guardia.{ck}')
        check(p1['MaxRafaga']['value'] == gcfg['max_rafaga'], 'AstraGuardiaAuto.MaxRafaga')
        for key, ck in [('YawSpeed', 'yaw_speed'), ('PitchSpeed', 'pitch_speed'),
                        ('PitchMin', 'pitch_min'), ('PitchMax', 'pitch_max'),
                        ('ReleaseSegundos', 'release_seconds')]:
            check(abs(p1[key]['value'] - cfg[ck]) < 1e-4, f'AstraGuardiaAuto.{key} espeja config.{ck}')
        for key, target in [('Launcher', B.IDS['launcher']), ('ShotAmmo', B.IDS['ammo']),
                            ('ShotSound', B.IDS['shot_sound']), ('OcupadaGuardia', B.IDS['ocupada'])]:
            check(p1[key]['value'] == {'form_id': target, 'alias': -1}, f'AstraGuardiaAuto.{key} -> {target:08X}')

    print('== 4) core: GLOB / NPC_ / ACHR del guardia ==')
    if gcfg:
        t, g = recs[B.IDS['ocupada']]
        check(t == 'GLOB' and g['FNAM'] == b's\0' and struct.unpack('<f', g['FLTV'])[0] == 0.0,
              f'GLOB {B.IDS["ocupada"]:08X} float 0.0')
        t, n = recs[B.IDS['guardia']]
        check(t == 'NPC_', f'NPC_ {B.IDS["guardia"]:08X}')
        check(n['FULL'].rstrip(b'\0').decode('cp1252') == gcfg['nombre'], 'FULL == guardia.nombre')
        if gcfg.get('paquete_torre'):
            pack = B.find_records(Path(cfg['runtime']) / 'Data/Skyrim.esm', [gcfg['paquete_torre']])[gcfg['paquete_torre']]
            check(struct.unpack('<I', n['PKID'])[0] == pack['fid'],
                  f'PKID = {struct.unpack("<I", n["PKID"])[0]:08X} ({gcfg["paquete_torre"]})')
        tfl = struct.unpack_from('<H', n['ACBS'], 18)[0]
        # Sin borrar estos bits el clon hereda el nombre y las patrullas del template.
        check(tfl & 0x0080 == 0, f'templateFlags.BaseData borrado (templateFlags={tfl:04X})')
        if gcfg.get('paquete_torre'):
            check(tfl & 0x0020 == 0, 'templateFlags.AIPackages borrado (manda paquete_torre)')
        nv = B.read_vmad(n['VMAD'])
        check(nv['scripts'][0]['name'] == 'AstraGuardiaNPC' and not nv['scripts'][0]['properties'],
              'VMAD del NPC = AstraGuardiaNPC sin properties')
        t, a = recs[B.IDS['guardia_ref']]
        # El engine solo instancia actores desde ACHR; un REFR con base NPC_ se ignora.
        check(t == 'ACHR', f'{B.IDS["guardia_ref"]:08X} es ACHR')
        check(struct.unpack('<I', a['NAME'])[0] == B.IDS['guardia'], 'ACHR.NAME -> NPC')
        check(struct.unpack('<II', a['XLKR'])[0] == B.IDS['ballesta_ref'], 'ACHR.XLKR -> ballesta')
        t, br = recs[B.IDS['ballesta_ref']]
        check(struct.unpack('<II', br['XLKR'])[0] == B.IDS['guardia_ref'], 'ballesta.XLKR -> ACHR (reciproco)')

    print('== 5) addons: masters y referencias al core ==')
    for rel in ADDONS:
        path = ROOT / rel
        if not path.exists():
            check(False, f'{rel} existe'); continue
        ap, arecs, _ = records(path)
        check(masters(ap)[-1] == 'AstraAsedio.esp', f'{rel}: ultimo master = AstraAsedio.esp')
        dangling = collections.Counter()
        for _, (t, ss) in arecs.items():
            for k in REF_SUBS:
                v = ss.get(k)
                if v and len(v) == 4:
                    ref = struct.unpack('<I', v)[0]
                    if ref >> 24 == 3 and ref not in recs:
                        dangling[f'{ref:08X}'] += 1
        check(not dangling, f'{rel}: 0 referencias colgantes a master 03' +
              ('' if not dangling else ' ' + str(dict(dangling))))

    print('== 6) dos torretas: MODL alto/bajo y quien coloca cada una ==')
    modl = {}
    for fid in (B.IDS['ballesta'], 0x03000B02, 0x03000B04):
        t, ss = recs.get(fid, ('<ausente>', {}))
        modl[fid] = ss.get('MODL', b'').rstrip(b'\0').decode('cp1252', 'replace')
    check(modl[B.IDS['ballesta']] == MODELO_ALTO,
          f'ACTI {B.IDS["ballesta"]:08X} (jugador) MODL = {modl[B.IDS["ballesta"]]!r}')
    check(modl[0x03000B02] == MODELO_ALTO,
          f'ACTI 03000B02 (tombstones deshabilitados) MODL = {modl[0x03000B02]!r}')
    check(modl[0x03000B04] == MODELO_BAJO,
          f'ACTI 03000B04 (guardia, sin mira) MODL = {modl[0x03000B04]!r}')
    nif_alto = ROOT / 'mod/meshes/AstraAsedio/ballesta.nif'
    nif_bajo = ROOT / 'mod/meshes/AstraAsedio/ballesta_guardia.nif'
    check(nif_alto.exists() and nif_bajo.exists(), 'existen ballesta.nif y ballesta_guardia.nif')
    if nif_alto.exists() and nif_bajo.exists():
        check(nif_alto.read_bytes() != nif_bajo.read_bytes(),
              'ballesta_guardia.nif es un archivo distinto de ballesta.nif')

    # El invariante que hace segura la torreta baja: NINGUNA referencia ACTIVA que la use
    # puede dejar que el jugador la opere, porque la mira nativa degenera con el pivote en
    # 117 (`reports/sight_path_v22_FAILED.json`). Se recorre TODO lo que apunta al ACTI bajo
    # en vez de una lista fija: una colocacion nueva que se olvide del flag rompe el test.
    DISABLED = 0x800
    usos_bajo, usos_alto = [], []
    for rel in ADDONS:
        ap, arecs, _ = records(ROOT / rel)
        for fid, (t, ss) in arecs.items():
            if 'NAME' not in ss or len(ss['NAME']) != 4:
                continue
            base = struct.unpack('<I', ss['NAME'])[0]
            if base not in (0x03000B04, B.IDS['ballesta'], 0x03000B02):
                continue
            off = next(o for tt, o, nn, dd in ap.recorrer() if tt != 'GRUP' and ap.form_id(o) == fid)
            disabled = bool(struct.unpack_from('<I', ap.d, off + 8)[0] & DISABLED)
            vmad = B.read_vmad(ss['VMAD']) if 'VMAD' in ss else {'scripts': []}
            props = {k: v['value'] for s in vmad['scripts'] for k, v in s['properties'].items()}
            item = (rel.split('/')[1], fid, disabled, props.get('AllowPlayerTakeover'),
                    props.get('UseSightCamera'))
            (usos_bajo if base == 0x03000B04 else usos_alto).append(item)

    esperado_bajo = {(r, f) for r, f in [('Whiterun', 0x04000B10),
                                         ('WhiterunTorres', 0x04000B70),
                                         ('WhiterunTorres', 0x04000B80)]}
    real_bajo = {(r, f) for r, f, d, _a, _c in usos_bajo if not d}
    check(real_bajo == esperado_bajo,
          f'colocaciones ACTIVAS del ACTI bajo = {sorted(real_bajo)}')
    for r, f, d, takeover, camera in usos_bajo:
        if d:
            continue
        check(takeover is not True, f'{r} {f:08X}: sin AllowPlayerTakeover (el jugador no la opera)')
        check(camera is not True, f'{r} {f:08X}: sin UseSightCamera (no hay mira nativa que romper)')
    # Y el ACTI alto sigue siendo el del jugador, con la mira intacta.
    check(any(r == 'Atalaya' and f == 0x04000A00 for r, f, d, _a, _c in usos_alto if not d),
          'el Atalaya usa el ACTI alto del jugador')
    check(any(r == 'WhiterunTorres' and f == 0x04000B40 for r, f, d, _a, _c in usos_alto if d),
          'WhiterunTorres conserva sus tombstones deshabilitados del ACTI alto')

    print()
    if fails:
        print(f'FALLARON {len(fails)} verificaciones:')
        for f in fails:
            print('  -', f)
        return 1
    print('CORE_V22 OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
