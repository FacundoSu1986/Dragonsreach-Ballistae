"""Read exported bytes, then reimport each final NIF, not the source scene."""
import bpy, addon_utils, json, sys, math, struct, hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/vendor'))
sys.path.insert(0,str(ROOT/'scripts'))
import nif_nodos
import nif_fisica
CFG=json.loads((ROOT/'config.json').read_text())
addon_utils.enable('io_scene_nifly',default_set=True)
from io_scene_nifly.pyn.pynifly import NifFile

def clean():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o,do_unlink=True)
    for a in list(bpy.data.actions): bpy.data.actions.remove(a)

report={'files':{},'failures':[]}
texturepaths=set()
for asset in ('torre','ballesta','virote'):
    path=ROOT/'mod/meshes/AstraAsedio'/f'{asset}.nif'
    binary=nif_nodos.leer(str(path))
    assert binary['version']=='0x14020007' and binary['bs']==100
    for typ,offset,size in binary['bloques']:
        if typ=='BSShaderTextureSet':
            pos=offset; count=struct.unpack_from('<I',binary['datos'],pos)[0]; pos+=4
            for _ in range(count):
                n=struct.unpack_from('<I',binary['datos'],pos)[0]; pos+=4
                p=binary['datos'][pos:pos+n].decode('cp1252'); pos+=n
                if p: texturepaths.add(p)
            assert pos==offset+size
    nf=NifFile(str(path))
    seq={}; scales={}
    for index,(typ,offset,size) in enumerate(binary['bloques']):
        if typ!='NiControllerManager': continue
        cm=nf.read_node(id=index)
        for name,s in cm.sequences.items():
            seq[name]={'start':s.properties.startTime,'stop':s.properties.stopTime,'targets':[b.node_name for b in s.controlled_blocks]}
            for link in s.controlled_blocks:
                data=link.interpolator.data
                if not data or not hasattr(data.properties,'scales'): continue
                n=data.properties.scales.numKeys
                if not n: continue
                typ,off,size=binary['bloques'][data.id]
                pos=off+size-(8+n*8)
                assert struct.unpack_from('<II',binary['datos'],pos)==(n,1)
                keys=[struct.unpack_from('<ff',binary['datos'],pos+8+i*8) for i in range(n)]
                scales[(name,link.node_name)]=keys
    clean(); bpy.context.scene.render.fps=30
    bpy.ops.import_scene.pynifly(filepath=str(path),blender_xf=False,create_bones=False)
    bpy.context.scene.frame_set(1); bpy.context.view_layer.update()
    visual=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith('bhk')]
    collision=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('bhk')]
    tris=0
    for o in visual:
        o.data.calc_loop_triangles(); tris+=len(o.data.loop_triangles)
        assert o.data.uv_layers.active, o.name+' missing UV'
        assert all(math.isfinite(x) for v in o.data.vertices for x in v.co)
        assert all(math.isfinite(x) for uv in o.data.uv_layers.active.data for x in uv.uv)
    allverts=[o.matrix_world@v.co for o in visual for v in o.data.vertices]
    bounds={'min':[min(v[i] for v in allverts) for i in range(3)],'max':[max(v[i] for v in allverts) for i in range(3)]}
    ct=0
    for o in collision: o.data.calc_loop_triangles(); ct+=len(o.data.loop_triangles)
    # v08 B7: alpha and Havok boxes are judged on the written bytes, every asset.
    report.setdefault('alpha_properties',{})[asset]=nif_fisica.propiedades_alfa(binary)
    if asset=='virote':
        body=CFG['projectile_body']
        assert len(collision)==1 and collision[0].get('collisionFilter_layer')=='PROJECTILE'
        assert collision[0].get('bhkMaterial')=='MATERIAL_ARROW'
        assert collision[0].get('pynRigidBody')=='bhkRigidBodyT'
        assert abs(collision[0].rigid_body.mass-body['mass'])<1e-4
        box=nif_fisica.cuerpos_caja(binary)[0];coverage=nif_fisica.cobertura(binary)[0]
        report['projectile_physics_verified']={'layer':collision[0].get('collisionFilter_layer'),'material':collision[0].get('bhkMaterial'),'body':collision[0].get('pynRigidBody'),'mass':collision[0].rigid_body.mass,
            'restitution':box['restitucion'],'box_coverage':coverage['fraccion'],'box_long_axis':coverage['eje'],'inertia':box['inercia'],
            'inertia_axis_aligned':nif_fisica.inercia_alineada(box),'vanilla_rules_failures':nif_fisica.reglas_vanilla(box)}
        report['projectile_box_ok']=(coverage['fraccion']>=nif_fisica.COBERTURA_MINIMA and nif_fisica.inercia_alineada(box)
            and not nif_fisica.reglas_vanilla(box) and abs(box['restitucion']-body['restitution'])<1e-6)
    report['files'][asset]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'shapes':len(visual),'triangles':tris,'vertices':sum(len(o.data.vertices) for o in visual),'collision_triangles':ct,'bbox_units':bounds,'sequences':list(seq),'sequence_details':seq,'nodes':{n['nombre']:{'translation':n['tr'],'rotation':n['rot'],'children':[binary['nodos'][h]['nombre'] for h in n['hijos'] if h in binary['nodos']]} for n in binary['nodos'].values()},'bytes':path.stat().st_size}
    if asset=='ballesta':
        assert set(seq)=={'Fire','Reset'}
        for name,duration in [('Fire',CFG['fire_seconds']),('Reset',CFG['reset_seconds'])]:
            assert abs(seq[name]['stop']-seq[name]['start']-duration)<.002, seq
            assert {'Cuerda_I','Cuerda_D','VIROTE_VISUAL','CTRL_BRAZO_I','CTRL_BRAZO_D'}.issubset(seq[name]['targets']),seq
        report['aim_nodes_have_no_animation_tracks']=all(not {'CTRL_GIRO_360','CTRL_ELEVACION','ProjectileNode','AstraSightCameraNode'}.intersection(v['targets']) for v in seq.values())
        assert {'CTRL_GIRO_360','CTRL_ELEVACION','ProjectileNode','OperatorNode','VIROTE_VISUAL'}.issubset(report['files'][asset]['nodes'])
        if CFG.get('use_sight_camera'):
            assert CFG['camera_node'] in report['files'][asset]['nodes']
        # Independently sample rope after import. Both inner endpoints meet.
        fire=next(a for a in bpy.data.actions if a.name=='Fire')
        for name in ('Cuerda_I','Cuerda_D','CTRL_BRAZO_I','CTRL_BRAZO_D','VIROTE_VISUAL'):
            o=bpy.data.objects.get(name)
            if o and o.animation_data:
                o.animation_data.action=fire
                slot=next((s for s in fire.slots if s.name_display==name),None)
                if slot: o.animation_data.action_slot=slot
        samples=[]; outer_samples=[]
        for seqname,frame in [('Fire',1+(f-1)*CFG['fire_seconds']/.6) for f in range(1,20)]+[('Reset',1+(f-1)*CFG['reset_seconds']/4.4) for f in range(1,134)]:
            action=bpy.data.actions[seqname]
            for name in ('Cuerda_I','Cuerda_D','CTRL_BRAZO_I','CTRL_BRAZO_D','VIROTE_VISUAL'):
                o=bpy.data.objects[name]
                o.animation_data.action=action
                o.animation_data.action_slot=next(s for s in action.slots if s.name_display==name)
            bpy.context.scene.frame_set(math.floor(frame),subframe=frame-math.floor(frame)); bpy.context.view_layer.update()
            # PyNifly 27's importer omits scalar animation. Read these keys
            # independently from the final bytes and combine them with the
            # imported translation/quaternion channels before measuring.
            t=(frame-1)/30
            for node in ('Cuerda_I','Cuerda_D'):
                keys=scales[(seqname,node)]
                if t<=keys[0][0]: value=keys[0][1]
                elif t>=keys[-1][0]: value=keys[-1][1]
                else:
                    a,b=next((a,b) for a,b in zip(keys,keys[1:]) if a[0]<=t<=b[0])
                    value=a[1]+(b[1]-a[1])*(t-a[0])/(b[0]-a[0])
                bpy.data.objects[node].scale=(value,value,value)
            bpy.context.view_layer.update()
            ends=[]
            for name in ('Cuerda_I_shape','Cuerda_D_shape'):
                o=bpy.data.objects[name]
                local=[v.co for v in o.data.vertices]
                ymax=max(v.y for v in local)
                ring=[o.matrix_world@v for v in local if abs(v.y-ymax)<1e-4]
                ends.append(sum(ring,Vector())/len(ring))
                ymin=min(v.y for v in local)
                outer_ring=[o.matrix_world@v for v in local if abs(v.y-ymin)<1e-4]
                outer=sum(outer_ring,Vector())/len(outer_ring)
                sign=-1 if name.startswith('Cuerda_I') else 1
                arm=bpy.data.objects['CTRL_BRAZO_I' if sign<0 else 'CTRL_BRAZO_D']
                tip=Vector((sign*120.4,29.89,18.55))
                outer_samples.append((outer-arm.matrix_world@tip).length)
            samples.append((ends[0]-ends[1]).length)
        report['rope_reimport_max_gap']=max(samples)
        report['rope_outer_attachment_max_error']=max(outer_samples)
        report['rope_poses_sampled']=len(samples)
        report['scale_keys_in_binary']={seq+'/'+node:len(keys) for (seq,node),keys in scales.items()}
        report['rope_endpoint_checks_pass']=max(samples)<.03 and max(outer_samples)<.03
        # El virote NO debe llevar pista de escala en el NIF: su visibilidad la
        # maneja el Papyrus con SetNodeScale (0.0 al confirmar, 1.0 al recargar y al
        # salir). Antes habia dos escritores sobre el mismo canal con valores distintos
        # (0.001 en el NIF y 0.0 en el script) y si la animacion fallaba el virote
        # quedaba invisible sin nada que lo restaurara.
        report['bolt_scale_owned_by_papyrus']=not any(n=='VIROTE_VISUAL' for _,n in scales)
        assert report['bolt_scale_owned_by_papyrus'], 'VIROTE_VISUAL must not carry a scale track'
        report['reimport_ballesta_actions']={a.name:[s.name_display for s in a.slots] for a in bpy.data.actions}

