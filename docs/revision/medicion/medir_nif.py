# -*- coding: utf-8 -*-
"""Solo lectura. Vuelca de NIFs SSE lo que usa la revision tecnica v07.

    python -B docs/revision/medicion/medir_nif.py [archivo.nif ...]

Sin argumentos mide los 3 NIF del mod y los vanilla de referencia (carpeta
`extracted` de config.json) y comprueba si WoodWalkway01.dds tiene texeles
transparentes. Por NIF informa: BSXFlags, NiStringExtraData, cuerpos Havok
(capa, masa, inercia, movimiento, caja en el marco del NIF), shaders, alfa,
shapes (tris, verts, atributos, caja visual) y secuencias Gamebryo. Para cada
caja Havok da la cobertura sobre el largo visual de las shapes con
BSLightingShaderProperty: es el chequeo que hoy no hace verify_assets.py.

Offsets de bhkRigidBody tomados de scripts/colision_caja.py de la skill
asset-nuevo-skyrim (inercia +116/+136/+156, masa +180, motionSystem +224);
traslacion +52 y rotacion +68 son los 64 bytes previos a la inercia.
"""
import json
import struct
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts' / 'vendor'))
import nif_nodos  # noqa: E402

CFG = json.loads((ROOT / 'config.json').read_text())
EXTRAIDO = Path(CFG['extracted'])
HK = 69.99125  # unidades de juego por unidad Havok

MOD = [ROOT / 'mod' / 'meshes' / 'AstraAsedio' / n for n in ('torre.nif', 'ballesta.nif', 'virote.nif')]
VANILLA = ['dlc01/weapons/crossbow/boltprojectile.nif',
           'dlc01/weapons/dwarven crossbow/dwarvenboltprojectile.nif',
           'dlc02/weapons/dwarvenbolts/bolts.nif',
           'traps/bowtrap/largebolt01.nif',
           'dlc01/traps/crossbowtraps/plaincrossbow/plaincrossbowtrap01.nif',
           'clutter/civilwar/catapult/civilwarcatapult01.nif']
TEXTURA_PISO = 'architecture/farmhouse/woodwalkway01.dds'

CAPA = {1: 'STATIC', 2: 'ANIMSTATIC', 3: 'TRANSPARENT', 4: 'CLUTTER', 5: 'WEAPON', 6: 'PROJECTILE',
        7: 'SPELL', 8: 'BIPED', 9: 'TREES', 10: 'PROPS', 11: 'WATER', 12: 'TRIGGER', 13: 'TERRAIN',
        14: 'TRAP', 15: 'NONCOLLIDABLE', 16: 'CLOUD_TRAP', 17: 'GROUND', 18: 'PORTAL',
        19: 'DEBRIS_SMALL', 20: 'DEBRIS_LARGE'}
MOVIMIENTO = {0: 'INVALID', 1: 'DYNAMIC', 2: 'SPHERE_INERTIA', 3: 'SPHERE_STABILIZED', 4: 'BOX_INERTIA',
              5: 'BOX_STABILIZED', 6: 'KEYFRAMED', 7: 'FIXED', 8: 'THIN_BOX', 9: 'CHARACTER'}
CALIDAD = {0: 'INVALID', 1: 'FIXED', 2: 'KEYFRAMED', 3: 'DEBRIS', 4: 'MOVING', 5: 'CRITICAL',
           6: 'BULLET', 7: 'USER', 8: 'CHARACTER', 9: 'KEYFRAMED_REPORT'}
BSX = ['Animated', 'Havok', 'Ragdoll', 'Complex', 'Addon', 'EditorMarker', 'Dynamic', 'Articulated',
       'NeedsTransformUpdates', 'ExternalEmit']
F1 = ['Specular', 'Skinned', 'TempRefraction', 'VertexAlpha', 'GreyToPalColor', 'GreyToPalAlpha',
      'UseFalloff', 'EnvMap', 'ReceiveShadows', 'CastShadows', 'FacegenDetail', 'Parallax',
      'ModelSpaceNormals', 'NonProjShadows', 'Landscape', 'Refraction', 'FireRefraction', 'EyeEnvMap',
      'HairSoftLight', 'ScreendoorAlphaFade', 'LocalmapHideSecret', 'FaceGenTint', 'OwnEmit',
      'ProjectedUV', 'MultipleTextures', 'RemappableTex', 'Decal', 'DynamicDecal', 'ParallaxOcc',
      'ExternalEmit', 'SoftEffect', 'ZBufferTest']
