Scriptname AstraGuardiaAuto extends ObjectReference
; =============================================================================
; Astra tower AI (hybrid mode): the ballista defends itself while
; the guard NPC operates it. The GUARD is the sensor: its vanilla combat decides
; when there is a threat (AstraGuardiaNPC tells it); this ballista is the weapon.
;
; Aims by rotating CTRL_GIRO_360 / CTRL_ELEVACION with NetImmerse
; (SetNodeLocalRotationMatrix, row-major 3x3 matrices identical to those of the
; native AstraSight: yaw -> rz(yaw), pitch -> rx(-pitch), rest = identity)
; and fires the REAL bolt (Launcher.Fire from ProjectileNode) after solving
; the projectile's own ballistics (speed 5400 u/s, effective gravity
; 0.35*9.81*70 = 240.345 u/s^2: donor PROJ speed and gravity, see Core.cpp).
;
; Good practices applied:
; - No loops: RegisterForSingleUpdate per phase; SLEEPING registers nothing
;   (waking up is an event sent by the guard).
; - No fragile persistent state: phase and target are re-derived from the
;   world in OnInit/OnLoad (guard in combat) and from the nodes themselves (the
;   current angle is READ from the node, not assumed).
; - No destructive step without revalidating ALL engagement rules:
;   hostility, detection, arc, range, elevation, and safety geometry
;   of the player and the guard (distance to the line of fire and to the impact).
; - Yields the machine WHENEVER the player uses it or the demo runs
;   (GlobalVariable AstraGuardiaOcupada, 1 during session and demo).
; - Properties with sane defaults: the script works even with
; an old ESP that does not fill them (form ones left None degrade with a trace).
;
; Phases: 0 SLEEPING - 1 TRACKING (aims with a smooth turn) - 2 SETTLE (one tick
; for the scene graph to propagate the rotation) - 3 FIRE (anim Fire) -
; 4 RELEASE (real projectile) - 5 RELOAD (anim Reset) - 6 COOLDOWN.
; =============================================================================

; --- forms (filled by build_plugin; degrade with a trace if missing) ---
Weapon Property Launcher Auto          ; bolt launcher (fires from ProjectileNode)
Ammo Property ShotAmmo Auto            ; the tower's own non-playable ammo
Sound Property ShotSound Auto          ; WPNCrossbowFire, like the player's path
GlobalVariable Property OcupadaGuardia Auto  ; 1 = player session or demo

; --- nodes (same names as AstraAsedioActi) ---
string Property YawNode = "CTRL_GIRO_360" Auto
string Property PitchNode = "CTRL_ELEVACION" Auto
string Property VisualBoltNode = "VIROTE_VISUAL" Auto

; --- projectile ballistics (donor PROJ; see docs/guardia_ai.md) ---
float Property VelocidadProyectil = 5400.0 Auto
float Property GravedadProyectil = 240.345 Auto  ; 0.35*9.81*70
float Property MuzzleAlto = 136.6 Auto       ; ProjectileNode z over the root (v22: 172.6 - 36)
float Property MuzzleAdelante = -224.0 Auto  ; ProjectileNode y over the root

; --- mechanical limits (mirror of AstraAsedioActi) ---
float Property YawSpeed = 40.0 Auto          ; turn degrees per second
float Property PitchSpeed = 20.0 Auto
float Property PitchMin = -5.0 Auto
float Property PitchMax = 80.0 Auto

; --- engagement rules (shots deal real damage: conservative) ---
float Property ArcMax = 60.0 Auto            ; max |heading| from the front (-Y)
float Property AlcanceMin = 900.0 Auto       ; closer than this the barrel cannot depress
float Property AlcanceMax = 8400.0 Auto      ; 120 m
float Property MargenLinea = 320.0 Auto      ; player/guard closer to the line: no shot
float Property MargenImpacto = 384.0 Auto    ; explosion radius (128) * 3
int Property MaxRafaga = 3 Auto              ; shots per engagement before cooling down
float Property Enfriamiento = 8.0 Auto
float Property Anticipacion = 0.5 Auto       ; 0 = aim where the target is
float Property ReleaseSegundos = 0.1 Auto
float Property TickSegundos = 0.12 Auto
bool Property QALog = false Auto

