# -*- coding: utf-8 -*-
"""Solo lectura. Barrido de la cabeza giratoria de ballesta.nif contra el puesto fijo del operador.

    python -B docs/revision/medicion/medir_barrido_operador.py

La cabeza gira 360 grados alrededor del eje Z de CTRL_GIRO_360 y eleva
alrededor del eje X de CTRL_ELEVACION (signo -1: el frente, -Y, sube). El
OperatorNode cuelga de la raiz fija. Para cada elevacion se rota la geometria
de la rama de elevacion, se suma la de la rama de giro y se mide, por debajo
de la altura del cuerpo (z <= 125 sobre la raiz), el radio respecto del eje de
giro. Como el giro es libre, todo vertice que caiga en el anillo del operador
pasa por el, en algun angulo, a esa altura. Las cuerdas (Cuerda_I/D) quedan
fuera: se animan por escala.

Capsula del operador: 18 u, la misma holgura que usa build_plugin.py para el
navmesh (capsule_clearance_xy).
"""
import math
import struct
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts' / 'vendor'))
import nif_nodos  # noqa: E402

RUTA = ROOT / 'mod' / 'meshes' / 'AstraAsedio' / 'ballesta.nif'
ALTURA_CUERPO = 125.0
CAPSULA = 18.0
ELEVACIONES = (-5, 0, 15, 30, 45, 60, 80)


def local(tr, rot, esc):
    return [[rot[f * 3 + c] * esc for c in range(3)] + [tr[f]] for f in range(3)]


def mul(A, B):
    return [[sum(A[f][k] * B[k][c] for k in range(3)) for c in range(3)] +
            [sum(A[f][k] * B[k][3] for k in range(3)) + A[f][3]] for f in range(3)]


def aplicar(M, p):
    return tuple(sum(M[f][c] * p[c] for c in range(3)) + M[f][3] for f in range(3))


def es_identidad(M, tol=1e-4):
    return all(abs(M[f][c] - (1.0 if f == c else 0.0)) < tol for f in range(3) for c in range(3))


def main():
    nif = nif_nodos.leer(str(RUTA))
    d, S, B, N = nif['datos'], nif['strings'], nif['bloques'], nif['nodos']
    padre = {h: b for b, n in N.items() for h in n['hijos']}
    por_nombre = {n['nombre']: b for b, n in N.items()}
    giro, elev, op = por_nombre['CTRL_GIRO_360'], por_nombre['CTRL_ELEVACION'], por_nombre['OperatorNode']

    def relativo(b, hasta):
        """Transformada de b expresada en el marco del nodo `hasta` (o de la raiz si None)."""
        M = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]
        while b in padre and padre[b] != hasta:
            b = padre[b]
            n = N[b]
            M = mul(local(n['tr'], n['rot'], n['esc']), M)
        return M

    M_giro = mul(relativo(giro, None), local(N[giro]['tr'], N[giro]['rot'], N[giro]['esc']))
    M_elev_en_giro = local(N[elev]['tr'], N[elev]['rot'], N[elev]['esc'])
    if not (es_identidad(M_giro) and es_identidad(M_elev_en_giro) and abs(M_giro[0][3]) < 1e-3 and abs(M_giro[1][3]) < 1e-3):
        print('AVISO: los pivotes tienen rotacion o el eje de giro no pasa por x=y=0; el radio no es el del eje')
    z_giro = M_giro[2][3]
    z_elev = z_giro + M_elev_en_giro[2][3]
    M_op = mul(relativo(op, None), local(N[op]['tr'], N[op]['rot'], N[op]['esc']))
    r_op = math.hypot(M_op[0][3], M_op[1][3])
    print('pivote de giro z=%.1f, pivote de elevacion z=%.1f (sobre la raiz)' % (z_giro, z_elev))
    print('OperatorNode xy=(%.1f, %.1f) cuelga de %s, radio=%.1f u; capsula=%.0f u -> cuerpo en r %.1f..%.1f'
          % (M_op[0][3], M_op[1][3], N[padre[op]]['nombre'], r_op, CAPSULA, r_op - CAPSULA, r_op + CAPSULA))

    rama_elev, rama_giro, fijo = [], [], []
    for i, (t, o, _s) in enumerate(B):
        if t != 'BSTriShape':
            continue
        nombre, = struct.unpack_from('<i', d, o)
        nombre = S[nombre]
        if nombre.startswith('Cuerda'):
            continue
        p = o + 4
        n_ed, = struct.unpack_from('<I', d, p)
        p += 4 + 4 * n_ed + 4 + 4
        tr = struct.unpack_from('<3f', d, p)
        rot = struct.unpack_from('<9f', d, p + 12)
        esc, = struct.unpack_from('<f', d, p + 48)
        p += 52 + 4 + 16 + 12
        desc, = struct.unpack_from('<Q', d, p)
        _nt, nv = struct.unpack_from('<HH', d, p + 8)
        datos = p + 16
        tam = (desc & 0xF) * 4
        cadena = []
        b = i
        while b in padre:
            b = padre[b]
            cadena.append(b)
        forma = local(tr, rot, esc)
        if elev in cadena:
            M, destino = mul(relativo(i, elev), forma), rama_elev
        elif giro in cadena:
            M, destino = mul(relativo(i, giro), forma), rama_giro
        else:
            M, destino = mul(relativo(i, None), forma), fijo
        destino.extend((aplicar(M, struct.unpack_from('<3f', d, datos + k * tam)), nombre) for k in range(nv))

    for grados in ELEVACIONES:
        a = math.radians(grados)
        puntos = []
        for (x, y, z), n in rama_elev:
            # rotacion en X por -a: el frente (-Y) sube cuando a > 0
            y2 = y * math.cos(a) + z * math.sin(a)
            z2 = -y * math.sin(a) + z * math.cos(a)
            puntos.append((math.hypot(x, y2), z_elev + z2, n))
        puntos += [(math.hypot(x, y), z_giro + z, n) for (x, y, z), n in rama_giro]
        bajos = [q for q in puntos if q[1] <= ALTURA_CUERPO]
        en_cuerpo = [q for q in bajos if r_op - CAPSULA <= q[0] <= r_op + CAPSULA]
        en_franja = [q for q in bajos if r_op - 30 <= q[0] <= r_op + 30]
        rmax = max(bajos, key=lambda q: q[0]) if bajos else None
        print('elevacion %+3d: vertices que giran bajo z %.0f: %5d | radio max %s | en franja r %.0f+-30: %5d | dentro de la capsula: %5d %s'
              % (grados, ALTURA_CUERPO, len(bajos),
                 '%.1f (z %.1f, %s)' % rmax if rmax else '-', r_op, len(en_franja), len(en_cuerpo),
                 sorted({q[2] for q in en_cuerpo}) if en_cuerpo else ''))
    print('parte fija: z %.1f..%.1f, radio max %.1f'
          % (min(q[0][2] for q in fijo), max(q[0][2] for q in fijo), max(math.hypot(q[0][0], q[0][1]) for q in fijo)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
