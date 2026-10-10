# -*- coding: utf-8 -*-
"""Plataforma de terreno bajo la torre: decodifica, aplana y re-codifica un LAND.

POR QUE EXISTE
--------------
Medido sobre el LAND de la celda 0000963D (Skyrim.esm y Update.esm tienen el MISMO
VHGT), la huella de la torre tiene 120 u (1,7 m) de desnivel: el terreno sube hacia
el NE (+33 u sobre el datum de la torre) y baja hacia el SO (-89 u). Resultado: 5 de
24 pilotes flotan (hasta 48,9 u), el pie de la escalera queda 58 u sobre el suelo.
Bajar toda la torre no sirve (el piso del cuarto bajo la plataforma se enterraria), y
mover la torre solo baja el desnivel de 120 a ~62 u. Por eso se aplana el terreno.

QUE HACE
--------
  1. decodifica VHGT (33x33 alturas, una cada 128 u, resolucion de 8 u);
  2. fija una altura de plataforma (multiplo de 8) en TODOS los vertices de cada
     cuadrante que toque la huella girada: asi cada punto de la huella cae en un
     cuadrante con las 4 esquinas iguales y da lo mismo como triangule el motor;
  3. dos anillos de transicion hacia el terreno original (mezcla 0,5 y 0,25);
  4. re-codifica VHGT y recalcula VNML (normales) de los vertices tocados.

Los bordes de la celda NO se tocan: la huella esta a mas de 1000 u de ellos, asi que
no hay costura con las celdas vecinas.

LO QUE ESTA MEDIDO Y LO QUE NO
------------------------------
Formato de VHGT: float offset + 1089 int8 (deltas) + 3 de relleno. Fila a fila: el
primer delta de cada fila se suma al arrastre de filas, el resto se acumula sobre el
vertice anterior; altura = acumulado * 8. Validado con dos controles que podian
fallar: en el centro de la torre da -4951,8 contra el Z -4952,88 que el usuario leyo
en el juego, y 53 de 62 objetos vanilla de la celda caen a +-60 u de ese terreno.

VNML son 3 int8 con signo, 127 = 1,0. Ninguna formula reproduce las normales
guardadas EXACTAS (el CK las suaviza): la de caras adyacentes queda a 1 de 127 de
mediana y a 11 como maximo sobre el terreno sin tocar. Es sombreado, no colision. Los
vertices aplanados llevan (0, 0, 127) exacto.
"""
import math
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

CELDA_X = 1
CELDA_Y = -4
ORIGEN_X = CELDA_X * 4096.0
ORIGEN_Y = CELDA_Y * 4096.0
PASO = 128.0
N = 33
ESCALA = 8.0

# huella de la torre en su marco local, medida: la torre llega a x -300..400 (con el
# descanso y los pilotes de la escalera) e y -570..300 (la rampa arranca en y -536).
HUELLA_X = (-300.0, 400.0)
HUELLA_Y = (-570.0, 300.0)
MARGEN = 64.0
ANILLOS = (0.5, 0.25)          # mezcla hacia el terreno original, anillo 1 y anillo 2


class ErrorTerreno(Exception):
    pass


# --- VHGT ---------------------------------------------------------------------

def decodificar_vhgt(vhgt):
    """(offset, H[fila][col]) con H en unidades del mundo."""
    if len(vhgt) != 1096:
        raise ErrorTerreno("VHGT de %d bytes, se esperaban 1096" % len(vhgt))
    off, = struct.unpack_from("<f", vhgt, 0)
    ds = struct.unpack_from("<1089b", vhgt, 4)
    h = [[0.0] * N for _ in range(N)]
    arrastre = off
    for r in range(N):
        arrastre += ds[r * N]
        acum = arrastre
        h[r][0] = acum * ESCALA
        for c in range(1, N):
            acum += ds[r * N + c]
            h[r][c] = acum * ESCALA
    return off, h


def codificar_vhgt(h, relleno=b"\0\0\0"):
    """VHGT de 1096 bytes para una rejilla H (en unidades del mundo, multiplos de 8)."""
    enteros = []
    for r in range(N):
        fila = []
        for c in range(N):
            q = h[r][c] / ESCALA
            if abs(q - round(q)) > 1e-6:
                raise ErrorTerreno("altura %.3f en (%d,%d) no es multiplo de %g"
                                   % (h[r][c], r, c, ESCALA))
            fila.append(int(round(q)))
        enteros.append(fila)
    off = float(enteros[0][0])           # el offset es la altura del primer vertice
    deltas = []
    arrastre = off
    for r in range(N):
        d0 = enteros[r][0] - arrastre
        arrastre = enteros[r][0]
        fila = [int(round(d0))]
        for c in range(1, N):
            fila.append(enteros[r][c] - enteros[r][c - 1])
        deltas.extend(fila)
    mal = [d for d in deltas if not -128 <= d <= 127]
    if mal:
        raise ErrorTerreno("delta fuera de int8 (%d..%d): la pendiente no cabe"
                           % (min(mal), max(mal)))
    # primer delta de la fila 0: offset ya incluye esa altura, asi que vale 0
    deltas[0] = 0
    return struct.pack("<f", off) + struct.pack("<1089b", *deltas) + relleno


