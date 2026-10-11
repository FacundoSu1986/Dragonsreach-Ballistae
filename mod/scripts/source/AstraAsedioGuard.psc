Scriptname AstraAsedioGuard extends ObjectReference
; v13 prototype: attach only to the dedicated NPC ACTI reference. Artillero is
; the plugin's new guard reference, never an existing vanilla actor or player.
Actor Property Artillero Auto
ObjectReference Property Puesto Auto
; v15: only new shared city stations opt in. Standby is a measured own marker.
bool Property AllowPlayerTakeover = false Auto
ObjectReference Property Standby Auto
Weapon Property Launcher Auto
Ammo Property ShotAmmo Auto
Sound Property ShotSound Auto
; These two values must match the NPC PROJ DATA: 5400 speed, 0.35 gravity.
; World acceleration = 0.35 * 9.81 * 70. Unknown/invalid values fail closed.
float Property ProjectileSpeed = 5400.0 Auto
float Property ProjectileGravity = 240.345 Auto
float Property CadenceSeconds = 2.5 Auto
float Property TurnRate = 30.0 Auto
float Property PitchMin = -20.0 Auto
float Property PitchMax = 45.0 Auto
; v14: per-reference sector measured against each existing tower's roof/posts.
float Property YawHalfSector = 60.0 Auto
float Property YawCenter = 0.0 Auto
float Property ReleaseSeconds = 0.0666667 Auto
float Property FireSeconds = 0.2 Auto
float Property ResetSeconds = 0.8 Auto
float Property TargetHeight = 60.0 Auto
string Property YawNode = "CTRL_GIRO_360" Auto
string Property PitchNode = "CTRL_ELEVACION" Auto
string Property MuzzleNode = "ProjectileNode" Auto
string Property VisualBoltNode = "VIROTE_VISUAL" Auto

; GuardAnim v01: private OAR bridge; player controller remains byte-identical.
Faction poseFaction
Faction fireFaction
Idle holdIdle
Idle exitIdle
Actor visualTarget
float visualScanAt = 0.0
bool guardPoseStarted = false
bool guardPoseFiring = false
float guardPoseFireAt = 0.0

bool running = false
bool recovering = false
bool updating = false
bool destroyed = false
bool faulted = false
bool matricesReady = false
bool pinBusy = false
bool sceneBusy = false
bool recoveryRequested = false
Actor ownedGuard
Actor shotTarget
int generation = 0
int token = -1
int serial = 0
; 0 tracking/idle, 1 Fire awaiting release, 2 launched, 3 Reset.
int phase = 0
float phaseAt = 0.0
float nextShotAt = 0.0
float lastTick = 0.0
float yaw = 0.0
float pitch = 0.0
float desiredYaw = 0.0
float desiredPitch = 0.0
float aimX = 0.0
float aimY = -1.0
float aimZ = 0.0
float targetHorizontal = 0.0
float[] yawBase
float[] pitchBase
float[] yawMatrix
float[] pitchMatrix
float[] rootWorldMatrix
float[] muzzleWorldMatrix
float[] rootPosition
float[] muzzlePosition
int timingRevision = 0
bool playerReserved = false
bool playerReady = false
bool playerRestored = false
bool stationRetired = false
int playerLease = 0
int playerSerial = 0

Event OnInit()
    BlockActivation(true)
    BeginRecovery()
EndEvent

Event OnLoad()
    InvalidatePlayerLease()
    ; Also invalidates any Fire/Reset stack restored from a save. Saved node
    ; transforms are not trusted: start a new token at the neutral rest pose.
    BeginRecovery()
EndEvent

Event OnUnload()
    InvalidatePlayerLease()
    Shutdown()
EndEvent

Event OnCellDetach()
    InvalidatePlayerLease()
    Shutdown()
EndEvent

Event OnDestructionStageChanged(int aiOldStage, int aiCurrentStage)
    if aiCurrentStage > 0
        destroyed = true
        Shutdown()
    endif
EndEvent

Event OnActivate(ObjectReference akActionRef)
    BlockActivation(true)
EndEvent

bool Function Current(int expectedGeneration, int expectedToken)
    return running && !stationRetired && !playerReserved && !recovering && !destroyed && !faulted && generation == expectedGeneration && token == expectedToken && token > 0
EndFunction

bool Function RetireStation()
    if !stationRetired
        stationRetired = true
        InvalidatePlayerLease()
        Shutdown()
    endif
    if pinBusy || sceneBusy
        return false
    endif
    ReleaseOwnedGuard()
    return !pinBusy && !sceneBusy && ownedGuard == None
EndFunction

Function InvalidatePlayerLease()
    ; Scalar invalidation precedes every yielding recovery operation.
    playerReserved = false
    playerReady = false
    playerRestored = false
    playerLease = 0
    if playerSerial < 2000000000
        playerSerial += 1
    endif
EndFunction

bool Function PlayerLeaseCurrent(int lease)
    return AllowPlayerTakeover && !stationRetired && !destroyed && playerReserved && lease > 0 && playerLease == lease
EndFunction

bool Function StationSceneAvailable()
    if !AllowPlayerTakeover
        return true
    endif
    ; IsEffectsQuiescent exists only on AstraSight 3.5.0 (50659328) or newer.
    ; An older or missing DLL has no native owner, so the scene is free.
    ; Calling the unbound native keeps BeginRecovery retrying every 0.2s.
    if SKSE.GetPluginVersion("AstraSight") < 50659328
        return true
    endif
    ; API4 token zero is a per-reference ownership/cleanup query. This also
    ; prevents load-event order from restoring NPC nodes over native cleanup.
    return AstraSightNative.IsEffectsQuiescent(Self, 0)
EndFunction

int Function ReservePlayerLease()
    if !AllowPlayerTakeover || stationRetired || destroyed || playerReserved || Standby == None || playerSerial >= 2000000000
        return -1
    endif
    Actor player = Game.GetPlayer()
    if playerReserved || destroyed || !AllowPlayerTakeover || Standby == None || Artillero == player
        return -1
    endif
    playerSerial += 1
    int lease = playerSerial
    playerLease = lease
    playerReserved = true
    playerReady = false
    playerRestored = false
    ; Current() is now false before Shutdown's external effects. Suspended
    ; shot stacks must complete their compensation before preparation can pass.
    Shutdown()
    if !PlayerLeaseCurrent(lease)
        return -1
    endif
    return lease
EndFunction

