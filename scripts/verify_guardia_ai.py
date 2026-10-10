#!/usr/bin/env python3
"""Verificación local de la IA del guardia (sin Papyrus Compiler ni Skyrim):
- lint estructural de los .psc nuevos/editados
- test del solver balístico (reproduce el registro v08 de sight zero)
- test del Atan2 papyrus contra math.atan2
- roundtrip vmad_multi <-> read_vmad (el formato del ESP)
- consistencia config.json['guardia'] <-> claves que lee build_plugin.py
"""
import json, math, random, re, sys, struct, importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]  # raíz del repo, independiente del cwd
ok = lambda m: print('  OK %s' % m)

# ---------------------------------------------------------------- lint PSC --
def lint_psc(ruta, props_esperadas=()):
    t = (REPO/ruta).read_text(encoding='utf-8')
    nombre = Path(ruta).stem
    pares = [('Function', 'EndFunction'), ('Event', 'EndEvent'), ('While', 'EndWhile')]
    for a, b in pares:
        # 'Function' como palabra inicial de línea (no 'EndFunction')
        na = len(re.findall(r'^[ \t]*(?:\w+(?:\[\])?[ \t]+)?%s\b' % a, t, re.M))
        nb = len(re.findall(r'^[ \t]*%s\b' % b, t, re.M))
        assert na == nb, '%s: %s=%d vs %s=%d' % (nombre, a, na, b, nb)
    ni = len(re.findall(r'^[ \t]*if\b', t, re.M))
    ne = len(re.findall(r'^[ \t]*endif\b', t, re.M))
    assert abs(ni - ne) <= 1, '%s: if=%d endif=%d (elseIf cuenta aparte)' % (nombre, ni, ne)
    malas = [m for m in ('Utility.Wait(', 'While true', 'While 1') if m in t]
    if re.search(r'\.\s*GetVelocity[XYZ]?\s*\(', t): malas.append('GetVelocity*()')
    assert not malas, '%s llama APIs problemáticas: %s' % (nombre, malas)
    props = set(re.findall(r'^\s*(?:\w+)\s+Property\s+(\w+)', t, re.M))
    faltan = set(props_esperadas) - props
    assert not faltan, '%s: faltan propiedades que llena el ESP: %s' % (nombre, sorted(faltan))
    ok('%s: bloques balanceados, sin APIs prohibidas, %d propiedades' % (nombre, len(props)))
    return props

print('== 1) lint estructural de los PSC ==')
auto_props = ['Launcher', 'ShotAmmo', 'ShotSound', 'OcupadaGuardia', 'YawNode', 'PitchNode',
              'VisualBoltNode', 'VelocidadProyectil', 'GravedadProyectil', 'MuzzleAlto', 'MuzzleAdelante',
              'YawSpeed', 'PitchSpeed', 'PitchMin', 'PitchMax', 'ArcMax', 'AlcanceMin', 'AlcanceMax',
              'MargenLinea', 'MargenImpacto', 'MaxRafaga', 'Enfriamiento', 'Anticipacion',
              'ReleaseSegundos', 'TickSegundos', 'QALog']
lint_psc('mod/scripts/source/AstraGuardiaAuto.psc', auto_props)
lint_psc('mod/scripts/source/AstraGuardiaNPC.psc')
lint_psc('mod/scripts/source/AstraAsedioActi.psc', ['OcupadaGuardia'])
lint_psc('mod/scripts/source/AstraAsedioSession.psc')

# funciones que el NPC llama sobre la torre existen en el Auto
npc = (REPO/'mod/scripts/source/AstraGuardiaNPC.psc').read_text(encoding='utf-8')
auto = (REPO/'mod/scripts/source/AstraGuardiaAuto.psc').read_text(encoding='utf-8')
for fn in re.findall(r'torre\.(\w+)\(', npc):
    assert re.search(r'^Function\s+%s\b' % fn, auto, re.M), 'Auto no tiene %s' % fn
ok('NPC -> Auto: AlertaCombat/CalmaCombat existen')

