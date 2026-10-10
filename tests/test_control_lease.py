"""Execute actual session PSC branches with deterministic native-boundary fixtures.

This scalar source evaluator is deliberately not a Papyrus VM. It checks the
session's code under specified reentrant native calls; it does not establish
engine scheduling, event delivery, persistence, or an in-game guarantee.
"""
import re
import ast
import unittest
from itertools import product
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'mod/scripts/source/AstraAsedioSession.psc'


class SessionSourceEvaluator:
    """Fail closed on syntax outside the scalar PSC subset used by the session."""

    def __init__(self, source):
        self.state = {}
        self.native = {}
        self.bodies = {
            name: (params, body)
            for name, params, body in re.findall(
                r'^(?:bool |int |float |string )?(?:Function|Event) (\w+)\(([^\n]*)\)\n(.*?)^End(?:Function|Event)',
                source, re.M | re.S,
            )
        }
        header = source.split('Event OnInit()')[0]
        for raw in header.splitlines()[1:]:
            line = raw.split(';', 1)[0].strip()
            if not line:
                continue
            declaration = re.fullmatch(r'(bool|int|float|string|\w+\[\]|\w+) (?:Property )?(\w+)(?: = (.+?))?(?: Auto)?', line)
            if declaration is None:
                raise AssertionError('Unsupported source declaration: ' + line)
            kind, name, value = declaration.groups()
            self.state[name] = self.expr(value, {}) if value else {
                'bool': False, 'int': 0, 'float': 0.0, 'string': '',
            }.get(kind, [] if kind.endswith('[]') else None)

    def expr(self, value, local):
        value = re.sub(r'\btrue\b', 'True', value, flags=re.I)
        value = re.sub(r'\bfalse\b', 'False', value, flags=re.I)
        value = value.replace('&&', ' and ').replace('||', ' or ')
        value = re.sub(r'!(?!=)', 'not ', value)
        calls = {name: (lambda *args, _name=name: self.run(_name, *args)) for name in self.bodies}
        value = re.sub(r'new float\[(\d+)\]', r'[0.0]*\1', value)
        value = re.sub(r'\b(\w+)\.Length\b', r'len(\1)', value, flags=re.I)
        # Placement fixtures return actual reference-shaped objects or None.
        # This evaluator does not establish the VM's runtime Form cast.
        value = re.sub(r'\s+as\s+(?:ObjectReference|AstraAsedioGuard)\b', '', value, flags=re.I)
        if value.strip().startswith('Debug.'):
            # Real PSC Trace strings coerce scalars/reference values in +.
            # Enable these native boundaries only for fixtures supplying Debug.
            class TraceStringAddition(ast.NodeTransformer):
                def visit_BinOp(self, node):
                    self.generic_visit(node)
                    if isinstance(node.op, ast.Add):
                        return ast.copy_location(ast.Call(func=ast.Name(id='psc_add',ctx=ast.Load()),args=[node.left,node.right],keywords=[]),node)
                    return node
            tree = ast.fix_missing_locations(TraceStringAddition().visit(ast.parse(value.strip(),mode='eval')))
            value = compile(tree,'<psc trace>','eval')
        def psc_add(left,right):
            return str(left)+str(right) if isinstance(left,str) or isinstance(right,str) else left+right
        return eval(value, {'__builtins__': {}, 'len': len,'psc_add':psc_add}, {**self.state, **calls, **self.native, **local})

    def run(self, name, *args):
        if name in self.native:
            return self.native[name](*args)
        params, body = self.bodies[name]
        declarations = [param.strip() for param in params.split(',') if param.strip()]
        names = [param.split()[1] for param in declarations]
        values = list(args)
        for param in declarations[len(values):]:
            if '=' not in param:
                raise AssertionError('Wrong argument count for ' + name)
            values.append(self.expr(param.split('=', 1)[1].strip(), {}))
        if len(names) != len(values):
            raise AssertionError('Wrong argument count for ' + name)
        local = dict(zip(names, values))
        stack = []
        lines = body.splitlines()
        index = 0
        loops = []
        steps = 0
        while index < len(lines):
            raw = lines[index]
            index += 1
            steps += 1
            if steps > 10000:
                raise AssertionError('Unbounded evaluator loop in ' + name)
            line = raw.split(';', 1)[0].strip()
            if not line:
                continue
            active = all(frame[2] for frame in stack)
            if line.startswith('while '):
                if active and self.expr(line[6:], local):
                    loops.append(index - 1)
                else:
                    depth = 1
                    while depth:
                        if index >= len(lines):
                            raise AssertionError('Unclosed source loop')
                        next_line = lines[index].strip()
                        index += 1
                        depth += int(next_line.startswith('while ')) - int(next_line == 'endwhile')
                continue
            if line == 'endwhile':
                index = loops.pop()
                continue
            if line.startswith('if '):
                branch = active and bool(self.expr(line[3:], local))
                stack.append([active, branch, branch])
                continue
            if line.startswith('elseif '):
                parent, taken, _ = stack[-1]
                branch = parent and not taken and bool(self.expr(line[7:], local))
                stack[-1] = [parent, taken or branch, branch]
                continue
            if line == 'else':
                parent, taken, _ = stack[-1]
                stack[-1] = [parent, True, parent and not taken]
                continue
            if line == 'endif':
                stack.pop()
                continue
            if not active:
                continue
            if line == 'return':
                return None
            if line.startswith('return '):
                return self.expr(line[7:], local)
            if line.startswith('Debug.') and 'Debug' not in self.state:
                continue
            declaration = re.fullmatch(r'(?:bool|int|float(?:\[\])?|string|Actor|ObjectReference|AstraAsedioActi|AstraAsedioGuard) (\w+) = (.+)', line)
            if declaration:
                local[declaration[1]] = self.expr(declaration[2], local)
                continue
            assignment = re.fullmatch(r'(\w+(?:\[.+?\])?)\s*(\+=|-=|=)\s*(.+)', line)
            if assignment:
                key, op, value = assignment.groups()
                if '[' in key:
                    array, offset = key.split('[', 1)
                    target = local if array in local else self.state
                    slot = self.expr(offset[:-1], local)
                    result = self.expr(value, local)
                    target[array][slot] = result if op == '=' else target[array][slot] + result if op == '+=' else target[array][slot] - result
                    continue
                target = local if key in local else self.state
                result = self.expr(value, local)
                target[key] = result if op == '=' else target[key] + result if op == '+=' else target[key] - result
                continue
            if re.match(r'^\w+(?:\.\w+)?\(', line):
                self.expr(line, local)
                continue
            raise AssertionError('Unsupported source statement: ' + line)
        if stack:
            raise AssertionError('Unclosed source conditional in ' + name)


