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


; v26: exclusive operator package; persisted v23 field names stay compatible.
; Legacy functions remain fenced to let old saved Papyrus stacks return safely.
bool v23Wanted = false
int v23PumpOwner = 0
int v23Generation = 0
int v23Serial = 0
int v23Token = 0
int v23PlacementVersion = 0
bool v23Warned = false
int v23LastStatus = -99
; v27: diagnosability + fault backoff. New names; old saves initialize defaults.
; v27WarnedRefs: one-shot trace when the Torres weapon/operator refs cannot
; resolve (the otherwise silent failure measured in the v21 packaging incident).
; v27Faults: consecutive native fault drains (status -2). Backs the next pump
; off instead of re-beginning every second (v25 log showed 134 churn cycles).
bool v27WarnedRefs = false
int v27Faults = 0
bool v28RetryWaited = false



Event OnInit()
    BlockActivation(true)
    StartV23()
EndEvent

Event OnLoad()
    StartV23()
EndEvent

Event OnUnload()
    StopV23()
EndEvent

Event OnCellDetach()
    StopV23()
EndEvent

Event OnDestructionStageChanged(int aiOldStage, int aiCurrentStage)
    if aiCurrentStage > 0
        destroyed = true
        StopV23()
    endif
EndEvent

Event OnActivate(ObjectReference akActionRef)
    BlockActivation(true)
EndEvent

bool Function Current(int expectedGeneration, int expectedToken)
    ; Fences every v22 aim/Fire/Reset stack restored from a save.
    return false
EndFunction

bool Function RetireStation()
    stationRetired = true
    StopV23()
    if v23Token <= 0 || !AstraGuardNative.IsAvailable()
        return !sceneBusy && !pinBusy
    endif
    return AstraGuardNative.EndOperation(Self, v23Token)
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
    ; Low Whiterun stations remain NPC-only.
    return -1
EndFunction

bool Function PreparePlayerLease(int lease)
    return false
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
    StartV23()
EndFunction

Function Shutdown()
    StopV23()
EndFunction

bool Function AcquirePin(int expectedGeneration)
    ; Retired v22 effects: a restored stack cannot acquire or write.
    return false
EndFunction

Function ReleaseOwnedGuard()
    ; Retired v22 effects: native NPC operation is the sole owner.
    return
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
    ; Retired v22 effects: native NPC operation is the sole owner.
    return
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
    ; Retired v22 effects: a restored stack cannot acquire or write.
    return false
EndFunction

Function SetVisualBolt(float scale, int expectedGeneration, int expectedToken)
    ; Retired v22 effects: native NPC operation is the sole owner.
    return
EndFunction

Function WriteAimNode(string node, float[] matrix, int expectedGeneration, int expectedToken)
    ; Retired v22 effects: native NPC operation is the sole owner.
    return
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
    ; Retired v22 effects: native NPC operation is the sole owner.
    return
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
    ; Retired v22 effects: native NPC operation is the sole owner.
    return
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
    PumpV23()
EndEvent

; Private OAR membership is held only while this controller owns its NPC.
bool Function LoadGuardAnimation()
    poseFaction = Game.GetFormFromFile(0x800, "DragonsreachBallistae_GuardAnims.esp") as Faction
    fireFaction = Game.GetFormFromFile(0x801, "DragonsreachBallistae_GuardAnims.esp") as Faction
    holdIdle = Game.GetFormFromFile(0x802, "DragonsreachBallistae_GuardAnims.esp") as Idle
    exitIdle = Game.GetFormFromFile(0x803, "DragonsreachBallistae_GuardAnims.esp") as Idle
    return SKSE.GetPluginVersion("OpenAnimationReplacer") >= 0 && poseFaction != None && fireFaction != None && holdIdle != None && exitIdle != None
EndFunction

Function StopGuardPose(Actor candidate)
    ; Retired v22 effects: native NPC operation is the sole owner.
    return
EndFunction

; The existing handoff waits for pinBusy. Keep it across every actor effect;
; a cancelled stack undoes its old effects before a new owner may move the NPC.
bool Function FinishGuardEffect(Actor candidate, int expectedGeneration, int expectedToken)
    ; Retired v22 effects: a restored stack cannot acquire or write.
    return false
EndFunction

bool Function StartGuardPose(int expectedGeneration, int expectedToken)
    ; Retired v22 effects: a restored stack cannot acquire or write.
    return false
EndFunction

bool Function SetGuardFirePose(bool fire, int expectedGeneration, int expectedToken)
    ; Retired v22 effects: a restored stack cannot acquire or write.
    return false
EndFunction

bool Function PositionOperator(int expectedGeneration, int expectedToken)
    ; Retired v22 effects: a restored stack cannot acquire or write.
    return false
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

