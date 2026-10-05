"""Source safety contract plus compile report, not an in-game execution claim."""
import json,re,unittest,sys
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))

class InputContractEvaluator(__import__('tests.test_control_lease', fromlist=['SessionSourceEvaluator']).SessionSourceEvaluator):
 """Execute actual PSC branches with explicit native fixtures, never a game VM."""
 def __init__(self,source):
  super().__init__(source)
  self.source=source;self.now=10.;self.menu=False
  self.state.update({'Utility':SimpleNamespace(GetCurrentRealTime=lambda:self.now,IsInMenuMode=lambda:self.menu),'Session':None,'Self':None,'player':SimpleNamespace(GetItemCount=lambda ammo:10),'SteelBolt':None,'QALog':False})
  self.native.update({'CanOperate':lambda generation:self.state['operating'] and generation==self.state['generation'],'Is3DLoaded':lambda:False,'UnregisterForUpdate':lambda:None,'UnregisterForAllKeys':lambda:None,'UnregisterForAllControls':lambda:None,'UnregisterForAllMenus':lambda:None,'ApplyAim':lambda:None})

def evaluate_operator_gate(source,actor,operator,matrix=(1.,0.,0.,0.,1.,0.,0.,0.,1.),scale=1.):
 """Evaluate the PSC's actual coordinate arithmetic; no duplicate range formula.
 This covers geometry only, not SKSE/Papyrus event dispatch or execution.
 """
 body=source.split('bool Function NearOperator()')[1].split('EndFunction')[0]
 scope={'actor':actor,'operator':operator,'rootWorldMatrix':matrix,'rootScale':scale,'OperatorHeight':119.,'OperatorDistance':160.,'OperatorVerticalTolerance':64.,'abs':abs}
 def expression(s):
  for axis,i in [('X',0),('Y',1),('Z',2)]:
   s=s.replace(f'player.GetPosition{axis}()',f'actor[{i}]').replace(f'NetImmerse.GetNodeWorldPosition{axis}(Self, OperatorNode, false)',f'operator[{i}]')
  return s.replace('Math.Abs','abs').replace('&&',' and ')
 for name,expr in re.findall(r'^\s*float (height|dx|dy|dz) = (.+)$',body,re.M):scope[name]=eval(expression(expr),{'__builtins__':{}},scope)
 expr=re.findall(r'^\s*return (.+)$',body,re.M)[-1]
 return eval(expression(expr),{'__builtins__':{}},scope)