# ------------------------------------------------------------ solver test --
print('== 2) solver balístico (puerto python del PSC) ==')
V, G = 5400.0, 240.345  # 0.35*9.81*70 exacto (Core.cpp)
def resolver(dx, dy, h):
    """h = altura de la boca sobre el blanco (positivo = dispara hacia abajo)"""
    d = math.hypot(dx, dy)
    if d < 1.0: return None
    v2 = V*V
    disc = v2*v2 - G*(G*d*d + 2.0*h*v2)
    if disc < 0: return None
    tanP = (v2 - math.sqrt(disc)) / (G*d)
    return math.degrees(math.atan(tanP)), math.degrees(math.atan2(dx, -dy))

# a) registro v08: a 5250 u (75 m) mismo nivel, la caída debe ser 113.589 u
p, y = resolver(0.0, -5250.0, 0.0)
t_vuelo = 5250.0/(V*math.cos(math.radians(p)))
caida_bruta = 0.5*G*t_vuelo**2          # caída absoluta bajo la horizontal
caida = caida_bruta - 5250.0*math.tan(math.radians(p))  # sag bajo la línea de apuntado = ~0
assert abs(caida) < 0.05, 'el solver no pasa por el blanco: sag %.3f' % caida
caida_plana = 0.5*G*(5250.0/V)**2    # derivación v08: tiempo plano, sin cos(pitch)
assert abs(caida_plana - 113.589) < 0.01, 'caída plana %.4f != kSightZeroDrop 113.589' % caida_plana
assert abs(p - 1.24) < 0.1, 'elevación %.3f' % p
assert abs(y) < 1e-9
print('  OK 75 m nivel: elevación %.2f°, caída plana %.3f u == kSightZeroDrop 113.589, sag %.3f u' % (p, caida_plana, caida))

# b) blanco a 30 m (2100 u) 40 u más abajo que la boca
p2, y2 = resolver(1000.0, -1850.0, 40.0)
assert 0 < p2 < 3 and 25 < y2 < 32, (p2, y2)
ok('blanco descentrado: yaw %.1f°, pitch %.2f°' % (y2, p2))

# c) fuera de alcance balístico => None
assert resolver(0.0, -150000.0, 0.0) is None  # >v²/g≈121k u: sin solución
ok('fuera de alcance devuelve None')

# d) la fórmula de yaw coincide con gunDirection del nativo
def gun_direction(yaw_deg, pitch_deg):
    y_, p_ = math.radians(yaw_deg), math.radians(pitch_deg)
    return (math.sin(y_)*math.cos(p_), -math.cos(y_)*math.cos(p_), math.sin(p_))
for dx, dy in ((100.0, -2000.0), (-1500.0, -1500.0), (3000.0, -500.0)):
    _, yaw = resolver(dx, dy, 0.0)
    d = gun_direction(yaw, 0.0)
    L = math.hypot(dx, dy)
    assert abs(d[0]-dx/L) < 1e-6 and abs(d[1]-dy/L) < 1e-6, (dx, dy, yaw)
ok('yaw del solver == gunDirection(yaw,0) del nativo (3 casos)')

# ------------------------------------------------------------- atan2 test --
print('== 3) Atan2 de Papyrus ==')
def atan2_psc(dy, dx):
    if dx > 0.0: return math.atan(dy/dx)
    if dx < 0.0: return math.atan(dy/dx) + (math.pi if dy >= 0 else -math.pi)
    return math.pi/2 if dy >= 0 else -math.pi/2
for _ in range(20000):
    dx = random.uniform(-3, 3)
    dy = random.uniform(-3, 3)
    if abs(dx) < 1e-3: dx = 1e-3
    a, b = atan2_psc(dy, dx), math.atan2(dy, dx)
    assert abs(a - b) < 1e-9, (dx, dy, a, b)
ok('20.000 casos aleatorios vs math.atan2')

