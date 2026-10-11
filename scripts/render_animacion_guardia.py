"""Render de demostración: un guardia opera la ballesta Astra de punta a punta.

Correr en la máquina de modding (Blender 4.4 + PyNifly 27, igual que build_assets.py):

    blender --background --python scripts/render_animacion_guardia.py

Ciclo animado a 30 fps (~22 s): el guardia (maniquí low-poly armado por script,
con IK analítico de dos huesos) da manivela al torno —los brazos se tensan y las
cuerdas se anclan punta→centro con la misma matemática de build_assets.sequences—,
saca un virote del atril, lo carga sobre el riel caminando, la ballesta se eleva,
mira por el alza y el guion (plano desde AstraSightCameraNode, v10), tira de la
palanca del gatillo y dispara: los brazos sueltan, el virote vuela con física
propia (arco de arma de asedio) y se clava en un blanco que el script coloca
exactamente en el punto de impacto pre-simulado.

Trabaja sobre los NIF exportados (mod/meshes/AstraAsedio), nunca sobre las fuentes
.blend ni sobre los NIF en disco: solo se edita la copia importada en memoria. El
volante, la manivela y la palanca del gatillo están fusionados en las mallas
estáticas del nif, así que sus triángulos se recortan de esa copia y se reemplazan
por proxies hijos de CTRL_ELEVACION que sí giran (y elevan con el carro).
Salidas: renders/Astra_guardia_disparo.mp4, renders/Astra_guardia_disparo.blend
(para retocar cámaras y volver a renderizar) y reports/animacion_guardia.json.

Desde la v-juego el script se divide en montar() + coreografiar() + main():
build_guardia.py reutiliza las dos primeras (sin cámaras ni blanco) para hornear
el mismo ciclo como NiControllerSequence "GuardiaCiclo" dentro de ballesta.nif.
"""
import bpy, addon_utils, bmesh, json, math, hashlib, random
from pathlib import Path
from mathutils import Vector, Matrix

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT/'config.json').read_text())
S = CFG['meters_to_units']
BASE = 6.65
RAISE = float(CFG.get('mount_raise_units', 0.0))          # 20 u: ya vienen dentro de los NIF v10
DROP = float(CFG.get('turret_drop_units', 0.0))           # 36 u: v22 bajó el cabezal (ergonomía)
TOPE = float(CFG['tower_top_units'])                      # raíz de la ballesta sobre la torre
PIVOT = float(CFG['pitch_pivot_units'])                   # altura de CTRL_ELEVACION sobre la raíz
GRAVEDAD = 9.81 * S                                       # u/s^2
V0 = 2100.0                                               # u/s (velocidad de demostración)
ELEVACION = math.radians(25.0)
REVOLUCIONES = 3.0                                        # vueltas de manivela para tensar
FPS = 30
MUESTRAS = 24                                             # Cycles; bajar si la máquina no llega
ANCHO, ALTO = 1280, 720
GUARDAR_BLEND = True

# ---- fases (frames) ---------------------------------------------------------
F_IDLE_FIN = 75
F_TORNO = (76, 240)          # manivela: la cuerda pasa de disparada (p=1) a tensada (p=0)
F_PASO_ATRIL = (244, 258)
F_ALCANCE = (262, 274)       # mano al virote apoyado en el atril
F_TIRAR = (274, 284)         # deslizarlo hacia arriba, fuera de la horquilla
F_LLEVAR = (284, 364)        # cargarlo caminando hasta el costado del riel (giro + 6 pasos)
F_COLOCAR = (366, 374)       # alzarlo y apoyarlo de lado sobre el riel
F_ASIENTO = 374              # swap exacto mano→riel (VIROTE_VISUAL pasa a escala 1)
F_SOLTAR = (374, 384)
F_ELEVAR = (410, 460)        # eleva mientras el guardia vuelve al puesto de tiro
F_AGARRE = (458, 470)        # mano a la empuñadura de la palanca
F_MIRA = (463, 492)          # plano por el alza y el guion
F_TIRON = (493, 496)
F_LIBERACION = 497
F_BRAZOS_FIN = 501
F_RECUADRO = 518
F_CAM_E = (493, 521)
F_CAM_F0 = 522

ARM_DELTA = {'CTRL_BRAZO_I': Vector((0, 0, 0.24)), 'CTRL_BRAZO_D': Vector((0, 0, -0.24))}

# Mecanismo en el espacio LOCAL de CTRL_ELEVACION (source v04; pivote de elevación a z=8.55 m).
EJE = Vector((0.735*S, 1.580*S, (8.48-8.55)*S))              # eje del tambor (gira en X)
MANGO0 = Vector((0.9125*S, 1.300*S, (8.27-8.55)*S))          # mango en reposo
VOLANTE_C = Vector((0.735*S, 1.580*S, (8.48-8.55)*S))
VOLANTE_R = 0.315*S
GATILLO_PIVOTE = Vector((0.0, 1.415*S, (8.625-8.55)*S))
GATILLO_EMP = Vector((0.0, 1.110*S, (8.16-8.55)*S))
CAJA_RECORTES = (   # (x0,x1,y0,y1,z0,z1) pitch-local: piezas fusionadas a reemplazar por proxies
    (0.64*S, 1.06*S, 1.24*S, 1.92*S, (8.15-8.55)*S, (8.82-8.55)*S),   # volante+manivela+mango+casquillo
    (-0.05*S, 0.05*S, 1.07*S, 1.44*S, (8.10-8.55)*S, (8.64-8.55)*S),  # palanca del gatillo
)
# Cuerdas en espacio RAÍZ (constantes de build_assets + alza v07 de 20 u - bajada v22 de 36 u).
RESTTIP = {
    'Cuerda_I': Vector((-1.89*S, -1.445*S, (8.83-BASE)*S + RAISE - DROP)),
    'Cuerda_D': Vector((1.89*S, -1.445*S, (8.83-BASE)*S + RAISE - DROP)),
}
CENTRO_Z = (8.83-BASE)*S + RAISE - DROP
Z_BLANCO = 280.0                                            # altura del centro del blanco

def abanico(f, a, b):
    if b <= a: return 1.0 if f >= b else 0.0
    return max(0.0, min(1.0, (f-a)/(b-a)))
def suave(x): return x*x*(3-2*x)
def envolver(a): return (a+math.pi) % (2*math.pi) - math.pi
def rot2(v, a): return Vector((v.x*math.cos(a)-v.y*math.sin(a), v.x*math.sin(a)+v.y*math.cos(a)))

def pre_simular():
    """Vuelo del virote sin bpy: frame de impacto y distancia del blanco.
    El origen es el centro aproximado del virote ya elevado (pitch-local (0,-76,-17.5))."""
    M = Matrix.Translation((0, 0, TOPE+PIVOT)) @ Matrix.Rotation(-ELEVACION, 4, 'X')
    origen = M @ Vector((0, -76.0, -17.5))
    v = Vector((0, -V0*math.cos(ELEVACION), V0*math.sin(ELEVACION)))
    t, f = 0.0, F_LIBERACION
    while f < F_LIBERACION + 400:
        t += 1.0/FPS; f += 1
        if origen.z + v.z*t - .5*GRAVEDAD*t*t <= Z_BLANCO:
            return f, abs(origen.y + v.y*t)
    raise RuntimeError('el virote nunca cae')

F_IMPACTO, D_BLANCO = pre_simular()
F_CAM_F1 = F_IMPACTO + 20
F_EPILOGO = F_IMPACTO + 21
TOTAL = F_IMPACTO + 78

