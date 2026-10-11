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
    Inicializar("OnInit")
EndEvent

Event OnLoad()
    ; Una carga a mitad de combate re-despierta la torre: el evento de estado
    ; de combate del guardia no se re-dispara tras el load.
    Inicializar("OnLoad")
    ; Defensa post-save (mismo patrón que OnLoad del ACTI): si la partida se
    ; guardó con el virote escondido a mitad de un ciclo, devolverlo.
    NetImmerse.SetNodeScale(Self, VisualBoltNode, 1.0, false)
    if guardia && guardia.IsInCombat()
        AlertaCombat(guardia.GetCombatTarget())
    endif
EndEvent

Event OnCellDetach()
    ; Celda descargada: dormir sin tocar nodos muertos. Un update pendiente
    ; que dispare después encuentra fase 0 y no re-agenda (el guardia no
    ; combate con su celda descargada, así que la rama de reintento tampoco).
    fase = 0
    blanco = None
    hayPosPrev = false
    if QALog
        Debug.Trace("AstraGuardiaAuto OnCellDetach: torre dormida")
    endif
EndEvent

Function Inicializar(string origen)
    guardia = GetLinkedRef() as Actor
    if QALog
        Debug.Trace("AstraGuardiaAuto " + origen + " guardia=" + guardia)
    endif
    LeerAnguloDeNodos()
    fase = 0
    rafaga = 0
    proximoIntento = 0.0
EndFunction

; =============================================================================
; Entradas del sensor (AstraGuardiaNPC) y del ciclo propio
; =============================================================================
Function AlertaCombat(Actor akBlanco)
    ; La sesión o la demo del jugador SIEMPRE tienen prioridad; si llegara un
    ; aviso durante esa ventana, se reintenta más tarde sin acumular updates.
    if Ocupada() 
        proximoIntento = Utility.GetCurrentRealTime() + 8.0
        if QALog
            Debug.Trace("AstraGuardiaAuto alerta pospuesta: ballesta ocupada")
        endif
        RegisterForSingleUpdate(8.5)
        return
    endif
    if akBlanco != None
        blanco = akBlanco
    endif
    if fase == 0
        fase = 1
        rafaga = 0
        hayPosPrev = false
        ultimoTick = Utility.GetCurrentRealTime()
        RegisterForSingleUpdate(TickSegundos)
        if QALog
            Debug.Trace("AstraGuardiaAuto despierta, blanco=" + blanco)
        endif
    endif
EndFunction

Function CalmaCombat()
    ; El guardia salió de combate: se termina el compromiso al acabar el ciclo
    ; en curso (nunca se aborta una secuencia ya iniciada: quedaría a medias).
    if fase > 0 && fase < 3
        fase = 0
        blanco = None
        if QALog
            Debug.Trace("AstraGuardiaAuto a dormir: fin del combate del guardia")
        endif
    endif
EndFunction

