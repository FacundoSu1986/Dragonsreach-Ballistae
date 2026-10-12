"""v29: dar EDID propio al juego legacy de los voladizos de Carrera Blanca.

El addon de los voladizos conserva, junto al puesto de guardia vigente
(0xB70-0xB84, base `AstraAsedio.esp:0x0B04`), el juego legacy de v13/v17
(0xB40-0xB54, base `0x0B02`) que nace con el flag `Initially Disabled` (0x800) y
solo existe para desactivar en partidas anteriores a v17. Los dos juegos se
crearon con el mismo literal `AstraVoladizo*`, asi que el plugin repite diez EDID.
No es un fallo funcional -- FormID, bases, VMAD, flags y colocacion no cambian --
pero ensucia el `Check for Errors` de xEdit, que sigue pendiente en
`docs/nexus/RELEASE_STATUS.md`.

Este script reescribe SOLO el subrecord EDID de esos diez refs y verifica que
nada mas cambia. `scripts/build_modular_v17.py` aplica el mismo renombrado al
copiar el legacy, para que una regeneracion produzca este mismo archivo.

Uso: python scripts/patch_legacy_edids_v29.py
"""
import hashlib
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import escritor_plugin as W
import patch_plugin_v12 as P

CITY = ROOT/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp'
REPORT = ROOT/'reports/legacy_edid_rename_v29.json'
# El puesto vigente 0xB70/0xB80 conserva su nombre: es el que citan los scripts,
# el runtime nativo y la documentacion vigente.
SIDES = [('Este', 0x04000B40), ('Oeste', 0x04000B50)]
PARTS = ['Ballesta', 'Guardia', 'Puesto', 'Espera', 'Plataforma']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rebuild(path, changes):
    """Reescribe el plugin aplicando `changes` (FormID -> bytes del registro)."""
    p = Plugin(path)
    groups = []
    cursor = p.inicio_datos
    while cursor < len(p.d):
        size = struct.unpack_from('<I', p.d, cursor+4)[0]
        groups.append(P.transform_groups(p.d[cursor:cursor+size], changes, set(), {}))
        cursor += size
    assert cursor == len(p.d)
    path.write_bytes(p.d[:p.inicio_datos] + b''.join(groups))
    check = Plugin(path)
    for typ, off, n, depth in check.recorrer():
        if typ != 'GRUP':
            check.subrecords(check.datos(off))


def main():
    before = Plugin(CITY)
    before_bytes = CITY.read_bytes()
    before_sha = sha(CITY)
    before_map = P.record_map(before)
    before_order = [before.form_id(off) for typ, off, n, d in before.recorrer() if typ != 'GRUP']

    renames, changes, expected = {}, {}, {}
    for side, start in SIDES:
        for offset, part in enumerate(PARTS):
            fid = start+offset
            new = f'AstraLegacyVoladizo{side}{part}'
            old = dict(Plugin.subrecords(before_map[fid][24:]))['EDID'].rstrip(b'\0').decode()
            assert old == f'AstraVoladizo{side}{part}', (hex(fid), old)
            assert new not in renames.values(), new
            renames[f'{fid:08X}'] = {'old': old, 'new': new}
            expected[fid] = new
            changes[fid] = P.modify_subs(before_map[fid], {'EDID': W.zstr(new)})

    rebuild(CITY, changes)

    after = Plugin(CITY)
    after_map = P.record_map(after)
    after_order = [after.form_id(off) for typ, off, n, d in after.recorrer() if typ != 'GRUP']

    # 1. Mismo conjunto y mismo orden de registros; cabecera TES4 intacta.
    assert set(after_map) == set(before_map), 'cambio el conjunto de FormID'
    assert after_order == before_order, 'cambio el orden de los registros'
    assert after.d[:24] == before_bytes[:24], 'cambio la cabecera del registro TES4'
    assert after.d[24:24+struct.unpack_from('<I', before_bytes, 4)[0]] == \
        before_bytes[24:24+struct.unpack_from('<I', before_bytes, 4)[0]], 'cambio el cuerpo del TES4'

    # 2. Solo cambian los diez EDID; en cada uno, solo ese subrecord.
    changed = sorted(fid for fid, raw in after_map.items() if raw != before_map[fid])
    assert changed == sorted(expected), [f'{f:X}' for f in changed]
    for fid in expected:
        old_raw, new_raw = before_map[fid], after_map[fid]
        assert old_raw[:4] == new_raw[:4] and old_raw[8:16] == new_raw[8:16], \
            f'{fid:X} cambio firma, flags o FormID'
        old_subs = list(Plugin.subrecords(old_raw[24:]))
        new_subs = list(Plugin.subrecords(new_raw[24:]))
        assert [k for k, v in old_subs] == [k for k, v in new_subs], f'{fid:X} cambiaron subrecords'
        for (k, v), (k2, v2) in zip(old_subs, new_subs):
            if k == 'EDID':
                assert v.rstrip(b'\0').decode() == renames[f'{fid:08X}']['old']
                assert v2.rstrip(b'\0').decode() == expected[fid]
            else:
                assert (k, v) == (k2, v2), f'{fid:X} cambio {k}'

    # 3. Ningun EDID repetido en el plugin completo.
    seen = {}
    for typ, off, n, depth in after.recorrer():
        if typ in ('GRUP', 'TES4'):
            continue
        key = dict(after.subrecords(after.datos(off))).get('EDID', b'').rstrip(b'\0').decode()
        if not key:
            continue
        assert key not in seen, f'EDID repetido {key}: {seen[key]:08X} y {after.form_id(off):08X}'
        seen[key] = after.form_id(off)

    # 4. El legacy conserva su contrato de convivencia: persistente y apagado
    #    sobre la base 0x0B02; el puesto vigente sigue despierto sobre 0x0B04.
    for side, start in SIDES:
        for offset in range(5):
            old, new = start+offset, start+0x30+offset
            old_off = next(o for t, o, n, d in after.recorrer()
                           if t != 'GRUP' and after.form_id(o) == old)
            new_off = next(o for t, o, n, d in after.recorrer()
                           if t != 'GRUP' and after.form_id(o) == new)
            old_flags = struct.unpack_from('<I', after.d, old_off+8)[0]
            new_flags = struct.unpack_from('<I', after.d, new_off+8)[0]
            assert old_flags & 0x400 and old_flags & 0x800, f'{old:08X} debe nacer persistente y apagado'
            assert not new_flags & 0x800, f'{new:08X} es el puesto vigente'

    header_count = len([1 for typ, off, n, d in after.recorrer() if typ != 'GRUP'])
    report = {'revision': 29, 'success': True, 'game_tested': False,
              'plugin': str(CITY.relative_to(ROOT)),
              'before_sha256': before_sha, 'after_sha256': sha(CITY),
              'records': header_count, 'renames': renames,
              'verified': ['conjunto y orden de FormID', 'subrecords identicos salvo EDID',
                           'firma, flags y FormID por registro', 'cabecera TES4 y conteo',
                           'EDID unico en todo el plugin',
                           'legacy persistente+apagado en 0x0B02, vigente en 0x0B04'],
              'why': 'el juego legacy 0xB40-0xB54 comparte celda con el puesto vigente '
                     '0xB70-0xB84 y repetia sus EDID',
              'zip_rebuild_required': True}
    REPORT.write_text(json.dumps(report, indent=2)+'\n')
    print('LEGACY_EDIDS_RENAMED', header_count, 'records', before_sha[:12], '->', sha(CITY)[:12])


if __name__ == '__main__':
    main()