class NativeControlFixture:
    """Only true flags change controls; hooks can interrupt before/after a native effect."""

    def __init__(self, source, movement=True, fighting=True, camswitch=True, looking=True, camera=0):
        self.vm = SessionSourceEvaluator(source)
        self.controls = [movement, fighting, camswitch, looking, True, True, True, True]
        self.calls = []
        self.camera_calls = []
        self.order = []
        self.hooks = {}
        self.running = True
        self.camera = camera
        self.force_immediate = True
        self.menu = False
        self.dead = False
        self.vm.native['IsRunning'] = self.is_running
        self.vm.state['Game'] = SimpleNamespace(
            IsMovementControlsEnabled=lambda: self.snapshot(0, 'movement'),
            IsFightingControlsEnabled=lambda: self.snapshot(1, 'fighting'),
            IsCamSwitchControlsEnabled=lambda: self.snapshot(2, 'camswitch'),
            IsLookingControlsEnabled=lambda: self.snapshot(3, 'looking'),
            GetPlayer=lambda: SimpleNamespace(IsDead=self.is_dead),
            ForceFirstPerson=lambda: self.force_camera(0, 'first'),
            ForceThirdPerson=lambda: self.force_camera(9, 'third'),
            DisablePlayerControls=lambda *flags: self.change(False, 'disable', flags),
            EnablePlayerControls=lambda *flags: self.change(True, 'enable', flags),
        )
        self.vm.state['Camera'] = SimpleNamespace(GetCameraState=self.camera_state)
        self.vm.state['SKSE'] = SimpleNamespace(GetPluginVersion=lambda name: 0x03030000)
        self.vm.state['AstraSightNative'] = SimpleNamespace(GetAPIVersion=lambda: 3, GetCameraState=self.camera_state)
        self.vm.state['Utility'] = SimpleNamespace(IsInMenuMode=self.menu_mode)

    def is_dead(self):
        self.interrupt('dead', 'before')
        value = self.dead
        self.interrupt('dead', 'after')
        return value

    def menu_mode(self):
        self.interrupt('menu', 'before')
        value = self.menu
        self.interrupt('menu', 'after')
        return value

    def camera_state(self):
        self.interrupt('camera', 'before')
        value = self.camera
        self.interrupt('camera', 'after')
        return value

    def force_camera(self, state, name):
        self.camera_calls.append(name)
        self.order.append(name)
        self.interrupt(name, 'before')
        if self.force_immediate:
            self.camera = state
        self.interrupt(name, 'after')

    def interrupt(self, name, phase):
        callback = self.hooks.pop((name, phase), None)
        if callback is not None:
            callback()

    def is_running(self):
        self.interrupt('running', 'before')
        value = self.running
        self.interrupt('running', 'after')
        return value

    def snapshot(self, index, name):
        self.interrupt(name, 'before')
        value = self.controls[index]
        self.interrupt(name, 'after')
        return value

    def change(self, enabled, name, flags):
        if len(flags) != 8 or any(type(flag) is not bool for flag in flags):
            raise AssertionError('Controls must use eight explicit boolean flags')
        self.calls.append((name, flags))
        self.order.append(name)
        self.interrupt(name, 'before')
        for index, owned in enumerate(flags):
            if owned:
                self.controls[index] = enabled
        self.interrupt(name, 'after')

    def gun(self):
        gun = SimpleNamespace(ends=0, token=-1, UseSightCamera=False)

        def end():
            gun.ends += 1
            self.vm.run('Release', gun, gun.token)

        gun.EndSession = end
        return gun


