"""Rebuild the three SE NIFs from the preserved v04; run with Blender 4.4."""
import bpy, bmesh, addon_utils, json, math, struct, sys
from pathlib import Path
from collections import defaultdict
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT/'config.json').read_text())
S = CFG['meters_to_units']
BASE = 6.65
FLAGS = 'SELECTIVE_UPDATE | SELECTIVE_UPDATE_TRANSF | SELECTIVE_UPDATE_CONTR | NO_ANIM_SYNC_S'
sys.path.insert(0,str(ROOT/'scripts/vendor'))
import nif_nodos

def patch_scale_keys(path, scales):
    """PyNifly 27 omits scale keys. Write standard NiTransformData float keys.

    No DLL/addon/global preference is changed. Block IDs and all references
    remain unchanged; only block lengths and their scalar key groups change.
    """
    from io_scene_nifly.pyn.pynifly import NifFile
    nf=NifFile(str(path)); parsed=nif_nodos.leer(str(path)); raw=parsed['datos']
    replacements={}
    for idx,(typ,off,size) in enumerate(parsed['bloques']):
        if typ!='NiControllerManager': continue
        for seq,sequence in nf.read_node(id=idx).sequences.items():
            for link in sequence.controlled_blocks:
                keys=scales.get((seq,link.node_name))
                if not keys: continue
                data_id=link.interpolator.properties.dataID
                dtype,doff,dsize=parsed['bloques'][data_id]
                assert dtype=='NiTransformData' and raw[doff+dsize-4:doff+dsize]==b'\0'*4
                replacements[data_id]=raw[doff:doff+dsize-4]+struct.pack('<II',len(keys),1)+b''.join(struct.pack('<ff',t,s) for t,s in keys)
    del nf
    assert len(replacements)==len(scales), (len(replacements),len(scales))
    # Locate the block-size array in the existing header.
    pos=raw.index(b'\n')+1+4+1+4+4+4
    for _ in range(3): pos+=1+raw[pos]
    types=struct.unpack_from('<H',raw,pos)[0]; pos+=2
    for _ in range(types): n=struct.unpack_from('<I',raw,pos)[0]; pos+=4+n
    pos+=2*parsed['n_bloques']
    header=bytearray(raw[:parsed['bloques'][0][1]])
    for idx,new in replacements.items(): struct.pack_into('<I',header,pos+idx*4,len(new))
    body=b''.join(replacements.get(idx,raw[off:off+size]) for idx,(typ,off,size) in enumerate(parsed['bloques']))
    last=parsed['bloques'][-1]; footer=raw[last[1]+last[2]:]
    path.write_bytes(bytes(header)+body+footer)

def select(objects, active=None):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects: o.select_set(True)
    bpy.context.view_layer.objects.active = active or objects[0]

def clear():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    for a in list(bpy.data.actions): bpy.data.actions.remove(a)

def empty(name, parent=None, location=(0,0,0), root=False):
    o = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(o)
    o.parent = parent
    o.location = location
    o['pynBlockName'] = 'BSFadeNode' if root else 'NiNode'
    o['pynNodeName'] = name
    o['pynNodeFlags'] = FLAGS
    if root: o['pynRoot'] = True
    return o

def materials():
    clear()
    specs = [
      ('architecture/farmhouse/lumbermill01.nif', {'wood':'woodpost02.dds','floor':'woodwalkway01.dds','rope':'rope01.dds'}),
      ('clutter/civilwar/catapult/civilwarcatapult01.nif', {'metal':'cwcatapult01.dds'}),
      ('dlc01/traps/crossbowtraps/plaincrossbow/plaincrossbowtrap01.nif', {'bolt':'bolt.dds'})]
    mats = {}
    report = {}
    for path, wanted in specs:
        before = set(bpy.data.materials)
        bpy.context.view_layer.objects.active = None
        bpy.ops.import_scene.pynifly(filepath=str(Path(CFG['extracted'])/'meshes'/path), blender_xf=False, import_animations=False, import_collisions=False, create_bones=False)
        fresh = sorted(set(bpy.data.materials)-before, key=lambda m:m.name)
        for key, suffix in wanted.items():
            matches = [m for m in fresh if m.get('BSShaderTextureSet_Diffuse','').lower().endswith(suffix)]
            if key=='metal': matches = [m for m in matches if m.get('BSShaderTextureSet_EnvMap')]
            if not matches: raise RuntimeError('Donor missing '+key)
            m = matches[0].copy()
            m.name = 'Astra_Vanilla_'+key
            m.use_fake_user = True
            # Solid boards retain the donor shader but do not use its cutout alpha.
            if key=='floor':
                for k in ('NiAlphaProperty_flags','NiAlphaProperty_threshold'):
                    if k in m: del m[k]
                # v08: PyNifly writes NiAlphaProperty while the shader's 'Alpha Property'
                # input stays linked (shader_io._export_alpha); v07 still shipped the cutout.
                for node in m.node_tree.nodes:
                    if 'Alpha Property' in node.inputs:
                        for link in list(node.inputs['Alpha Property'].links): m.node_tree.links.remove(link)
            mats[key] = m
            report[key] = {'donor':path, 'diffuse':m.get('BSShaderTextureSet_Diffuse'), 'normal':m.get('BSShaderTextureSet_Normal'), 'shader':m.get('Shader_Type','Default'), 'source_material':matches[0].name}
        clear()
    (ROOT/'reports/material_donors.json').write_text(json.dumps(report,indent=2))
    bpy.data.libraries.write(str(ROOT/'build/donor_materials.blend'),set(mats.values()),fake_user=True)
    return {key:mat.name for key,mat in mats.items()}

