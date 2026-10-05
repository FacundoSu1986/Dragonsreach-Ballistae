# -*- coding: utf-8 -*-
"""Cuerpos Havok de caja y propiedades de alfa de un NIF SSE, leidos del binario.

Lo usan build_assets.py (parche del cuerpo del virote), verify_assets.py (dentro
de Blender) y tests/test_v08_nif_fisica.py. Python puro: sin bpy ni PyNifly,
para verificar el archivo escrito y no la escena.

OFFSETS. bhkRigidBody: los de scripts/colision_caja.py de la skill
asset-nuevo-skyrim (inercia +116/+136/+156 en una matriz 3x4 de filas de 16 B,
masa +180, motionSystem +224). Traslacion +52, rotacion +68 (cuaternion xyzw)
y centro de masa +164 son los vectores de 16 B que preceden a la inercia y a la
masa; la restitucion es el octavo float desde la masa (+208). bhkBoxShape:
radio +4, semiejes +16. Verificados contra BoltProjectile.nif vanilla (masa 5,
friccion 0,5, restitucion 0,4, inercia 1,3276/0,0439/1,3358).
"""
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent/'vendor'))
import nif_nodos  # noqa: E402

HK = 69.99125            # unidades de juego por unidad Havok
COBERTURA_MINIMA = 0.90  # fraccion del largo visual que la caja tiene que cubrir
RADIO_TOPE = 0.1         # bhkRadius == min(semieje menor, 0,1): 2.667 de 2.684 cajas vanilla
ALINEACION_MINIMA = 0.99 # coseno entre el eje largo de la caja y el del visual (~8 grados)


def _ejes(q):
    """Imagen de cada eje del cuerpo (filas) en el marco del NIF, cuaternion Havok xyzw."""
    x, y, z, w = q
    return [(1 - 2 * (y * y + z * z), 2 * (x * y + w * z), 2 * (x * z - w * y)),
            (2 * (x * y - w * z), 1 - 2 * (x * x + z * z), 2 * (y * z + w * x)),
            (2 * (x * z + w * y), 2 * (y * z - w * x), 1 - 2 * (x * x + y * y))]


def _local(tr, rot, esc):
    return [[rot[f * 3 + c] * esc for c in range(3)] + [tr[f]] for f in range(3)]


def _mul(a, b):
    return [[sum(a[f][k] * b[k][c] for k in range(3)) for c in range(3)] +
            [sum(a[f][k] * b[k][3] for k in range(3)) + a[f][3]] for f in range(3)]


def _aplicar(m, p):
    return tuple(sum(m[f][c] * p[c] for c in range(3)) + m[f][3] for f in range(3))


def _saltar_net(d, p):
    """NiObjectNET: nombre, extra data y controller. Devuelve (nombre, offset siguiente)."""
    nombre, = struct.unpack_from('<i', d, p)
    n, = struct.unpack_from('<I', d, p + 4)
    return nombre, p + 8 + 4 * n + 4


def _shapes(nif):
    """(indice, nombre, offset, transformada local, shader, alfa, desc, n_verts, offset_vertices)."""
    d, s = nif['datos'], nif['strings']
    out = []
    for i, (t, o, _tam) in enumerate(nif['bloques']):
        if t != 'BSTriShape':
            continue
        nombre, p = _saltar_net(d, o)
        p += 4                                       # flags
        tr = struct.unpack_from('<3f', d, p)
        rot = struct.unpack_from('<9f', d, p + 12)
        esc, = struct.unpack_from('<f', d, p + 48)
        p += 52 + 4 + 16                             # escala, colision, esfera
        _piel, shader, alfa = struct.unpack_from('<3i', d, p)
        desc, = struct.unpack_from('<Q', d, p + 12)
        _nt, nv = struct.unpack_from('<HH', d, p + 20)
        out.append((i, s[nombre] if 0 <= nombre < len(s) else '?', o, _local(tr, rot, esc),
                    shader, alfa, desc, nv, p + 28))
    return out


def _mundo_padre(nif):
    """Funcion indice -> matriz de mundo del padre (nodos y shapes)."""
    nodos = nif['nodos']
    padre = {h: b for b, n in nodos.items() for h in n['hijos']}
    cache = {}

    def mundo_nodo(b):
        if b not in cache:
            n = nodos[b]
            m = _local(n['tr'], n['rot'], n['esc'])
            cache[b] = _mul(mundo_nodo(padre[b]), m) if b in padre else m
        return cache[b]

    ident = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]
    return lambda b: mundo_nodo(padre[b]) if b in padre else ident


