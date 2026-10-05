Scriptname AstraAsedioSession extends Quest
; Own only controls observed as enabled. Idempotent cleanup survives save/load.
AstraAsedioActi activeGun
bool acquiredMovement = false
bool acquiredFighting = false
bool acquiredCamSwitch = false
int savedCamera = -1
bool changedPerspective = false
int generation = 0
bool acquiring = false
bool releasing = false
bool cleanupRequested = false

Event OnInit()
    Debug.Trace("AstraAsedio session quest initialized running=" + IsRunning())
EndEvent

int Function Acquire(AstraAsedioActi gun)
    if gun == None
        return -1
    endif
    if acquiring || releasing || activeGun != None
        return -1
    endif
    ; Keep one acquisition in flight across every native call, including IsRunning.
    acquiring = true
    cleanupRequested = false
    generation += 1
    int leaseGeneration = generation
    bool questRunning = IsRunning()
    if !questRunning || cleanupRequested || generation != leaseGeneration
        FinishCancelledAcquire()
        return -1
    endif
    activeGun = gun
    ; Local snapshots survive cleanup; never restore a flag read from invalidated state.
    bool movementSnapshot = Game.IsMovementControlsEnabled()
    bool fightingSnapshot = Game.IsFightingControlsEnabled()
    bool camSwitchSnapshot = Game.IsCamSwitchControlsEnabled()
    bool lookingSnapshot = Game.IsLookingControlsEnabled()
    int cameraSnapshot = ReadCameraState()
    if cleanupRequested || generation != leaseGeneration || activeGun != gun || !lookingSnapshot || (cameraSnapshot != 0 && cameraSnapshot != 8 && cameraSnapshot != 9)
        FinishCancelledAcquire()
        return -1
    endif
    acquiredMovement = movementSnapshot
    acquiredFighting = fightingSnapshot
    acquiredCamSwitch = camSwitchSnapshot
    savedCamera = cameraSnapshot
    ; Looking remains vanilla. Never enable controls owned by another mod.
    Game.DisablePlayerControls(acquiredMovement, acquiredFighting, acquiredCamSwitch, false, false, false, false, false)
    ; Cleanup can arrive while Disable is suspended or after its effect.
    if cleanupRequested || generation != leaseGeneration || activeGun != gun
        RollbackAcquire(movementSnapshot, fightingSnapshot, camSwitchSnapshot, cameraSnapshot, false)
        return -1
    endif
    int currentCamera = ReadCameraState()
    if cleanupRequested || generation != leaseGeneration || activeGun != gun || (currentCamera != 0 && currentCamera != 8 && currentCamera != 9)
        RollbackAcquire(movementSnapshot, fightingSnapshot, camSwitchSnapshot, cameraSnapshot, false)
        return -1
    endif
    if currentCamera != 0
        ; ForceFirstPerson is void. Acti separately waits for actual state 0.
        ; Mark intent before the native boundary so cancellation rolls back its effect.
        changedPerspective = cameraSnapshot == 8 || cameraSnapshot == 9
        Game.ForceFirstPerson()
    endif
    if cleanupRequested || generation != leaseGeneration || activeGun != gun
        RollbackAcquire(movementSnapshot, fightingSnapshot, camSwitchSnapshot, cameraSnapshot, changedPerspective)
        return -1
    endif
    acquiring = false
    return leaseGeneration
EndFunction

Function RollbackAcquire(bool restoreMovement, bool restoreFighting, bool restoreCamSwitch, int previousCamera, bool restorePerspective)
    acquiredMovement = false
    acquiredFighting = false
    acquiredCamSwitch = false
    changedPerspective = false
    savedCamera = -1
    activeGun = None
    Game.EnablePlayerControls(restoreMovement, restoreFighting, restoreCamSwitch, false, false, false, false, false)
    RestorePerspective(previousCamera, restorePerspective)
    FinishCancelledAcquire()
EndFunction

int Function ReadCameraState()
    ; Save/load cleanup must still release owned controls with a missing/old DLL.
    if SKSE.GetPluginVersion("AstraSight") < 33554432
        return -1
    endif
    return AstraSightNative.GetCameraState()
EndFunction

Function RestorePerspective(int previousCamera, bool restorePerspective)
    if !restorePerspective || (previousCamera != 8 && previousCamera != 9)
        return
    endif
    Actor operator = Game.GetPlayer()
    if operator == None || operator.IsDead() || Utility.IsInMenuMode()
        return
    endif
    ; Never replace a foreign special camera, death view, or menu transition.
    ; ForceThirdPerson restores the perspective, not the exact 8/9 camera variant.
    if ReadCameraState() == 0
        Game.ForceThirdPerson()
    endif
EndFunction

bool Function IsCurrent(AstraAsedioActi gun, int token)
    return gun != None && !acquiring && !releasing && !cleanupRequested && activeGun == gun && generation == token
EndFunction

Function FinishCancelledAcquire()
    acquiredMovement = false
    acquiredFighting = false
    acquiredCamSwitch = false
    savedCamera = -1
    changedPerspective = false
    activeGun = None
    cleanupRequested = false
    ; Last assignment: a replacement lease cannot overtake cancellation/rollback.
    acquiring = false
EndFunction

Function Release(AstraAsedioActi gun, int token)
    if acquiring && activeGun == gun && gun != None && (token < 0 || token == generation)
        RestoreControls()
        return
    endif
    if !IsCurrent(gun, token)
        return
    endif
    RestoreControls()
EndFunction

Function RestoreControls()
    if acquiring
        ; Acquire owns rollback. Do not race its pending native Disable with Enable.
        cleanupRequested = true
        generation += 1
        return
    endif
    if releasing
        return
    endif
    if activeGun == None && !acquiredMovement && !acquiredFighting && !acquiredCamSwitch && !changedPerspective
        return
    endif
    releasing = true
    bool restoreMovement = acquiredMovement
    bool restoreFighting = acquiredFighting
    bool restoreCamSwitch = acquiredCamSwitch
    int previousCamera = savedCamera
    bool restorePerspective = changedPerspective
    AstraAsedioActi oldGun = activeGun
    int oldToken = generation
    acquiredMovement = false
    acquiredFighting = false
    acquiredCamSwitch = false
    savedCamera = -1
    changedPerspective = false
    activeGun = None
    generation += 1
    ; Releasing stays held through native End. Saves without the DLL cannot
    ; invoke an unregistered function; global native load/revert also clears it.
    if oldGun != None && oldGun.UseSightCamera && SKSE.GetPluginVersion("AstraSight") >= 1
        AstraSightNative.EndSight(oldGun, oldToken)
    endif
    Game.EnablePlayerControls(restoreMovement, restoreFighting, restoreCamSwitch, false, false, false, false, false)
    RestorePerspective(previousCamera, restorePerspective)
    ; Hold the release guard until native restoration finishes.
    releasing = false
EndFunction

Function EmergencyCleanup()
    AstraAsedioActi gun = activeGun
    RestoreControls()
    if gun != None
        gun.EndSession()
    endif
EndFunction