; =============================================================================
; Ciclo por fases (sin bucles: cada fase pide su próximo tick)
; =============================================================================
Event OnUpdate()
    if Ocupada()
        ; El jugador tomó la máquina a mitad de maniobra: ceder YA. El nativo
        ; captura los ángulos actuales como base de su sesión, así que no hay
        ; que restaurar nada; solo reintentar si el guardia sigue en combate.
        if fase == 4
            ; La anim de fuego ya corrió: completar la liberación para que no
            ; quede un disparo fantasma (anim vacía sin proyectil).
            FaseLiberacion()
        endif
        if fase == 4 || fase == 5
            ; Rearmar y devolver el virote visual: la recarga normal no va a
            ; correr (fase pasa a 0), y el ACTI del jugador no restaura la
            ; escala al abrir su sesión.
            PlayGamebryoAnimation("Reset", true)
            NetImmerse.SetNodeScale(Self, VisualBoltNode, 1.0, false)
        endif
        fase = 0
        blanco = None
        hayPosPrev = false
        proximoIntento = Utility.GetCurrentRealTime() + 8.0
        if guardia && guardia.IsInCombat()
            RegisterForSingleUpdate(8.5)
        endif
        return
    endif
    float ahora = Utility.GetCurrentRealTime()
    float dt = ahora - ultimoTick
    if dt < 0.0
        dt = 0.0
    endif
    ultimoTick = ahora
    if fase == 0
        ; Reintento perdido: si este update llega DESPUÉS de que el jugador
        ; soltó la máquina y el guardia sigue en combate, hay que despertar
        ; (el evento de combate del guardia no se re-dispara: su estado no
        ; cambió). Sin esta rama, la torre dormía hasta el próximo combate.
        if guardia && guardia.IsInCombat() && ahora >= proximoIntento
            AlertaCombat(guardia.GetCombatTarget())
        endif
        return
    endif
    if fase == 1
        FaseRastreo(ahora, dt)
    elseif fase == 2
        fase = 3
        RegisterForSingleUpdate(TickSegundos)
    elseif fase == 3
        FaseFuego()
    elseif fase == 4
        FaseLiberacion()
    elseif fase == 5
        FaseRecarga()
    elseif fase == 6
        rafaga = 0
        fase = 1
        RegisterForSingleUpdate(TickSegundos)
    endif
EndEvent

Function FaseRastreo(float ahora, float dt)
    ; El blanco vivo lo decide el combate del guardia, no este script.
    ElegirBlanco()
    string razon = ReglaEnganche()
    if razon != ""
        if QALog
            Debug.Trace("AstraGuardiaAuto no engancha: " + razon)
        endif
        DormirSiCalma(ahora)
        return
    endif
    float[] sol = new float[2]
    if !ResolverBlanco(dt, sol)
        DormirSiCalma(ahora)
        return
    endif
    float solYaw = sol[0]
    float solPitch = sol[1]
    ; Giro suave a velocidades del jugador: la torre apunta como un operador.
    ; El avance del slew se mide contra el tick nominal, no contra el dt real
    ; acumulado en recarga/enfriamiento: tras una pausa la torre NO recupera
    ; el tiempo perdido (avanzaría cientos de grados en un update).
    float dtSlew = dt
    if dtSlew > TickSegundos
        dtSlew = TickSegundos
    endif
    float dyaw = Envolver(solYaw - yawActual)
    float dpitch = solPitch - pitchActual
    float pasoYaw = YawSpeed * dtSlew
    float pasoPitch = PitchSpeed * dtSlew
    if Math.Abs(dyaw) <= pasoYaw
        yawActual = solYaw
    else
        yawActual = yawActual + pasoYaw * Signo(dyaw)
    endif
    if Math.Abs(dpitch) <= pasoPitch
        pitchActual = solPitch
    else
        pitchActual = pitchActual + pasoPitch * Signo(dpitch)
    endif
    AplicarNodos()
    if Math.Abs(Envolver(solYaw - yawActual)) < 1.5 && Math.Abs(solPitch - pitchActual) < 1.5
        ; ASIENTO: un tick completo con los nodos ya quietos para que el grafo
        ; de escena propague la rotación ANTES del disparo (Launcher.Fire lee
        ; el mundo del ProjectileNode; el nativo llama updateWorld explícito,
        ; desde Papyrus garantizamos lo mismo esperando un frame).
        fase = 2
        RegisterForSingleUpdate(TickSegundos)
    else
        RegisterForSingleUpdate(TickSegundos)
    endif
EndFunction

Function FaseFuego()
    string razon = ReglaEnganche()
    if razon != ""
        if QALog
            Debug.Trace("AstraGuardiaAuto disparo abortado: " + razon)
        endif
        fase = 1
        RegisterForSingleUpdate(TickSegundos)
        return
    endif
    if !PlayGamebryoAnimation("Fire", true)
        Debug.Trace("AstraGuardiaAuto FIRE_ANIMATION_FAILED")
        fase = 1
        RegisterForSingleUpdate(1.0)
        return
    endif
    fase = 4
    RegisterForSingleUpdate(ReleaseSegundos)
