Scriptname AstraAsedioPlayerAlias extends ReferenceAlias
AstraAsedioSession Property Session Auto
Event OnInit()
    Debug.Trace("AstraAsedio Player alias initialized ref=" + GetReference() + " session=" + Session)
EndEvent
Event OnPlayerLoadGame()
    CleanupSession()
EndEvent
Event OnDeath(Actor akKiller)
    CleanupSession()
EndEvent
Event OnCellDetach()
    CleanupSession()
EndEvent
Function CleanupSession()
    if Session != None
        Session.EmergencyCleanup()
    else
        Debug.Trace("AstraAsedio player alias PROPERTY_SESSION_NONE")
        Debug.Notification("Astra: falta la quest de limpieza del jugador.")
    endif
EndFunction