F2 = ['ZBufferWrite', 'LODLandscape', 'LODObjects', 'NoFade', 'DoubleSided', 'VertexColors', 'GlowMap',
      'AssumeShadowmask', 'PackedTangent', 'MultiIndexSnow', 'VertexLighting', 'UniformScale',
      'FitSlope', 'Billboard', 'NoLODLandBlend', 'EnvMapLightFade', 'Wireframe', 'WeaponBlood',
      'HideOnLocalMap', 'PremultAlpha', 'CloudLOD', 'AnisoLighting', 'NoTranspMultisample',
      'Unused01', 'MultiLayerParallax', 'SoftLighting', 'RimLighting', 'BackLighting', 'Unused02',
      'TreeAnim', 'EffectLighting', 'HDLODObjects']
ATRIB = ['VERTEX', 'UV', 'UV2', 'NORMAL', 'TANGENT', 'COLORS', 'SKINNED', 'LAND', 'EYE', '?', 'FULLPREC']


def bits(v, nombres):
    return '|'.join(n for i, n in enumerate(nombres) if v >> i & 1)


def saltar_net(d, p):
    """NiObjectNET: nombre, extra data, controller. Devuelve (nombre, offset siguiente)."""
    nombre, = struct.unpack_from('<i', d, p)
    n, = struct.unpack_from('<I', d, p + 4)
    return nombre, p + 8 + 4 * n + 4


def local(tr, rot, esc):
    return [[rot[f * 3 + c] * esc for c in range(3)] + [tr[f]] for f in range(3)]


def mul(A, B):
    return [[sum(A[f][k] * B[k][c] for k in range(3)) for c in range(3)] +
            [sum(A[f][k] * B[k][3] for k in range(3)) + A[f][3]] for f in range(3)]


def aplicar(M, p):
    return tuple(sum(M[f][c] * p[c] for c in range(3)) + M[f][3] for f in range(3))


def ejes_quat(x, y, z, w):
    """Imagen de cada eje local (filas) para un cuaternion Havok xyzw."""
    return [(1 - 2 * (y * y + z * z), 2 * (x * y + w * z), 2 * (x * z - w * y)),
            (2 * (x * y - w * z), 1 - 2 * (x * x + z * z), 2 * (y * z + w * x)),
            (2 * (x * z + w * y), 2 * (y * z - w * x), 1 - 2 * (x * x + y * y))]


def mundo_de_bloques(nif):
    """{indice de bloque: matriz de mundo del PADRE}, para nodos y shapes."""
    nodos = nif['nodos']
    padre = {h: b for b, n in nodos.items() for h in n['hijos']}
    cache = {}

    def mundo_nodo(b):
        if b not in cache:
            n = nodos[b]
            M = local(n['tr'], n['rot'], n['esc'])
            cache[b] = mul(mundo_nodo(padre[b]), M) if b in padre else M
        return cache[b]

    ident = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]
    return lambda b: mundo_nodo(padre[b]) if b in padre else ident


