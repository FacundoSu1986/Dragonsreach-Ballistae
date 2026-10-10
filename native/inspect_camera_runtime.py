"""Read-only vtable/consumer disassembly against the existing 1170 executable."""
from pathlib import Path
import struct,sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'build/native/python'))
import pefile,capstone
DB=Path(r'G:\Modding\MO2\SkyrimSE\mods\Address Library All in One\SKSE\Plugins\versionlib-1-6-1170-0.bin')
EXE=Path(r'G:\Modding\Skyrim_Runtime_1.6.1170\SkyrimSE.exe')
b=DB.read_bytes(); pos=0
def read(fmt):
 global pos
 v=struct.unpack_from('<'+fmt,b,pos);pos+=struct.calcsize(fmt);return v[0] if len(v)==1 else v
fmt=read('i');version=read('4i');n=read('i');pos+=n;ptr=read('i');count=read('i');lastid=lastoff=0;mapping={}
for _ in range(count):
 t=read('B');lo=t&15;hi=t>>4
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
 lastid=decode(lo,lastid);lastoff=decode(hi&7,lastoff//ptr if hi&8 else lastoff)*(ptr if hi&8 else 1);mapping[lastid]=lastoff
pe=pefile.PE(str(EXE));base=pe.OPTIONAL_HEADER.ImageBase;md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
lines=[f'Exe SHA256 {hashlib.sha256(EXE.read_bytes()).hexdigest()}',f'Address Library header {fmt} {version}']
for name,id,slots in [('FirstPersonState',214855,[3,4,5]),('PlayerCamera',214859,[2])]:
 vt=mapping[id]
 for slot in slots:
  addr=struct.unpack('<Q',pe.get_data(vt+8*slot,8))[0];rva=addr-base
  lines.append(f'\n{name} slot {slot} ID {id} vtableRVA 0x{vt:x} functionRVA 0x{rva:x}')
  for ins in md.disasm(pe.get_data(rva,2400),addr):
   lines.append(f'{ins.address-base:08x} {ins.mnemonic:8} {ins.op_str}')
   if ins.mnemonic=='ret':break
(ROOT/'reports/native_runtime_disassembly.txt').write_text('\n'.join(lines),encoding='utf-8')
print('\n'.join(lines))
