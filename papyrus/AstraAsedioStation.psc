Scriptname AstraAsedioStation extends AstraAsedioActi
; Both scripts are siblings on the same city gun. VMAD links Guard to Self.
AstraAsedioGuard Property Guard Auto

AstraAsedioGuard stationCoordinator
int stationLease = 0
int stationRevision = 0
int stationBusyRevision = -1
bool stationBusy = false
bool stationWaiting = false
bool stationReleasing = false
bool stationUnavailable = false
bool stationDestroyed = false
float stationWaitStarted = 0.0
float stationWaitDeadline = 0.0
; 0 means this release has not yet sampled a live effects query.
float stationReleaseStarted = 0.0
float stationReleaseDeadline = 0.0

Event OnInit()
    Parent.OnInit()
EndEvent

bool Function StationCurrent(int expectedRevision, AstraAsedioGuard expectedGuard, int expectedLease)
    return stationRevision == expectedRevision && stationCoordinator == expectedGuard && stationLease == expectedLease
EndFunction

Function ScheduleStationPoll()
    ; The parent's first update can be delivered before its entry stack returns.
    ; Keep that request alive while our slot prevents delegation into the parent.
    if stationWaiting || stationReleasing || (stationBusy && stationLease > 0)
        RegisterForSingleUpdate(0.05)
    endif
EndFunction

Function FinishStationCall(int expectedRevision)
    ; Load/unload can invalidate the revision but cannot replace this mutation
    ; slot. Its old stack must return before any newer reservation can start.
    if stationBusy && stationBusyRevision == expectedRevision
        stationBusy = false
        stationBusyRevision = -1
    endif
EndFunction

string Function StationNativeFailure(int expectedRevision, AstraAsedioGuard expectedGuard, int expectedLease)
    ; Avoid reserving the NPC if the wildcard cleanup binding is unavailable.
    int skseVersion = SKSE.GetVersion()
    if !StationCurrent(expectedRevision, expectedGuard, expectedLease)
        return "STATION_ENTRY_CANCELLED"
    endif
    if skseVersion < 2
        return "SKSE_MISSING: launch Skyrim through SKSE64."
    endif
    int pluginVersion = SKSE.GetPluginVersion("AstraSight")
    if !StationCurrent(expectedRevision, expectedGuard, expectedLease)
        return "STATION_ENTRY_CANCELLED"
    endif
    if pluginVersion < 50659392
        return "NATIVE_SIGHT_MISSING: install the AstraSight.dll of this release."
    endif
    int api = AstraSightNative.GetAPIVersion()
    if !StationCurrent(expectedRevision, expectedGuard, expectedLease)
        return "STATION_ENTRY_CANCELLED"
    endif
    if api != 4
        return "NATIVE_API_MISMATCH: reinstall all files of this release."
    endif
    bool available = AstraSightNative.IsAvailable()
    if !StationCurrent(expectedRevision, expectedGuard, expectedLease)
        return "STATION_ENTRY_CANCELLED"
    endif
    if !available
        return "NATIVE_SIGHT_UNAVAILABLE: the native sight is not available."
    endif
    return ""
EndFunction

Event OnActivate(ObjectReference akActionRef)
    if stationBusy || stationWaiting || stationReleasing || stationDestroyed || stationUnavailable
        return
    endif
    stationBusy = true
    int activationRevision = stationRevision
    stationBusyRevision = activationRevision
    Debug.Trace("AstraAsedioStation activate ref=" + Self + " revision=" + activationRevision)
    AstraAsedioGuard coordinator = stationCoordinator
    int lease = stationLease
    Actor operator = Game.GetPlayer()
    if !StationCurrent(activationRevision, coordinator, lease) || akActionRef != operator
        FinishStationCall(activationRevision)
        ScheduleStationPoll()
        return
    endif
    if lease > 0
        bool active = Parent.IsPlayerOperating()
        if StationCurrent(activationRevision, coordinator, lease) && active
            ; Preserve the parent's input debounce and exit behavior.
            Parent.OnActivate(akActionRef)
        endif
        bool stillActive = Parent.IsPlayerOperating()
        FinishStationCall(activationRevision)
        if !StationCurrent(activationRevision, coordinator, lease) || !stillActive
            EndSession()
        endif
        return
    endif
    AstraAsedioGuard configuredGuard = Guard
    if configuredGuard == None
        FinishStationCall(activationRevision)
        Parent.RejectActivation("PROPERTY_GUARD_NONE: the station coordinator is missing.")
        return
    endif
    string nativeFailure = StationNativeFailure(activationRevision, coordinator, lease)
    if !StationCurrent(activationRevision, coordinator, lease)
        FinishStationCall(activationRevision)
        ScheduleStationPoll()
        return
    endif
    if nativeFailure != ""
        Parent.RejectActivation(nativeFailure)
        FinishStationCall(activationRevision)
        ScheduleStationPoll()
        return
    endif
    coordinator = configuredGuard
    stationRevision += 1
    activationRevision = stationRevision
    stationBusyRevision = activationRevision
    stationCoordinator = coordinator
    stationWaiting = true
    lease = coordinator.ReservePlayerLease()
    ; A cancellation during Reserve cannot forget a lease returned after it.
    ; No newer reservation can exist while this callback holds stationBusy.
    if lease > 0
        stationLease = lease
    endif
    if !StationCurrent(activationRevision, coordinator, lease) || lease <= 0
        Debug.Trace("AstraAsedioStation reservation rejected ref=" + Self + " lease=" + lease)
        FinishStationCall(activationRevision)
        EndSession()
        return
    endif
    float now = Utility.GetCurrentRealTime()
    if !StationCurrent(activationRevision, coordinator, lease) || now != now || now < 0.0 || now > 1000000000.0
        FinishStationCall(activationRevision)
        EndSession()
        return
    endif
    stationWaitStarted = now
    ; Preparation includes several yielding scene and actor natives. Keep a
    ; finite bound without cancelling a successful four-second preparation.
    stationWaitDeadline = now + 10.0
    Parent.RegisterMenus()
    FinishStationCall(activationRevision)
    if !StationCurrent(activationRevision, coordinator, lease)
        EndSession()
        return
    endif
    PollStationEntry()