bool Function PreparePlayerLease(int lease)
    if !PlayerLeaseCurrent(lease) || pinBusy || sceneBusy || recovering || running
        return false
    endif
    if playerReady
        return true
    endif
    bool sceneFree = StationSceneAvailable()
    if !PlayerLeaseCurrent(lease) || pinBusy || sceneBusy || !sceneFree
        return false
    endif
    int scenePluginVersion = SKSE.GetPluginVersion("AstraSight")
    if !PlayerLeaseCurrent(lease) || scenePluginVersion < 50659392
        return false
    endif
    ReleaseOwnedGuard()
    if !PlayerLeaseCurrent(lease) || pinBusy || sceneBusy
        return false
    endif
    bool placed = EnsureCityPlacement(generation, lease)
    if !PlayerLeaseCurrent(lease) || pinBusy || sceneBusy || !placed
        return false
    endif
    if !playerRestored
        bool loaded = Is3DLoaded()
        bool controls = NetImmerse.HasNode(Self, YawNode, false) && NetImmerse.HasNode(Self, PitchNode, false)
        if !PlayerLeaseCurrent(lease) || pinBusy || sceneBusy || !loaded || !controls
            return false
        endif
        ; Both exported controls have identity rest. Never recapture a aimed
        ; matrix as the next controller's rest, or aim would be applied twice.
        float[] rest = new float[9]
        rest[0] = 1.0
        rest[4] = 1.0
        rest[8] = 1.0
        sceneBusy = true
        bool settled = AstraSightNative.ResetIdleScene(Self)
        if PlayerLeaseCurrent(lease) && settled
            NetImmerse.SetNodeLocalRotationMatrix(Self, YawNode, rest, false)
        endif
        if PlayerLeaseCurrent(lease) && settled
            NetImmerse.SetNodeLocalRotationMatrix(Self, PitchNode, rest, false)
        endif
        sceneBusy = false
        if !PlayerLeaseCurrent(lease)
            QueueDeferredRecovery()
            return false
        endif
        if !settled
            return false
        endif
        yaw = 0.0
        pitch = 0.0
        playerRestored = true
    endif
    Actor candidate = Artillero
    Actor player = Game.GetPlayer()
    if !PlayerLeaseCurrent(lease) || pinBusy || sceneBusy || candidate == player
        return false
    endif
    if candidate != None
        bool usable = !candidate.IsDead() && !candidate.IsDisabled() && candidate.Is3DLoaded()
        if !PlayerLeaseCurrent(lease) || pinBusy || sceneBusy
            return false
        endif
        if usable
            ObjectReference waitPoint = Standby
            if waitPoint == None
                return false
            endif
            pinBusy = true
            candidate.MoveTo(waitPoint)
            if PlayerLeaseCurrent(lease)
                candidate.SetDontMove(true)
            endif
            if !PlayerLeaseCurrent(lease)
                ; Keep the slot until the old True/Move effect and compensation
                ; finish. A new recovery cannot pin/move a guard meanwhile.
                candidate.SetDontMove(false)
                pinBusy = false
                QueueDeferredRecovery()
                return false
            endif
            ownedGuard = candidate
            pinBusy = false
        endif
    endif
    if !PlayerLeaseCurrent(lease) || pinBusy || sceneBusy
        return false
    endif
    playerReady = true
    return true
EndFunction

bool Function ReleasePlayerLease(int lease)
    if !PlayerLeaseCurrent(lease)
        return false
    endif
    InvalidatePlayerLease()
    Shutdown()
    ; The player caller must first acknowledge native effects quiescence.
    ; Guard recovery still waits for its own scene/pin compensation slots.
    BeginRecovery()
    return true
EndFunction

bool Function Finite(float value, float minimum, float maximum)
    return value == value && value >= minimum && value <= maximum
EndFunction

Function NormalizeTimingProperties()
    ; Saved v13 VMAD properties override new source defaults. Migrate once;
    ; subsequent custom values remain intact when finite and compatible.
    if timingRevision < 14
        if FireSeconds >= 0.29999 && FireSeconds <= 0.30001
            FireSeconds = 0.2
        endif
        if ReleaseSeconds >= 0.09999 && ReleaseSeconds <= 0.10001
            ReleaseSeconds = 0.0666667
        endif
        if ResetSeconds >= 1.19999 && ResetSeconds <= 1.20001
            ResetSeconds = 0.8
        endif
        if CadenceSeconds >= 3.99999 && CadenceSeconds <= 4.00001
            CadenceSeconds = 2.5
        endif
        timingRevision = 14
    endif
    if !Finite(FireSeconds, 0.2, 2.0)
        FireSeconds = 0.2
    endif
    if !Finite(ReleaseSeconds, 0.0666666, 1.0) || ReleaseSeconds > FireSeconds
        ReleaseSeconds = 0.0666667
    endif
    if !Finite(ResetSeconds, 0.8, 5.0)
        ResetSeconds = 0.8
    endif
    CadenceSeconds = SafeCadenceSeconds()
EndFunction

float Function SafeCadenceSeconds()
    if !Finite(CadenceSeconds, 2.5, 60.0)
        return 2.5
    endif
    return CadenceSeconds
EndFunction

bool Function EnsureCityPlacement(int expectedGeneration, int lease = 0)
    ; B70/B80 are fresh persistent placements in the ESP. Never MoveTo or
    ; SetAngle the gun/markers while loading or handing it to the player:
    ; that can unload/reload the gun and invalidate both sibling controllers.
    if pinBusy || sceneBusy || generation != expectedGeneration || destroyed || stationRetired
        return false
    endif
    if !AllowPlayerTakeover
        return true
    endif
    if lease > 0
        return PlayerLeaseCurrent(lease)
    endif
    return recovering && !playerReserved && token == -1 && !faulted
EndFunction

