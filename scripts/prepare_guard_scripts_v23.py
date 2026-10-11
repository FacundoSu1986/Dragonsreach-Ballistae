"""Generate v23 lifecycle wrapper with fenced v22 saved-stack compatibility."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/'mod/scripts/source'


def baseline(name):
    return subprocess.check_output(['git','show','46bfbf7:mod/scripts/source/'+name+'.psc'],
        cwd=ROOT).decode('utf-8-sig').replace('\r\n','\n')


def function(text,name,body):
    expression = r'(?m)^([^\n]*\bFunction '+re.escape(name)+r'\([^\n]*\))\n[\s\S]*?^EndFunction'
    result,count = re.subn(expression,lambda m:m[1]+'\n'+body+'\nEndFunction',text)
    if count != 1:
        raise ValueError((name,count))
    return result


def event(text,name,body):
    expression = r'(?m)^(Event '+re.escape(name)+r'\([^\n]*\))\n[\s\S]*?^EndEvent'
    result,count = re.subn(expression,lambda m:m[1]+'\n'+body+'\nEndEvent',text)
    if count != 1:
        raise ValueError((name,count))
    return result


def main(runtime_include=None):
    guard = baseline('AstraAsedioGuard')
    for name,body in {
        'OnInit':'    BlockActivation(true)\n    StartV23()',
        'OnLoad':'    StartV23()',
        'OnUnload':'    StopV23()',
        'OnCellDetach':'    StopV23()',
        'OnDestructionStageChanged':'    if aiCurrentStage > 0\n        destroyed = true\n        StopV23()\n    endif',
        'OnUpdate':'    PumpV23()',
    }.items():
        guard = event(guard,name,body)
    guard = function(guard,'Current','    ; Fences every v22 aim/Fire/Reset stack restored from a save.\n    return false')
    # Legacy engine mutators cannot compete with the native owner, even when a
    # saved frame resumes inside an old helper. Keep signatures for VM recovery.
    silent_void = ('ReleaseOwnedGuard','RestoreNeutralScene','SetVisualBolt',
        'WriteAimNode','ApplyAim','StopGuardPose','CommitShot')
    silent_bool = ('AcquirePin','PlaySceneAnimation','StartGuardPose',
        'SetGuardFirePose','PositionOperator','FinishGuardEffect')
    for name in silent_void:
        guard = function(guard,name,'    ; Retired v22 effects: native NPC operation is the sole owner.\n    return')
    for name in silent_bool:
        guard = function(guard,name,'    ; Retired v22 effects: a restored stack cannot acquire or write.\n    return false')
    guard = function(guard,'BeginRecovery','    StartV23()')
    guard = function(guard,'Shutdown','    StopV23()')
    guard = function(guard,'ReservePlayerLease','    ; Low Whiterun stations remain NPC-only.\n    return -1')
    guard = function(guard,'PreparePlayerLease','    return false')
    guard = function(guard,'RetireStation',
        '    stationRetired = true\n    StopV23()\n    if v23Token <= 0 || !AstraGuardNative.IsAvailable()\n        return !sceneBusy && !pinBusy\n    endif\n    return AstraGuardNative.EndOperation(Self, v23Token)')
    inc = (runtime_include or ROOT/'scripts/guard_runtime_v23.pscinc').read_text()
    declarations,code = inc.split('Function StartV23()',1)
    guard = guard.replace('Event OnInit()',declarations+'\nEvent OnInit()',1)
    guard += '\nFunction StartV23()'+code
    assert 'Launcher.Fire(' not in guard
    (SRC/'AstraAsedioGuard.psc').write_text(guard,encoding='utf-8',newline='\n')

    # Saved Auto instances keep all properties and function signatures. They
    # unregister old timers and can only forward combat hints to the new owner.
    auto = baseline('AstraGuardiaAuto')
    pattern = r'(?m)^([^\n]*\bFunction ([A-Za-z0-9_]+)\([^\n]*\))\n[\s\S]*?^EndFunction'
    def retired(match):
        header,name = match[1],match[2]
        first = header.strip().split()[0].lower()
        body = '    ; v23 retired actuator; retained for existing saved instances.\n'
        if name == 'AlertaCombat':
            parameter = re.search(r'Actor\s+(\w+)',header,re.I)[1]
            body += '    ObjectReference stationRef = Self\n    AstraAsedioGuard controller = stationRef as AstraAsedioGuard\n    if controller != None\n        controller.NotifyCombatV23('+parameter+')\n    endif\n'
        if first == 'bool': body += '    return false'
        elif first in ('float','int'): body += '    return 0'
        elif first == 'actor': body += '    return None'
        else: body += '    UnregisterForUpdate()'
        return header+'\n'+body+'\nEndFunction'
    auto = re.sub(pattern,retired,auto)
    auto = re.sub(r'(?m)^(Event [^\n]+)\n[\s\S]*?^EndEvent',
        lambda m:m[1]+'\n    UnregisterForUpdate()\nEndEvent',auto)
    assert 'Launcher.Fire(' not in auto
    (SRC/'AstraGuardiaAuto.psc').write_text(auto,encoding='utf-8',newline='\n')

    alias = baseline('AstraAsedioPlayerAlias')
    alias = alias.replace('    StartCityRetirement()','    StartCityRetirement()\n    BootstrapGuardV23()')
    alias += '''
Function BootstrapGuardV23()
    Quest sensors = Game.GetFormFromFile(0x00000806, "AstraAsedio_GuardAnim.esp") as Quest
    if sensors != None && !sensors.IsRunning()
        sensors.Start()
    endif
    int index = 0
    while index < 2
        int formID = 0x00000B70+index*16
        AstraAsedioGuard controller = Game.GetFormFromFile(formID, "AstraAsedio_WhiterunTorres.esp") as AstraAsedioGuard
        if controller != None
            controller.StartV23()
        endif
        index += 1
    endwhile
EndFunction
'''
    (SRC/'AstraAsedioPlayerAlias.psc').write_text(alias,encoding='utf-8',newline='\n')
    # Keep the old linked-ref function for saved stack compatibility. Its Auto
    # target is retired; all live sensors use the single station controller.
    sensor = '''Scriptname AstraGuardiaNPC extends Actor

AstraGuardiaAuto Function Torre()
    return GetLinkedRef() as AstraGuardiaAuto
EndFunction

AstraAsedioGuard Function ControllerV23()
    return GetLinkedRef() as AstraAsedioGuard
EndFunction

Event OnInit()
    AstraAsedioGuard controller = ControllerV23()
    if controller != None
        controller.StartV23()
    endif
EndEvent

Event OnLoad()
    AstraAsedioGuard controller = ControllerV23()
    if controller != None
        controller.StartV23()
        controller.NotifyCombatV23(GetCombatTarget())
    endif
EndEvent

Event OnCombatStateChanged(Actor akTarget, int aeCombatState)
    AstraAsedioGuard controller = ControllerV23()
    if controller != None
        controller.NotifyCombatV23(akTarget)
    endif
EndEvent

Event OnDeath(Actor akKiller)
    AstraAsedioGuard controller = ControllerV23()
    if controller != None
        controller.StopV23()
    endif
EndEvent

Event OnUnload()
    AstraAsedioGuard controller = ControllerV23()
    if controller != None
        controller.StopV23()
    endif
EndEvent
'''
    (SRC/'AstraGuardiaNPC.psc').write_text(sensor,encoding='utf-8',newline='\n')
    print('GUARD_V23_SCRIPTS_PREPARED')


if __name__ == '__main__':
    main()