EndEvent

bool Function StationEntryValid(int expectedRevision, AstraAsedioGuard expectedGuard, int expectedLease, Actor operator)
    if !StationCurrent(expectedRevision, expectedGuard, expectedLease) || operator == None || stationUnavailable || stationDestroyed
        return false
    endif
    bool loaded = Is3DLoaded()
    if !StationCurrent(expectedRevision, expectedGuard, expectedLease) || !loaded
        return false
    endif
    bool menuOpen = Utility.IsInMenuMode()
    if !StationCurrent(expectedRevision, expectedGuard, expectedLease) || menuOpen
        return false
    endif
    bool dead = operator.IsDead()
    if !StationCurrent(expectedRevision, expectedGuard, expectedLease) || dead
        return false
    endif
    float now = Utility.GetCurrentRealTime()
    return StationCurrent(expectedRevision, expectedGuard, expectedLease) && now == now && now >= stationWaitStarted && now <= stationWaitDeadline
EndFunction

Function PollStationEntry()
    if stationBusy || !stationWaiting || stationReleasing
        return
    endif
    stationBusy = true
    int entryRevision = stationRevision
    stationBusyRevision = entryRevision
    AstraAsedioGuard coordinator = stationCoordinator
    int lease = stationLease
    Actor operator = Game.GetPlayer()
    bool valid = StationEntryValid(entryRevision, coordinator, lease, operator)
    if !StationCurrent(entryRevision, coordinator, lease) || !valid
        Debug.Trace("AstraAsedioStation entry cancelled before prepare ref=" + Self + " lease=" + lease)
        FinishStationCall(entryRevision)
        EndSession()
        return
    endif
    bool ready = coordinator.PreparePlayerLease(lease)
    ; A native Prepare can return after the deadline, menu, death or 3D loss.
    valid = StationEntryValid(entryRevision, coordinator, lease, operator)
    if !StationCurrent(entryRevision, coordinator, lease) || !valid
        Debug.Trace("AstraAsedioStation entry cancelled after prepare ref=" + Self + " lease=" + lease + " ready=" + ready)
        FinishStationCall(entryRevision)
        EndSession()
        return
    endif
    if !ready
        FinishStationCall(entryRevision)
        ScheduleStationPoll()
        return
    endif
    Parent.ResetStationAim()
    valid = StationEntryValid(entryRevision, coordinator, lease, operator)
    if !StationCurrent(entryRevision, coordinator, lease) || !valid
        FinishStationCall(entryRevision)
        EndSession()
        return
    endif
    stationWaiting = false
    Debug.Trace("AstraAsedioStation entering player sight ref=" + Self + " lease=" + lease)
    Parent.OnActivate(operator)
    ; OnActivate may have suspended before acquiring controls. A child cancel
    ; must run End again after its return to drain any late parent entry.
    bool active = Parent.IsPlayerOperating()
    FinishStationCall(entryRevision)
    if !StationCurrent(entryRevision, coordinator, lease) || !active
        EndSession()
    endif
EndFunction

Function EndSession()
    ; Invalidate entry/query stacks before the parent's first native boundary.
    stationRevision += 1
    stationWaiting = false
    stationReleaseStarted = 0.0
    stationReleaseDeadline = 0.0
    stationReleasing = stationCoordinator != None
    Parent.EndSession()
    PollStationRelease()
    ScheduleStationPoll()
EndFunction

