# -*- coding: utf-8 -*-
"""v22: baja la torreta de `ballesta.nif` parcheando BYTES, sin reexportar.

Por que no se reexporta con PyNifly: medido en el workspace de la bajada
(`probar_roundtrip.py`), el round-trip pierde nodos vacios
(`AstraBallesta:ROOT`, `AstraSightCameraNode`, `BSXFlags:BSX`, `OperatorNode`,
`ProjectileNode`), gana un `Scene Root:ROOT` y reemparenta TODAS las mallas. El
contrato de Papyrus lee `ProjectileNode` y `AstraSightCameraNode` por nombre en
runtime; perderlos rompe el disparo. Ademas el round-trip es silencioso: no da
error, solo un archivo distinto. Por eso se parchea el binario y se verifica el
resultado contra el original.

Es el productor EXACTO del `ballesta.nif` del paquete v22: sobre el NIF v21
(`sha256 bcee401b...`) da `sha256 ebe715e7...`. `build_assets.py` NO debe
reconstruir este NIF para la bajada (reconstruye la torre y el virote tambien, y
su torre no coincide con la embarcada); este script toca un solo archivo.

QUE HACE, y por que asi:

1) `CTRL_GIRO_360` baja DELTA unidades (traslacion pura del nodo). Eso arrastra
   toda la torreta: `CTRL_ELEVACION`, los brazos, la cuerda, el virote, la mira,
   `ProjectileNode` y el collar `CTRL_GIRO_360_metal`. Una traslacion de nodo no
   toca las normales de las mallas: es la operacion mas segura que hay.

2) El pedestal (`AstraBallesta_floor/metal/wood`) NO cuelga de `CTRL_GIRO_360`:
   cuelga de la raiz (verificado con `arbol_completo.py`). Por eso bajarlo es una
   operacion INDEPENDIENTE y no hay doble conteo. Se aplasta en Z con
   z' = Z0 + (z-Z0)*K para z > Z0.

   K = 1 - DELTA/(TOPE-Z0), de modo que la cota mas alta del pedestal baja
   EXACTAMENTE DELTA -- la misma cantidad que la torreta. Asi el apoyo
   poste/torreta queda igual que estaba (el poste sobresale 2.1 u por encima del
   pivote, antes y despues). Por debajo de Z0 no se toca nada: la base sigue
   apoyada donde estaba, sin abrir luces contra la plataforma.

3) Las normales NO se corrigen, a proposito. Medido (`probe_layout_vertice.py`):
   la normal no esta ni como triple float ni como 3 int8 en ningun offset de los
   32 bytes del vertice. Corregir un campo cuya ubicacion no se pudo determinar
   es como se rompe un asset que funcionaba. El error que queda es de sombreado y
   solo en caras oblicuas: un aplastado en Z deja las normales horizontales
   (paredes, que son la mayoria) y las verticales (tapas) EXACTAMENTE iguales;
   solo los biseles se desvian, ~10 grados con K=0.694. En un pedestal de pocos
   poligonos es imperceptible.

`DELTA` y `Z0` salen de `config.json` (`turret_drop_units` y
`turret_drop_base_units`); `TOPE` se mide de los bytes. Todas las verificaciones
son fallas duras: si alguna no se cumple, no se escribe nada. Un parche que corre
y mueve los vertices equivocados es peor que un parche que no corre.

Uso:  python scripts/bajar_ballesta.py <entrada.nif> <salida.nif> [--seco]
"""
import json
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts", "vendor"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import nif_nodos  # noqa: E402

CFG = json.loads(open(os.path.join(ROOT, "config.json")).read())

# --- parametros de la bajada -------------------------------------------------
# NO aplicada en el repo: `reports/sight_path_v22_FAILED.json` mide que la
# bajada rompe el contrato de camara de v10 (holgura cabeza->camara 29.8 -> 10.0,
# camara->malla del arma 10.3 -> 2.9 con la esfera del motor en 12-15 u, y pierde
# `near_plane_check_falsified`). Por eso `config.json` vuelve al pivote 153 y
# estas dos claves no estan. El script las lee con default para poder reaplicar
# la bajada cuando se rediseñe la camara.
DELTA = float(CFG.get("turret_drop_units", 36.0))       # 36.0 u: manos 6.6 u bajo el hombro
Z0 = float(CFG.get("turret_drop_base_units", 20.0))     # 20.0: por debajo no se toca
# TOPE: cota mas alta del pedestal en el NIF v21, el poste AstraBallesta_wood.
# Es el valor DOCUMENTADO (2 decimales) y el que fija K en el NIF embarcado del
# paquete v22 (sha256 ebe715e7...). Medirlo con precision de float32 da
# 137.59998321533203; usarlo cambiaria K en ~1e-7 y por tanto los bytes de los
# vertices. Se usa el valor documentado y se comprueba que coincide con el
# medido (tolerancia 0.01 u).
TOPE = 137.60

