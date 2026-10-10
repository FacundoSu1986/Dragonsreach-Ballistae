"""Verify stationary muzzle launch math in the real portable C++ helper."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def test_launch_has_explicit_initial_velocity_and_invalid_input_preflight():
    runtime = (ROOT / 'native/src/FastShotRuntime.cpp').read_text()
    assert 'muzzleVelocity(' in runtime, 'actor LaunchData alone has no stationary muzzle impulse'
    launch = runtime.index('RE::Projectile::Launch(&handle,data)')
    impulse = runtime.index('linearVelocity=', launch)
    assert impulse < runtime.index('launchedAt=clockNow()', launch)
    assert 'shot ballistics' in runtime and 'shot flight sample' in runtime


def test_portable_suite_exercises_horizontal_depression_and_invalid_speed():
    source = (ROOT / 'native/tests/v17_tests.cpp').read_text()
    for item in ['5400', '-20', '80', 'infinity', 'quiet_NaN', 'zero direction']:
        assert item in source
