"""Derive the current gate without editing historical verification scripts."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'scripts/verify_v18_release.py').read_text()
source=source.replace('v18','v19').replace('V18','V19').replace('Parent v17 was modified','Parent v18 was modified')
source=source.replace("'test_v19_runtime']","'test_v18_runtime','test_v19_handoff','test_v19_pex_privacy']")
source=source.replace('2368','2376').replace("'revision':18","'revision':19")
source=source.replace("ROOT/'scripts/compile_papyrus.py']","ROOT/'scripts/compile_papyrus.py',ROOT/'scripts/pex_metadata.py']")
(ROOT/'scripts/verify_v19_release.py').write_text(source)
if __name__=='__main__':print('Current v19 gate created')
