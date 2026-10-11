Scriptname AstraGuardOperatorAlias extends ReferenceAlias
AstraAsedioGuard Property Controller Auto

Event OnLoad()
    if Controller != None
        Controller.StartV23()
    endif
EndEvent

Event OnCombatStateChanged(Actor akTarget, int aeCombatState)
    if Controller != None
        Controller.NotifyCombatV23(akTarget)
    endif
EndEvent

Event OnDeath(Actor akKiller)
    if Controller != None
        Controller.StopV23()
    endif
EndEvent

Event OnUnload()
    if Controller != None
        Controller.StopV23()
    endif
EndEvent
