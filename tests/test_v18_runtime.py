"""Regressions from the retained v17 engine trace; not an engine simulation."""
from pathlib import Path
import re
import pytest
from test_v16_placement_recovery import mounted

ROOT=Path(__file__).resolve().parents[1]

def test_measured_engine_speed_is_normalized_before_initial_velocity():
    log=(ROOT/'reports/runtime_evidence_v18/AstraSight.log').read_text()
    assert 'calculated_speed=756.000 power=0.350 speed_mult=1.000' in log
    cpp=(ROOT/'native/src/FastShotRuntime.cpp').read_text()
    assert 'speedMultiplierCorrection(' in cpp
    assert cpp.index('rt.speedMult=',cpp.index('RE::Projectile::Launch(&handle,data)')) < cpp.index('rt.linearVelocity=',cpp.index('RE::Projectile::Launch(&handle,data)'))

@pytest.mark.parametrize('site',['este','oeste'])
def test_static_city_handoff_never_moves_or_reloads_the_gun(site):
    f=mounted(site)
    # Both are equivalent/near positions that the old migration wanted to
    # "repair", invalidating the lease through the real ref lifecycle.
    f.root_pos=[0.,f.gun_y,f.deck+.8];f.root_angle=[0.,0.,360.]
    def reload_on_move(*args):
        f.run('OnUnload')
        pytest.fail('Moving the gun cancels the player lease and reloads its 3D')
    f.MoveTo=reload_on_move;f.SetAngle=reload_on_move
    lease=f.run('ReservePlayerLease')
    assert f.run('PreparePlayerLease',lease)
    assert f.vm.state['playerReady'] and f.guard.pos==f.wait.pos
    assert f.placement_moves==[]

def test_recovery_also_preserves_static_city_refs():
    f=mounted('oeste');f.MoveTo=lambda *a:pytest.fail('Recovery moved a static gun')
    f.SetAngle=lambda *a:pytest.fail('Recovery rotated a static gun')
    f.load();assert f.vm.state['running'] and f.guard.pinned
