Scriptname AstraAsedioActi extends ObjectReference
AstraAsedioSession Property Session Auto
Weapon Property Launcher Auto
Ammo Property ShotAmmo Auto
Ammo Property SteelBolt Auto
Sound Property ShotSound Auto
GlobalVariable Property OcupadaGuardia Auto   ; v-guardia: 1 durante sesión o demo
float Property FireSeconds = 0.3 Auto
float Property ReleaseSeconds = 0.1 Auto
float Property ResetSeconds = 1.2 Auto
float Property CycleSeconds = 1.5 Auto
bool Property ContinuousFire = false Auto
float Property YawSpeed = 40.0 Auto
float Property PitchSpeed = 20.0 Auto
float Property PitchMin = -5.0 Auto
float Property PitchMax = 80.0 Auto
float Property PitchPivotHeight = 153.0 Auto
bool Property UseMouseAim = true Auto
bool Property UseSightCamera = true Auto
float Property OperatorDistance = 160.0 Auto
float Property OperatorHeight = 119.0 Auto
float Property OperatorVerticalTolerance = 64.0 Auto
float Property TickSeconds = 0.05 Auto
float Property PitchSign = -1.0 Auto
bool Property QALog = false Auto
string Property YawNode = "CTRL_GIRO_360" Auto
string Property PitchNode = "CTRL_ELEVACION" Auto
string Property OperatorNode = "OperatorNode" Auto
string Property VisualBoltNode = "VIROTE_VISUAL" Auto
float yaw = 0.0
float pitch = 0.0
float[] yawBase
float[] pitchBase
float[] yawMatrix
float[] pitchMatrix
float[] rootWorldMatrix
float[] muzzleWorldMatrix
float[] rootPosition
float[] muzzlePosition
Actor player
bool operating = false
float demoUntil = 0.0   ; v-guardia: activación bloqueada mientras corre la demo
bool updating = false
bool heldFire = true
bool repeatFire = false
bool heldMode = false
int repeatRevision = 0
bool heldLeft = false
bool heldRight = false
bool heldUp = false
bool heldDown = false
bool releaseLeft = false
bool releaseRight = false
bool releaseUp = false
bool releaseDown = false
bool inputPaused = true
bool firstUpdatePending = false
bool cameraEntryPending = false
bool nativeSightRequested = false
bool sightFreezePending = false
bool sightThawPending = false
bool endingSession = false
int sightFreezeGeneration = -1
float cameraEntryStartedAt = 0.0
float cameraEntryDeadline = 0.0
bool menuWasOpen = false
bool shotCommitted = false
bool needsReset = false
bool matricesReady = false
string matrixFailure = ""
string operatorFailure = ""
string shotFailure = ""
int activateKeyboard = -1
int activateMouse = -1
int fireKeyboard = -1
int fireMouse = -1
int modeKeyboard = -1
int modeMouse = -1
int generation = 0
int token = -1
int shotGeneration = -1
int phase = 0
int settleFrames = 0
float elapsed = 0.0
float lastTick = 0.0
float activateReadyAt = 0.0
float activateBlockedUntil = 0.0
; v09: counts Attack releases. A press compares it across its own native calls, so a
; release handled while the press is suspended can never be overwritten by that press.
int fireReleaseSerial = 0
; v09: the same for the Sprint mode key (a swallowed release blocked the next toggle).
int modeReleaseSerial = 0
; v09: after a menu the camera passes through tween/transition states while AstraSight
; keeps the sight suspended; until this real time those states are waited, not fatal.
float cameraGraceUntil = 0.0

Event OnInit()
    BlockActivation(true)
EndEvent

Event OnLoad()
    ; A save may restore pending OnUpdate before the player alias load callback.
    ; Invalidate that saved active session before any restored 3D can launch.
    if endingSession
        ; A saved suspended End has already cleared token/operating. Recover its
        ; lease through the quest and invalidate that stack before it can resume.
        endingSession = false
        generation += 1
        if Session != None
            Session.EmergencyCleanup()
        endif
    endif
    if operating || nativeSightRequested
        EndSession()
    endif
    endingSession = true
    int loadGeneration = generation
    BlockActivation(true)
    ; NetImmerse local changes are not serialized with the 3D. Reapply saved angles.
    bool captured = CaptureMatrices()
    if generation != loadGeneration || token != -1 || operating
        return
    endif
    if captured
        ApplyAim()
        if generation != loadGeneration || token != -1 || operating
            return
        endif
        NetImmerse.SetNodeScale(Self, VisualBoltNode, 1.0, false)
    else
        Debug.Trace("AstraAsedio OnLoad: " + matrixFailure)
    endif
    if generation == loadGeneration && token == -1 && !operating
        endingSession = false
    endif
EndEvent

Event OnUnload()
    EndSession()
EndEvent

; v-guardia: ciclo completo del guardia (torno, carga desde el atril, apuntado
; y disparo) horneado como NiControllerSequence "GuardiaCiclo" dentro de
; ballesta.nif por scripts/build_guardia.py. El jugador mira; la secuencia
; fuerza el estado de cada nodo que anima (incluido CTRL_GIRO_360 a rumbo 0).
Function PlayGuardiaDemo()
    if operating || endingSession
        return
    endif
    Debug.Trace("AstraAsedio demo del guardia (GuardiaCiclo)")
    if OcupadaGuardia
        OcupadaGuardia.SetValue(1)
        RegisterForSingleUpdate(26.0)
    endif
    bool demoStarted = PlayGamebryoAnimation("GuardiaCiclo", true)
    if !demoStarted
        Debug.Trace("AstraAsedio GUARDIA_CICLO_MISSING: la secuencia no está en el NIF (corré build_guardia.py)")
    endif
EndFunction