def material_key(name):
    n = name.lower()
    if 'canamo' in n: return 'rope'
    if any(t in n for t in ('hierro','acero','huecos')): return 'metal'
    if 'pluma' in n or 'estandarte' in n or 'cuero' in n: return 'bolt'
    if 'tablas' in n: return 'floor'
    return 'wood'

def remap_uv(o, keys):
    """Long grain follows each source component's longest local axis.

    Wood is tileable. Metal samples a measured solid iron region of the
    catapult atlas, instead of spreading its wood/rope regions over rivets.
    Curved source ropes retain their sweep UV. No atlas is redistributed.
    """
    mesh = o.data
    uv = mesh.uv_layers.active or mesh.uv_layers.new(name='UVMap')
    bounds = [[min(v.co[i] for v in mesh.vertices),max(v.co[i] for v in mesh.vertices)] for i in range(3)]
    longest = max(range(3),key=lambda i:bounds[i][1]-bounds[i][0])
    for p in mesh.polygons:
        key = keys[p.material_index]
        if key=='rope': continue
        normal_axis = max(range(3),key=lambda i:abs(p.normal[i]))
        axes = [i for i in range(3) if i!=normal_axis]
        if longest in axes: axes.remove(longest); axes.append(longest)
        for li in p.loop_indices:
            co = mesh.vertices[mesh.loops[li].vertex_index].co
            if key=='wood':
                # WoodPost02 is an atlas: its right quarter contains end grain.
                # Tile only along V; side U stays inside the measured wood band.
                u=(co[axes[0]]-bounds[axes[0]][0])/max(1e-8,bounds[axes[0]][1]-bounds[axes[0]][0])
                if normal_axis==longest:
                    v=(co[axes[1]]-bounds[axes[1]][0])/max(1e-8,bounds[axes[1]][1]-bounds[axes[1]][0])
                    uv.data[li].uv=(.78+.20*u,.02+.22*v)
                else: uv.data[li].uv=(.03+.65*u,co[axes[1]]/1.8)
            elif key=='floor':
                # Walkway grain runs horizontally in the vanilla texture.
                uv.data[li].uv=(co[axes[1]]/1.8,co[axes[0]]/.6)
            elif key=='metal':
                vals=[(co[i]-bounds[i][0])/max(1e-8,bounds[i][1]-bounds[i][0]) for i in axes]
                uv.data[li].uv=(.05+.15*vals[0], .55+.15*vals[1])
            else:
                vals=[(co[i]-bounds[i][0])/max(1e-8,bounds[i][1]-bounds[i][0]) for i in axes]
                if 'punta' in o.name.lower(): uv.data[li].uv=(.02+.14*vals[0],.04+.22*vals[1])
                elif 'pluma' in o.name.lower(): uv.data[li].uv=(.19+.095*vals[0],.55+.44*vals[1])
                elif 'astil' in o.name.lower(): uv.data[li].uv=(.03+.13*vals[0],.35+.63*vals[1])
                else: uv.data[li].uv=(.34+.40*vals[0],.08+.40*vals[1])

def box_faces(base):
    return [(base,base+1,base+2,base+3),(base+4,base+7,base+6,base+5),(base,base+4,base+5,base+1),
            (base+1,base+5,base+6,base+2),(base+2,base+6,base+7,base+3),(base+3,base+7,base+4,base)]

def box_verts(lo, hi):
    return [(lo[0],lo[1],lo[2]),(hi[0],lo[1],lo[2]),(hi[0],hi[1],lo[2]),(lo[0],hi[1],lo[2]),
            (lo[0],lo[1],hi[2]),(hi[0],lo[1],hi[2]),(hi[0],hi[1],hi[2]),(lo[0],hi[1],hi[2])]

def iron_mesh(name, parent, boxes, ring=None, spike=None, mat=None):
    """v10 iron sights in the parent's local units: boxes, an optional ring about +Y and a spike."""
    vertices, faces = [], []
    for lo, hi in boxes:
        base = len(vertices); vertices += box_verts(lo, hi); faces += box_faces(base)
    if ring:
        (cx, cy, cz), major, minor, n, m = ring
        base = len(vertices)
        for i in range(n):
            a = math.tau*i/n
            for j in range(m):
                b = math.tau*j/m; r = major + minor*math.cos(b)
                vertices.append((cx + r*math.cos(a), cy + minor*math.sin(b), cz + r*math.sin(a)))
        for i in range(n):
            for j in range(m):
                faces.append((base+i*m+j, base+((i+1)%n)*m+j, base+((i+1)%n)*m+(j+1)%m, base+i*m+(j+1)%m))
    if spike:
        (x, y, z0), half, top = spike
        base = len(vertices)
        vertices += [(x-half,y-half,z0),(x+half,y-half,z0),(x+half,y+half,z0),(x-half,y+half,z0),(x,y,top)]
        faces += [(base,base+3,base+2,base+1),(base,base+1,base+4),(base+1,base+2,base+4),(base+2,base+3,base+4),(base+3,base,base+4)]
    mesh = bpy.data.meshes.new(name+'_mesh'); mesh.from_pydata(vertices, [], faces); mesh.update()
    o = bpy.data.objects.new(name, mesh); bpy.context.scene.collection.objects.link(o); o.parent = parent
    mesh.materials.append(mat)
    bm = bmesh.new(); bm.from_mesh(mesh); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(mesh); bm.free()
    remap_uv(o, ['metal'])
    return o

