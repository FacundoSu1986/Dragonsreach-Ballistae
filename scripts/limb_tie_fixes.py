"""Amarras de poste ajustadas a la madera real.

Que cambia respecto de la version anterior, y por que:

1. PROYECCION SOBRE LA MALLA REAL. Antes el centro del anillo salia de desplazar
   el CASCO CONVEXO de la seccion. El casco puentea entre la madera y el fleje y,
   sobre todo, es del ancho de la seccion mas gruesa aunque el poste ya se haya
   afinado: ahi el anillo queda de mayor diametro que el tronco y cuelga. Ahora
   cada punto del centro se proyecta sobre la superficie real del poste y queda a
   RADIO + holgura de ella, medido contra la malla y no contra un proxy.

2. BANDA AXIAL. Antes cada amarra era UN anillo en un plano: agarraba una sola
   seccion y, en el tramo conico, todo lo que quedara mas alla del plano se
   separaba. Ahora la amarra son TURNOS vueltas consecutivas a lo largo del eje
   del poste, cada una con su propia seccion real, de modo que sigue la conicidad.

3. PERFIL REDONDO. Antes el tubo era hexagonal: su cara interior era una cuerda
   recta, tocaba la madera solo en el centro y en los bordes se levantaba, que
   es justo lo que se ve "flotando". Con mas lados el interior es una curva que
   se apoya en la madera.

4. Holgura de diseno de 1.5 mm a 0.8 mm.

Lo que NO cambia: el nombre de los objetos, sus padres, el material, el chequeo de
malla cerrada y el informe que se escribe.
"""
import bpy, json, math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

RADIO = 0.014        # m, radio del cordon
HOLGURA = 0.0008     # m, holgura de diseno entre madera y cordon
TURNOS = 2           # vueltas consecutivas por amarra
LADO = 8             # lados del tubo
PUNTOS = 16          # puntos por vuelta: el perimetro del poste mide ~660 mm
PASO_ANG = math.pi / 7.5   # 24 grados al derivar la seccion


def hull2(points):
    pts = sorted(set((round(p[0], 8), round(p[1], 8)) for p in points))
    if len(pts) < 3:
        return pts
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo = []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 1e-10:
            lo.pop()
        lo.append(p)
    hi = []
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 1e-10:
            hi.pop()
        hi.append(p)
    return [Vector((x, y, 0)) for x, y in lo[:-1] + hi[:-1]]


def section(objects, frame):
    """Puntos de la seccion real en el plano z=0 del marco dado."""
    points = []
    inverse = frame.inverted()
    for obj in objects:
        verts = [inverse @ obj.matrix_world @ v.co for v in obj.data.vertices]
        for edge in obj.data.edges:
            a, b = (verts[i] for i in edge.vertices)
            if abs(a.z) < 1e-7:
                points.append(a)
            if a.z * b.z < 0:
                points.append(a + (b - a) * (-a.z / (b.z - a.z)))
    hull = hull2(points)
    if len(hull) < 3:
        raise RuntimeError('No closed limb section at binding')
    return hull


def rounded_offset(hull, distance):
    out = []
    for i, p in enumerate(hull):
        prev = (p - hull[i - 1]).normalized()
        after = (hull[(i + 1) % len(hull)] - p).normalized()
        n0 = Vector((prev.y, -prev.x, 0))
        n1 = Vector((after.y, -after.x, 0))
        angle0 = math.atan2(n0.y, n0.x)
        arc = (math.atan2(n1.y, n1.x) - angle0) % math.tau
        count = max(1, math.ceil(arc / PASO_ANG))
        for j in range(count + 1):
            angle = angle0 + arc * j / count
            point = p + Vector((math.cos(angle), math.sin(angle), 0)) * distance
            if not out or (point - out[-1]).length > 1e-6:
                out.append(point)
    return out


def resample(puntos, k):
    """k puntos equiespaciados en longitud de arco; el ultimo cierra el anillo."""
    n = len(puntos)
    largo = [0.0]
    for i in range(1, n + 1):
        largo.append(largo[-1] + (puntos[i % n] - puntos[i - 1]).length)
    total = largo[-1]
    salida = []
    for i in range(k):
        d = total * i / k
        j = 0
        while j < n and largo[j + 1] < d:
            j += 1
        span = largo[j + 1] - largo[j]
        t = 0.0 if span < 1e-12 else (d - largo[j]) / span
        salida.append(puntos[j].lerp(puntos[(j + 1) % n], t))
    return salida


