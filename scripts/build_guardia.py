"""Añade a ballesta.nif el guardia y su ciclo completo "GuardiaCiclo" (22 s).

Corre en Blender 4.4 + PyNifly sobre el NIF EXPORTADO (no sobre el .blend
fuente): re-importa mod/meshes/AstraAsedio/ballesta.nif CON animaciones y
colisiones, recorta de la copia el torno/palanca que build_assets fusionó
(los proxies giratorios ya verificados del render los reemplazan), monta el
maniquí con materiales del propio NIF (texturas vanilla) y hornea UNA
NiControllerSequence "GuardiaCiclo" que comparte nodos con Fire/Reset.

En el juego: activar la ballesta EN SIGILO dispara la demo (rama demo de
mod/scripts/source/AstraAsedioActi.psc, compilable con compile_papyrus.py);
activarla normal sigue operando la ballesta como siempre. Sin cambios de ESP:
PlayGamebryoAnimation no requiere registrar la secuencia.

Detalles de estado:
- Guardia y atril viven en el NIF con escala 0.001 (invisibles); GuardiaCiclo
  los muestra desde su primer frame y el guardia queda visible al terminar.
- Los proxies de volante/manivela/palanca reemplazan la geometría recortada y
  quedan visibles en reposo (rotación 0): el gameplay sin demo es idéntico.
- La secuencia fuerza CTRL_GIRO_360 a rumbo 0 al arrancar (las posturas del
  guardia están horneadas para ese rumbo) y el virote disparado se desvanece
  tras el impacto (no hay blanco físico in-game).

Uso:  blender --python scripts/build_guardia.py    (requiere build_assets previo)
"""
import bpy, addon_utils, json, math, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_assets
import render_animacion_guardia as rag
from mathutils import Vector

EN_PRUEBA = bool(os.environ.get('ASTRA_GUARDIA_MOCK'))
NIF = ROOT/'mod/meshes/AstraAsedio/ballesta.nif'
ACCION = 'GuardiaCiclo'


def asegurar_accion(nombre):
    """La importación debe traer Fire/Reset; normaliza nombre y props."""
    a = bpy.data.actions.get(nombre)
    if a is None:
        cand = next((x for x in bpy.data.actions if nombre.lower() in x.name.lower()), None)
        assert cand, 'la importación no trajo la secuencia %r (¿PyNifly sin import_animations?)' % nombre
        cand.name = nombre
        a = cand
    a['pynController'] = 'NiControllerSequence'
    a.use_fake_user = True
    return a


def mats_del_nif():
    """Materiales del propio ballesta.nif importado (texturas vanilla)."""
    fuente, mats = {}, {}
    for o in bpy.data.objects:
        if o.type != 'MESH' or not o.data.materials:
            continue
        n = o.name.lower()
        if 'wood' in n: fuente['tunica'] = fuente['madera'] = o.data.materials[0]
        elif 'metal' in n: fuente['hierro'] = o.data.materials[0]
        elif 'cuerda' in n: fuente['tela'] = fuente['cuero'] = o.data.materials[0]
        elif 'bolt' in n: fuente['piel'] = o.data.materials[0]
    aliases = dict(tunica='Guardia_tunica', tela='Guardia_tela', cuero='Guardia_cuero',
                   hierro='Guardia_hierro', piel='Guardia_piel', madera='Madera_proxy')
    colores = dict(tunica=(.42, .36, .19), tela=(.24, .21, .17), cuero=(.22, .15, .10),
                   hierro=(.36, .38, .41), piel=(.68, .48, .36), madera=(.35, .24, .14))
    for k in ('tunica', 'tela', 'cuero', 'hierro', 'piel'):
        if k in fuente:
            m = fuente[k]
        else:                                   # respaldo: color plano
            m = rag.material(aliases[k], colores[k])
        mats[k] = m
    if 'madera' in fuente:
        mats['madera'] = fuente['madera']
    return mats