# ----------------------------------------------------------------------------
def clave(o, f):
    o.keyframe_insert('location', frame=f)
    if o.rotation_mode == 'QUATERNION': o.keyframe_insert('rotation_quaternion', frame=f)
    else: o.keyframe_insert('rotation_euler', frame=f)
    o.keyframe_insert('scale', frame=f)

def fijar(o, M, f, padre=None):
    """Fija la matriz MUNDO de o (la del padre ya resuelta en Python) y la clava."""
    P = o.parent.matrix_world.copy() if (padre is None and o.parent is not None) else (padre or Matrix.Identity(4))
    loc, rot, esc = (P.inverted() @ M).decompose()
    o.location, o.rotation_quaternion, o.scale = loc, rot, esc
    clave(o, f)

def apuntar_Y(origen, fin):
    d = Vector(fin) - Vector(origen)
    return Matrix.Translation(origen) @ d.normalized().to_track_quat('Y', 'Z').to_matrix().to_4x4()

def normales(m):
    bm = bmesh.new(); bm.from_mesh(m)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bm.to_mesh(m); bm.free(); m.update()

def malla_caja(nombre, lo, hi, padre, mat, escena):
    vv = [(x, y, z) for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]
    caras = [(0,1,3,2),(4,6,7,5),(0,4,5,1),(1,5,7,3),(2,3,7,6),(0,2,6,4)]
    m = bpy.data.meshes.new(nombre); m.from_pydata(vv, [], caras); m.update()
    o = bpy.data.objects.new(nombre, m); escena.collection.objects.link(o); o.parent = padre
    m.materials.append(mat)
    return o

def malla_tubo(nombre, p0, p1, radio, padre, mat, escena, lados=8):
    eje = (Vector(p1)-Vector(p0)).normalized()
    ref = Vector((1, 0, 0)) if abs(eje.x) < .9 else Vector((0, 0, 1))
    u = eje.cross(ref).normalized(); w = eje.cross(u)
    vv = [Vector(p0) + radio*(u*math.cos(i*math.tau/lados) + w*math.sin(i*math.tau/lados)) for i in range(lados)]
    vv += [Vector(p1) + radio*(u*math.cos(i*math.tau/lados) + w*math.sin(i*math.tau/lados)) for i in range(lados)]
    caras = [tuple(range(lados-1, -1, -1)), tuple(range(lados, 2*lados))]
    caras += [(i, (i+1) % lados, (i+1) % lados+lados, i+lados) for i in range(lados)]
    m = bpy.data.meshes.new(nombre); m.from_pydata([tuple(v) for v in vv], [], caras); normales(m)
    o = bpy.data.objects.new(nombre, m); escena.collection.objects.link(o); o.parent = padre
    m.materials.append(mat)
    return o

def recortar(obj, pitch, cajas, informe):
    """Borra de la copia importada las caras totalmente dentro de cada caja (pitch-local)."""
    bm = bmesh.new(); bm.from_mesh(obj.data)
    M = pitch.matrix_world.inverted() @ obj.matrix_world
    dentro = lambda v: any(c[0] <= v.x <= c[1] and c[2] <= v.y <= c[3] and c[4] <= v.z <= c[5] for c in cajas)
    borrar = [f for f in bm.faces if all(dentro(M @ v.co) for v in f.verts)]
    if borrar:
        bmesh.ops.delete(bm, geom=borrar, context='FACES'); bm.to_mesh(obj.data); obj.data.update()
    informe[obj.name] = informe.get(obj.name, 0) + len(borrar)
    bm.free()

def material(nombre, color, rugosidad=.8, metalico=0.0):
    m = bpy.data.materials.new(nombre); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Roughness'].default_value = rugosidad
    b.inputs['Metallic'].default_value = metalico
    return m

