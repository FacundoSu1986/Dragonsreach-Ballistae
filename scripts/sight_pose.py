"""v10 sight pose: tail camera on the rear-sight -> zero-target line, front post on that line.

Pure Python (no bpy), the same formulas as Astra::sightPose in native/src/Core.cpp. Used by the
Blender verification/renders and by tests/test_v10_sight.py, which also checks the constants
against config.json and the final ESP/NIF.

World frame, game units. Inputs per frame:
  rear     rear sight centre = AstraSightCameraNode world position (the v08 camera anchor)
  right    anchor right axis (world), used to keep the camera roll of the weapon
  muzzle   ProjectileNode world position; bore = its local +Y in world
  root_pos/root_up/scale   ballista reference root
The zero target is where the bolt is after flying ZERO_RANGE along the bore: gravity pulls it
ZERO_DROP straight down (world -Z) in that time, at any elevation. The bolt flies in world units
whatever the model scale, so range and drop are not scaled; the sight geometry is.
"""
import math

ZERO_RANGE = 5250.0        # 75 m from the muzzle (sight_zero_meters * meters_to_units)
ZERO_DROP = 113.589        # 0.5 * (0.35*9.81*70) * (5250/5400)^2, PROJ gravity and speed
FRONT_POST_ALONG = 230.0   # rear sight (local y 80) to front post (local y -150, wood front of the stock) along the bore
TAIL_DISTANCE = 120.0      # camera behind the rear sight at low elevation (the "cola")
MIN_CAMERA_HEIGHT = 65.0   # camera never below this above the root (pedestal collision is 35: 30 u sweep clearance)
MIN_CAMERA_DISTANCE = 0.0


def add(a, b): return (a[0]+b[0], a[1]+b[1], a[2]+b[2])
def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def mul(a, s): return (a[0]*s, a[1]*s, a[2]*s)
def dot(a, b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def norm(a): return math.sqrt(dot(a, a))
def unit(a):
    n = norm(a)
    return mul(a, 1.0/n)


def pose(rear, right, muzzle, bore, root_pos, root_up, scale=1.0):
    """{'camera','forward','right','up','front_post','target','distance'} or None when degenerate."""
    if not (norm(bore) >= 1e-9 and 0 < scale < math.inf):
        return None
    bore = unit(bore)
    target = add(add(muzzle, mul(bore, ZERO_RANGE)), (0.0, 0.0, -ZERO_DROP))
    if not norm(sub(target, rear)) >= 1e-6:
        return None
    n = unit(sub(target, rear))
    along = dot(n, bore)
    if along < 0.9:
        return None
    front = add(rear, mul(n, FRONT_POST_ALONG*scale/along))
    height = dot(sub(rear, root_pos), root_up)
    rise = dot(n, root_up)
    d = TAIL_DISTANCE*scale
    if rise > 1e-9:
        d = min(d, (height - MIN_CAMERA_HEIGHT*scale)/rise)
    d = max(d, MIN_CAMERA_DISTANCE*scale)
    camera = sub(rear, mul(n, d))
    r = sub(right, mul(n, dot(right, n)))
    if norm(r) < 1e-6:
        return None
    r = unit(r)
    up = cross(r, n)
    return {'camera': camera, 'forward': n, 'right': r, 'up': up, 'front_post': front, 'target': target, 'distance': d}