Function BeginRecovery()
    if playerReserved || stationRetired
        return
    endif
    int probeGeneration = generation
    bool sceneFree = StationSceneAvailable()
    if generation != probeGeneration || playerReserved
        return
    endif
    if !sceneFree
        running = false
        generation += 1
        int deferredGeneration = generation
        token = -1
        recovering = false
        updating = false
        phase = 0
        shotTarget = None
        matricesReady = false
        recoveryRequested = true
        bool loaded = Is3DLoaded()
        if loaded && generation == deferredGeneration && !playerReserved && !pinBusy && !sceneBusy
            RegisterForSingleUpdate(0.2)
        endif
        return
    endif
    running = false
    generation += 1
    int recoveryGeneration = generation
    token = -1
    serial += 1
    recovering = true
    updating = false
    phase = 0
    shotTarget = None
    faulted = false
    matricesReady = false
    recoveryRequested = false
    ; Invalidate saved callbacks before migrating properties or touching 3D.
    NormalizeTimingProperties()
    if pinBusy || sceneBusy
        ; A preceding native still owns a mutation slot. Defer this generation
        ; until its effect and any compensation have finished.
        recoveryRequested = true
        recovering = false
        return
    endif
    UnregisterForUpdate()
    if generation != recoveryGeneration || token != -1
        return
    endif
    ReleaseOwnedGuard()
    if generation != recoveryGeneration || token != -1
        return
    endif
    Actor player = Game.GetPlayer()
    if generation != recoveryGeneration || token != -1
        return
    endif
    BlockActivation(true)
    if generation != recoveryGeneration || token != -1
        return
    endif
    if destroyed || Artillero == None || Artillero == player || Puesto == None || Launcher == None || ShotAmmo == None
        faulted = true
        recovering = false
        return
    endif
    bool gunLoaded = Is3DLoaded()
    bool guardLoaded = Artillero.Is3DLoaded()
    bool guardDead = Artillero.IsDead()
    bool guardDisabled = Artillero.IsDisabled()
    if generation != recoveryGeneration || token != -1
        return
    endif
    if guardDead || guardDisabled || destroyed
        faulted = true
        recovering = false
        return
    endif
    if !gunLoaded || !guardLoaded
        recovering = false
        if gunLoaded
            RegisterForSingleUpdate(1.0)
        endif
        return
    endif
    bool placed = EnsureCityPlacement(recoveryGeneration)
    if generation != recoveryGeneration || token != -1
        return
    endif
    if !placed
        recovering = false
        recoveryRequested = true
        QueueDeferredRecovery()
        return
    endif
    bool captured = CaptureMatrices()
    if generation != recoveryGeneration || token != -1
        return
    endif
    if !captured
        faulted = true
        recovering = false
        Debug.Trace("AstraAsedioGuard: missing or invalid model controls; controller stopped.")
        return
    endif
    float distance = Artillero.GetDistance(Puesto)
    if generation != recoveryGeneration || token != -1
        return
    endif
    if !Finite(distance, 0.0, 1000000.0)
        faulted = true
        recovering = false
        return
    endif
    if distance > 64.0
        ; A suspended recovery MoveTo can apply after player reservation or a
        ; newer load. Retain the mutation slot until that old move returns;
        ; Prepare must not move/pin the guard in Standby before this effect.
        Actor movingGuard = Artillero
        ObjectReference recoveryPoint = Puesto
        pinBusy = true
        movingGuard.MoveTo(recoveryPoint)
        bool moveCurrent = generation == recoveryGeneration && token == -1 && recovering && !playerReserved && !destroyed && !faulted
        pinBusy = false
        if !moveCurrent
            QueueDeferredRecovery()
            return
        endif
    endif
    bool aliveAfterMove = !Artillero.IsDead() && !Artillero.IsDisabled() && Artillero.Is3DLoaded()
    if generation != recoveryGeneration || token != -1
        return
    endif
    if !aliveAfterMove
        faulted = true
        recovering = false
        return
    endif
    bool pinAcquired = AcquirePin(recoveryGeneration)
    if generation != recoveryGeneration || token != -1
        return
    endif
    if !pinAcquired
        faulted = true
        recovering = false
        return
    endif
    yaw = 0.0
    pitch = 0.0
    token = serial
    running = true
    recovering = false
    int recoveryToken = token
    float now = Utility.GetCurrentRealTime()
    if !Current(recoveryGeneration, recoveryToken)
        return
    endif
    if !Finite(now, 0.0, 1000000000.0)
        faulted = true
        Shutdown()
        return
    endif
    lastTick = now
    nextShotAt = now + SafeCadenceSeconds()
    bool resetStarted = PlaySceneAnimation("Reset", recoveryGeneration, recoveryToken)
    if !Current(recoveryGeneration, recoveryToken)
        return
    endif
    if !resetStarted
        faulted = true
        Shutdown()
        return
    endif
    ApplyAim(recoveryGeneration, recoveryToken)
    if !Current(recoveryGeneration, recoveryToken)
        return
    endif
    bool positioned = PositionOperator(recoveryGeneration, recoveryToken)
    if !Current(recoveryGeneration, recoveryToken)
        return
    endif
    bool posed = positioned && StartGuardPose(recoveryGeneration, recoveryToken)
    if !Current(recoveryGeneration, recoveryToken)
        return
    endif
    if !posed
        faulted = true
        Shutdown()
        return
    endif
    SetVisualBolt(1.0, recoveryGeneration, recoveryToken)
    if Current(recoveryGeneration, recoveryToken)
        RegisterForSingleUpdate(0.2)
    endif
EndFunction

Function Shutdown()
    running = false
    generation += 1
    int cleanupGeneration = generation
    token = -1
    recovering = false
    updating = false
    phase = 0
    shotTarget = None
    visualTarget = None
    visualScanAt = 0.0
    matricesReady = false
    recoveryRequested = false
    UnregisterForUpdate()
    if generation != cleanupGeneration || token != -1
        return
    endif
    ; If acquisition is pending, its originating stack performs compensation
    ; after the True effect returns. No newer generation can pin before then.
    ReleaseOwnedGuard()
    if generation != cleanupGeneration || token != -1
        return
    endif
    if !sceneBusy
        sceneBusy = true
        RestoreNeutralScene()
        sceneBusy = false
        QueueDeferredRecovery()
    endif
EndFunction

bool Function AcquirePin(int expectedGeneration)
    if pinBusy || generation != expectedGeneration || token != -1 || !recovering || destroyed || faulted
        return false
    endif
    bool animationReady = LoadGuardAnimation()
    if generation != expectedGeneration || !animationReady
        Debug.Trace("AstraAsedioGuard: enable OAR and AstraAsedio_GuardAnim.esp to operate the NPC.")
        return false
    endif
    Actor candidate = Artillero
    pinBusy = true
    candidate.SetDontMove(true)
    if generation != expectedGeneration || token != -1 || !recovering || destroyed || faulted
        ; Cancellation may run before the native True effect. Keep the slot
        ; locked while undoing that effect, so an old False cannot unpin a new
        ; owner's guard. Shutdown never discards this pending compensation.
        candidate.SetDontMove(false)
        pinBusy = false
        QueueDeferredRecovery()
        return false
    endif
    ownedGuard = candidate
    pinBusy = false
    return true
EndFunction

Function ReleaseOwnedGuard()
    if pinBusy
        return
    endif
    Actor previousGuard = ownedGuard
    ownedGuard = None
    if previousGuard == None
        return
    endif
    pinBusy = true
    Actor player = Game.GetPlayer()
    if previousGuard != player
        StopGuardPose(previousGuard)
        previousGuard.SetDontMove(false)
    endif
    pinBusy = false
    QueueDeferredRecovery()
EndFunction

