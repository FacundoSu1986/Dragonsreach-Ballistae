"""v22: verifica las DOS torretas (alta para el jugador, baja para el guardia).

Por que existe: el diseno de dos alturas reparte el mismo contrato de Papyrus entre dos
NIF. Nada en el ESP dice que `ballesta_guardia.nif` sea `ballesta.nif` bajado 36 u, ni que
el pivote alto coincida con `config.pitch_pivot_units`, ni que el muzzle alto coincida con
`guardia.muzzle_alto`. Si esos numeros se separan, el sintoma en juego es un guardia
apuntando al aire o una mira que no apunta: exactamente el tipo de desincronizacion que ya
paso una vez (`reports/revision_adversarial_v22.md`). Aca se comparan los bytes de los dos
NIF contra el ESP y contra el config.

Uso: python scripts/verify_torreta_baja_v22.py
"""
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'scripts/vendor')]
from parser_esm import Plugin
import build_plugin as B
import nif_nodos

NIF_ALTO = ROOT / 'mod/meshes/AstraAsedio/ballesta.nif'
NIF_BAJO = ROOT / 'mod/meshes/AstraAsedio/ballesta_guardia.nif'
CORE = ROOT / 'mod/AstraAsedio.esp'

# La bajada. Espejo de `bajar_ballesta.py` (que la lee de config con estos defaults) y de
# la linea `AstraGuardiaAuto.MuzzleAlto` del PSC. Si cambia, cambian los tres lugares.
DELTA = 36.0
PIVOTE_ALTO = 153.0
PIVOTE_BAJO = 117.0
MUZZLE_ALTO = 172.6
MUZZLE_BAJO = 136.6
# Pedestal: por debajo de Z0 no se toca; TOPE es la cota mas alta del NIF v21 (el poste).
Z0 = 20.0
TOPE = 137.60

# Nodos que cuelgan del cabezal: bajan los DELTA exactos. Los dos de la raiz no se mueven.
BAJAN = ('CTRL_GIRO_360', 'CTRL_ELEVACION', 'ProjectileNode', 'AstraSightCameraNode',
         'AstraSightFrontPost', 'Cuerda_I', 'Cuerda_D', 'CTRL_BRAZO_I', 'CTRL_BRAZO_D',
         'VIROTE_VISUAL')
QUIETOS = ('AstraBallesta', 'OperatorNode')
# Mallenas del pedestal: la base no se mueve; la cota superior baja DELTA (afinidad en Z).
PEDESTAL = ('AstraBallesta_floor', 'AstraBallesta_metal', 'AstraBallesta_wood')

fails = []


def check(cond, msg):
    print(('  OK   ' if cond else '  FAIL ') + msg)
    if not cond:
        fails.append(msg)


def cerca(a, b, tol=0.02):
    return abs(a - b) <= tol


# Layout del BSTriShape, MEDIDO (mismo que documenta `bajar_ballesta.py`). Se repite aca a
# proposito: este verificador tiene que poder correr aunque el generador cambie, y un
# helper compartido lo ataria a la implementacion que justamente audita.
OFF_NUM_TRI, OFF_NUM_VERT, OFF_DATA_SIZE, OFF_VERTICES, STRIDE = 108, 110, 112, 116, 32


def bbox_z_malla(nif, nombre):
    """(z_min, z_max) de la BSTriShape llamada `nombre`. Valida el layout antes de leer."""
    for b, (tipo, off, tam) in enumerate(nif['bloques']):
        if tipo != 'BSTriShape':
            continue
        i, = struct.unpack_from('<i', nif['datos'], off)
        if nif['strings'][i] != nombre:
            continue
        nt, = struct.unpack_from('<H', nif['datos'], off + OFF_NUM_TRI)
        nv, = struct.unpack_from('<H', nif['datos'], off + OFF_NUM_VERT)
        ds, = struct.unpack_from('<I', nif['datos'], off + OFF_DATA_SIZE)
        if ds != nv * STRIDE + nt * 6 or (tam - ds) not in (OFF_VERTICES, OFF_VERTICES + 4):
            raise SystemExit('layout inesperado en %s (dataSize=%d, tam=%d)' % (nombre, ds, tam))
        ini = off + OFF_VERTICES + STRIDE * nv
        idx = struct.unpack_from('<%dH' % (3 * nt), nif['datos'], ini)
        if any(v >= nv for v in idx):
            raise SystemExit('indices fuera de rango en %s' % nombre)
        zs = [struct.unpack_from('<f', nif['datos'], off + OFF_VERTICES + STRIDE * k + 8)[0]
              for k in range(nv)]
        return min(zs), max(zs)
    raise SystemExit('no encontre la malla %s' % nombre)


