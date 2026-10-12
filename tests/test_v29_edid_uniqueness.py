"""Los plugins empaquetados no pueden repetir un EDID.

Sembrado por la colisión de v17: el addon de los voladizos conserva el juego
legacy (0xB40-0xB54, copiado de la baseline v16) junto al juego vigente
(0xB70-0xB84), y ambos nacieron con el mismo literal `AstraVoladizo*`. No es un
fallo funcional -- el legacy nace con `Initially Disabled` (0x800) y el runtime
solo conoce el par 0xB70/0xB80 -- pero ensucia el `Check for Errors` de xEdit, que
sigue pendiente en `docs/nexus/RELEASE_STATUS.md`.

Ademas fija el contrato que hace segura esa convivencia: el legacy sigue
deshabilitado y persistente sobre su propia base (AstraAsedio.esp 0x0B02) y el
vigente sigue habilitado sobre la base baja 0x0B04.
"""
from pathlib import Path
import struct
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]
from parser_esm import Plugin

PLUGINS = ['mod/AstraAsedio.esp',
           'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp',
           'addons/Whiterun/AstraAsedio_Whiterun.esp',
           'addons/Atalaya/AstraAsedio_Atalaya.esp',
           'addons/GuardAnim/AstraAsedio_GuardAnim.esp']
LEGACY = list(range(0x04000B40, 0x04000B45)) + list(range(0x04000B50, 0x04000B55))
CURRENT = list(range(0x04000B70, 0x04000B75)) + list(range(0x04000B80, 0x04000B85))
LEGACY_NAMES = ['AstraLegacyVoladizoEsteBallesta', 'AstraLegacyVoladizoEsteGuardia',
                'AstraLegacyVoladizoEstePuesto', 'AstraLegacyVoladizoEsteEspera',
                'AstraLegacyVoladizoEstePlataforma', 'AstraLegacyVoladizoOesteBallesta',
                'AstraLegacyVoladizoOesteGuardia', 'AstraLegacyVoladizoOestePuesto',
                'AstraLegacyVoladizoOesteEspera', 'AstraLegacyVoladizoOestePlataforma']
CURRENT_NAMES = ['AstraVoladizoEsteBallesta', 'AstraVoladizoEsteGuardia',
                 'AstraVoladizoEstePuesto', 'AstraVoladizoEsteEspera',
                 'AstraVoladizoEstePlataforma', 'AstraVoladizoOesteBallesta',
                 'AstraVoladizoOesteGuardia', 'AstraVoladizoOestePuesto',
                 'AstraVoladizoOesteEspera', 'AstraVoladizoOestePlataforma']
CITY = 'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp'


def opened(path):
    plugin = Plugin(str(ROOT/path))
    found = {plugin.form_id(off): off for typ, off, _n, _depth in plugin.recorrer()
             if typ not in ('GRUP', 'TES4')}
    return plugin, found


def sub(plugin, off, key):
    return dict(plugin.subrecords(plugin.datos(off))).get(key, b'')


def edid(plugin, off):
    return sub(plugin, off, 'EDID').rstrip(b'\0').decode()


class EdidUniqueness(unittest.TestCase):
    def test_no_plugin_repeats_an_edid(self):
        """Un EDID duplicado confunde a xEdit/CK y no aporta nada."""
        for name in PLUGINS:
            if not (ROOT/name).exists():
                continue
            plugin, found = opened(name)
            seen = {}
            for fid, off in found.items():
                key = edid(plugin, off)
                if not key:
                    continue
                if key in seen:
                    self.fail(f'{name}: EDID repetido {key} en {fid:08X} y {seen[key]:08X}')
                seen[key] = fid

    def test_legacy_and_current_games_use_distinct_names(self):
        plugin, found = opened(CITY)
        for fid, expected in zip(LEGACY, LEGACY_NAMES):
            self.assertEqual(edid(plugin, found[fid]), expected, f'{fid:08X}')
        for fid, expected in zip(CURRENT, CURRENT_NAMES):
            self.assertEqual(edid(plugin, found[fid]), expected, f'{fid:08X}')

    def test_legacy_game_stays_disabled_persistent_and_on_its_own_base(self):
        """Si esto cambia, cambia el contrato con las partidas anteriores a v17.

        Por cada voladizo: ballesta, guardia, puesto, espera y plataforma; las
        columnas son base de la ballesta, NPC, marcador y STAT de ese lado.
        """
        plugin, found = opened(CITY)
        sides = [('Este', 0x04000B00, 0x04000B60), ('Oeste', 0x04000B01, 0x04000B61)]
        for index, (side, npc, platform) in enumerate(sides):
            legacy_start = 0x04000B40 + 16*index
            current_start = 0x04000B70 + 16*index
            expected_legacy = [0x03000B02, npc, 0x34, 0x34, platform]
            expected_current = [0x03000B04, npc, 0x34, 0x34, platform]
            for offset in range(5):
                old, new = legacy_start + offset, current_start + offset
                self.assertEqual(sub(plugin, found[old], 'EDID').rstrip(b'\0').decode(),
                                 LEGACY_NAMES[index*5 + offset], f'{side} {old:08X}')
                self.assertNotEqual(old, new)
                self.assertEqual(
                    struct.unpack('<I', sub(plugin, found[old], 'NAME'))[0],
                    expected_legacy[offset], f'{side} legacy {old:08X}')
                self.assertEqual(
                    struct.unpack('<I', sub(plugin, found[new], 'NAME'))[0],
                    expected_current[offset], f'{side} vigente {new:08X}')
                old_flags = struct.unpack_from('<I', plugin.d, found[old] + 8)[0]
                new_flags = struct.unpack_from('<I', plugin.d, found[new] + 8)[0]
                self.assertTrue(old_flags & 0x800, f'{old:08X} debe nacer Initially Disabled')
                self.assertTrue(old_flags & 0x400, f'{old:08X} debe ser persistente (ref guardada)')
                self.assertFalse(new_flags & 0x800,
                                 f'{new:08X} es el puesto vigente, no puede nacer apagado')


if __name__ == '__main__':
    unittest.main()