Function QueueDeferredRecovery()
    if playerReserved || pinBusy || sceneBusy || !recoveryRequested || destroyed || faulted
        return
    endif
    int queueGeneration = generation
    bool loaded = Is3DLoaded()
    if generation != queueGeneration || pinBusy || sceneBusy || !recoveryRequested || destroyed || faulted
        return
    endif
    if loaded
        RegisterForSingleUpdate(0.2)
    endif
EndFunction

Function RestoreNeutralScene()
    if !StationSceneAvailable()
        return
    endif
    ; Called only while sceneBusy holds the mutation slot. New OnLoad callbacks
    ; may invalidate state, but cannot write a newer pose until these effects
    ; finish. This also compensates an old hide/Fire effect applied after load.
    bool loaded = Is3DLoaded()
    if loaded
        if AllowPlayerTakeover
            ; Shared city stations settle existing sequences directly, as the
            ; player's native cleanup does. Avoid replaying a full Reset here.
            if SKSE.GetPluginVersion("AstraSight") >= 50659392
                AstraSightNative.ResetIdleScene(Self)
            endif
        else
            PlayGamebryoAnimation("Reset", true)
        endif
        NetImmerse.SetNodeScale(Self, VisualBoltNode, 1.0, false)
    endif
EndFunction

bool Function FinishSceneEffect(int expectedGeneration, int expectedToken)
    bool valid = Current(expectedGeneration, expectedToken)
    if !valid
        RestoreNeutralScene()
    endif
    sceneBusy = false
    QueueDeferredRecovery()
    return valid
EndFunction

bool Function PlaySceneAnimation(string name, int expectedGeneration, int expectedToken)
    if sceneBusy || !Current(expectedGeneration, expectedToken)
        return false
    endif
    sceneBusy = true
    bool started = PlayGamebryoAnimation(name, true)
    bool valid = FinishSceneEffect(expectedGeneration, expectedToken)
    return valid && started
EndFunction

Function SetVisualBolt(float scale, int expectedGeneration, int expectedToken)
    if sceneBusy || !Current(expectedGeneration, expectedToken)
        return
    endif
    sceneBusy = true
    NetImmerse.SetNodeScale(Self, VisualBoltNode, scale, false)
    FinishSceneEffect(expectedGeneration, expectedToken)
EndFunction

Function WriteAimNode(string node, float[] matrix, int expectedGeneration, int expectedToken)
    if sceneBusy || !Current(expectedGeneration, expectedToken)
        return
    endif
    sceneBusy = true
    NetImmerse.SetNodeLocalRotationMatrix(Self, node, matrix, false)
    FinishSceneEffect(expectedGeneration, expectedToken)
EndFunction

bool Function CaptureMatrices()
    int captureGeneration = generation
    if SKSE.GetVersion() < 2 || !Is3DLoaded()
        return false
    endif
    if !NetImmerse.HasNode(Self, YawNode, false) || !NetImmerse.HasNode(Self, PitchNode, false) || !NetImmerse.HasNode(Self, MuzzleNode, false) || !NetImmerse.HasNode(Self, VisualBoltNode, false)
        return false
    endif
    if generation != captureGeneration || token != -1 || !recovering
        return false
    endif
    ; The packaged v13 NIF has identity rest controls. Use that fixed rest,
    ; rather than recapturing a previously aimed node after recovery. Never
    ; compare typed arrays with None (Bethesda emits a poisoned array cast).
    yawBase = new float[9]
    pitchBase = new float[9]
    yawMatrix = new float[9]
    pitchMatrix = new float[9]
    rootWorldMatrix = new float[9]
    muzzleWorldMatrix = new float[9]
    rootPosition = new float[3]
    muzzlePosition = new float[3]
    yawBase[0] = 1.0
    yawBase[4] = 1.0
    yawBase[8] = 1.0
    pitchBase[0] = 1.0
    pitchBase[4] = 1.0
    pitchBase[8] = 1.0
    matricesReady = true
    return true
EndFunction

Function ApplyAim(int expectedGeneration, int expectedToken)
    if !Current(expectedGeneration, expectedToken) || !matricesReady
        return
    endif
    float yc = Math.Cos(yaw)
    float ys = Math.Sin(yaw)
    float pc = Math.Cos(-pitch)
    float ps = Math.Sin(-pitch)
    if !Current(expectedGeneration, expectedToken)
        return
    endif
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
    ; Same row-major products as the player controller: Rz(yaw)*rest and
    ; Rx(-pitch)*rest. The bore is local -Y; ProjectileNode supplies world +Y.
    WriteAimNode(YawNode, yawMatrix, expectedGeneration, expectedToken)
    if !Current(expectedGeneration, expectedToken)
        return
    endif
    WriteAimNode(PitchNode, pitchMatrix, expectedGeneration, expectedToken)
EndFunction

bool Function RotationValid(float[] matrix)
    int i = 0
    while i < 9
        if !Finite(matrix[i], -1.05, 1.05)
            return false
        endif
        i += 1
    endwhile
    float a = matrix[0]*matrix[0] + matrix[3]*matrix[3] + matrix[6]*matrix[6]
    float b = matrix[1]*matrix[1] + matrix[4]*matrix[4] + matrix[7]*matrix[7]
    float c = matrix[2]*matrix[2] + matrix[5]*matrix[5] + matrix[8]*matrix[8]
    float ab = matrix[0]*matrix[1] + matrix[3]*matrix[4] + matrix[6]*matrix[7]
    float ac = matrix[0]*matrix[2] + matrix[3]*matrix[5] + matrix[6]*matrix[8]
    float bc = matrix[1]*matrix[2] + matrix[4]*matrix[5] + matrix[7]*matrix[8]
    float determinant = matrix[0]*(matrix[4]*matrix[8]-matrix[5]*matrix[7]) - matrix[1]*(matrix[3]*matrix[8]-matrix[5]*matrix[6]) + matrix[2]*(matrix[3]*matrix[7]-matrix[4]*matrix[6])
    return Math.Abs(a - 1.0) <= 0.002 && Math.Abs(b - 1.0) <= 0.002 && Math.Abs(c - 1.0) <= 0.002 && Math.Abs(ab) <= 0.002 && Math.Abs(ac) <= 0.002 && Math.Abs(bc) <= 0.002 && Math.Abs(determinant - 1.0) <= 0.004
EndFunction