EndFunction

Function FaseLiberacion()
    ; Espejo de la vía del jugador (AstraAsedioActi.BeginShot): anim Fire ya
    ; en curso, lanzamiento desde ProjectileNode, virote visual oculto y un
    ; solo cue de sonido (Weapon.Fire desde un objeto no suena solo).
    if Launcher == None || ShotAmmo == None
        Debug.Trace("AstraGuardiaAuto PROPIEDADES_FALTAN: Launcher/ShotAmmo sin llenar (¿ESP sin regenerar?)")
        fase = 0
        return
    endif
    Launcher.Fire(Self, ShotAmmo)
    NetImmerse.SetNodeScale(Self, VisualBoltNode, 0.0, false)
    if ShotSound
        ShotSound.Play(Self)
    endif
    rafaga += 1
    fase = 5
    ; Entrar a la recarga YA (la anim Reset se lanza desde FaseRecarga, como
    ; en la vía del jugador: disparo -> Reset inmediato -> esperar): esperar
    ; ResetSegundos aquí lanzaría el rearme tarde y alargaría el ciclo al
    ; doble, con el virote invisible el doble de tiempo.
    RegisterForSingleUpdate(0.05)
EndFunction

Function FaseRecarga()
    ; Reset re-arma el mecanismo. La escala del virote visual la restaura ESTE
    ; script, no la animación: las anim Gamebryo del NIF no tocan escalas
    ; (PyNifly omite las scale keys), y en la vía del jugador quien la sube a
    ; 1.0 es AstraAsedioActi, no la secuencia. Sin esto, la torre quedaría
    ; sin virote visible para siempre tras el primer disparo.
    PlayGamebryoAnimation("Reset", true)
    NetImmerse.SetNodeScale(Self, VisualBoltNode, 1.0, false)
    if rafaga >= MaxRafaga
        fase = 6
        RegisterForSingleUpdate(Enfriamiento)
        if QALog
            Debug.Trace("AstraGuardiaAuto ráfaga completa (" + rafaga + "): enfriando")
        endif
    else
        fase = 1
        RegisterForSingleUpdate(ResetSegundos() + TickSegundos)
    endif
EndFunction

Function DormirSiCalma(float ahora)
    if guardia == None || !guardia.IsInCombat()
        fase = 0
        blanco = None
    elseif ahora < proximoIntento
        RegisterForSingleUpdate(proximoIntento - ahora + 0.25)
    else
        proximoIntento = ahora + 1.0
        RegisterForSingleUpdate(1.25)
    endif
EndFunction

; =============================================================================
; Reglas de enganche: TODO lo que debe ser cierto para apuntar o disparar
; =============================================================================
Function ElegirBlanco()
    if guardia == None
        guardia = GetLinkedRef() as Actor
    endif
    Actor objetivo = guardia.GetCombatTarget()
    if objetivo != None && objetivo != blanco
        blanco = objetivo
        hayPosPrev = false
        if QALog
            Debug.Trace("AstraGuardiaAuto nuevo blanco del guardia: " + blanco)
        endif
    endif
    if blanco != None && blanco.IsDead()
        blanco = objetivo
        hayPosPrev = false
    endif
EndFunction

