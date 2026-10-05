"""v09 tower: straight side stair (Ballesta_Astra_Escalera_Directa_v01 design) plus the rustic pass.

Runs in Blender after build_assets.py and replaces ONLY torre.nif. It rebuilds the stair from the
preserved v04 source, measures the collision boxes, then bends the visual meshes (rustico.py), so
the Havok shapes, the walkable route and the navmesh inputs are exactly those of the square stair
design (reports/reference_collision_escalera_directa.json). It also refreshes the tower bounds in
reports/assets.json, which build_plugin.py turns into the STAT OBND.
"""
import bpy, bmesh, addon_utils, json, math, sys, hashlib
from pathlib import Path
from collections import defaultdict
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'scripts/vendor'))
import build_assets as A
import rustico, nif_fisica, nif_nodos
S=A.S
# Design chosen by the user for the other agent's stair: gentle slope, single flight.
X0,X1,Y1,Z1=4.02,5.22,2.8,6.485
SLOPE=3.225/5.2
Y0=Y1-Z1/SLOPE
COUNT=34
TREAD=(Y1-Y0)/COUNT
RISE=Z1/COUNT

def bounds(o):
    p=[o.matrix_world@Vector(v) for v in o.bound_box]
    return ([min(v[i] for v in p) for i in range(3)],[max(v[i] for v in p) for i in range(3)])

def cube(name,center,size,material,collection):
    bpy.ops.mesh.primitive_cube_add(size=1,location=center)
    o=bpy.context.object; o.name=name
    for c in list(o.users_collection): c.objects.unlink(o)
    collection.objects.link(o)
    o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(material)
    bevel=o.modifiers.new('Bisel_madera','BEVEL');bevel.width=.009;bevel.segments=1
    bpy.ops.object.modifier_apply(modifier=bevel.name)
    return o

def beam(name,a,b,width,depth,material,collection):
    a,b=Vector(a),Vector(b);d=b-a
    o=cube(name,(a+b)/2,(width,depth,d.length),material,collection)
    o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
    return o

