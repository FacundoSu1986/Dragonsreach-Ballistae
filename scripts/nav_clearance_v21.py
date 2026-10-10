"""Continuous triangle/prism proxy: 18-unit radius, 128-unit NPC headroom.

Extends each navigation triangle's plane over its horizontal safety buffer.
This deliberately checks the whole traversable surface, not selected patrol
waypoints. It cannot certify Skyrim AI, dragon physics, or save migration.
"""
import numpy as np
from shapely.geometry import Polygon,LineString,Point
from shapely.strtree import STRtree

def projection(tri):
    p=Polygon(tri[:,:2])
    if p.area>1e-8:return p
    v=np.unique(tri[:,:2],axis=0)
    if len(v)==1:return Point(v[0])
    return LineString(v)

def vertices(shape):
    if shape.is_empty:return []
    if hasattr(shape,'geoms'):return [p for g in shape.geoms for p in vertices(g)]
    if shape.geom_type=='Polygon':return list(shape.exterior.coords)
    return list(shape.coords)

def obstacle_z(tri,xy):
    a,b,c=tri
    M=np.column_stack((b[:2]-a[:2],c[:2]-a[:2]))
    if abs(np.linalg.det(M))>1e-8:
        uv=np.linalg.solve(M,np.array(xy)-a[:2]);return [a[2]+uv@np.array([b[2]-a[2],c[2]-a[2]])]
    # A vertical face projects to a line: take both heights on all three edges.
    axis=int(np.argmax(np.ptp(tri[:,:2],axis=0)));q=xy[axis];zs=[]
    for v,w in ((a,b),(b,c),(c,a)):
        delta=w[axis]-v[axis]
        if abs(delta)<1e-8:
            if abs(q-v[axis])<1e-5:zs.extend([v[2],w[2]])
        else:
            t=(q-v[axis])/delta
            if -1e-5<=t<=1+1e-5:zs.append(v[2]+t*(w[2]-v[2]))
    assert zs,('Vertical projection failed',tri,xy)
    return zs

def check(collision_triangles,nav_triangles,radius=18,height=128):
    polygons=[];planes=[];indices=[]
    for i,t in enumerate(nav_triangles):
        p=Polygon(t[:,:2])
        if p.area<1e-8:continue
        normal=np.cross(t[1]-t[0],t[2]-t[0])
        if abs(normal[2])<1e-8:continue
        planes.append((t[0],normal));polygons.append(p.buffer(radius));indices.append(i)
    tree=STRtree(polygons);hits=[]
    for ci,tri in enumerate(collision_triangles):
        shape=projection(tri)
        for ni in tree.query(shape,predicate='intersects'):
            xy=vertices(shape.intersection(polygons[ni]))
            a,n=planes[ni];d=[]
            for p in xy:
                nz=a[2]-(n[0]*(p[0]-a[0])+n[1]*(p[1]-a[1]))/n[2]
                d.extend(z-nz for z in obstacle_z(tri,p))
            if d and min(d)<=height and max(d)>=2:
                hits.append({'collision_triangle':ci,'navigation_triangle':indices[ni],'relative_z_min':float(min(d)),'relative_z_max':float(max(d))})
    return hits