# --- normales -----------------------------------------------------------------

def _cruz(u, w):
    return (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])


def normal_vertice(h, r, c):
    """Normal (int8 x3) por promedio de las caras adyacentes (diagonal a-d)."""
    def p(rr, cc):
        return (cc * PASO, rr * PASO, h[rr][cc])
    acc = [0.0, 0.0, 0.0]
    for dr in (-1, 0):
        for dc in (-1, 0):
            r0, c0 = r + dr, c + dc
            if 0 <= r0 < N - 1 and 0 <= c0 < N - 1:
                a, b, cc_, d = p(r0, c0), p(r0, c0 + 1), p(r0 + 1, c0), p(r0 + 1, c0 + 1)
                for t in ((a, b, d), (a, d, cc_)):
                    u = tuple(t[1][i] - t[0][i] for i in range(3))
                    w = tuple(t[2][i] - t[0][i] for i in range(3))
                    n = _cruz(u, w)
                    if n[2] < 0:
                        n = tuple(-x for x in n)
                    m = math.sqrt(sum(x * x for x in n))
                    acc = [acc[i] + n[i] / m for i in range(3)]
    m = math.sqrt(sum(x * x for x in acc))
    return tuple(int(round(x / m * 127)) for x in acc)


def decodificar_vnml(vnml):
    return [[struct.unpack_from("<3b", vnml, (r * N + c) * 3) for c in range(N)]
            for r in range(N)]


def codificar_vnml(normales):
    out = bytearray()
    for r in range(N):
        for c in range(N):
            out += struct.pack("<3b", *normales[r][c])
    return bytes(out)


# --- geometria ----------------------------------------------------------------

def interpolar(h, x, y):
    """Altura bilineal en (x, y) del mundo. Aproximacion: el motor triangula."""
    gx = (x - ORIGEN_X) / PASO
    gy = (y - ORIGEN_Y) / PASO
    c = min(N - 2, max(0, int(gx)))
    r = min(N - 2, max(0, int(gy)))
    fx, fy = gx - c, gy - r
    return (h[r][c] * (1 - fx) * (1 - fy) + h[r][c + 1] * fx * (1 - fy)
            + h[r + 1][c] * (1 - fx) * fy + h[r + 1][c + 1] * fx * fy)


def a_local(mundo, x, y):
    """(lx, ly) de un punto del mundo en el marco de la torre (inversa de la rotacion)."""
    import mundo_v11 as M
    r = M.matriz_colocacion(mundo)["r"]
    dx, dy = x - mundo["x"], y - mundo["y"]
    return (r[0][0] * dx + r[1][0] * dy, r[0][1] * dx + r[1][1] * dy)


def en_huella(lx, ly, margen=0.0):
    return (HUELLA_X[0] - margen <= lx <= HUELLA_X[1] + margen
            and HUELLA_Y[0] - margen <= ly <= HUELLA_Y[1] + margen)


def distancia_a_huella(lx, ly):
    """Distancia (marco local) de un punto al rectangulo de la huella; 0 si esta dentro."""
    dx = max(HUELLA_X[0] - lx, 0.0, lx - HUELLA_X[1])
    dy = max(HUELLA_Y[0] - ly, 0.0, ly - HUELLA_Y[1])
    return math.hypot(dx, dy)


def _cuadrante_toca_huella(mundo, r, c):
    """Un cuadrante (r, c) toca la huella si alguna de sus esquinas, de sus puntos
    intermedios o algun punto de la huella cae dentro de el. Se muestrea fino: el
    cuadrante mide 128 u y la huella 700 x 870."""
    x0 = ORIGEN_X + c * PASO
    y0 = ORIGEN_Y + r * PASO
    pasos = 8
    for i in range(pasos + 1):
        for j in range(pasos + 1):
            lx, ly = a_local(mundo, x0 + PASO * i / pasos, y0 + PASO * j / pasos)
            if en_huella(lx, ly, MARGEN):
                return True
    # huella mas chica que el cuadrante: sus esquinas dentro del cuadrante
    return False


def vertices_a_aplanar(mundo):
    """Conjunto de (r, c): las 4 esquinas de cada cuadrante que toca la huella."""
    fijos = set()
    for r in range(N - 1):
        for c in range(N - 1):
            if _cuadrante_toca_huella(mundo, r, c):
                fijos.update({(r, c), (r, c + 1), (r + 1, c), (r + 1, c + 1)})
    return fijos


def vecinos(r, c):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if (dr or dc) and 0 <= r + dr < N and 0 <= c + dc < N:
                yield r + dr, c + dc


def cuantizar(z):
    return round(z / ESCALA) * ESCALA


