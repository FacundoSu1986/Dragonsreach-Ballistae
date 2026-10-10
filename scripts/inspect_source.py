"""Read-only Blender inspection used to define the export and collision."""
import json
from pathlib import Path
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
cfg = json.loads((ROOT / 'config.json').read_text())
bpy.ops.wm.open_mainfile(filepath=cfg['source'], load_ui=False, use_scripts=False)
bpy.context.scene.frame_set(1)
out = {'collections': {}, 'controls': {}}
for coll in bpy.data.collections:
    if coll.name.startswith(('90_', '95_')):
        continue
    meshes = []
    for ob in coll.objects:
        if ob.type != 'MESH':
            continue
        points = [ob.matrix_world @ Vector(v) for v in ob.bound_box]
        meshes.append({'name': ob.name, 'parent': ob.parent.name if ob.parent else None,
                       'min': [min(v[k] for v in points) for k in range(3)],
                       'max': [max(v[k] for v in points) for k in range(3)],
                       'materials': [m.name for m in ob.data.materials if m],
                       'tris': sum(len(p.vertices)-2 for p in ob.data.polygons),
                       'shape_keys': [k.name for k in ob.data.shape_keys.key_blocks] if ob.data.shape_keys else []})
    out['collections'][coll.name] = meshes
for ob in bpy.data.objects:
    if ob.name.startswith('CTRL_'):
        out['controls'][ob.name] = {'matrix': [list(row) for row in ob.matrix_world], 'parent': ob.parent.name if ob.parent else None}
(ROOT / 'reports/source_inspection.json').write_text(json.dumps(out, indent=2), encoding='utf8')
print('ASTRA_INSPECTION_OK')
