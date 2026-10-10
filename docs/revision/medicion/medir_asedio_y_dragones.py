# -*- coding: utf-8 -*-
"""Solo lectura. Como hace dano un virote de asedio vanilla y que defensas tiene un dragon.

    python -B docs/revision/medicion/medir_asedio_y_dragones.py

Vuelca, de los ESM del `runtime` de config.json:
  - la explosion (EXPL) de los proyectiles de asedio vanilla y del virote de
    fuego DLC1: fuerza, dano, radio (DATA+24) y encantamiento (EITM);
  - piel (WNAM -> ARMO, armadura = DNAM/100) y habilidades (SPLO) de DragonRace
    y de tres dragones de encuentro, con los efectos de cada habilidad;
  - los sonidos de disparo (SNAM/XNAM/TNAM) de ballestas y armas de asedio y
    el sonido de vuelo (DATA+40) de sus proyectiles;
  - FURN e IDLE con "Ballista" en el EDID (para saber si existe una animacion
    vanilla de operador humano).
"""
import json
import struct
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts' / 'vendor'))
from parser_esm import Plugin  # noqa: E402

DATA = Path(json.loads((ROOT / 'config.json').read_text())['runtime']) / 'Data'
ARCHIVOS = ['Skyrim.esm', 'Dawnguard.esm', 'Dragonborn.esm']
TIPOS = ('PROJ', 'EXPL', 'ENCH', 'RACE', 'ARMO', 'SPEL', 'SHOU', 'MGEF', 'NPC_', 'WEAP', 'SNDR', 'FURN', 'IDLE')
PROYECTILES = ('TrapDweBallistaBolt', 'CWCatapultProjectile', 'DLC1BoltSteelProjectileFire',
               'DLC2ArrowDwarvenBallistaBoltProjectile', 'DLC1BoltSteelProjectile')
ARMAS = ('DLC1CrossBow', 'DLC1DwarvenCrossBow', 'DLC1TrapCrossbowWeapon01', 'TrapDweBallistaWeaponL01',
         'DLC2crDwarvenBallistaBow01', 'CWCatapultWeapon')
DRAGONES = ('EncDragon01Fire', 'EncDragon05Fire', 'DLC1EncDragon07Fire')


def cargar():
    recs = {}
    for f in ARCHIVOS:
        p = Plugin(str(DATA / f))
        for t, o, _n, _p in p.recorrer():
            if t not in TIPOS:
                continue
            ss = p.subrecords(p.datos(o))
            sd = {}
            for k, v in ss:
                sd.setdefault(k, v)
            ed = sd.get('EDID', b'').rstrip(b'\0').decode('cp1252', 'replace')
            recs[(f, p.form_id(o))] = (t, sd, ss, ed)
    return recs


def buscar(recs, fid, archivo):
    """(archivo, record) de una referencia hecha desde `archivo`."""
    candidatos = [(f, x) for (f, x) in recs if x & 0xFFFFFF == fid & 0xFFFFFF]
    if fid >> 24 == 0:
        candidatos = [c for c in candidatos if c[0] == 'Skyrim.esm' and c[1] >> 24 == 0] or candidatos
    else:
        candidatos = [c for c in candidatos if c[0] == archivo] or candidatos
    return (candidatos[0][0], recs[candidatos[0]]) if candidatos else (None, None)


def edid(recs, fid, archivo):
    _f, r = buscar(recs, fid, archivo)
    return r[3] if r else '%08X' % fid


def efectos(recs, archivo, ss):
    """[(MGEF, magnitud)] de un SPEL/ENCH: pares EFID + EFIT."""
    fuera, actual = [], None
    for k, v in ss:
        if k == 'EFID':
            actual, = struct.unpack('<I', v)
        elif k == 'EFIT' and actual is not None:
            fuera.append((edid(recs, actual, archivo), round(struct.unpack_from('<f', v)[0], 1)))
    return fuera


