"""Read source ties and limb geometry before fitting the six main bindings."""
import bpy,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
cfg=json.loads((ROOT/'config.json').read_text())
bpy.ops.wm.open_mainfile(filepath=cfg['source'],use_scripts=False,load_ui=False)
bpy.context.scene.frame_set(1);bpy.context.view_layer.update()
parts={}
for obj in bpy.data.objects:
    if obj.name.startswith(('Ligadura_limbo','Ligadura_punta','Limbo_arco','Fleje_arco')):
        points=[obj.matrix_world@v.co for v in obj.data.vertices]
        edges={}
        for p in obj.data.polygons:
            for a,b in p.edge_keys:edges[tuple(sorted((a,b)))]=edges.get(tuple(sorted((a,b))),0)+1
        parts[obj.name]={'parent':obj.parent.name,'matrix_world':[list(r) for r in obj.matrix_world],
                         'local_bbox':[list(v) for v in obj.bound_box],'vertices':len(points),'faces':len(obj.data.polygons),
                         'world_vertices':[list(v) for v in points],
                         'boundary_edges':sum(v==1 for v in edges.values()),'nonmanifold_edges':sum(v!=2 for v in edges.values())}
(ROOT/'reports/limb_ties_diagnosis.json').write_text(json.dumps(parts,indent=2))
for name,p in parts.items():print(name,p['vertices'],p['faces'],'open edges',p['boundary_edges'],'worldmatrix',p['matrix_world'])