; --- state (transient: everything is recovered from the world) ---
int fase = 0
Actor blanco = None
Actor guardia = None
int rafaga = 0
float yawActual = 0.0
float pitchActual = 0.0
float ultimoTick = 0.0
float proximoIntento = 0.0
float xPrev = 0.0
float yPrev = 0.0
float zPrev = 0.0
bool hayPosPrev = false

Event OnInit()
    UnregisterForUpdate()
EndEvent

Event OnLoad()
    UnregisterForUpdate()
EndEvent

Event OnCellDetach()
    UnregisterForUpdate()
EndEvent

Function Inicializar(string origen)
    ; v23 retired actuator; retained for existing saved instances.
    UnregisterForUpdate()
EndFunction

; =============================================================================
; Inputs from the sensor (AstraGuardiaNPC) and from the own cycle
; =============================================================================
Function AlertaCombat(Actor akBlanco)
    ; v23 retired actuator; retained for existing saved instances.
    ObjectReference stationRef = Self
    AstraAsedioGuard controller = stationRef as AstraAsedioGuard
    if controller != None
        controller.NotifyCombatV23(akBlanco)
    endif
    UnregisterForUpdate()
EndFunction

Function CalmaCombat()
    ; v23 retired actuator; retained for existing saved instances.
    UnregisterForUpdate()
EndFunction

; =============================================================================
; Phase cycle (no loops: each phase requests its next tick)
; =============================================================================
Event OnUpdate()
    UnregisterForUpdate()
EndEvent

Function FaseRastreo(float ahora, float dt)
    ; v23 retired actuator; retained for existing saved instances.
    UnregisterForUpdate()
EndFunction

Function FaseFuego()
    ; v23 retired actuator; retained for existing saved instances.
    UnregisterForUpdate()
EndFunction

Function FaseLiberacion()
    ; v23 retired actuator; retained for existing saved instances.
    UnregisterForUpdate()
EndFunction

Function FaseRecarga()
    ; v23 retired actuator; retained for existing saved instances.
    UnregisterForUpdate()
EndFunction

Function DormirSiCalma(float ahora)
    ; v23 retired actuator; retained for existing saved instances.
    UnregisterForUpdate()
EndFunction

; =============================================================================
; Engagement rules: EVERYTHING that must hold to aim or fire
; =============================================================================
Function ElegirBlanco()
    ; v23 retired actuator; retained for existing saved instances.
    UnregisterForUpdate()
EndFunction

string Function ReglaEnganche()
    ; v23 retired actuator; retained for existing saved instances.
    UnregisterForUpdate()
EndFunction

bool Function LineaSegura(Actor quien)
    ; v23 retired actuator; retained for existing saved instances.
    return false
EndFunction

; =============================================================================
; Ballistics: same projectile, same math as the v08 sight-zero record
; (tests/test_v08_sight_zero.py re-derives 5400 u/s and 240.345 u/s^2).
; =============================================================================
bool Function ResolverBlanco(float dt, float[] sol)
    ; v23 retired actuator; retained for existing saved instances.
    return false
EndFunction

; =============================================================================
; Nodes: row-major matrices identical to the native ones (Plugin.cpp).
; yaw -> rz(r) rows [c,-s,0][s,c,0][0,0,1]; pitch -> rx(-p) rows
; [1,0,0][0,cp,sp][0,-sp,cp]. The rest pose of both nodes is the identity.
; =============================================================================
Function AplicarNodos()
    ; v23 retired actuator; retained for existing saved instances.
    UnregisterForUpdate()
EndFunction

Function LeerAnguloDeNodos()
    ; v23 retired actuator; retained for existing saved instances.
    UnregisterForUpdate()
EndFunction

; =============================================================================
; Utilities
; =============================================================================
bool Function Ocupada()
    ; v23 retired actuator; retained for existing saved instances.
    return false
EndFunction

float Function ResetSegundos()
    ; v23 retired actuator; retained for existing saved instances.
    return 0
EndFunction

float Function Envolver(float angulo)
    ; v23 retired actuator; retained for existing saved instances.
    return 0
EndFunction

float Function Signo(float v)
    ; v23 retired actuator; retained for existing saved instances.
    return 0
EndFunction

float Function Grados(float rad)
    ; v23 retired actuator; retained for existing saved instances.
    return 0
EndFunction

float Function Radianes(float deg)
    ; v23 retired actuator; retained for existing saved instances.
    return 0
EndFunction

float Function Atan2(float dy, float dx)
    ; v23 retired actuator; retained for existing saved instances.
    return 0
EndFunction
