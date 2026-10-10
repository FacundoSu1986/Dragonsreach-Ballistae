"""v11 tower: own rustic geometry around the vanilla pieces of config.json -> tower_v11 (spec §2).

Runs in Blender after build_assets.py, as build_stairs.py did in v10, and replaces ONLY torre.nif:
ballesta.nif and virote.nif keep v10's bytes. The own geometry comes from tower_v11_geometry.py
(pure Python, tested without Blender); this script adds the stockade materials, keeps the v04
turntable, measures the v10 walking collision exactly as v10 measured it, exports and reports.
Nothing vanilla is exported or saved: stilts, braces, room and door are ESP references, and the
donor NIFs are imported only to copy their shader recipes into materials.
"""
import bpy, bmesh, addon_utils, json, math, sys, hashlib
from pathlib import Path
from collections import defaultdict
from mathutils import Vector
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]
import build_assets as A
import tower_v11_geometry as G
import v11_layout as L
import nif_fisica, nif_nodos
S = A.S
# v10 stair (build_stairs.py), metres: the ramp and its edge barriers do not change (spec, invariants).
X0, X1, Y1, Z1 = 4.02, 5.22, 2.8, 6.485
SLOPE = 3.225/5.2
Y0 = Y1 - Z1/SLOPE
KEEP = ('Plataforma_giratoria', 'Aro_hierro', 'Refuerzo_radial')     # the v04 turntable under the ballista
# New material keys used only by torre.nif; ballesta.nif keeps its v10 keys and bytes.
STOCKADE = {'stockade_wood': ('clutter/stockade/stockadewoodbeam01.nif', 'stockadewood01.dds'),
            'stockade_extra': ('clutter/stockade/stockadewoodbeam01.nif', 'stockadeextra01.dds'),
            'stockade_planks': ('clutter/stockade/stockadescaffoldtop0sided01.nif', 'stockadeplanks01.dds')}

def bounds(o):
    p = [o.matrix_world @ Vector(v) for v in o.bound_box]
    return ([min(v[i] for v in p) for i in range(3)], [max(v[i] for v in p) for i in range(3)])

def stockade_materials():
    """Copy each stockade shader recipe from a vanilla NIF into a material; keep no vanilla mesh."""
    report = json.loads((ROOT/'reports/material_donors.json').read_text())
    mats = {}
    for key, (path, suffix) in STOCKADE.items():
        A.clear(); before = set(bpy.data.materials)
        bpy.context.view_layer.objects.active = None
        bpy.ops.import_scene.pynifly(filepath=str(Path(A.CFG['extracted'])/'meshes'/path), blender_xf=False,
                                     import_animations=False, import_collisions=False, create_bones=False)
        fresh = sorted(set(bpy.data.materials) - before, key=lambda m: m.name)
        matches = [m for m in fresh if m.get('BSShaderTextureSet_Diffuse', '').lower().endswith(suffix)]
        if not matches: raise RuntimeError('Donor missing ' + key)
        m = matches[0].copy(); m.name = 'Astra_Vanilla_' + key; m.use_fake_user = True
        # Solid wood: the recipe without cutout alpha (verify_assets.py requires no NiAlphaProperty).
        for k in ('NiAlphaProperty_flags', 'NiAlphaProperty_threshold'):
            if k in m: del m[k]
        for node in m.node_tree.nodes:
            if 'Alpha Property' in node.inputs:
                for link in list(node.inputs['Alpha Property'].links): m.node_tree.links.remove(link)
        mats[key] = m
        report[key] = {'donor': path, 'diffuse': m.get('BSShaderTextureSet_Diffuse'), 'normal': m.get('BSShaderTextureSet_Normal'),
                       'shader': m.get('Shader_Type', 'Default'), 'source_material': matches[0].name, 'used_by': 'torre.nif only'}
    A.clear()
    for mesh in [me for me in bpy.data.meshes if me.users == 0]: bpy.data.meshes.remove(mesh)
    (ROOT/'reports/material_donors.json').write_text(json.dumps(report, indent=2))
    bpy.data.libraries.write(str(ROOT/'build/donor_materials_v11.blend'), set(mats.values()), fake_user=True)
    return {key: mat.name for key, mat in mats.items()}