def altura_plataforma(mundo):
    """Multiplo de 8 mas cercano al Z de la torre (la diferencia se absorbe)."""
    return cuantizar(mundo["z"])


def aplanar(h, mundo, z_plataforma=None):
    """Devuelve (h_nuevo, fijos, anillos) con la plataforma aplicada."""
    zp = altura_plataforma(mundo) if z_plataforma is None else z_plataforma
    fijos = vertices_a_aplanar(mundo)
    if not fijos:
        raise ErrorTerreno("la huella no toca ningun cuadrante: coordenadas del mundo mal")
    borde = [(r, c) for r, c in fijos if r in (0, N - 1) or c in (0, N - 1)]
    if borde:
        raise ErrorTerreno("la plataforma llega al borde de la celda en %s: habria costura "
                           "con la celda vecina" % borde[:3])
    nuevo = [fila[:] for fila in h]
    for r, c in fijos:
        nuevo[r][c] = zp
    hecho = set(fijos)
    anillos = []
    frente = set(fijos)
    for mezcla in ANILLOS:
        siguiente = set()
        for r, c in frente:
            for q in vecinos(r, c):
                if q not in hecho:
                    siguiente.add(q)
        for r, c in siguiente:
            nuevo[r][c] = cuantizar(mezcla * zp + (1 - mezcla) * h[r][c])
        borde = [(r, c) for r, c in siguiente if r in (0, N - 1) or c in (0, N - 1)]
        if borde:
            raise ErrorTerreno("un anillo llega al borde de la celda en %s" % borde[:3])
        hecho |= siguiente
        anillos.append(siguiente)
        frente = siguiente
    return nuevo, fijos, anillos


def aplicar_a_land(sub, mundo, z_plataforma=None):
    """`sub` es el dict de subrecords de un LAND (nombre -> bytes). Devuelve
    (dict nuevo, informe). Solo cambian VHGT y VNML; el resto queda igual."""
    off, h = decodificar_vhgt(sub["VHGT"])
    nuevo, fijos, anillos = aplanar(h, mundo, z_plataforma)
    normales = decodificar_vnml(sub["VNML"])
    tocados = set(fijos)
    for a in anillos:
        tocados |= a
    # las normales de un vertice dependen de sus vecinos: se recalculan los tocados y
    # sus vecinos inmediatos
    recalcular = set(tocados)
    for r, c in tocados:
        recalcular.update(vecinos(r, c))
    # La fila/columna del borde se comparte con la celda vecina y su normal guardada
    # incluye las caras del otro lado: recalcularla solo con esta celda crearia una
    # costura de iluminacion. Sus alturas no cambian, asi que su normal se conserva.
    recalcular = {(r, c) for r, c in recalcular
                  if 0 < r < N - 1 and 0 < c < N - 1}
    for r, c in recalcular:
        if (r, c) in fijos:
            normales[r][c] = (0, 0, 127)
        else:
            normales[r][c] = normal_vertice(nuevo, r, c)
    salida = dict(sub)
    salida["VHGT"] = codificar_vhgt(nuevo, sub["VHGT"][-3:])
    salida["VNML"] = codificar_vnml(normales)
    informe = {"z_plataforma": altura_plataforma(mundo) if z_plataforma is None
               else z_plataforma,
               "vertices_planos": len(fijos),
               "vertices_anillo": [len(a) for a in anillos],
               "cambio_max": max(abs(nuevo[r][c] - h[r][c])
                                 for r in range(N) for c in range(N)),
               "vertices_cambiados": sum(1 for r in range(N) for c in range(N)
                                         if nuevo[r][c] != h[r][c])}
    return salida, informe


# --- medicion de la huella ------------------------------------------------------

def medir(h, mundo, pilotes, pie_escalera=(323.4, -536.0), z_torre=None):
    """Huecos de la torre contra el terreno h.

    pilotes: [(lx, ly, bottom_z_local)]. hueco = base_en_mundo - terreno: positivo =
    el pilote flota, negativo = enterrado. Devuelve un dict con las cifras que importan.
    """
    import mundo_v11 as M
    import v11_layout as L
    z0 = mundo["z"] if z_torre is None else z_torre
    col = M.matriz_colocacion(mundo)

    def terreno(lx, ly):
        p = L.apply(col, (lx, ly, 0.0))
        return interpolar(h, p[0], p[1])

    huecos = [(z0 + bz) - terreno(lx, ly) for lx, ly, bz in pilotes]
    pie = z0 - terreno(*pie_escalera)
    zs = [terreno(lx, ly) for lx in range(int(HUELLA_X[0]), int(HUELLA_X[1]) + 1, 25)
          for ly in range(int(HUELLA_Y[0]), int(HUELLA_Y[1]) + 1, 25)]
    return {"pilotes_que_flotan": sum(1 for g in huecos if g > 1.0),
            "hueco_max": max(huecos),
            "pie_escalera_sobre_suelo": pie,
            "relieve_huella": max(zs) - min(zs)}