class SessionContract(unittest.TestCase):
 def setUp(self):
  p=ROOT/'mod/scripts/source/AstraAsedioActi.psc'
  self.assertTrue(p.exists(),'missing controller PSC');self.s=p.read_text()
 def test_single_native_launch_and_precommit_checks(self):
  self.assertEqual(self.s.count('Launcher.Fire(Self, ShotAmmo)'),1)
  body=self.s.split('Function CommitShot')[1].split('EndFunction')[0]
  self.assertLess(body.index('CanOperate'),body.index('RemoveItem'))
  self.assertLess(body.index('GetItemCount'),body.index('RemoveItem'))
  self.assertLess(body.index('shotCommitted = true'),body.index('RemoveItem'))
  self.assertLess(body.index('RemoveItem'),body.index('Launcher.Fire'))
 def test_controls_capture_and_only_owned_controls_restored(self):
  self.s=(ROOT/'mod/scripts/source/AstraAsedioSession.psc').read_text()
  self.assertIn('Game.IsMovementControlsEnabled()',self.s);self.assertIn('Game.IsFightingControlsEnabled()',self.s)
  self.assertRegex(self.s,r'DisablePlayerControls\(acquiredMovement, acquiredFighting, acquiredCamSwitch, false, false, false, false, false\)')
  self.assertRegex(self.s,r'EnablePlayerControls\(restoreMovement, restoreFighting, restoreCamSwitch, false, false, false, false, false\)')
 def test_cleanup_on_load_death_and_unload(self):
  alias=(ROOT/'mod/scripts/source/AstraAsedioPlayerAlias.psc').read_text()
  self.assertIn('Event OnPlayerLoadGame()',alias);self.assertIn('Event OnDeath',alias)
  self.assertIn('EmergencyCleanup',alias)
  self.assertIn('Event OnUnload()',self.s);self.assertIn('generation += 1',self.s)
  self.assertNotIn('Utility.Wait(',self.s);self.assertNotIn('RegisterForUpdate(',self.s)
  self.assertIn('RegisterForSingleUpdate',self.s)
 def test_reloading_3d_invalidates_saved_active_session_before_restoring_aim(self):
  onload=self.s.split('Event OnLoad()')[1].split('EndEvent')[0]
  self.assertIn('EndSession()',onload)
  self.assertLess(onload.index('EndSession()'),onload.index('CaptureMatrices()'))
 def test_cycle_clock_is_not_clamped_to_aim_safety_dt(self):
  self.assertIn('float dtCycle = dt',self.s)
  self.assertEqual(self.s.count('elapsed += dtCycle'),2)
  self.assertNotIn('elapsed += dt\n',self.s)
 def test_world_transform_verified_before_consuming_ammo(self):
  body=self.s.split('Function CommitShot')[1].split('EndFunction')[0]
  self.assertIn('ShotTransformReady()',body)
  self.assertLess(body.index('ShotTransformReady()'),body.index('RemoveItem'))
  self.assertIn('NetImmerse.GetNodeWorldRotationMatrix(Self, "ProjectileNode"',self.s)
  self.assertIn('directionDot < 0.999',self.s)
  self.assertIn('positionError > 4.0',self.s)
 def test_aim_thaws_after_release_and_cleanup_preserves_reload(self):
  self.assertIn('phase == 0 || shotCommitted',self.s)
  self.assertIn('bool needsReset',self.s)
  end=self.s.split('Function EndSession()')[1].split('EndFunction')[0]
  self.assertIn('needsReset = true',end)
  begin=self.s.split('Event OnActivate')[1].split('EndEvent')[0]
  self.assertIn('if needsReset',begin)
 def test_matrix_initialization_does_not_cast_none_to_an_array(self):
  # The installed v01 PEX reused a Float[] temp after casting None into it.
  # The real VM log then rejected all eight ArrayCreate instructions.
  arrays=re.findall(r'^float\[\]\s+(\w+)',self.s,re.M)
  for array in arrays:
   self.assertNotRegex(self.s,rf'\b{array}\s*==\s*None|\b{array}\s*=\s*None')
 def test_activation_rejections_have_a_visible_reason(self):
  body=self.s.split('Event OnActivate')[1].split('EndEvent')[0]
  self.assertIn('RejectActivation(',body)
  self.assertIn('Function RejectActivation(string reason)',self.s)
  reject=self.s.split('Function RejectActivation')[1].split('EndFunction')[0]
  self.assertIn('Debug.Notification(',reject);self.assertIn('Debug.Trace(',reject)
  self.assertIn('SKSE.GetVersion()',body)
  self.assertIn('Session.IsRunning()',body)
  self.assertIn('OperatorHeight',self.s)
 def test_operator_gate_accepts_roof_at_145_units_but_rejects_lower_floor(self):
  operator=(73.5,101.5,584.5)
  self.assertTrue(evaluate_operator_gate(self.s,(73.5,246.5,465.5),operator))
  self.assertTrue(evaluate_operator_gate(self.s,(73.5,101.5,462.7),operator))
  self.assertFalse(evaluate_operator_gate(self.s,(73.5,101.5,2.),operator))
  self.assertFalse(evaluate_operator_gate(self.s,(73.5,262.5,465.5),operator))
  self.assertFalse(evaluate_operator_gate(self.s,(73.5,101.5,530.5),operator))
 def test_operator_foot_projection_honors_root_rotation_and_scale(self):
  import math
  matrix=(1.,0.,0.,0.,math.cos(.5),math.sin(.5),0.,-math.sin(.5),math.cos(.5))
  scale=2.;foot=(73.5,101.5,465.5)
  operator=tuple(foot[i]+119.*scale*matrix[2+3*i] for i in range(3))
  self.assertTrue(evaluate_operator_gate(self.s,foot,operator,matrix,scale))
  self.assertIn('rootWorldMatrix[i] != rootWorldMatrix[i]',self.s)
  self.assertIn('rootScale != rootScale',self.s)
 def test_all_scripts_compiled_by_real_bethesda_compiler(self):
  report=json.loads((ROOT/'reports/plugin_compile.json').read_text())
  self.assertTrue(report['success'])
  self.assertGreaterEqual(len(report['scripts']),3)
  for r in report['scripts']:
   import hashlib
   self.assertEqual(r['source_sha256'],hashlib.sha256((ROOT/r['source']).read_bytes()).hexdigest())
   self.assertEqual(r['exit_code'],0);self.assertGreater((ROOT/r['pex']).stat().st_size,128)
   self.assertEqual(r['sha256'],hashlib.sha256((ROOT/r['pex']).read_bytes()).hexdigest())
   self.assertTrue(r['bytecode_safety']['no_none_to_array_casts'])
 def test_input_uses_skse_events_instead_of_the_directinput_poll_cache(self):
  self.assertNotIn('Input.IsKeyPressed(',self.s)
  for code in (203,205,200,208):self.assertIn(f'RegisterForKey({code})',self.s)
  for control in ('Activate','Right Attack/Block'):
   self.assertIn(f'RegisterForControl("{control}")',self.s)
   for device in (0,1):self.assertIn(f'Input.GetMappedKey("{control}", {device})',self.s)
  for event in ('OnKeyDown','OnKeyUp','OnControlDown','OnControlUp'):
   self.assertIn(f'Event {event}(',self.s)
  aim=self.s.split('Function UpdateAim(')[1].split('EndFunction')[0]
  for held in ('heldLeft','heldRight','heldUp','heldDown'):self.assertIn(f'if {held}',aim)
 def test_new_activation_and_control_cancel_without_waiting_for_update(self):
  activate=self.s.split('Event OnActivate(')[1].split('EndEvent')[0]
  active_branch=activate.split('if operating')[1].split('endif')[0]
  self.assertIn('RequestExit(',active_branch)
  self.assertNotIn('ALREADY_OPERATING',activate)
  control=self.s.split('Event OnControlDown(')[1].split('EndEvent')[0]
  self.assertIn('RequestExit(',control)
  exit_body=self.s.split('Function RequestExit(')[1].split('EndFunction')[0]
  self.assertIn('activateReadyAt',exit_body)
  self.assertIn('EndSession()',exit_body)
  self.assertNotIn('updating',exit_body)
  self.assertNotIn('menuWasOpen',exit_body)
 def test_menu_discards_held_and_pending_input_and_requires_a_release(self):
  pause=self.s.split('Function PauseInput()')[1].split('EndFunction')[0]
  self.assertIn('ClearHeldInput(true)',pause)
  self.assertIn('CancelPendingShot()',pause)
  clear=self.s.split('Function ClearHeldInput(')[1].split('EndFunction')[0]
  for held in ('heldLeft','heldRight','heldUp','heldDown'):self.assertIn(f'{held} = false',clear)
  for suffix in ('Left','Right','Up','Down'):self.assertIn(f'release{suffix} = release{suffix} || held{suffix}',clear)
  key=self.s.split('Function SetAimKey(')[1].split('EndFunction')[0]
  self.assertIn('InputReady()',key)
  for block in ('releaseLeft','releaseRight','releaseUp','releaseDown'):self.assertIn(f'{block} = false',key)
 def test_fire_latch_is_taken_before_validation_and_no_poll_can_launch(self):
  fire=self.s.split('Function RequestShot()')[1].split('EndFunction')[0]
  self.assertLess(fire.index('heldFire = true'),fire.index('BeginShot('))
  update=self.s.split('Event OnUpdate()')[1].split('EndEvent')[0]
  self.assertNotIn('BeginShot(',update)
  commit=self.s.split('Function CommitShot(')[1].split('EndFunction')[0]
  self.assertLess(commit.index('InputReady()'),commit.index('RemoveItem'))
 def test_cancellation_invalidates_pending_generation_and_unregisters_input(self):
  cancel=self.s.split('Function CancelPendingShot()')[1].split('EndFunction')[0]
  self.assertIn('generation += 1',cancel);self.assertIn('shotGeneration = -1',cancel)
  self.assertIn('!shotCommitted',cancel)
  end=self.s.split('Function EndSession()')[1].split('EndFunction')[0]
  for call in ('UnregisterForAllKeys()','UnregisterForAllControls()','UnregisterForAllMenus()'):
   self.assertIn(call,end)
  self.assertIn('ClearHeldInput(true)',end)
 def test_shot_failure_diagnostics_include_transform_and_animation_reasons(self):
  for reason in ('SHOT_MATRIX_READ_FAILED','SHOT_POSITION_READ_FAILED','SHOT_DIRECTION_MISMATCH','SHOT_POSITION_MISMATCH','FIRE_ANIMATION_FAILED'):
   self.assertIn(reason,self.s)
  reject=self.s.split('Function RejectShot(')[1].split('EndFunction')[0]
  self.assertIn('Debug.Trace(',reject);self.assertIn('Debug.Notification(',reject)
 def test_first_update_diagnostic_has_a_one_shot_guard(self):
  update=self.s.split('Event OnUpdate()')[1].split('EndEvent')[0]
  trace=update.split('if firstUpdatePending')[1].split('endif')[0]
  self.assertIn('firstUpdatePending = false',trace);self.assertIn('first OnUpdate',trace)