def ik2(obj_sup, obj_inf, obj_fin, origen, objetivo, pole, L1, L2, f, matriz_padre, plano=None):
    """IK analítico de dos huesos; la geometría de cada segmento va a lo largo de +Y.
    plano: matriz de orientación fija para el último objeto (pie plano al caminar)."""
    O, T = Vector(origen), Vector(objetivo)
    d = T - O; L = min(max(d.length, abs(L1-L2)+.5), L1+L2-.5)
    dirr = d.normalized() if d.length > 1e-6 else Vector((0, 0, 1))
    pv = Vector(pole) - O
    pp = pv - dirr*pv.dot(dirr)
    if pp.length < 1e-5:
        pp = dirr.cross(Vector((1, 0, 0)))
        if pp.length < 1e-5: pp = dirr.cross(Vector((0, 0, 1)))
    pp = pp.normalized()
    a = math.acos(max(-1, min(1, (L1*L1 + L*L - L2*L2)/(2*L1*L))))
    E = O + dirr*(L1*math.cos(a)) + pp*(L1*math.sin(a))
    Tc = O + dirr*L
    M_sup, M_inf = apuntar_Y(O, E), apuntar_Y(E, Tc)
    M_fin = (Matrix.Translation(Tc) @ plano) if plano is not None else apuntar_Y(Tc, Tc+dirr)
    fijar(obj_sup, M_sup, f, padre=matriz_padre)
    fijar(obj_inf, M_inf, f, padre=M_sup)
    fijar(obj_fin, M_fin, f, padre=M_inf)

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def montar(con_render=True, mats=None, accion_demo=None, completo=False):
    """Monta la escena del guardia sobre la ballesta importada del NIF exportado.

    Devuelve el rig (dict de nodos, paradas y constantes) para coreografiar().
    con_render: agrega torre, blanco, virotes previos y virutas (solo el video).
    mats: materiales tunica/tela/cuero/hierro/piel[/madera] (None = colores de
    estudio). accion_demo: acción asignada a todos los nodos que el bucle
    keyframea, para exportar el ciclo completo como UNA NiControllerSequence.
    completo: importar también animaciones y colisiones (re-export del NIF).
    """
    informe, escena = {}, bpy.context.scene
    addon_utils.enable('io_scene_nifly', default_set=True)
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)

    # ---- NIF exportados (como render_assets.py: visual, sin animaciones ni colisión)
    for nombre in (('torre', 'ballesta') if con_render else ('ballesta',)):
        viejo = set(bpy.data.objects)
        bpy.context.view_layer.objects.active = None
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.import_scene.pynifly(filepath=str(ROOT/'mod/meshes/AstraAsedio'/f'{nombre}.nif'),
                                     blender_xf=False, import_animations=completo,
                                     import_collisions=completo, create_bones=False)
        if nombre == 'ballesta':
            raiz = next(o for o in set(bpy.data.objects)-viejo if o.get('pynRoot'))
            raiz.location.z = TOPE
    def nodo(nombre):
        o = bpy.data.objects.get(nombre)
        if o is None:
            cand = [c for c in bpy.data.objects if nombre in c.name and c.type == 'EMPTY']
            assert cand, 'falta '+nombre+' en la importación'
            o = cand[0]
        return o
    pitch, brazo_i, brazo_d = nodo('CTRL_ELEVACION'), nodo('CTRL_BRAZO_I'), nodo('CTRL_BRAZO_D')
    cuerda_i, cuerda_d = nodo('Cuerda_I'), nodo('Cuerda_D')
    virote = nodo('VIROTE_VISUAL')
    for o in (cuerda_i, cuerda_d, virote):
        o.rotation_mode = 'QUATERNION'   # fijar() escribe rotation_quaternion
    virote_malla = next(o for o in virote.children if o.type == 'MESH')
    mira_nodo = nodo('AstraSightCameraNode')
    giro360 = nodo('CTRL_GIRO_360')   # la secuencia demo lo vuelve a rumbo 0
    base_brazo = {brazo_i.name: brazo_i.rotation_euler.copy(), brazo_d.name: brazo_d.rotation_euler.copy()}
    base_pitch = pitch.rotation_euler.copy()
    brazos = [(cuerda_i, brazo_i), (cuerda_d, brazo_d)]

    bpy.context.view_layer.update()
    ASIENTO = virote_malla.matrix_world.copy()               # virote cargado sobre el riel
    ML = virote_malla.matrix_local.copy()                    # mesh → nodo VIROTE_VISUAL
    ML_INV = ML.inverted()
    c_local = sum((v.co for v in virote_malla.data.vertices), Vector((0, 0, 0)))/len(virote_malla.data.vertices)
    punta = {}
    for nd, br in brazos:
        punta[nd.name] = br.matrix_world.inverted() @ (raiz.matrix_world @ RESTTIP[nd.name])
        nd['rest_length'] = (Vector((0, 1.03*S, CENTRO_Z)) - RESTTIP[nd.name]).length
    # cirugía: quitar de la copia importada volante/manivela/palanca fusionados
    for o in [c for c in pitch.children if c.type == 'MESH']: recortar(o, pitch, CAJA_RECORTES, informe)


    # ---- materiales (mats=None: colores de estudio; el juego pasa una función
    # que toma los del NIF recién importado, o un dict ya armado)
    if callable(mats): mats = mats()
    if mats is None:
        mats = dict(tunica=material('Guardia_tunica', (.42, .36, .19)),
                    tela=material('Guardia_tela', (.24, .21, .17)),
                    cuero=material('Guardia_cuero', (.22, .15, .10), .65),
                    hierro=material('Guardia_hierro', (.36, .38, .41), .35, .9),
                    piel=material('Guardia_piel', (.68, .48, .36), .6))
    tunica = mats['tunica']; tela = mats['tela']; cuero = mats['cuero']
    hierro = mats['hierro']; piel = mats['piel']
    madera = mats.get('madera')
    if madera is None:
        for o in pitch.children:
            if o.type == 'MESH' and 'wood' in o.name.lower() and o.data.materials: madera = o.data.materials[0]
    if madera is None: madera = material('Madera_proxy', (.35, .24, .14))

    # ---- proxies del mecanismo (hijos de pitch: giran y elevan con el carro)
    volante = bpy.data.objects.new('ProxyVolante', None)
    escena.collection.objects.link(volante); volante.parent = pitch; volante.location = VOLANTE_C
    for i in range(4):
        malla_caja('volante_rayo'+str(i), (-.9, -VOLANTE_R+1.5, -.9), (.9, VOLANTE_R-1.5, .9),
                   volante, madera, escena).rotation_euler = (i*math.tau/4, 0, 0)
    for r in (VOLANTE_R+1.6, VOLANTE_R-2.6):
        w = r*math.sin(math.pi/12)+1.8
        for i in range(12):
            malla_caja('volante_arco%.0f_%d' % (r, i), (-1.7, -w, r-1.7), (1.7, w, r+1.7),
                       volante, madera, escena).rotation_euler = (i*math.tau/12, 0, 0)
    malla_tubo('volante_cubo', (-2.2, 0, 0), (2.2, 0, 0), 4.5, volante, hierro, escena)
    malla_tubo('volante_manguito', (2.2, 0, 0), (7.6, 0, 0), 3.3, volante, hierro, escena)

    manivela = bpy.data.objects.new('ProxyManivela', None)
    escena.collection.objects.link(manivela); manivela.parent = pitch; manivela.location = EJE
    rel = MANGO0 - EJE
    malla_tubo('manivela_brazo', (0, 0, 0), rel, 2.2, manivela, madera, escena)
    malla_tubo('manivela_mango', (rel.x-1, rel.y, rel.z), (rel.x+13.5, rel.y, rel.z), 3.0, manivela, cuero, escena)

    gatillo = bpy.data.objects.new('ProxyGatillo', None)
    escena.collection.objects.link(gatillo); gatillo.parent = pitch; gatillo.location = GATILLO_PIVOTE
    relg = GATILLO_EMP - GATILLO_PIVOTE
    malla_tubo('gatillo_barra', (0, 0, 0), relg, 1.8, gatillo, hierro, escena)
    malla_caja('gatillo_empuñadura', (relg.x-2.2, relg.y-1.2, relg.z-4.5), (relg.x+2.2, relg.y+1.2, relg.z+4.5),
               gatillo, cuero, escena)


    # ---- blanco (donde cae el virote), virotes previos, atril, virutas
    PISO = TOPE - 2.8                                        # disco de madera de la torre
    blanco, virutas, vel_virutas = None, [], []
    if con_render:
        blanco = bpy.data.objects.new('Blanco', None)
        escena.collection.objects.link(blanco); blanco.location = (0, -D_BLANCO, 0)
        malla_caja('blanco_tabla', (-75, -4, Z_BLANCO-90), (75, 4, Z_BLANCO+90), blanco, madera, escena)
        malla_caja('blanco_anillo', (-45, -4.6, Z_BLANCO-60), (45, 4.6, Z_BLANCO+60), blanco, material('Tinta', (.55, .16, .1)), escena)
        malla_caja('blanco_centro', (-16, -5.2, Z_BLANCO-16), (16, 5.2, Z_BLANCO+16), blanco, material('Hueso', (.85, .8, .7)), escena)
        for x in (-95, 95): malla_caja('blanco_pata'+str(x), (x-6, -6, -5), (x+6, 6, Z_BLANCO+95), blanco, madera, escena)
        malla_caja('blanco_paca1', (-150, 26, -2), (-80, 96, 40), blanco, material('Paca', (.62, .5, .25)), escena)
        malla_caja('blanco_paca2', (88, 16, -2), (154, 86, 38), blanco, material('Paca2', (.58, .46, .22)), escena)
        for i, (pos, ang) in enumerate((((60, -D_BLANCO-280, 10), .55), ((-38, -D_BLANCO+7, Z_BLANCO+34), .03))):
            v = bpy.data.objects.new('virote_previo'+str(i), virote_malla.data)
            escena.collection.objects.link(v)
            v.matrix_world = Matrix.Translation(pos) @ Matrix.Rotation(ang, 4, 'X') @ Matrix.Translation(-c_local)
        mat_viruta = material('Viruta', (.7, .55, .3))
        virutas = [malla_caja('viruta'+str(i), (-1.6, -1.6, -1.6), (1.6, 1.6, 1.6), None, mat_viruta, escena) for i in range(7)]
        for v in virutas:
            v.rotation_mode = 'QUATERNION'; v.scale = (.001, .001, .001)
        rng = random.Random(7)
        vel_virutas = [Vector((rng.uniform(-1, 1), rng.uniform(-.5, -1), rng.uniform(.4, 1.4))).normalized()*rng.uniform(90, 220)
                       for _ in virutas]
    # atril: hijo de la raíz de la ballesta (no gira con la puntería del jugador);
    # z local relativo a la raíz para que los pies queden sobre el disco de la torre
    atril = bpy.data.objects.new('Atril', None)
    escena.collection.objects.link(atril); atril.parent = raiz; atril.location = (128, 62, PISO-TOPE)
    malla_caja('atril_base', (-7, -17, 0), (7, 17, 26), atril, madera, escena)
    malla_caja('atril_horquilla', (-6, -4, 208), (6, 4, 232), atril, madera, escena)
    M_ATRIL = (Matrix.Translation((128, 62, PISO+74)) @ Matrix.Rotation(math.radians(-68), 4, 'X')
               @ Matrix.Translation(-c_local))
    M_ATRIL_TIRADO = M_ATRIL @ Matrix.Translation((0, -26, 0))
    vir_atril = []
    for i, dx in enumerate((-4.5, 0, 4.5)):
        v = bpy.data.objects.new('virote_atril'+str(i), virote_malla.data)
        escena.collection.objects.link(v); v.parent = atril; v.rotation_mode = 'QUATERNION'
        v.matrix_world = M_ATRIL @ Matrix.Translation((dx, 0, 0))
        vir_atril.append(v)
    virote_mano = bpy.data.objects.new('Virote_mano', virote_malla.data)
    escena.collection.objects.link(virote_mano); virote_mano.parent = raiz; virote_mano.rotation_mode = 'QUATERNION'
    virote_mano.scale = (.001, .001, .001)

    # ---- guardia (maniquí low-poly, +Y local = frente, pies en z local 0)
    guardia = bpy.data.objects.new('Guardia', None)
    escena.collection.objects.link(guardia); guardia.parent = raiz; guardia.rotation_mode = 'QUATERNION'
    cadera = bpy.data.objects.new('Guardia_cadera', None)
    escena.collection.objects.link(cadera); cadera.parent = guardia
    cadera.location = (0, 0, 56.3); cadera.rotation_mode = 'QUATERNION'
    malla_caja('g_torso', (-10.5, -5.7, 3), (10.5, 5.7, 46), cadera, tunica, escena)
    malla_caja('g_falda', (-9.5, -5.9, -13), (9.5, 5.9, 4), cadera, tela, escena)
    malla_caja('g_cinto', (-10.7, -6.1, 2), (10.7, 6.1, 6), cadera, cuero, escena)
    malla_caja('g_hombreraI', (-14.6, -5, 40), (-7.4, 5, 47), cadera, hierro, escena)
    malla_caja('g_hombreraD', (7.4, -5, 40), (14.6, 5, 47), cadera, hierro, escena)
    cabeza = bpy.data.objects.new('Guardia_cabeza', None)
    escena.collection.objects.link(cabeza); cabeza.parent = cadera
    cabeza.location = (0, .8, 52); cabeza.rotation_mode = 'QUATERNION'
    malla_tubo('g_cabeza', (0, 0, -5.5), (0, 0, 5.5), 6.5, cabeza, piel, escena, 10)
    malla_tubo('g_casco', (0, 0, .6), (0, 0, 8.2), 7.2, cabeza, hierro, escena, 10)
    malla_caja('g_nariz_casco', (-.9, 5.4, -3.4), (.9, 8.6, 3), cabeza, hierro, escena)
    EXT = {}
    for lado, sx in (('I', -1), ('D', 1)):
        hombro = bpy.data.objects.new('hombro_'+lado, None)
        escena.collection.objects.link(hombro); hombro.parent = cadera
        hombro.location = (sx*10.5, 0, 44); hombro.rotation_mode = 'QUATERNION'
        sup = bpy.data.objects.new('brazo_sup_'+lado, None)
        escena.collection.objects.link(sup); sup.parent = hombro; sup.rotation_mode = 'QUATERNION'
        malla_caja('g_brazo_sup_'+lado, (-3, 0, -3), (3, 27, 3), sup, tunica, escena)
        inf = bpy.data.objects.new('brazo_inf_'+lado, None)
        escena.collection.objects.link(inf); inf.parent = sup; inf.rotation_mode = 'QUATERNION'
        malla_caja('g_brazo_inf_'+lado, (-2.5, 0, -2.5), (2.5, 25, 2.5), inf, piel, escena)
        mano = bpy.data.objects.new('mano_'+lado, None)
        escena.collection.objects.link(mano); mano.parent = inf; mano.rotation_mode = 'QUATERNION'
        malla_caja('g_mano_'+lado, (-2, 0, -2), (2, 8, 2), mano, cuero, escena)
        cadera_p = bpy.data.objects.new('cadera_pierna_'+lado, None)
        escena.collection.objects.link(cadera_p); cadera_p.parent = cadera
        cadera_p.location = (sx*6.8, 0, -1); cadera_p.rotation_mode = 'QUATERNION'
        psup = bpy.data.objects.new('pierna_sup_'+lado, None)
        escena.collection.objects.link(psup); psup.parent = cadera_p; psup.rotation_mode = 'QUATERNION'
        malla_caja('g_pierna_sup_'+lado, (-3.2, 0, -3.2), (3.2, 30, 3.2), psup, tela, escena)
        pinf = bpy.data.objects.new('pierna_inf_'+lado, None)
        escena.collection.objects.link(pinf); pinf.parent = psup; pinf.rotation_mode = 'QUATERNION'
        malla_caja('g_pierna_inf_'+lado, (-2.7, 0, -2.7), (2.7, 30, 2.7), pinf, cuero, escena)
        pie = bpy.data.objects.new('pie_'+lado, None)
        escena.collection.objects.link(pie); pie.parent = pinf; pie.rotation_mode = 'QUATERNION'
        malla_caja('g_pie_'+lado, (-3.5, -4, -2.2), (3.5, 15, 0), pie, cuero, escena)
        EXT[lado] = dict(sup=sup, inf=inf, mano=mano, psup=psup, pinf=pinf, pie=pie, sx=sx)


    # ---- paradas y pasos: la raíz interpola suave entre paradas; los pasos se
    # generan del camino (pies alternados, zancada ~25 u, el pie rezagado alcanza
    # al final de cada tramo para quedar plantado en la postura de llegada)
    # Matrix.Rotation(yaw,'Z') lleva el +Y local a (-sin, cos): para encarar
    # (dx, dy) el rumbo correcto es atan2(-dx, dy), NO atan2(dx, dy)
    PSI_A = math.atan2(-(EJE.x-95), 110.6-85)                # frente al torno
    PSI_B = math.atan2(105-128, 62-78)                       # frente al atril
    PSI_V = math.atan2(103-24, -76-68)                       # arranca la caminata de carga
    PSI_C = math.pi/2 - .35                                  # mirando el riel desde su costado
    PSI_V2 = math.atan2(-(33-27), 42+58)                     # camino de vuelta (+Y)
    PSI_P = math.atan2(-(34-33), 78-42)                      # último tramo, sigue el camino
    PSI_E = math.atan2(34-0, 50-78)                          # frente a la palanca
    PARADAS = [  # (frame, x, y, yaw)
        (F_PASO_ATRIL[0]-1, 95, 85, PSI_A),
        (F_PASO_ATRIL[1], 105, 78, PSI_B),
        (F_TIRAR[1], 105, 78, PSI_B),
        (F_TIRAR[1]+8, 103, 68, PSI_V),
        (F_LLEVAR[1], 24, -76, PSI_C),
        (F_ASIENTO, 24, -76, PSI_C),
        (F_SOLTAR[1]+2, 27, -58, PSI_V2),
        (F_AGARRE[0]-26, 33, 42, PSI_P),      # camina mirando el camino...
        (F_AGARRE[0]-14, 34, 78, PSI_E),      # ...y pivota al final hacia la palanca
    ]
    def zancada(pos, yaw, lado):
        fwd = Vector((-math.sin(yaw), math.cos(yaw)))   # mismo convenio que el torso
        per = Vector((fwd.y, -fwd.x))
        p = Vector(pos) + per*(6.8 if lado == 'D' else -6.8) - fwd*2
        return Vector((p.x, p.y, PISO+2.2))
    pies_pos = {'I': zancada((95, 85), PSI_A, 'I'), 'D': zancada((95, 85), PSI_A, 'D')}
    PASOS = []
    _lado = 'I'
    for a, b in zip(PARADAS, PARADAS[1:]):
        f0, f1 = a[0], b[0]
        pa, pb = Vector((a[1], a[2])), Vector((b[1], b[2]))
        L = (pb - pa).length
        if L < 8 or f1 - f0 < 10:
            continue
        n = max(1, round(L/38))
        sep = (f1 - f0 - 2) / (n + 1)
        dur = max(7, min(12, int(sep) - 1))
        for k in range(n + 1):        # último = el pie rezagado llega a la postura
            u = min(1.0, (k + 1) / n)
            pos = pa.lerp(pb, u)
            yaw_p = a[3] + envolver(b[3] - a[3]) * min(1.0, u + .2)
            f_ini = round(f0 + 1 + sep*k)
            PASOS.append((_lado, f_ini, f_ini + dur, zancada(pos, yaw_p, _lado)))
            _lado = 'D' if _lado == 'I' else 'I'

    # zona de la órbita del mango donde el guardia puede agarrar (elevación 0)
    M_rel0 = raiz.matrix_world.inverted() @ pitch.matrix_world
    EJE_MUNDO = raiz.matrix_world @ (M_rel0 @ EJE)
    rel_orb = MANGO0 - EJE
    r_orb = Vector((rel_orb.y, rel_orb.z)).length
    beta0 = math.atan2(rel_orb.z, rel_orb.y)
    hd = Vector((95, 85)) + rot2(Vector((10.5, 0)), PSI_A)
    HD = Vector((hd.x, hd.y, PISO+100.3))
    beta_cerca = math.atan2(HD.z-EJE_MUNDO.z, HD.y-EJE_MUNDO.y)
    LIM = 0.8
    ESPERA = EJE_MUNDO + Vector((rel_orb.x, r_orb*math.cos(beta_cerca+LIM), r_orb*math.sin(beta_cerca+LIM)))

    def mango_mundo(phi, M_rel):
        return raiz.matrix_world @ (M_rel @ (EJE + Matrix.Rotation(phi, 4, 'X') @ rel_orb))
    def gatillo_mundo(tirada, M_rel):
        return raiz.matrix_world @ (M_rel @ (GATILLO_PIVOTE + Matrix.Rotation(tirada, 4, 'X') @ (GATILLO_EMP-GATILLO_PIVOTE)))

    estado_mano = {l: dict(pose=None, agarre=False) for l in 'ID'}
    M_pitch_lanz = None; vuelo = None; congelado = None; impacto_f = None; pos_vuelo = None

    if accion_demo is not None:
        accion_demo.use_fake_user = True
        nodos = [brazo_i, brazo_d, pitch, volante, manivela, gatillo, cuerda_i, cuerda_d,
                 virote, virote_mano, guardia, cadera, cabeza, atril, giro360] \
                + [EXT[l][k] for l in 'ID' for k in ('sup', 'inf', 'mano', 'psup', 'pinf', 'pie')] \
                + list(vir_atril)
        for nd in nodos:
            nd.animation_data_create(); nd.animation_data.action = accion_demo
    return dict(escena=escena, informe=informe, raiz=raiz, giro360=giro360, pitch=pitch,
                brazo_i=brazo_i, brazo_d=brazo_d, brazos=brazos, cuerda_i=cuerda_i, cuerda_d=cuerda_d,
                virote=virote, virote_malla=virote_malla, mira_nodo=mira_nodo,
                base_brazo=base_brazo, base_pitch=base_pitch, punta=punta, ASIENTO=ASIENTO,
                ML=ML, ML_INV=ML_INV, c_local=c_local,
                volante=volante, manivela=manivela, gatillo=gatillo,
                PISO=PISO, atril=atril, M_ATRIL=M_ATRIL, M_ATRIL_TIRADO=M_ATRIL_TIRADO,
                vir_atril=vir_atril, virote_mano=virote_mano,
                guardia=guardia, cadera=cadera, cabeza=cabeza, EXT=EXT,
                PARADAS=PARADAS, PASOS=PASOS, pies_pos=pies_pos,
                EJE_MUNDO=EJE_MUNDO, rel_orb=rel_orb, r_orb=r_orb, beta0=beta0,
                beta_cerca=beta_cerca, LIM=LIM, ESPERA=ESPERA,
                mango_mundo=mango_mundo, gatillo_mundo=gatillo_mundo, estado_mano=estado_mano,
                blanco=blanco, virutas=virutas, vel_virutas=vel_virutas, cams=None, mats=mats)