Event OnActivate(ObjectReference akActionRef)
    int activationGeneration = generation
    int activationToken = token
    Debug.Trace("AstraAsedio OnActivate ref=" + Self + " actor=" + akActionRef)
    if generation != activationGeneration || token != activationToken
        return
    endif
    bool actionIsPlayer = akActionRef == Game.GetPlayer()
    if generation != activationGeneration || token != activationToken
        return
    endif
    if !actionIsPlayer
        RejectActivation("ACTOR_NOT_PLAYER: solo el jugador puede manejarla.")
        return
    endif
    ; v-guardia: mientras corre la demo, el guardia manda en la máquina.
    if Utility.GetCurrentRealTime() < demoUntil
        return
    endif
    ; v-guardia: activar EN SIGILO = demo del guardia (ciclo completo, ~22 s).
    if Game.GetPlayer().IsSneaking()
        demoUntil = Utility.GetCurrentRealTime() + 24.0
        PlayGuardiaDemo()
        return
    endif
    if endingSession
        return
    endif
    if operating
        RequestExit("OnActivate")
        return
    endif
    ; Key/control events and OnActivate can describe the same physical press.
    ; A cancellation must not immediately reacquire controls from that press.
    float activationTime = Utility.GetCurrentRealTime()
    if operating || endingSession || generation != activationGeneration || token != activationToken
        return
    endif
    if activationTime < activateBlockedUntil
        return
    endif
    player = Game.GetPlayer()
    if SKSE.GetVersion() < 2
        RejectActivation("SKSE_MISSING: inicia Skyrim con SKSE64.")
        return
    endif
    ; API 3 supplies cached shot preflight; reject mixed version installations.
    ; v10: AstraSight 3.3 drives the tail sight camera and the front post; older DLLs are rejected.
    int nativeVersion = SKSE.GetPluginVersion("AstraSight")
    if operating || endingSession || generation != activationGeneration
        return
    endif
    if nativeVersion < 50528256
        RejectActivation("NATIVE_SIGHT_MISSING: instala AstraSight.dll 3.3.0 de esta versión.")
        return
    endif
    int nativeAPI = AstraSightNative.GetAPIVersion()
    if operating || endingSession || generation != activationGeneration
        return
    endif
    if nativeAPI != 3
        RejectActivation("NATIVE_API_MISMATCH: reinstala los archivos completos de esta versión.")
        return
    endif
    if UseSightCamera
        ; Never silently switch to legacy aim.
        if !AstraSightNative.IsAvailable()
            RejectActivation("NATIVE_SIGHT_UNAVAILABLE: la mira nativa no está disponible.")
            return
        endif
        if operating || endingSession || generation != activationGeneration
            return
        endif
    endif
    if Session == None
        RejectActivation("PROPERTY_SESSION_NONE: falta AstraAsedioSessionQuest.")
        return
    endif
    if Launcher == None
        RejectActivation("PROPERTY_LAUNCHER_NONE: falta el arma de disparo.")
        return
    endif
    if ShotAmmo == None
        RejectActivation("PROPERTY_SHOTAMMO_NONE: falta el virote nativo.")
        return
    endif
    if SteelBolt == None
        RejectActivation("PROPERTY_STEELBOLT_NONE: falta el virote de acero.")
        return
    endif
    if !Session.IsRunning()
        RejectActivation("SESSION_NOT_RUNNING: la quest de control no ha iniciado.")
        return
    endif
    if player.IsDead()
        RejectActivation("PLAYER_DEAD: no se puede operar durante la muerte.")
        return
    endif
    if !Game.IsLookingControlsEnabled()
        RejectActivation("LOOKING_CONTROLS_DISABLED: otro control ha bloqueado la mirada.")
        return
    endif
    int activationCamera = ReadCameraState()
    if activationCamera != 0 && activationCamera != 8 && activationCamera != 9
        RejectActivation("CAMERA_STATE_UNSUPPORTED: sal de la cámara especial para operar.")
        return
    endif
    if !CaptureMatrices()
        RejectActivation(matrixFailure)
        return
    endif
    if !NearOperator()
        RejectActivation(operatorFailure)
        return
    endif
    if operating || endingSession || generation != activationGeneration
        return
    endif
    int acquiredToken = Session.Acquire(Self)
    if operating || endingSession || generation != activationGeneration
        ; Acquire owns its rollback; a late result is scoped to that old lease.
        Session.Release(Self, acquiredToken)
        return
    endif
    token = acquiredToken
    if token < 0
        RejectActivation("SESSION_ENTRY_CANCELLED: entrada cancelada o sesión de control ocupada.")
        return
    endif
    generation += 1
    int entryGeneration = generation
    int entryToken = token
    operating = true
    if OcupadaGuardia
        OcupadaGuardia.SetValue(1)
    endif
    cameraEntryPending = true
    cameraEntryStartedAt = Utility.GetCurrentRealTime()
    ; Scheduled 0.05s ticks are requests, not a guaranteed engine frequency.
    cameraEntryDeadline = cameraEntryStartedAt + 1.5
    bool aligned = false
    if cameraEntryStartedAt == cameraEntryStartedAt && cameraEntryStartedAt >= 0.0 && cameraEntryStartedAt <= 1000000000.0
        aligned = AlignLookToWeapon(entryGeneration)
    endif
    if !operating || generation != entryGeneration || token != entryToken
        return
    endif
    if !aligned
        RejectActivation("CAMERA_ENTRY_FAILED: no se pudo alinear la mirada.")
        EndSession()
        return
    endif
    phase = 0
    if needsReset
        phase = 3
        elapsed = 0.0
        bool entryResetStarted = PlayGamebryoAnimation("Reset", true)
        if !operating || generation != entryGeneration || token != entryToken
            return
        endif
        if !entryResetStarted
            RejectShot("RESET_ANIMATION_FAILED: no se pudo iniciar la recarga.")
            EndSession()
            return
        endif
    endif
    ClearHeldInput(false)
    inputPaused = false
    menuWasOpen = false
    cameraGraceUntil = 0.0
    lastTick = Utility.GetCurrentRealTime()
    activateReadyAt = lastTick + 0.35
    firstUpdatePending = true
    RegisterMenus()
    RegisterInput()
    if !operating || generation != entryGeneration || token != entryToken
        return
    endif
    RegisterForSingleUpdate(TickSeconds)
    Debug.Trace("AstraAsedio session acquired token=" + token + " generation=" + generation)
    Debug.Notification("Astra: ratón apunta, ataque dispara, activar sale. Necesita virotes de acero.")
EndEvent

Function RejectActivation(string reason)
    ; Rejections are always visible, even when detailed shot QA is disabled.
    Debug.Trace("AstraAsedio activation rejected: " + reason)
    Debug.Notification("Astra: " + reason)
EndFunction

Function RegisterMenus()
    RegisterForMenu("InventoryMenu")
    RegisterForMenu("MagicMenu")
    RegisterForMenu("MapMenu")
    RegisterForMenu("Journal Menu")
    RegisterForMenu("TweenMenu")
    RegisterForMenu("Console")
    RegisterForMenu("Dialogue Menu")
    RegisterForMenu("Loading Menu")
    RegisterForMenu("BarterMenu")
    RegisterForMenu("ContainerMenu")
    RegisterForMenu("FavoritesMenu")
    RegisterForMenu("Sleep/Wait Menu")
    RegisterForMenu("MessageBoxMenu")
EndFunction

Function RegisterInput()
    ; Explicit keyboard/mouse lookup avoids GetMappedKey's auto-gamepad choice.
    activateKeyboard = Input.GetMappedKey("Activate", 0)
    activateMouse = Input.GetMappedKey("Activate", 1)
    fireKeyboard = Input.GetMappedKey("Right Attack/Block", 0)
    fireMouse = Input.GetMappedKey("Right Attack/Block", 1)
    modeKeyboard = Input.GetMappedKey("Sprint", 0)
    modeMouse = Input.GetMappedKey("Sprint", 1)
    RegisterForKey(203)
    RegisterForKey(205)
    RegisterForKey(200)
    RegisterForKey(208)
    RegisterMappedKey(activateKeyboard)
    RegisterMappedKey(activateMouse)
    RegisterMappedKey(fireKeyboard)
    RegisterMappedKey(fireMouse)
    RegisterMappedKey(modeKeyboard)
    RegisterMappedKey(modeMouse)
    RegisterForControl("Activate")
    RegisterForControl("Right Attack/Block")
    RegisterForControl("Sprint")
    Debug.Trace("AstraAsedio input registered generation=" + generation + " activate=" + activateKeyboard + "," + activateMouse + " fire=" + fireKeyboard + "," + fireMouse + " arrows=203,205,200,208")
EndFunction

Function RegisterMappedKey(int keyCode)
    if keyCode >= 0 && keyCode != 255 && keyCode < 266
        RegisterForKey(keyCode)
    endif
EndFunction

bool Function InputReady()
    int inputGeneration = generation
    int inputToken = token
    if !operating || cameraEntryPending
        return false
    endif
    bool inputMenuOpen = Utility.IsInMenuMode()
    if !operating || cameraEntryPending || generation != inputGeneration || token != inputToken || inputMenuOpen
        return false
    endif
    ; A fresh event can arrive after menu close but before the next aim tick.
    ; Resume here so that edge is accepted; do not discard its held state later.
    if inputPaused || menuWasOpen
        ResumeInput()
    endif
    bool resumedMenuOpen = Utility.IsInMenuMode()
    return operating && !cameraEntryPending && generation == inputGeneration && token == inputToken && !inputPaused && !menuWasOpen && !resumedMenuOpen
EndFunction

Function ResumeInput()
    ; PauseInput already cleared holds and marked keys requiring a release.
    ; Preserve those per-key gates while resetting the menu clock immediately.
    int resumeGeneration = generation
    int resumeToken = token
    inputPaused = false
    menuWasOpen = false
    float resumedAt = Utility.GetCurrentRealTime()
    ; v09: the camera grace counts from the first observation that the menu is gone, not from
    ; when it opened (a menu held open longer than the grace ended the session).
    if operating && token == resumeToken
        cameraGraceUntil = resumedAt + 3.0
    endif
    if !operating || generation != resumeGeneration || token != resumeToken || inputPaused || menuWasOpen
        return
    endif
    lastTick = resumedAt
EndFunction

Function ClearHeldInput(bool requireRelease)
    if requireRelease
        ; Only keys known to be held need to release. Fresh keys remain usable.
        releaseLeft = releaseLeft || heldLeft
        releaseRight = releaseRight || heldRight
        releaseUp = releaseUp || heldUp
        releaseDown = releaseDown || heldDown
    else
        releaseLeft = false
        releaseRight = false
        releaseUp = false
        releaseDown = false
    endif
    heldLeft = false
    heldRight = false
    heldUp = false
    heldDown = false
    heldFire = heldFire && requireRelease
    heldMode = heldMode && requireRelease
    StopRepeatFire()
EndFunction

Function StopRepeatFire()
    repeatFire = false
    repeatRevision += 1
EndFunction

