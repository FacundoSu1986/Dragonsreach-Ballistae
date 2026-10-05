"""Read PE exports and SKSE metadata without loading/launching any binary."""
from pathlib import Path
import sys,struct,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'build/native/python'))
import pefile
DLL=ROOT/'mod/SKSE/Plugins/AstraSight.dll';pe=pefile.PE(str(DLL))
exports={s.name.decode():s.address for s in pe.DIRECTORY_ENTRY_EXPORT.symbols if s.name}
assert pe.FILE_HEADER.Machine==0x8664
assert set(exports)=={'SKSEPlugin_Load','SKSEPlugin_Query','SKSEPlugin_Version'}
data=pe.get_data(exports['SKSEPlugin_Version'],848)
u32=lambda offset:struct.unpack_from('<I',data,offset)[0]
name=data[8:264].split(b'\0')[0].decode();compat=[u32(780+4*i) for i in range(16)]
runtime=(1<<24)|(6<<16)|(1170<<4)
assert name=='AstraSight' and u32(4)==0x03030000
assert data[776]&1 and data[776]&4
assert compat[0]==runtime and not any(compat[1:])
assert u32(844)==(2<<24)|(2<<16)|(8<<4)
report={'dll':str(DLL.relative_to(ROOT)),'sha256':hashlib.sha256(DLL.read_bytes()).hexdigest(),'size':DLL.stat().st_size,'machine':'AMD64 (0x8664)','exports':exports,'metadata':{'version_data':u32(0),'plugin_name':name,'packed_plugin_version':u32(4),'address_library':bool(data[776]&1),'structs_post_629':bool(data[776]&4),'compatible_packed_versions':compat,'minimum_skse_packed':u32(844)},'imports':[entry.dll.decode() for entry in pe.DIRECTORY_ENTRY_IMPORT],'verified_by':'PE parse only; DLL not loaded and game not launched'}
(ROOT/'reports/native_binary_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
