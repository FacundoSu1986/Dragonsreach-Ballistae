import bpy,addon_utils,json,sys,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts/vendor'))
import nif_nodos
addon_utils.enable('io_scene_nifly',default_set=True)
from io_scene_nifly.pyn.pynifly import NifFile
p=ROOT/'mod/meshes/AstraAsedio/ballesta.nif';b=nif_nodos.leer(str(p));nf=NifFile(str(p))
out=[]
for idx,(typ,off,size) in enumerate(b['bloques']):
 if typ not in ('NiControllerManager','NiControllerSequence','NiTransformController','NiTextKeyExtraData','NiTransformData'):continue
 node=nf.read_node(id=idx)
 props={name:list(getattr(node.properties,name)) if hasattr(getattr(node.properties,name),'__len__') else str(getattr(node.properties,name)) for name,_ in node.properties._fields_}
 out.append({'id':idx,'type':typ,'size':size,'head_hex':b['datos'][off:off+min(size,80)].hex(),'properties':props})
 if typ=='NiControllerManager':
  for name,seq in node.sequences.items():
   out.append({'sequence':name,'id':seq.id,'links':[{'name':link.node_name,'data':link.interpolator.properties.dataID,'controller':str(link.properties.controllerID)} for link in seq.controlled_blocks]})
(ROOT/'build/animation_layout.json').write_text(json.dumps(out,indent=2))
print('layout recorded')