string Function ReglaEnganche()
    if blanco == None
        return "SIN_BLANCO"
    endif
    if blanco.IsDead()
        return "BLANCO_MUERTO"
    endif
    Actor jugador = Game.GetPlayer()
    ; Nunca al jugador, ni siquiera si el guardia lo tiene como target de
    ; combate (p. ej. el jugador lo agredió): la geometría de seguridad lo
    ; frenaría igual (distancia 0 a la línea de fuego), pero es una regla
    ; explícita y no un efecto colateral.
    if blanco == jugador
        return "BLANCO_JUGADOR"
    endif
    ; Solo se dispara a quien es hostil para el jugador o para el guardia:
    ; nunca a aliados, neutrales ni al propio jugador.
    if !blanco.IsHostileToActor(jugador) && !(guardia && blanco.IsHostileToActor(guardia))
        return "NO_HOSTIL"
    endif
    ; Detección: la vista del guardia es el control de línea de visión del
    ; híbrido (la detección vanilla incluye LOS). Sin guardia vivo, solo se
    ; confía en blancos ya comprometidos y cercanos.
    if guardia && guardia.IsDead()
        guardia = None
    endif
    if guardia
        if !blanco.IsDetectedBy(guardia)
            return "SIN_LINEA_GUARDIA"
        endif
    elseif blanco.GetDistance(Self) > 4000.0
        return "SIN_GUARDIA_LEJOS"
    endif
    float dx = blanco.GetPositionX() - GetPositionX()
    float dy = blanco.GetPositionY() - GetPositionY()
    float dist = Math.Sqrt(dx*dx + dy*dy)
    if dist < AlcanceMin
        return "DEMASIADO_CERCA"
    endif
    if dist > AlcanceMax
        return "DEMASIADO_LEJOS"
    endif
    ; Arco de tiro frontal: la boca apunta a -Y en reposo; se descentra el
    ; rumbo para no barrer la escalera ni la zona del operador.
    float rumbo = Math.Abs(Envolver(Grados(Atan2(dx, -dy))))
    if rumbo > ArcMax
        return "FUERA_DE_ARCO"
    endif
    ; Geometría de seguridad: nadie del bando propio en la línea de fuego ni
    ; cerca del punto de impacto (la explosión del virote tiene 128 u).
    if !LineaSegura(jugador) 
        return "JUGADOR_EN_LINEA"
    endif
    if guardia && !LineaSegura(guardia)
        return "GUARDIA_EN_LINEA"
    endif
    if jugador.GetDistance(blanco) < MargenImpacto
        return "JUGADOR_CERCA_DEL_BLANCO"
    endif
    if guardia && guardia.GetDistance(blanco) < MargenImpacto
        return "GUARDIA_CERCA_DEL_BLANCO"
    endif
    return ""
EndFunction

bool Function LineaSegura(Actor quien)
    ; Distancia 2D del actor al segmento boca->blanco (proyección con clamp).
    ; Seguro = lejos de la línea Y lejos del blanco: el "||" sería un bug
    ; (marcaría "seguro" a quien pelea en melee contra el blanco, y el virote
    ; de asedio con radio 128 lo mataría). El margen de explosión completo
    ; (MargenImpacto) lo aplican los checks dedicados de ReglaEnganche.
    float ax = GetPositionX()
    float ay = GetPositionY()
    float bx = blanco.GetPositionX()
    float by = blanco.GetPositionY()
    float px = quien.GetPositionX()
    float py = quien.GetPositionY()
    float abx = bx - ax
    float aby = by - ay
    float ab2 = abx*abx + aby*aby
    float t = 0.0
    if ab2 > 0.0001
        t = ((px - ax)*abx + (py - ay)*aby) / ab2
    endif
    if t < 0.0
        t = 0.0
    elseif t > 1.0
        t = 1.0
    endif
    float cx = ax + abx*t
    float cy = ay + aby*t
    float dx = px - cx
    float dy = py - cy
    return Math.Sqrt(dx*dx + dy*dy) > MargenLinea && quien.GetDistance(blanco) > 200.0
EndFunction

