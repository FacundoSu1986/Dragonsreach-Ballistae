Scriptname AstraGuardiaAuto extends ObjectReference
; =============================================================================
; IA de la torre Astra (modo híbrido): la ballesta se defiende sola mientras
; el guardia NPC la opera. El GUARDIA es el sensor: su combate vanilla decide
; cuándo hay amenaza (AstraGuardiaNPC le avisa); esta ballesta es el arma.
;
; Apunta rotando CTRL_GIRO_360 / CTRL_ELEVACION con NetImmerse
; (SetNodeLocalRotationMatrix, matrices fila-major 3x3 idénticas a las del
; nativo AstraSight: yaw -> rz(yaw), pitch -> rx(-pitch), reposo = identidad)
; y dispara el virote REAL (Launcher.Fire desde ProjectileNode) tras resolver
; la balística del propio proyectil (velocidad 5400 u/s, gravedad efectiva
; 0.35*9.81*70 = 240.345 u/s^2: PROJ speed y gravedad del donante, ver Core.cpp).
;
; Buenas prácticas aplicadas:
; - Sin bucles: RegisterForSingleUpdate por fase; DURMIENDO no registra nada
;   (el despertar es por evento desde el guardia).
; - Sin estado persistente frágil: la fase y el objetivo se re-derivan del
;   mundo en OnInit/OnLoad (guardia en combate) y de los propios nodos (el
;   ángulo actual se LEE del nodo, no se asume).
; - Ningún paso destructivo sin revalidar TODAS las reglas de enganche:
;   hostilidad, detección, arco, alcance, elevación, y geometría de seguridad
;   del jugador y del guardia (distancia a la línea de fuego y al impacto).
; - Cede la máquina SIEMPRE que la use el jugador o corra la demo
;   (GlobalVariable AstraGuardiaOcupada, en 1 durante sesión y demo).
; - Propiedades con valores por defecto sanos: el script funciona incluso con
;   un ESP viejo que no las llene (las de form en None se degradan con traza).
;
; Fases: 0 DURMIENDO · 1 RASTREO (apunta con giro suave) · 2 ASIENTO (un tick
; para que el grafo de escena propague la rotación) · 3 FUEGO (anim Fire) ·
; 4 LIBERACIÓN (proyectil real) · 5 RECARGA (anim Reset) · 6 ENFRIAMIENTO.
; =============================================================================

; --- forms (los llena build_plugin; degradan con traza si faltan) ---
Weapon Property Launcher Auto          ; lanzavirotes (dispara desde ProjectileNode)
Ammo Property ShotAmmo Auto            ; munición no jugable de la propia torre
Sound Property ShotSound Auto          ; WPNCrossbowFire, como la vía del jugador
GlobalVariable Property OcupadaGuardia Auto  ; 1 = sesión o demo del jugador

; --- nodos (mismos nombres que AstraAsedioActi) ---
string Property YawNode = "CTRL_GIRO_360" Auto
string Property PitchNode = "CTRL_ELEVACION" Auto
string Property VisualBoltNode = "VIROTE_VISUAL" Auto

; --- balística del proyectil (PROJ donante; ver docs/guardia_ai.md) ---
float Property VelocidadProyectil = 5400.0 Auto
float Property GravedadProyectil = 240.345 Auto  ; 0.35*9.81*70
float Property MuzzleAlto = 136.6 Auto       ; z del ProjectileNode sobre la raíz (v22: 172.6 - 36)
float Property MuzzleAdelante = -224.0 Auto  ; y del ProjectileNode sobre la raíz

; --- límites mecánicos (espejo de AstraAsedioActi) ---
float Property YawSpeed = 40.0 Auto          ; grados/segundo del giro
float Property PitchSpeed = 20.0 Auto
float Property PitchMin = -5.0 Auto
float Property PitchMax = 80.0 Auto

; --- reglas de enganche (disparo con daño real: conservadoras) ---
float Property ArcMax = 60.0 Auto            ; |rumbo| máximo desde el frente (-Y)
float Property AlcanceMin = 900.0 Auto       ; más cerca no se puede deprimir
float Property AlcanceMax = 8400.0 Auto      ; 120 m
float Property MargenLinea = 320.0 Auto      ; jugador/guardia más cerca de la línea: no se dispara
float Property MargenImpacto = 384.0 Auto    ; radio de la explosión (128) * 3
int Property MaxRafaga = 3 Auto              ; tiros por compromiso antes de enfriar
float Property Enfriamiento = 8.0 Auto
float Property Anticipacion = 0.5 Auto       ; 0 = apunta a donde está el blanco
float Property ReleaseSegundos = 0.1 Auto
float Property TickSegundos = 0.12 Auto
bool Property QALog = false Auto

; --- estado (transitorio: todo se recupera del mundo) ---
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
; Entradas del sensor (AstraGuardiaNPC) y del ciclo propio
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
; Ciclo por fases (sin bucles: cada fase pide su próximo tick)
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
; Reglas de enganche: TODO lo que debe ser cierto para apuntar o disparar
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
; Balística: mismo proyectil, misma matemática que el registro v08 de sight
; zero (tests/test_v08_sight_zero.py re-deriva 5400 u/s y 240.345 u/s^2).
; =============================================================================
bool Function ResolverBlanco(float dt, float[] sol)
    ; v23 retired actuator; retained for existing saved instances.
    return false
EndFunction

; =============================================================================
; Nodos: matrices fila-major idénticas a las del nativo (Plugin.cpp).
; yaw -> rz(r) filas [c,-s,0][s,c,0][0,0,1]; pitch -> rx(-p) filas
; [1,0,0][0,cp,sp][0,-sp,cp]. El reposo de ambos nodos es la identidad.
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
; Utilidades
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