def add_iron_sights(pitch, mats):
    """v10 (user, 2026-10-05): rear ring (alza) at the sight anchor and a front post (guion) on an
    arch at the wood front of the stock. AstraSight moves the post node onto the zero line each frame;
    here it is placed for flat fire. Everything clears the bolt (x within 7.3, z below 27.3)."""
    import sight_pose
    sc = CFG['sight']; rear = tuple(CFG.get('camera_local_units',(0,80,40))); y_post = sc['front_post_local_y']
    pivot = CFG['pitch_pivot_units']
    world = lambda v: (v[0], v[1], v[2]+pivot)
    flat = sight_pose.pose(world(rear), (-1,0,0), world((0,-224,19.6)), (0,-1,0), (0,0,0), (0,0,1))
    tip = (0.0, y_post, flat['front_post'][2]-pivot)
    if abs(flat['front_post'][1]-y_post) > 1e-6: raise RuntimeError('front post along-bore distance does not match config')
    rx, ry, rz = rear
    rear_parts = iron_mesh('CTRL_ELEVACION_alza', pitch,
        [((-1.1, ry-1.4, 9.0), (1.1, ry+1.4, rz-6.9)), ((-4.0, ry-4.0, 8.0), (4.0, ry+4.0, 10.5))],
        ring=((rx, ry, rz), 6.5, 1.1, 24, 6), mat=mats['metal'])
    arch = iron_mesh('CTRL_ELEVACION_guion_arco', pitch,
        [((-13.0, y_post-1.5, 14.0), (-10.5, y_post+1.5, 31.5)), ((10.5, y_post-1.5, 14.0), (13.0, y_post+1.5, 31.5)),
         ((-13.0, y_post-1.5, 29.0), (13.0, y_post+1.5, 31.5))], mat=mats['metal'])
    node = empty(sc['front_post_node'], pitch, tip)
    post = iron_mesh('AstraSightFrontPost_guion', node, [((-1.2,-1.2,-10.0),(1.2,1.2,-2.4))],
        spike=((0.0,0.0,-2.4), 1.2, 0.0), mat=mats['metal'])
    report = {'rear_sight_local': list(rear), 'front_post_tip_flat_local': list(tip), 'front_post_node': sc['front_post_node'],
              'ring_inner_radius': 6.5-1.1, 'arch_clear_height': 29.0, 'arch_half_width_inner': 10.5,
              'flat_camera_local': [flat['camera'][0], flat['camera'][1], flat['camera'][2]-pivot]}
    (ROOT/'reports/iron_sights.json').write_text(json.dumps(report, indent=2))
    return [rear_parts, arch, post], node

def merge_parts(parts, parent, name, mat, offset=(0,0,0)):
    vertices, faces, uvloops = [], [], []
    inverse = parent.matrix_world.inverted()
    deps = bpy.context.evaluated_depsgraph_get()
    for obj, key, indices in parts:
        evaluated = obj.evaluated_get(deps)
        mesh = evaluated.to_mesh(preserve_all_data_layers=True,depsgraph=deps)
        mesh.calc_loop_triangles()
        xf = inverse @ Matrix.Translation(Vector(offset)) @ Matrix.Scale(S,4) @ obj.matrix_world
        base = len(vertices)
        vertices.extend(tuple(xf@v.co) for v in mesh.vertices)
        for t in mesh.loop_triangles:
            if mesh.polygons[t.polygon_index].material_index not in indices: continue
            faces.append(tuple(base+i for i in t.vertices))
            uvloops.append([tuple(mesh.uv_layers.active.data[i].uv) for i in t.loops])
        evaluated.to_mesh_clear()
    mesh=bpy.data.meshes.new(name+'_mesh'); mesh.from_pydata(vertices,[],faces); mesh.update()
    o=bpy.data.objects.new(name,mesh); bpy.context.scene.collection.objects.link(o); o.parent=parent
    mesh.materials.append(mat)
    uv=mesh.uv_layers.new(name='UVMap')
    for p, coords in zip(mesh.polygons,uvloops):
        for i,c in zip(p.loop_indices,coords): uv.data[i].uv=c
    # Remove unused vertices introduced when separating source material slots.
    bm=bmesh.new(); bm.from_mesh(mesh)
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bm.to_mesh(mesh); bm.free()
    color=mesh.color_attributes.new(name='Col',type='FLOAT_COLOR',domain='CORNER')
    for v in color.data: v.color=(1,1,1,1)
    return o

def boxes_mesh(name, boxes, ramps=()):
    vertices,faces=[],[]
    cube=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    for lo,hi in boxes:
        b=len(vertices)
        vertices.extend([(lo[0],lo[1],lo[2]),(hi[0],lo[1],lo[2]),(hi[0],hi[1],lo[2]),(lo[0],hi[1],lo[2]),(lo[0],lo[1],hi[2]),(hi[0],lo[1],hi[2]),(hi[0],hi[1],hi[2]),(lo[0],hi[1],hi[2])])
        faces.extend(tuple(b+i for i in reversed(f)) for f in cube)
    for ramp in ramps:
        x0,x1,y0,y1,z0,z1=ramp[:6]
        b=len(vertices); dz=ramp[6] if len(ramp)==7 else .15*S
        vertices.extend([(x0,y0,z0-dz),(x1,y0,z0-dz),(x1,y1,z1-dz),(x0,y1,z1-dz),(x0,y0,z0),(x1,y0,z0),(x1,y1,z1),(x0,y1,z1)])
        faces.extend(tuple(b+i for i in reversed(f)) for f in cube)
    mesh=bpy.data.meshes.new(name); mesh.from_pydata(vertices,[],faces); mesh.update()
    bm=bmesh.new(); bm.from_mesh(mesh); bmesh.ops.recalc_face_normals(bm,faces=bm.faces); bmesh.ops.triangulate(bm,faces=bm.faces); bm.to_mesh(mesh); bm.free()
    return mesh

