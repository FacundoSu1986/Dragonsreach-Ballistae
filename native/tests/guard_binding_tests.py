"""Read the actual addon record bindings, not a duplicate fixture."""
from pathlib import Path
import re,struct,zlib,sys
ROOT=Path(__file__).resolve().parents[2]
city=ROOT/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp'
core=ROOT/'mod/AstraAsedio.esp'
def records(path):
 data=path.read_bytes();result={};masters=[]
 def walk(start,end):
  pos=start
  while pos<end:
   tag=data[pos:pos+4];size=struct.unpack_from('<I',data,pos+4)[0]
   if tag==b'GRUP':walk(pos+24,pos+size);pos+=size;continue
   flags,form=struct.unpack_from('<II',data,pos+8);body=data[pos+24:pos+24+size]
   if flags&0x40000:body=zlib.decompress(body[4:])
   sub={};offset=0;extended=None
   while offset<len(body):
    kind=body[offset:offset+4];n=struct.unpack_from('<H',body,offset+4)[0];offset+=6
    if kind==b'XXXX':extended=struct.unpack_from('<I',body,offset)[0];offset+=n;continue
    n=extended if extended is not None else n;extended=None;value=body[offset:offset+n];offset+=n;sub.setdefault(kind,[]).append(value)
   if tag==b'TES4':masters.extend(v.rstrip(b'\0').decode() for v in sub.get(b'MAST',[]))
   else:result[form&0xFFFFFF]=(tag,sub)
   pos+=24+size
 walk(0,len(data));return masters,result
declared=re.search(r'GuardStationPlugin="([^"]+)"',(ROOT/'native/include/Astra/GuardPolicy.h').read_text()).group(1)
assert declared==city.name,f'native binding {declared} does not identify actual addon {city.name}'
masters,forms=records(city);coreMasters,coreForms=records(core)
assert coreForms[0xB04][0]==b'ACTI','low base must be an activator in the real core plugin'
for gun,actor in [(0xB70,0xB71),(0xB80,0xB81)]:
 assert forms[gun][0]==b'REFR' and forms[actor][0]==b'ACHR'
 raw=struct.unpack('<I',forms[gun][1][b'NAME'][0])[0]
 owner=masters[raw>>24] if raw>>24<len(masters) else city.name
 assert owner==core.name and raw&0xFFFFFF==0xB04,f'{gun:X} does not bind low core ACTI B04'
runtime=(ROOT/'native/src/GuardRuntime.cpp').read_text()
assert 'const RE::hkbGeneratorOutput**' in runtime and 'RE::hkbGeneratorOutput&' in runtime and 'float offset' in runtime,'Generate hook must preserve OAR real five-argument ABI'
assert 'GuardStationPlugin' in runtime,'runtime must use the binding checked against the actual addon'
sys.dont_write_bytecode=True;sys.path.insert(0,str(ROOT/'scripts/vendor'))
import nif_nodos
nodes=nif_nodos.leer(str(ROOT/'mod/meshes/AstraAsedio/ballesta_guardia.nif'))['nodos']
for name in ['CTRL_GIRO_360','CTRL_ELEVACION']:
 node=next(n for n in nodes.values() if n['nombre']==name)
 assert all(abs(x-y)<1e-6 for x,y in zip(node['rot'],[1,0,0,0,1,0,0,0,1])),f'{name} must have identity authored neutral rotation'
assert 's.yawBase=Mat{};s.pitchBase=Mat{};' in runtime,'readquisition must not retain live aim as next neutral base'
print('Actual city/core binding, authored neutral NIF and real Generate ABI contract: PASS')
