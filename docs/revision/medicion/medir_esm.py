# -*- coding: utf-8 -*-
"""Solo lectura. Tabla vanilla de balistica, dano y salud de dragones.

    python -B docs/revision/medicion/medir_esm.py

Lee Skyrim.esm, Dawnguard.esm y Dragonborn.esm del `runtime` de config.json
con scripts/vendor/parser_esm.py y vuelca:
  - PROJ de tipo Arrow o de asedio (Ballista/Catapult): gravedad, velocidad,
    alcance, fuerza de impacto, radio de colision, flags, modelo;
  - AMMO: dano, flags (0x2 no jugable, 0x4 flecha), proyectil;
  - WEAP base (sin CNAM) de ballesta o de trampa/asedio: dano, velocidad;
  - GMST de flechas, proyectiles y gravedad;
  - RACE de dragon (salud inicial en DATA+36) y NordRace como control (50);
  - NPC_ de razas de dragon: nivel, offset de salud, autocalculo.
Layouts: DATA de PROJ de 92 bytes (flags u16, tipo u16, gravedad, velocidad,
alcance, ..., explosion +36, sonido +40, impacto +52, radio +72), DATA de AMMO
(proyectil, flags, dano), ACBS de NPC_ de 24 bytes.
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
TIPOS = ('PROJ', 'AMMO', 'WEAP', 'GMST', 'RACE', 'NPC_')
FLAGS_PROJ = {0x1: 'Hitscan', 0x2: 'Explosion', 0x4: 'AltTrigger', 0x8: 'MuzzleFlash', 0x20: 'CanBeDisabled',
              0x40: 'CanBePickedUp', 0x80: 'Supersonic', 0x100: 'PinsLimbs', 0x200: 'PassSmallTransp',
              0x400: 'NoCombatAimCorr'}


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
            recs[(f, p.form_id(o))] = (t, sd, ed)
    return recs


def nombre(recs, fid):
    """EDID de una referencia. Indice de master 0 = Skyrim.esm."""
    candidatos = [(f, x, r) for (f, x), r in recs.items() if x & 0xFFFFFF == fid & 0xFFFFFF]
    if fid >> 24 == 0:
        candidatos = [c for c in candidatos if c[0] == 'Skyrim.esm' and c[1] >> 24 == 0] or candidatos
    return candidatos[0][2][2] if candidatos else '%08X' % fid


def main():
    recs = cargar()
    orden = sorted(recs.items(), key=lambda kv: (kv[1][2].lower(), kv[0][0]))

    print('== PROJ tipo Arrow o de asedio')
    for (f, _fid), (t, sd, ed) in orden:
        if t != 'PROJ' or 'DATA' not in sd:
            continue
        fl, tipo, grav, vel, alc = struct.unpack_from('<HHfff', sd['DATA'])
        if tipo != 0x40 and not any(k in ed.lower() for k in ('ballista', 'catapult')):
            continue
        impacto, = struct.unpack_from('<f', sd['DATA'], 52)
        radio, = struct.unpack_from('<f', sd['DATA'], 72)
        modelo = sd.get('MODL', b'').rstrip(b'\0').decode('cp1252', 'replace')
        print('%-14s %-40s tipo=0x%02X grav=%.2f vel=%7.0f alcance=%6.0f impacto=%5.1f radio=%.1f flags=%s modelo=%s'
              % (f, ed, tipo, grav, vel, alc, impacto, radio, '|'.join(v for k, v in FLAGS_PROJ.items() if fl & k), modelo))

    print('\n== AMMO')
    for (f, _fid), (t, sd, ed) in orden:
        if t != 'AMMO' or 'DATA' not in sd:
            continue
        proj, fl, dano = struct.unpack_from('<IIf', sd['DATA'])
        print('%-14s %-34s dano=%5.1f flags=0x%X (%s%s) proyectil=%s'
              % (f, ed, dano, fl, 'flecha' if fl & 4 else 'virote', ', no jugable' if fl & 2 else '', nombre(recs, proj)))

    print('\n== WEAP base (sin CNAM): ballestas y armas de trampa/asedio')
    for (f, _fid), (t, sd, ed) in orden:
        if t != 'WEAP' or 'CNAM' in sd or len(sd.get('DATA', b'')) != 10 or len(sd.get('DNAM', b'')) != 100:
            continue
        anim = sd['DNAM'][0]
        if anim != 9 and not any(k in ed.lower() for k in ('trap', 'ballista', 'catapult')):
            continue
        _valor, peso, dano = struct.unpack('<IfH', sd['DATA'])
        vel, = struct.unpack_from('<f', sd['DNAM'], 4)
        tambaleo, = struct.unpack_from('<f', sd['DNAM'], 96)
        print('%-14s %-34s anim=%d dano=%3d velocidad=%.3f peso=%.1f stagger=%.2f' % (f, ed, anim, dano, vel, peso, tambaleo))

    print('\n== GMST de flechas, proyectiles y gravedad')
    for (f, _fid), (t, sd, ed) in orden:
        if t != 'GMST' or not any(k in ed.lower() for k in ('arrow', 'bolt', 'projectile', 'gravity', 'crossbow')):
            continue
        v = sd.get('DATA', b'')
        if ed[:1] == 'f' and len(v) >= 4:
            valor = '%.4f' % struct.unpack_from('<f', v)[0]
        elif ed[:1] in 'iub' and len(v) >= 4:
            valor = str(struct.unpack_from('<i', v)[0])
        else:
            valor = '(cadena localizada %s)' % v.hex()
        print('%-14s %-40s %s' % (f, ed, valor))

    print('\n== RACE de dragon (salud inicial = DATA+36) y NordRace de control')
    razas = {}
    for (f, fid), (t, sd, ed) in orden:
        if t == 'RACE' and ('dragon' in ed.lower() or ed == 'NordRace') and 'DATA' in sd:
            razas[fid & 0xFFFFFF] = ed
            print('%-14s %-30s %08X salud inicial=%.0f' % (f, ed, fid, struct.unpack_from('<f', sd['DATA'], 36)[0]))

    print('\n== NPC_ de razas de dragon (sin sacerdotes): ACBS')
    dragon = {k for k, v in razas.items() if 'dragon' in v.lower() and 'priest' not in v.lower()}
    for (f, _fid), (t, sd, ed) in orden:
        if t != 'NPC_' or 'RNAM' not in sd or 'ACBS' not in sd:
            continue
        raza, = struct.unpack('<I', sd['RNAM'])
        if raza & 0xFFFFFF not in dragon:
            continue
        fl, _m, _s, nivel, _cmin, _cmax, _vel, _disp, _tpl, offset, _bo = struct.unpack_from('<IhhhHHHhHhH', sd['ACBS'])
        nivel_txt = 'x%.2f' % (nivel / 1000.0) if fl & 0x80 else str(nivel)
        print('%-14s %-40s raza=%-22s nivel=%-5s offsetSalud=%5d autocalculo=%s'
              % (f, ed, razas.get(raza & 0xFFFFFF, '?'), nivel_txt, offset, bool(fl & 0x10)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
