"""Make the source ratchet legible: mounted pawl, hinge pin and anchored leaf spring."""
import bpy, bmesh, math, json
from mathutils import Vector


def apply(root):
    parent=bpy.data.objects['CTRL_ELEVACION']
    collection=bpy.data.collections['04_Ballesta']
    iron=bpy.data.materials['Ballesta_hierro_forjado']
    steel=bpy.data.materials['Ballesta_acero_gastado']
    created=[]
    for name in ('Una_trinquete','Muelle_una'):
        bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True)

    def part(name, vertices, faces, material=iron, bevel=.0025):
        inverse=parent.matrix_world.inverted()
        mesh=bpy.data.meshes.new(name+'_mesh')
        mesh.from_pydata([inverse@Vector(v) for v in vertices],[],faces);mesh.update()
        obj=bpy.data.objects.new(name,mesh);collection.objects.link(obj);obj.parent=parent
        mesh.materials.append(material)
        bm=bmesh.new();bm.from_mesh(mesh)
        bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
        if bevel:
            bmesh.ops.bevel(bm,geom=list(bm.edges),offset=bevel,segments=1,affect='EDGES',clamp_overlap=True)
            bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
        bm.to_mesh(mesh);bm.free();mesh.update()
        created.append(obj)
        return obj

    def box(name,lo,hi,material=iron):
        x0,y0,z0=lo;x1,y1,z1=hi
        return part(name,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
                         (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],
                    [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],material)

    def profile(name,x0,x1,yz,material=iron,bevel=.0015):
        n=len(yz);vv=[(x,y,z) for x in (x0,x1) for y,z in yz]
        ff=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
        ff.extend((i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n))
        return part(name,vv,ff,material,bevel)

    def axle(name,x0,x1,y,z,radius,segments=12,material=steel):
        vv=[(x,y+radius*math.cos(i*math.tau/segments),z+radius*math.sin(i*math.tau/segments))
            for x in (x0,x1) for i in range(segments)]
        ff=[tuple(range(segments-1,-1,-1)),tuple(range(segments,2*segments))]
        ff.extend((i,(i+1)%segments,(i+1)%segments+segments,i+segments) for i in range(segments))
        return part(name,vv,ff,material,.001)

    # A continuous bracket reaches the side of the stock and supports the pawl.
    box('Soporte_trinquete_placa',(-.240,1.770,8.375),(-.140,1.900,8.730))
    box('Soporte_trinquete_brazo',(-.640,1.810,8.700),(-.190,1.890,8.734))
    box('Oreja_eje_trinquete_I',(-.649,1.803,8.719),(-.622,1.856,8.782))
    box('Oreja_eje_trinquete_D',(-.578,1.803,8.719),(-.551,1.856,8.782))
    profile('Una_trinquete',-.621,-.579,
            [(1.842,8.785),(1.842,8.740),(1.635,8.758),(1.603,8.736),
             (1.570,8.736),(1.568,8.781)])
    axle('Eje_una_trinquete',-.669,-.531,1.830,8.759,.018)
    axle('Cabeza_eje_trinquete_I',-.678,-.651,1.830,8.759,.032,6)
    axle('Cabeza_eje_trinquete_D',-.549,-.522,1.830,8.759,.032,6)
    # Thin leaf spring: bottom anchored to the bracket, tip rests on the pawl.
    curve=[(1.885,8.724),(1.876,8.791),(1.836,8.802),(1.795,8.791),(1.745,8.781)]
    profile('Muelle_una',-.620,-.580,curve+[(y,z-.009) for y,z in reversed(curve)],bevel=0)
    axle('Remache_anclaje_muelle',-.648,-.552,1.883,8.723,.020,8)
    for i,z in enumerate((8.438,8.597)):
        axle('Remache_soporte_trinquete_'+str(i),-.263,-.223,1.823,z,.028,8)
    # Close the small hub-to-crank gap on the opposite side of the winding drum.
    axle('Casquillo_manivela_torno',.747,.833,1.580,8.480,.052,12)
    bpy.context.view_layer.update()
    rows=[]
    for obj in created:
        pp=[obj.matrix_world@v.co for v in obj.data.vertices]
        obj.data.calc_loop_triangles()
        rows.append({'name':obj.name,'parent':parent.name,'triangles':len(obj.data.loop_triangles),
                     'bbox_m':{'min':[min(v[i] for v in pp) for i in range(3)],
                               'max':[max(v[i] for v in pp) for i in range(3)]}})
    report={'original_files_modified':False,'replaced':['Una_trinquete','Muelle_una'],
            'intent':'Pawl engages ratchet teeth, pin is seated in bracket, spring anchored and resting on pawl.',
            'new_parts':rows,'parent':'CTRL_ELEVACION','animated_individually':False}
    (root/'reports/mechanism_revision.json').write_text(json.dumps(report,indent=2))
    return created