; =============================================================================
; Balística: mismo proyectil, misma matemática que el registro v08 de sight
; zero (tests/test_v08_sight_zero.py re-deriva 5400 u/s y 240.345 u/s^2).
; =============================================================================
bool Function ResolverBlanco(float dt, float[] sol)
    ; Escribe el apuntado en `sol` (2 elementos) y devuelve true; false si no hay
    ; solucion. El array va por parametro a proposito: un `float[]` de retorno que
    ; pueda ser None obliga al compilador a emitir `Cast float[] None`, que el gate
    ; de compile_papyrus rechaza y que en el VM envenena ArrayCreate. Y devolver un
    ; array vacio no es opcion: Papyrus exige entre 1 y 128 elementos (`new float[0]`
    ; no compila).
    ; Posición futura aproximada del blanco. Papyrus no tiene GetVelocity:
    ; la velocidad se MIDE entre ticks (posición actual vs. anterior).
    float tx = blanco.GetPositionX()
    float ty = blanco.GetPositionY()
    float tz = blanco.GetPositionZ()
    if Anticipacion > 0.0
        float vx = 0.0
        float vy = 0.0
        float vz = 0.0
        if hayPosPrev && dt > 0.016
            vx = (tx - xPrev) / dt
            vy = (ty - yPrev) / dt
            vz = (tz - zPrev) / dt
        endif
        xPrev = tx
        yPrev = ty
        zPrev = tz
        hayPosPrev = true
        float dist = Math.Sqrt((tx - GetPositionX())*(tx - GetPositionX()) + (ty - GetPositionY())*(ty - GetPositionY()))
        float tVuelo = dist / (VelocidadProyectil * 0.99)
        tx += vx * tVuelo * Anticipacion
        ty += vy * tVuelo * Anticipacion
        tz += vz * tVuelo * Anticipacion
    endif
    ; La boca del arma en mundo (la celda de pruebas coloca la raíz a 0 grados;
    ; generalizar leyendo el nodo si se instala en otro emplazamiento).
    float mx = GetPositionX()
    float my = GetPositionY() + MuzzleAdelante
    float mz = GetPositionZ() + MuzzleAlto
    float dx = tx - mx
    float dy = ty - my
    float d = Math.Sqrt(dx*dx + dy*dy)
    if d < 1.0
        return false
    endif
    ; Solución balística (tiro bajo) para un blanco a altura relativa
    ; dzRel = altura del BLANCO sobre la boca (negativa si está más abajo,
    ; que es lo normal desde una torre):
    ;   tan(p) = (v^2 - sqrt(v^4 - g*(g*d^2 + 2*dzRel*v^2))) / (g*d)
    ; OJO al signo: el término lleva la altura del BLANCO sobre la boca, no
    ; al revés. Con dzRel < 0 el discriminante se relaja y el ángulo baja.
    ; (Verificado contra integración del vuelo: z(t_llegada) == dzRel.)
    ; Devuelve un array VACIO (length 0) si no llega: nunca None, para no emitir Cast float[] None.
    float dzRel = tz - mz
    float v2 = VelocidadProyectil * VelocidadProyectil
    float disc = v2*v2 - GravedadProyectil*(GravedadProyectil*d*d + 2.0*dzRel*v2)
    if disc < 0.0
        if QALog
            Debug.Trace("AstraGuardiaAuto fuera de alcance balístico")
        endif
        return false
    endif
    float tanP = (v2 - Math.Sqrt(disc)) / (GravedadProyectil * d)
    float solPitch = Grados(Math.Atan(tanP))
    if solPitch < PitchMin || solPitch > PitchMax
        if QALog
            Debug.Trace("AstraGuardiaAuto elevación " + solPitch + " fuera de (" + PitchMin + ", " + PitchMax + ")")
        endif
        return false
    endif
    ; gunDirection del nativo: (sin(y)cos(p), -cos(y)cos(p), sin(p)); para
    ; apuntar a (dx, dy): sin(y) = dx/L y cos(y) = -dy/L.
    sol[0] = Grados(Atan2(dx, -dy))
    sol[1] = solPitch
    return true
EndFunction