Function RequestFireMode()
    int modeGeneration = generation
    int modeToken = token
    int pressReleaseSerial = modeReleaseSerial
    bool readyForMode = InputReady()
    if !operating || generation != modeGeneration || token != modeToken
        return
    endif
    bool releasedDuringPress = modeReleaseSerial != pressReleaseSerial
    if !readyForMode
        heldMode = !releasedDuringPress
        return
    endif
    if heldMode
        return
    endif
    heldMode = !releasedDuringPress
    ContinuousFire = !ContinuousFire
    StopRepeatFire()
    ; Require a fresh Attack press after every mode change.
    if ContinuousFire
        Debug.Notification("Astra: tiro continuo. Mantén Ataque; Sprint cambia el modo.")
    else
        Debug.Notification("Astra: tiro individual. Sprint cambia el modo.")
    endif
EndFunction

Function TryRepeatShot(int expectedGeneration)
    int repeatToken = token
    int expectedRevision = repeatRevision
    if !operating || generation != expectedGeneration || phase != 0 || !ContinuousFire || !repeatFire
        return
    endif
    bool repeatInputReady = InputReady()
    if !operating || generation != expectedGeneration || token != repeatToken || phase != 0 || !ContinuousFire || !repeatFire || repeatRevision != expectedRevision || !repeatInputReady
        return
    endif
    BeginShot(expectedGeneration, expectedRevision)
EndFunction

Function SetAimKey(int keyCode, bool isDown)
    if !operating
        return
    endif
    int keyGeneration = generation
    int keyToken = token
    bool aimInputReady = true
    if isDown
        aimInputReady = InputReady()
        if !operating || generation != keyGeneration || token != keyToken
            return
        endif
    endif
    if isDown && !aimInputReady
        if keyCode == 203
            releaseLeft = true
        elseif keyCode == 205
            releaseRight = true
        elseif keyCode == 200
            releaseUp = true
        elseif keyCode == 208
            releaseDown = true
        endif
        return
    endif
    if keyCode == 203
        if !isDown
            heldLeft = false
            releaseLeft = false
        elseif !releaseLeft
            heldLeft = true
        endif
    elseif keyCode == 205
        if !isDown
            heldRight = false
            releaseRight = false
        elseif !releaseRight
            heldRight = true
        endif
    elseif keyCode == 200
        if !isDown
            heldUp = false
            releaseUp = false
        elseif !releaseUp
            heldUp = true
        endif
    elseif keyCode == 208
        if !isDown
            heldDown = false
            releaseDown = false
        elseif !releaseDown
            heldDown = true
        endif
    endif
EndFunction

Event OnKeyDown(int keyCode)
    if !operating
        return
    endif
    int keyEventGeneration = generation
    int keyEventToken = token
    Debug.Trace("AstraAsedio OnKeyDown code=" + keyCode + " phase=" + phase + " generation=" + generation)
    if !operating || generation != keyEventGeneration || token != keyEventToken
        return
    endif
    if keyCode == activateKeyboard || keyCode == activateMouse
        RequestExit("OnKeyDown")
    elseif keyCode == fireKeyboard || keyCode == fireMouse
        RequestShot()
    elseif keyCode == modeKeyboard || keyCode == modeMouse
        RequestFireMode()
    else
        SetAimKey(keyCode, true)
    endif
EndEvent

Event OnKeyUp(int keyCode, float holdTime)
    if !operating
        return
    endif
    SetAimKey(keyCode, false)
    if keyCode == fireKeyboard || keyCode == fireMouse
        fireReleaseSerial += 1
        heldFire = false
        StopRepeatFire()
        ; Traced after the state change: the trace call may yield.
        Debug.Trace("AstraAsedio OnKeyUp code=" + keyCode + " phase=" + phase + " generation=" + generation)
    elseif keyCode == modeKeyboard || keyCode == modeMouse
        modeReleaseSerial += 1
        heldMode = false
    endif
EndEvent

Event OnControlDown(string control)
    if !operating
        return
    endif
    int controlEventGeneration = generation
    int controlEventToken = token
    Debug.Trace("AstraAsedio OnControlDown control=" + control + " phase=" + phase + " generation=" + generation)
    if !operating || generation != controlEventGeneration || token != controlEventToken
        return
    endif
    if control == "Activate"
        RequestExit("OnControlDown")
    elseif control == "Right Attack/Block"
        RequestShot()
    elseif control == "Sprint"
        RequestFireMode()
    endif
EndEvent

Event OnControlUp(string control, float holdTime)
    if operating && control == "Right Attack/Block"
        fireReleaseSerial += 1
        heldFire = false
        StopRepeatFire()
    elseif operating && control == "Sprint"
        modeReleaseSerial += 1
        heldMode = false
    endif
EndEvent

Function RequestExit(string inputSource)
    ; Exit is independent of OnUpdate, including when that callback is delayed.
    int exitGeneration = generation
    int exitToken = token
    if !operating
        return
    endif
    bool exitMenuOpen = Utility.IsInMenuMode()
    if !operating || generation != exitGeneration || token != exitToken || exitMenuOpen
        return
    endif
    float requestedExitAt = Utility.GetCurrentRealTime()
    if !operating || generation != exitGeneration || token != exitToken
        return
    endif
    if requestedExitAt < activateReadyAt
        return
    endif
    Debug.Trace("AstraAsedio cancel source=" + inputSource + " generation=" + generation)
    if !operating || generation != exitGeneration || token != exitToken
        return
    endif
    EndSession()
EndFunction

Function RequestShot()
    int requestGeneration = generation
    int requestToken = token
    ; v09: InputReady calls natives and may yield. A release handled meanwhile belongs to
    ; this press: never latch or arm the burst over it (v08 kept firing with the key up).
    int pressReleaseSerial = fireReleaseSerial
    bool shotInputReady = InputReady()
    if !operating || generation != requestGeneration || token != requestToken
        return
    endif
    bool releasedDuringPress = fireReleaseSerial != pressReleaseSerial
    if !shotInputReady
        if operating && !releasedDuringPress
            heldFire = true
        endif
        return
    endif
    if heldFire
        return
    endif
    ; Key and control delivery share one latch; failed/busy attempts also latch.
    ; The press still fires once if it was already released.
    heldFire = !releasedDuringPress
    repeatFire = ContinuousFire && !releasedDuringPress
    Debug.Trace("AstraAsedio fire input phase=" + phase + " generation=" + generation)
    if !operating || generation != requestGeneration || token != requestToken
        return
    endif
    if phase == 0
        BeginShot(requestGeneration)
    endif
EndFunction

Function PauseInput()
    int pauseToken = token
    inputPaused = true
    menuWasOpen = true
    ClearHeldInput(true)
    CancelPendingShot()
    if !operating || token != pauseToken || !inputPaused || !menuWasOpen
        return
    endif
    ; Cancellation may legitimately advance generation on the same lease.
    int pauseGeneration = generation
    float pausedAt = Utility.GetCurrentRealTime()
    if !operating || generation != pauseGeneration || token != pauseToken || !inputPaused || !menuWasOpen
        return
    endif
    lastTick = pausedAt
    ; v09: menus open and close through here; the camera may need a moment to return.
    cameraGraceUntil = pausedAt + 3.0
EndFunction

Function CancelPendingShot()
    if !shotCommitted && (phase == 1 || phase == 2)
        int cancelledGeneration = shotGeneration
        int cancelledToken = token
        generation += 1
        int cancellationGeneration = generation
        shotGeneration = -1
        needsReset = true
        phase = 3
        elapsed = 0.0
        settleFrames = 0
        ThawSight(cancelledGeneration, cancelledToken)
        if !operating || generation != cancellationGeneration || token != cancelledToken || phase != 3
            return
        endif
        Debug.Trace("AstraAsedio pending shot cancelled generation=" + generation)
        bool reset3DLoaded = Is3DLoaded()
        if !operating || generation != cancellationGeneration || token != cancelledToken || phase != 3
            return
        endif
        if reset3DLoaded
            bool cancelledResetStarted = PlayGamebryoAnimation("Reset", true)
            if !operating || generation != cancellationGeneration || token != cancelledToken || phase != 3
                return
            endif
            if !cancelledResetStarted
                RejectShot("RESET_ANIMATION_FAILED: cancelación del disparo.")
                EndSession()
            endif
        endif
    endif
EndFunction

Event OnMenuOpen(string menuName)
    if operating
        if cameraEntryPending
            EndSession()
        else
            PauseInput()
        endif
        Debug.Trace("AstraAsedio OnMenuOpen menu=" + menuName + " generation=" + generation)
    endif
EndEvent
Event OnMenuClose(string menuName)
    ; Menu-open state is retained until first active update, even if updates stop in menus.
    if operating
        PauseInput()
        Debug.Trace("AstraAsedio OnMenuClose menu=" + menuName + " generation=" + generation)
    endif
EndEvent


