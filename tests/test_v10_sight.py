"""v10 tail sight: constants, the pure-Python pose, the written NIF and the native contract.

Evidence: reports/user_evidence_v09.json (camera pulled toward the player head by the pedestal
collision; user choice: camera at the tail sliding forward with elevation, rear ring + front post).
These are data and source contracts plus the Python port of Astra::sightPose; no engine runs here.
"""
import hashlib, json, math, re, struct, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts')); sys.path.insert(0, str(ROOT/'scripts/vendor'))
import nif_nodos, sight_pose as S
from parser_esm import Plugin

CFG = json.loads((ROOT/'config.json').read_text())
NIF = ROOT/'mod/meshes/AstraAsedio/ballesta.nif'


def nodes():
    return {n['nombre']: n for n in nif_nodos.leer(str(NIF))['nodos'].values()}


def native_constants():
    source = (ROOT/'native/src/Core.cpp').read_text()
    m = re.search(r'constexpr double kPoseZeroRange=([\d.]+),kPoseZeroDrop=([\d.]+),kFrontPostAlong=([\d.]+),kTailDistance=([\d.]+),kMinCameraHeight=([\d.]+),kMinCameraDistance=([\d.]+);', source)
    return [float(v) for v in m.groups()] if m else None


def rx(a, v):
    c, s = math.cos(a), math.sin(a)
    return (v[0], c*v[1]-s*v[2], s*v[1]+c*v[2])


def rz(a, v):
    c, s = math.cos(a), math.sin(a)
    return (c*v[0]-s*v[1], s*v[0]+c*v[1], v[2])


def pose_at(yaw, elevation):
    pivot = (0, 0, CFG['pitch_pivot_units'])
    frame = lambda v: rz(math.radians(yaw), rx(-math.radians(elevation), v))
    world = lambda v: S.add(pivot, frame(v))
    rear = world(tuple(CFG['camera_local_units'])); muzzle = world((0, -224, 19.6))
    return S.pose(rear, frame((-1, 0, 0)), muzzle, frame((0, -1, 0)), (0, 0, 0), (0, 0, 1)), frame, pivot


class Constants(unittest.TestCase):
    def test_python_and_native_constants_come_from_config_esp_and_nif(self):
        plugin = Plugin(ROOT/'mod/AstraAsedio.esp')
        proj = next(dict(plugin.subrecords(plugin.datos(o)))['DATA'] for t, o, n, d in plugin.recorrer() if t == 'PROJ')
        gravity, speed = struct.unpack_from('<ff', proj, 4)
        zero = CFG['sight_zero_meters'] * CFG['meters_to_units']
        drop = .5 * gravity * 9.81 * CFG['meters_to_units'] * (zero / speed) ** 2
        along = CFG['camera_local_units'][1] - CFG['sight']['front_post_local_y']
        expected = [zero, drop, along, CFG['sight']['tail_distance_units'], CFG['sight']['min_camera_height_units'], CFG['sight']['min_camera_distance_units']]
        python = [S.ZERO_RANGE, S.ZERO_DROP, S.FRONT_POST_ALONG, S.TAIL_DISTANCE, S.MIN_CAMERA_HEIGHT, S.MIN_CAMERA_DISTANCE]
        native = native_constants()
        self.assertIsNotNone(native, 'sight pose constants missing from Core.cpp')
        for name, e, p, n in zip(('range', 'drop', 'post', 'tail', 'height', 'distance'), expected, python, native):
            with self.subTest(constant=name):
                self.assertAlmostEqual(p, e, delta=max(1e-3, abs(e)*1e-5))
                self.assertEqual(p, n)

    def test_camera_floor_keeps_the_sweep_clear_of_the_pedestal(self):
        # The v09 log fitted the engine camera sphere at ~12-15 u; keep 30 u above the pedestal box.
        self.assertGreaterEqual(S.MIN_CAMERA_HEIGHT - CFG['sight']['pedestal_collision_height_units'], 30.0)


