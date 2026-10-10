"""v10/v11: verify the tail sight camera against the camera pull-in found in the v09 log, and render the sight (Blender).

v11: the collision of every vanilla piece of config.json -> tower_v11 (stilts, braces, room, door), placed
with the shared transform (v11_layout.piece_solids), joins the tower and ballista collision below; the
thresholds are v10's (spec §4).

The v09 recorder showed Skyrim pulling the camera toward the player head when collision lay between
the head and the camera (reports/user_evidence_v09.json). On the WRITTEN NIFs this script measures,
for sampled poses (24 yaws every 15 degrees x 9 elevations) and every operator foot position on a
20 u grid that AstraSight accepts (within 160 u of the crank foot, |dz| <= 64) and that stands on
walkable reimported Havok collision with room for the body (this includes the pedestal top: a jump
clears its 35 u):
  - a guaranteed lower bound of the head->camera segment clearance to that collision (distance to the
    collision is 1-Lipschitz along the segment; close intervals are refined);
  - camera clearance to every visual mesh except the iron sights, and to the iron sights against the
    15 u near plane; that no weapon geometry inside the view is cut by that near plane; that the sight
    line camera->zero target is free except at the front post tip;
  - with the post node written the way Plugin.cpp writes it (pitch-local R^T(F-T)/s), that the camera,
    the written rear-ring centre and the written post apex are collinear.
It also renders the sight view at 0, 35 and 80 degrees. Static geometry, not the engine. Against the
pedestal box the 30 u clearance also holds by construction: camera >= 65 u, eyes >= 108.9 u above the root.
Not covered: tower visual-only meshes (only tower collision enters the sweep).
"""
import bpy, addon_utils, json, math, sys, hashlib
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import sight_pose as S
import v11_layout as L
CFG = json.loads((ROOT/'config.json').read_text())
TOP = CFG['tower_top_units']; PIVOT = CFG['pitch_pivot_units']
SWEEP_CLEARANCE = 25.0      # engine sphere ~12-15 u (fitted to the v09 log) plus margin
CAMERA_CLEARANCE = 8.0
NEAR_PLANE = 15.0           # Skyrim default fNearDistance: the iron sights must stay beyond it
OPERATOR_RADIUS, OPERATOR_DZ = 160.0, 64.0   # AstraSight and Papyrus operator acceptance (Plugin.cpp, AstraAsedioActi.psc)
BODY_RADIUS = 10.0          # smaller than the player capsule on purpose: admits more foot positions
EYE_ABOVE_FEET = 120.5      # v09 log: eye 109.3 above the root with the feet on the outer floor (-11.2)
addon_utils.enable('io_scene_nifly', default_set=True)
bpy.context.preferences.addons['io_scene_nifly'].preferences.sky_texture_path_1 = str(Path(CFG['extracted'])/'textures')
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
collision_vs, collision_ts = [], []
visual = []
for name in ('torre', 'ballesta'):
    old = set(bpy.data.objects); bpy.context.view_layer.objects.active = None
    bpy.ops.import_scene.pynifly(filepath=str(ROOT/'mod/meshes/AstraAsedio'/f'{name}.nif'), blender_xf=False, import_animations=False, import_collisions=True, create_bones=False)
    new = set(bpy.data.objects) - old
    if name == 'ballesta':
        # With collisions imported, PyNifly leaves the node empties and the collision shape outside the
        # root's hierarchy; lift every top-level ballista object onto the tower.
        for o in new:
            if o.parent is None: o.location.z += TOP
    bpy.context.view_layer.update()
    for o in new:
        if o.type != 'MESH': continue
        if o.name.startswith('bhk'):
            o.data.calc_loop_triangles(); base = len(collision_vs)
            pts = [o.matrix_world @ v.co for v in o.data.vertices]
            collision_vs += pts; collision_ts += [tuple(base+i for i in t.vertices) for t in o.data.loop_triangles]
        elif name == 'ballesta':
            visual.append(o)
# v11: the vanilla pieces' collision in place (memory only; nothing vanilla is saved).
vanilla_triangles = 0
for piece in CFG['tower_v11']['pieces']:
    for solid in L.piece_solids(piece, CFG):
        for tri in L.solid_triangles(solid):
            base = len(collision_vs); collision_vs += [Vector(p) for p in tri]; collision_ts.append((base, base + 1, base + 2))
            vanilla_triangles += 1