def alinear_inicio(anillo, referencia):
    """Rotea la lista para que el punto 0 quede en el angulo de la referencia.

    Sin esto, cada vuelta arrancaria en un angulo distinto (rounded_offset empieza
    por el vertice 0 del casco, que cambia al cambiar la seccion) y el tramo que
    une el final de una vuelta con el principio de la siguiente cortaria la cuerda:
    aparece un pliegue anguloso visible en la amarra.
    """
    if not referencia:
        return anillo
    cx = sum(p.x for p in anillo) / len(anillo)
    cy = sum(p.y for p in anillo) / len(anillo)
    mejor, idx = None, 0
    for i, p in enumerate(anillo):
        ang = math.atan2(p.y - cy, p.x - cx)
        d = abs((ang - referencia + math.pi) % math.tau - math.pi)
        if mejor is None or d < mejor:
            mejor, idx = d, i
    return anillo[idx:] + anillo[:idx]


def proyectar(bvh, mundo, holgura):
    """Lleva un punto del centro a holgura+radio de la superficie real."""
    hit, normal, _idx, dist = bvh.find_nearest(mundo)
    objetivo = RADIO + holgura
    if normal is not None and normal.length > 1e-9:
        return hit + normal.normalized() * objetivo
    d = mundo - hit
    if d.length < 1e-9:
        return hit + Vector((objetivo, 0, 0))
    return hit + d.normalized() * objetivo