bool Function ReadPose(int expectedGeneration, int expectedToken)
    if !Current(expectedGeneration, expectedToken) || !matricesReady
        return false
    endif
    bool rootRead = NetImmerse.GetNodeWorldRotationMatrix(Self, "", rootWorldMatrix, false)
    if !Current(expectedGeneration, expectedToken) || !rootRead
        return false
    endif
    bool muzzleRead = NetImmerse.GetNodeWorldRotationMatrix(Self, MuzzleNode, muzzleWorldMatrix, false)
    if !Current(expectedGeneration, expectedToken) || !muzzleRead
        return false
    endif
    bool rootPointRead = NetImmerse.GetNodeWorldPosition(Self, "", rootPosition, false)
    if !Current(expectedGeneration, expectedToken) || !rootPointRead
        return false
    endif
    bool muzzlePointRead = NetImmerse.GetNodeWorldPosition(Self, MuzzleNode, muzzlePosition, false)
    if !Current(expectedGeneration, expectedToken) || !muzzlePointRead
        return false
    endif
    if !RotationValid(rootWorldMatrix) || !RotationValid(muzzleWorldMatrix)
        return false
    endif
    int i = 0
    while i < 3
        if !Finite(rootPosition[i], -1000000.0, 1000000.0) || !Finite(muzzlePosition[i], -1000000.0, 1000000.0)
            return false
        endif
        i += 1
    endwhile
    return Current(expectedGeneration, expectedToken)
EndFunction

bool Function GuardReady(int expectedGeneration, int expectedToken)
    if !Current(expectedGeneration, expectedToken) || ownedGuard == None || ownedGuard != Artillero
        return false
    endif
    bool ready = Is3DLoaded() && !IsDisabled() && ownedGuard.Is3DLoaded() && !ownedGuard.IsDead() && !ownedGuard.IsDisabled()
    float distance = ownedGuard.GetDistance(Self)
    return Current(expectedGeneration, expectedToken) && ready && Finite(distance, 0.0, 240.0)
EndFunction

bool Function ValidTarget(Actor target, int expectedGeneration, int expectedToken)
    if !GuardReady(expectedGeneration, expectedToken) || target == None || target == Artillero
        return false
    endif
    Actor player = Game.GetPlayer()
    if !Current(expectedGeneration, expectedToken) || target == player
        return false
    endif
    bool valid = target.Is3DLoaded() && !target.IsDisabled() && !target.IsDead() && !target.IsPlayerTeammate() && target.IsHostileToActor(Artillero) && target.GetCombatState() > 0 && Artillero.GetCombatState() == 1
    bool visible = Artillero.HasLOS(target)
    Actor combatTarget = Artillero.GetCombatTarget()
    return Current(expectedGeneration, expectedToken) && valid && visible && combatTarget == target
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

bool Function SampleTarget(Actor target, int expectedGeneration, int expectedToken)
    return SampleHorizontalTarget(target, expectedGeneration, expectedToken)
EndFunction

float Function Approach(float value, float goal, float maximumStep)
    float difference = goal - value
    if difference > maximumStep
        return value + maximumStep
    elseif difference < -maximumStep
        return value - maximumStep
    endif
    return goal
EndFunction

Function TurnToward(float dt, int expectedGeneration, int expectedToken)
    ; Rate and timing are bounded even if an ESP property is modified.
    float rate = TurnRate
    if !Finite(rate, 1.0, 30.0)
        rate = 30.0
    endif
    float nextYaw = Approach(yaw, desiredYaw, rate*dt)
    float nextPitch = 0.0
    if !Current(expectedGeneration, expectedToken)
        return
    endif
    yaw = nextYaw
    pitch = nextPitch
    ApplyAim(expectedGeneration, expectedToken)
EndFunction

bool Function PointNearSegment(float px, float py, float pz, float ax, float ay, float az, float bx, float by, float bz, float radius)
    float dx = bx-ax
    float dy = by-ay
    float dz = bz-az
    float lengthSquared = dx*dx + dy*dy + dz*dz
    if lengthSquared <= 0.00001
        return true
    endif
    float along = ((px-ax)*dx + (py-ay)*dy + (pz-az)*dz)/lengthSquared
    if along < 0.0
        along = 0.0
    elseif along > 1.0
        along = 1.0
    endif
    dx = px-(ax+along*dx)
    dy = py-(ay+along*dy)
    dz = pz-(az+along*dz)
    return dx*dx + dy*dy + dz*dz <= radius*radius
EndFunction

bool Function PlayerClear(int expectedGeneration, int expectedToken)
    Actor player = Game.GetPlayer()
    if !Current(expectedGeneration, expectedToken) || player == None
        return false
    endif
    bool playerLoaded = player.Is3DLoaded()
    float px = player.GetPositionX()
    float py = player.GetPositionY()
    float pz = player.GetPositionZ()
    float height = player.GetHeight()
    if !Current(expectedGeneration, expectedToken) || !playerLoaded || !Finite(px, -1000000.0, 1000000.0) || !Finite(py, -1000000.0, 1000000.0) || !Finite(pz, -1000000.0, 1000000.0) || !Finite(height, 1.0, 512.0)
        return false
    endif
    if height < 128.0
        height = 128.0
    endif
    height += 64.0
    ; Five samples include feet/head and cover the whole vertical body estimate.
    ; Radius adds half the spacing to an 80-unit capsule margin. Eight bounded
    ; trajectory segments use the measured muzzle +Y and world gravity, so the
    ; protection follows the projectile arc rather than a straight target ray.
    float radius = 80.0 + height/8.0
    float bx = muzzleWorldMatrix[1]
    float by = muzzleWorldMatrix[4]
    float bz = muzzleWorldMatrix[7]
    float boreHorizontal = Math.Sqrt(bx*bx + by*by)
    if boreHorizontal < 0.01
        return false
    endif
    float totalTime = targetHorizontal/(ProjectileSpeed*boreHorizontal)
    if !Finite(totalTime, 0.00001, 30.0)
        return false
    endif
    float ax = muzzlePosition[0]
    float ay = muzzlePosition[1]
    float az = muzzlePosition[2]
    int step = 1
    while step <= 8
        float t = totalTime*step/8.0
        float ex = muzzlePosition[0] + bx*ProjectileSpeed*t
        float ey = muzzlePosition[1] + by*ProjectileSpeed*t
        float ez = muzzlePosition[2] + bz*ProjectileSpeed*t - 0.5*ProjectileGravity*t*t
        int sample = 0
        while sample <= 4
            if PointNearSegment(px, py, pz+height*sample/4.0, ax, ay, az, ex, ey, ez, radius)
                return false
            endif
            sample += 1
        endwhile
        ax = ex
        ay = ey
        az = ez
        step += 1
    endwhile
    return Current(expectedGeneration, expectedToken)
EndFunction