class Pose(unittest.TestCase):
    def test_camera_post_and_target_are_collinear_everywhere(self):
        for yaw in (0, 90, 180, 270):
            for elevation in (-5, 0, 20, 35, 45, 60, 80):
                p, frame, pivot = pose_at(yaw, elevation)
                with self.subTest(yaw=yaw, elevation=elevation):
                    a = S.unit(S.sub(p['front_post'], p['camera'])); b = S.unit(S.sub(p['target'], p['camera']))
                    self.assertLess(S.norm(S.cross(a, b)), 1e-9)
                    self.assertTrue(p['camera'][2] >= S.MIN_CAMERA_HEIGHT - 1e-6 or p['distance'] == S.TAIL_DISTANCE)

    def test_tail_at_flat_fire_and_slide_at_high_elevation(self):
        flat, frame, pivot = pose_at(0, 0)
        self.assertEqual(flat['distance'], S.TAIL_DISTANCE)
        self.assertAlmostEqual(flat['camera'][1], 200.0, delta=.05)
        high, frame, pivot = pose_at(0, 80)
        self.assertLess(high['distance'], 20.0)
        previous = 1e9
        for elevation in range(-5, 81, 5):
            d = pose_at(0, elevation)[0]['distance']
            self.assertLessEqual(d, previous + 1e-9); previous = d

    def test_golden_values_shared_with_the_native_suite(self):
        # The same numbers are asserted in native/tests/v10_tests.cpp against Astra::sightPose.
        for elevation, distance, post_z in ((0, 120.0, 34.451), (45, 86.048, 35.768), (80, 16.432, 38.304)):
            p, frame, pivot = pose_at(0, elevation)
            local = rx(math.radians(elevation), S.sub(p['front_post'], pivot))
            with self.subTest(elevation=elevation):
                self.assertAlmostEqual(p['distance'], distance, delta=1e-3)
                self.assertAlmostEqual(local[1], CFG['sight']['front_post_local_y'], places=6)
                self.assertAlmostEqual(local[2], post_z, delta=1e-3)
                if distance < S.TAIL_DISTANCE:
                    self.assertAlmostEqual(p['camera'][2], S.MIN_CAMERA_HEIGHT, places=6)

    def test_model_scale_scales_the_sight_but_not_the_ballistics(self):
        frame = lambda v: rx(-math.radians(30), v)
        world = lambda v: S.mul(S.add((0, 0, CFG['pitch_pivot_units']), frame(v)), 2.0)
        muzzle, bore = world((0, -224, 19.6)), frame((0, -1, 0))
        p = S.pose(world(tuple(CFG['camera_local_units'])), frame((-1, 0, 0)), muzzle, bore, (0, 0, 0), (0, 0, 1), 2.0)
        expected = S.add(S.add(muzzle, S.mul(bore, S.ZERO_RANGE)), (0, 0, -S.ZERO_DROP))
        self.assertLess(S.norm(S.sub(p['target'], expected)), 1e-9)
        self.assertAlmostEqual(S.dot(S.sub(p['front_post'], world(tuple(CFG['camera_local_units']))), bore), 2.0*S.FRONT_POST_ALONG, places=6)
        self.assertLessEqual(p['distance'], 2.0*S.TAIL_DISTANCE + 1e-9)

    def test_degenerate_inputs_return_none_like_the_native_pose(self):
        self.assertIsNone(S.pose((0, 0, 0), (1, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 1)))
        self.assertIsNone(S.pose((0, 0, 0), (0, 5250, -113.589), (0, 0, 0), (0, 1, 0), (0, 0, 0), (0, 0, 1)))
        self.assertIsNone(S.pose((0, 0, 0), (1, 0, 0), (0, 10, 0), (0, 1, 0), (0, 0, 0), (0, 0, 1), 0.0))
        self.assertIsNone(S.pose((0, 5250, -113.589), (1, 0, 0), (0, 0, 0), (0, 1, 0), (0, 0, 0), (0, 0, 1)))


