"""Own cantilever platforms in local Skyrim units; vanilla origins are immutable."""
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]
FLOOR=-.354012

def box(name,lo,hi,kind='floor'):
    return {'name':name,'lo':list(lo),'hi':list(hi),'kind':kind}

def site(name):
    assert name in ('este','oeste')
    origin=([17801.74,-8324.61,-3615.66] if name=='este' else [15225.56,-8306.52,-4127.66])
    east=name=='este';deck=FLOOR+(72 if east else 0);rear=-240 if east else -180;front=-710 if east else -630
    gun=[0.,-500. if east else -420.,deck]
    floors=[box('Deck',[-260,front,deck-12],[260,rear,deck])]
    if east:
        floors += [box('Toe',[128,-78,FLOOR-12],[145,-22,FLOOR])]
        for i,top in enumerate((20,40,60)):
            floors.append(box('OutwardStep'+str(i),[145+10*i,-78,FLOOR-12],[155+10*i if i<2 else 181,-22,FLOOR+top],'step'))
        floors += [box('SouthStep',[146,-102,FLOOR+60],[202,-78,deck],'step'),
                   box('Landing',[146,-150,deck-12],[202,-102,deck]),
                   box('Dogleg',[68,-178,deck-12],[174,-122,deck]),
                   box('Bridge',[68,-240,deck-12],[124,-150,deck])]
        nodes=[[110,-50,FLOOR],[122,-50,FLOOR],[145,-50,FLOOR+20],[150,-50,FLOOR+20],
               [155,-50,FLOOR+40],[160,-50,FLOOR+40],[165,-50,FLOOR+60],[170,-50,FLOOR+60],
               [174,-78,FLOOR+60],[174,-78,deck],[174,-150,deck],[96,-150,deck],
               [96,-240,deck],[96,-280,deck],[210,-300,deck],[124,-356,deck]]
    else:
        floors += [box('Bridge',[-36,-180,FLOOR-12],[36,-126,FLOOR])]
        nodes=[[0,-100,FLOOR],[0,-126,FLOOR],[0,-218,FLOOR],[210,-218,FLOOR],
               [210,-250,FLOOR],[124,-276,FLOOR]]
    # Low rails preserve the complete depressed shot sector. Rear entry is open.
    rails=[box('WestRail',[-260,front,deck],[ -248,rear,deck+48],'rail'),
           box('EastRail',[248,front,deck],[260,rear,deck+48],'rail'),
           box('FrontRail',[-260,front,deck],[260,front+12,deck+48],'rail')]
    if east:
        rails += [box('RearLeft',[-260,rear-12,deck],[62,rear,deck+48],'rail'),
                  box('RearRight',[130,rear-12,deck],[260,rear,deck+48],'rail')]
    else:
        rails += [box('RearLeft',[-260,rear-12,deck],[-42,rear,deck+48],'rail'),
                  box('RearRight',[42,rear-12,deck],[260,rear,deck+48],'rail')]
    support=json.loads((ROOT/'reports/v15_platform_support_refs.json').read_text())
    support=next(s for s in support if s['name']==name)
    braces=[]
    for x in (-96,96):
        hit=next(h for h in support['hits'] if h['x']==x)
        a=hit['point'].copy();a[1]-=4
        braces.append({'a':a,'b':[x,front+50,deck-26],'radius':13,'wall_ref':support['ref']})
    return {'name':name,'origin':origin,'floor_local_z':FLOOR,'deck_local_z':deck,
            'floor_boxes':floors,'rail_boxes':rails,'collision_boxes':floors+rails,
            'gun_local_pos':gun,'gun_world_pos':[a+b for a,b in zip(gun,origin)],
            'operator_local_foot':[124,gun[1]+144,deck],
            'standby_local_foot':[-210,rear-40 if east else rear-40,deck],
            'scale':1.,'yaw_deg':0.,'yaw_range':[-60,60],'pitch_range':[-20,80],
            'step_rises':[20,20,20,12] if east else [],'route_nodes':nodes,
            'braces':braces,'original_reference_overrides':[], 'engine_verified':False}