class BytecodeSafety(unittest.TestCase):
 def test_rejects_the_observed_none_cast_then_arraycreate_sequence(self):
  import compile_papyrus
  self.assertTrue(hasattr(compile_papyrus,'validate_assembly'),'no array bytecode safety validator')
  bad='.local ::temp27 Float[]\nCast ::temp27 None\nArrayCreate ::temp27 9'
  with self.assertRaisesRegex(ValueError,'None.*array'):
   compile_papyrus.validate_assembly(bad)
 def test_accepts_typed_array_allocation_and_object_none_checks(self):
  import compile_papyrus
  self.assertTrue(hasattr(compile_papyrus,'validate_assembly'),'no array bytecode safety validator')
  valid='.local ::temp27 Float[]\n.local ::temp28 ObjectReference\nArrayCreate ::temp27 9\nCast ::temp28 None'
  self.assertTrue(compile_papyrus.validate_assembly(valid)['no_none_to_array_casts'])
 def test_legacy_poll_only_controller_bytecode_is_rejected(self):
  import compile_papyrus
  legacy='\n'.join('.function '+event for event in ('OnKeyDown','OnKeyUp','OnControlDown','OnControlUp'))+'\nCallStatic input IsKeyPressed ::temp1 203'
  with self.assertRaisesRegex(ValueError,'poll-only'):compile_papyrus.validate_input_assembly(legacy)

