"""Renders of the v11 tower as it will stand in the cell (Blender; nothing is saved, spec §4).

torre.nif and ballesta.nif from mod/, each vanilla piece of config.json -> tower_v11 imported from
config.extracted and placed with the shared transform (v11_layout.piece_matrix). The vanilla
meshes live only in this Blender session: the script never writes a .blend.

Usage: blender -b --factory-startup --python-exit-code 1 --python scripts/render_v11.py -- [view ...] [--out DIR] [--fast]
Views: referencia escalera puerta uniones bajo_plataforma (default: all).
"""
import bpy, addon_utils, math, sys
from pathlib import Path
from mathutils import Matrix, Vector
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]
import v11_layout as L

ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
FAST = '--fast' in ARGS
OUT = Path(ARGS[ARGS.index('--out') + 1]) if '--out' in ARGS else ROOT/'renders'
VIEWS = {  # camera location, look-at point, lens mm
    'referencia':      ((1250.0, -1150.0, 1150.0), (40.0, -60.0, 260.0), 38),
    'escalera':        ((900.0, -980.0, 420.0), (300.0, -200.0, 230.0), 32),
    'puerta':          ((60.0, -620.0, 150.0), (0.0, -118.0, 100.0), 30),
    'uniones':         ((520.0, -520.0, 470.0), (262.0, -262.0, 360.0), 45),
    'bajo_plataforma': ((420.0, -700.0, 110.0), (0.0, -118.0, 120.0), 24),
    'escudos':         ((620.0, -700.0, 760.0), (0.0, -40.0, 500.0), 40),
    'escudo_n':        ((160.0, 660.0, 560.0), (130.0, 262.0, 490.0), 75),
    'escudo_o':        ((-660.0, -40.0, 560.0), (-262.0, 0.0, 490.0), 75),
}
wanted = [v for v in ARGS if v in VIEWS] or list(VIEWS)

def import_nif(path):
    before = set(bpy.data.objects)
    bpy.context.view_layer.objects.active = None
    bpy.ops.import_scene.pynifly(filepath=str(path), blender_xf=False, import_animations=False, import_collisions=False, create_bones=False)
    new = set(bpy.data.objects) - before
    roots = [o for o in new if o.parent is None]
    return roots, new

def place(roots, m):
    M = Matrix([[m['r'][i][j]*m['s'] for j in range(3)] + [m['t'][i]] for i in range(3)] + [[0, 0, 0, 1]])
    for r in roots: r.matrix_world = M @ r.matrix_world

def main():
    global SWING
    addon_utils.enable('io_scene_nifly', default_set=True)
    cfg = L.load_cfg(); SWING = L.door_swing(cfg)
    bpy.context.preferences.addons['io_scene_nifly'].preferences.sky_texture_path_1 = str(Path(cfg['extracted'])/'textures')
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    import_nif(ROOT/'mod/meshes/AstraAsedio/torre.nif')
    roots, _ = import_nif(ROOT/'mod/meshes/AstraAsedio/ballesta.nif')
    for r in roots: r.location.z += cfg['tower_top_units']
    door_nodes = []
    for p in cfg['tower_v11']['pieces']:
        roots, new = import_nif(Path(cfg['extracted'])/'meshes'/p['modl'])
        place(roots, L.piece_matrix(p))
        # Only the hinge node turns; its shape 'Door01:7' is a child and must not turn twice.
        if p['role'] == 'puerta': door_nodes += [o for o in new if o.type == 'EMPTY' and o.name.split('.')[0] == 'Door01']
    # v12: escudos vanilla colgados de la baranda. Misma fuente que el parche del ESP
    # (config.json -> tower_v11.escudos), para que lo que se ve sea lo que se carga.
    escudos = cfg['tower_v11'].get('escudos')
    if escudos:
        for item in escudos['items']:
            roots, _ = import_nif(Path(cfg['extracted'])/'meshes'/escudos['modl'])
            place(roots, L.transform_matrix(item['pos'], item['rot_deg'], item.get('scale', 1.0), *L.engine_convention()))
    # Ground of the test cell and light.
    bpy.ops.mesh.primitive_plane_add(size=6000, location=(0, -200, 0))
    ground = bpy.context.object; mat = bpy.data.materials.new('suelo'); mat.diffuse_color = (0.18, 0.18, 0.19, 1)
    mat.use_nodes = True; mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.16, 0.16, 0.17, 1)
    ground.data.materials.append(mat)
    sun = bpy.data.lights.new('sol', 'SUN'); sun.energy = 3.5; so = bpy.data.objects.new('sol', sun)
    bpy.context.scene.collection.objects.link(so); so.rotation_euler = (math.radians(50), math.radians(10), math.radians(150))
    world = bpy.data.worlds.new('mundo'); bpy.context.scene.world = world; world.use_nodes = True
    world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.32, 0.33, 0.35, 1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.9
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_EEVEE_NEXT'
    sc.render.resolution_x, sc.render.resolution_y = (960, 760) if FAST else (1600, 1260)
    if hasattr(sc, 'eevee'): sc.eevee.taa_render_samples = 16 if FAST else 64
    cam = bpy.data.cameras.new('cam'); cam.clip_start = 5; cam.clip_end = 20000
    co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
    OUT.mkdir(parents=True, exist_ok=True)
    for view in wanted:
        loc, target, lens = VIEWS[view]
        # The door renders open at the Open sequence's rest key (-92 degrees), turned the way the vanilla
        # furniture showed the engine reads XYZ keys (v11_layout.door_swing).
        for d in door_nodes: d.rotation_euler.z = math.radians(SWING['local_sign']*-92.0 if view in ('puerta', 'bajo_plataforma') else 0.0)
        co.location = loc; cam.lens = lens
        co.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
        sc.render.filepath = str(OUT/('v11_%s.png' % view))
        bpy.ops.render.render(write_still=True)
        print('RENDERED', sc.render.filepath)

if __name__ == '__main__': main()