def floor_z(s,x,y):
    hits=[b['hi'][2] for b in s['floor_boxes'] if b['lo'][0]-.001<=x<=b['hi'][0]+.001 and b['lo'][1]-.001<=y<=b['hi'][1]+.001]
    return max(hits) if hits else None

def route_samples(s,spacing=4):
    out=[]
    for a,b in zip(s['route_nodes'][:-1],s['route_nodes'][1:]):
        n=max(1,math.ceil(math.dist(a,b)/spacing))
        out.extend([[p+(q-p)*i/n for p,q in zip(a,b)] for i in range(n+1)])
    return out

def build(name,cfg):
    from tower_v12_geometry import Tower
    s=site(name);t=Tower(cfg);deck=s['deck_local_z'];floors=s['floor_boxes']
    for b in floors:
        lo,hi=b['lo'],b['hi'];nx=math.ceil((hi[0]-lo[0])/26);w=(hi[0]-lo[0])/nx
        for i in range(nx):
            t.plank(b['name']+'Board'+str(i),[lo[0]+w*(i+.5),(lo[1]+hi[1])/2,hi[2]-4],
                    (0,1,0),(0,0,1),hi[1]-lo[1],w,8,fixed_width=True,twist=0)
        if b['kind']=='step':
            # Solid timber riser faces make the short staircase read as a
            # supported construction rather than suspended horizontal boards.
            t.plank(b['name']+'Riser',[(lo[0]+hi[0])/2,lo[1]+4,(lo[2]+hi[2])/2],
                    (0,0,1),(0,-1,0),hi[2]-lo[2],hi[0]-lo[0],8,fixed_width=True,twist=0)
    front=floors[0]['lo'][1];rear=floors[0]['hi'][1]
    # Main joists are carried by two long beams and wall-to-front diagonals.
    for x in (-96,96):
        t.log('MainBeam'+str(x),(x,rear+20,deck-26),(x,front+8,deck-26),14,bend=(0,0))
    for y in range(int(front+25),int(rear),92):
        t.log('CrossBeam'+str(y),(-258,y,deck-19),(258,y,deck-19),11,bend=(0,0))
    for i,b in enumerate(s['braces']):
        t.log('DiagonalBrace'+str(i),b['a'],b['b'],13,bend=(0,0))
        x,y,z=b['a'];t.log('WallLedger'+str(i),(x,y,z-40),(x,y,z+45),16,bend=(0,0))
    # Visual rails fit entirely inside their exported Havok envelope.
    for b in s['rail_boxes']:
        lo,hi=b['lo'],b['hi'];along_y=(hi[1]-lo[1])>(hi[0]-lo[0]);axis=(0,1,0) if along_y else (1,0,0)
        start=[(lo[0]+hi[0])/2,(lo[1]+hi[1])/2,deck+42];end=start.copy()
        ax=1 if along_y else 0;start[ax]=lo[ax]+6;end[ax]=hi[ax]-6
        t.log(b['name']+'Top',start,end,5,bend=(0,0))
        length=math.dist(start,end);n=max(1,math.ceil(length/120))
        for i in range(n+1):
            p=[start[j]+(end[j]-start[j])*i/n for j in range(3)]
            t.log(b['name']+'Post'+str(i),(p[0],p[1],deck-6),(p[0],p[1],deck+43),5,bend=(0,0))
    # Supporting beams below the narrow access slabs (never above foot surface).
    for b in floors[1:]:
        lo,hi=b['lo'],b['hi'];z=min(lo[2]+3,hi[2]-14)
        t.log(b['name']+'Under',((lo[0]+hi[0])/2,lo[1],z),((lo[0]+hi[0])/2,hi[1],z),6,bend=(0,0))
    return s,t.parts