bool Function ShotPreflight(Actor target, int expectedGeneration, int expectedToken)
    if !SampleTarget(target, expectedGeneration, expectedToken)
        return false
    endif
    ; Check both commanded pose and target against the actual render-task pose.
    float yc = Math.Cos(yaw)
    float ys = Math.Sin(yaw)
    float pc = Math.Cos(pitch)
    float ps = Math.Sin(pitch)
    float lx = ys*pc
    float ly = -yc*pc
    float wx = rootWorldMatrix[0]*lx + rootWorldMatrix[1]*ly + rootWorldMatrix[2]*ps
    float wy = rootWorldMatrix[3]*lx + rootWorldMatrix[4]*ly + rootWorldMatrix[5]*ps
    float wz = rootWorldMatrix[6]*lx + rootWorldMatrix[7]*ly + rootWorldMatrix[8]*ps
    float poseDot = wx*muzzleWorldMatrix[1] + wy*muzzleWorldMatrix[4] + wz*muzzleWorldMatrix[7]
    float targetDot = aimX*muzzleWorldMatrix[1] + aimY*muzzleWorldMatrix[4] + aimZ*muzzleWorldMatrix[7]
    if !Finite(poseDot, 0.99995, 1.002) || !Finite(targetDot, 0.99995, 1.002) || !Current(expectedGeneration, expectedToken)
        return false
    endif
    bool clear = PlayerClear(expectedGeneration, expectedToken)
    bool menuOpen = Utility.IsInMenuMode()
    bool targetValid = ValidTarget(target, expectedGeneration, expectedToken)
    return Current(expectedGeneration, expectedToken) && clear && !menuOpen && targetValid
EndFunction

Function BeginShot(Actor target, int expectedGeneration, int expectedToken)
    if !Current(expectedGeneration, expectedToken) || phase != 0
        return
    endif
    float now = Utility.GetCurrentRealTime()
    if !Current(expectedGeneration, expectedToken) || phase != 0 || !Finite(now, 0.0, 1000000000.0) || now < nextShotAt
        return
    endif
    bool bodyStarted = SetGuardFirePose(true, expectedGeneration, expectedToken)
    if !Current(expectedGeneration, expectedToken) || !bodyStarted
        return
    endif
    guardPoseFireAt = now
    phase = 1
    phaseAt = now
    shotTarget = target
    float cadence = SafeCadenceSeconds()
    nextShotAt = now + cadence
    bool started = PlaySceneAnimation("Fire", expectedGeneration, expectedToken)
    if !Current(expectedGeneration, expectedToken) || phase != 1 || shotTarget != target
        return
    endif
    if !started
        AbortShot(expectedGeneration, expectedToken)
    endif
EndFunction

Function CommitShot(Actor target, int expectedGeneration, int expectedToken)
    if sceneBusy || !Current(expectedGeneration, expectedToken) || phase != 1 || shotTarget != target
        return
    endif
    float now = Utility.GetCurrentRealTime()
    ; Obtain the clock before the final scene/target preflight: a yielding clock
    ; must not create a fresh native boundary between validation and launch.
    bool safe = ShotPreflight(target, expectedGeneration, expectedToken)
    if !Current(expectedGeneration, expectedToken) || phase != 1 || shotTarget != target
        return
    endif
    if !safe || !Finite(now, 0.0, 1000000000.0)
        AbortShot(expectedGeneration, expectedToken)
        return
    endif
    float cadence = SafeCadenceSeconds()
    if nextShotAt < now+cadence
        nextShotAt = now+cadence
    endif
    ; Reserve before the native call. Weapon.Fire is an external launch, not a
    ; success boolean or an atomic transaction; it cannot be undone afterwards.
    phase = 2
    phaseAt = now
    if !Current(expectedGeneration, expectedToken) || phase != 2 || shotTarget != target
        return
    endif
    ; Weapon.Fire can suspend before its irreversible projectile effect. Keep
    ; the same scene slot as animations until it returns and any old pose is
    ; compensated; player preparation must wait for this launch to drain.
    sceneBusy = true
    Launcher.Fire(Self, ShotAmmo)
    bool launchCurrent = FinishSceneEffect(expectedGeneration, expectedToken)
    if !launchCurrent || !Current(expectedGeneration, expectedToken) || phase != 2
        return
    endif
    ; The post-launch clock closes delays during release/preflight/Fire itself.
    ; It creates no boundary between target validation and the native launch.
    float launchedAt = Utility.GetCurrentRealTime()
    if !Current(expectedGeneration, expectedToken) || phase != 2
        return
    endif
    if !Finite(launchedAt, 0.0, 1000000000.0)
        faulted = true
        Shutdown()
        return
    endif
    phaseAt = launchedAt
    if nextShotAt < launchedAt+cadence
        nextShotAt = launchedAt+cadence
    endif
    SetVisualBolt(0.0, expectedGeneration, expectedToken)
    if !Current(expectedGeneration, expectedToken) || phase != 2
        return
    endif
    if ShotSound != None
        ShotSound.Play(Self)
    endif
EndFunction

Function AbortShot(int expectedGeneration, int expectedToken)
    if !Current(expectedGeneration, expectedToken) || phase == 0
        return
    endif
    SetGuardFirePose(false, expectedGeneration, expectedToken)
    if Current(expectedGeneration, expectedToken)
        StartReset(expectedGeneration, expectedToken)
    endif
EndFunction

Function StartReset(int expectedGeneration, int expectedToken)
    float now = Utility.GetCurrentRealTime()
    if !Current(expectedGeneration, expectedToken)
        return
    endif
    phase = 3
    phaseAt = now
    bool started = PlaySceneAnimation("Reset", expectedGeneration, expectedToken)
    if !Current(expectedGeneration, expectedToken)
        return
    endif
    if !started
        faulted = true
        Shutdown()
    endif
EndFunction

Function FinishUpdate(int expectedGeneration, int expectedToken, float delay)
    if !Current(expectedGeneration, expectedToken)
        return
    endif
    updating = false
    RegisterForSingleUpdate(delay)
EndFunction