bool Function NearOperator()
    operatorFailure = ""
    if !Is3DLoaded() || !NetImmerse.HasNode(Self, OperatorNode, false)
        operatorFailure = "OPERATOR_NODE_UNAVAILABLE: la manivela aún no está cargada."
        return false
    endif
    if !NetImmerse.GetNodeWorldRotationMatrix(Self, "", rootWorldMatrix, false)
        operatorFailure = "OPERATOR_ROOT_MATRIX_FAILED: no se pudo leer la raíz de la ballesta."
        return false
    endif
    int i = 0
    while i < 9
        if rootWorldMatrix[i] != rootWorldMatrix[i] || Math.Abs(rootWorldMatrix[i]) > 1.05
            operatorFailure = "OPERATOR_ROOT_MATRIX_INVALID: transformación no finita."
            return false
        endif
        i += 1
    endwhile
    float rootScale = NetImmerse.GetNodeScale(Self, "", false)
    if rootScale != rootScale || rootScale <= 0.0 || rootScale > 100.0
        operatorFailure = "OPERATOR_ROOT_SCALE_INVALID: escala no válida."
        return false
    endif
    ; OperatorNode is the hand point. Actor position is the feet. Convert the
    ; measured 119-unit root-space height through the root rotation and scale.
    float height = OperatorHeight*rootScale
    float dx = player.GetPositionX() - NetImmerse.GetNodeWorldPositionX(Self, OperatorNode, false) + height*rootWorldMatrix[2]
    float dy = player.GetPositionY() - NetImmerse.GetNodeWorldPositionY(Self, OperatorNode, false) + height*rootWorldMatrix[5]
    float dz = player.GetPositionZ() - NetImmerse.GetNodeWorldPositionZ(Self, OperatorNode, false) + height*rootWorldMatrix[8]
    if dx != dx || dy != dy || dz != dz || Math.Abs(dx) > 1000000.0 || Math.Abs(dy) > 1000000.0 || Math.Abs(dz) > 1000000.0
        operatorFailure = "OPERATOR_POSITION_INVALID: posición no finita."
        return false
    endif
    ; v09: an in-range check leaves no message behind (v08 kept the out-of-range text after
    ; a successful activation and later attached it to unrelated sight failures).
    operatorFailure = ""
    bool inRange = dx*dx + dy*dy <= OperatorDistance*OperatorDistance && Math.Abs(dz) <= OperatorVerticalTolerance
    if !inRange
        operatorFailure = "OPERATOR_OUT_OF_RANGE: Acércate a la manivela. dx=" + dx + " dy=" + dy + " dz=" + dz
    endif
    return dx*dx + dy*dy <= OperatorDistance*OperatorDistance && Math.Abs(dz) <= OperatorVerticalTolerance
EndFunction

string Function SessionFailureReason()
    ; v09: in sight mode the operator range is checked natively; Papyrus never reads it there.
    if UseSightCamera
        return "NATIVE_SIGHT_NOT_READY: la mira nativa no está activa (cambió la cámara o el contexto)."
    endif
    if operatorFailure != ""
        return operatorFailure
    endif
    return "SESSION_CONTEXT_LOST: la sesión de control ya no es válida."
EndFunction

int Function ReadCameraState()
    ; Save/load cleanup must still release owned controls with a missing/old DLL.
    if SKSE.GetPluginVersion("AstraSight") < 33554432
        return -1
    endif
    return AstraSightNative.GetCameraState()
EndFunction

bool Function CanOperate(int expectedGeneration)
    if UseSightCamera
        ; Readiness includes game-thread life, camera, operator and loaded-node checks.
        return operating && !cameraEntryPending && generation == expectedGeneration && Session.IsCurrent(Self, token) && AstraSightNative.IsSightReady(Self, token)
    endif
    return operating && !cameraEntryPending && generation == expectedGeneration && Session.IsCurrent(Self, token) && ReadCameraState() == 0 && !player.IsDead() && NearOperator() && NetImmerse.HasNode(Self, "ProjectileNode", false) && NetImmerse.HasNode(Self, YawNode, false) && NetImmerse.HasNode(Self, PitchNode, false) && NetImmerse.HasNode(Self, VisualBoltNode, false) && (!UseSightCamera || AstraSightNative.IsSightReady(Self, token))
EndFunction

float Function HeadingFromVector(float vectorX, float vectorY, float fallback)
    float horizontal = Math.Sqrt(vectorX*vectorX + vectorY*vectorY)
    if horizontal < 0.00001
        return fallback
    endif
    float cosine = vectorY/horizontal
    if cosine > 1.0
        cosine = 1.0
    elseif cosine < -1.0
        cosine = -1.0
    endif
    float angle = Math.ACos(cosine)
    if vectorX < 0.0
        angle = 360.0 - angle
    endif
    if angle >= 360.0
        angle -= 360.0
    endif
    return angle
EndFunction

bool Function ReadAimRoot()
    if !NetImmerse.GetNodeWorldRotationMatrix(Self, "", rootWorldMatrix, false)
        return false
    endif
    int i = 0
    while i < 9
        if rootWorldMatrix[i] != rootWorldMatrix[i] || Math.Abs(rootWorldMatrix[i]) > 1.05
            return false
        endif
        i += 1
    endwhile
    return true
EndFunction

bool Function AlignLookToWeapon(int expectedGeneration)
    if !ReadAimRoot()
        return false
    endif
    float yc = Math.Cos(yaw)
    float ys = Math.Sin(yaw)
    float pc = Math.Cos(pitch)
    float ps = Math.Sin(pitch)
    float lx = ys*pc
    float ly = -yc*pc
    float wx = rootWorldMatrix[0]*lx + rootWorldMatrix[1]*ly + rootWorldMatrix[2]*ps
    float wy = rootWorldMatrix[3]*lx + rootWorldMatrix[4]*ly + rootWorldMatrix[5]*ps
    float wz = rootWorldMatrix[6]*lx + rootWorldMatrix[7]*ly + rootWorldMatrix[8]*ps
    if wx != wx || wy != wy || wz != wz || wz < -1.001 || wz > 1.001
        return false
    endif
    if wz > 1.0
        wz = 1.0
    elseif wz < -1.0
        wz = -1.0
    endif
    float heading = HeadingFromVector(wx, wy, player.GetAngleZ())
    float angleX = -Math.ASin(wz)
    bool currentLease = Session.IsCurrent(Self, token)
    bool menuOpen = Utility.IsInMenuMode()
    bool playerDead = player.IsDead()
    if !currentLease || menuOpen || playerDead || !operating || generation != expectedGeneration
        return false
    endif
    player.SetAngle(angleX, 0.0, heading)
    currentLease = Session.IsCurrent(Self, token)
    return currentLease && operating && generation == expectedGeneration
EndFunction

bool Function PollFirstPerson(int expectedGeneration)
    int entryToken = token
    float now = Utility.GetCurrentRealTime()
    int cameraState = ReadCameraState()
    bool currentLease = Session.IsCurrent(Self, entryToken)
    bool menuOpen = Utility.IsInMenuMode()
    bool playerDead = player.IsDead()
    if !operating || generation != expectedGeneration || token != entryToken
        return false
    endif
    if !currentLease
        EndSession()
        return false
    endif
    if menuOpen || playerDead || now != now || now < cameraEntryStartedAt || now >= cameraEntryDeadline || (cameraState != 0 && cameraState != 6 && cameraState != 8 && cameraState != 9)
        RejectActivation("CAMERA_ENTRY_FAILED: primera persona no disponible.")
        EndSession()
        return false
    endif
    if cameraState != 0
        return false
    endif
    if UseSightCamera
        if !nativeSightRequested
            ; Mark before the native boundary so exit can invalidate a pending Begin.
            nativeSightRequested = true
            bool accepted = AstraSightNative.BeginSight(Self, entryToken, yaw, pitch)
            if !operating || generation != expectedGeneration || token != entryToken
                ; Begin may have returned after End; old reference+token is safe.
                AstraSightNative.EndSight(Self, entryToken)
                return false
            endif
            if !accepted
                RejectActivation("NATIVE_SIGHT_BEGIN_FAILED: la mira rechazó la entrada.")
                EndSession()
                return false
            endif
        endif
        bool ready = AstraSightNative.IsSightReady(Self, entryToken)
        if !operating || generation != expectedGeneration || token != entryToken
            return false
        endif
        if !ready
            return false
        endif
        now = Utility.GetCurrentRealTime()
        menuOpen = Utility.IsInMenuMode()
        playerDead = player.IsDead()
        if !operating || generation != expectedGeneration || token != entryToken
            return false
        endif
        if menuOpen || playerDead || now != now || now < cameraEntryStartedAt || now >= cameraEntryDeadline
            RejectActivation("NATIVE_SIGHT_ENTRY_TIMEOUT: la mira no estuvo lista a tiempo.")
            EndSession()
            return false
        endif
    endif
    cameraEntryPending = false
    ResumeInput()
    return operating && generation == expectedGeneration