Function StartV23()
    v27WarnedRefs = false
    v28RetryWaited = false
    generation += 1
    running = false
    recovering = false
    v23Generation += 1
    v23Wanted = !stationRetired && !destroyed
    UnregisterForUpdate()
    if v23Token > 0 && AstraGuardNative.IsAvailable()
        AstraGuardNative.EndOperation(Self, v23Token)
    endif
    RegisterForSingleUpdate(0.2)
EndFunction

Function StopV23()
    generation += 1
    running = false
    v23Generation += 1
    v23Wanted = false
    UnregisterForUpdate()
    if v23Token > 0 && AstraGuardNative.IsAvailable()
        AstraGuardNative.EndOperation(Self, v23Token)
    endif
EndFunction

Actor Function ResolveV23Operator()
    ObjectReference east = Game.GetFormFromFile(0x00000B70, "DragonsreachBallistae_WhiterunTowers.esp") as ObjectReference
    if Self == east
        return Game.GetFormFromFile(0x00000B71, "DragonsreachBallistae_WhiterunTowers.esp") as Actor
    endif
    ObjectReference west = Game.GetFormFromFile(0x00000B80, "DragonsreachBallistae_WhiterunTowers.esp") as ObjectReference
    if Self == west
        return Game.GetFormFromFile(0x00000B81, "DragonsreachBallistae_WhiterunTowers.esp") as Actor
    endif
    return None
EndFunction

bool Function V23Current(int expected)
    return v23Generation == expected && v23Wanted && !stationRetired && !destroyed
EndFunction

bool Function MigrateV23(Actor actorRef, int expected)
    if !V23Current(expected) || actorRef == None || Puesto == None
        return false
    endif
    if !Is3DLoaded() || !actorRef.Is3DLoaded() || actorRef.IsDead()
        return false
    endif
    ; Existing persistent markers can also carry a saved transform: recompute.
    float angle = GetAngleZ()
    float px = GetPositionX() - 151.0*Math.Sin(angle)
    float py = GetPositionY() + 151.0*Math.Cos(angle)
    float pz = GetPositionZ()
    if !V23Current(expected)
        return false
    endif
    Puesto.SetPosition(px, py, pz)
    if !V23Current(expected)
        return false
    endif
    Puesto.SetAngle(0.0, 0.0, angle+180.0)
    int index = 0
    while index < 6 && V23Current(expected)
        if index == 0 || index == 1 || index == 4 || index == 5
            Faction privateFlag = Game.GetFormFromFile(0x00000800+index, "DragonsreachBallistae_GuardAnims.esp") as Faction
            if privateFlag != None
                actorRef.RemoveFromFaction(privateFlag)
            endif
        endif
        index += 1
    endwhile
    if !V23Current(expected)
        return false
    endif
    actorRef.SetDontMove(false)
    if !V23Current(expected)
        return false
    endif
    actorRef.SetHeadTracking(true)
    if !V23Current(expected)
        return false
    endif
    ; Remove the active v22 idle graph state as well as its private OAR gates.
    Debug.SendAnimationEvent(actorRef, "IdleForceDefaultState")
    if !V23Current(expected)
        return false
    endif
    Idle previousExit = Game.GetFormFromFile(0x00000803, "DragonsreachBallistae_GuardAnims.esp") as Idle
    if previousExit != None
        actorRef.PlayIdle(previousExit)
    endif
    if !V23Current(expected)
        return false
    endif
    actorRef.SetPosition(px, py, pz)
    if !V23Current(expected)
        return false
    endif
    actorRef.SetAngle(0.0, 0.0, angle+180.0)
    if !V23Current(expected)
        return false
    endif
    ; Only the two owned operators are migrated; retain their armor/inventory.
    actorRef.StopCombat()
    if !V23Current(expected)
        return false
    endif
    actorRef.SheatheWeapon()
    if !V23Current(expected)
        return false
    endif
    actorRef.EvaluatePackage()
    if !V23Current(expected)
        return false
    endif
    Artillero = actorRef
    ownedGuard = None
    pinBusy = false
    sceneBusy = false
    phase = 0
    shotTarget = None
    guardPoseStarted = false
    guardPoseFiring = false
    v23PlacementVersion = 26
    Debug.Trace("Astra guard v26 migrated ref="+actorRef+" station="+Self)
    return true
EndFunction

bool Function PrepareShieldV26(Actor actorRef, int expected)
    if !V23Current(expected) || actorRef == None || actorRef != ResolveV23Operator()
        return false
    endif
    Armor shield = actorRef.GetEquippedShield()
    if !V23Current(expected)
        return false
    endif
    if shield != None
        ; Free the left hand of these two owned operators; keep inventory.
        ; Equipment changes can rebuild 3D. Yield and re-query next pump.
        actorRef.UnequipItem(shield, true, true)
        return false
    endif
    return true
EndFunction