Event OnUpdate()
    if updating || recovering || pinBusy || sceneBusy || destroyed || faulted
        return
    endif
    if !running
        BeginRecovery()
        return
    endif
    updating = true
    int updateGeneration = generation
    int updateToken = token
    float now = Utility.GetCurrentRealTime()
    if !Current(updateGeneration, updateToken)
        return
    endif
    if !Finite(now, 0.0, 1000000000.0)
        faulted = true
        Shutdown()
        return
    endif
    if now < lastTick
        ; GetCurrentRealTime restarts with the runtime. This second recovery path
        ; rejects a pending saved update even before a restored OnLoad callback.
        BeginRecovery()
        return
    endif
    float dt = now-lastTick
    if dt > 0.4
        dt = 0.4
    endif
    lastTick = now
    bool ready = GuardReady(updateGeneration, updateToken)
    if !Current(updateGeneration, updateToken)
        return
    endif
    if !ready
        bool dead = Artillero.IsDead()
        bool guardLoaded = Artillero.Is3DLoaded()
        bool gunLoaded = Is3DLoaded()
        if !Current(updateGeneration, updateToken)
            return
        endif
        ; Death/displacement releases the pin and stops until a new load. A
        ; temporarily unloaded guard may recover when its 3D attaches again.
        faulted = dead || guardLoaded
        Shutdown()
        if !faulted && gunLoaded && !destroyed
            RegisterForSingleUpdate(1.0)
        endif
        return
    endif
    if guardPoseFiring && now >= guardPoseFireAt+1.0
        SetGuardFirePose(false, updateGeneration, updateToken)
    endif
    if !Current(updateGeneration, updateToken)
        return
    endif
    bool menuOpen = Utility.IsInMenuMode()
    if !Current(updateGeneration, updateToken)
        return
    endif
    if menuOpen && (phase == 1 || phase == 2)
        AbortShot(updateGeneration, updateToken)
    endif
    if !Current(updateGeneration, updateToken)
        return
    endif
    if phase == 1
        ; Fixed bounds are used if edited timing properties are invalid.
        float releaseDelay = ReleaseSeconds
        if !Finite(releaseDelay, 0.0666666, 1.0) || releaseDelay > FireSeconds
            releaseDelay = 0.0666667
        endif
        if now >= phaseAt+releaseDelay
            CommitShot(shotTarget, updateGeneration, updateToken)
        endif
        FinishUpdate(updateGeneration, updateToken, 0.05)
        return
    elseif phase == 2
        float fireDelay = FireSeconds
        if !Finite(fireDelay, 0.2, 2.0)
            fireDelay = 0.2
        endif
        if now >= phaseAt+fireDelay
            StartReset(updateGeneration, updateToken)
        endif
        FinishUpdate(updateGeneration, updateToken, 0.05)
        return
    elseif phase == 3
        float resetDelay = ResetSeconds
        if !Finite(resetDelay, 0.8, 5.0)
            resetDelay = 0.8
        endif
        if now >= phaseAt+resetDelay
            SetVisualBolt(1.0, updateGeneration, updateToken)
            if !Current(updateGeneration, updateToken)
                return
            endif
            phase = 0
            shotTarget = None
        endif
        FinishUpdate(updateGeneration, updateToken, 0.05)
        return
    endif
    if menuOpen
        FinishUpdate(updateGeneration, updateToken, 1.0)
        return
    endif
    Actor target = ChooseVisualTarget(now, updateGeneration, updateToken)
    bool sampled = SampleVisualTarget(target, updateGeneration, updateToken)
    if !Current(updateGeneration, updateToken)
        return
    endif
    ; A reachable enemy refines yaw from the actual muzzle rather than root.
    if sampled && ValidTarget(target, updateGeneration, updateToken)
        SampleTarget(target, updateGeneration, updateToken)
    endif
    if !Current(updateGeneration, updateToken)
        return
    endif
    if sampled
        TurnToward(dt, updateGeneration, updateToken)
    endif
    if !Current(updateGeneration, updateToken)
        return
    endif
    bool positioned = PositionOperator(updateGeneration, updateToken)
    if !Current(updateGeneration, updateToken)
        return
    endif
    if !positioned
        faulted = true
        Shutdown()
        return
    endif
    ; The bounded player trajectory check is needed only when a shot is due.
    if now >= nextShotAt
        bool aligned = ShotPreflight(target, updateGeneration, updateToken)
        if !Current(updateGeneration, updateToken)
            return
        endif
        if aligned
            BeginShot(target, updateGeneration, updateToken)
        endif
    endif
    if Current(updateGeneration, updateToken)
        if phase == 1
            FinishUpdate(updateGeneration, updateToken, 0.02)
        else
            FinishUpdate(updateGeneration, updateToken, 0.05)
        endif
    endif
EndEvent

; Private OAR membership is held only while this controller owns its NPC.
bool Function LoadGuardAnimation()
    poseFaction = Game.GetFormFromFile(0x800, "AstraAsedio_GuardAnim.esp") as Faction
    fireFaction = Game.GetFormFromFile(0x801, "AstraAsedio_GuardAnim.esp") as Faction
    holdIdle = Game.GetFormFromFile(0x802, "AstraAsedio_GuardAnim.esp") as Idle
    exitIdle = Game.GetFormFromFile(0x803, "AstraAsedio_GuardAnim.esp") as Idle
    return SKSE.GetPluginVersion("OpenAnimationReplacer") >= 0 && poseFaction != None && fireFaction != None && holdIdle != None && exitIdle != None
EndFunction

Function StopGuardPose(Actor candidate)
    if candidate == None || candidate == Game.GetPlayer()
        return
    endif
    if fireFaction != None
        candidate.RemoveFromFaction(fireFaction)
    endif
    if poseFaction != None
        candidate.RemoveFromFaction(poseFaction)
    endif
    if exitIdle != None && candidate.Is3DLoaded() && !candidate.IsDead()
        candidate.PlayIdle(exitIdle)
    endif
    candidate.SetHeadTracking(true)
    guardPoseFiring = false
    guardPoseStarted = false
EndFunction

; The existing handoff waits for pinBusy. Keep it across every actor effect;
; a cancelled stack undoes its old effects before a new owner may move the NPC.
bool Function FinishGuardEffect(Actor candidate, int expectedGeneration, int expectedToken)
    bool valid = Current(expectedGeneration, expectedToken) && ownedGuard == candidate
    if !valid
        StopGuardPose(candidate)
        candidate.SetDontMove(false)
        if ownedGuard == candidate
            ownedGuard = None
        endif
    endif
    pinBusy = false
    QueueDeferredRecovery()
    return valid
EndFunction

bool Function StartGuardPose(int expectedGeneration, int expectedToken)
    if pinBusy || !GuardReady(expectedGeneration, expectedToken)
        return false
    endif
    Actor candidate = ownedGuard
    pinBusy = true
    candidate.RemoveFromFaction(fireFaction)
    if Current(expectedGeneration, expectedToken)
        candidate.SetFactionRank(poseFaction, 0)
    endif
    if Current(expectedGeneration, expectedToken)
        candidate.SetHeadTracking(false)
    endif
    if Current(expectedGeneration, expectedToken)
        candidate.SheatheWeapon()
    endif
    bool started = false
    if Current(expectedGeneration, expectedToken)
        started = candidate.PlayIdle(holdIdle)
    endif
    bool valid = FinishGuardEffect(candidate, expectedGeneration, expectedToken)
    if valid
        guardPoseStarted = started
        guardPoseFiring = false
    endif
    return valid && started
EndFunction

