Scriptname AstraAsedioPlayerAlias extends ReferenceAlias
AstraAsedioSession Property Session Auto
bool cityRetirementPending = false
bool cityRetirementBusy = false
Event OnInit()
    Debug.Trace("AstraAsedio Player alias initialized ref=" + GetReference() + " session=" + Session)
    StartCityRetirement()
    BootstrapGuardV23()
EndEvent
Event OnPlayerLoadGame()
    CleanupSession()
    StartCityRetirement()
    BootstrapGuardV23()
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
        Debug.Notification("Ballista: the player cleanup quest is missing.")
    endif
EndFunction

Function StartCityRetirement()
    cityRetirementPending = true
    RegisterForSingleUpdate(0.2)
EndFunction

Event OnUpdate()
    if !cityRetirementPending
        return
    endif
    if cityRetirementBusy
        RegisterForSingleUpdate(0.2)
        return
    endif
    cityRetirementBusy = true
    bool east = RetireLegacyCity(0x00000B40, 0x00000B70)
    bool west = RetireLegacyCity(0x00000B50, 0x00000B80)
    cityRetirementPending = !east || !west
    cityRetirementBusy = false
    if cityRetirementPending
        RegisterForSingleUpdate(0.2)
    endif
EndEvent

bool Function RetireLegacyCity(int oldID, int newID)
    ObjectReference replacement = Game.GetFormFromFile(newID, "DragonsreachBallistae_WhiterunTowers.esp") as ObjectReference
    if replacement == None
        return true
    endif
    ObjectReference previous = Game.GetFormFromFile(oldID, "DragonsreachBallistae_WhiterunTowers.esp") as ObjectReference
    if previous == None
        return true
    endif
    ; Pre-3.5.0 has no effects query and no native owner. Retirement continues.
    ; Waiting would reschedule this alias every 0.2s and never disable the refs.
    if SKSE.GetPluginVersion("AstraSight") >= 50659328
        if !AstraSightNative.IsEffectsQuiescent(previous, 0)
            return false
        endif
    endif
    AstraAsedioGuard controller = previous as AstraAsedioGuard
    if controller != None
        bool drained = controller.RetireStation()
        if !drained
            return false
        endif
    endif
    ; Only the five known own refs are retired. The replacement has fresh VMAD
    ; bindings; vanilla towers, patrols, navmesh and other mods are untouched.
    int offset = 0
    while offset < 5
        ObjectReference item = Game.GetFormFromFile(oldID + offset, "DragonsreachBallistae_WhiterunTowers.esp") as ObjectReference
        if item != None
            item.Disable(false)
        endif
        offset += 1
    endwhile
    Debug.Trace("AstraAsedio city retired legacy=" + oldID + " replacement=" + newID)
    return true
EndFunction

Function BootstrapGuardV23()
    Quest sensors = Game.GetFormFromFile(0x00000806, "DragonsreachBallistae_GuardAnims.esp") as Quest
    if sensors != None && !sensors.IsRunning()
        sensors.Start()
    endif
    int index = 0
    while index < 2
        int formID = 0x00000B70+index*16
        AstraAsedioGuard controller = Game.GetFormFromFile(formID, "DragonsreachBallistae_WhiterunTowers.esp") as AstraAsedioGuard
        if controller != None
            ; Revoke the old token before changing alias/package state. The
            ; controller waits for its effects barrier before relocating.
            controller.StartV23()
            Actor operatorRef = Game.GetFormFromFile(formID+1, "DragonsreachBallistae_WhiterunTowers.esp") as Actor
            if sensors != None && sensors.IsRunning() && operatorRef != None
                ReferenceAlias operatorAlias = sensors.GetAlias(index) as ReferenceAlias
                if operatorAlias != None
                    ; These two v24 aliases are Optional, so Clear is legal.
                    ; Refilling reapplies ALPC to FF bases restored from saves.
                    operatorAlias.Clear()
                    operatorAlias.ForceRefTo(operatorRef)
                    operatorRef.EvaluatePackage()
                endif
            endif
        endif
        index += 1
    endwhile
EndFunction