report['visual_triangles_total']=sum(f['triangles'] for f in report['files'].values())
report['collision_triangles_total']=sum(f['collision_triangles'] for f in report['files'].values())
report['texture_paths']=sorted(texturepaths)
report['vanilla_textures_exist']=bool(texturepaths) and all(p.lower().startswith('textures\\') and p.lower().endswith('.dds') and (Path(CFG['extracted'])/p).is_file() for p in texturepaths)
checks={'visual_budget':report['visual_triangles_total']<=40000,'collision_budget':report['collision_triangles_total']<=2000,'tower_shapes':report['files']['torre']['shapes']<=8,'ballesta_shapes':report['files']['ballesta']['shapes']<=32,'textures':report['vanilla_textures_exist'],'aim_tracks':report['aim_nodes_have_no_animation_tracks'],'rope':report['rope_endpoint_checks_pass'],
        'no_alpha_properties':not any(report['alpha_properties'].values()),'projectile_box':report.get('projectile_box_ok',False)}
report['checks']=checks; report['ok']=all(checks.values())
(ROOT/'reports/assets_verified.json').write_text(json.dumps(report,indent=2))
assets=json.loads((ROOT/'reports/assets.json').read_text())
for key,f in report['files'].items(): assets[key]={'bbox_units':f['bbox_units']}
(ROOT/'reports/assets.json').write_text(json.dumps(assets,indent=2))
assert report['ok'],checks
print('ASTRA_ASSETS_VERIFIED',report['visual_triangles_total'],report['collision_triangles_total'])