bool Function SetGuardFirePose(bool fire, int expectedGeneration, int expectedToken)
    if pinBusy || !GuardReady(expectedGeneration, expectedToken) || !guardPoseStarted
        return false
    endif
    Actor candidate = ownedGuard
    pinBusy = true
    if fire
        candidate.SetFactionRank(fireFaction, 0)
    else
        candidate.RemoveFromFaction(fireFaction)
    endif
    bool valid = FinishGuardEffect(candidate, expectedGeneration, expectedToken)
    if valid
        guardPoseFiring = fire
    endif
    return valid
EndFunction

bool Function PositionOperator(int expectedGeneration, int expectedToken)
    if pinBusy || !GuardReady(expectedGeneration, expectedToken) || !ReadPose(expectedGeneration, expectedToken)
        return false
    endif
    ; Root is level in the station records. Keep Z fixed even during the sweep.
    float localX = -151.0*Math.Sin(yaw)
    float localY = 151.0*Math.Cos(yaw)
    float px = rootPosition[0] + rootWorldMatrix[0]*localX + rootWorldMatrix[1]*localY
    float py = rootPosition[1] + rootWorldMatrix[3]*localX + rootWorldMatrix[4]*localY
    float frontX = rootWorldMatrix[0]*Math.Sin(yaw) - rootWorldMatrix[1]*Math.Cos(yaw)
    float frontY = rootWorldMatrix[3]*Math.Sin(yaw) - rootWorldMatrix[4]*Math.Cos(yaw)
    float heading = HeadingFromVector(frontX, frontY, 0.0)
    if !Current(expectedGeneration, expectedToken)
        return false
    endif
    Actor candidate = ownedGuard
    pinBusy = true
    candidate.SetPosition(px, py, rootPosition[2])
    if Current(expectedGeneration, expectedToken)
        candidate.SetAngle(0.0, 0.0, heading)
    endif
    return FinishGuardEffect(candidate, expectedGeneration, expectedToken)
EndFunction

bool Function VisualTargetValid(Actor target, int expectedGeneration, int expectedToken)
    if !GuardReady(expectedGeneration, expectedToken) || target == None || target == Artillero
        return false
    endif
    bool valid = target.Is3DLoaded() && !target.IsDisabled() && !target.IsDead()
    bool visible = Artillero.HasLOS(target)
    return Current(expectedGeneration, expectedToken) && valid && visible
EndFunction

bool Function SampleVisualTarget(Actor target, int expectedGeneration, int expectedToken)
    if !VisualTargetValid(target, expectedGeneration, expectedToken) || !ReadPose(expectedGeneration, expectedToken)
        return false
    endif
    float dx = target.GetPositionX() - rootPosition[0]
    float dy = target.GetPositionY() - rootPosition[1]
    float distanceSquared = dx*dx + dy*dy
    if !Current(expectedGeneration, expectedToken) || !Finite(distanceSquared, 6400.0, 36000000.0)
        return false
    endif
    float lx = rootWorldMatrix[0]*dx + rootWorldMatrix[3]*dy
    float ly = rootWorldMatrix[1]*dx + rootWorldMatrix[4]*dy
    float angle = HeadingFromVector(lx, -ly, yaw)
    if angle > 180.0
        angle -= 360.0
    endif
    if !Finite(YawHalfSector, 1.0, 60.0) || !Finite(YawCenter, -60.0+YawHalfSector, 60.0-YawHalfSector) || !Finite(angle, YawCenter-YawHalfSector, YawCenter+YawHalfSector) || !Current(expectedGeneration, expectedToken)
        return false
    endif
    desiredYaw = angle
    desiredPitch = 0.0
    return true
EndFunction

Actor Function ChooseVisualTarget(float now, int expectedGeneration, int expectedToken)
    Actor enemy = Artillero.GetCombatTarget()
    if ValidTarget(enemy, expectedGeneration, expectedToken) && SampleVisualTarget(enemy, expectedGeneration, expectedToken)
        visualTarget = enemy
        return enemy
    endif
    if SampleVisualTarget(visualTarget, expectedGeneration, expectedToken)
        return visualTarget
    endif
    visualTarget = None
    if now < visualScanAt || !Current(expectedGeneration, expectedToken)
        return None
    endif
    visualScanAt = now + 1.0
    Actor candidate = Game.GetPlayer()
    if SampleVisualTarget(candidate, expectedGeneration, expectedToken)
        visualTarget = candidate
        return candidate
    endif
    int attempt = 0
    while attempt < 6 && Current(expectedGeneration, expectedToken)
        candidate = Game.FindRandomActor(rootPosition[0], rootPosition[1], rootPosition[2], 6000.0)
        if SampleVisualTarget(candidate, expectedGeneration, expectedToken)
            visualTarget = candidate
            return candidate
        endif
        attempt += 1
    endwhile
    return None
EndFunction

bool Function HorizontalReachable(Actor target, float horizontal, int expectedGeneration, int expectedToken)
    if !Current(expectedGeneration, expectedToken) || !Finite(horizontal, 80.0, 6000.0) || !Finite(ProjectileSpeed, 1.0, 100000.0) || !Finite(ProjectileGravity, 0.0, 5000.0)
        return false
    endif
    float baseZ = target.GetPositionZ()
    float height = target.GetHeight()
    float travel = horizontal/ProjectileSpeed
    float boltZ = muzzlePosition[2] - 0.5*ProjectileGravity*travel*travel
    bool validHeights = Finite(baseZ, -1000000.0, 1000000.0) && Finite(height, 24.0, 8192.0)
    return Current(expectedGeneration, expectedToken) && validHeights && (boltZ >= (baseZ + 8.0)) && (boltZ <= (baseZ + height - 8.0))
EndFunction

bool Function SampleHorizontalTarget(Actor target, int expectedGeneration, int expectedToken)
    if !ValidTarget(target, expectedGeneration, expectedToken) || !ReadPose(expectedGeneration, expectedToken)
        return false
    endif
    float dx = target.GetPositionX() - muzzlePosition[0]
    float dy = target.GetPositionY() - muzzlePosition[1]
    float horizontal = Math.Sqrt(dx*dx + dy*dy)
    if !HorizontalReachable(target, horizontal, expectedGeneration, expectedToken)
        return false
    endif
    float wx = dx/horizontal
    float wy = dy/horizontal
    float lx = rootWorldMatrix[0]*wx + rootWorldMatrix[3]*wy
    float ly = rootWorldMatrix[1]*wx + rootWorldMatrix[4]*wy
    float angle = HeadingFromVector(lx, -ly, yaw)
    if angle > 180.0
        angle -= 360.0
    endif
    if !Finite(angle, YawCenter-YawHalfSector, YawCenter+YawHalfSector) || !Current(expectedGeneration, expectedToken)
        return false
    endif
    desiredYaw = angle
    desiredPitch = 0.0
    aimX = wx
    aimY = wy
    aimZ = 0.0
    targetHorizontal = horizontal
    return true
EndFunction
