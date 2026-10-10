# -*- coding: utf-8 -*-
"""Lleva el layout local de la torre v11 a coordenadas de mundo.

POR QUE EXISTE
--------------
La torre esta modelada y verificada con su origen en (0,0,0), que es el datum de
suelo (la primera rampa arranca exactamente ahi). Para ponerla en el mundo hay que
componer la colocacion con el layout local de cada pieza. La composicion NO se hace
girando los angulos: girar angulos no es componer rotaciones cuando hay mas de un eje
con rotacion. Se componen matrices y se vuelve a extraer euler al final, que es lo
unico que el motor sabe leer de un REFR.

DONDE ESTA EL SIGNO DEL 43.15
-----------------------------
La convencion del repo esta MEDIDA, no supuesta: reports/angle_convention.json dice
order='ZYX', signs=(-1,-1,-1), con 1707 pares de REFR vanilla reales. O sea que un
rot_deg de motor 'z' produce una rotacion matematica de -z. Por eso el 43.15 que da
el usuario, si viene del juego/CK, se pasa por la MISMA convencion y sale una
rotacion matematica de -43.15. El numero vive en un solo lugar (config, campo
mundo.rot_z_deg) y se cambia de signo ahi si la torre queda mirando al reves. No
esta duplicado en ningun archivo mas, justamente para que no haya dos verdades.

AUTOCOMPROBACION
----------------
Con --autotest el modulo se verifica a si mismo antes de usarse:
  - identidad: con rot 0 y pos 0, la pieza sale igual que entra
  - composicionKnown: rotar dos veces 90 sobre Z = 180, no 90
  - derecha: una pieza en +X local sale en +Y con rot_z=90 de motor
Si algo de eso falla, aborta. Un modulo de transformacion que no puede fallar no
prueba nada.
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import v11_layout as L  # noqa: E402

CONFIG = ROOT / "config.json"


def cargar_colocacion(ruta=CONFIG):
    cfg = json.loads(ruta.read_text(encoding="utf-8"))
    mundo = cfg["tower_v11"]["mundo"]
    return mundo


def matriz_colocacion(mundo):
    """Matriz de colocacion de la torre, con la convencion del repo."""
    return L.transform_matrix((mundo["x"], mundo["y"], mundo["z"]),
                              (0.0, 0.0, mundo["rot_z_deg"]), 1.0,
                              *L.engine_convention())


def _mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)]
            for i in range(3)]


def llevar(pieza, mundo=None):
    """(pos_mundo, rot_deg_mundo) de una pieza del layout local.

    pos_mundo   = t_colocacion + R_colocacion * (escala * pos_local)
    R_mundo     = R_colocacion * R_local
    rot_mundo   = euler_from_matrix(R_mundo)   -> angulos de motor otra vez
    """
    mundo = mundo if mundo is not None else cargar_colocacion()
    col = matriz_colocacion(mundo)
    loc = L.piece_matrix(pieza)
    r = _mul(col["r"], loc["r"])
    t = col["t"]
    p = L.apply(col, pieza["pos"])
    return p, L.euler_from_matrix(r)


def torre_principal(mundo=None):
    """La torre y la ballista, que no son piezas del layout: van enteras al mundo."""
    mundo = mundo if mundo is not None else cargar_colocacion()
    col = matriz_colocacion(mundo)
    return [(mundo["x"], mundo["y"], mundo["z"]), (0.0, 0.0, mundo["rot_z_deg"])]


def autotest():
    fallo = []

    def chk(nombre, cond, detalle=""):
        print("  %-46s %s%s" % (nombre, "OK" if cond else "FALLA",
                                "" if cond else "  <- " + detalle))
        if not cond:
            fallo.append(nombre)

    print("AUTOTEST de mundo_v11")

    # 1. identidad: sin giro ni traslacion, la pieza no se mueve
    mundo0 = {"x": 0.0, "y": 0.0, "z": 0.0, "rot_z_deg": 0.0}
    pieza = {"pos": [-263.774, -264.028, 207.519],
             "rot_deg": [-89.2672, 24.405, 0.5039], "scale": 1.0}
    p, r = llevar(pieza, mundo0)
    chk("identidad: posicion intacta",
        max(abs(a - b) for a, b in zip(p, pieza["pos"])) < 1e-6, str(p))
    chk("identidad: angulos intactos",
        max(abs(a - b) for a, b in zip(r, pieza["rot_deg"])) < 1e-6, str(r))

    # 2. traslacion pura mueve por el offset y no cambia los angulos
    mundoT = {"x": 1000.0, "y": -2000.0, "z": -4952.88, "rot_z_deg": 0.0}
    p2, r2 = llevar(pieza, mundoT)
    chk("traslacion pura: +offset exacto",
        max(abs((a - b) - c) for a, b, c in
            zip(p2, pieza["pos"], (1000.0, -2000.0, -4952.88))) < 1e-6, str(p2))
    chk("traslacion pura: angulos intactos",
        max(abs(a - b) for a, b in zip(r2, pieza["rot_deg"])) < 1e-6, str(r2))

    # 3. DOS giros de 90 tienen que dar 180, no 90. Si esto pasa, se estan
    #    composing angulos en vez de matrices, que es el error clasico.
    #    Se compara el ANGULO (envuelto a 360), no el signo literal: con la
    #    convencion del repo el signo de la salida depende de atan2 y no es
    #    lo que se esta probando. Comparar el signo seria un control que
    #    puede fallar por la rama de atan2 y no por la composicion.
    def dif_ang(a, b):
        return abs(((a - b) + 180.0) % 360.0 - 180.0)

    a = {"pos": (0, 0, 0), "rot_deg": (0, 0, 0), "scale": 1.0}
    b = {"pos": (0, 0, 0), "rot_deg": (0, 0, 90.0), "scale": 1.0}
    m90 = {"r": matriz_colocacion({"x": 0, "y": 0, "z": 0, "rot_z_deg": 90.0})["r"],
           "t": (0, 0, 0), "s": 1.0}
    mb = L.piece_matrix(b)
    rcomp = _mul(m90["r"], mb["r"])
    chk("composicion de matrices: 90+90 = 180",
        dif_ang(L.euler_from_matrix(rcomp)[2], 180.0) < 1e-6,
        str(L.euler_from_matrix(rcomp)))

    # 3b. control NEGATIVO del 3: con dos ejes y Z=0, sumar angulos Y componer
    #     matrices dan lo MISMO, porque en orden ZYX con c=0 la descomposicion es
    #     exacta. Ese caso no puede fallar, asi que no prueba nada. El primer caso
    #     de la serie (X luego Y)，结果 si se puede expresar como (90,0,90), o
    #     sea que tampoco distingue. Lo que si distingue es una rotacion de los
    #     TRES ejes componida consigo misma: ahi sumar duplica cada angulo y el
    #     orden de aplicacion se pierde.
    ang = (30.0, 40.0, 50.0)
    ra = L.transform_matrix((0, 0, 0), ang, 1.0, *L.engine_convention())
    r2 = _mul(ra["r"], ra["r"])
    rsum = L.transform_matrix((0, 0, 0), (2 * ang[0], 2 * ang[1], 2 * ang[2]),
                              1.0, *L.engine_convention())["r"]
    chk("control NEGATIVO: componer != sumar angulos",
        max(abs(r2[i][j] - rsum[i][j]) for i in range(3) for j in range(3)) > 1e-6,
        "las dos matrices salieron iguales: este control no distinguiria nada")
    ex2, ey2, ez2 = L.euler_from_matrix(r2)
    r_ida = L.transform_matrix((0, 0, 0), (ex2, ey2, ez2), 1.0, *L.engine_convention())["r"]
    chk("ida y vuelta: euler(compuesta) reconstruye la misma matriz",
        max(abs(r_ida[i][j] - r2[i][j]) for i in range(3) for j in range(3)) < 1e-9,
        "(%.2f, %.2f, %.2f)" % (ex2, ey2, ez2))
    exa, eya, eza = L.euler_from_matrix(ra["r"])
    chk("y la original vuelve a (30, 40, 50)",
        dif_ang(exa, 30.0) < 1e-6 and dif_ang(eya, 40.0) < 1e-6
        and dif_ang(eza, 50.0) < 1e-6, "(%.2f, %.2f, %.2f)" % (exa, eya, eza))

    # 4. mano: con rot_z de motor +90, el eje +X local debe caer en -Y del mundo.
    #    El signo NO se supone: sale de la convencion medida del repo.
    conv_z = L.engine_convention()[1][2]
    mundoR = {"x": 0, "y": 0, "z": 0, "rot_z_deg": 90.0}
    col = matriz_colocacion(mundoR)
    eje = L.apply(col, (1.0, 0.0, 0.0))
    esperado = (0.0, -1.0, 0.0) if conv_z < 0 else (0.0, 1.0, 0.0)
    chk("rot_z=90 manda +X local a %s" % (esperado,),
        max(abs(x - y) for x, y in zip(eje, esperado)) < 1e-9, str(eje))

    # 5. el radio de la base sobrevive a la rotacion: distancia al centro constante
    r0 = math.hypot(pieza["pos"][0], pieza["pos"][1])
    mundo43 = {"x": 6068.65, "y": -13188.53, "z": -4952.88, "rot_z_deg": 43.15}
    p3, _ = llevar(pieza, mundo43)
    r3 = math.hypot(p3[0] - 6068.65, p3[1] + 13188.53)
    chk("radio al centro conservado (%.3f vs %.3f)" % (r0, r3),
        abs(r0 - r3) < 1e-6, "")

    # 6. los 64 REFR reales del layout entran todos sin excepcion
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    piezas = cfg["tower_v11"]["pieces"]
    fuera = [llevar(x, mundo43) for x in piezas]

    # 6a. una rotacion SOLO sobre Z no puede mover nada en Z. Es la propiedad
    #     mas fuerte y mas facil de untrue: si se rompe, se mezclaron ejes.
    dz = max(abs((p[2] - mundo43["z"]) - x["pos"][2])
             for x, (p, _r) in zip(piezas, fuera))
    chk("rotacion sobre Z no altera la altura de NINGUNA pieza", dz < 1e-6, "%.6f" % dz)

    # 6b. TODO tiene que caer dentro del chunk (1,-4) = [4096,8192] x [-16384,-12288].
    #     Si una pieza se sale, la celda no la carga y desaparece en el juego.
    cx0, cx1 = 4096.0, 8192.0
    cy0, cy1 = -16384.0, -12288.0
    fuera_chunk = [p for p, _ in fuera
                   if not (cx0 <= p[0] <= cx1 and cy0 <= p[1] <= cy1)]
    chk("las %d piezas caen dentro del chunk (1,-4)" % len(piezas),
        not fuera_chunk, "fuera: %s" % fuera_chunk[:3])

    # 6c. altura sobre el suelo del sitio, informado como DATO. El layout son
    #     las piezas vanilla; la copa de la torre (559.5 segun torre.nif) es
    #     del mesh, no del layout, asi que no se puede exigir aqui.
    loc_z = [x["pos"][2] for x in piezas]
    print("  %-46s Z local %.1f .. %.1f  (medida del layout)"
          % ("altura del layout sobre el datum local:", min(loc_z), max(loc_z)))
    chk("el layout no se hunde mas de 100 u bajo el datum",
        min(loc_z) > -100.0, "min local = %.1f" % min(loc_z))

    # 7. los 5 escudos tambien, porque comparten el mismo giro
    esc = cfg["tower_v11"]["escudos"]
    esc_mundo = [llevar({"pos": e["pos"], "rot_deg": e["rot_deg"],
                         "scale": e.get("escala", 1.0)}, mundo43) for e in esc["items"]]
    fuera_esc = [p for p, _ in esc_mundo
                 if not (cx0 <= p[0] <= cx1 and cy0 <= p[1] <= cy1)]
    chk("los %d escudos caen dentro del chunk (1,-4)" % len(esc["items"]),
        not fuera_esc, "fuera: %s" % fuera_esc[:3])
    # Lo que importa del escudo no es su distancia AL CENTRO sino a la BARANDA:
    # N1 y N2 estan en el lado norte con x desfasado, asi que su radio al centro es
    # 329.7 y el "303" de config es la distancia perpendicular a la cara.
    #
    # Y se mide EN MARCO LOCAL, no en mundo: rotar y trasladar es rigido, asi que
    # la distancia a la baranda es la misma en los dos marcos. Medirla en mundo
    # con la direccion local sin rotarla mezcla marcos y da numeros sin sentido
    # (daba -165 para un escudo que esta exactamente a la misma distancia que
    # los demas). El autotest lo delata porque solo tres de cinco coincidian.
    #   distancia = |centro . mirar| - 297.4   (297.4 = cara exterior medida)
    #   half_grosor = 5.3 (Z local -8.52..2.06 de Armor\Iron\Shield.nif)
    CARA_BARANDA = 297.4
    HALF_GROSOR = 5.3
    fuera = []
    for e in esc["items"]:
        px, py, _pz = e["pos"]
        mx, my = e["mirar"]
        fuera.append((e["nombre"], abs(px * mx + py * my) - CARA_BARANDA))
    chk("los 5 escudos a la misma distancia de la cara (%s)"
        % ", ".join("%s %.1f" % (n, d) for n, d in fuera),
        max(d for _n, d in fuera) - min(d for _n, d in fuera) < 1.0,
        "estan escalonados respecto de la baranda")
    chk("los 5 escudos quedan por FUERA de la baranda",
        all(d > 0 for _n, d in fuera), str(fuera))
    chk("y pegados a ella, sin hundirse ni flotar (%.1f..%.1f de holgura)"
        % (min(d for _n, d in fuera) - HALF_GROSOR,
           max(d for _n, d in fuera) + HALF_GROSOR),
        all(d - HALF_GROSOR > 0 for _n, d in fuera)
        and all(d + HALF_GROSOR < 25.0 for _n, d in fuera), str(fuera))

    print("  %d fallos" % len(fallo))
    return 0 if not fallo else 1


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) > 1 and sys.argv[1] == "--autotest":
        return autotest()
    mundo = cargar_colocacion()
    print("colocacion:", json.dumps(mundo, ensure_ascii=False))
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    piezas = cfg["tower_v11"]["pieces"]
    print("primeras 5 piezas llevadas al mundo:")
    for x in piezas[:5]:
        p, r = llevar(x, mundo)
        print("  %-22s pos=(%.1f, %.1f, %.1f) rot=(%.2f, %.2f, %.2f)"
              % (x["name"], p[0], p[1], p[2], r[0], r[1], r[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())