class ControlLeaseContract(unittest.TestCase):
    def fixture(self, **kwargs):
        return NativeControlFixture(SOURCE.read_text(), **kwargs)

    def assert_released(self, fixture, initial=(True, True, True)):
        if len(initial) == 2:
            initial = (*initial, True)
        self.assertEqual(fixture.controls[:3], list(initial), 'a cancelled lease stranded or enabled unowned controls')
        self.assertTrue(all(fixture.controls[3:]))
        self.assertIsNone(fixture.vm.state['activeGun'])
        self.assertFalse(fixture.vm.state['acquiredMovement'])
        self.assertFalse(fixture.vm.state['acquiredFighting'])
        self.assertFalse(fixture.vm.state.get('acquiredCamSwitch', True))

    def test_cleanup_during_movement_snapshot_cannot_resume_with_a_new_token(self):
        fixture = self.fixture()
        gun = fixture.gun()
        fixture.hooks[('movement', 'after')] = lambda: fixture.vm.run('EmergencyCleanup')
        token = fixture.vm.run('Acquire', gun)
        self.assertEqual(token, -1, 'cancelled Acquire returned the cleanup generation as a valid token')
        self.assert_released(fixture)

    def test_cleanup_before_disable_aborts_without_enabling_any_controls(self):
        for boundary in ('running', 'movement', 'fighting', 'camswitch', 'looking', 'camera'):
            for phase in ('before', 'after'):
                for cleanup in ('EmergencyCleanup', 'RestoreControls'):
                    with self.subTest(boundary=boundary, phase=phase, cleanup=cleanup):
                        fixture = self.fixture()
                        fixture.hooks[(boundary, phase)] = lambda: fixture.vm.run(cleanup)
                        self.assertEqual(fixture.vm.run('Acquire', fixture.gun()), -1)
                        self.assert_released(fixture)
                        self.assertEqual(fixture.calls, [], 'cancellation before Disable must not toggle controls')

    def test_cleanup_over_native_disable_rolls_back_only_the_captured_controls(self):
        for initial in product((True, False), repeat=3):
            for phase in ('before', 'after'):
                for cleanup in ('EmergencyCleanup', 'RestoreControls'):
                    with self.subTest(initial=initial, phase=phase, cleanup=cleanup):
                        fixture = self.fixture(movement=initial[0], fighting=initial[1], camswitch=initial[2])
                        fixture.hooks[('disable', phase)] = lambda: fixture.vm.run(cleanup)
                        self.assertEqual(fixture.vm.run('Acquire', fixture.gun()), -1)
                        self.assert_released(fixture, initial)
                        flags = (*initial, False, False, False, False, False)
                        self.assertEqual(fixture.calls, [('disable', flags), ('enable', flags)])

    def test_incomplete_acquisition_is_never_current_and_cannot_admit_another_lease(self):
        for boundary in ('running', 'movement', 'fighting', 'camswitch', 'looking', 'camera', 'disable'):
            for phase in ('before', 'after'):
                with self.subTest(boundary=boundary, phase=phase):
                    fixture = self.fixture()
                    gun, contender = fixture.gun(), fixture.gun()
                    observations = []

                    def interrupted():
                        observations.append(fixture.vm.run('IsCurrent', gun, fixture.vm.state['generation']))
                        observations.append(fixture.vm.run('Acquire', contender))

                    fixture.hooks[(boundary, phase)] = interrupted
                    token = fixture.vm.run('Acquire', gun)
                    self.assertEqual(observations, [False, -1])
                    self.assertGreater(token, 0)
                    self.assertTrue(fixture.vm.run('IsCurrent', gun, token))
                    fixture.vm.run('Release', gun, token)
                    self.assert_released(fixture)

    def test_cleanup_can_repeat_and_reenter_during_cancelled_acquisition_rollback(self):
        fixture = self.fixture(movement=False)
        gun, contender = fixture.gun(), fixture.gun()
        observations = []

        def cancel():
            fixture.vm.run('EmergencyCleanup')
            fixture.vm.run('EmergencyCleanup')
            fixture.vm.run('RestoreControls')

        def rollback():
            self.assertIsNone(fixture.vm.state['activeGun'])
            observations.append(fixture.vm.run('Acquire', contender))
            fixture.vm.run('EmergencyCleanup')
            fixture.vm.run('RestoreControls')
            observations.append(fixture.vm.run('Acquire', contender))

        fixture.hooks[('disable', 'after')] = cancel
        fixture.hooks[('enable', 'before')] = rollback
        fixture.hooks[('enable', 'after')] = rollback
        self.assertEqual(fixture.vm.run('Acquire', gun), -1)
        self.assertEqual(observations, [-1, -1, -1, -1])
        self.assert_released(fixture, (False, True))
        self.assertEqual([name for name, _ in fixture.calls], ['disable', 'enable'])
        new_token = fixture.vm.run('Acquire', contender)
        self.assertTrue(fixture.vm.run('IsCurrent', contender, new_token))
        fixture.vm.run('Release', contender, new_token)
        self.assert_released(fixture, (False, True))

    def test_release_blocks_new_leases_until_native_enable_has_completed(self):
        for phase in ('before', 'after'):
            with self.subTest(phase=phase):
                fixture = self.fixture()
                gun, contender = fixture.gun(), fixture.gun()
                token = fixture.vm.run('Acquire', gun)
                attempts = []

                def interrupted():
                    self.assertIsNone(fixture.vm.state['activeGun'])
                    self.assertFalse(fixture.vm.run('IsCurrent', gun, token))
                    attempts.append(fixture.vm.run('Acquire', contender))
                    fixture.vm.run('EmergencyCleanup')
                    fixture.vm.run('Release', gun, token)
                    attempts.append(fixture.vm.run('Acquire', contender))

                fixture.hooks[('enable', phase)] = interrupted
                fixture.vm.run('Release', gun, token)
                self.assertEqual(attempts, [-1, -1])
                self.assert_released(fixture)
                self.assertEqual([name for name, _ in fixture.calls], ['disable', 'enable'])
                new_token = fixture.vm.run('Acquire', contender)
                self.assertTrue(fixture.vm.run('IsCurrent', contender, new_token))
                self.assertEqual(fixture.controls[:2], [False, False])
                fixture.vm.run('Release', contender, new_token)
                self.assert_released(fixture)

    def test_normal_release_preserves_prelocked_controls_and_ignores_stale_release(self):
        for initial in product((True, False), repeat=3):
            with self.subTest(initial=initial):
                fixture = self.fixture(movement=initial[0], fighting=initial[1], camswitch=initial[2])
                gun = fixture.gun()
                token = fixture.vm.run('Acquire', gun)
                self.assertEqual(fixture.controls[:2], [False, False])
                self.assertTrue(fixture.vm.run('IsCurrent', gun, token))
                fixture.vm.run('Release', gun, token)
                self.assert_released(fixture, initial)
                previous_calls = list(fixture.calls)
                fixture.vm.run('Release', gun, token)
                self.assertEqual(fixture.calls, previous_calls)
                contender = fixture.gun()
                next_token = fixture.vm.run('Acquire', contender)
                self.assertGreater(next_token, token)
                fixture.vm.run('Release', gun, token)
                self.assertTrue(fixture.vm.run('IsCurrent', contender, next_token))
                self.assertEqual(fixture.controls[:2], [False, False])
                fixture.vm.run('Release', contender, next_token)
                self.assert_released(fixture, initial)

    def test_emergency_cleanup_releases_the_current_gun_once_and_cannot_restore_globally(self):
        fixture = self.fixture(fighting=False)
        gun = fixture.gun()
        gun.token = fixture.vm.run('Acquire', gun)
        fixture.vm.run('EmergencyCleanup')
        self.assertEqual(gun.ends, 1)
        self.assert_released(fixture, (True, False))
        previous_calls = list(fixture.calls)
        fixture.vm.run('EmergencyCleanup')
        fixture.vm.run('RestoreControls')
        fixture.vm.run('Release', gun, gun.token)
        self.assertEqual(fixture.calls, previous_calls)
        self.assertFalse(fixture.vm.run('IsCurrent', None, fixture.vm.state['generation']))

    def test_invalid_gun_and_stopped_quest_do_not_toggle_controls_or_block_a_later_lease(self):
        fixture = self.fixture()
        self.assertEqual(fixture.vm.run('Acquire', None), -1)
        fixture.running = False
        self.assertEqual(fixture.vm.run('Acquire', fixture.gun()), -1)
        self.assert_released(fixture)
        self.assertEqual(fixture.calls, [])
        fixture.running = True
        gun = fixture.gun()
        token = fixture.vm.run('Acquire', gun)
        self.assertTrue(fixture.vm.run('IsCurrent', gun, token))
        fixture.vm.run('Release', gun, token)
        self.assert_released(fixture)

    def test_source_evaluator_rejects_unsupported_statements(self):
        source = SOURCE.read_text().replace('generation += 1', 'Unsupported instruction', 1)
        fixture = NativeControlFixture(source)
        with self.assertRaisesRegex(AssertionError, 'Unsupported source statement'):
            fixture.vm.run('Acquire', fixture.gun())


if __name__ == '__main__':
    unittest.main()
