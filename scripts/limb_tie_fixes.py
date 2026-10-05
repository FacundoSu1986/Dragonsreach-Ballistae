"""Fit closed rope bindings to measured bow/steel cross sections in memory."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

def hull2(points):
    pts=sorted(set((round(p[0],8),round(p[1],8)) for p in points))
    def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];hi=[]
    for p in pts:
        while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=1e-10:lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi)>=2 and cross(hi[-2],hi[-1],p)<=1e-10:hi.pop()
        hi.append(p)
    return [Vector((x,y,0)) for x,y in lo[:-1]+hi[:-1]]

def section(objects,frame):
    points=[];inverse=frame.inverted()
    for obj in objects:
        verts=[inverse@obj.matrix_world@v.co for v in obj.data.vertices]
        for edge in obj.data.edges:
            a,b=(verts[i] for i in edge.vertices)
            if abs(a.z)<1e-7:points.append(a)
            if a.z*b.z<0:points.append(a+(b-a)*(-a.z/(b.z-a.z)))
    hull=hull2(points)
    if len(hull)<3:raise RuntimeError('No closed limb section at binding')
    return hull

def rounded_offset(hull,distance):
    out=[]
    for i,p in enumerate(hull):
        prev=(p-hull[i-1]).normalized();after=(hull[(i+1)%len(hull)]-p).normalized()
        n0=Vector((prev.y,-prev.x,0));n1=Vector((after.y,-after.x,0))
        angle0=math.atan2(n0.y,n0.x);arc=(math.atan2(n1.y,n1.x)-angle0)%math.tau
        count=max(1,math.ceil(arc/(math.pi/9)))
        for j in range(count+1):
            angle=angle0+arc*j/count
            point=p+Vector((math.cos(angle),math.sin(angle),0))*distance
            if not out or (point-out[-1]).length>1e-6:out.append(point)
    return out

def apply(root):
    report={'original_files_modified':False,'method':'Closed six-sided rope swept around rounded measured wood+steel convex cross sections',
            'rope_radius_m':0.014,'designed_clearance_m':0.0015,'parts':[]}
    for obj in sorted(list(bpy.data.objects),key=lambda o:o.name):
        if not obj.name.startswith(('Ligadura_limbo','Ligadura_punta')):continue
        side=obj.parent.name[-1];pieces=[bpy.data.objects['Limbo_arco_'+side],bpy.data.objects['Fleje_arco_'+side]]
        world_verts=[];polys=[]
        for piece in pieces:
            off=len(world_verts);world_verts.extend(piece.matrix_world@v.co for v in piece.data.vertices)
            polys.extend(tuple(off+i for i in p.vertices) for p in piece.data.polygons)
        bvh=BVHTree.FromPolygons(world_verts,polys)
        frame=obj.matrix_world.copy();hull=section(pieces,frame);radius=report['rope_radius_m']
        path=rounded_offset(hull,radius+report['designed_clearance_m'])
        previous=[bvh.find_nearest(obj.matrix_world@v.co)[3] for v in obj.data.vertices]
        distances=[bvh.find_nearest(frame@v)[3]-radius for v in path]
        verts=[];faces=[];uvs=[];count=len(path);sides=6
        lengths=[0.]
        for i in range(1,count):lengths.append(lengths[-1]+(path[i]-path[i-1]).length)
        perimeter=lengths[-1]+(path[0]-path[-1]).length
        for i,p in enumerate(path):
            tangent=(path[(i+1)%count]-path[i-1]).normalized()
            outward=Vector((tangent.y,-tangent.x,0)).normalized()
            for j in range(sides):
                angle=math.tau*j/sides
                verts.append(tuple(p+radius*(math.cos(angle)*outward+math.sin(angle)*Vector((0,0,1)))))
        for i in range(count):
            for j in range(sides):
                faces.append((i*sides+j,i*sides+(j+1)%sides,((i+1)%count)*sides+(j+1)%sides,((i+1)%count)*sides+j))
                u0=lengths[i]/(radius*math.tau);u1=(lengths[i+1] if i+1<count else perimeter)/(radius*math.tau)
                uvs.append(((j/sides,u0),((j+1)/sides,u0),((j+1)/sides,u1),(j/sides,u1)))
        old_mesh=obj.data;materials=list(old_mesh.materials)
        mesh=bpy.data.meshes.new(obj.name+'_ajustada');mesh.from_pydata(verts,[],faces);mesh.update()
        for material in materials:mesh.materials.append(material)
        layer=mesh.uv_layers.new(name='UVMap')
        for face,coords in zip(mesh.polygons,uvs):
            face.use_smooth=True
            for li,uv in zip(face.loop_indices,coords):layer.data[li].uv=uv
        obj.data=mesh
        if old_mesh.users==0:bpy.data.meshes.remove(old_mesh)
        edges={}
        for face in mesh.polygons:
            for e in face.edge_keys:edges[e]=edges.get(e,0)+1
        if any(c!=2 for c in edges.values()):raise RuntimeError('Open rope binding '+obj.name)
        if max(distances)>0.012:raise RuntimeError('Binding does not hug limb '+obj.name+': '+str(max(distances)))
        report['parts'].append({'name':obj.name,'parent':obj.parent.name,'closed_manifold':True,'triangles':len(faces)*2,
                                'previous_max_rope_vertex_distance_to_limb_m':max(previous),
                                'centerline_clearance_min_m':min(distances),'centerline_clearance_max_m':max(distances),
                                'section_hull':[[v.x,v.y] for v in hull],'path_local':[list(v) for v in path],
                                'source_world_frame':[list(r) for r in frame]})
    if len(report['parts'])!=14:raise RuntimeError('Expected seven bindings per bow limb')
    (Path(root)/'reports/limb_ties_revision.json').write_text(json.dumps(report,indent=2))
    return report