def add_collision(root, boxes, ramps=()):
    o=bpy.data.objects.new('bhkCompressedMeshShape',boxes_mesh('Astra_collision',boxes,ramps)); bpy.context.scene.collection.objects.link(o)
    o['pynCollisionFlags']='ACTIVE | SYNC_ON_UPDATE'; o['pynCollisionBlockname']='bhkCollisionObject'
    o['bhkMaterial']='WOOD'; o['motionSystem']='FIXED'; o['qualityType']='FIXED'
    o['collisionFilter_layer']='STATIC'; o['collisionFilterCopy_layer']='STATIC'
    o['bhkRadius']=.005; o['penetrationDepth']=.1
    select([o]); bpy.ops.rigidbody.object_add(); o.rigid_body.mass=0; o.rigid_body.type='PASSIVE'; o.rigid_body.collision_shape='MESH'; o.rigid_body.friction=.7
    o.hide_render=True
    root.constraints.new('COPY_TRANSFORMS').target=o
    return o

def sequences(nodes, arm_delta, rope_spec):
    endpoint_tests=[]
    # PyNifly bakes quaternion channels at integer frames. Export at the original
    # sampling density first, then compress the final key times without losing poses.
    for seq,duration in [('Fire',.6),('Reset',4.4)]:
        action=bpy.data.actions.new(seq); action['pynController']='NiControllerSequence'; action.use_fake_user=True
        final_frame=19 if seq=='Fire' else 133
        frames=range(1,final_frame+1)
        for node in nodes:
            node.animation_data_create(); node.animation_data.action=action
        for frame in frames:
            t=(frame-1)/30
            release_at=CFG['release_seconds']*.6/CFG['fire_seconds']
            progress=min(1,t/release_at) if seq=='Fire' else max(0,1-t/4.4)
            for name,delta in arm_delta.items():
                o=bpy.data.objects[name]; o.rotation_euler=Vector(delta)*progress; o.keyframe_insert(data_path='rotation_euler',frame=frame)
            bpy.context.view_layer.update()
            center=Vector((0,1.03-2.42*progress,8.83))*S-Vector((0,0,BASE*S))
            for name,arm,tip in rope_spec:
                start=bpy.data.objects[arm].matrix_world@Vector(tip)
                direction=center-start
                o=bpy.data.objects[name]; o.location=bpy.data.objects['CTRL_ELEVACION'].matrix_world.inverted()@start
                o.rotation_mode='QUATERNION'; o.rotation_quaternion=Vector((0,1,0)).rotation_difference(direction.normalized())
                ratio=direction.length/o['rest_length']
                # Escala uniforme, y tiene que serlo. export() solo recoge la
                # componente X de la escala (fc.array_index==0) y patch_scale_keys
                # escribe UN float por clave, asi que el grupo de claves de escala
                # solo puede transportar un escalar. Poner (1, ratio, 1) haria que
                # el NIF no estirara la cuerda y el extremo interno se separaria del
                # nock durante Fire/Reset.
                # Consecuencia cosmetica conocida: la cuerda adelgaza un 39% al
                # tensarse, porque el tubo hexagonal se escala en bloque. Arreglarlo
                # exige un grupo de claves con keySize=3 (tiempo, sx, sy, sz) tanto en
                # patch_scale_keys como en el importador de verify_assets, y eso hay
                # que probarlo dentro del juego antes de cambiarlo.
                o.scale=(ratio,ratio,ratio)
                for p in ('location','rotation_quaternion','scale'): o.keyframe_insert(data_path=p,frame=frame)
                bpy.context.view_layer.update(); predicted=o.matrix_world@Vector((0,o['rest_length'],0))
                endpoint_tests.append({'sequence':seq,'frame':frame,'node':name,'error':(predicted-center).length})
            bolt=bpy.data.objects['VIROTE_VISUAL']
            # La escala del virote la maneja el Papyrus (SetNodeScale 0.0 al confirmar,
            # 1.0 al recargar y al salir). tracks de escala del NIF eran un segundo
            # escritor sobre el mismo canal con otro valor (0.001), y si la animacion
            # fallaba dejaba el virote invisible sin nada que lo restaurara.
            bolt.location=(0,0,0); bolt.keyframe_insert(data_path='location',frame=frame)
        action.use_frame_range=True; action.frame_start=1; action.frame_end=final_frame
        for layer in action.layers:
            for strip in layer.strips:
                for cb in strip.channelbags:
                    for fc in cb.fcurves:
                        for kp in fc.keyframe_points:
                            kp.interpolation='BEZIER'; kp.handle_left_type='VECTOR'; kp.handle_right_type='VECTOR'
                        if fc.data_path=='scale' and cb.slot_handle==bpy.data.objects['VIROTE_VISUAL'].animation_data.action_slot.handle:
                            for kp in fc.keyframe_points: kp.interpolation='CONSTANT'
    for o in nodes:
        o['pynActionSlots']=json.dumps({'Fire':o.name,'Reset':o.name})
        o.animation_data.action=bpy.data.actions['Fire']
    bpy.context.scene.frame_set(1); bpy.context.view_layer.update()
    return endpoint_tests