def record_subrecords(path, fid):
    p = Plugin(str(path))
    for t, o, n, d in p.recorrer():
        if t == 'GRUP':
            continue
        if p.form_id(o) == fid:
            return t, dict(p.subrecords(p.datos(o)))
    return '<ausente>', {}


def main():
    if not (NIF_ALTO.exists() and NIF_BAJO.exists()):
        print('FAIL faltan los NIF:', NIF_ALTO, NIF_BAJO)
        return 1
    cfg = json.loads((ROOT / 'config.json').read_text())
    gcfg = cfg.get('guardia') or {}

    print('== 1) los dos NIF tienen la MISMA estructura ==')
    alto = nif_nodos.leer(str(NIF_ALTO))
    bajo = nif_nodos.leer(str(NIF_BAJO))
    check(alto['n_bloques'] == bajo['n_bloques'],
          f'misma cantidad de bloques: {alto["n_bloques"]} vs {bajo["n_bloques"]}')
    pos_a, _ = nif_nodos.mundo(alto)
    pos_b, _ = nif_nodos.mundo(bajo)
    check(set(pos_a) == set(pos_b),
          f'mismos nombres de nodo ({len(pos_a)})' +
          ('' if set(pos_a) == set(pos_b) else
           f' solo-alto={sorted(set(pos_a) - set(pos_b))} solo-bajo={sorted(set(pos_b) - set(pos_a))}'))

    print('== 2) los nodos del cabezal bajan DELTA exactos ==')
    for nombre in BAJAN:
        if nombre not in pos_a or nombre not in pos_b:
            check(False, f'{nombre} presente en los dos NIF')
            continue
        d = pos_a[nombre][2] - pos_b[nombre][2]
        check(cerca(d, DELTA), f'{nombre}: z {pos_a[nombre][2]:.3f} -> {pos_b[nombre][2]:.3f} (baja {d:.3f})')
    print('== 3) la raiz y el operador NO se mueven ==')
    for nombre in QUIETOS:
        if nombre not in pos_a or nombre not in pos_b:
            check(False, f'{nombre} presente en los dos NIF')
            continue
        d = abs(pos_a[nombre][2] - pos_b[nombre][2])
        check(cerca(d, 0.0), f'{nombre}: z {pos_a[nombre][2]:.3f} -> {pos_b[nombre][2]:.3f} (delta {d:.3f})')

    print('== 4) pivote y muzzle coinciden con el ESP y el config ==')
    # El NIF alto es el que corre la mira del jugador: su pivote es la constante que el
    # VMAD `AstraAsedioActi.PitchPivotHeight` le pasa a `AstraSightNative`.
    check(cerca(pos_a['CTRL_ELEVACION'][2], PIVOTE_ALTO),
          f'NIF alto CTRL_ELEVACION z = {pos_a["CTRL_ELEVACION"][2]:.3f} == {PIVOTE_ALTO}')
    check(cerca(pos_b['CTRL_ELEVACION'][2], PIVOTE_BAJO),
          f'NIF bajo CTRL_ELEVACION z = {pos_b["CTRL_ELEVACION"][2]:.3f} == {PIVOTE_BAJO}')
    check(cerca(pos_a['ProjectileNode'][2], MUZZLE_ALTO),
          f'NIF alto ProjectileNode z = {pos_a["ProjectileNode"][2]:.3f} == {MUZZLE_ALTO}')
    check(cerca(pos_b['ProjectileNode'][2], MUZZLE_BAJO),
          f'NIF bajo ProjectileNode z = {pos_b["ProjectileNode"][2]:.3f} == {MUZZLE_BAJO}')
    check(cerca(cfg['pitch_pivot_units'], pos_a['CTRL_ELEVACION'][2]),
          f'config.pitch_pivot_units = {cfg["pitch_pivot_units"]} == pivote del NIF alto')
    check(cerca(gcfg.get('muzzle_alto', 0.0), pos_a['ProjectileNode'][2], 1e-4),
          f'guardia.muzzle_alto = {gcfg.get("muzzle_alto")} == muzzle del NIF alto')
    # El VMAD del ACTI del jugador tiene que llevar el pivote alto, no el bajo.
    t, ss = record_subrecords(CORE, B.IDS['ballesta'])
    vm = B.read_vmad(ss['VMAD'])['scripts'][0]['properties']
    check(cerca(vm['PitchPivotHeight']['value'], pos_a['CTRL_ELEVACION'][2], 1e-4),
          f'VMAD AstraAsedioActi.PitchPivotHeight = {vm["PitchPivotHeight"]["value"]} == pivote alto')

    print('== 5) el pedestal: la base quieta y el tope por afinidad ==')
    # El pedestal no cuelga del cabezal, asi que se aplasta en Z: z' = Z0 + (z-Z0)*K para
    # z > Z0, con K = 1 - DELTA/(TOPE-Z0). Solo el elemento mas alto (el poste, TOPE) baja
    # DELTA exactos; los demas bajan menos, y por eso no alcanza con comparar contra DELTA.
    K = 1.0 - DELTA / (TOPE - Z0)
    for nombre in PEDESTAL:
        z0a, z1a = bbox_z_malla(alto, nombre)
        z0b, z1b = bbox_z_malla(bajo, nombre)
        check(cerca(z0a, z0b, 1e-6),
              f'{nombre}: base z {z0a:.4f} -> {z0b:.4f} (no se mueve)')
        check(cerca(z1b, Z0 + (z1a - Z0) * K),
              f'{nombre}: tope z {z1a:.4f} -> {z1b:.4f} (afinidad K={K:.6f})')
    # El mas alto es el que define TOPE: tiene que bajar DELTA exactos.
    z0w, z1w = bbox_z_malla(alto, PEDESTAL[-1])
    z0wb, z1wb = bbox_z_malla(bajo, PEDESTAL[-1])
    check(cerca(z1w, TOPE, 0.01), f'{PEDESTAL[-1]} define TOPE ({z1w:.4f} == {TOPE})')
    check(cerca(z1w - z1wb, DELTA), f'{PEDESTAL[-1]}: tope baja {z1w - z1wb:.4f} == DELTA')

    print('== 6) cada ACTI apunta al NIF que le toca ==')
    for fid, nombre, modelo in ((B.IDS['ballesta'], 'jugador', 'ballesta.nif'),
                                (0x03000B02, 'tombstones deshabilitados', 'ballesta.nif'),
                                (0x03000B04, 'guardia (voladizos + Carrera Blanca)', 'ballesta_guardia.nif')):
        _, ss = record_subrecords(CORE, fid)
        modl = ss.get('MODL', b'').rstrip(b'\0').decode('cp1252', 'replace')
        check(modl == 'AstraAsedio\\' + modelo, f'ACTI {fid:08X} ({nombre}) MODL -> {modelo}')

    rep = {'revision': 22, 'delta_units': DELTA,
           'nif_alto': {'path': str(NIF_ALTO.relative_to(ROOT)), 'pivote_z': pos_a['CTRL_ELEVACION'][2],
                        'muzzle_z': pos_a['ProjectileNode'][2], 'nodos': len(pos_a)},
           'nif_bajo': {'path': str(NIF_BAJO.relative_to(ROOT)), 'pivote_z': pos_b['CTRL_ELEVACION'][2],
                        'muzzle_z': pos_b['ProjectileNode'][2], 'nodos': len(pos_b)},
           'usa_alto': {'ACTI_03000801': 'jugador (core + Atalaya)',
                        'ACTI_03000B02': 'voladizos de WhiterunTorres (AstraAsedioStation, mira nativa)'},
           'usa_bajo': {'ACTI_03000B04': 'torreta guardia-exclusiva de Carrera Blanca (04000B10)'},
           'ok': not fails, 'fails': fails}
    (ROOT / 'reports/torreta_baja_v22.json').write_text(json.dumps(rep, ensure_ascii=False, indent=2))

    print()
    if fails:
        print(f'FALLARON {len(fails)} verificaciones')
        return 1
    print('TORRETA_BAJA_V22 OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