def uv_simple(o, escala=30.0):
    """UV planar por cara (proyección según la normal dominante): las texturas
    vanilla del NIF se ven con veta en lugar de un color plano de la esquina.
    Solo se aplica a las mallas nuevas (cajas/tubos del guardia y los proxies)."""
    m = o.data
    if not m.polygons:
        return
    capa = m.uv_layers.new(name='UVMap') if not len(m.uv_layers) else m.uv_layers.active
    if capa is None:
        return
    lo = [min(v.co[i] for v in m.vertices) for i in range(3)]
    for p in m.polygons:
        vs = [m.vertices[i] for i in p.vertices]
        n = (vs[1].co-vs[0].co).cross(vs[2].co-vs[0].co) if len(vs) >= 3 else Vector((0, 0, 1))
        eje = max(range(3), key=lambda i: abs(n[i]))
        u_ax, v_ax = [i for i in range(3) if i != eje]
        for k, vi in enumerate(p.vertices):
            co = m.vertices[vi].co
            capa.data[p.loop_indices[k]].uv = ((co[u_ax]-lo[u_ax])/escala, (co[v_ax]-lo[v_ax])/escala)


def main():
    addon_utils.enable('io_scene_nifly', default_set=True)
    sha_origen = rag.hashlib.sha256(NIF.read_bytes()).hexdigest() if NIF.exists() else None

    accion = bpy.data.actions.new(ACCION)
    accion['pynController'] = 'NiControllerSequence'
    accion.use_fake_user = True

    # ---- montaje (import round-trip + cirugía + proxies + guardia + paradas)
    rig = rag.montar(con_render=False, mats=mats_del_nif, accion_demo=accion, completo=True)

    # UVs de las mallas nuevas (el virote en mano comparte datos con el del NIF)
    for o in bpy.data.objects:
        if o.type == 'MESH' and o.name.startswith(('g_', 'volante_', 'manivela_', 'gatillo_', 'atril_')):
            uv_simple(o)

    fire, reset = asegurar_accion('Fire'), asegurar_accion('Reset')
    colisiones = [o for o in bpy.data.objects if o.name.lower().startswith('bhk')]
    bsx = [o for o in bpy.data.objects if 'bsxflags' in o.name.lower()]
    assert colisiones, 'la importación no trajo colisiones (¿import_collisions?)'
    assert bsx, 'falta el nodo BSXFlags del NIF original'

    # ---- claves de estado propias del juego (caen en GuardiaCiclo)
    giro360 = rig['giro360']
    giro360.rotation_euler = (0, 0, 0)          # rumbo 0: posturas horneadas
    rag.clave(giro360, 1); rag.clave(giro360, rag.TOTAL)
    atril = rig['atril']
    atril.scale = (1, 1, 1); rag.clave(atril, 1)  # visible durante todo el ciclo

    # ---- coreografía completa (mecanismo + guardia, sin cámaras ni blanco)
    coreo = rag.coreografiar(rig, con_render=False)
    assert coreo['impacto_f'] is not None, 'el virote no llegó al plano de impacto'

    # ---- pynActionSlots: GuardiaCiclo en todos los animados; Fire/Reset en los compartidos
    compartidos = {rig['brazo_i'].name, rig['brazo_d'].name, rig['cuerda_i'].name,
                   rig['cuerda_d'].name, rig['virote'].name}
    animados = {s.name_display for a in (accion, fire, reset) for s in a.slots}
    for nombre in sorted(animados):
        o = bpy.data.objects.get(nombre)
        if o is None:
            continue
        slots = {ACCION: nombre}
        if nombre in compartidos:
            slots['Fire'] = nombre; slots['Reset'] = nombre
        o['pynActionSlots'] = json.dumps(slots)

    # ---- reposo: guardia y atril escondidos; el resto queda como se ve
    rig['guardia'].scale = (.001, .001, .001)
    atril.scale = (.001, .001, .001)
    for v in rig['vir_atril']:
        v.scale = (.001, .001, .001)
    rig['virote_mano'].scale = (.001, .001, .001)

    # ---- la raíz vuelve al origen: el NIF se coloca desde la celda, no interno
    rig['raiz'].location = (0, 0, 0)
    bpy.context.view_layer.update()

    # ---- autodiagnóstico antes de exportar
    nodos_accion = sorted(s.name_display for s in accion.slots)
    claves = sum(len(fc.keyframe_points) for capa in accion.layers for tira in capa.strips
                 for bolsa in tira.channelbags for fc in bolsa.fcurves)
    assert len(nodos_accion) >= 30, 'GuardiaCiclo anima muy pocos nodos: %d' % len(nodos_accion)
    assert 20000 < claves < 200000, 'GuardiaCiclo con %d claves (esperadas ~60k)' % claves
    for a in (fire, reset):
        n = sum(len(fc.keyframe_points) for capa in a.layers for tira in capa.strips
                for bolsa in tira.channelbags for fc in bolsa.fcurves)
        assert n > 0, 'la secuencia %s perdió sus claves' % a.name
    bpy.context.scene.frame_set(rag.TOTAL); bpy.context.view_layer.update()
    g = rig['guardia'].matrix_world.translation
    esperado = (rig['PARADAS'][-1][1], rig['PARADAS'][-1][2], rig['PISO']-rag.TOPE)
    assert (rag.Vector(g)-rag.Vector(esperado)).length < 3, \
        'guardia final %s, esperado %s' % ([round(x, 1) for x in g.v] if hasattr(g, 'v') else list(g), esperado)

    # ---- exportar (patrón de build_assets.export): extraer escalas, exportar, parchear
    escalas = {}
    for a in bpy.data.actions:
        for capa in a.layers:
            for tira in capa.strips:
                for bolsa in tira.channelbags:
                    for fc in list(bolsa.fcurves):
                        if fc.data_path == 'scale' and fc.array_index == 0:
                            escalas[(a.name, bolsa.slot.name_display)] = \
                                [((kp.co.x-1)/30, kp.co.y) for kp in fc.keyframe_points]
                            bolsa.fcurves.remove(fc)
    ruta = Path('/tmp/ballesta_guardia_prueba.nif') if EN_PRUEBA else NIF
    bpy.ops.object.select_all(action='DESELECT')
    for o in bpy.data.objects:
        o.select_set(True)
    bpy.context.view_layer.objects.active = rig['raiz']
    bpy.ops.export_scene.pynifly(filepath=str(ruta), target_game='SKYRIMSE', blender_xf=False,
                                 intuit_defaults=False, export_animations=True,
                                 preserve_hierarchy=True, export_modifiers=False, export_colors=True)
    if not EN_PRUEBA and escalas:
        build_assets.patch_scale_keys(ruta, escalas)   # PyNifly omite claves de escala

    (ROOT/'reports/guardia_juego.json').write_text(json.dumps({
        'proposito': 'GuardiaCiclo horneada en ballesta.nif: demo completa in-game.',
        'accion': ACCION, 'frames': rag.TOTAL, 'duracion_s': round(rag.TOTAL/rag.FPS, 2),
        'impacto_frame': coreo['impacto_f'],
        'nodos_animados': nodos_accion,
        'nodos_compartidos_con_fire_reset': sorted(compartidos),
        'claves_totales': claves,
        'escalas_reparchadas': {('%s/%s' % k): len(v) for k, v in escalas.items()},
        'cirugia_caras_borradas': rig['informe'],
        'colisiones_importadas': len(colisiones), 'bsxflags': bool(bsx),
        'materiales_guardia': {k: m.name for k, m in rig['mats'].items()},
        'nif_sha256_antes': sha_origen,
        'salida': str(ruta), 'en_prueba': EN_PRUEBA,
        'notas': ['activar en sigilo = demo (AstraAsedioActi.psc); activar normal = manejarla',
                  'sin cambios de ESP: PlayGamebryoAnimation no requiere registro',
                  'el guardia queda visible al terminar el ciclo; virote se desvanece tras el impacto',
                  'Confirmar in-game: comportamiento del nodo al terminar la secuencia y round-trip de colisiones'],
    }, indent=2))
    print('ASTRA_GUARDIA_BUILT -> %s (%d nodos, %d claves)' % (ruta, len(nodos_accion), claves))


if __name__ == '__main__':
    main()
