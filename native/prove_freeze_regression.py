"""Temporarily remove atomic-freeze behavior, prove test failure, restore source."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1];source=root/'native/src/Core.cpp';original=source.read_text(encoding='utf-8')
needle='if(freeze)frozen_=true;return snapshot_.aim;'
assert needle in original
try:
 source.write_text(original.replace(needle,'if(freeze)frozen_=false;return snapshot_.aim;'),encoding='utf-8')
 with (root/'reports/native_freeze_red.log').open('w',encoding='utf-8') as output:
  result=subprocess.run([sys.executable,str(root/'scripts/build_native.py'),'--core-only','--build-dir','build/native/core-verified','--no-receipt'],cwd=root,stdout=output,stderr=subprocess.STDOUT)
 assert result.returncode!=0, 'Regression failed to catch missing freeze'
 log=(root/'reports/native_freeze_red.log').read_text(encoding='utf-8',errors='replace')
 assert 'FAIL: prepared frame cannot overwrite frozen aim' in log
 print('RED verified: tests detect missing freeze before prepared frame apply')
finally:
 source.write_text(original,encoding='utf-8')
