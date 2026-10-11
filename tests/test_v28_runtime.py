"""Regressions for the observed v27 missing grip and endless retry loop."""
import unittest,re,hashlib,json
from pathlib import Path
from tests import test_v27_guard_resilience as V27
ROOT=Path(__file__).resolve().parents[1]
class Guard28(unittest.TestCase):
 def test_retry_reaches_begin_after_one_scheduled_delay(self):
  source=(ROOT/'mod/scripts/source/AstraAsedioGuard.psc').read_text()
  pump=source.split('Function PumpV23()',1)[1]
  branch=re.search(r'if (v27Faults > 0[^\n]*)\n(.*?)FinishPumpV23\(expected, backoff\)',pump,re.S)
  self.assertIsNotNone(branch)
  condition,body=branch.groups()
  state={'v27Faults':1,'v28RetryWaited':False}
  expression=condition.strip().replace('&&',' and ').replace('!','not ')
  waits=0
  for update in range(2):
   if eval(expression,{'__builtins__':{}},state):
    waits+=1
    for name,value in re.findall(r'(v28RetryWaited) = (true|false)',body):state[name]=value=='true'
  self.assertEqual(waits,1,'v27 loops forever in the same backoff instead of reaching BeginOperation')
 def test_main_pump_applies_pose_before_any_aim_or_fire_decision(self):
  cpp=(ROOT/'native/src/GuardRuntime.cpp').read_text()
  tick=cpp.split('void GuardRuntime::tick(float dt)',1)[1]
  self.assertIn('settleGrip(s,gun.get(),actor.get(),obs)',tick)
  self.assertLess(tick.index('settleGrip('),tick.index('s.cycle.startFire('))
  self.assertLess(tick.index('settleGrip('),tick.index('guardGripFresh('))
 def test_snapshot_measured_hold_without_grip(self):
  info=json.loads((ROOT/'reports/diagnosis_v27_grip.json').read_text())
  data=(ROOT/'build/guard-v28/observed_v27_AstraSight.log').read_bytes()
  self.assertEqual(hashlib.sha256(data).hexdigest(),info['log_sha256'])
  self.assertGreater(info['hold_confirmed'],0);self.assertEqual(info['grip_confirmed'],0)
  self.assertFalse(info['character_hook_execution_thread_measured'])
class Resilience28(V27.GuardResilience27):
 def test_faulted_acquisitions_back_off_instead_of_rebeginning_every_second(self):
  pump=(ROOT/'mod/scripts/source/AstraAsedioGuard.psc').read_text().split('Function PumpV23()',1)[1]
  accepted=pump.split('bool accepted = AstraGuardNative.BeginOperation(',1)[1].split('endif',1)[0]
  self.assertNotIn('v27Faults = 0',accepted)
  healthy=pump.split('if status == 1 || status == 2 || status == 3',1)[1].split('endif',1)[0]
  self.assertIn('v27Faults = 0',healthy)
  self.assertIn('v28RetryWaited = false',healthy)
  self.assertIn('v27Faults += 1',pump)
  self.assertIn('if v27Faults > 3',pump)
 def test_version_bump_is_consistent_across_sources_and_checkers(self):
  plugin=(ROOT/'native/src/Plugin.cpp').read_text()
  for value in ('v.PluginVersion({3,5,9,0})','info->version=0x03050090','AstraSight 3.5.9 API 4'):self.assertIn(value,plugin)
  self.assertIn('project(AstraSight VERSION 3.5.9',(ROOT/'native/CMakeLists.txt').read_text())
  self.assertIn('0x03050090',(ROOT/'native/verify_binary.py').read_text())
  self.assertIn('50659472',(ROOT/'scripts/build_native.py').read_text())
if __name__=='__main__':unittest.main()