EndFunction

int Function SampleSightAimResult(int expectedGeneration, bool freeze)
    ; 1 = applied actual pose, 0 = a valid context changed, -1 = fatal native loss.
    int aimToken = token
    if !SightSampleCurrent(expectedGeneration, aimToken, freeze)
        return 0
    endif
    bool ready = AstraSightNative.IsSightReady(Self, aimToken)
    bool readinessMenu = Utility.IsInMenuMode()
    if !SightSampleCurrent(expectedGeneration, aimToken, freeze) || readinessMenu
        return 0
    endif
    if !ready
        return -1
    endif
    float[] snapshot = AstraSightNative.CaptureAim(Self, aimToken, freeze)
    ; Context precedes value validation: menus/attack may discard an empty old read.
    bool sampleMenu = Utility.IsInMenuMode()
    if !SightSampleCurrent(expectedGeneration, aimToken, freeze) || sampleMenu
        return 0
    endif
    if snapshot.Length != 2
        return -1
    endif
    float nextYaw = snapshot[0]
    float nextPitch = snapshot[1]
    ; v09: the native yaw is a double in [0,360); as float, 359.99999x rounds to exactly 360.0
    ; (v08 rejected the first sample at yaw 0 and ended the session). Same direction as 0.
    if nextYaw == 360.0
        nextYaw = 0.0
    endif
    if nextYaw != nextYaw || nextPitch != nextPitch || nextYaw < 0.0 || nextYaw >= 360.0 || nextPitch < PitchMin || nextPitch > PitchMax
        return -1
    endif
    bool currentLease = Session.IsCurrent(Self, aimToken)
    int cameraState = ReadCameraState()
    bool menuOpen = Utility.IsInMenuMode()
    if !SightSampleCurrent(expectedGeneration, aimToken, freeze) || menuOpen
        return 0
    endif
    if !currentLease
        return -1
    endif
    if cameraState != 0
        ; v09: AstraSight keeps the sight suspended while a menu camera (TweenMenu) owns the
        ; view; right after the menu the camera passes through tween/transition states.
        ; Wait for first person within the grace; outside it the loss is permanent.
        float graceNow = Utility.GetCurrentRealTime()
        if (cameraState == 6 || cameraState == 7) && graceNow < cameraGraceUntil
            return 0
        endif
        return -1
    endif
    yaw = nextYaw
    pitch = nextPitch
    ; Native owns all in-session aim/node writes. These are cache values only.
    return 1
EndFunction

bool Function SightSampleCurrent(int expectedGeneration, int expectedToken, bool freeze)
    if !operating || cameraEntryPending || generation != expectedGeneration || token != expectedToken || inputPaused || menuWasOpen
        return false
    endif
    if freeze
        return phase == 1 && shotGeneration == expectedGeneration && !shotCommitted
    endif
    return phase == 0 || phase == 3 || shotCommitted
EndFunction

Function ThawSight(int frozenGeneration, int frozenToken)
    if !UseSightCamera || !operating || token != frozenToken || sightFreezeGeneration != frozenGeneration
        return
    endif
    ; Block a new freeze while a suspended old unfreeze finishes on this token.
    sightThawPending = true
    if !sightFreezePending
        sightFreezeGeneration = -1
    endif
    bool thawed = AstraSightNative.SetFrozen(Self, frozenToken, false)
    if !operating || token != frozenToken
        return
    endif
    sightThawPending = false
    if !thawed
        RejectShot("NATIVE_SIGHT_THAW_FAILED: se perdió la mira nativa.")
        EndSession()
    endif
EndFunction

bool Function SampleLookAim(int expectedGeneration)
    return SampleLookAimResult(expectedGeneration) == 1
EndFunction

int Function SampleLookAimResult(int expectedGeneration)
    ; 1 applied, 0 discarded after a valid context change, -1 invalid sample.
    ; A nested attack can freeze aim while a periodic native read is pending.
    if !operating || cameraEntryPending || generation != expectedGeneration || inputPaused || menuWasOpen || Utility.IsInMenuMode() || (phase != 0 && phase != 3 && !shotCommitted)
        return 0
    endif
    float heading = player.GetAngleZ()
    float angleX = player.GetAngleX()
    if heading != heading || angleX != angleX || Math.Abs(heading) > 720.0 || Math.Abs(angleX) > 360.0 || !ReadAimRoot()
        return -1
    endif
    ; Skyrim may report wrapped angle X. Positive camera X looks down.
    while angleX > 180.0
        angleX -= 360.0
    endwhile
    while angleX <= -180.0
        angleX += 360.0
    endwhile
    float horizontal = Math.Cos(-angleX)
    float wx = Math.Sin(heading)*horizontal
    float wy = Math.Cos(heading)*horizontal
    float wz = Math.Sin(-angleX)
    ; Row-major R transpose maps world look into the reference's local frame.
    float lx = rootWorldMatrix[0]*wx + rootWorldMatrix[3]*wy + rootWorldMatrix[6]*wz
    float ly = rootWorldMatrix[1]*wx + rootWorldMatrix[4]*wy + rootWorldMatrix[7]*wz
    float lz = rootWorldMatrix[2]*wx + rootWorldMatrix[5]*wy + rootWorldMatrix[8]*wz
    float lengthSquared = lx*lx + ly*ly + lz*lz
    if lengthSquared != lengthSquared || lengthSquared < 0.99 || lengthSquared > 1.01
        return -1
    endif
    float vectorMagnitude = Math.Sqrt(lengthSquared)
    lx = lx/vectorMagnitude
    ly = ly/vectorMagnitude
    lz = lz/vectorMagnitude
    if lz > 1.0
        lz = 1.0
    elseif lz < -1.0
        lz = -1.0
    endif
    float nextYaw = HeadingFromVector(lx, -ly, yaw)
    float nextPitch = Math.ASin(lz)
    if nextPitch > PitchMax
        nextPitch = PitchMax
    elseif nextPitch < PitchMin
        nextPitch = PitchMin
    endif
    ; Every native read/math call may yield. Revalidate the scalar generation
    ; after the final external checks, before publishing either aim angle.
    bool currentLease = Session.IsCurrent(Self, token)
    int cameraState = ReadCameraState()
    bool menuOpen = Utility.IsInMenuMode()
    if !operating || generation != expectedGeneration || cameraEntryPending
        return 0
    endif
    if !currentLease
        return -1
    endif
    if menuOpen || inputPaused || menuWasOpen
        return 0
    endif
    if cameraState != 0
        return -1
    endif
    if phase != 0 && phase != 3 && !shotCommitted
        return 0
    endif
    yaw = nextYaw
    pitch = nextPitch
    ApplyAim()
    return 1
EndFunction

bool Function CaptureMatrices()
    matrixFailure = ""
    if SKSE.GetVersion() < 2
        matrixFailure = "SKSE_MISSING: inicia Skyrim con SKSE64."
        return false
    endif
    if !Is3DLoaded()
        matrixFailure = "MODEL_NOT_LOADED: la malla aún no está cargada."
        return false
    endif
    if !NetImmerse.HasNode(Self, YawNode, false)
        matrixFailure = "NODE_MISSING: " + YawNode
        return false
    endif
    if !NetImmerse.HasNode(Self, PitchNode, false)
        matrixFailure = "NODE_MISSING: " + PitchNode
        return false
    endif
    if !NetImmerse.HasNode(Self, VisualBoltNode, false)
        matrixFailure = "NODE_MISSING: " + VisualBoltNode
        return false
    endif
    if !NetImmerse.HasNode(Self, "ProjectileNode", false)
        matrixFailure = "NODE_MISSING: ProjectileNode"
        return false
    endif
    if !NetImmerse.HasNode(Self, OperatorNode, false)
        matrixFailure = "NODE_MISSING: " + OperatorNode
        return false
    endif
    ; NIF rotations are identity in the packaged contract; bases stay per reference.
    ; Comparing an array to None emits a failing None -> Float[] cast in
    ; Skyrim. The compiler reuses that poisoned temp for every ArrayCreate.
    ; Track successful capture with a scalar and leave typed arrays intact.
    if !matricesReady
        yawBase = new float[9]
        pitchBase = new float[9]
        yawMatrix = new float[9]
        pitchMatrix = new float[9]
        rootWorldMatrix = new float[9]
        muzzleWorldMatrix = new float[9]
        rootPosition = new float[3]
        muzzlePosition = new float[3]
        if !NetImmerse.GetNodeLocalRotationMatrix(Self, YawNode, yawBase, false) || !NetImmerse.GetNodeLocalRotationMatrix(Self, PitchNode, pitchBase, false)
            matrixFailure = "MATRIX_READ_FAILED: no se pudieron capturar los controles de giro."
            return false
        endif
        matricesReady = true
    endif
    return true