def volcar(ruta):
    nif = nif_nodos.leer(str(ruta))
    d, S, B = nif['datos'], nif['strings'], nif['bloques']
    st = lambda i: S[i] if 0 <= i < len(S) else None  # noqa: E731
    mundo_padre = mundo_de_bloques(nif)
    print('\n=====', ruta)
    hist = {}
    for t, _o, _s in B:
        hist[t] = hist.get(t, 0) + 1
    print('bloques:', ', '.join('%s x%d' % kv for kv in sorted(hist.items())))
    total_t = total_v = 0
    largo_visual = [None, None]  # Y min/max de shapes con BSLightingShaderProperty
    cajas = []
    for i, (t, o, s) in enumerate(B):
        if t == 'BSXFlags':
            nombre, v = struct.unpack_from('<iI', d, o)
            print('BSXFlags %s = %d (%s)' % (st(nombre), v, bits(v, BSX)))
        elif t == 'NiStringExtraData':
            nombre, v = struct.unpack_from('<ii', d, o)
            print('NiStringExtraData %s = %s' % (st(nombre), st(v)))
        elif t == 'bhkCollisionObject':
            destino, fl, cuerpo = struct.unpack_from('<iHi', d, o)
            print('bhkCollisionObject[%d] destino=%d flags=0x%X cuerpo=%d(%s)' % (i, destino, fl, cuerpo, B[cuerpo][0]))
        elif t.startswith('bhkRigidBody'):
            forma, capa = struct.unpack_from('<iB', d, o)
            tr = struct.unpack_from('<3f', d, o + 52)
            q = struct.unpack_from('<4f', d, o + 68)
            inercia = [struct.unpack_from('<f', d, o + k)[0] for k in (116, 136, 156)]
            masa, amort_l, amort_a, _tf, _gf, friccion, _rf, restit = struct.unpack_from('<8f', d, o + 180)
            mov, _desact, _solver, cal = struct.unpack_from('<4B', d, o + 224)
            print('%s[%d] forma=%s capa=%s masa=%.3f inercia=%s amort=%.4f/%.4f friccion=%.2f restitucion=%.2f movimiento=%s calidad=%s'
                  % (t, i, B[forma][0], CAPA.get(capa, capa), masa, [round(x, 4) for x in inercia],
                     amort_l, amort_a, friccion, restit, MOVIMIENTO.get(mov, mov), CALIDAD.get(cal, cal)))
            tf, of, _sf = B[forma]
            if tf == 'bhkBoxShape':
                material, radio = struct.unpack_from('<If', d, of)
                semi = struct.unpack_from('<3f', d, of + 16)
                ejes = ejes_quat(*q)
                ext = [sum(abs(ejes[k][j]) * semi[k] for k in range(3)) for j in range(3)]
                centro = [x * HK for x in tr]
                print('   bhkBoxShape material=0x%08X radio=%.5f semiejes(havok)=%s' % (material, radio, [round(x, 5) for x in semi]))
                print('   caja en el marco del NIF (u): largo X/Y/Z=%s centro=%s'
                      % ([round(2 * x * HK, 2) for x in ext], [round(x, 2) for x in centro]))
                cajas.append((centro[1] - ext[1] * HK, centro[1] + ext[1] * HK))
        elif t == 'BSLightingShaderProperty':
            tipo, = struct.unpack_from('<I', d, o)
            _n, p = saltar_net(d, o + 4)
            f1, f2 = struct.unpack_from('<II', d, p)
            p += 8 + 16
            texset, = struct.unpack_from('<i', d, p)
            p += 4 + 16
            _clamp, alfa, _refr, brillo = struct.unpack_from('<Ifff', d, p)
            p += 16
            espec = struct.unpack_from('<4f', d, p)
            p += 16 + 8
            extra = ' envMapScale=%.2f' % struct.unpack_from('<f', d, p)[0] if tipo == 1 else ''
            texturas = []
            if 0 <= texset < len(B) and B[texset][0] == 'BSShaderTextureSet':
                q2 = B[texset][1]
                n, = struct.unpack_from('<I', d, q2)
                q2 += 4
                for _ in range(n):
                    largo, = struct.unpack_from('<I', d, q2)
                    texturas.append(d[q2 + 4:q2 + 4 + largo].decode('cp1252', 'replace'))
                    q2 += 4 + largo
            print('BSLightingShaderProperty[%d] tipo=%d brillo=%.0f especular=%.2f alfa=%.2f%s'
                  % (i, tipo, brillo, espec[3], alfa, extra))
            print('   F1=%s' % bits(f1, F1))
            print('   F2=%s' % bits(f2, F2))
            print('   texturas=%s' % [x for x in texturas if x])
        elif t == 'NiAlphaProperty':
            _n, p = saltar_net(d, o)
            fl, umbral = struct.unpack_from('<HB', d, p)
            print('NiAlphaProperty[%d] flags=%d (0x%X) umbral=%d' % (i, fl, fl, umbral))
        elif t == 'BSTriShape':
            nombre, p = saltar_net(d, o)
            p += 4
            tr = struct.unpack_from('<3f', d, p)
            rot = struct.unpack_from('<9f', d, p + 12)
            esc, = struct.unpack_from('<f', d, p + 48)
            p += 52 + 4 + 16
            _piel, shader, alfa = struct.unpack_from('<3i', d, p)
            p += 12
            desc, = struct.unpack_from('<Q', d, p)
            p += 8
            nt, nv = struct.unpack_from('<HH', d, p)
            p += 8
            total_t += nt
            total_v += nv
            caja = ''
            if nv:
                M = mul(mundo_padre(i), local(tr, rot, esc))
                tam = (desc & 0xF) * 4
                pts = [aplicar(M, struct.unpack_from('<3f', d, p + k * tam)) for k in range(nv)]
                lo = [min(q[j] for q in pts) for j in range(3)]
                hi = [max(q[j] for q in pts) for j in range(3)]
                caja = ' caja=%s..%s' % ([round(x, 1) for x in lo], [round(x, 1) for x in hi])
                if 0 <= shader < len(B) and B[shader][0] == 'BSLightingShaderProperty':
                    largo_visual[0] = lo[1] if largo_visual[0] is None else min(largo_visual[0], lo[1])
                    largo_visual[1] = hi[1] if largo_visual[1] is None else max(largo_visual[1], hi[1])
            print('BSTriShape[%d] %s tris=%d verts=%d vertice=%dB atributos=%s alfa=%d%s'
                  % (i, st(nombre), nt, nv, (desc & 0xF) * 4, bits(desc >> 44 & 0xFFF, ATRIB), alfa, caja))
        elif t == 'NiControllerSequence':
            nombre, nb, _crece = struct.unpack_from('<iII', d, o)
            p = o + 12 + nb * 29
            _peso, claves, ciclo, frec, ini, fin = struct.unpack_from('<fiIfff', d, p)
            print('NiControllerSequence %s bloques=%d ciclo=%s frecuencia=%.2f inicio=%.3f fin=%.3f textKeys=%s'
                  % (st(nombre), nb, {0: 'LOOP', 1: 'REVERSE', 2: 'CLAMP'}.get(ciclo, ciclo), frec, ini, fin,
                     'si' if claves >= 0 else 'no'))
    print('TOTAL BSTriShape: tris=%d verts=%d' % (total_t, total_v))
    if largo_visual[0] is not None:
        largo = largo_visual[1] - largo_visual[0]
        print('largo visual en Y (shapes con BSLightingShaderProperty): %.2f u (%.2f..%.2f)' % (largo, largo_visual[0], largo_visual[1]))
        for a, b in cajas:
            comun = max(0.0, min(b, largo_visual[1]) - max(a, largo_visual[0]))
            print('cobertura de la caja Havok sobre ese largo: %.1f %% (caja Y %.2f..%.2f)' % (100.0 * comun / largo, a, b))