NODO_BAJADO = "CTRL_GIRO_360"
# z de CTRL_GIRO_360 en el NIF v21 sin parchear. Es la referencia contra la que
# el script se autoprotege de correr dos veces (36+36=72 u de bajada).
Z_GIRO_V21 = 135.5
MALLAS_PEDESTAL = ("AstraBallesta_floor", "AstraBallesta_metal",
                   "AstraBallesta_wood")

# Layout del BSTriShape, MEDIDO (probe_layout_vertice.py):
#   numTriangles  u16 en off+108
#   numVertices   u16 en off+110
#   dataSize      u32 en off+112  (= nv*32 + nt*6)
#   vertices      en off+116, stride 32, primeros 12 bytes = 3 float32 XYZ
OFF_NUM_TRI = 108
OFF_NUM_VERT = 110
OFF_DATA_SIZE = 112
OFF_VERTICES = 116
STRIDE = 32


def nombre_bloque(nif, b):
    off = nif["bloques"][b][1]
    i, = struct.unpack_from("<i", nif["datos"], off)
    s = nif["strings"]
    return s[i] if 0 <= i < len(s) else "?"


def off_traslacion(datos, off):
    """Offset de los 3 float de traslacion de un NiNode."""
    p = off + 4                                     # name
    n_ed, = struct.unpack_from("<I", datos, p)
    p += 4 + 4 * n_ed                               # extraData[]
    p += 4                                          # controller
    p += 4                                          # flags
    return p


def indice_de_nodo(nif, nombre):
    for b in nif["nodos"]:
        if nif["nodos"][b]["nombre"] == nombre:
            return b
    return None


def descendientes(nif, raiz):
    """Todos los bloques alcanzables desde `raiz`, nodos y mallas."""
    vistos, cola = set(), [raiz]
    while cola:
        b = cola.pop()
        if b in vistos:
            continue
        vistos.add(b)
        n = nif["nodos"].get(b)
        if n:
            cola.extend(h for h in n["hijos"] if 0 <= h < nif["n_bloques"])
    return vistos


def bbox_vertices(datos, off, nv):
    xs, ys, zs = [], [], []
    for i in range(nv):
        x, y, z = struct.unpack_from("<3f", datos, off + OFF_VERTICES
                                     + STRIDE * i)
        xs.append(x); ys.append(y); zs.append(z)
    return (min(xs), max(xs)), (min(ys), max(ys)), (min(zs), max(zs))


def bloques_pedestal(nif):
    out = {}
    for b, (tipo, _o, _s) in enumerate(nif["bloques"]):
        if tipo == "BSTriShape" and nombre_bloque(nif, b) in MALLAS_PEDESTAL:
            out.setdefault(nombre_bloque(nif, b), []).append(b)
    return out


def validar_layout(datos, off, tam, nombre):
    """Falla si el bloque no tiene el layout medido. Devuelve (nt, nv)."""
    nt, = struct.unpack_from("<H", datos, off + OFF_NUM_TRI)
    nv, = struct.unpack_from("<H", datos, off + OFF_NUM_VERT)
    ds, = struct.unpack_from("<I", datos, off + OFF_DATA_SIZE)
    if ds != nv * STRIDE + nt * 6:
        raise SystemExit(
            "LAYOUT INESPERADO en %s: dataSize=%d pero nv*32+nt*6=%d"
            % (nombre, ds, nv * STRIDE + nt * 6))
    if ds != tam - OFF_VERTICES:
        if tam - ds not in (OFF_VERTICES, OFF_VERTICES + 4):
            raise SystemExit(
                "LAYOUT INESPERADO en %s: tam=%d, dataSize=%d (esperado %d o %d)"
                % (nombre, tam, ds, OFF_VERTICES + ds, OFF_VERTICES + 4 + ds))
    # Prueba fuerte e independiente de toda constante: los indices de triangulo
    # tienen que apuntar a vertices que existen.
    ini_idx = off + OFF_VERTICES + STRIDE * nv
    if ini_idx + 6 * nt > off + tam:
        raise SystemExit(
            "LAYOUT INESPERADO en %s: los indices se salen del bloque" % nombre)
    idx = struct.unpack_from("<%dH" % (3 * nt), datos, ini_idx)
    malos = [v for v in idx if v >= nv]
    if malos:
        raise SystemExit(
            "LAYOUT INESPERADO en %s: %d indices >= nv=%d (primeros: %s)"
            % (nombre, len(malos), nv, malos[:5]))
    return nt, nv