class InputBehaviorContract(unittest.TestCase):
 def setUp(self):
  self.vm=InputContractEvaluator((ROOT/'mod/scripts/source/AstraAsedioActi.psc').read_text())
  self.vm.state.update(operating=True,inputPaused=False,menuWasOpen=False,heldFire=False,generation=7,activateReadyAt=10.35,UseMouseAim=False,UseSightCamera=False)
 def test_cancel_press_during_initial_debounce_does_not_exit_but_later_press_does(self):
  self.vm.run('RequestExit','test');self.assertTrue(self.vm.state['operating'])
  self.vm.now=10.36;self.vm.run('RequestExit','test')
  self.assertFalse(self.vm.state['operating']);self.assertEqual(self.vm.state['generation'],8)
 def test_held_arrow_is_stopped_by_menu_and_a_queued_down_cannot_rearm_it(self):
  self.vm.run('SetAimKey',203,True);self.assertTrue(self.vm.state['heldLeft'])
  self.vm.run('PauseInput');self.assertFalse(self.vm.state['heldLeft'])
  self.vm.state.update(inputPaused=False,menuWasOpen=False)
  self.vm.run('SetAimKey',203,True);self.assertFalse(self.vm.state['heldLeft'])
  self.vm.run('SetAimKey',203,False);self.vm.run('SetAimKey',203,True)
  self.assertTrue(self.vm.state['heldLeft'])
 def test_first_new_arrow_and_attack_press_after_session_entry_operate(self):
  self.vm.state['heldFire']=True
  self.vm.run('ClearHeldInput',False)
  self.vm.run('SetAimKey',200,True);self.assertTrue(self.vm.state['heldUp'])
  self.vm.run('RequestShot');self.assertEqual(self.vm.state['phase'],1)
  self.assertEqual(self.vm.state['shotGeneration'],7)
 def test_menu_does_not_require_a_dummy_release_for_a_key_that_was_not_held(self):
  self.vm.run('SetAimKey',203,True);self.vm.run('PauseInput')
  self.vm.state.update(inputPaused=False,menuWasOpen=False)
  self.vm.run('ClearHeldInput',True)
  self.vm.run('SetAimKey',200,True);self.assertTrue(self.vm.state['heldUp'])
  self.vm.run('RequestShot');self.assertEqual(self.vm.state['phase'],1)
 def test_fresh_input_after_menu_close_operates_before_the_next_update(self):
  self.vm.menu=True;self.vm.run('OnMenuOpen','InventoryMenu')
  self.vm.menu=False;self.vm.now=25.;self.vm.run('OnMenuClose','InventoryMenu')
  self.vm.run('SetAimKey',200,True);self.vm.run('RequestShot')
  self.assertEqual((self.vm.state['heldUp'],self.vm.state['phase']),(True,1))
  self.assertFalse(self.vm.state['inputPaused']);self.assertFalse(self.vm.state['menuWasOpen'])
  self.assertEqual(self.vm.state['lastTick'],25.)
 def test_closing_one_nested_menu_does_not_resume_input_while_another_is_open(self):
  self.vm.menu=True;self.vm.run('OnMenuOpen','InventoryMenu')
  self.vm.run('OnMenuClose','MessageBoxMenu')
  self.vm.run('SetAimKey',200,True);self.vm.run('RequestShot')
  self.assertTrue(self.vm.state['inputPaused']);self.assertFalse(self.vm.state['heldUp'])
  self.assertEqual(self.vm.state['phase'],0)
 def test_press_delivered_while_menu_is_open_requires_release_afterward(self):
  self.vm.run('PauseInput');self.vm.menu=True
  self.vm.run('SetAimKey',200,True);self.vm.run('RequestShot')
  self.vm.menu=False;self.vm.state.update(inputPaused=False,menuWasOpen=False)
  self.vm.run('SetAimKey',200,True);self.vm.run('RequestShot')
  self.assertFalse(self.vm.state['heldUp']);self.assertEqual(self.vm.state['phase'],0)
  self.vm.run('SetAimKey',200,False);self.vm.run('OnControlUp','Right Attack/Block',.2)
  self.vm.run('SetAimKey',200,True);self.vm.run('RequestShot')
  self.assertTrue(self.vm.state['heldUp']);self.assertEqual(self.vm.state['phase'],1)
 def test_key_and_control_fire_down_share_one_attempt_until_release(self):
  attempts=[];self.vm.native['BeginShot']=lambda generation:attempts.append(generation)
  self.vm.run('RequestShot');self.vm.run('RequestShot');self.assertEqual(attempts,[7])
  self.vm.run('OnControlUp','Right Attack/Block',.2)
  self.vm.run('RequestShot');self.assertEqual(attempts,[7,7])
 def test_pause_invalidates_precommit_shot_and_leaves_ammo_unconsumed(self):
  self.vm.menu=True
  self.vm.state.update(phase=2,shotCommitted=False,shotGeneration=7)
  self.vm.run('PauseInput')
  self.assertEqual(self.vm.state['generation'],8);self.assertEqual(self.vm.state['shotGeneration'],-1)
  self.assertFalse(self.vm.run('InputReady'));self.assertEqual(self.vm.state['phase'],3)
  self.assertFalse(self.vm.expr('CanOperate(7)',{}))
 def test_pause_preserves_already_consumed_shot_reload(self):
  self.vm.state.update(phase=2,shotCommitted=True,shotGeneration=7)
  self.vm.run('PauseInput')
  self.assertEqual(self.vm.state['generation'],7);self.assertTrue(self.vm.state['shotCommitted'])
 def test_reactivation_closes_and_the_same_input_pulse_cannot_reopen(self):
  actor=object();self.vm.state['Game']=SimpleNamespace(GetPlayer=lambda:actor)
  self.vm.now=10.36;self.vm.run('OnActivate',actor)
  self.assertFalse(self.vm.state['operating'])
  self.vm.run('OnActivate',actor);self.assertFalse(self.vm.state['operating'])
 def install_launch_fixtures(self):
  result={'ammo':10,'launches':0}
  def remove(ammo,count,silent):result['ammo']-=count
  def launch(ref,ammo):result['launches']+=1
  self.vm.state.update(player=SimpleNamespace(GetItemCount=lambda ammo:result['ammo'],RemoveItem=remove),Launcher=SimpleNamespace(Fire=launch),ShotAmmo=None,NetImmerse=SimpleNamespace(SetNodeScale=lambda *args:None),VisualBoltNode='VIROTE_VISUAL',phase=2,shotGeneration=7)
  self.vm.native['ShotTransformReady']=lambda:True
  return result
 def test_native_commit_consumes_exactly_once_even_if_requested_twice(self):
  result=self.install_launch_fixtures()
  self.vm.run('CommitShot',7);self.vm.run('CommitShot',7)
  self.assertEqual(result,{'ammo':9,'launches':1})
 def test_exit_during_transform_preflight_does_not_consume_or_launch(self):
  result=self.install_launch_fixtures()
  def cancel_then_return():
   self.vm.run('EndSession')
   return True
  self.vm.native['ShotTransformReady']=cancel_then_return
  self.vm.run('CommitShot',7)
  self.assertEqual(result,{'ammo':10,'launches':0})
  self.assertFalse(self.vm.state['operating'])
 def test_menu_cancellation_during_preflight_does_not_consume_or_launch(self):
  result=self.install_launch_fixtures()
  def pause_then_return():
   self.vm.menu=True;self.vm.run('PauseInput')
   return True
  self.vm.native['ShotTransformReady']=pause_then_return
  self.vm.run('CommitShot',7)
  self.assertEqual(result,{'ammo':10,'launches':0})
  self.assertEqual(self.vm.state['phase'],3)
 def test_exit_restores_controls_before_requesting_visual_reset(self):
  calls=[]
  self.vm.state.update(Session=SimpleNamespace(Release=lambda *args:calls.append('release')),NetImmerse=SimpleNamespace(SetNodeScale=lambda *args:calls.append('scale')),VisualBoltNode='VIROTE_VISUAL')
  self.vm.native.update(Is3DLoaded=lambda:True,PlayGamebryoAnimation=lambda *args:calls.append('reset'))
  self.vm.run('EndSession')
  self.assertEqual(calls,['release','reset','scale'])
 def test_cancelled_generation_cannot_launch_late_even_after_menu_resumes(self):
  result=self.install_launch_fixtures();self.vm.state.update(phase=2,shotCommitted=False,shotGeneration=7)
  self.vm.run('PauseInput');self.vm.state.update(inputPaused=False,menuWasOpen=False)
  self.vm.run('CommitShot',7)
  self.assertEqual(result,{'ammo':10,'launches':0});self.assertTrue(self.vm.state['operating'])
  self.assertEqual(self.vm.state['phase'],3)
if __name__=='__main__':unittest.main()