def measure_invariants():
    """v10's walking collision, measured from the v04 source exactly as build_stairs.py did."""
    floor_groups = defaultdict(list); barriers = []
    for o in bpy.context.scene.objects:
        if o.type != 'MESH' or not any(c.name == '03_Plataforma' for c in o.users_collection): continue
        lo, hi = bounds(o); name = o.name.split('.')[0]
        if any(t in name for t in ('Tablon_azotea', 'Descanso_azotea')): floor_groups[name].append((lo, hi))
        elif 'Parapeto_traves' in name and 6.6 < lo[2] < 7:
            lo[2] = 6.485; barriers.append((lo, hi))
    barriers = list({tuple(round(v, 4) for p in b for v in p): b for b in barriers}.values())
    floorboxes, walk = [], []
    for name, parts in floor_groups.items():
        lo = [min(a[j] for a, b in parts) for j in range(3)]; hi = [max(b[j] for a, b in parts) for j in range(3)]
        floorboxes.append((lo, hi)); walk.append({'name': name, 'min': [v*S for v in lo], 'max': [v*S for v in hi]})
    assert len(walk) == 2 and abs(max(f['max'][2] for f in walk) - Z1*S) < .001, walk
    assert len(barriers) == 5, len(barriers)
    return barriers, floorboxes, walk

def part_object(p, mats, coll):
    """One editable object per own part (metres, as the v04 scene)."""
    me = bpy.data.meshes.new(p['name'])
    me.from_pydata([tuple(c/S for c in v) for v in p['verts']], [], p['faces']); me.update()
    keys = sorted(set(p['mats']))
    for k in keys: me.materials.append(mats[k])
    me.polygons.foreach_set('material_index', [keys.index(k) for k in p['mats']])
    me.polygons.foreach_set('use_smooth', [p['kind'] in ('log', 'rope') and k != 'stockade_extra' for k in p['mats']])
    uv = me.uv_layers.new(name='UVMap')
    for poly in me.polygons:
        corners = p['face_uvs'][poly.index] if 'face_uvs' in p else None
        for n, li in enumerate(poly.loop_indices): uv.data[li].uv = corners[n] if corners else p['uvs'][me.loops[li].vertex_index]
    o = bpy.data.objects.new(p['name'], me); coll.objects.link(o)
    return o

def merge_own(parts, key, name, mat, root):
    """All own faces of one material in one shape (game units). Logs and ropes keep shared vertices
    (smooth bark); planks get their own vertices per face, so they stay flat when exported."""
    verts, vuv, faces, smooth = [], [], [], []
    for p in parts:
        idx = [i for i, k in enumerate(p['mats']) if k == key]
        if not idx: continue
        if p['kind'] in ('log', 'rope'):
            used = sorted({j for i in idx for j in p['faces'][i]}); remap = {j: len(verts) + n for n, j in enumerate(used)}
            verts += [p['verts'][j] for j in used]; vuv += [p['uvs'][j] for j in used]
            for i in idx:
                faces.append(tuple(remap[j] for j in p['faces'][i])); smooth.append(key != 'stockade_extra')
        else:
            for i in idx:
                f = p['faces'][i]; base = len(verts)
                verts += [p['verts'][j] for j in f]
                vuv += p['face_uvs'][i] if 'face_uvs' in p else [p['uvs'][j] for j in f]
                faces.append(tuple(range(base, base + len(f)))); smooth.append(False)
    me = bpy.data.meshes.new(name + '_mesh'); me.from_pydata(verts, [], faces); me.update()
    me.materials.append(mat); me.polygons.foreach_set('use_smooth', smooth)
    uv = me.uv_layers.new(name='UVMap')
    for poly in me.polygons:
        for li in poly.loop_indices: uv.data[li].uv = vuv[me.loops[li].vertex_index]
    color = me.color_attributes.new(name='Col', type='FLOAT_COLOR', domain='CORNER')
    for v in color.data: v.color = (1, 1, 1, 1)
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o); o.parent = root
    return o

