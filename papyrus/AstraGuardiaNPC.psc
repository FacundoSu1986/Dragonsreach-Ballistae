Scriptname AstraGuardiaNPC extends Actor

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