def cuerpos_caja(nif):
    """[{...}] por cada bhkRigidBody(T) cuya forma es una bhkBoxShape."""
    d, bloques = nif['datos'], nif['bloques']
    out = []
    for i, (t, o, _tam) in enumerate(bloques):
        if not t.startswith('bhkRigidBody'):
            continue
        forma, = struct.unpack_from('<i', d, o)
        if not 0 <= forma < len(bloques) or bloques[forma][0] != 'bhkBoxShape':
            continue
        fo = bloques[forma][1]
        out.append({
            'cuerpo': i, 'tipo': t, 'forma': forma, 'offset_cuerpo': o, 'offset_forma': fo,
            'radio': struct.unpack_from('<f', d, fo + 4)[0],
            'semiejes_hk': list(struct.unpack_from('<3f', d, fo + 16)),
            'traslacion_hk': list(struct.unpack_from('<3f', d, o + 52)),
            'rotacion': list(struct.unpack_from('<4f', d, o + 68)),
            'inercia': [struct.unpack_from('<f', d, o + k)[0] for k in (116, 136, 156)],
            'masa': struct.unpack_from('<f', d, o + 180)[0],
            'restitucion': struct.unpack_from('<f', d, o + 208)[0],
        })
    return out


def mundo_del_cuerpo(nif, cuerpo):
    """Matriz de mundo del nodo que lleva el bhkCollisionObject de ese cuerpo.

    NiCollisionObject: target +0 (Ptr), flags +4 (u16), body +6 (Ref). Sin
    objeto de colision que lo referencie, identidad.
    """
    d, bloques = nif['datos'], nif['bloques']
    ident = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]
    for t, o, _tam in bloques:
        if t.endswith('CollisionObject') and struct.unpack_from('<i', d, o + 6)[0] == cuerpo:
            nodo, = struct.unpack_from('<i', d, o)
            n = nif['nodos'].get(nodo)
            if n is None:
                return ident
            return _mul(_mundo_padre(nif)(nodo), _local(n['tr'], n['rot'], n['esc']))
    return ident


def extension_en_nif(caja, mundo=None):
    """(semiejes, centro) de la caja en los ejes del NIF, en unidades de juego.

    `mundo` es la matriz del nodo dueño de la colisión (mundo_del_cuerpo); sin
    ella se supone identidad.
    """
    m = mundo or [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]
    ejes = [[sum(m[f][c] * e[c] for c in range(3)) for f in range(3)] for e in _ejes(caja['rotacion'])]
    semi = caja['semiejes_hk']
    ext = [sum(abs(ejes[k][j]) * semi[k] for k in range(3)) * HK for j in range(3)]
    return ext, list(_aplicar(m, [c * HK for c in caja['traslacion_hk']]))


def caja_visual(nif):
    """(min, max) en el marco del NIF de las shapes con BSLightingShaderProperty."""
    d, bloques = nif['datos'], nif['bloques']
    mundo_padre = _mundo_padre(nif)
    lo, hi = [float('inf')] * 3, [float('-inf')] * 3
    for i, _nombre, _o, local, shader, _alfa, desc, nv, datos in _shapes(nif):
        if not nv or not 0 <= shader < len(bloques) or bloques[shader][0] != 'BSLightingShaderProperty':
            continue
        m = _mul(mundo_padre(i), local)
        paso = (desc & 0xF) * 4
        for k in range(nv):
            p = _aplicar(m, struct.unpack_from('<3f', d, datos + k * paso))
            for j in range(3):
                lo[j] = min(lo[j], p[j])
                hi[j] = max(hi[j], p[j])
    return lo, hi


def cobertura(nif):
    """[{cuerpo, eje, eje_caja, fraccion}]: largo visual cubierto por cada caja.

    Se mide sobre el eje mas largo del VISUAL, y la caja tiene que tener ese
    mismo eje como el suyo mas largo: una caja del largo correcto pero cruzada
    (de pie o de costado) da fraccion 0. Medir sobre el eje propio de la caja
    aprobaba esa caja cruzada con 1,0.
    """
    lo, hi = caja_visual(nif)
    eje = max(range(3), key=lambda j: hi[j] - lo[j])
    largo = hi[eje] - lo[eje]
    out = []
    for caja in cuerpos_caja(nif):
        mundo = mundo_del_cuerpo(nif, caja['cuerpo'])
        ext, centro = extension_en_nif(caja, mundo)
        eje_caja = max(range(3), key=lambda j: ext[j])
        # Direccion del semieje mayor de la caja en el NIF: las extensiones de
        # una caja inclinada menos de ~26 grados todavia cubren el 90 %.
        k = max(range(3), key=lambda i: caja['semiejes_hk'][i])
        d = [sum(mundo[f][c] * _ejes(caja['rotacion'])[k][c] for c in range(3)) for f in range(3)]
        norma = sum(v * v for v in d) ** 0.5
        coseno = abs(d[eje]) / norma if norma else 0.0
        comun = max(0.0, min(centro[eje] + ext[eje], hi[eje]) - max(centro[eje] - ext[eje], lo[eje]))
        alineada = eje_caja == eje and coseno >= ALINEACION_MINIMA
        fraccion = comun / largo if largo > 0 and alineada else 0.0
        out.append({'cuerpo': caja['cuerpo'], 'eje': 'XYZ'[eje], 'eje_caja': 'XYZ'[eje_caja], 'coseno_eje': coseno,
                    'fraccion': fraccion, 'largo_visual': largo, 'largo_caja': 2 * ext[eje_caja]})
    return out