EndFunction

Function ApplyAim()
    int applyGeneration = generation
    if UseSightCamera && operating
        return
    endif
    float yc = Math.Cos(yaw)
    float ys = Math.Sin(yaw)
    float pc = Math.Cos(pitch*PitchSign)
    float ps = Math.Sin(pitch*PitchSign)
    ; Rz(yaw) * measured base; Rx(sign*pitch) * measured base, row-major SKSE matrix.
    int j = 0
    while j < 3
        yawMatrix[j] = yc*yawBase[j] - ys*yawBase[j+3]
        yawMatrix[j+3] = ys*yawBase[j] + yc*yawBase[j+3]
        yawMatrix[j+6] = yawBase[j+6]
        pitchMatrix[j] = pitchBase[j]
        pitchMatrix[j+3] = pc*pitchBase[j+3] - ps*pitchBase[j+6]
        pitchMatrix[j+6] = ps*pitchBase[j+3] + pc*pitchBase[j+6]
        j += 1
    endwhile
    if UseSightCamera && (operating || generation != applyGeneration)
        return
    endif
    NetImmerse.SetNodeLocalRotationMatrix(Self, YawNode, yawMatrix, false)
    if UseSightCamera && (operating || generation != applyGeneration)
        return
    endif
    NetImmerse.SetNodeLocalRotationMatrix(Self, PitchNode, pitchMatrix, false)
EndFunction

Event OnUpdate()
    ; v-guardia: la ventana de la demo (22 s) se cierra aquí; los ticks de
    ; sesión no se tocan (cuando operating es true esta rama nunca corre).
    if !operating && !endingSession && OcupadaGuardia && OcupadaGuardia.GetValue() == 1 \
        && Utility.GetCurrentRealTime() >= demoUntil
        OcupadaGuardia.SetValue(0)
    endif
    if updating || !operating
        return
    endif
    updating = true
    int currentGeneration = generation
    int currentPhase = phase
    int currentToken = token
    if firstUpdatePending
        firstUpdatePending = false
        Debug.Trace("AstraAsedio first OnUpdate token=" + token + " generation=" + generation + " phase=" + phase)
    endif
    float now = Utility.GetCurrentRealTime()
    ; This clock can return after exit/re-entry. Never publish it into B's timer.
    if !operating || generation != currentGeneration || token != currentToken
        updating = false
        if operating && token == currentToken
            RegisterForSingleUpdate(TickSeconds)
        endif
        return
    endif
    float dt = now - lastTick
    lastTick = now
    if cameraEntryPending
        if !PollFirstPerson(currentGeneration)
            updating = false
            if operating
                RegisterForSingleUpdate(TickSeconds)
            endif
            return
        endif
        dt = 0.0
    endif
    if Utility.IsInMenuMode()
        if !inputPaused
            PauseInput()
        endif
        updating = false
        if operating
            RegisterForSingleUpdate(TickSeconds)
        endif
        return
    endif
    if menuWasOpen
        ResumeInput()
        dt = 0.0
    endif
    bool operationValid = CanOperate(currentGeneration)
    bool operationMenu = Utility.IsInMenuMode()
    if !operating || generation != currentGeneration || token != currentToken
        updating = false
        if operating && token == currentToken
            ; v09: a cancelled shot changes the generation on the same lease; keep ticking.
            RegisterForSingleUpdate(TickSeconds)
        endif
        return
    endif
    if operationMenu || inputPaused || menuWasOpen
        if !inputPaused
            PauseInput()
        endif
        updating = false
        if operating
            RegisterForSingleUpdate(TickSeconds)
        endif
        return
    endif
    if !operationValid
        Debug.Trace("AstraAsedio operation invalid generation=" + currentGeneration + " reason=" + SessionFailureReason())
        if UseSightCamera
            RejectShot("NATIVE_SIGHT_OPERATION_INVALID: se perdió la mira o su contexto.")
        endif
        updating = false
        EndSession()
        return
    endif
    if UseSightCamera
        bool sightReady = AstraSightNative.IsSightReady(Self, currentToken)
        bool nativeMenuOpen = Utility.IsInMenuMode()
        if !operating || generation != currentGeneration || token != currentToken
            updating = false
            if operating && token == currentToken
                ; v09: a cancelled shot changes the generation on the same lease; keep ticking.
                RegisterForSingleUpdate(TickSeconds)
            endif
            return
        endif
        if nativeMenuOpen || inputPaused || menuWasOpen
            if !inputPaused
                PauseInput()
            endif
            updating = false
            if operating
                RegisterForSingleUpdate(TickSeconds)
            endif
            return
        endif
        if !sightReady
            RejectShot("NATIVE_SIGHT_NOT_READY: se perdió la mira nativa.")
            updating = false
            EndSession()
            return
        endif
    endif
    float dtCycle = dt
    if dtCycle < 0.0
        dtCycle = 0.0
    endif
    if dt > 0.15
        dt = 0.15
    elseif dt < 0.0
        dt = 0.0
    endif
    ; Freeze the shot direction until native Release; reload can be aimed.
    if phase == 0 || shotCommitted || phase == 3
        UpdateAim(dt)
    endif
    ; Reads/ApplyAim can yield to attack or menus. That old tick must neither
    ; count as a settle frame for a new shot nor advance a paused cycle clock.
    bool menuAfterAim = Utility.IsInMenuMode()
    if !operating || generation != currentGeneration || phase != currentPhase || inputPaused || menuWasOpen || menuAfterAim
        if operating && generation == currentGeneration && menuAfterAim && !inputPaused
            PauseInput()
        endif
        updating = false
        if operating
            RegisterForSingleUpdate(TickSeconds)
        endif
        return
    endif
    if phase == 1 && !sightFreezePending && !sightThawPending
        ; Native CaptureAim already captured an applied coherent world pose.
        ; Legacy still requires three separate world-transform settling ticks.
        settleFrames += 1
        if UseSightCamera || settleFrames >= 3
            bool shotPrepared = PrepareShotAnimation(shotGeneration)
            if !operating || generation != currentGeneration || token != currentToken || phase != 1 || inputPaused || menuWasOpen
                updating = false
                if operating
                    RegisterForSingleUpdate(TickSeconds)
                endif
                return
            endif
            if shotPrepared
                phase = 2
                elapsed = 0.0
                if QALog
                    Debug.Trace("AstraAsedio phase Fire generation=" + generation)
                endif
            else
                StopRepeatFire()
                RejectShot(shotFailure)
                ThawSight(currentGeneration, currentToken)
                if !operating || generation != currentGeneration || token != currentToken || phase != 1
                    updating = false
                    if operating && token == currentToken
                        RegisterForSingleUpdate(TickSeconds)
                    endif
                    return
                endif
                phase = 0
                needsReset = false
            endif
        endif
    elseif phase == 2
        elapsed += dtCycle
        if elapsed >= ReleaseSeconds && !shotCommitted
            CommitShot(shotGeneration)
            if !operating || generation != currentGeneration
                updating = false
                if operating && token == currentToken
                    RegisterForSingleUpdate(TickSeconds)
                endif
                return
            endif
        endif
        if elapsed >= FireSeconds
            if !operating || generation != currentGeneration || token != currentToken || phase != 2 || inputPaused || menuWasOpen
                updating = false
                if operating && token == currentToken
                    RegisterForSingleUpdate(TickSeconds)
                endif
                return
            endif
            bool cycleResetStarted = PlayGamebryoAnimation("Reset", true)
            ; A suspended Reset may return after exit/re-entry or cancellation.
            ; Neither success nor failure belongs to a replacement shot/lease.
            if !operating || generation != currentGeneration || token != currentToken || phase != 2 || inputPaused || menuWasOpen
                updating = false
                if operating && token == currentToken
                    RegisterForSingleUpdate(TickSeconds)
                endif
                return
            endif
            if cycleResetStarted
                phase = 3
                elapsed = 0.0
            else
                RejectShot("RESET_ANIMATION_FAILED: fin del disparo.")
                updating = false
                EndSession()
                return
            endif
        endif
    elseif phase == 3
        elapsed += dtCycle
        if elapsed >= ResetSeconds
            NetImmerse.SetNodeScale(Self, VisualBoltNode, 1.0, false)
            bool reloadMenuOpen = Utility.IsInMenuMode()
            ; Visual restoration can return after a new shot/lease or menu.
            ; Only the same active reload may publish completion state.
            if !operating || generation != currentGeneration || token != currentToken || phase != 3 || inputPaused || menuWasOpen || reloadMenuOpen
                if operating && generation == currentGeneration && token == currentToken && reloadMenuOpen && !inputPaused
                    PauseInput()
                endif
                updating = false
                if operating && token == currentToken
                    RegisterForSingleUpdate(TickSeconds)
                endif
                return
            endif
            phase = 0
            needsReset = false
            shotCommitted = false
            TryRepeatShot(currentGeneration)
        endif
    endif
    updating = false
    if operating
        RegisterForSingleUpdate(TickSeconds)
    endif