; =============================================================================
; Nodos: matrices fila-major idénticas a las del nativo (Plugin.cpp).
; yaw -> rz(r) filas [c,-s,0][s,c,0][0,0,1]; pitch -> rx(-p) filas
; [1,0,0][0,cp,sp][0,-sp,cp]. El reposo de ambos nodos es la identidad.
; =============================================================================
Function AplicarNodos()
    float[] m = new float[9]
    float r = Radianes(yawActual)
    float c = Math.Cos(r)
    float s = Math.Sin(r)
    m[0] = c
    m[1] = -s
    m[2] = 0.0
    m[3] = s
    m[4] = c
    m[5] = 0.0
    m[6] = 0.0
    m[7] = 0.0
    m[8] = 1.0
    NetImmerse.SetNodeLocalRotationMatrix(Self, YawNode, m, false)
    r = Radianes(-pitchActual)
    c = Math.Cos(r)
    s = Math.Sin(r)
    m[0] = 1.0
    m[1] = 0.0
    m[2] = 0.0
    m[3] = 0.0
    m[4] = c
    m[5] = -s
    m[6] = 0.0
    m[7] = s
    m[8] = c
    NetImmerse.SetNodeLocalRotationMatrix(Self, PitchNode, m, false)
EndFunction

Function LeerAnguloDeNodos()
    ; Recuperar el apuntado tras un load: el ángulo se LEE del nodo (así la
    ; torre parte del último rumbo del jugador, no de un supuesto).
    float[] m = new float[9]
    if NetImmerse.GetNodeLocalRotationMatrix(Self, YawNode, m, false) && m.Length == 9
        ; AplicarNodos escribe m[0]=cos, m[3]=sin: atan2(m[3], m[0]) devuelve el yaw.
        ; Atan2 es un helper DE ESTE SCRIPT (abajo), no de Math: Math solo tiene Atan.
        yawActual = Grados(Atan2(m[3], m[0]))
    endif
    if NetImmerse.GetNodeLocalRotationMatrix(Self, PitchNode, m, false) && m.Length == 9
        ; AplicarNodos escribe rx(-pitch): m[4]=cos(p), m[5]=+sin(p). El pitch
        ; es atan2(m[5], m[4]) DIRECTO (con el signo de m[5] invertido se
        ; recuperaba negado y el slew saltaba tras cada load).
        pitchActual = Grados(Atan2(m[5], m[4]))
    endif
    if QALog
        Debug.Trace("AstraGuardiaAuto ángulos de nodo: yaw=" + yawActual + " pitch=" + pitchActual)
    endif
EndFunction

; =============================================================================
; Utilidades
; =============================================================================
bool Function Ocupada()
    return OcupadaGuardia != None && OcupadaGuardia.GetValue() == 1
EndFunction

float Function ResetSegundos()
    ; 1.2 s de Reset + margen de un tick para que la secuencia asiente.
    return 1.2 + TickSegundos
EndFunction

float Function Envolver(float angulo)
    ; A (-180, 180].
    while angulo > 180.0
        angulo -= 360.0
    endWhile
    while angulo <= -180.0
        angulo += 360.0
    endWhile
    return angulo
EndFunction

float Function Signo(float v)
    if v < 0.0
        return -1.0
    endif
    return 1.0
EndFunction

float Function Grados(float rad)
    return rad * 57.2957795131
EndFunction

float Function Radianes(float deg)
    return deg * 0.0174532925
EndFunction

float Function Atan2(float dy, float dx)
    ; Papyrus no trae atan2; cuadrantes completos, dx = 0 incluido.
    if dx > 0.0
        return Math.Atan(dy / dx)
    elseif dx < 0.0
        if dy >= 0.0
            return Math.Atan(dy / dx) + 3.14159265359
        else
            return Math.Atan(dy / dx) - 3.14159265359
        endif
    elseif dy >= 0.0
        return 1.57079632679
    else
        return -1.57079632679
    endif
EndFunction