def apply(root):
    report = {
        'original_files_modified': False,
        'method': 'Closed rope lashing swept as an axial band and projected onto the real limb mesh',
        'rope_radius_m': RADIO,
        'designed_clearance_m': HOLGURA,
        'turns_per_binding': TURNOS,
        'tube_sides': LADO,
        'parts': [],
    }
    for obj in sorted(list(bpy.data.objects), key=lambda o: o.name):
        if not obj.name.startswith(('Ligadura_limbo', 'Ligadura_punta')):
            continue
        side = obj.parent.name[-1]
        piezas = [bpy.data.objects['Limbo_arco_' + side], bpy.data.objects['Fleje_arco_' + side]]
        world_verts = []
        polys = []
        for piece in piezas:
            off = len(world_verts)
            world_verts.extend(piece.matrix_world @ v.co for v in piece.data.vertices)
            polys.extend(tuple(off + i for i in p.vertices) for p in piece.data.polygons)
        bvh = BVHTree.FromPolygons(world_verts, polys)

        frame0 = obj.matrix_world.copy()
        anterior = [bvh.find_nearest(obj.matrix_world @ v.co)[3] for v in obj.data.vertices]

        # ---- dos vueltas, cada una un anillo cerrado e independiente ----
        # No se hace una helice continua: al unir el final de una vuelta con el
        # principio de la siguiente, los tubos se pisan (paso < diametro) y aparece
        # un repliegue anguloso visible en la amarra. Dos anillos separados se leen
        # como dos vueltas de una atadura real y cada uno usa el mismo marco que ya
        # funcionaba en la version anterior.
        paso = 2 * RADIO * 1.06          # un pelo mas que el diametro: no se pisan
        verts = []
        faces = []
        uvs = []
        camino_mundo = []
        estaciones = []
        base = 0
        for t in range(TURNOS):
            offset = (t - (TURNOS - 1) / 2.0) * paso
            fr = frame0.copy()
            fr.translation = (frame0 @ Vector((0, 0, offset))).to_3d()
            hull = section(piezas, fr)
            anillo = resample(rounded_offset(hull, RADIO + HOLGURA), PUNTOS)
            proyectados = [proyectar(bvh, fr @ q, HOLGURA) for q in anillo]
            gap = [bvh.find_nearest(p)[3] - RADIO for p in proyectados]
            estaciones.append({'offset_m': offset, 'section_points': len(hull),
                               'section_radius_max_m': max(Vector((h.x, h.y, 0)).length for h in hull),
                               'gap_min_m': min(gap), 'gap_max_m': max(gap)})
            camino_mundo.extend(proyectados)

            count = len(proyectados)
            # La malla vive en el marco LOCAL del objeto amarra (frame0), no en el de
            # la estacion (fr): usar fr.inverted() correria cada vuelta por su propio
            # desplazamiento sobre el eje y las dos se separarian del poste.
            ring = [frame0.inverted() @ p for p in proyectados]
            lengths = [0.0]
            for i in range(1, count):
                lengths.append(lengths[-1] + (ring[i] - ring[i - 1]).length)
            perimeter = lengths[-1] + (ring[0] - ring[-1]).length
            for i, p in enumerate(ring):
                tangent = (ring[(i + 1) % count] - ring[i - 1]).normalized()
                outward = Vector((tangent.y, -tangent.x, 0))
                outward = outward.normalized() if outward.length > 1e-9 else Vector((1, 0, 0))
                arriba = Vector((0, 0, 1))
                for j in range(LADO):
                    ang = math.tau * j / LADO
                    verts.append(tuple(p + RADIO * (math.cos(ang) * outward + math.sin(ang) * arriba)))
            for i in range(count):
                for j in range(LADO):
                    faces.append((base + i * LADO + j, base + i * LADO + (j + 1) % LADO,
                                  base + ((i + 1) % count) * LADO + (j + 1) % LADO,
                                  base + ((i + 1) % count) * LADO + j))
                    u0 = lengths[i] / (RADIO * math.tau)
                    u1 = (lengths[i + 1] if i + 1 < count else perimeter) / (RADIO * math.tau)
                    uvs.append(((j / LADO, u0), ((j + 1) / LADO, u0), ((j + 1) / LADO, u1), (j / LADO, u1)))
            base += count * LADO

        old_mesh = obj.data
        materials = list(old_mesh.materials)
        mesh = bpy.data.meshes.new(obj.name + '_ajustada')
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        for material in materials:
            mesh.materials.append(material)
        layer = mesh.uv_layers.new(name='UVMap')
        for face, coords in zip(mesh.polygons, uvs):
            face.use_smooth = True
            for li, uv in zip(face.loop_indices, coords):
                layer.data[li].uv = uv
        obj.data = mesh
        if old_mesh.users == 0:
            bpy.data.meshes.remove(old_mesh)

        # ---- controles que tienen que poder fallar ----
        edges = {}
        for face in mesh.polygons:
            for e in face.edge_keys:
                edges[e] = edges.get(e, 0) + 1
        if any(c != 2 for c in edges.values()):
            raise RuntimeError('Open rope binding ' + obj.name)
        gaps = [bvh.find_nearest(p)[3] - RADIO for p in camino_mundo]
        if min(gaps) < -0.001:
            raise RuntimeError('Rope sinks into the limb ' + obj.name + ': ' + str(min(gaps)))
        if max(gaps) > 0.006:
            raise RuntimeError('Rope does not hug the limb ' + obj.name + ': ' + str(max(gaps)))
        if (max(gaps) - min(gaps)) > 0.004:
            raise RuntimeError('Rope ring is not snug ' + obj.name + ': spread ' + str(max(gaps) - min(gaps)))

        # Control de posicion: la malla tiene que quedar SOBRE el poste. Esta
        # comprobacion existe porque una version anterior de este archivo escribio
        # los puntos del centro en espacio de mundo dentro de una malla que espera
        # espacio local, y las amarras quedaron a 600 u del poste. verify_assets.py
        # no lo detecta: no mira donde esta la geometria de las amarras.
        mundo_rope = [obj.matrix_world @ v.co for v in mesh.vertices]
        mundo_tronco = [p.matrix_world @ v.co for p in piezas for v in p.data.vertices]
        for eje in range(3):
            r_lo = min(v[eje] for v in mundo_rope); r_hi = max(v[eje] for v in mundo_rope)
            t_lo = min(v[eje] for v in mundo_tronco); t_hi = max(v[eje] for v in mundo_tronco)
            if r_hi < t_lo - 0.05 or r_lo > t_hi + 0.05:
                raise RuntimeError('Binding %s is off the limb on axis %d: rope %.3f..%.3f vs limb %.3f..%.3f'
                                   % (obj.name, eje, r_lo, r_hi, t_lo, t_hi))

        report['parts'].append({
            'name': obj.name, 'parent': obj.parent.name, 'closed_manifold': True,
            'triangles': len(faces) * 2, 'vertices': len(verts),
            'centreline_gap_min_m': min(gaps), 'centreline_gap_max_m': max(gaps),
            'previous_max_rope_vertex_distance_to_limb_m': max(anterior),
            'stations': estaciones,
            'path_world': [list(p) for p in camino_mundo],
        })
    if len(report['parts']) != 14:
        raise RuntimeError('Expected seven bindings per bow limb')
    (Path(root) / 'reports/limb_ties_revision.json').write_text(json.dumps(report, indent=2))
    return report