def disk_planks_uv(o):
    """The turntable boards in the stockade plank texture: boards along y, about 26 u wide."""
    me = o.data; uv = me.uv_layers.active or me.uv_layers.new(name='UVMap')
    for poly in me.polygons:
        for li in poly.loop_indices:
            co = o.matrix_world @ me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv = (0.02 + co.x*S/260.0, co.y*S/256.0)

def main():
    addon_utils.enable('io_scene_nifly', default_set=True)
    bpy.context.preferences.addons['io_scene_nifly'].preferences.sky_texture_path_1 = str(Path(A.CFG['extracted'])/'textures')
    base = json.loads((ROOT/'reports/collision_walkable.json').read_text())     # weapon-side keys from build_assets.py
    names = A.materials()
    names.update(stockade_materials())
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'source/Torre_Ballesta_lowpoly_v04.blend'), use_scripts=False)
    bpy.context.scene.frame_set(1)
    for lib in ('donor_materials.blend', 'donor_materials_v11.blend'):
        with bpy.data.libraries.load(str(ROOT/'build'/lib), link=False) as (src, dst):
            dst.materials = [n for n in names.values() if n in src.materials]
    mats = {k: bpy.data.materials[v] for k, v in names.items()}
    barriers, floorboxes, walk = measure_invariants()
    keep = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o.name.split('.')[0] in KEEP]
    removed = len(bpy.data.objects) - len(keep)
    for o in list(bpy.data.objects):
        if o not in keep: bpy.data.objects.remove(o, do_unlink=True)
    # Own geometry, one editable object per part.
    out = G.build(A.CFG)
    coll = bpy.data.collections.new('11_Torre_Rustica'); bpy.context.scene.collection.children.link(coll)
    for p in out['parts']: part_object(p, mats, coll)
    # The kept turntable: stockade boards, the iron as in v10.
    disk_parts = defaultdict(list)
    for o in keep:
        keys = [A.material_key(m.name) for m in o.data.materials]
        if o.name.startswith('Plataforma_giratoria'):
            disk_planks_uv(o); disk_parts['stockade_planks'].append((o, 'stockade_planks', list(range(len(keys)))))
        else:
            A.remap_uv(o, keys)
            for k in sorted(set(keys)): disk_parts[k].append((o, k, [i for i, v in enumerate(keys) if v == k]))
    # Editable source with the ballista as reference (own geometry only, nothing vanilla).
    bpy.context.view_layer.objects.active = None; bpy.ops.object.select_all(action='DESELECT')
    before = set(bpy.data.objects)
    bpy.ops.import_scene.pynifly(filepath=str(ROOT/'mod/meshes/AstraAsedio/ballesta.nif'), blender_xf=False, import_animations=False,
                                 import_collisions=False, create_bones=False)
    imported = set(bpy.data.objects) - before
    for root in [o for o in imported if o.get('pynRoot')]: root.scale = (1/S,)*3; root.location.z = A.CFG['tower_top_units']/S
    ref = bpy.data.collections.new('04_Ballesta_Referencia'); bpy.context.scene.collection.children.link(ref)
    for o in imported:
        for c in list(o.users_collection): c.objects.unlink(o)
        ref.objects.link(o)
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'source/Torre_rustica_v11.blend'))
    # Export: one shape per material, the v10 walking collision plus the new boxes.
    tower = A.empty('AstraTorre', root=True); bpy.context.view_layer.update()
    objects = [merge_own(out['parts'], key, 'Torre_' + key, mats[key], tower)
               for key in ('stockade_wood', 'stockade_extra', 'stockade_planks', 'rope')]
    objects += [A.merge_parts(parts, tower, 'Torre_disco_' + key, mats[key]) for key, parts in sorted(disk_parts.items())]
    ramp = tuple(v*S for v in (X0, X1, Y0, Y1, 0, Z1))
    rails = [tuple(v*S for v in (a, b, Y0, Y1, 1.05, Z1 + 1.05, 1.05)) for a, b in ((X0 - .03, X0 + .07), (X1 - .07, X1 + .03))]
    new_boxes = [(b['min'], b['max']) for b in out['boxes']]
    col = A.add_collision(tower, [([v*S for v in a], [v*S for v in b]) for a, b in barriers + floorboxes] + new_boxes, [ramp] + rails)
    bm = bmesh.new(); bm.from_mesh(col.data)
    r0 = [bm.verts.new((2.15*S*math.cos(j*math.tau/24), 2.15*S*math.sin(j*math.tau/24), 6.48*S)) for j in range(24)]
    r1 = [bm.verts.new((v.co.x, v.co.y, 6.61*S)) for v in r0]
    bm.faces.new(tuple(reversed(r0))); bm.faces.new(tuple(r1))
    for j in range(24): bm.faces.new((r0[j], r0[(j + 1) % 24], r1[(j + 1) % 24], r1[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bmesh.ops.triangulate(bm, faces=bm.faces); bm.to_mesh(col.data); bm.free()
    A.export('torre', tower, objects + [col])
    nif = ROOT/'mod/meshes/AstraAsedio/torre.nif'; nif_sha = hashlib.sha256(nif.read_bytes()).hexdigest()
    # Reports.
    sources = ['barrera_baja_%d' % k for k in range(len(barriers))] + [b['name'] for b in out['boxes']]
    collision = {'floors_units': walk, 'ramps': [{'name': 'Astra_Directa', 'x': [X0*S, X1*S], 'y': [Y0*S, Y1*S], 'z': [0, Z1*S]}],
                 'solid_boxes_units': [{'min': [v*S for v in a], 'max': [v*S for v in b]} for a, b in barriers] +
                                      [{'min': list(a), 'max': list(b)} for a, b in new_boxes],
                 'stair_edge_barriers_units': [{'min': [r[0], r[2], 0], 'max': [r[1], r[3], r[5]]} for r in rails],
                 'ballesta_fixed_box_units': base['ballesta_fixed_box_units'], 'walkable_disk_units': base['walkable_disk_units']}
    (ROOT/'reports/collision_walkable.json').write_text(json.dumps(collision, indent=2))
    lo, hi = nif_fisica.caja_visual(nif_nodos.leer(str(nif)))
    assets = json.loads((ROOT/'reports/assets.json').read_text())
    assets['torre'] = {'bbox_units': {'min': lo, 'max': hi}, 'source': 'scripts/build_tower_v11.py (written torre.nif)'}
    (ROOT/'reports/assets.json').write_text(json.dumps(assets, indent=2))
    stair = {'width_units': (X1 - X0)*S, 'horizontal_run_units': (Y1 - Y0)*S, 'rise_units': Z1*S, 'angle_degrees': math.degrees(math.atan(SLOPE)),
             'steps': G.COUNT, 'riser_units': G.RISE, 'tread_units': G.TREAD, 'handrail_above_ramp_units': G.HANDRAIL_ABOVE_RAMP,
             'stringer_bottom_below_ramp_units': A.CFG['tower_v11']['stair']['pile_drop'],
             'solid_box_sources': sources, 'pasamanos_soporte_bboxes': out['supports'],
             'design_origin': 'v11 rustic stair on the v10 ramp (tower_v11_geometry.py)', 'game_tested': False}
    (ROOT/'reports/stair_design.json').write_text(json.dumps(stair, indent=2))
    rustic = {'counts': out['counts'], 'triangles_own': out['triangles'], 'irregularity': A.CFG['tower_v11']['irregularity'],
              'logs': out['logs'], 'planks': out['planks'], 'ropes': out['ropes'], 'v04_objects_removed': removed,
              'kept_v04_turntable': sorted(o.name for o in keep), 'collision_moved': False, 'torre_nif_sha256': nif_sha}
    (ROOT/'reports/rustico.json').write_text(json.dumps(rustic, indent=2, default=list))
    print('V11_TOWER_EXPORTED', out['counts'], 'own triangles', out['triangles'], 'boxes', len(sources), 'sha', nif_sha[:12])

if __name__ == '__main__': main()
