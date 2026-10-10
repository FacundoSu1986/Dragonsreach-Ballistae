"""Plataforma de terreno de v11: el LAND que escribe AstraAsedio.esp bajo la torre.

Cada control esta pensado para poder fallar:
  - el decodificador se valida contra la realidad (el Z que el usuario leyo en el juego y
    los objetos vanilla de la celda), no contra si mismo;
  - la plataforma se mide sobre el archivo escrito, con un lector independiente;
  - el control negativo exige que el terreno VANILLA no pase el mismo criterio.
"""
import math
import struct
import unittest

import _mundo_helpers as H
from parser_esm import Plugin

PISO_PLATAFORMA = -4952.0
HUELLA_X = (-300.0, 400.0)
HUELLA_Y = (-570.0, 300.0)
PIE_ESCALERA = (323.4, -536.0)


def huecos_de_pilotes(h, z_torre):
    """hueco = base del pilote en el mundo - terreno. Positivo: flota."""
    out = {}
    for nombre, lx, ly, bz in H.pilotes():
        x, y = H.a_mundo(lx, ly)
        out[nombre] = (z_torre + bz) - H.altura(h, x, y)
    return out


def relieve_de_la_huella(h):
    zs = []
    for lx in range(int(HUELLA_X[0]), int(HUELLA_X[1]) + 1, 25):
        for ly in range(int(HUELLA_Y[0]), int(HUELLA_Y[1]) + 1, 25):
            x, y = H.a_mundo(lx, ly)
            zs.append(H.altura(h, x, y))
    return max(zs) - min(zs)


def fallas(h, z_torre):
    """Lista de criterios que el terreno h NO cumple para la torre en z_torre."""
    malas = []
    flotan = [n for n, g in huecos_de_pilotes(h, z_torre).items() if g > 1.0]
    if flotan:
        malas.append('pilotes que flotan: %d' % len(flotan))
    x, y = H.a_mundo(*PIE_ESCALERA)
    pie = z_torre - H.altura(h, x, y)
    if abs(pie) > 1.5:
        malas.append('pie de la escalera a %.1f u del suelo' % pie)
    rel = relieve_de_la_huella(h)
    if rel > 2.0:
        malas.append('relieve de la huella %.1f u' % rel)
    return malas


@unittest.skipUnless(H.HAY_JUEGO, 'hace falta el runtime de Skyrim del config')
class DecodificadorContraLaRealidad(unittest.TestCase):
    """VHGT decodificado a mano: tiene que coincidir con lo que se ve en el juego."""

    def test_el_centro_da_el_z_que_el_usuario_leyo_en_el_juego(self):
        h = H.decodificar(dict(H.land_ganador())['VHGT'])
        terreno = H.altura(h, H.MUNDO['x'], H.MUNDO['y'])
        self.assertLess(abs(terreno - H.MUNDO['z']), 3.0,
                        'terreno %.1f contra Z de la torre %.2f' % (terreno, H.MUNDO['z']))

    def test_los_objetos_vanilla_de_la_celda_estan_sobre_ese_terreno(self):
        h = H.decodificar(dict(H.land_ganador())['VHGT'])
        difs = []
        for fid, (fl, subs) in H.refrs_vanilla_de_la_celda().items():
            d = dict(subs).get('DATA', b'')
            if len(d) >= 24 and not fl & H.PERSISTENTE:
                x, y, z = struct.unpack_from('<3f', d, 0)
                if H.CHUNK[0] <= x < H.CHUNK[1] and H.CHUNK[2] <= y < H.CHUNK[3]:
                    difs.append(z - H.altura(h, x, y))
        self.assertGreaterEqual(len(difs), 50)
        cerca = sum(1 for q in difs if abs(q) < 60.0)
        self.assertGreaterEqual(cerca / len(difs), 0.75,
                                '%d de %d objetos a +-60 u del terreno' % (cerca, len(difs)))

    def test_skyrim_y_update_tienen_la_misma_altura_en_esta_celda(self):
        a = dict(H.land_de('Skyrim.esm'))['VHGT']
        b = dict(H.land_de('Update.esm'))['VHGT']
        self.assertEqual(a, b)


