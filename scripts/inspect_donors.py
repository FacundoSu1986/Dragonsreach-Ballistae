import bpy, addon_utils, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
C = json.loads((ROOT/'config.json').read_text())
addon_utils.enable('io_scene_nifly', default_set=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
donors = ['architecture/farmhouse/lumbermill01.nif', 'clutter/civilwar/catapult/civilwarcatapult01.nif', 'dlc01/traps/crossbowtraps/plaincrossbow/plaincrossbowtrap01.nif']
out = {}
for donor in donors:
    old = set(bpy.data.materials)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None
    bpy.ops.import_scene.pynifly(filepath=str(Path(C['extracted'])/'meshes'/donor), blender_xf=False)
    out[donor] = [{ 'name': m.name, 'props': {k:str(v) for k,v in m.items()}, 'images': [{'node': n.name, 'path': n.image.filepath} for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]} for m in set(bpy.data.materials)-old]
(ROOT/'reports/donors.json').write_text(json.dumps(out, indent=2))
print('ASTRA_DONORS_OK')
