"""Guard the actual native callback wiring against the observed v15 regression."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]


def body(source,signature):
    start=source.index(signature);opening=source.index('{',start);depth=1;end=opening+1
    while depth:
        depth += (source[end]=='{')-(source[end]=='}');end+=1
    return source[opening+1:end-1]


def test_fast_shot_dispatch_uses_frame_callback_seen_in_runtime_log():
    log=(ROOT/'reports/runtime_evidence_2026-10-09/AstraSight.log').read_text()
    beats=re.findall(r'frames=(\d+).*?post\(writes/skips\)=(\d+)/(\d+)',log)
    assert beats and max(int(x[0]) for x in beats)>20
    assert all(x[1:]==('0','0') for x in beats)
    source=(ROOT/'native/src/Plugin.cpp').read_text()
    observed=body(source,'void update(RE::FirstPersonState*')
    assert 'fastShots.tick();' in observed, 'Native firing has no pump in the observed frame callback'
    # Dispatch must occur after apply/publish has returned, never from inside
    # Session::update's locked callback (inventory/animation call into engine).
    assert observed.index('fastShots.tick();') > observed.index('},true,reinterpret_cast<uintptr_t>(root));')
    assert 'fastShots.tick();' not in body(source,'void cameraUpdate(')
    assert source.count('fastShots.tick();')==1