# ----------------------------------------------------------------------------
def coreografiar(rig, con_render=True):
    """Bucle frame a frame: keyframea mecanismo + guardia (+ cámaras/blanco si
    con_render). Las claves caen en la acción asignada a cada nodo (ver montar).
    Devuelve dict(impacto_f=...) para los reportes."""
    raiz = rig['raiz']; pitch = rig['pitch']
    brazo_i, brazo_d, brazos, punta = rig['brazo_i'], rig['brazo_d'], rig['brazos'], rig['punta']
    virote = rig['virote']
    volante, manivela, gatillo = rig['volante'], rig['manivela'], rig['gatillo']
    base_brazo, base_pitch = rig['base_brazo'], rig['base_pitch']
    guardia, cadera, cabeza, EXT = rig['guardia'], rig['cadera'], rig['cabeza'], rig['EXT']
    vir_atril, virote_mano = rig['vir_atril'], rig['virote_mano']
    M_ATRIL, M_ATRIL_TIRADO = rig['M_ATRIL'], rig['M_ATRIL_TIRADO']
    ASIENTO, ML, ML_INV, c_local = rig['ASIENTO'], rig['ML'], rig['ML_INV'], rig['c_local']
    PISO, PARADAS, PASOS, pies_pos = rig['PISO'], rig['PARADAS'], rig['PASOS'], rig['pies_pos']
    EJE_MUNDO, ESPERA, LIM = rig['EJE_MUNDO'], rig['ESPERA'], rig['LIM']
    beta0, beta_cerca = rig['beta0'], rig['beta_cerca']
    mango_mundo, gatillo_mundo = rig['mango_mundo'], rig['gatillo_mundo']
    estado_mano = rig['estado_mano']
    blanco, virutas, vel_virutas = rig['blanco'], rig['virutas'], rig['vel_virutas']
    if con_render:
        camB, camC, camC_t, camD, camS, camA = rig['cams']
    M_pitch_lanz = None; vuelo = None; congelado = None; impacto_f = None; pos_vuelo = None
    mira_prev = None

    # ---- bucle frame a frame
    for f in range(1, TOTAL+1):
        t = f/FPS
        # p: 1=disparada, 0=tensa (convención de build_assets.sequences)
        if f <= F_TORNO[0]: p = 1.0
        elif f <= F_TORNO[1]: p = 1.0 - suave(abanico(f, *F_TORNO))
        elif f < F_LIBERACION: p = 0.0
        elif f <= F_BRAZOS_FIN: p = abanico(f, F_LIBERACION, F_BRAZOS_FIN)**.55
        else: p = 1.0
        giro = -REVOLUCIONES*math.tau*(1.0-p)
        elev = ELEVACION*suave(abanico(f, *F_ELEVAR))
        tirada = .42*suave(abanico(f, *F_TIRON))*(1-suave(abanico(f, F_BRAZOS_FIN+2, F_RECUADRO)))
        retro = .022*math.sin(math.pi*abanico(f, F_LIBERACION, F_RECUADRO)) if F_LIBERACION < f <= F_RECUADRO else 0.0

        # mecanismo
        for br, nombre in ((brazo_i, 'CTRL_BRAZO_I'), (brazo_d, 'CTRL_BRAZO_D')):
            br.rotation_euler = base_brazo[nombre] + ARM_DELTA[nombre]*p
            clave(br, f)
        pitch.rotation_euler = (base_pitch.x - elev - retro, base_pitch.y, base_pitch.z)
        clave(pitch, f)
        volante.rotation_euler = (giro, 0, 0); clave(volante, f)
        manivela.rotation_euler = (giro, 0, 0); clave(manivela, f)
        gatillo.rotation_euler = (tirada, 0, 0); clave(gatillo, f)
        if f == F_LIBERACION:
            bpy.context.view_layer.update(); M_pitch_lanz = pitch.matrix_world.copy()
        bpy.context.view_layer.update()
        M_raiz, M_pitch = raiz.matrix_world.copy(), pitch.matrix_world.copy()
        M_rel = M_raiz.inverted() @ M_pitch

        # cuerdas ancladas punta→centro (la matemática de sequences())
        centro = M_raiz @ Vector((0, (1.03-2.42*p)*S, CENTRO_Z))
        for nd, br in brazos:
            inicio = br.matrix_world @ punta[nd.name]      # matrix_world ya incluye el pitch
            direccion = centro - inicio
            M = Matrix.Translation(inicio) @ direccion.normalized().to_track_quat('Y', 'Z').to_matrix().to_4x4()
            ratio = direccion.length/nd['rest_length']
            fijar(nd, M @ Matrix.Diagonal((ratio, ratio, ratio, 1.0)), f, padre=M_pitch)

        # virote del riel: oculto → cargado (swap en F_ASIENTO) → vuelo → clavado
        if f < F_ASIENTO:
            virote.scale = (.001, .001, .001); virote.location = (0, 0, 0); clave(virote, f)
        elif f < F_LIBERACION:
            virote.scale = (1, 1, 1); virote.location = (0, 0, 0); clave(virote, f)
        else:
            if vuelo is None:
                pos0 = M_pitch_lanz @ (ML @ c_local)
                v0 = M_pitch_lanz.to_quaternion() @ Vector((0, -V0, 0))   # V0 a lo largo del riel ya elevado
                tt, vuelo = 0.0, [pos0]
                while len(vuelo) < 400:
                    tt += 1.0/FPS
                    vuelo.append(pos0 + v0*tt + Vector((0, 0, -.5*GRAVEDAD*tt*tt)))
                    if vuelo[-1].y <= -D_BLANCO or vuelo[-1].z <= Z_BLANCO-95: break
            i = f - F_LIBERACION
            if i < len(vuelo):
                pos = vuelo[i]; pos_vuelo = pos
                delta = pos - vuelo[max(0, i-1)]
                vdir = delta.normalized() if delta.length > 1e-9 else (M_pitch_lanz.to_quaternion() @ Vector((0, -1, 0)))
                q_vel = Vector((0, -1, 0)).rotation_difference(vdir)
                q = M_pitch_lanz.to_quaternion().slerp(q_vel, min(1.0, i/12.0))
                if congelado is None and (pos.y <= -D_BLANCO or pos.z <= Z_BLANCO-95):
                    impacto_f = f
                    congelado = Matrix.Translation(pos - vdir*130) @ q.to_matrix().to_4x4() @ ML_INV
                fijar(virote, congelado or (Matrix.Translation(pos) @ q.to_matrix().to_4x4() @ ML_INV),
                      f, padre=M_pitch_lanz)
            else:
                clave(virote, f)

        # ---- guardia: raíz, cadera, pies
        if f <= PARADAS[0][0]: px, py, yaw = PARADAS[0][1], PARADAS[0][2], PARADAS[0][3]
        elif f >= PARADAS[-1][0]: px, py, yaw = PARADAS[-1][1], PARADAS[-1][2], PARADAS[-1][3]
        else:
            i = next(j for j, s in enumerate(PARADAS) if f <= s[0])
            a, b = PARADAS[i-1], PARADAS[i]
            u = suave(abanico(f, a[0], b[0]))
            px, py = a[1]+(b[1]-a[1])*u, a[2]+(b[2]-a[2])*u
            yaw = a[3]+envolver(b[3]-a[3])*u
        rec = abanico(f, F_LIBERACION, F_LIBERACION+4)*(1-suave(abanico(f, F_LIBERACION+5, F_RECUADRO)))
        doblar = suave(abanico(f, F_ALCANCE[0]-4, F_ALCANCE[0]+8))*(1-suave(abanico(f, F_TIRAR[1]+6, F_TIRAR[1]+18)))
        lean_torno = .22*suave(abanico(f, F_TORNO[0]+6, F_TORNO[0]+20))*(1-suave(abanico(f, F_TORNO[1]-14, F_TORNO[1]-2)))
        lean_colocar = .25*suave(abanico(f, F_COLOCAR[0]-6, F_COLOCAR[0]))*(1-suave(abanico(f, F_SOLTAR[0], F_SOLTAR[1])))
        en_paso = any(s[1] <= f <= s[2] for s in PASOS)
        M_raiz_g = Matrix.Translation((px, py, PISO)) @ Matrix.Rotation(yaw, 4, 'Z')
        M_guardia = M_raiz_g @ Matrix.Translation((0, -5.0*rec, 0))
        fijar(guardia, M_guardia, f)
        fwd = Vector((-math.sin(yaw), math.cos(yaw), 0))
        zc = 56.3 - 21*doblar + math.sin(t*math.tau*.4)*.7 + (1.2 if en_paso else 0)
        # altura de cadera "a la medida": el pie plantado más estirado tiene que
        # seguir al alcance de la pierna (30+30 u) mientras la raíz camina
        d_peor = 0.0
        for l in 'ID':
            if any(s[0] == l and s[1] <= f <= s[2] for s in PASOS):
                continue                                   # pie en el aire: no limita
            hx = Vector((px, py)) + rot2(Vector((6.8 if l == 'D' else -6.8, 0)), yaw)
            d_peor = max(d_peor, (hx - Vector((pies_pos[l].x, pies_pos[l].y))).length)
        zc = min(zc, 3.2 + math.sqrt(max(0.0, 58.0*58.0 - d_peor*d_peor)))
        M_cadera = M_raiz_g @ Matrix.Translation((0, 0, zc)) @ Matrix.Rotation(-(.52*doblar + lean_torno + lean_colocar), 4, 'X')
        fijar(cadera, M_cadera, f, padre=M_guardia)
        RZ = Matrix.Rotation(yaw, 4, 'Z')
        for lado in 'ID':
            paso = next((s for s in PASOS if s[0] == lado and s[1] <= f <= s[2]), None)
            if paso:
                u = suave(abanico(f, paso[1], paso[2]))
                destino = pies_pos[lado].lerp(paso[3], u) + Vector((0, 0, 6.5*math.sin(math.pi*u)))
                if f == paso[2]: pies_pos[lado] = Vector(paso[3])
            else:
                destino = pies_pos[lado]
            cadera_p = M_cadera @ Matrix.Translation((EXT[lado]['sx']*6.8, 0, -1))
            ik2(EXT[lado]['psup'], EXT[lado]['pinf'], EXT[lado]['pie'],
                cadera_p.translation, destino, cadera_p.translation + fwd*40, 30, 30, f, cadera_p, plano=RZ)

        # matriz del virote en mano (una sola fuente de verdad), pensada por su
        # CENTRO (c_local): tirón en el atril → centro al costado del guardia
        # (punto de equilibrio, a la altura del pecho) → centro al riel. M_vm se
        # reconstruye como T(pos − q@c_local)@q, así el centro va exactamente a
        # donde lo planeamos y en F_ASIENTO cae clavado en la matriz ASIENTO.
        M_vm = None
        if F_TIRAR[0] <= f < F_ASIENTO:
            if f <= F_TIRAR[1]:
                M_vm = M_ATRIL @ Matrix.Translation((0, -26*suave(abanico(f, *F_TIRAR)), 0))
            else:
                centro_deseado = (M_raiz_g @ Matrix.Translation((12, 6, 100))).translation
                if f < F_COLOCAR[0]:
                    u = suave(abanico(f, F_TIRAR[1], F_COLOCAR[0]))
                    q = M_ATRIL_TIRADO.rotation.to_quaternion().slerp(ASIENTO.rotation.to_quaternion(), u)
                    pos = (M_ATRIL_TIRADO @ c_local).lerp(centro_deseado, u)
                else:
                    u = suave(abanico(f, F_COLOCAR[0], F_ASIENTO))
                    q = ASIENTO.rotation.to_quaternion()
                    pos = centro_deseado.lerp(ASIENTO @ c_local, u)
                M_vm = Matrix.Translation(pos - q @ c_local) @ q.to_matrix().to_4x4()

        # cabeza: torno → mango → virote (atril o en mano) → camino de vuelta → boca → vuelo → blanco
        if f < F_TORNO[0]: mira_c = EJE_MUNDO
        elif f < F_ALCANCE[0]: mira_c = mango_mundo(giro, M_rel)
        elif f < F_TIRAR[1]: mira_c = M_ATRIL @ (c_local + Vector((0, -140, 0)))
        elif f < F_ASIENTO: mira_c = M_vm @ c_local
        elif f < F_AGARRE[0]: mira_c = M_raiz_g @ Vector((0, 100, 30))
        elif f < F_LIBERACION: mira_c = M_raiz @ (M_rel @ Vector((0, -224, 19.6)))
        elif pos_vuelo is not None and impacto_f is None: mira_c = pos_vuelo
        else: mira_c = Vector((0, -D_BLANCO, Z_BLANCO))
        if mira_prev is None: mira_prev = Vector(mira_c)
        mira_c = mira_prev.lerp(Vector(mira_c), min(1, 6/FPS))   # sin cortes secos de mirada
        mira_prev = Vector(mira_c)
        pivote_cab = M_cadera @ Vector((0, .8, 52))
        fijar(cabeza, apuntar_Y(pivote_cab, mira_c), f, padre=M_cadera)

        # manos: reposo, manivela con regrip, carga a dos manos, palanca, sobresalto
        hombroI = (M_cadera @ Matrix.Translation((-10.5, 0, 44))).translation
        hombroD = (M_cadera @ Matrix.Translation((10.5, 0, 44))).translation
        reposo = lambda h, sx: h + Matrix.Rotation(yaw, 3, 'Z') @ Vector((sx*3, 1, -47))
        objI, objD = reposo(hombroI, -1), reposo(hombroD, 1)
        en_torno = F_TORNO[0] <= f <= F_TORNO[1]+3
        if en_torno:
            mango = mango_mundo(giro, M_rel)
            en_zona = abs(envolver(beta0 + giro - beta_cerca)) < LIM
            for lado, dx in (('D', 3.0), ('I', -6.0)):
                st = estado_mano[lado]
                if st['agarre']:
                    if en_zona: st['pose'] = mango + Vector((dx, 0, 0))
                    else: st['agarre'] = False
                else:
                    st['pose'] += (ESPERA+Vector((dx, 0, 0))-st['pose'])*min(1, 6/FPS)
                    if en_zona and (st['pose']-mango).length < 8: st['agarre'] = True
        else:
            if M_vm is not None:
                objD = M_vm @ (c_local + Vector((0, -10, 0)))
                objI = M_vm @ (c_local + Vector((0, 10, 0))) if f >= F_LLEVAR[0]+4 else reposo(hombroI, -1)
            elif F_AGARRE[0]-2 <= f <= F_RECUADRO:
                objD = gatillo_mundo(tirada, M_rel)
            if F_LIBERACION <= f <= F_RECUADRO:
                sacudida = math.sin(math.pi*abanico(f, F_LIBERACION, F_RECUADRO))
                objD += Vector((6, 4, 14))*sacudida; objI += Vector((-6, 4, 14))*sacudida
        for lado, h, obj, sx in (('I', hombroI, objI, -1), ('D', hombroD, objD, 1)):
            st = estado_mano[lado]
            if st['pose'] is None: st['pose'] = Vector(obj)
            if en_torno:
                pass                 # durante el torno manda la máquina de estados
            elif M_vm is not None and (lado == 'D' or f >= F_LLEVAR[0]+4):
                st['pose'] = Vector(obj)   # empuñadura firme: la mano sigue al virote
            else:
                st['pose'] += (Vector(obj)-st['pose'])*min(1, 12/FPS)
            polo = h + Matrix.Rotation(yaw, 3, 'Z') @ Vector((sx, -.2, -.75))*30
            ik2(EXT[lado]['sup'], EXT[lado]['inf'], EXT[lado]['mano'], h, st['pose'], polo, 27, 25, f,
                M_cadera @ Matrix.Translation((sx*10.5, 0, 44)))

        # virote en mano y atril (swap invisible: mano→riel en F_ASIENTO)
        if M_vm is not None:
            fijar(virote_mano, M_vm, f)
        else:
            virote_mano.scale = (.001, .001, .001); clave(virote_mano, f)
        vir_atril[1].scale = (1, 1, 1) if f < F_TIRAR[0] else (.001, .001, .001)
        clave(vir_atril[1], f)
        if f < F_TIRAR[0]:
            for v in (vir_atril[0], vir_atril[2]): clave(v, f)

        # juego: sin blanco físico, el virote disparado se desvanece tras el
        # impacto (si no, quedaría clavado en el aire a 80 m de la torre)
        if not con_render and impacto_f is not None and f == min(impacto_f+8, TOTAL):
            virote.scale = (.001, .001, .001); clave(virote, f)

        if con_render:
            # blanco: sacudida y virutas al impacto
            if impacto_f is not None and f >= impacto_f:
                dt = (f-impacto_f)/FPS
                blanco.rotation_euler = (.05*math.exp(-dt*3.5)*math.sin(dt*math.tau*3.2), 0, 0)
                clave(blanco, f)
                p0 = Vector((0, -D_BLANCO, Z_BLANCO))
                for i, (v, vv) in enumerate(zip(virutas, vel_virutas)):
                    tt = dt - .02*i
                    if 0 < tt < .5:
                        posv = p0 + vv*tt + Vector((0, 0, -.5*GRAVEDAD*tt*tt))
                        fijar(v, Matrix.Translation((posv.x, posv.y, max(posv.z, 2))), f)
                    else:
                        v.scale = (.001, .001, .001); clave(v, f)
            else:
                blanco.rotation_euler = (0, 0, 0); clave(blanco, f)
                for v in virutas: v.scale = (.001, .001, .001); clave(v, f)

        if con_render:
            # deriva sutil de cámaras
            uB = abanico(f, *F_TORNO)
            camB.location = (330-28*uB, 430-24*uB, 655); clave(camB, f)
            uC = abanico(f, F_PASO_ATRIL[0]-3, F_ASIENTO)
            camC.location = (330-40*uC, -120+60*uC, 730-20*uC); clave(camC, f)
            camC_t.location = Vector((60, 20, 560)).lerp(Vector((0, -76, 595)), uC); clave(camC_t, f)
            uD = abanico(f, F_ELEVAR[0]-9, F_MIRA[0]-1)
            camD.location = (430-30*uD, 480-30*uD, 760-35*uD); clave(camD, f)
            camS.data.lens = 50+35*suave(abanico(f, *F_MIRA)); camS.data.keyframe_insert('lens', frame=f)
            a2 = math.radians(215+42*f/TOTAL)
            camA.location = (1150*math.cos(a2), 1150*math.sin(a2)-100, 880-70*abanico(f, F_EPILOGO, TOTAL)); clave(camA, f)

    # claves frame a frame: interpolación lineal; todo el easing vive en los valores
    for accion in bpy.data.actions:
        for capa in accion.layers:
            for tira in capa.strips:
                for bolsa in tira.channelbags:
                    for fc in bolsa.fcurves:
                        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'


    return dict(impacto_f=impacto_f, pos_vuelo=pos_vuelo)