def transparencia_dxt1(ruta):
    """Cuenta texeles transparentes en el mip 0 de un DDS DXT1 (BC1)."""
    d = ruta.read_bytes()
    if d[:4] != b'DDS ' or d[84:88] != b'DXT1':
        print('\n=====', ruta, '\nno es DXT1: fourcc=%r' % d[84:88])
        return
    alto, ancho = struct.unpack_from('<II', d, 12)
    n = (ancho // 4) * (alto // 4)
    bloques = texeles = 0
    for k in range(n):
        c0, c1, idx = struct.unpack_from('<HHI', d, 128 + 8 * k)
        if c0 <= c1:  # modo de 3 colores: el indice 3 es transparente
            m = sum(1 for j in range(16) if idx >> (2 * j) & 3 == 3)
            if m:
                bloques += 1
                texeles += m
    print('\n=====', ruta)
    print('DXT1 %dx%d: bloques con texeles transparentes %d de %d; texeles transparentes %.3f %%'
          % (ancho, alto, bloques, n, 100.0 * texeles / (16 * n)))


def main(argv):
    rutas = [Path(a) for a in argv] or MOD + [EXTRAIDO / 'meshes' / r for r in VANILLA]
    fallas = 0
    for r in rutas:
        try:
            volcar(r)
        except Exception as e:  # un NIF ilegible no tiene que tapar los demas
            fallas += 1
            print('\n=====', r, '\nERROR', repr(e))
    if not argv:
        transparencia_dxt1(EXTRAIDO / 'textures' / TEXTURA_PISO)
    return 1 if fallas else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
