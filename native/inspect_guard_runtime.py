"""Read-only evidence for AE1170 actor/clip hooks; never loads the executable."""
from pathlib import Path
import argparse,struct,sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--vendor-dir',type=Path,required=True);args=p.parse_args()
sys.dont_write_bytecode=True
sys.path.insert(0,str(args.vendor_dir/'python'))
import pefile
DB=Path(r'G:\Modding\MO2\SkyrimSE\mods\Address Library All in One\SKSE\Plugins\versionlib-1-6-1170-0.bin')
EXE=Path(r'G:\Modding\Skyrim_Runtime_1.6.1170\SkyrimSE.exe')
b=DB.read_bytes();pos=0
def read(fmt):
 global pos
 value=struct.unpack_from('<'+fmt,b,pos);pos+=struct.calcsize(fmt);return value[0] if len(value)==1 else value
fmt=read('i');version=read('4i');n=read('i');pos+=n;ptr=read('i');count=read('i');lastid=lastoff=0;mapping={}
def decode(k,previous):
 if k==0:return read('Q')
 if k==1:return previous+1
 if k==2:return previous+read('B')
 if k==3:return previous-read('B')
 if k==4:return previous+read('H')
 if k==5:return previous-read('H')
 if k==6:return read('H')
 if k==7:return read('I')
 raise ValueError(k)
for _ in range(count):
 t=read('B');lo=t&15;hi=t>>4;lastid=decode(lo,lastid);lastoff=decode(hi&7,lastoff//ptr if hi&8 else lastoff)*(ptr if hi&8 else 1);mapping[lastid]=lastoff
pe=pefile.PE(str(EXE));base=pe.OPTIONAL_HEADER.ImageBase
assert version==(1,6,1170,0)
hooks=[]
for name,id,slot in [('PlayerCharacter::Update',208040,0xAD),('Character::Update',207886,0xAD),('hkbClipGenerator::Generate',226785,0x17)]:
 vt=mapping[id];address=struct.unpack('<Q',pe.get_data(vt+8*slot,8))[0];rva=address-base
 section=next((s for s in pe.sections if s.VirtualAddress<=rva<s.VirtualAddress+s.Misc_VirtualSize),None)
 assert section and section.Characteristics&0x20000000,f'{name} does not point to executable code'
 hooks.append({'name':name,'ae_vtable_id':id,'slot':slot,'vtable_rva':vt,'function_rva':rva,'executable_section':section.Name.rstrip(b'\0').decode()})
result={'runtime':'1.6.1170.0','executable_sha256':hashlib.sha256(EXE.read_bytes()).hexdigest(),'address_library_sha256':hashlib.sha256(b).hexdigest(),'inspection':'PE and Address Library only; binaries never loaded or modified','hooks':hooks,'camera_hook_dependency':False,'wrapped_text_decode_verified':False,'in_game_order_verified':False,'scope':'Confirms only Address Library vtable/slot pointers into an executable PE section. Steam-wrapped on-disk .text was not decoded; this does not prove function implementation, pump cadence, animation execution or post-IK render ordering.'}
out=ROOT/'reports/native_guard_hook_evidence.json';out.write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='hooks'},indent=2));print([(h['name'],hex(h['function_rva'])) for h in hooks])