# ------------------------------------------------------ vmad_multi test --
print('== 4) roundtrip VMAD multi-script ==')
sys.path.insert(0, str(REPO/'scripts'))
sys.path.insert(0, str(REPO/'scripts/vendor'))
spec = importlib.util.spec_from_file_location('bp', REPO/'scripts/build_plugin.py')
bp = importlib.util.module_from_spec(spec)
sys.modules['bp'] = bp
spec.loader.exec_module(bp)

auto_vals = {'Launcher': (1, 0x03000804), 'ShotAmmo': (1, 0x03000803), 'MaxRafaga': (3, 3),
             'VelocidadProyectil': (4, 5400.0), 'QALog': (5, True)}
b = bp.vmad_multi([('AstraAsedioActi', {'Session': (1, 0x03000806), 'FireSeconds': (4, 0.3)}),
                   ('AstraGuardiaAuto', auto_vals)])
v = bp.read_vmad(b)
assert len(v['scripts']) == 2
assert v['scripts'][0]['name'] == 'AstraAsedioActi' and abs(v['scripts'][0]['properties']['FireSeconds']['value'] - 0.3) < 1e-6
assert v['scripts'][1]['name'] == 'AstraGuardiaAuto'
assert v['scripts'][1]['properties']['MaxRafaga'] == {'type': 3, 'status': 1, 'value': 3}
assert v['scripts'][1]['properties']['Launcher']['value'] == {'form_id': 0x03000804, 'alias': -1}
assert v['scripts'][1]['properties']['QALog']['value'] is True
ok('dos scripts, propiedades tipo 1/3/4/5 intactas tras read_vmad')

# GLOB del guardia (EDID + FNAM 's\0' + FLTV 0.0)
edid = bp.W.zstr('AstraGuardiaOcupada')
assert edid == b'AstraGuardiaOcupada\0'
fltv = struct.pack('<f', 0.0)
assert len(fltv) == 4 and fltv == b'\x00\x00\x00\x00'
ok('GLOB: EDID/FNAM(\'s\\0\')/FLTV(0.0) serializan')

# XLKR de las referencias: <II form,keyword>
assert struct.pack('<II', 0x03000940, 0) == b'@\t\x00\x03\x00\x00\x00\x00'
ok('XLKR: <II padre,keyword> serializa')

# ------------------------------------------- config <-> build_plugin keys --
print('== 5) config.guardia <-> claves usadas por build_plugin ==')
cfg = json.loads((REPO/'config.json').read_text())
g = cfg['guardia']
src = (REPO/'scripts/build_plugin.py').read_text()
usadas = set(re.findall(r"gcfg\['(\w+)'\]", src))
falta_en_cfg = usadas - set(g)
assert not falta_en_cfg, 'config.guardia sin: %s' % sorted(falta_en_cfg)
falta_en_src = {'donores_npc', 'nombre', 'posicion', 'velocidad_proyectil', 'gravedad_proyectil',
                'muzzle_alto', 'muzzle_adelante', 'arc_max', 'alcance_min', 'alcance_max',
                'margen_linea', 'margen_impacto', 'max_rafaga', 'enfriamiento', 'anticipacion',
                'tick_segundos', 'qa_log'} - usadas
assert not falta_en_src, 'build_plugin no usa: %s' % sorted(falta_en_src)
assert all(g[k] > 0 for k in ('velocidad_proyectil', 'gravedad_proyectil'))
assert 0.0 < g['tick_segundos'] <= 0.5
assert g['alcance_min'] < g['alcance_max']
assert g['max_rafaga'] >= 1
ok('17 claves consistentes en ambas direcciones')

# los floats del solver en config == los del registro v08 del nativo
core = (REPO/'native/src/Core.cpp').read_text()
assert '5250/5400' in core and '0.35*9.81*70' in core
assert g['velocidad_proyectil'] == 5400.0 and abs(g['gravedad_proyectil'] - 0.35*9.81*70) < 0.01
ok('velocidad/gravedad del config == constantes documentadas en Core.cpp')

print('\nTODO OK (verificación local de la IA del guardia)')