def bajar(ruta_entrada, ruta_salida, seco=False):
    nif = nif_nodos.leer(ruta_entrada)
    datos = bytearray(nif["datos"])
    print("=== %s  (%d bytes, %d bloques)"
          % (os.path.basename(ruta_entrada), len(datos), nif["n_bloques"]))

    # --- 0. comprobacion estructural: el pedestal NO cuelga del giro ---------
    b_giro = indice_de_nodo(nif, NODO_BAJADO)
    if b_giro is None:
        raise SystemExit("no encontre el nodo %s" % NODO_BAJADO)
    debajo_del_giro = descendientes(nif, b_giro)
    ped = bloques_pedestal(nif)
    for nombre in MALLAS_PEDESTAL:
        for b in ped.get(nombre, []):
            if b in debajo_del_giro:
                raise SystemExit(
                    "ESTRUCTURA INESPERADA: %s cuelga de %s. Bajarlo ademas "
                    "del nodo seria contar la bajada dos veces."
                    % (nombre, NODO_BAJADO))
    print("    [ok] el pedestal no cuelga de %s: no hay doble bajada"
          % NODO_BAJADO)

    # TOPE es constante (ver arriba); se comprueba contra el medido en los bytes.
    tope_medido = max(bbox_vertices(datos, nif["bloques"][b][1],
                                    validar_layout(datos, nif["bloques"][b][1],
                                                    nif["bloques"][b][2], nombre)[1])[2][1]
                      for nombre in MALLAS_PEDESTAL for b in ped.get(nombre, []))
    if abs(tope_medido - TOPE) > 0.01:
        raise SystemExit("TOPE medido %.4f != documentado %.2f"
                         % (tope_medido, TOPE))
    K = 1.0 - DELTA / (TOPE - Z0)
    print("    DELTA=%.2f u   Z0=%.1f   TOPE=%.2f (medido %.4f)   K=%.6f"
          % (DELTA, Z0, TOPE, tope_medido, K))
    print("")

    # --- 1. nodo CTRL_GIRO_360 ---------------------------------------------
    tipo, off_giro, tam_giro = nif["bloques"][b_giro]
    p_tr = off_traslacion(datos, off_giro)
    tx, ty, tz = struct.unpack_from("<3f", datos, p_tr)
    print("    [1] %s  traslacion (%8.3f, %8.3f, %8.3f)"
          % (NODO_BAJADO, tx, ty, tz))
    if abs(tz - (Z_GIRO_V21 - DELTA)) < 0.01:
        raise SystemExit(
            "PARECE YA PARCHEADO: la traslacion ya es z=%.3f. Correrlo dos "
            "veces bajaria la ballesta %.0f u. Se aborta."
            % (tz, 2 * DELTA))
    if abs(tz - Z_GIRO_V21) > 0.01:
        raise SystemExit(
            "TRASLACION INESPERADA: z=%.3f, se esperaba %.1f. El archivo no es "
            "el que se midio; revisar antes de parchear." % (tz, Z_GIRO_V21))
    struct.pack_into("<3f", datos, p_tr, tx, ty, tz - DELTA)
    print("        ->      (%8.3f, %8.3f, %8.3f)   (z - %.1f)"
          % (tx, ty, tz - DELTA, DELTA))

    # --- 2. pedestal: aplastado en Z ---------------------------------------
    print("")
    for nombre in MALLAS_PEDESTAL:
        bloques = ped.get(nombre, [])
        if len(bloques) != 1:
            raise SystemExit("esperaba 1 bloque BSTriShape llamado %s, hay %d"
                             % (nombre, len(bloques)))
        b = bloques[0]
        _t, off, tam = nif["bloques"][b]
        nt, nv = validar_layout(datos, off, tam, nombre)
        (x0, x1), (y0, y1), (z0, z1) = bbox_vertices(datos, off, nv)
        print("    [2] %-22s nv=%-5d nt=%-5d  z antes [%8.3f, %8.3f]"
              % (nombre, nv, nt, z0, z1))

        movidos = 0
        for i in range(nv):
            pz = off + OFF_VERTICES + STRIDE * i + 8
            z, = struct.unpack_from("<f", datos, pz)
            if z > Z0:
                struct.pack_into("<f", datos, pz, Z0 + (z - Z0) * K)
                movidos += 1
        (x0b, x1b), (y0b, y1b), (z0b, z1b) = bbox_vertices(datos, off, nv)
        print("        ->   %-5d vertices movidos de %d.  z despues "
              "[%8.3f, %8.3f]" % (movidos, nv, z0b, z1b))
        print("             x [%8.3f, %8.3f] sin cambios: %s"
              % (x0b, x1b, abs(x0b - x0) < 1e-6 and abs(x1b - x1) < 1e-6))
        print("             y [%8.3f, %8.3f] sin cambios: %s"
              % (y0b, y1b, abs(y0b - y0) < 1e-6 and abs(y1b - y1) < 1e-6))
        if abs(z0 - z0b) > 1e-6:
            raise SystemExit("  el fondo del pedestal se movio: no deberia")
        # Solo el elemento MAS ALTO baja DELTA exactos: es la definicion de K.
        esperado = Z0 + (z1 - Z0) * K
        if abs(z1b - esperado) > 0.02:
            raise SystemExit(
                "  la cota superior no sigue la afinidad: %.3f -> %.3f "
                "(esperado %.3f)" % (z1, z1b, esperado))
        if abs(z1 - TOPE) < 0.01 and abs((z1 - z1b) - DELTA) > 0.02:
            raise SystemExit(
                "  el elemento mas alto no bajo DELTA: %.3f -> %.3f"
                % (z1, z1b))

    # --- 3. escribir y RELEER ---------------------------------------------
    print("")
    if seco:
        print("    [3] modo seco: no se escribio nada")
        return len(datos)
    with open(ruta_salida, "wb") as fh:
        fh.write(bytes(datos))
    print("    [3] escrito %s (%d bytes)" % (os.path.basename(ruta_salida),
                                             len(datos)))

    # La verificacion relee el archivo del disco. Comprobar el bytearray en
    # memoria diria que el parche se armo bien, no que se guardo bien.
    v = nif_nodos.leer(ruta_salida)
    if v["n_bloques"] != nif["n_bloques"]:
        raise SystemExit("se perdieron bloques: %d -> %d"
                         % (nif["n_bloques"], v["n_bloques"]))
    pos_a, _ = nif_nodos.mundo(nif)
    pos_b, _ = nif_nodos.mundo(v)
    if set(pos_a) != set(pos_b):
        raise SystemExit("cambio la lista de nodos:\n  solo en original: %s\n"
                         "  solo en parcheado: %s"
                         % (sorted(set(pos_a) - set(pos_b)),
                            sorted(set(pos_b) - set(pos_a))))
    print("        nodos: %d (los mismos nombres)" % len(pos_b))
    print("")
    print("    %-26s %12s %12s %10s" % ("nodo", "z antes", "z despues",
                                        "delta"))
    esperados = {
        NODO_BAJADO: DELTA,
        "CTRL_ELEVACION": DELTA,
        "ProjectileNode": DELTA,
        "AstraSightCameraNode": DELTA,
        "AstraSightFrontPost": DELTA,
        "Cuerda_I": DELTA, "Cuerda_D": DELTA,
        "CTRL_BRAZO_I": DELTA, "CTRL_BRAZO_D": DELTA,
        "VIROTE_VISUAL": DELTA,
        "AstraBallesta": 0.0,
        "OperatorNode": 0.0,
    }
    for nombre in sorted(esperados, key=lambda n: -pos_b[n][2]):
        za, zb = pos_a[nombre][2], pos_b[nombre][2]
        d = za - zb
        marca = "" if abs(d - esperados[nombre]) < 0.02 else "  <== INESPERADO"
        print("    %-26s %12.3f %12.3f %10.3f%s"
              % (nombre, za, zb, d, marca))
        if abs(d - esperados[nombre]) > 0.02:
            raise SystemExit("  %s bajo %.3f, se esperaba %.3f"
                             % (nombre, d, esperados[nombre]))
    return len(datos)


def main():
    a = sys.argv[1:]
    seco = "--seco" in a
    a = [x for x in a if x != "--seco"]
    if len(a) != 2:
        print(__doc__)
        return 2
    entrada, salida = a
    if not seco and os.path.abspath(entrada) == os.path.abspath(salida):
        raise SystemExit("entrada y salida iguales: usar un temporal")
    bajar(entrada, salida, seco=seco)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