def habilidad(recs, fid, archivo):
    """'TIPO EDID efectos=[...]' de un SPLO (SPEL o SHOU); los gritos no tienen EFID propio."""
    fs, sp = buscar(recs, fid, archivo)
    if sp is None:
        return '%08X (no esta en los ESM leidos)' % fid
    return '%s %-34s efectos=%s' % (sp[0], sp[3], efectos(recs, fs, sp[2]))


def main():
    recs = cargar()
    orden = sorted(recs.items(), key=lambda kv: (kv[1][3].lower(), kv[0][0]))

    print('== Proyectiles de asedio vanilla y su explosion')
    for (f, _fid), (t, sd, _ss, ed) in orden:
        if t != 'PROJ' or not ed.startswith(PROYECTILES):
            continue
        dd = sd['DATA']
        _fl, tipo, grav, vel = struct.unpack_from('<HHff', dd)
        expl, sonido = struct.unpack_from('<II', dd, 36)
        impacto, = struct.unpack_from('<f', dd, 52)
        linea = '%-14s %-40s tipo=0x%02X grav=%.2f vel=%.0f impacto=%.1f vuelo=%s' % (
            f, ed, tipo, grav, vel, impacto, edid(recs, sonido, f) if sonido else '-')
        if expl:
            fe, r = buscar(recs, expl, f)
            ed_ = r[1].get('DATA', b'')
            fuerza, dano, radio = struct.unpack_from('<3f', ed_, 24)
            ench = ' EITM=%s' % edid(recs, struct.unpack('<I', r[1]['EITM'])[0], fe) if 'EITM' in r[1] else ''
            linea += '\n%57s-> EXPL %s fuerza=%.0f dano=%.0f radio=%.0f%s' % ('', r[3], fuerza, dano, radio, ench)
        print(linea)

    print('\n== DragonRace: piel y habilidades')
    for (f, _fid), (t, sd, ss, ed) in orden:
        if t != 'RACE' or ed != 'DragonRace' or f != 'Skyrim.esm':
            continue
        fp, piel = buscar(recs, struct.unpack('<I', sd['WNAM'])[0], f)
        print('%s %s piel=%s armadura=%.1f' % (f, ed, piel[3], struct.unpack_from('<i', piel[1]['DNAM'])[0] / 100.0))
        for k, v in ss:
            if k == 'SPLO':
                print('   SPLO %s' % habilidad(recs, struct.unpack('<I', v)[0], f))

    print('\n== Dragones de encuentro: piel propia y habilidades')
    for (f, _fid), (t, sd, ss, ed) in orden:
        if t != 'NPC_' or ed not in DRAGONES:
            continue
        piel = 'de la raza'
        if 'WNAM' in sd:
            fid_piel, = struct.unpack('<I', sd['WNAM'])
            _fp, r = buscar(recs, fid_piel, f)
            piel = ('%s armadura=%.1f' % (r[3], struct.unpack_from('<i', r[1]['DNAM'])[0] / 100.0)
                    if r else '%08X (no esta en los ESM leidos)' % fid_piel)
        print('%-14s %-22s piel=%s' % (f, ed, piel))
        for k, v in ss:
            if k == 'SPLO':
                print('   SPLO %s' % habilidad(recs, struct.unpack('<I', v)[0], f))

    print('\n== Sonidos de disparo de ballestas y armas de asedio')
    for (f, _fid), (t, sd, _ss, ed) in orden:
        if t == 'WEAP' and ed in ARMAS:
            sonidos = {k: edid(recs, struct.unpack('<I', sd[k])[0], f) for k in ('SNAM', 'XNAM', 'TNAM') if k in sd}
            print('%-14s %-28s %s' % (f, ed, sonidos or 'sin sonidos'))

    print('\n== FURN e IDLE con "Ballista" en el EDID')
    for (f, _fid), (t, sd, _ss, ed) in orden:
        if t in ('FURN', 'IDLE') and 'ballista' in ed.lower():
            extra = sd.get('MODL', sd.get('DNAM', b'')).rstrip(b'\0').decode('cp1252', 'replace')
            print('%-14s %s %-34s %s' % (f, t, ed, extra))
    return 0


if __name__ == '__main__':
    sys.exit(main())