EndEvent

Function UpdateAim(float dt)
        if UseSightCamera
            int sightGeneration = generation
            int sightToken = token
            int sightResult = SampleSightAimResult(sightGeneration, false)
            if sightResult < 0 && operating && generation == sightGeneration && token == sightToken
                RejectShot("NATIVE_SIGHT_SAMPLE_FAILED: se perdió la mira nativa.")
                EndSession()
            endif
            return
        endif
        if UseMouseAim
            int aimGeneration = generation
            int sampleResult = SampleLookAimResult(aimGeneration)
            if sampleResult < 0 && operating && generation == aimGeneration
                EndSession()
            endif
            return
        endif
        if heldLeft
            yaw += YawSpeed*dt
        endif
        if heldRight
            yaw -= YawSpeed*dt
        endif
        if heldUp
            pitch += PitchSpeed*dt
        endif
        if heldDown
            pitch -= PitchSpeed*dt
        endif
        if pitch > PitchMax
            pitch = PitchMax
        elseif pitch < PitchMin
            pitch = PitchMin
        endif
        if yaw >= 360.0
            yaw -= 360.0
        elseif yaw < 0.0
            yaw += 360.0
        endif
        ApplyAim()
EndFunction

Function BeginShot(int expectedGeneration, int expectedRepeatRevision = -1)
    int expectedToken = token
    bool shotSessionValid = InputReady() && CanOperate(expectedGeneration)
    bool shotMenuOpen = Utility.IsInMenuMode()
    if !operating || generation != expectedGeneration || token != expectedToken
        return
    endif
    if expectedRepeatRevision >= 0 && (!ContinuousFire || !repeatFire || repeatRevision != expectedRepeatRevision)
        return
    endif
    if shotMenuOpen || inputPaused || menuWasOpen
        return
    endif
    if !shotSessionValid
        RejectShot("SHOT_SESSION_INVALID: " + SessionFailureReason())
        if UseSightCamera
            EndSession()
        endif
        return
    endif
    ; A click between scheduled ticks must freeze the current mouse direction.
    if !UseSightCamera && UseMouseAim && !SampleLookAim(expectedGeneration)
        RejectShot("SHOT_AIM_SAMPLE_FAILED: mirada no disponible o sesión cancelada.")
        return
    endif
    int shotAvailableAmmo = player.GetItemCount(SteelBolt)
    if !operating || generation != expectedGeneration || token != expectedToken || phase != 0
        return
    endif
    if shotAvailableAmmo < 1
        StopRepeatFire()
        RejectShot("SHOT_NO_STEEL_BOLT: necesita un virote de acero.")
        return
    endif
    ; Look/matrix/ammo natives may yield to exit, menus, or another shot.
    if !operating || generation != expectedGeneration || token != expectedToken || cameraEntryPending || inputPaused || menuWasOpen || phase != 0 || sightFreezePending || sightThawPending
        RejectShot("SHOT_STALE_BEFORE_FREEZE: sesión cancelada durante el apuntado.")
        return
    endif
    if expectedRepeatRevision >= 0 && (!ContinuousFire || !repeatFire || repeatRevision != expectedRepeatRevision)
        return
    endif
    shotGeneration = expectedGeneration
    shotCommitted = false
    needsReset = true
    settleFrames = 0
    phase = 1
    if UseSightCamera
        ; Reserve the shot before the native call; nested Attack cannot freeze twice.
        sightFreezeGeneration = expectedGeneration
        sightFreezePending = true
        int freezeResult = SampleSightAimResult(expectedGeneration, true)
        if !operating || token != expectedToken || sightFreezeGeneration != expectedGeneration
            return
        endif
        sightFreezePending = false
        if freezeResult == 0 || generation != expectedGeneration || phase != 1
            ThawSight(expectedGeneration, expectedToken)
            ; v09: a freeze discarded with nothing else taking the shot (the camera still returning
            ; from a menu) must not leave phase 1 behind: the next tick would fire unfrozen.
            if operating && token == expectedToken && generation == expectedGeneration && phase == 1 && !shotCommitted && shotGeneration == expectedGeneration
                phase = 0
                needsReset = false
                shotGeneration = -1
            endif
            return
        endif
        if freezeResult < 0
            RejectShot("NATIVE_SIGHT_FREEZE_FAILED: no se pudo fijar el disparo.")
            EndSession()
            return
        endif
    endif
    if QALog
        Debug.Trace("AstraAsedio phase settle yaw=" + yaw + " pitch=" + pitch + " generation=" + generation)
    endif
EndFunction

Function RejectShot(string reason)
    Debug.Trace("AstraAsedio shot rejected: " + reason)
    Debug.Notification("Astra: " + reason)
EndFunction

bool Function PrepareShotAnimation(int expectedGeneration)
    if !InputReady() || !CanOperate(expectedGeneration)
        shotFailure = "SHOT_SESSION_INVALID: " + SessionFailureReason()
        return false
    endif
    if !UseSightCamera && player.GetItemCount(SteelBolt) < 1
        shotFailure = "SHOT_NO_STEEL_BOLT: necesita un virote de acero."
        return false
    endif
    bool transformReady = ShotTransformReady()
    if !operating || generation != expectedGeneration || phase != 1 || inputPaused || menuWasOpen
        return false
    endif
    if !transformReady
        return false
    endif
    if !PlayGamebryoAnimation("Fire", true)
        shotFailure = "FIRE_ANIMATION_FAILED: PlayGamebryoAnimation devolvió false."
        return false
    endif
    return true
EndFunction