@unittest.skipUnless(H.HAY_JUEGO, 'hace falta el runtime de Skyrim del config')
class PlataformaEnElEsp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.esp = Plugin(str(H.ESP))
        cls.land = H.land_del_esp(cls.esp)
        cls.vanilla = H.land_ganador()
        cls.h = H.decodificar(dict(cls.land)['VHGT']) if cls.land else None
        cls.h0 = H.decodificar(dict(cls.vanilla)['VHGT'])

    def test_el_esp_trae_el_land_de_la_celda(self):
        self.assertIsNotNone(self.land, 'el ESP no sobrescribe el LAND de la celda 0000963D')

    def test_ningun_pilote_flota_ni_el_pie_de_la_escalera_ni_la_huella(self):
        self.assertEqual(fallas(self.h, H.MUNDO['z']), [])

    def test_control_negativo_el_terreno_vanilla_no_pasa_el_mismo_criterio(self):
        malas = fallas(self.h0, H.MUNDO['z'])
        self.assertEqual(len(malas), 3, malas)       # flotan, pie de escalera, relieve
        self.assertGreater(relieve_de_la_huella(self.h0), 100.0)

    def test_la_plataforma_esta_a_una_altura_que_el_formato_puede_guardar(self):
        self.assertEqual(PISO_PLATAFORMA % 8, 0)
        x, y = H.a_mundo(0, 0)
        self.assertEqual(H.altura(self.h, x, y), PISO_PLATAFORMA)
        self.assertLess(abs(PISO_PLATAFORMA - H.MUNDO['z']), 1.0)

    def test_los_bordes_de_la_celda_no_cambian_alturas_ni_normales(self):
        for r in range(33):
            for c in range(33):
                if r in (0, 32) or c in (0, 32):
                    self.assertEqual(self.h[r][c], self.h0[r][c], (r, c))
                    i = (r * 33 + c) * 3
                    self.assertEqual(dict(self.land)['VNML'][i:i + 3],
                                     dict(self.vanilla)['VNML'][i:i + 3], (r, c))

    def test_solo_cambia_una_zona_acotada_alrededor_de_la_torre(self):
        cambiados = [(r, c) for r in range(33) for c in range(33)
                     if self.h[r][c] != self.h0[r][c]]
        self.assertTrue(cambiados)
        t = math.radians(H.MUNDO['rot_z_deg'])
        for r, c in cambiados:
            dx, dy = 4096.0 + c * 128.0 - H.MUNDO['x'], -16384.0 + r * 128.0 - H.MUNDO['y']
            lx, ly = dx * math.cos(t) - dy * math.sin(t), dx * math.sin(t) + dy * math.cos(t)
            fuera = math.hypot(max(HUELLA_X[0] - lx, 0.0, lx - HUELLA_X[1]),
                               max(HUELLA_Y[0] - ly, 0.0, ly - HUELLA_Y[1]))
            # margen de 64 u + el cuadrante (128 u) + 2 anillos de 128 u, en diagonal
            self.assertLess(fuera, 64.0 + 3 * 128.0 * 2 ** 0.5, (r, c, round(fuera)))

    def test_el_resto_de_las_capas_del_land_es_el_de_update(self):
        n, v = dict(self.land), dict(self.vanilla)
        self.assertEqual(sorted(n), sorted(v))
        for k in v:
            if k not in ('VHGT', 'VNML'):
                self.assertEqual(n[k], v[k], k)

    def test_las_normales_de_la_plataforma_son_planas_y_las_demas_se_parecen(self):
        norm = dict(self.land)['VNML']
        n0 = dict(self.vanilla)['VNML']
        planos = 0
        for r in range(33):
            for c in range(33):
                i = (r * 33 + c) * 3
                a, b = struct.unpack_from('<3b', norm, i), struct.unpack_from('<3b', n0, i)
                if self.h[r][c] == PISO_PLATAFORMA and a == (0, 0, 127):
                    planos += 1
                self.assertGreater(a[2], 60, 'normal casi horizontal en (%d,%d): %s' % (r, c, a))
                self.assertLess(max(abs(a[i2] - b[i2]) for i2 in range(3)), 128)
        self.assertGreaterEqual(planos, 80)

    def test_los_objetos_vanilla_acompanan_al_suelo_que_se_movio(self):
        """Familia entera: todo REFR vanilla de la celda cuyo suelo cambio mas de 15 u
        tiene un override con la Z corrida, y el override no toca nada mas."""
        overrides = {}
        cur = None
        for t, o, _n, _d in self.esp.recorrer():
            if t == 'CELL':
                cur = self.esp.form_id(o)
            elif t == 'REFR' and cur == H.CELDA and (self.esp.form_id(o) >> 24) == 0:
                overrides[self.esp.form_id(o)] = list(Plugin.subrecords(self.esp.datos(o)))
        esperados = set()
        for fid, (fl, subs) in H.refrs_vanilla_de_la_celda().items():
            d = dict(subs).get('DATA', b'')
            if len(d) < 24 or fl & H.PERSISTENTE:
                continue
            x, y, z = struct.unpack_from('<3f', d, 0)
            dz = H.altura(self.h, x, y) - H.altura(self.h0, x, y)
            if abs(dz) > 15.0:
                esperados.add(fid)
                self.assertIn(fid, overrides, 'falta el override del objeto %08X' % fid)
                nz = struct.unpack_from('<f', dict(overrides[fid])['DATA'], 8)[0]
                self.assertLess(abs(nz - (z + dz)), 0.2, '%08X' % fid)
                resto = [(k, v) for k, v in overrides[fid] if k != 'DATA']
                self.assertEqual(resto, [(k, v) for k, v in subs if k != 'DATA'], '%08X' % fid)
                self.assertEqual(dict(overrides[fid])['DATA'][:8], d[:8])
                self.assertEqual(dict(overrides[fid])['DATA'][12:], d[12:])
        self.assertEqual(set(overrides), esperados, 'overrides de objetos que no hacian falta')


if __name__ == '__main__':
    unittest.main()