def export(name, root, objects, animated=False):
    flags=empty('BSXFlags:'+name,root); flags['BSXFlags_Name']='BSX'; flags['BSXFlags_Value']=('HAVOC | DYNAMIC | ARTICULATED' if name=='virote' else 'HAVOC | COMPLEX'+(' | ANIMATED | ARTICULATED' if animated else ''))
    select(objects+[root,flags],root)
    path=ROOT/'mod/meshes/AstraAsedio'/f'{name}.nif'
    scales={}
    if animated:
        for action in bpy.data.actions:
            for layer in action.layers:
                for strip in layer.strips:
                    for cb in strip.channelbags:
                        for fc in list(cb.fcurves):
                            if fc.data_path=='scale':
                                if fc.array_index==0: scales[(action.name,cb.slot.name_display)]=[((kp.co.x-1)/30,kp.co.y) for kp in fc.keyframe_points]
                                cb.fcurves.remove(fc)
    bpy.ops.export_scene.pynifly(filepath=str(path),target_game='SKYRIMSE',blender_xf=False,intuit_defaults=False,export_animations=animated,preserve_hierarchy=True,export_modifiers=False,export_colors=True)
    if scales:
        patch_scale_keys(path,scales)
        for (seq,node),keys in scales.items():
            obj=bpy.data.objects[node]; obj.animation_data.action=bpy.data.actions[seq]
            obj.animation_data.action_slot=next(s for s in obj.animation_data.action.slots if s.name_display==node)
            for t,s in keys:
                obj.scale=(s,s,s); obj.keyframe_insert(data_path='scale',frame=t*30+1)
        for node in {n for s,n in scales}:
            obj=bpy.data.objects[node]; obj.animation_data.action=bpy.data.actions['Fire']; obj.animation_data.action_slot=next(s for s in obj.animation_data.action.slots if s.name_display==node)
        bpy.context.scene.frame_set(1); bpy.context.view_layer.update()
    if animated:
        from retime_v07 import retime
        compressed,retimed=retime(path,{'Fire':CFG['fire_seconds'],'Reset':CFG['reset_seconds']})
        path.write_bytes(compressed)
        # v08: the shipped ballesta.nif comes from this build, so its timing receipt does too.
        (ROOT/'reports/animation_retime.json').write_text(json.dumps(retimed,indent=2))
    return str(path)

def bolt_points(objects, placement):
    """Evaluated vertices of source bolt parts with merge_parts' transform plus the bolt placement."""
    deps=bpy.context.evaluated_depsgraph_get(); points=[]
    for obj in objects:
        evaluated=obj.evaluated_get(deps); mesh=evaluated.to_mesh()
        m=placement@Matrix.Translation(Vector((0,0,-8.83*S)))@Matrix.Scale(S,4)@obj.matrix_world
        points.extend(m@v.co for v in mesh.vertices)
        evaluated.to_mesh_clear()
    return points

def patch_projectile_body(path, half, centre, shaft_names):
    """v08 B3: fit the copied steel-bolt Havok box to this bolt.

    The donor box measures the 0.83 m steel bolt (20 % of this one), and the
    exporter rewrote it with a permuted body frame while keeping the donor
    inertia, so the least-inertia axis ended on the 0.25 u thickness. Fixed-size
    fields are rewritten in place; the inertia keeps the donor's per-axis ratio
    to the box formula (heuristic: no vanilla dynamic body of this size exists).
    """
    import nif_fisica
    donor_path=Path(CFG['extracted'])/'meshes/dlc01/weapons/crossbow/boltprojectile.nif'
    donor=nif_fisica.cuerpos_caja(nif_nodos.leer(str(donor_path)))[0]
    body=CFG['projectile_body']; semi=[v/nif_fisica.HK for v in half]
    long_axis=lambda v:max(range(3),key=lambda k:v[k])
    if long_axis(donor['semiejes_hk'])!=1 or long_axis(semi)!=1:raise RuntimeError('Donor and bolt boxes must share the body Y long axis')
    inertia=nif_fisica.inercia_por_donante(donor,semi,body['mass'])
    box=nif_fisica.parchear_cuerpo_caja(path,half,centre,body['mass'],body['restitution'],inertia,tuple(donor['rotacion']))
    coverage=nif_fisica.cobertura(nif_nodos.leer(str(path)))[0]
    failures=nif_fisica.reglas_vanilla(box)
    if coverage['fraccion']<nif_fisica.COBERTURA_MINIMA or not nif_fisica.inercia_alineada(box) or failures:
        raise RuntimeError('Projectile body patch failed its own checks: %s %s'%(coverage,failures))
    report={'mass':body['mass'],'restitution':body['restitution'],'half_extents_units':list(half),'centre_units':list(centre),
            'half_extents_havok':box['semiejes_hk'],'radius_havok':box['radio'],'rotation_xyzw':box['rotacion'],'inertia':box['inercia'],
            'box_coverage':coverage['fraccion'],'visual_length_units':coverage['largo_visual'],'inertia_axis_aligned':True,'vanilla_rules_failures':failures,
            'shaft_parts':sorted(shaft_names),'donor':str(donor_path.relative_to(Path(CFG['extracted']))),'donor_inertia':donor['inercia'],
            'inertia_rule':'HEURISTIC: donor inertia/box-formula ratio kept per axis','mass_rule':'HEURISTIC: no vanilla dynamic body of this size',
            'in_game_verified':False}
    (ROOT/'reports/projectile_body.json').write_text(json.dumps(report,indent=2))
    return report