class WrittenNif(unittest.TestCase):
    def test_front_post_node_is_under_the_pitch_node_at_the_flat_zero(self):
        n = nodes(); post = n[CFG['sight']['front_post_node']]
        pitch = next(i for i, v in nif_nodos.leer(str(NIF))['nodos'].items() if v['nombre'] == 'CTRL_ELEVACION')
        self.assertIn(next(i for i, v in nif_nodos.leer(str(NIF))['nodos'].items() if v['nombre'] == CFG['sight']['front_post_node']), nif_nodos.leer(str(NIF))['nodos'][pitch]['hijos'])
        flat = pose_at(0, 0)[0]['front_post']
        for a, b in zip(post['tr'], (0.0, CFG['sight']['front_post_local_y'], flat[2] - CFG['pitch_pivot_units'])):
            self.assertAlmostEqual(a, b, places=3)

    def test_iron_sight_shapes_are_exported(self):
        names = set(nif_nodos.leer(str(NIF))['strings'])
        for shape in ('CTRL_ELEVACION_alza', 'CTRL_ELEVACION_guion_arco', 'AstraSightFrontPost_guion'):
            self.assertIn(shape, names)

    def test_pedestal_collision_is_the_lowered_box(self):
        box = json.loads((ROOT/'reports/collision_walkable.json').read_text())['ballesta_fixed_box_units']
        self.assertAlmostEqual(box['max'][2] - box['min'][2], CFG['sight']['pedestal_collision_height_units'], places=3)

    def test_sight_path_verification_is_for_these_nifs(self):
        report = json.loads((ROOT/'reports/sight_path_verified.json').read_text())
        baseline=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v13')
        current=json.loads((ROOT/'config.json').read_text())
        before=json.loads((baseline/'config.json').read_text())
        changed={k for k in before.keys()|current.keys() if before.get(k)!=current.get(k)}
        # Los retiempos de v13, mas los movimientos documentados posteriores: v14
        # sube la API nativa a 4, v20/v21 reubican la torre (tower_v11.mundo) y v21
        # agrega el bloque del guardia (guardia). Nada mas puede derivar.
        self.assertEqual(changed,{'source','fire_seconds','release_seconds','reset_seconds','cycle_seconds',
                                  'native_api_version','tower_v11','guardia'})
        # v14 dejo de ser "el NIF de v13 retimado" (su NIF difiere por mas que el
        # retiempo), asi que esa identidad pertenece al contrato de v14, no al actual.
        # Lo que si se puede afirmar hoy: v22 NO toco este NIF, sigue siendo el mismo
        # que el ZIP v21 publicado. Es el nucleo del diseno de dos torretas.
        self.assertEqual(hashlib.sha256((ROOT/'mod/meshes/AstraAsedio/ballesta.nif').read_bytes()).hexdigest(),
                         'bcee401b79a3708ec16452ba23dd7e6364eb421bab310a218595232fac5d9e17')
        self.assertTrue(report['success'])
        # Fixed thresholds here, not the ones the script wrote: engine sphere ~12-15 u plus margin; near plane 15 u.
        self.assertGreaterEqual(report['min_head_to_camera_collision_clearance'], 25.0)
        self.assertGreaterEqual(report['min_camera_to_weapon_mesh'], 8.0)
        self.assertGreaterEqual(report['min_camera_to_sight_meshes'], 15.0)
        self.assertLess(report['max_sight_colinearity_error'], 1e-4)
        self.assertEqual(report['sight_line_blocked_count'], 0)
        self.assertEqual(report['near_plane_cut_poses'], 0)
        self.assertIs(report['near_plane_check_falsified'], True)
        # The pedestal top is a reachable operator position (a jump clears 35 u); it must be sampled.
        self.assertGreater(report['operator_positions_on_pedestal'], 0)
        # El informe es para los NIF de ESTE arbol. La rama "la ballesta todavia es la
        # de v13" caduco cuando v14 cambio ese NIF; hoy ambos se leen del arbol vivo.
        for name in ('torre', 'ballesta'):
            self.assertEqual(report['nif_sha256'][name], hashlib.sha256((ROOT/'mod/meshes/AstraAsedio'/f'{name}.nif').read_bytes()).hexdigest())
        # Camera parameters live outside the NIFs: the evidence must be for these scripts and config.
        # Los tres se leen del arbol vivo; la rama que pedia el config de v13 caduco.
        for name in ('scripts/sight_pose.py', 'scripts/verify_sight_path.py', 'config.json'):
            self.assertEqual(report['inputs_sha256'][name], hashlib.sha256((ROOT/name).read_bytes()).hexdigest(), name)