bool Function ShotTransformReady()
    shotFailure = ""
    if UseSightCamera
        ; API 3 checks a frozen snapshot only; no scene access on the VM tasklet.
        if !AstraSightNative.ValidateShot(Self, token, yaw, pitch, PitchPivotHeight)
            shotFailure = "SHOT_NATIVE_PREFLIGHT_FAILED: pose congelada o boca no válida."
            return false
        endif
        return true
    endif
    ; Verify the render-task update, including any reference rotation/scale.
    ; SKSE matrix values are row-major; projectile forward is its local +Y.
    if !NetImmerse.GetNodeWorldRotationMatrix(Self, "", rootWorldMatrix, false) || !NetImmerse.GetNodeWorldRotationMatrix(Self, "ProjectileNode", muzzleWorldMatrix, false)
        shotFailure = "SHOT_MATRIX_READ_FAILED: raíz o ProjectileNode."
        return false
    endif
    if !NetImmerse.GetNodeWorldPosition(Self, "", rootPosition, false) || !NetImmerse.GetNodeWorldPosition(Self, "ProjectileNode", muzzlePosition, false)
        shotFailure = "SHOT_POSITION_READ_FAILED: raíz o ProjectileNode."
        return false
    endif
    int i = 0
    while i < 9
        if rootWorldMatrix[i] != rootWorldMatrix[i] || muzzleWorldMatrix[i] != muzzleWorldMatrix[i] || Math.Abs(rootWorldMatrix[i]) > 1.05 || Math.Abs(muzzleWorldMatrix[i]) > 1.05
            shotFailure = "SHOT_MATRIX_INVALID: índice=" + i
            return false
        endif
        i += 1
    endwhile
    i = 0
    while i < 3
        if rootPosition[i] != rootPosition[i] || muzzlePosition[i] != muzzlePosition[i] || Math.Abs(rootPosition[i]) > 1000000.0 || Math.Abs(muzzlePosition[i]) > 1000000.0
            shotFailure = "SHOT_POSITION_INVALID: índice=" + i
            return false
        endif
        i += 1
    endwhile
    float yc = Math.Cos(yaw)
    float ys = Math.Sin(yaw)
    float pc = Math.Cos(pitch)
    float ps = Math.Sin(pitch)
    float lx = ys*pc
    float ly = -yc*pc
    float lz = ps
    float ex = rootWorldMatrix[0]*lx + rootWorldMatrix[1]*ly + rootWorldMatrix[2]*lz
    float ey = rootWorldMatrix[3]*lx + rootWorldMatrix[4]*ly + rootWorldMatrix[5]*lz
    float ez = rootWorldMatrix[6]*lx + rootWorldMatrix[7]*ly + rootWorldMatrix[8]*lz
    float directionDot = ex*muzzleWorldMatrix[1] + ey*muzzleWorldMatrix[4] + ez*muzzleWorldMatrix[7]
    float directionLength = muzzleWorldMatrix[1]*muzzleWorldMatrix[1] + muzzleWorldMatrix[4]*muzzleWorldMatrix[4] + muzzleWorldMatrix[7]*muzzleWorldMatrix[7]
    if directionDot < 0.999 || Math.Abs(directionLength - 1.0) > 0.002
        shotFailure = "SHOT_DIRECTION_MISMATCH: dot=" + directionDot + " length=" + directionLength + " yaw=" + yaw + " pitch=" + pitch
        return false
    endif
    ; Packaged NIF pivot total is explicit in VMAD (v04: 153 units),
    ; ProjectileNode (0,-224,19.6) under pitch, local Rz180.
    ly = -224.0*pc + 19.6*ps
    lx = -ly*ys
    lz = PitchPivotHeight + 224.0*ps + 19.6*pc
    ly = ly*yc
    float rootScale = NetImmerse.GetNodeScale(Self, "", false)
    if rootScale != rootScale || rootScale <= 0.0 || rootScale > 100.0
        shotFailure = "SHOT_ROOT_SCALE_INVALID: scale=" + rootScale
        return false
    endif
    ex = rootPosition[0] + rootScale*(rootWorldMatrix[0]*lx + rootWorldMatrix[1]*ly + rootWorldMatrix[2]*lz)
    ey = rootPosition[1] + rootScale*(rootWorldMatrix[3]*lx + rootWorldMatrix[4]*ly + rootWorldMatrix[5]*lz)
    ez = rootPosition[2] + rootScale*(rootWorldMatrix[6]*lx + rootWorldMatrix[7]*ly + rootWorldMatrix[8]*lz)
    float dx = ex - muzzlePosition[0]
    float dy = ey - muzzlePosition[1]
    float dz = ez - muzzlePosition[2]
    float positionError = dx*dx + dy*dy + dz*dz
    if positionError > 4.0
        shotFailure = "SHOT_POSITION_MISMATCH: squaredError=" + positionError + " dx=" + dx + " dy=" + dy + " dz=" + dz
        return false
    endif
    return true
EndFunction

Function CommitShot(int expectedGeneration)
    int committedToken = token
    if shotCommitted
        return
    endif
    bool commitSessionValid = InputReady() && CanOperate(expectedGeneration)
    bool commitMenuOpen = Utility.IsInMenuMode()
    if !operating || generation != expectedGeneration || token != committedToken
        return
    endif
    if commitMenuOpen || inputPaused || menuWasOpen
        PauseInput()
        return
    endif
    if !commitSessionValid
        RejectShot("SHOT_CANCELLED_BEFORE_COMMIT: " + SessionFailureReason())
        EndSession()
        return
    endif
    int availableAmmo = player.GetItemCount(SteelBolt)
    if !operating || generation != expectedGeneration || token != committedToken
        return
    endif
    if availableAmmo < 1
        RejectShot("SHOT_NO_STEEL_BOLT: antes del lanzamiento.")
        EndSession()
        return
    endif
    bool commitTransformReady = ShotTransformReady()
    if !operating || generation != expectedGeneration || token != committedToken
        return
    endif
    if !commitTransformReady
        RejectShot(shotFailure)
        EndSession()
        return
    endif
    ; External preflight calls can yield. Revalidate only local scalar state
    ; after those calls, before claiming the ammo/native-launch transaction.
    if !operating || generation != expectedGeneration || shotGeneration != expectedGeneration || phase != 2 || shotCommitted || inputPaused || menuWasOpen
        RejectShot("SHOT_STALE_AFTER_PREFLIGHT: el disparo se canceló durante la comprobación.")
        return
    endif
    ; From this point the shot is committed: removal and native Fire are
    ; external operations, not an atomic Papyrus block or a success boolean.
    shotCommitted = true
    player.RemoveItem(SteelBolt, 1, true)
    Launcher.Fire(Self, ShotAmmo)
    if operating && token == committedToken && generation == expectedGeneration && phase == 2 && shotCommitted
        ThawSight(expectedGeneration, committedToken)
    endif
    ; Cosmetic work follows launch and never hides the bolt in a newer session.
    if operating && generation == expectedGeneration && phase == 2
        NetImmerse.SetNodeScale(Self, VisualBoltNode, 0.0, false)
    endif
    ; v08: Weapon.Fire from a reference plays no attack sound; one cue per launched bolt.
    ; After thaw and hiding the visual bolt: Play is a native call and may cost a frame,
    ; which must not keep the sight frozen or show the visual and launched bolts together.
    if ShotSound
        ShotSound.Play(Self)
    endif
    if QALog && !UseSightCamera
        Debug.Trace("AstraAsedio Fire committed yaw=" + yaw + " pitch=" + pitch + " generation=" + generation + " muzzle=" + muzzlePosition[0] + "," + muzzlePosition[1] + "," + muzzlePosition[2] + " forward=" + muzzleWorldMatrix[1] + "," + muzzleWorldMatrix[4] + "," + muzzleWorldMatrix[7])
    endif
EndFunction

Function EndSession()
    if endingSession
        return
    endif
    endingSession = true
    int oldToken = token
    bool restoreSightAim = UseSightCamera && nativeSightRequested && matricesReady
    int oldPhase = phase
    bool oldCommitted = shotCommitted
    if phase > 0
        needsReset = true
    endif
    operating = false
    if OcupadaGuardia && Utility.GetCurrentRealTime() >= demoUntil
        OcupadaGuardia.SetValue(0)
    endif
    cameraEntryPending = false
    cameraGraceUntil = 0.0
    firstUpdatePending = false
    generation += 1
    int cleanupGeneration = generation
    token = -1
    nativeSightRequested = false
    sightFreezePending = false
    sightThawPending = false
    sightFreezeGeneration = -1
    shotGeneration = -1
    phase = 0
    shotCommitted = false
    updating = false
    inputPaused = true
    menuWasOpen = false
    ClearHeldInput(true)
    Debug.Trace("AstraAsedio EndSession token=" + oldToken + " generation=" + cleanupGeneration + " phase=" + oldPhase + " committed=" + oldCommitted)
    if !CleanupCurrent(cleanupGeneration)
        return
    endif
    float exitTime = Utility.GetCurrentRealTime()
    if !CleanupCurrent(cleanupGeneration)
        return
    endif
    activateBlockedUntil = exitTime + 0.35
    UnregisterForUpdate()
    if !CleanupCurrent(cleanupGeneration)
        return
    endif
    UnregisterForAllKeys()
    if !CleanupCurrent(cleanupGeneration)
        return
    endif
    UnregisterForAllControls()
    if !CleanupCurrent(cleanupGeneration)
        return
    endif
    UnregisterForAllMenus()
    if !CleanupCurrent(cleanupGeneration)
        return
    endif
    if UseSightCamera && oldToken > 0 && SKSE.GetPluginVersion("AstraSight") >= 1
        AstraSightNative.EndSight(Self, oldToken)
    endif
    if Session != None
        Session.Release(Self, oldToken)
    endif
    if generation != cleanupGeneration || token != -1 || operating
        return
    endif
    if Is3DLoaded()
        if generation != cleanupGeneration || token != -1 || operating
            return
        endif
        if restoreSightAim
            ; Native may have advanced after the last PSC read. Restore one coherent
            ; cached pose after End, before next Begin can remove that initial pose.
            ApplyAim()
        endif
        if !CleanupCurrent(cleanupGeneration)
            return
        endif
        PlayGamebryoAnimation("Reset", true)
        if !CleanupCurrent(cleanupGeneration)
            return
        endif
        NetImmerse.SetNodeScale(Self, VisualBoltNode, 1.0, false)
    endif
    if CleanupCurrent(cleanupGeneration)
        endingSession = false
    endif
EndFunction

bool Function CleanupCurrent(int expectedGeneration)
    return endingSession && generation == expectedGeneration && token == -1 && !operating
EndFunction