collision = BVHTree.FromPolygons(collision_vs, collision_ts, all_triangles=True)
pedestal_top = max(p.z for p in collision_vs if abs(p.x) < 95 and abs(p.y) < 92 and p.z > TOP - 1)
anchor_check = bpy.data.objects[CFG['sight']['rear_sight_node']]
if abs(anchor_check.matrix_world.translation.z - (TOP + PIVOT + 40)) > 1e-3 or abs(pedestal_top - TOP - CFG['sight']['pedestal_collision_height_units']) > 0.1:
    raise SystemExit(f'scene placement wrong: anchor z {anchor_check.matrix_world.translation.z}, pedestal top {pedestal_top}')
yaw_node = bpy.data.objects['CTRL_GIRO_360']; pitch_node = bpy.data.objects['CTRL_ELEVACION']
post = bpy.data.objects[CFG['sight']['front_post_node']]; anchor = bpy.data.objects[CFG['sight']['rear_sight_node']]
muzzle = bpy.data.objects['ProjectileNode']
if post.parent is not pitch_node or anchor.parent is not pitch_node:
    raise SystemExit('sight node hierarchy differs from the one Plugin.cpp requires')
yaw_base = yaw_node.matrix_local.copy(); pitch_base = pitch_node.matrix_local.copy(); post_base = post.matrix_local.copy()
ring_mesh = next(o for o in visual if o.name.startswith('CTRL_ELEVACION_alza'))
post_mesh = next(o for o in visual if o.name.startswith('AstraSightFrontPost_guion'))
sight_meshes = [ring_mesh, post_mesh]
# Everything else the camera could touch or look through: moving head, iron-sight arch and fixed base.
weapon_meshes = [o for o in visual if o not in sight_meshes]
ray_meshes = [o for o in visual if o is not post_mesh]   # the line must pass the ring hole; it ends on the post apex

def pose_scene(yaw, elevation):
    m = Matrix.Rotation(math.radians(yaw), 4, 'Z') @ yaw_base; m.translation = yaw_base.translation; yaw_node.matrix_local = m
    p = Matrix.Rotation(math.radians(-elevation), 4, 'X') @ pitch_base; p.translation = pitch_base.translation; pitch_node.matrix_local = p
    bpy.context.view_layer.update()
    rear = anchor.matrix_world.translation; right = anchor.matrix_world.to_3x3() @ Vector((1, 0, 0))
    bore = (muzzle.matrix_world.to_3x3() @ Vector((0, 1, 0))).normalized()
    # root at (0,0,TOP): heights are measured from the root
    sp = S.pose(tuple(rear), tuple(right), tuple(muzzle.matrix_world.translation), tuple(bore), (0, 0, TOP), (0, 0, 1))
    # Written as Plugin.cpp writes it: postLocal = R^T (F - T) / s in the pitch node's space.
    pw = pitch_node.matrix_world; scale = pw.to_scale()[0]
    local = pw.to_3x3().normalized().transposed() @ (Vector(sp['front_post']) - pw.translation) / scale
    m = post_base.copy(); m.translation = local; post.matrix_local = m
    bpy.context.view_layer.update()
    return sp

def world_vertices(o):
    return [o.matrix_world @ v.co for v in o.data.vertices]

def written_sight_points():
    """Rear-ring centre and post apex measured on the written meshes (not on the pose)."""
    inv = pitch_node.matrix_world.inverted(); up = (pitch_node.matrix_world.to_3x3() @ Vector((0, 0, 1))).normalized()
    centre = inv @ anchor.matrix_world.translation
    ring = [inv @ v for v in world_vertices(ring_mesh)]
    ring = [v for v in ring if abs(v.y - centre.y) <= 1.15 and 5.3 <= math.hypot(v.x - centre.x, v.z - centre.z) <= 7.7]
    if len(ring) < 100:
        raise SystemExit(f'rear ring not found in the written mesh ({len(ring)} vertices)')
    lo = Vector([min(v[i] for v in ring) for i in range(3)]); hi = Vector([max(v[i] for v in ring) for i in range(3)])
    apex = max(world_vertices(post_mesh), key=lambda v: v.dot(up))
    return pitch_node.matrix_world @ ((lo + hi)/2), apex

TAN_H = math.tan(math.radians(85/2)); TAN_V = TAN_H*9/16   # renders' 85 degree horizontal FOV, 16:9