def main():
    addon_utils.enable('io_scene_nifly',default_set=True)
    material_names=materials()
    bpy.ops.wm.open_mainfile(filepath=CFG['source'],use_scripts=False); bpy.context.scene.frame_set(1)
    sys.path.insert(0,str(ROOT/'scripts'))
    from mechanism_source_fixes import apply as fix_mechanism
    fix_mechanism(ROOT)
    from limb_tie_fixes import apply as fix_limb_ties
    fix_limb_ties(ROOT)
    with bpy.data.libraries.load(str(ROOT/'build/donor_materials.blend'),link=False) as (src,dst):
        dst.materials=list(material_names.values())
    mats={key:bpy.data.materials[name] for key,name in material_names.items()}
    bpy.context.scene.render.fps=30
    source=[o for o in bpy.context.scene.objects if o.type=='MESH' and not any(c.name.startswith(('90_','95_')) for c in o.users_collection)]
    arms={name:list(bpy.data.objects[name].rotation_euler) for name in ['CTRL_BRAZO_I','CTRL_BRAZO_D']}
    bpy.context.scene.frame_set(153)
    delta={name:[v-a for v,a in zip(bpy.data.objects[name].rotation_euler,rest)] for name,rest in arms.items()}
    bpy.context.scene.frame_set(1); bpy.context.view_layer.update()
    snapshots={o.name:o.matrix_world.copy() for o in bpy.data.objects}
    for o in bpy.data.objects:
        if o.animation_data: o.animation_data_clear()
    for a in list(bpy.data.actions): bpy.data.actions.remove(a)
    groups=defaultdict(list)
    source_boxes=[]; floor_groups=defaultdict(list); steps=defaultdict(list)
    for o in source:
        keys=[material_key(m.name) for m in o.data.materials]
        if not keys: raise RuntimeError('Materialless source '+o.name)
        if o.parent and o.parent.name=='CTRL_PROYECTIL': keys=['bolt']*len(keys)
        remap_uv(o,keys)
        if any(c.name=='04_Ballesta' for c in o.users_collection):
            parent=o.parent.name if o.parent else 'AstraBallesta'
            if o.name=='Cuerda_principal': continue
            if parent=='CTRL_PROYECTIL': parent='VIROTE_VISUAL'
            for k in sorted(set(keys)): groups[('ballesta',parent,k)].append((o,k,[i for i,v in enumerate(keys) if v==k]))
        else:
            for k in sorted(set(keys)): groups[('torre','AstraTorre',k)].append((o,k,[i for i,v in enumerate(keys) if v==k]))
            corners=[o.matrix_world@Vector(v) for v in o.bound_box]
            lo=[min(v[i] for v in corners) for i in range(3)]; hi=[max(v[i] for v in corners) for i in range(3)]
            n=o.name.split('.')[0]
            if '_Peldano' in n: steps[n].append((lo,hi))
            elif any(t in n for t in ('Tablon_azotea','Descanso_azotea','Balcon_frontal','Balcon_izquierdo','Balcon_trasero','Descanso_arranque','Enlace_frontal')): floor_groups[n].append((lo,hi))
            elif any(t in n for t in ('poste','Marco_puerta','Puerta_tabla','Pilar')):
                source_boxes.append((lo,hi))
            elif 'Parapeto_traves' in n or 'Baranda' in n and 'traves' in n:
                # Lower rails make continuous edge protection up to their top.
                if lo[2] < 3.7 or 6.6 < lo[2] < 7:
                    lo[2]=3.26 if hi[2]<5 else 6.485
                    source_boxes.append((lo,hi))
    # Exterior circulation needs four broad solid log walls, not one collision
    # box per log. The original closed decorative door remains a closed wall.
    source_boxes.extend([
      ((-2.17,-2.13,0),(2.17,-1.73,6.05)),
      ((-2.17,1.73,0),(2.17,2.13,6.05)),
      ((-2.13,-1.73,0),(-1.73,1.73,6.05)),
      ((1.73,-1.73,0),(2.13,1.73,6.05))])
    unique={tuple(round(v,4) for p in box for v in p):box for box in source_boxes}
    source_boxes=list(unique.values())
    floorboxes=[]; walk=[]
    for name,parts in floor_groups.items():
        lo=[min(a[i] for a,b in parts) for i in range(3)]; hi=[max(b[i] for a,b in parts) for i in range(3)]
        floorboxes.append((lo,hi)); walk.append({'name':name,'min':lo,'max':hi})
    ramps=[]; ramp_report=[]; rails=[]
    for name,parts in steps.items():
        parts.sort(key=lambda p:p[0][1]); lo=parts[0][0]; hi=parts[-1][1]
        # Bottom intercept at ground/landing, top exactly joins landing.
        z0=0 if 'inferior' in name else 3.26; z1=3.26 if 'inferior' in name else 6.485
        x0=min(a[0] for a,b in parts); x1=max(b[0] for a,b in parts)
        y0=lo[1]; y1=hi[1]
        ramps.append(tuple(v*S for v in (x0,x1,y0,y1,z0,z1)))
        ramp_report.append({'name':name,'x':[x0*S,x1*S],'y':[y0*S,y1*S],'z':[z0*S,z1*S]})
        for rx0,rx1 in ([(x1-.07,x1+.03)] if 'inferior' in name else [(x0-.03,x0+.07),(x1-.07,x1+.03)]):
            rails.append(tuple(v*S for v in (rx0,rx1,y0,y1,z0+1.05,z1+1.05,1.05)))
    tower=empty('AstraTorre',root=True); bpy.context.view_layer.update()
    tower_objs=[merge_parts(parts,tower,'Torre_'+key,mats[key]) for (asset,parent,key),parts in groups.items() if asset=='torre']
    col=add_collision(tower,[([v*S for v in a],[v*S for v in b]) for a,b in source_boxes+floorboxes],ramps+rails)
    # The fixed wooden disk stands 8.75 units above the continuous roof floor.
    # Support its surface so a player standing at the crank does not sink in it.
    bm=bmesh.new(); bm.from_mesh(col.data)
    ring0=[bm.verts.new((2.15*S*math.cos(j*math.tau/24),2.15*S*math.sin(j*math.tau/24),6.48*S)) for j in range(24)]
    ring1=[bm.verts.new((v.co.x,v.co.y,6.61*S)) for v in ring0]
    bm.faces.new(tuple(reversed(ring0))); bm.faces.new(tuple(ring1))
    for j in range(24): bm.faces.new((ring0[j],ring0[(j+1)%24],ring1[(j+1)%24],ring1[j]))
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces); bmesh.ops.triangulate(bm,faces=bm.faces)
    bm.to_mesh(col.data); bm.free(); col.data.update()
    tower_objs.append(col)
    export('torre',tower,tower_objs)
    # Park original source objects outside the export selection.
    ball=empty('AstraBallesta',root=True)
    yaw=empty('CTRL_GIRO_360',ball,(0,0,(8.3-BASE)*S))
    pitch=empty('CTRL_ELEVACION',yaw,(0,0,.25*S))
    left=empty('CTRL_BRAZO_I',pitch,(-.17*S,-1.872*S,.015*S))
    right=empty('CTRL_BRAZO_D',pitch,(.17*S,-1.872*S,.015*S))
    bolt=empty('VIROTE_VISUAL',pitch)
    projectile=empty('ProjectileNode',pitch,(0,-3.2*S,.28*S)); projectile.rotation_euler.z=math.pi
    sight=empty(CFG.get('camera_node','AstraSightCameraNode'),pitch,tuple(CFG.get('camera_local_units',(0,80,40))))
    # Logical +Y forward follows the projectile. Native FP convention is adapted
    # from the engine's original rotation; this is not a camera quaternion.
    sight.rotation_euler.z=math.pi
    operator=empty('OperatorNode',ball,(1.05*S,1.45*S,1.7*S))
    # Source controls have the same names; use explicit mapping, not Blender's .001 names.
    node_map={'AstraBallesta':ball,'CTRL_GIRO_360':yaw,'CTRL_ELEVACION':pitch,'CTRL_BRAZO_I':left,'CTRL_BRAZO_D':right,'VIROTE_VISUAL':bolt}
    for desired,obj in node_map.items():
        old=bpy.data.objects.get(desired)
        if old and old is not obj: old.name='SOURCE_'+desired
        obj.name=desired; obj['pynNodeName']=desired
    bpy.context.view_layer.update()
    ball_objs=[merge_parts(parts,node_map[parent],parent+'_'+key,mats[key],(0,0,-BASE*S)) for (asset,parent,key),parts in groups.items() if asset=='ballesta']
    ropes=[]; rope_spec=[]
    for name,arm,sign in [('Cuerda_I',left,-1),('Cuerda_D',right,1)]:
        node=empty(name,pitch); ropes.append(node)
        resttip=Vector((sign*1.89,-1.445,8.83))*S-Vector((0,0,BASE*S))
        center=Vector((0,1.03,8.83))*S-Vector((0,0,BASE*S))
        length=(center-resttip).length; node['rest_length']=length
        # Six-sided tube along +Y, transformed and lengthened by its own node.
        vertices=[]
        for y in (0,length):
            for j in range(6): vertices.append((.027*S*math.cos(j*math.tau/6),y,.027*S*math.sin(j*math.tau/6)))
        faces=[(j,(j+1)%6,(j+1)%6+6,j+6) for j in range(6)]
        faces.extend([tuple(range(5,-1,-1)),tuple(range(6,12))])
        mesh=bpy.data.meshes.new(name+'_mesh'); mesh.from_pydata(vertices,[],faces); mesh.materials.append(mats['rope']); mesh.update()
        o=bpy.data.objects.new(name+'_shape',mesh); bpy.context.scene.collection.objects.link(o); o.parent=node
        uv=mesh.uv_layers.new(name='UVMap')
        for p in mesh.polygons:
            for li in p.loop_indices:
                idx=mesh.loops[li].vertex_index; uv.data[li].uv=((idx%6)/6,(idx//6)*6)
        ball_objs.append(o)
        tip=arm.matrix_world.inverted()@resttip
        rope_spec.append((name,arm.name,tuple(tip)))
    endpoint=sequences([left,right,bolt]+ropes,delta,rope_spec)
    fixed=[o for o in ball_objs if o.parent is ball]
    # Dragon elevation: retain local animation pivots and extend the fixed
    # support from its unchanged base before raising the complete rotating head.
    lift=float(CFG.get('mount_raise_units',0.0))
    old_fixed_min=min(v.co.z for o in fixed for v in o.data.vertices)
    old_fixed_max=max(v.co.z for o in fixed for v in o.data.vertices)
    if lift:
        support_scale=(old_fixed_max-old_fixed_min+lift)/(old_fixed_max-old_fixed_min)
        for o in fixed:
            for v in o.data.vertices:
                v.co.z=old_fixed_min+(v.co.z-old_fixed_min)*support_scale
            o.data.update()
        yaw.location.z+=lift
        bpy.context.view_layer.update()
    (ROOT/'reports/mount_revision.json').write_text(json.dumps({'raise_units':lift,'fixed_base_before':old_fixed_min,'fixed_base_after':min(v.co.z for o in fixed for v in o.data.vertices),'fixed_top_before':old_fixed_max,'fixed_top_after':max(v.co.z for o in fixed for v in o.data.vertices),'yaw_pivot_z':yaw.location.z,'pitch_pivot_z':yaw.location.z+pitch.location.z,'moving_local_pivots_unchanged':True,'source_original_modified':False},indent=2))
    verts=[o.matrix_world@v.co for o in fixed for v in o.data.vertices]
    lo=[min(v[i] for v in verts) for i in range(3)]; hi=[max(v[i] for v in verts) for i in range(3)]
    # v10: the v09 camera recorder showed Skyrim pulling the sight camera toward the player head when this
    # box (137.6 u, above the ~109 u eye) lay between them. Below the eye line it still keeps players out.
    hi[2]=min(hi[2],lo[2]+CFG['sight']['pedestal_collision_height_units'])
    ball_col=add_collision(ball,[(lo,hi)]); ball_objs.append(ball_col)
    sights,front_post=add_iron_sights(pitch,mats); ball_objs.extend(sights)
    export('ballesta',ball,ball_objs+[yaw,pitch,left,right,bolt,projectile,sight,front_post,operator]+ropes,True)
    # Standalone projectile preserves the loaded siege bolt's dimensions.
    # Place its leading tip at the muzzle and point it along local +Y.
    proj=empty('AstraVirote',root=True); bpy.context.view_layer.update()
    parts=[p for (asset,parent,key),ps in groups.items() if asset=='ballesta' and parent=='VIROTE_VISUAL' for p in ps]
    shape=merge_parts(parts,proj,'AstraVirote_shape',mats['bolt'],(0,0,-8.83*S))
    xf=Matrix.Translation((0,-3.02*S,0))@Matrix.Rotation(math.pi,4,'Z')
    shape.data.transform(xf)
    # v08 B3: full bolt length from every part, cross-section from the shaft only (not the fletching or broadhead).
    placement=xf@proj.matrix_world.inverted()
    every=bolt_points({o for o,k,i in parts},placement)
    shaft_objects={o for o,k,i in parts if 'astil' in o.name.lower()}
    if not shaft_objects:raise RuntimeError('The bolt has no shaft part')
    shaft=bolt_points(shaft_objects,placement)
    ylo=min(p.y for p in every); yhi=max(p.y for p in every)
    xlo=min(p.x for p in shaft); xhi=max(p.x for p in shaft); zlo=min(p.z for p in shaft); zhi=max(p.z for p in shaft)
    bolt_half=((xhi-xlo)/2,(yhi-ylo)/2,(zhi-zlo)/2); bolt_centre=((xhi+xlo)/2,(yhi+ylo)/2,(zhi+zlo)/2)
    # Preserve the real steel projectile's Havok body, filter and box shape.
    before=set(bpy.data.objects); select([shape]); bpy.ops.object.select_all(action='DESELECT'); bpy.context.view_layer.objects.active=None
    bpy.ops.import_scene.pynifly(filepath=str(Path(CFG['extracted'])/'meshes/dlc01/weapons/crossbow/BoltProjectile.nif'),blender_xf=False,import_animations=False,create_bones=False)
    donor_objects=set(bpy.data.objects)-before
    projectile_col=next(o for o in donor_objects if o.name.startswith('bhkBoxShape'))
    donor_root=next(o for o in donor_objects if o.get('pynRoot'))
    proj['pynNodeFlags']=donor_root['pynNodeFlags']
    proj.constraints.new('COPY_TRANSFORMS').target=projectile_col
    projectile_col.hide_render=True
    for o in donor_objects-{projectile_col}: bpy.data.objects.remove(o,do_unlink=True)
    export('virote',proj,[shape,projectile_col])
    patch_projectile_body(ROOT/'mod/meshes/AstraAsedio/virote.nif',bolt_half,bolt_centre,[o.name for o in shaft_objects])
    # Keep only new objects in the editable export scene.
    for o in list(source): bpy.data.objects.remove(o,do_unlink=True)
    for o in list(bpy.data.objects):
        if o.name.startswith(('SOURCE_','Camera','Light','Referencia','CTRL_PROYECTIL')) or any(c.name.startswith(('90_','95_')) for c in o.users_collection): bpy.data.objects.remove(o,do_unlink=True)
    bpy.context.scene.render.fps=30
    for name,old,new in [('Fire',.6,CFG['fire_seconds']),('Reset',4.4,CFG['reset_seconds'])]:
        action=bpy.data.actions[name];factor=new/old
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for curve in bag.fcurves:
                        for key in curve.keyframe_points:
                            for point in (key.co,key.handle_left,key.handle_right):point.x=1+(point.x-1)*factor
        action.frame_end=1+30*new
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'source/Astra_export.blend'))
    report={'elevation_sign':-1,'yaw_rest_matrix':[1,0,0,0,1,0,0,0,1],'pitch_rest_matrix':[1,0,0,0,1,0,0,0,1],'ballesta_placement_z':BASE*S,'OperatorNode':list(operator.location),'ProjectileNode':list(projectile.location),'arm_delta':delta,'rope_endpoint_max_error':max(e['error'] for e in endpoint),'rope_endpoint_samples':len(endpoint),'floor_surfaces':walk,'ramps':ramp_report,'collision_triangles':len(col.data.polygons)+len(ball_col.data.polygons),'donor_uv_note':'wood local-axis grain; inspected solid metal region u=.05..20,v=.55..70; bolt projected regions; render review required'}
    (ROOT/'reports/assets.json').write_text(json.dumps(report,indent=2))
    (ROOT/'reports/collision_walkable.json').write_text(json.dumps({'floors_units':[{'name':w['name'],'min':[v*S for v in w['min']],'max':[v*S for v in w['max']]} for w in walk],'ramps':ramp_report,'solid_boxes_units':[{'min':[v*S for v in a],'max':[v*S for v in b]} for a,b in source_boxes],'stair_edge_barriers_units':[{'min':[r[0],r[2],r[4]-r[6]],'max':[r[1],r[3],r[5]]} for r in rails],'ballesta_fixed_box_units':{'min':lo,'max':hi},'walkable_disk_units':{'center':[0,0],'radius':150.5,'top_z':462.7,'step_from_roof':8.75,'ck_navmesh_surface_adjustment_pending':True}},indent=2))
    print('ASTRA_ASSETS_BUILT')

if __name__=='__main__': main()