def main():
    # build_assets.py has just written the v08-layout walkable data; keep its weapon-side keys.
    base=json.loads((ROOT/'reports/collision_walkable.json').read_text())
    addon_utils.enable('io_scene_nifly',default_set=True)
    bpy.context.preferences.addons['io_scene_nifly'].preferences.sky_texture_path_1=str(Path(A.CFG['extracted'])/'textures')
    names=A.materials()
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'source/Torre_Ballesta_lowpoly_v04.blend'),use_scripts=False)
    bpy.context.scene.frame_set(1)
    with bpy.data.libraries.load(str(ROOT/'build/donor_materials.blend'),link=False) as (src,dst):
        dst.materials=list(names.values())
    mats={k:bpy.data.materials[v] for k,v in names.items()}
    coll=bpy.data.collections['02_Escaleras']
    removed=sorted(o.name for o in coll.all_objects)
    wood=bpy.data.materials['Madera_envejecida_PREVIEW']
    # Reuse the original beveled tread mesh, including its local detail.
    template=bpy.data.objects['V04_Tramo_superior_Peldano'].data.copy()
    for o in list(coll.all_objects):bpy.data.objects.remove(o,do_unlink=True)
    for i in range(COUNT):
        mesh=template.copy()
        local_lo=[min(v.co[j] for v in mesh.vertices) for j in range(3)]
        local_hi=[max(v.co[j] for v in mesh.vertices) for j in range(3)]
        sizes=(X1-X0,TREAD,.15)
        for v in mesh.vertices:
            for j in range(3):v.co[j]=(v.co[j]-(local_lo[j]+local_hi[j])/2)*sizes[j]/(local_hi[j]-local_lo[j])
        o=bpy.data.objects.new('Astra_Directa_Peldano_%02d'%(i+1),mesh);coll.objects.link(o)
        # The smooth collision crosses each tread at its centre, within half a riser.
        o.location=((X0+X1)/2,Y0+(i+.5)*TREAD,(i+.5)*RISE-.075)
    for side,x in [('interior',X0+.06),('exterior',X1-.06)]:
        beam('Astra_Directa_Zanca_'+side,(x,Y0,-.16),(x,Y1,Z1-.16),.15,.25,wood,coll)
        for h in (.53,1.06):
            beam('Astra_Directa_Baranda_%s_%.2f'%(side,h),(x,Y0,h),(x,Y1,Z1+h),.10,.10,wood,coll)
        for i in range(15):
            y=Y0+(Y1-Y0)*i/14;z=(y-Y0)*SLOPE
            beam('Astra_Directa_Balaustre_%s_%02d'%(side,i),(x,y,z-.09),(x,y,z+1.06),.10,.10,wood,coll)
        for i,t in enumerate((.24,.48,.72)):
            y=Y0+(Y1-Y0)*t;z=Z1*t-.25
            cube('Astra_Directa_Pilar_%s_%02d'%(side,i),(x,y,z/2),(.20,.20,z),wood,coll)
    for i,t in enumerate((.24,.48,.72)):
        y=Y0+(Y1-Y0)*t;z=Z1*t-.31
        beam('Astra_Directa_Travesano_%02d'%i,(X0-.05,y,z),(X1+.05,y,z),.18,.18,wood,coll)
        for x,direction in ((X0+.06,1),(X1-.06,-1)):
            beam('Astra_Directa_Jabalcon_%02d_%d'%(i,direction),(x,y,max(.03,z-.65)),(x+direction*.40,y,z),.12,.12,wood,coll)
    bpy.context.view_layer.update()
    source=[o for o in bpy.context.scene.objects if o.type=='MESH' and any(c.name in ('01_Torre','02_Escaleras','03_Plataforma') for c in o.users_collection)]
    groups=defaultdict(list);source_boxes=[];floor_groups=defaultdict(list)
    for o in source:
        keys=[A.material_key(m.name) for m in o.data.materials]
        A.remap_uv(o,keys)
        for key in sorted(set(keys)):groups[key].append((o,key,[i for i,v in enumerate(keys) if v==key]))
        lo,hi=bounds(o);name=o.name.split('.')[0]
        if any(t in name for t in ('Tablon_azotea','Descanso_azotea')):floor_groups[name].append((lo,hi))
        elif any(t in name for t in ('poste','Marco_puerta','Puerta_tabla','Pilar')):source_boxes.append((lo,hi))
        elif 'Parapeto_traves' in name and 6.6<lo[2]<7:
            lo[2]=6.485;source_boxes.append((lo,hi))
        for j,key in enumerate(keys):o.data.materials[j]=mats[key]
    source_boxes.extend([
        ((-2.17,-2.13,0),(2.17,-1.73,6.05)),((-2.17,1.73,0),(2.17,2.13,6.05)),
        ((-2.13,-1.73,0),(-1.73,1.73,6.05)),((1.73,-1.73,0),(2.13,1.73,6.05))])
    source_boxes=list({tuple(round(v,4) for p in b for v in p):b for b in source_boxes}.values())
    floorboxes=[];walk=[]
    for name,parts in floor_groups.items():
        lo=[min(a[j] for a,b in parts) for j in range(3)];hi=[max(b[j] for a,b in parts) for j in range(3)]
        floorboxes.append((lo,hi));walk.append({'name':name,'min':[v*S for v in lo],'max':[v*S for v in hi]})
    assert len(walk)==2 and abs(max(f['max'][2] for f in walk)-Z1*S)<.001
    # Collision boxes are measured above; the rustic pass bends visual meshes only.
    aged=rustico.envejecer(source)
    floors=[v for v in aged.values() if v['piso']]
    rustic={'objects':aged,'count':len(aged),'floor_pieces':len(floors),
        'max_displacement_m':max(v['desplazamiento_max_m'] for v in aged.values()),'collision_moved':False,
        'rules':{k:list(v) for k,v in rustico.REGLAS},'thickness':rustico.GROSOR,'floor_vertical_limit_m':rustico.TOPE_PISO_Z,
        'floor_vertical_measured_m':max(v['desplazamiento_vertical_max_m'] for v in floors)}
    # Keep the tower source editable by component, with the current weapon as a reference.
    for o in list(bpy.data.objects):
        if any(c.name.startswith(('04_','90_','95_')) for c in o.users_collection):bpy.data.objects.remove(o,do_unlink=True)
    bpy.context.view_layer.objects.active=None;bpy.ops.object.select_all(action='DESELECT')
    before=set(bpy.data.objects)
    bpy.ops.import_scene.pynifly(filepath=str(ROOT/'mod/meshes/AstraAsedio/ballesta.nif'),blender_xf=False,import_animations=False,import_collisions=False,create_bones=False)
    imported=set(bpy.data.objects)-before
    for root in [o for o in imported if o.get('pynRoot')]:root.scale=(1/S,)*3;root.location.z=A.CFG['tower_top_units']/S
    ref=bpy.data.collections.new('04_Ballesta_Referencia');bpy.context.scene.collection.children.link(ref)
    for o in imported:
        for c in list(o.users_collection):c.objects.unlink(o)
        ref.objects.link(o)
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'source/Torre_escalera_rustica.blend'))
    tower=A.empty('AstraTorre',root=True);bpy.context.view_layer.update()
    objects=[A.merge_parts(parts,tower,'Torre_'+key,mats[key]) for key,parts in groups.items()]
    ramp=tuple(v*S for v in (X0,X1,Y0,Y1,0,Z1))
    rails=[tuple(v*S for v in (a,b,Y0,Y1,1.05,Z1+1.05,1.05)) for a,b in ((X0-.03,X0+.07),(X1-.07,X1+.03))]
    col=A.add_collision(tower,[([v*S for v in a],[v*S for v in b]) for a,b in source_boxes+floorboxes],[ramp]+rails)
    bm=bmesh.new();bm.from_mesh(col.data)
    r0=[bm.verts.new((2.15*S*math.cos(j*math.tau/24),2.15*S*math.sin(j*math.tau/24),6.48*S)) for j in range(24)]
    r1=[bm.verts.new((v.co.x,v.co.y,6.61*S)) for v in r0]
    bm.faces.new(tuple(reversed(r0)));bm.faces.new(tuple(r1))
    for j in range(24):bm.faces.new((r0[j],r0[(j+1)%24],r1[(j+1)%24],r1[j]))
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bmesh.ops.triangulate(bm,faces=bm.faces);bm.to_mesh(col.data);bm.free()
    A.export('torre',tower,objects+[col])
    rustic['torre_nif_sha256']=hashlib.sha256((ROOT/'mod/meshes/AstraAsedio/torre.nif').read_bytes()).hexdigest()
    (ROOT/'reports/rustico.json').write_text(json.dumps(rustic,indent=2))
    collision={'floors_units':walk,'ramps':[{'name':'Astra_Directa','x':[X0*S,X1*S],'y':[Y0*S,Y1*S],'z':[0,Z1*S]}],
        'solid_boxes_units':[{'min':[v*S for v in a],'max':[v*S for v in b]} for a,b in source_boxes],
        'stair_edge_barriers_units':[{'min':[r[0],r[2],0],'max':[r[1],r[3],r[5]]} for r in rails],
        'ballesta_fixed_box_units':base['ballesta_fixed_box_units'],'walkable_disk_units':base['walkable_disk_units']}
    (ROOT/'reports/collision_walkable.json').write_text(json.dumps(collision,indent=2))
    # Tower OBND for the ESP: visual bounds of the written NIF, read from its bytes.
    lo,hi=nif_fisica.caja_visual(nif_nodos.leer(str(ROOT/'mod/meshes/AstraAsedio/torre.nif')))
    assets=json.loads((ROOT/'reports/assets.json').read_text())
    assets['torre']={'bbox_units':{'min':lo,'max':hi},'source':'scripts/build_stairs.py (written torre.nif)'}
    (ROOT/'reports/assets.json').write_text(json.dumps(assets,indent=2))
    detail={'width_m':X1-X0,'horizontal_run_m':Y1-Y0,'rise_m':Z1,'angle_degrees':math.degrees(math.atan(SLOPE)),
        'start_m':[(X0+X1)/2,Y0,0],'end_m':[(X0+X1)/2,Y1,Z1],'steps':COUNT,'riser_m':RISE,'tread_m':TREAD,
        'handrail_height_m':1.06,'old_objects_removed':removed,'design_origin':'Ballesta_Astra_Escalera_Directa_v01',
        'rustic_pass':'scripts/rustico.py (v09 amplitudes)','weapon_and_projectile_exported':False,'game_tested':False}
    (ROOT/'reports/stair_design.json').write_text(json.dumps(detail,indent=2))
    print('STAIR_TOWER_EXPORTED',round(detail['angle_degrees'],2),round(detail['horizontal_run_m'],3),len(removed),len(aged))

if __name__=='__main__':main()
