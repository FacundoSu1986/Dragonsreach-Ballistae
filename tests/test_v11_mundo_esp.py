"""Colocacion de la torre en el mundo: override de la celda vanilla 0000963D en el ESP.

Reemplaza el camino de parchear Skyrim.esm. Lo que se fija aca son los defectos medidos de
ese camino, enumerando la FAMILIA (todos los REFR, todos los GRUP de nivel superior, todas
las celdas), no el caso que se vio:

  - un REFR cuyo NAME apunta a un FormID que no existe en el archivo que lo resuelve;
  - una celda exterior que repite el grid de otra;
  - DATA del REFR mal armado (3 float de posicion + 3 float de rotacion, radianes);
  - objetos del laboratorio interior (losas de piso, luces, blancos) en la tundra.
"""
import collections
import json
import math
import struct
import unittest

import _mundo_helpers as H
from parser_esm import Plugin

REFR_AL_MUNDO = 72
LABORATORIO = ('ArcheryTarget', 'ArcheryTargetTripod', 'XMarkerHeading', 'WRIntFloorSTMid01Large')


def zstr(b):
    return b.rstrip(b'\0').decode('cp1252', 'replace')


class Estructura(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.p = Plugin(str(H.ESP))
        cls.d = cls.p.d
        cls.items = list(cls.p.recorrer())            # lanza si el archivo no embaldosa
        cls.registros = {}
        for t, o, _n, pr in cls.items:
            if t != 'GRUP':
                cls.registros.setdefault(cls.p.form_id(o), []).append((t, o, pr))

    def test_el_recorrido_embaldosa_el_archivo(self):
        self.assertGreater(len(self.items), 200)

    def test_un_solo_grup_de_nivel_superior_por_tipo(self):
        """El defecto de los escudos era un segundo GRUP STAT al final; vale para cualquier tipo."""
        etiquetas = [self.d[o + 8:o + 12] for t, o, _n, pr in self.items if t == 'GRUP' and pr == 0]
        dup = [k for k, v in collections.Counter(etiquetas).items() if v > 1]
        self.assertEqual(dup, [], 'GRUP de nivel superior repetidos: %s' % dup)

    def test_hedr_numrecords_y_next_object_id(self):
        hedr = [v for k, v in Plugin.subrecords(self.p.datos(0)) if k == 'HEDR'][0]
        _version, n, siguiente = struct.unpack('<fiI', hedr)
        self.assertEqual(n, len(self.items) - 1)                 # sin el TES4
        propios = [f & 0xFFFFFF for f in self.registros if f >> 24 == 3]
        self.assertGreater(siguiente, max(propios))

    def test_registros_nuevos_en_version_44_y_sin_comprimir(self):
        for fid, lista in self.registros.items():
            for t, o, _pr in lista:
                self.assertEqual(struct.unpack_from('<H', self.d, o + 20)[0], 44, '%s %08X' % (t, fid))
                if t in ('WRLD', 'CELL', 'LAND', 'REFR'):
                    self.assertFalse(struct.unpack_from('<I', self.d, o + 8)[0] & H.COMPRIMIDO,
                                     '%s %08X' % (t, fid))

    def test_hay_exactamente_un_wrld_tamriel_sin_ofst_ni_rnam(self):
        wrld = [(f, o) for f, v in self.registros.items() for t, o, _ in v if t == 'WRLD']
        self.assertEqual([f for f, _ in wrld], [0x3C])
        claves = [k for k, _ in Plugin.subrecords(self.p.datos(wrld[0][1]))]
        self.assertNotIn('OFST', claves)
        self.assertNotIn('RNAM', claves)
        self.assertEqual(claves[0], 'EDID')

    @unittest.skipUnless(H.HAY_JUEGO, 'hace falta el runtime de Skyrim del config')
    def test_wrld_es_la_version_ganadora_de_los_masters_salvo_el_nombre(self):
        o = [o for f, v in self.registros.items() for t, o, _ in v if t == 'WRLD'][0]
        mio = [(k, v) for k, v in Plugin.subrecords(self.p.datos(o))]
        dg = H.plugin('Dawnguard.esm')
        for t, oo, _n, _d in dg.recorrer():
            if t == 'WRLD' and dg.form_id(oo) == 0x3C:
                ref = [(k, v) for k, v in Plugin.subrecords(dg.datos(oo)) if k not in ('OFST', 'RNAM')]
        # FULL es la unica diferencia: ID de string localizado en el master, texto en este plugin
        self.assertEqual([k for k, _ in mio], [k for k, _ in ref])
        for (k, a), (_k, b) in zip(mio, ref):
            if k != 'FULL':
                self.assertEqual(a, b, k)
        self.assertEqual(dict(mio)['FULL'], b'Skyrim\x00')

    def test_ningun_campo_de_texto_es_un_id_de_string_localizado(self):
        """Familia entera: este plugin NO es localizado (TES4 sin bit 0x80), asi que todo FULL,
        DESC, SHRT y NAM1 de TODO record tiene que ser una cadena terminada en cero. Un FULL de
        4 bytes copiado de Skyrim.esm se lee como basura ("æ "): SSEEdit lo marco en WRLD."""
        self.assertEqual(struct.unpack_from('<I', self.d, 8)[0] & 0x80, 0)
        vistos = 0
        for t, o, _n, _pr in self.items:
            if t in ('GRUP', 'TES4'):
                continue
            for k, v in Plugin.subrecords(self.p.datos(o)):
                if k in ('FULL', 'DESC', 'SHRT', 'NAM1'):
                    vistos += 1
                    self.assertTrue(v.endswith(b'\0') and b'\0' not in v[:-1],
                                    '%s %08X %s = %r no es texto' % (t, self.p.form_id(o), k, v))
        self.assertGreater(vistos, 0, 'el control no encontro ningun campo de texto')


@unittest.skipUnless(H.HAY_JUEGO, 'hace falta el runtime de Skyrim del config')
class CeldaDelMundo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.p = Plugin(str(H.ESP))
        cls.d = cls.p.d
        cls.refs = {}
        cur = None
        for t, o, _n, _pr in cls.p.recorrer():
            if t == 'CELL':
                cur = cls.p.form_id(o)
            elif t == 'REFR':
                cls.refs[cls.p.form_id(o)] = (cur, struct.unpack_from('<I', cls.d, o + 8)[0],
                                              list(Plugin.subrecords(cls.p.datos(o))))
        cls.nuevos = {f: v for f, v in cls.refs.items() if v[0] == H.CELDA and f >> 24 == 3}
        cls.propios = {}
        for t, o, _n, _pr in cls.p.recorrer():
            if t not in ('GRUP', 'TES4'):
                cls.propios[cls.p.form_id(o)] = t

    def test_la_cadena_de_grup_es_la_de_update_esm(self):
        mia = H.cadena(self.p, H.CELDA)
        self.assertIsNotNone(mia, 'el ESP no tiene la celda 0000963D')
        self.assertEqual(mia, H.cadena(H.plugin('Update.esm'), H.CELDA))
        self.assertEqual([g[0] for g in mia], [0, 1, 4, 5])

    def test_ninguna_celda_exterior_del_esp_repite_el_grid_de_una_vanilla(self):
        """El parche de Skyrim.esm creaba 00F00001 sobre el grid (1,-4) de 0000963D."""
        sk = H.plugin('Skyrim.esm')
        vanilla = {}
        mundo = None
        for t, o, _n, _d in sk.recorrer():
            if t == 'GRUP' and struct.unpack_from('<i', sk.d, o + 12)[0] == 1:
                mundo = struct.unpack_from('<I', sk.d, o + 8)[0]
            elif t == 'CELL' and mundo == 0x3C:
                xc = dict(Plugin.subrecords(sk.datos(o))).get('XCLC')
                if xc:
                    vanilla[struct.unpack_from('<2i', xc, 0)] = sk.form_id(o)
        for t, o, _n, _d in self.p.recorrer():
            if t != 'CELL':
                continue
            xc = dict(Plugin.subrecords(self.p.datos(o))).get('XCLC')
            if xc:
                grid = struct.unpack_from('<2i', xc, 0)
                self.assertEqual(vanilla.get(grid), self.p.form_id(o),
                                 'la celda %08X repite el grid %s de %s'
                                 % (self.p.form_id(o), grid, vanilla.get(grid)))

    def test_cada_nuevo_refr_viaja_con_su_base_y_cae_dentro_del_chunk(self):
        self.assertEqual(len(self.nuevos), REFR_AL_MUNDO)
        for fid, (_c, flags, subs) in self.nuevos.items():
            d = dict(subs)
            self.assertEqual(len(d['DATA']), 24, '%08X' % fid)
            x, y, z, rx, ry, rz = struct.unpack('<6f', d['DATA'])
            self.assertTrue(H.CHUNK[0] <= x < H.CHUNK[1] and H.CHUNK[2] <= y < H.CHUNK[3],
                            '%08X fuera del chunk (1,-4): (%.0f, %.0f)' % (fid, x, y))
            self.assertTrue(all(abs(a) < 7 for a in (rx, ry, rz)), 'rotacion en radianes %08X' % fid)
            self.assertFalse(flags & H.PERSISTENTE, 'persistente en una celda con grid: %08X' % fid)

    def test_todo_name_de_todo_refr_del_esp_resuelve_en_su_archivo(self):
        """La familia entera: 00xxxxxx existe en Skyrim.esm; 03xxxxxx existe en el ESP."""
        sk = H.plugin('Skyrim.esm')
        necesarios = {struct.unpack('<I', dict(s)['NAME'])[0] for _c, _f, s in self.refs.values()}
        vanilla = {b for b in necesarios if b >> 24 == 0}
        vistos = set()
        for t, o, _n, _d in sk.recorrer():
            if t not in ('GRUP', 'TES4') and sk.form_id(o) in vanilla:
                vistos.add(sk.form_id(o))
        self.assertEqual(vanilla - vistos, set(), 'bases vanilla que no existen en Skyrim.esm')
        for b in necesarios:
            self.assertIn(b >> 24, (0, 3), 'master inesperado en %08X' % b)
            if b >> 24 == 3:
                self.assertIn(b, self.propios, 'base propia %08X que el ESP no define' % b)

    def test_nada_del_laboratorio_interior_viaja_al_mundo(self):
        sk = H.plugin('Skyrim.esm')
        prohibidas = set()
        for t, o, _n, _d in sk.recorrer():
            if t == 'STAT' and zstr(dict(Plugin.subrecords(sk.datos(o))).get('EDID', b'')) in LABORATORIO:
                prohibidas.add(sk.form_id(o))
        self.assertEqual(len(prohibidas), len(LABORATORIO))
        luces = {f for f, t in self.propios.items() if t == 'LIGH'}
        for fid, (_c, _f, subs) in self.nuevos.items():
            base = struct.unpack('<I', dict(subs)['NAME'])[0]
            self.assertNotIn(base, prohibidas, '%08X es del laboratorio' % fid)
            self.assertNotIn(base, luces, '%08X es una luz del laboratorio' % fid)

    def test_las_posiciones_se_recalculan_a_mano_desde_la_celda_de_prueba(self):
        """Rigido a mano (sin mundo_v11): x' = X + x cos + y sin ; y' = Y - x sin + y cos ; z' = Z + z."""
        t = math.radians(H.MUNDO['rot_z_deg'])
        informe = json.loads((H.ROOT / 'reports/mundo_esp_v11.json').read_text(encoding='utf-8'))
        origen = {f: v for f, v in self.refs.items() if v[0] == 0x03000807}
        self.assertEqual(len(informe['refr_en_mundo']), REFR_AL_MUNDO)
        for par in informe['refr_en_mundo']:
            _c, _f, so = origen[int(par['origen'], 16)]
            _c, _f, sn = self.nuevos[int(par['nuevo'], 16)]
            x, y, z = struct.unpack_from('<3f', dict(so)['DATA'], 0)
            nx, ny, nz = struct.unpack_from('<3f', dict(sn)['DATA'], 0)
            self.assertAlmostEqual(nx, H.MUNDO['x'] + x * math.cos(t) + y * math.sin(t), delta=0.05)
            self.assertAlmostEqual(ny, H.MUNDO['y'] - x * math.sin(t) + y * math.cos(t), delta=0.05)
            self.assertAlmostEqual(nz, H.MUNDO['z'] + z, delta=0.05)
            self.assertEqual(dict(so)['NAME'], dict(sn)['NAME'])
            self.assertEqual(dict(so).get('XSCL'), dict(sn).get('XSCL'))

    def test_la_rotacion_global_se_compone_con_la_de_cada_pieza(self):
        """Con rotacion SOLO en Z, el giro del mundo suma al de la pieza (composicion de
        matrices con un solo eje: la suma de angulos es exacta). Se compara el angulo Z
        envuelto, con el signo de la convencion medida del repo (rot de motor = -rot matematico)."""
        origen = {f: v for f, v in self.refs.items() if v[0] == 0x03000807}
        informe = json.loads((H.ROOT / 'reports/mundo_esp_v11.json').read_text(encoding='utf-8'))
        vistos = 0
        for par in informe['refr_en_mundo']:
            _c, _f, so = origen[int(par['origen'], 16)]
            _c, _f, sn = self.nuevos[int(par['nuevo'], 16)]
            ro = struct.unpack_from('<3f', dict(so)['DATA'], 12)
            rn = struct.unpack_from('<3f', dict(sn)['DATA'], 12)
            if abs(ro[0]) < 1e-6 and abs(ro[1]) < 1e-6:           # solo Z
                esperado = math.degrees(ro[2]) + H.MUNDO['rot_z_deg']
                dif = abs((math.degrees(rn[2]) - esperado + 180.0) % 360.0 - 180.0)
                self.assertLess(dif, 0.01, par['origen'])
                vistos += 1
        self.assertGreaterEqual(vistos, 3)           # torre, ballesta, cofre, escudos...

    def test_la_celda_de_prueba_y_su_navmesh_quedan_byte_a_byte(self):
        antes = H.ANTES.read_bytes()
        despues = H.ESP.read_bytes()

        def grupo(d, etiqueta):
            p = struct.unpack_from('<I', d, 4)[0] + 24
            while p < len(d):
                tam, = struct.unpack_from('<I', d, p + 4)
                if d[p:p + 4] == b'GRUP' and d[p + 8:p + 12] == etiqueta:
                    return d[p:p + tam]
                p += tam if d[p:p + 4] == b'GRUP' else tam + 24
        self.assertEqual(grupo(antes, b'CELL'), grupo(despues, b'CELL'))
        self.assertEqual(grupo(antes, b'NAVI'), grupo(despues, b'NAVI'))

    def test_los_stat_del_esp_son_los_de_antes_en_un_solo_grupo(self):
        antes = Plugin(str(H.ANTES))
        ids_antes = {antes.form_id(o) for t, o, _n, _d in antes.recorrer() if t == 'STAT'}
        ahora = {f for f, t in self.propios.items() if t == 'STAT'}
        self.assertEqual(ids_antes, ahora)

    def test_masters_sin_cambios_y_solo_vanilla(self):
        mast = [v.rstrip(b'\0').decode() for k, v in Plugin.subrecords(self.p.datos(0)) if k == 'MAST']
        self.assertEqual(mast, ['Skyrim.esm', 'Update.esm', 'Dawnguard.esm'])


if __name__ == '__main__':
    unittest.main()