def near_plane_intrusions(cam, sp, items, near=NEAR_PLANE):
    """Names of items (name, world vertices, BVH) reaching into the view volume the near plane removes (the
    pyramid between the camera and the near plane): a triangle crossing its faces overlaps it, one fully inside
    has its vertices inside."""
    fwd, rgt, upv = Vector(sp['forward']), Vector(sp['right']), Vector(sp['up'])
    corners = [cam + fwd*near + rgt*(sx*near*TAN_H) + upv*(sy*near*TAN_V) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    pyramid = BVHTree.FromPolygons([cam] + corners, [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (1, 2, 3), (1, 3, 4)], all_triangles=True)
    found = []
    for name, verts, tree in items:
        inside = False
        for p in verts:
            d = p - cam; z = d.dot(fwd)
            if 0 < z < near and abs(d.dot(rgt)) <= z*TAN_H and abs(d.dot(upv)) <= z*TAN_V: inside = True; break
        if inside or tree.overlap(pyramid): found.append(name)
    return found

def segment_clearance(a, b, n=60, refine=16):
    """(sampled minimum, guaranteed lower bound) of the distance from segment a-b to the collision."""
    pts = [a + (b - a)*(k/n) for k in range(n + 1)]
    d = [collision.find_nearest(p)[3] for p in pts]
    step = (b - a).length/n; sampled = min(d); bound = 1e9
    for i in range(n):
        lb = (d[i] + d[i+1] - step)/2
        if lb < SWEEP_CLEARANCE + 5:
            dd = [d[i]] + [collision.find_nearest(pts[i] + (pts[i+1] - pts[i])*(k/refine))[3] for k in range(1, refine)] + [d[i+1]]
            sampled = min(sampled, min(dd))
            lb = min((dd[k] + dd[k+1] - step/refine)/2 for k in range(refine))
        bound = min(bound, lb)
    return sampled, bound

def trees(objs):
    out = []
    for o in objs:
        o.data.calc_loop_triangles()
        out.append(BVHTree.FromPolygons([o.matrix_world @ v.co for v in o.data.vertices], [tuple(t.vertices) for t in o.data.loop_triangles], all_triangles=True))
    return out

def body_fits(f):
    return all(collision.find_nearest(f + Vector((0, 0, h)), BODY_RADIUS)[0] is None for h in (BODY_RADIUS + 1, 30, 50, 70, 90, 110))

# Operator feet: every walkable collision surface on the grid that AstraSight accepts (the crank foot is the
# root-level point under OperatorNode (73.5, 101.5)), found by casting down through every layer.
crank = Vector((73.5, 101.5)); down = Vector((0, 0, -1))
feet = []
for gx in range(-260, 261, 20):
    for gy in range(-260, 261, 20):
        x, y = gx + 0.37, gy + 0.23   # off the box-face diagonals, where a BVH ray can miss both triangles
        if (Vector((x, y)) - crank).length > OPERATOR_RADIUS: continue
        z = TOP + OPERATOR_DZ + 0.5
        for _ in range(20):
            hit = collision.ray_cast(Vector((x, y, z)), down, z - (TOP - OPERATOR_DZ - 0.5))
            if hit[0] is None: break
            if hit[1].z > 0.64 and abs(hit[0].z - TOP) <= OPERATOR_DZ and body_fits(hit[0]): feet.append(hit[0].copy())
            z = hit[0].z - 0.05
on_pedestal = [f for f in feet if abs(f.z - TOP - CFG['sight']['pedestal_collision_height_units']) < 0.5]
floor_heights = sorted({round(f.z - TOP, 1) for f in feet})
rows = []; worst_sweep = (1e9, None); sampled_sweep = 1e9; worst_camera = (1e9, None); worst_sight = (1e9, None)
blocked = []; clipped = []; colinear = 0.0; alignment = 0.0
for elevation in (-20, -15, -10, -5, 0, 15, 35, 38, 45, 60, 70, 80):
    for yaw in range(0, 360, 15):
        sp = pose_scene(yaw, elevation)
        cam = Vector(sp['camera']); tgt = Vector(sp['target'])
        weapon_trees = trees(weapon_meshes)
        d_cam = min(t.find_nearest(cam)[3] for t in weapon_trees)
        if d_cam < worst_camera[0]: worst_camera = (d_cam, (yaw, elevation))
        d_sight = min(t.find_nearest(cam)[3] for t in trees(sight_meshes))
        if d_sight < worst_sight[0]: worst_sight = (d_sight, (yaw, elevation))
        cut = near_plane_intrusions(cam, sp, [(o.name, world_vertices(o), t) for o, t in zip(weapon_meshes, weapon_trees)])
        if cut: clipped.append({'yaw': yaw, 'elevation': elevation, 'meshes': cut})
        ray = (tgt - cam).normalized()
        for t in trees(ray_meshes):
            hit = t.ray_cast(cam, ray, (tgt - cam).length)
            if hit[0] is not None: blocked.append({'yaw': yaw, 'elevation': elevation, 'distance': hit[3]})
        ring_centre, apex = written_sight_points()
        for point in (ring_centre, apex):
            off = ray.cross(point - cam).length
            alignment = max(alignment, off); colinear = max(colinear, off/max(1.0, (point - cam).length))
        for f in feet:
            eye = f + Vector((0, 0, EYE_ABOVE_FEET))
            sampled, bound = segment_clearance(eye, cam)
            sampled_sweep = min(sampled_sweep, sampled)
            if bound < worst_sweep[0]: worst_sweep = (bound, {'yaw': yaw, 'elevation': elevation, 'eye': list(eye)})
        rows.append({'yaw': yaw, 'elevation': elevation, 'camera_distance_behind_rear': sp['distance'], 'camera_height_above_root': cam.z - TOP, 'camera_to_weapon': d_cam, 'camera_to_sight_meshes': d_sight})
# Falsify the near-plane check: a big face crossing the clipped slice with every vertex outside it (only the
# overlap path can see it), and the rear ring at +80 against a 20 u near plane (it sits at ~16.5 u).
sp = pose_scene(0, 0); cam = Vector(sp['camera']); fwd, rgt, upv = Vector(sp['forward']), Vector(sp['right']), Vector(sp['up'])
big = [cam + fwd*10 + rgt*500, cam + fwd*10 - rgt*500 + upv*300, cam + fwd*10 - rgt*500 - upv*300]
probe_face = near_plane_intrusions(cam, sp, [('face', big, BVHTree.FromPolygons(big, [(0, 1, 2)], all_triangles=True))])
sp = pose_scene(0, 80)
probe_ring = near_plane_intrusions(Vector(sp['camera']), sp, [(ring_mesh.name, world_vertices(ring_mesh), trees([ring_mesh])[0])], near=20.0)
near_plane_falsified = probe_face == ['face'] and probe_ring == [ring_mesh.name]
report = {'scope': 'Static geometry on the written NIFs, sampled poses (24 yaws x 12 elevations including -20 degrees). The engine sphere radius (~12-15 u) and its start at the eye are fitted to the v09 camera recorder log, not measured in the engine.',
    'operator_positions': len(feet), 'operator_positions_on_pedestal': len(on_pedestal), 'operator_foot_heights_above_root': floor_heights,
    'operator_rule': f'within {OPERATOR_RADIUS:.0f} u of the crank foot, |dz| <= {OPERATOR_DZ:.0f}, walkable collision, body radius {BODY_RADIUS:.0f} u free up to 110 u; eye = feet + {EYE_ABOVE_FEET}',
    'poses': len(rows), 'pedestal_collision_top_above_root': pedestal_top - TOP,
    'min_head_to_camera_collision_clearance': worst_sweep[0], 'min_head_to_camera_collision_sampled': sampled_sweep,
    'sweep_bound': 'guaranteed lower bound: distance to the collision is 1-Lipschitz along the segment; intervals within 30 u refined 16x',
    'worst_sweep_case': worst_sweep[1], 'required_sweep_clearance': SWEEP_CLEARANCE,
    'min_camera_to_weapon_mesh': worst_camera[0], 'worst_camera_case': worst_camera[1], 'required_camera_clearance': CAMERA_CLEARANCE,
    'min_camera_to_sight_meshes': worst_sight[0], 'worst_sight_mesh_case': worst_sight[1], 'required_near_plane': NEAR_PLANE,
    'near_plane_cuts_in_view': clipped[:10], 'near_plane_cut_poses': len(clipped), 'near_plane_check_falsified': near_plane_falsified,
    'near_plane_rule': 'no weapon triangle overlaps, and no weapon vertex lies inside, the view pyramid between the camera and the 15 u near plane (85 degree 16:9 frustum)',
    'not_covered': 'Tower visual-only geometry is outside the camera, near-plane and sight-line checks (tower and vanilla collision are in the sweep); within the 200 u camera radius the v11 tower keeps only the v04 turntable and the deck planks, both low.',
    'vanilla_collision_triangles': vanilla_triangles, 'vanilla_pieces': len(CFG['tower_v11']['pieces']),
    'sight_line_blocked_by_weapon': blocked[:10], 'sight_line_blocked_count': len(blocked),
    'max_sight_colinearity_error': colinear, 'max_sight_alignment_error_units': alignment,
    'alignment_points': 'written rear-ring centre (bounding box of the ring vertices) and written post apex, post node set as Plugin.cpp sets it',
    'nif_sha256': {n: hashlib.sha256((ROOT/'mod/meshes/AstraAsedio'/f'{n}.nif').read_bytes()).hexdigest() for n in ('torre', 'ballesta')},
    'inputs_sha256': {n: hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ('scripts/sight_pose.py', 'scripts/verify_sight_path.py', 'config.json', 'scripts/v11_layout.py', 'reports/angle_convention.json')},
    'rows': rows}
ok = (worst_sweep[0] >= SWEEP_CLEARANCE and worst_camera[0] >= CAMERA_CLEARANCE and worst_sight[0] >= NEAR_PLANE
      and not blocked and not clipped and near_plane_falsified and colinear < 1e-4 and len(on_pedestal) > 0 and len(feet) > len(on_pedestal))
report['success'] = ok
(ROOT/'reports/sight_path_verified.json').write_text(json.dumps(report, indent=2))
print('SIGHT_PATH', 'ok' if ok else 'FAILED', 'feet', len(feet), 'pedestal', len(on_pedestal), 'heights', floor_heights, 'sweep', round(worst_sweep[0], 2), 'sampled', round(sampled_sweep, 2),
      'camera', round(worst_camera[0], 1), 'sight', round(worst_sight[0], 1), 'blocked', len(blocked), 'near_cut', len(clipped), 'near_falsified', near_plane_falsified, probe_face, probe_ring, 'colinear', colinear, 'align', alignment)
# Renders of the sight view (Skyrim-like 85 degree horizontal FOV); textures from the extracted vanilla set.
scene = bpy.context.scene; scene.render.engine = 'CYCLES'; scene.cycles.samples = 32
scene.render.resolution_x = 1600; scene.render.resolution_y = 900; scene.world.color = (.32, .32, .32)
scene.view_settings.view_transform = 'AgX'; scene.view_settings.look = 'AgX - Medium High Contrast'; scene.view_settings.exposure = .75
for i, (pos, power) in enumerate((((-450, -750, 1100), 7e6), ((800, -350, 600), 3.5e6), ((200, 650, 1000), 5e6))):
    d = bpy.data.lights.new(f'L{i}', 'AREA'); d.energy = power; d.size = 600
    o = bpy.data.objects.new(f'L{i}', d); scene.collection.objects.link(o); o.location = pos
    o.rotation_euler = (Vector((0, 0, 260)) - o.location).to_track_quat('-Z', 'Y').to_euler()
cd = bpy.data.cameras.new('Sight'); cam_obj = bpy.data.objects.new('Sight', cd); scene.collection.objects.link(cam_obj)
cd.type = 'PERSP'; cd.sensor_fit = 'HORIZONTAL'; cd.angle = math.radians(85); cd.clip_start = NEAR_PLANE; cd.clip_end = 8000; scene.camera = cam_obj
images = []
for elevation in (-20, 0, 35, 80):
    sp = pose_scene(0, elevation)
    basis = Matrix((Vector(sp['right']), Vector(sp['up']), -Vector(sp['forward']))).transposed()
    cam_obj.matrix_world = Matrix.Translation(Vector(sp['camera'])) @ basis.to_4x4()
    path = ROOT/f'renders/Astra_mira_v11_{elevation:02d}.png'; scene.render.filepath = str(path); bpy.ops.render.render(write_still=True)
    images.append(str(path.relative_to(ROOT)))
report['renders'] = images
(ROOT/'reports/sight_path_verified.json').write_text(json.dumps(report, indent=2))
if not ok:
    raise SystemExit('sight path verification failed')
print('SIGHT_PATH_RENDERS_OK')