Function PollStationRelease()
    if stationBusy || !stationReleasing
        return
    endif
    stationBusy = true
    int releaseRevision = stationRevision
    stationBusyRevision = releaseRevision
    AstraAsedioGuard coordinator = stationCoordinator
    int lease = stationLease
    bool active = Parent.IsPlayerOperating()
    if !StationCurrent(releaseRevision, coordinator, lease) || active
        FinishStationCall(releaseRevision)
        ScheduleStationPoll()
        return
    endif
    bool pending = Parent.IsPlayerCleanupPending()
    if !StationCurrent(releaseRevision, coordinator, lease) || pending
        FinishStationCall(releaseRevision)
        ScheduleStationPoll()
        return
    endif
    ; 3.5.0+ only. An older or missing DLL has no native owner: release now.
    int pluginVersion = SKSE.GetPluginVersion("AstraSight")
    if !StationCurrent(releaseRevision, coordinator, lease)
        FinishStationCall(releaseRevision)
        ScheduleStationPoll()
        return
    endif
    bool quiet = true
    if pluginVersion >= 50659328
        quiet = AstraSightNative.IsEffectsQuiescent(Self, 0)
    endif
    if !StationCurrent(releaseRevision, coordinator, lease)
        FinishStationCall(releaseRevision)
        ScheduleStationPoll()
        return
    endif
    if !quiet
        float now = Utility.GetCurrentRealTime()
        if !StationCurrent(releaseRevision, coordinator, lease)
            FinishStationCall(releaseRevision)
            ScheduleStationPoll()
            return
        endif
        ; A live query that never settles must not poll at 20 Hz for the
        ; session. Five seconds, or a restarted or invalid clock, releases.
        bool clockOk = now == now && now >= 0.0 && now <= 1000000000.0
        if clockOk && stationReleaseDeadline <= 0.0
            stationReleaseStarted = now
            stationReleaseDeadline = now + 5.0
        endif
        if clockOk && now >= stationReleaseStarted && now <= stationReleaseDeadline
            FinishStationCall(releaseRevision)
            ScheduleStationPoll()
            return
        endif
        Debug.Trace("AstraAsedioStation effects quiescence timed out ref=" + Self + " lease=" + lease)
        if !StationCurrent(releaseRevision, coordinator, lease)
            FinishStationCall(releaseRevision)
            ScheduleStationPoll()
            return
        endif
        quiet = true
    endif
    if !StationCurrent(releaseRevision, coordinator, lease) || !quiet
        FinishStationCall(releaseRevision)
        ScheduleStationPoll()
        return
    endif
    ; Only this release may clear its own window. A nested EndSession during
    ; the trace already installed the next one under a new revision.
    stationReleaseStarted = 0.0
    stationReleaseDeadline = 0.0
    if coordinator != None && lease > 0
        ; Release matches only this captured lease; a guard load may already
        ; have revoked it. Never read Guard again for an old release.
        coordinator.ReleasePlayerLease(lease)
    endif
    if StationCurrent(releaseRevision, coordinator, lease)
        stationCoordinator = None
        stationLease = 0
        stationReleasing = false
    endif
    FinishStationCall(releaseRevision)
    ScheduleStationPoll()
EndFunction

Event OnUpdate()
    if stationWaiting
        PollStationEntry()
    elseif stationReleasing
        PollStationRelease()
    elseif !stationBusy && stationLease > 0
        stationBusy = true
        int updateRevision = stationRevision
        stationBusyRevision = updateRevision
        AstraAsedioGuard coordinator = stationCoordinator
        int lease = stationLease
        bool active = Parent.IsPlayerOperating()
        if StationCurrent(updateRevision, coordinator, lease) && active
            Parent.OnUpdate()
        endif
        bool stillActive = Parent.IsPlayerOperating()
        FinishStationCall(updateRevision)
        if !StationCurrent(updateRevision, coordinator, lease) || !stillActive
            EndSession()
        endif
    endif
    ScheduleStationPoll()
EndEvent

Event OnMenuOpen(string menuName)
    if stationWaiting
        EndSession()
    else
        Parent.OnMenuOpen(menuName)
    endif
EndEvent

Event OnUnload()
    Debug.Trace("AstraAsedioStation OnUnload ref=" + Self + " revision=" + stationRevision)
    stationUnavailable = true
    EndSession()
EndEvent

Event OnCellDetach()
    Debug.Trace("AstraAsedioStation OnCellDetach ref=" + Self + " revision=" + stationRevision)
    stationUnavailable = true
    EndSession()
EndEvent

Event OnDestructionStageChanged(int aiOldStage, int aiCurrentStage)
    if aiCurrentStage > 0
        stationDestroyed = true
        EndSession()
    endif
EndEvent

Event OnLoad()
    Debug.Trace("AstraAsedioStation OnLoad ref=" + Self + " revision=" + stationRevision)
    ; Never call Parent.OnLoad: its matrix capture/aim restore races the guard.
    stationUnavailable = false
    stationRevision += 1
    int loadRevision = stationRevision
    bool ownSlot = !stationBusy
    if ownSlot
        stationBusy = true
        stationBusyRevision = loadRevision
    endif
    stationWaiting = false
    stationReleaseStarted = 0.0
    stationReleaseDeadline = 0.0
    stationReleasing = stationCoordinator != None
    ; Keep stationBusy until any saved suspended entry stack returns. Its
    ; revision is invalid, and its completion drains the late parent activation.
    Parent.RecoverStationLoad()
    Parent.NormalizeTimingProperties()
    BlockActivation(true)
    if ownSlot
        FinishStationCall(loadRevision)
    endif
    PollStationRelease()
    ScheduleStationPoll()
EndEvent