Function PumpV23()
    if v23PumpOwner == v23Generation || !v23Wanted || stationRetired || destroyed
        return
    endif
    int expected = v23Generation
    v23PumpOwner = expected
    bool available = AstraGuardNative.IsAvailable() && AstraGuardNative.GetAPIVersion() == 1
    if !V23Current(expected)
        FinishPumpV23(expected, 0.0)
        return
    endif
    Actor actorRef = ResolveV23Operator()
    if !V23Current(expected)
        FinishPumpV23(expected, 0.0)
        return
    endif
    if actorRef == None || !Is3DLoaded() || !actorRef.Is3DLoaded() || actorRef.IsDead()
        if actorRef == None && !v27WarnedRefs
            ; The v21 incident was exactly this silent loop: Torres.esp absent,
            ; so 0xB70/0xB71 and 0xB80/0xB81 never resolve and nothing traces.
            Debug.Trace("Astra guard v27: operator refs missing; enable DragonsreachBallistae_WhiterunTowers.esp (B70/B71, B80/B81). station="+Self)
            v27WarnedRefs = true
        endif
        if v23Token > 0 && available
            AstraGuardNative.EndOperation(Self, v23Token)
        endif
        FinishPumpV23(expected, 1.0)
        return
    endif
    ; A v22 upgrade must release the old pin/pose even if OAR is unavailable.
    ; v22 has no native token; an existing v23 owner still drains below first.
    if v23PlacementVersion < 26 && v23Token == 0
        bool migratedBeforeAvailability = MigrateV23(actorRef, expected)
    endif
    if !V23Current(expected)
        FinishPumpV23(expected, 0.0)
        return
    endif
    if !available
        if !v23Warned
            Debug.Trace("Astra guard v26: NPC runtime/OAR unavailable; firing disabled.")
            v23Warned = true
        endif
        FinishPumpV23(expected, 2.0)
        return
    endif
    if v23Token > 0
        int status = AstraGuardNative.GetStatus(Self, v23Token)
        if !V23Current(expected)
            FinishPumpV23(expected, 0.0)
            return
        endif
        if status != v23LastStatus
            Debug.Trace("Astra guard v26 status="+status+" station="+Self+" token="+v23Token)
            v23LastStatus = status
        endif
        if status == 1 || status == 2 || status == 3
            v27Faults = 0
            v28RetryWaited = false
        endif
        if status == -1
            ; Clean end of a finished operation; not an acquisition fault.
            v27Faults = 0
            v28RetryWaited = false
            v23Token = 0
        elseif status == -2
            bool drained = AstraGuardNative.EndOperation(Self, v23Token)
            if V23Current(expected) && drained
                v23Token = 0
                v27Faults += 1
                v28RetryWaited = false
            endif
        endif
    endif
    if V23Current(expected) && v23Token == 0
        if v27Faults > 0 && !v28RetryWaited
            ; v27: after a native acquisition fault (status -2 drained), back
            ; off instead of re-beginning every second (v25 churned 134 times).
            ; Fail-closed: the native safety contract is untouched; only the
            ; Papyrus retry cadence slows down.
            float backoff = 5.0
            if v27Faults > 3
                backoff = 30.0
            endif
            Debug.Trace("Astra guard v27: backoff "+backoff+"s after "+v27Faults+" faulted acquisition(s); first clause is logged in AstraSight.log. station="+Self)
            v28RetryWaited = true
            FinishPumpV23(expected, backoff)
            return
        endif
        bool migrated = v23PlacementVersion >= 26
        if !migrated
            migrated = MigrateV23(actorRef, expected)
        endif
        if migrated && V23Current(expected) && v23Serial < 2000000000
            if !PrepareShieldV26(actorRef, expected)
                FinishPumpV23(expected, 0.2)
                return
            endif
            if !V23Current(expected)
                FinishPumpV23(expected, 0.0)
                return
            endif
            v23Serial += 1
            int candidate = v23Serial
            bool accepted = AstraGuardNative.BeginOperation(Self, actorRef, candidate, Launcher, ShotAmmo, ShotSound)
            if V23Current(expected) && accepted
                v23Token = candidate
                v23Warned = false
            elseif accepted
                AstraGuardNative.EndOperation(Self, candidate)
            endif
        endif
    endif
    FinishPumpV23(expected, 1.0)
EndFunction

Function FinishPumpV23(int expected, float delay)
    if v23PumpOwner != expected
        return
    endif
    v23PumpOwner = 0
    if delay > 0.0 && V23Current(expected)
        RegisterForSingleUpdate(delay)
    endif
EndFunction

Function NotifyCombatV23(Actor target)
    if v23Wanted && v23Token > 0 && AstraGuardNative.IsAvailable()
        AstraGuardNative.NotifyCombat(Self, v23Token, target)
    endif
EndFunction