def inercia_alineada(caja):
    """Con masa > 0, el eje de menor inercia es el del semieje mayor (los dos en el marco del cuerpo)."""
    if caja['masa'] <= 0:
        return True
    menor = min(range(3), key=lambda k: caja['inercia'][k])
    largo = max(range(3), key=lambda k: caja['semiejes_hk'][k])
    return menor == largo


def reglas_vanilla(caja):
    """Las dos REGLAS de colision_caja.py; devuelve las fallas (vacio si cumple)."""
    fallas = []
    esperado = min(min(caja['semiejes_hk']), RADIO_TOPE)
    if abs(caja['radio'] - esperado) > 1e-6:
        fallas.append('bhkRadius %.6f, se esperaba min(semieje menor, %.1f) = %.6f' % (caja['radio'], RADIO_TOPE, esperado))
    if (caja['masa'] > 0) != (max(caja['inercia']) > 0):
        fallas.append('masa %.3f con inercia %s: masa > 0 <=> diagonal > 0' % (caja['masa'], caja['inercia']))
    return fallas


def propiedades_alfa(nif):
    """[{shape, flags, umbral}] por cada NiAlphaProperty del archivo.

    Las que referencia una BSTriShape llevan su nombre; un bloque NiAlphaProperty
    que ninguna shape referencia tambien cuenta (shape None): la regla es que
    no haya ninguno, no solo ninguno enganchado.
    """
    d, bloques = nif['datos'], nif['bloques']
    out = []
    usados = set()
    for _i, nombre, _o, _local_, _shader, alfa, _desc, _nv, _datos in _shapes(nif):
        if 0 <= alfa < len(bloques) and bloques[alfa][0] == 'NiAlphaProperty':
            _n, p = _saltar_net(d, bloques[alfa][1])
            flags, umbral = struct.unpack_from('<HB', d, p)
            out.append({'shape': nombre, 'flags': flags, 'umbral': umbral})
            usados.add(alfa)
    for i, (t, o, _tam) in enumerate(bloques):
        if t == 'NiAlphaProperty' and i not in usados:
            _n, p = _saltar_net(d, o)
            flags, umbral = struct.unpack_from('<HB', d, p)
            out.append({'shape': None, 'bloque': i, 'flags': flags, 'umbral': umbral})
    return out


def formula_caja(semiejes_hk, masa):
    """Inercia de libro de una caja maciza, m(a^2+b^2)/12 con lados completos."""
    lados = [2 * s for s in semiejes_hk]
    return [masa * (lados[1] ** 2 + lados[2] ** 2) / 12, masa * (lados[0] ** 2 + lados[2] ** 2) / 12,
            masa * (lados[0] ** 2 + lados[1] ** 2) / 12]


def inercia_por_donante(donante, semiejes_hk, masa):
    """HEURISTICA: conserva eje por eje la razon inercia/formula del donante.

    La skill midio que esa razon no es regla (va de 1,2 a 471, mediana 7,1);
    escalar la del donante es lo razonable cuando no hay un vanilla equivalente.
    """
    antes = formula_caja(donante['semiejes_hk'], donante['masa'])
    despues = formula_caja(semiejes_hk, masa)
    return [donante['inercia'][k] / antes[k] * despues[k] for k in range(3)]


def parchear_cuerpo_caja(ruta, semiejes_u, centro_u, masa, restitucion, inercia, rotacion=(0.0, 0.0, 1.0, 0.0)):
    """Reescribe en el lugar el unico cuerpo de caja del NIF: forma, pose, inercia, masa y restitucion.

    Todos los campos son de tamano fijo: ningun bloque cambia de largo ni de
    indice. El radio sigue la regla vanilla y el centro de masa queda en 0.
    """
    ruta = Path(ruta)
    nif = nif_nodos.leer(str(ruta))
    cajas = cuerpos_caja(nif)
    if len(cajas) != 1:
        raise ValueError('se esperaba exactamente un cuerpo de caja y hay %d' % len(cajas))
    caja = cajas[0]
    b = bytearray(nif['datos'])
    semi = [v / HK for v in semiejes_u]
    struct.pack_into('<f', b, caja['offset_forma'] + 4, min(min(semi), RADIO_TOPE))
    struct.pack_into('<3f', b, caja['offset_forma'] + 16, *semi)
    o = caja['offset_cuerpo']
    struct.pack_into('<4f', b, o + 52, *(v / HK for v in centro_u), 0.0)
    struct.pack_into('<4f', b, o + 68, *rotacion)
    for fila in range(3):
        valores = [0.0, 0.0, 0.0, 0.0]
        valores[fila] = inercia[fila]
        struct.pack_into('<4f', b, o + 116 + 16 * fila, *valores)
    struct.pack_into('<4f', b, o + 164, 0.0, 0.0, 0.0, 0.0)
    struct.pack_into('<f', b, o + 180, masa)
    struct.pack_into('<f', b, o + 208, restitucion)
    ruta.write_bytes(bytes(b))
    return cuerpos_caja(nif_nodos.leer(str(ruta)))[0]