# ----------------------------------------------------------------------------
def main():
    escena = bpy.context.scene
    ruta_tex = Path(CFG['extracted'])/'textures'
    if ruta_tex.exists():
        bpy.context.preferences.addons['io_scene_nifly'].preferences.sky_texture_path_1 = str(ruta_tex)
    rig = montar(con_render=True)
    informe = rig['informe']
    pitch, base_pitch, mira_nodo = rig['pitch'], rig['base_pitch'], rig['mira_nodo']

    # ---- piso, luces, mundo
    bpy.ops.mesh.primitive_plane_add(size=13000, location=(0, -2800, -2))
    bpy.context.object.data.materials.append(material('Piso_estudio', (.11, .13, .15)))
    def luz(nombre, pos, potencia, tam, mira):
        d = bpy.data.lights.new(nombre, 'AREA'); d.energy = potencia; d.shape = 'DISK'; d.size = tam
        o = bpy.data.objects.new(nombre, d); escena.collection.objects.link(o); o.location = pos
        o.rotation_euler = (Vector(mira)-o.location).to_track_quat('-Z', 'Y').to_euler()
    luz('Key', (-450, -750, 1100), 7000000, 650, (0, 0, 320))
    luz('Fill', (800, -350, 600), 3500000, 500, (0, 0, 320))
    luz('Rim', (200, 650, 1000), 5000000, 600, (0, 0, 320))
    luz('LuzBlanco', (150, -D_BLANCO+700, 1000), 5000000, 700, (0, -D_BLANCO, 300))
    escena.world.color = (.32, .32, .32)


    # ---- render
    escena.render.engine = 'CYCLES'; escena.cycles.samples = MUESTRAS
    escena.cycles.use_denoising = True
    escena.render.resolution_x, escena.render.resolution_y = ANCHO, ALTO
    escena.render.resolution_percentage = 100
    escena.render.fps = FPS; escena.render.use_motion_blur = True
    escena.view_settings.view_transform = 'AgX'
    escena.view_settings.look = 'AgX - Medium High Contrast'
    escena.view_settings.exposure = .75
    escena.render.image_settings.file_format = 'FFMPEG'
    escena.render.ffmpeg.format = 'MPEG4'; escena.render.ffmpeg.codec = 'H264'
    escena.render.ffmpeg.constant_rate_factor = 'HIGH'; escena.render.ffmpeg.audio_codec = 'NONE'
    escena.frame_start, escena.frame_end = 1, TOTAL


    # ---- cámaras: una por plano, cambian por marcas de tiempo
    pitch.rotation_euler = (base_pitch.x - ELEVACION, base_pitch.y, base_pitch.z)
    bpy.context.view_layer.update()
    POS_MIRA = mira_nodo.matrix_world.translation.copy()
    pitch.rotation_euler = base_pitch
    bpy.context.view_layer.update()

    cams = {}
    def camara(nombre, pos, mira, lente=45, clip=12):
        d = bpy.data.cameras.new(nombre); d.lens = lente; d.clip_start = clip; d.clip_end = 14000
        o = bpy.data.objects.new(nombre, d); escena.collection.objects.link(o); o.location = pos
        t = bpy.data.objects.new(nombre+'_mira', None); escena.collection.objects.link(t); t.location = mira
        c = o.constraints.new('TRACK_TO'); c.target = t
        c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
        cams[nombre] = (o, t)
        return o, t
    a0 = math.radians(215)
    camA, _ = camara('CamTorre', (1150*math.cos(a0), 1150*math.sin(a0)-100, 880), (0, -100, 420), 45, 20)
    camB, _ = camara('CamManivela', (330, 430, 655), (60, 95, 595), 55, 10)
    camC, camC_t = camara('CamCarga', (330, -120, 730), (60, 20, 560), 50, 10)
    camD, _ = camara('CamApuntado', (430, 480, 760), (10, 40, 640), 48, 10)
    camS, _ = camara('CamMira', POS_MIRA, (0, -D_BLANCO, Z_BLANCO), 50, 5)
    camE, _ = camara('CamDisparo', (560, -280, 690), (0, -140, 655), 40, 12)
    camF, _ = camara('CamBlanco', (170, -D_BLANCO+380, Z_BLANCO+80), (0, -D_BLANCO, Z_BLANCO), 38, 12)
    escena.camera = camA
    for f, c in ((1, camA), (F_TORNO[0], camB), (F_PASO_ATRIL[0]-3, camC), (F_ELEVAR[0]-9, camD),
                 (F_MIRA[0], camS), (F_CAM_E[0], camE), (F_CAM_F0, camF), (F_EPILOGO, camA)):
        escena.timeline_markers.new('c%d' % f, frame=f).camera = c
    rig['cams'] = (camB, camC, camC_t, camD, camS, camA)

    res = coreografiar(rig, con_render=True)
    impacto_f = res['impacto_f']

    # ---- salidas
    escena.render.filepath = str(ROOT/'renders/Astra_guardia_disparo.mp4')
    bpy.ops.render.render(animation=True)
    if GUARDAR_BLEND:
        bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'renders/Astra_guardia_disparo.blend'))
    sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
    (ROOT/'reports/animacion_guardia.json').write_text(json.dumps({
        'proposito': 'Demo animada del ciclo completo: manivela, carga, apuntado y disparo.',
        'fps': FPS, 'frames': TOTAL, 'duracion_s': round(TOTAL/FPS, 2),
        'fases': {'torno': F_TORNO, 'carga': [F_PASO_ATRIL, F_ALCANCE, F_TIRAR, F_LLEVAR, F_COLOCAR, F_ASIENTO],
                  'apuntado': [F_ELEVAR, F_AGARRE, F_MIRA, F_TIRON],
                  'liberacion': F_LIBERACION, 'impacto_estimado': F_IMPACTO,
                  'impacto_real': impacto_f, 'epilogo': F_EPILOGO},
        'virote': {'v0_u_s': V0, 'elevacion_grados': math.degrees(ELEVACION),
                   'blanco': [0, -round(D_BLANCO, 1), Z_BLANCO], 'distancia_m': round(D_BLANCO/S, 1)},
        'cirugia_en_memoria': {'caras_borradas': informe,
                               'nota': 'solo la copia importada; los NIF en disco no se tocan'},
        'camaras': sorted(cams), 'texturas_vanilla': bool(ruta_tex.exists()),
        'nif_sha256': {n: sha(ROOT/'mod/meshes/AstraAsedio'/f'{n}.nif') for n in ('torre', 'ballesta')},
        'salidas': ['renders/Astra_guardia_disparo.mp4', 'renders/Astra_guardia_disparo.blend'],
    }, indent=2))
    print('LISTO: %d frames (%.1f s) -> %s' % (TOTAL, TOTAL/FPS, escena.render.filepath))

if __name__ == '__main__':
    main()
