"""v27 contracts: measured-clause correction, diagnosability, bounded churn.

Basis (measured, this machine, 2026-10-11 17:12-17:14, AstraSight 3.5.7):
93 acquisitions followed by 93 cancellations with
clause=running package has no owned idle override; assignedPackage=B90,
runningPackage=FF000F64/FF000F65 (PlayIdle run-once wrapper) and
idle=00000000 in every cycle. The v26 predicate (running || ownIdle) is
unsatisfiable on this engine route, so v27 removes that gate for acquired
leases; the OAR clip-observation hook remains the arbitrator of owned-idle
identity and still cancels (bounded) when no canonical replacement shows.
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PSC = (ROOT / 'mod/scripts/source/AstraAsedioGuard.psc').read_text()
CPP = (ROOT / 'native/src/GuardRuntime.cpp').read_text()
POLICY = (ROOT / 'native/src/GuardPolicy.cpp').read_text()
V26T = (ROOT / 'native/tests/v26_guard_tests.cpp').read_text()


class GuardResilience27(unittest.TestCase):
    def test_missing_station_refs_trace_once_per_load(self):
        self.assertIn('bool v27WarnedRefs = false', PSC)
        self.assertIn('if actorRef == None && !v27WarnedRefs', PSC)
        self.assertIn('Astra guard v27: operator refs missing; enable AstraAsedio_WhiterunTorres.esp', PSC)
        self.assertIn('v27WarnedRefs = true', PSC)

    def test_faulted_acquisitions_back_off_instead_of_rebeginning_every_second(self):
        pump = PSC.split('Function PumpV23()', 1)[1]
        drain = pump.split('elseif status == -2', 1)[1]
        self.assertIn('v27Faults += 1', drain)
        self.assertIn("v27Faults = 0", pump.split('if status == -1', 1)[1].split('elseif', 1)[0])
        accept = pump.split('bool accepted = AstraGuardNative.BeginOperation(', 1)[1]
        self.assertIn('v27Faults = 0', accept.split('endif', 1)[0])
        self.assertLess(pump.index('Astra guard v27: backoff '), pump.index('AstraGuardNative.BeginOperation('))
        self.assertIn('FinishPumpV23(expected, backoff)', pump)
        self.assertIn('if v27Faults > 3', pump)

    def test_acquired_lease_tolerates_the_measured_runonce_wrapper(self):
        # The measured-unsatisfiable predicate is gone; acquisition requires
        # assigned B90 + sheathed, and running==B90 is still required BEFORE
        # any acquisition (acquired=false branch unchanged).
        self.assertIn('assigned&&sheathed&&(running||acquired)', POLICY)
        self.assertNotIn('running package has no owned idle override', CPP)
        self.assertIn('assigned package / weapon-state contract broken', CPP)
        # Diagnostics keep printing running/runOnce/idle fields for the clause.
        self.assertIn('currentProcessIdle', CPP)
        # v29 retired the two closed paths this test used to pin (cancel when OAR
        # samples stop; grip confirmation gating Fire/Launch). They never passed
        # in game. Their replacements are pinned by tests/test_v29_guard_simple.py.

    def test_v26_policy_table_matches_measured_semantics(self):
        self.assertIn('check(guardOperatorPackage(true,false,false,true,true)', V26T)
        self.assertIn('check(!guardOperatorPackage(true,false,true,false,true)', V26T)
        self.assertIn("currentProcessIdle stays null", V26T)

    def test_install_log_distinguishes_missing_oar_module_from_rejected_api(self):
        self.assertIn('OAR Animations V1={} (module loaded={})', CPP)

    def test_v26_fail_closed_strings_survive(self):
        # 'hold replacement not observable' left with v29: missing samples re-request, never cancel.
        for kept in ('guard v26 context', 'guard v26 reject',
                     'operator personal weapon not fully sheathed', 'owned operator package missing'):
            self.assertIn(kept, CPP, kept)

    @unittest.skip('AstraSight 3.5.8 superseded; current version pinned by test_v29_guard_simple.test_version_is_360_everywhere')
    def test_version_bump_is_consistent_across_sources_and_checkers(self):
        plugin = (ROOT / 'native/src/Plugin.cpp').read_text()
        self.assertIn('v.PluginVersion({3,5,8,0})', plugin)
        self.assertIn('info->version=0x03050080', plugin)
        self.assertIn('AstraSight 3.5.8 API 4', plugin)
        self.assertIn('project(AstraSight VERSION 3.5.8', (ROOT / 'native/CMakeLists.txt').read_text())
        self.assertIn('0x03050080', (ROOT / 'native/verify_binary.py').read_text())
        self.assertIn("50659456", (ROOT / 'scripts/build_native.py').read_text())


if __name__ == '__main__':
    unittest.main()
