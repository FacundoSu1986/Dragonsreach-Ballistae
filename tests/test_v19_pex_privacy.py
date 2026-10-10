"""Public PEX headers can be anonymized without modifying executable data."""
import struct
import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from pex_metadata import anonymize, metadata


def text(s):
    b=s.encode();return struct.pack('>H',len(b))+b


def sample():
    return bytes.fromhex('fa57c0de03020001')+struct.pack('>Q',123456)+text('Astra.psc')+text('private-author')+text('private-host')+b'\x00\x11executable-tables\x00\xff'


def test_anonymize_preserves_source_timestamp_and_all_executable_tables():
    original=sample();clean=anonymize(original)
    before,old_end=metadata(original);after,new_end=metadata(clean)
    assert before['user']=='private-author' and before['computer']=='private-host'
    assert after=={**before,'user':'AstraAsedio','computer':'Build'}
    assert clean[new_end:]==original[old_end:] and clean[:16]==original[:16]


@pytest.mark.parametrize('bad',[b'',b'bad magic',sample()[:20],sample()[:35]])
def test_truncated_or_other_format_is_rejected(bad):
    with pytest.raises(ValueError):anonymize(bad)