class NativeContract(unittest.TestCase):
    def test_plugin_drives_camera_and_front_post_from_sight_pose(self):
        source = (ROOT/'native/src/Plugin.cpp').read_text()
        self.assertIn('auto pose=sightPose(anchor.translation,anchor.rotation*Vec{1,0,0},projectile.translation,projectile.rotation*Vec{0,1,0},rootWorld.translation,rootWorld.rotation*Vec{0,0,1},rootWorld.scale);', source)
        self.assertIn('binding.frontPost->local.translate=', source)
        self.assertIn('binding.frontPost.reset(root->GetObjectByName("AstraSightFrontPost"));', source)
        self.assertIn('binding.frontPost->parent!=binding.pitch.get()', source)
        self.assertIn('length(anchorForward-expected)>0.02', source)

    def test_verified_operator_area_is_the_one_the_game_enforces(self):
        # verify_sight_path.py sweeps only the operator area it declares; it must be the area the final ESP
        # (VMAD), the PSC defaults and AstraSight accept, or the evidence would miss reachable positions.
        from build_plugin import read_vmad
        plugin = Plugin(ROOT/'mod/AstraAsedio.esp')
        record = next(o for t, o, n, d in plugin.recorrer() if t == 'ACTI')
        props = read_vmad(dict(plugin.subrecords(plugin.datos(record)))['VMAD'])['scripts'][0]['properties']
        verifier = (ROOT/'scripts/verify_sight_path.py').read_text(encoding='utf-8')
        m = re.search(r'^OPERATOR_RADIUS, OPERATOR_DZ = ([\d.]+), ([\d.]+)', verifier, re.M)
        self.assertIsNotNone(m)
        radius, dz = float(m.group(1)), float(m.group(2))
        self.assertEqual((props['OperatorDistance']['value'], props['OperatorVerticalTolerance']['value']), (radius, dz))
        psc = (ROOT/'mod/scripts/source/AstraAsedioActi.psc').read_text(encoding='utf-8')
        self.assertIn(f'float Property OperatorDistance = {radius:.1f} Auto', psc)
        self.assertIn(f'float Property OperatorVerticalTolerance = {dz:.1f} Auto', psc)
        native = (ROOT/'native/src/Plugin.cpp').read_text()
        self.assertIn(f'distance.x*distance.x+distance.y*distance.y>{radius:.0f}*{radius:.0f}', native)
        self.assertIn(f'std::abs(distance.z)>{dz:.0f}', native)
        # Centre and height of that area: the verifier's crank foot is the written OperatorNode lowered by
        # the operator height that Papyrus (ESP VMAD and PSC default) and AstraSight subtract.
        c = re.search(r'^crank = Vector\(\(([-\d.]+), ([-\d.]+)\)\)', verifier, re.M)
        self.assertIsNotNone(c)
        operator = nodes()['OperatorNode']['tr']
        height = props['OperatorHeight']['value']
        for a, b in zip(operator, (float(c.group(1)), float(c.group(2)), height)):
            self.assertAlmostEqual(a, b, places=3)
        self.assertIn(f'float Property OperatorHeight = {height:.1f} Auto', psc)
        self.assertIn(f'Vec{{0,0,{height:.0f}*rootWorld.scale}}', native)

    def test_controller_requires_the_shipped_astrasight(self):
        psc = (ROOT/'mod/scripts/source/AstraAsedioActi.psc').read_text(encoding='utf-8')
        # El gate de 3.4 (50593792) quedo atras: v21 exige AstraSight 3.5.0 y API 4.
        self.assertIn('if nativeVersion < 50659328', psc)
        self.assertIn('if nativeAPI != 4', psc)


if __name__ == '__main__':
    unittest.main()
