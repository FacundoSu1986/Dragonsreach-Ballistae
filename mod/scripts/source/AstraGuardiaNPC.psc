Scriptname AstraGuardiaNPC extends Actor
; =============================================================================
; Guardia de la torre Astra (la mitad "humana" del híbrido).
;
; Su IA de presencia y combate es 100% vanilla: paquetes del NPC clonado del
; donante (sandbox en la ubicación del editor) y combate estándar del motor.
; Este script SOLO es el sensor de la torre: traduce su estado de combate a
; la interfaz de AstraGuardiaAuto (AlertaCombat / CalmaCombat) a través del
; linked ref (XLKR hacia la referencia de la ballesta, definido en el ESP).
;
; Buenas prácticas: cero sondeo (todo por eventos), sin estado propio que
; guardar, propiedades ninguna (todo por linked ref), y re-sincronización al
; cargar partida (el evento de combate no se re-dispara tras un load).
; =============================================================================

AstraGuardiaAuto Function Torre()
    ObjectReference enlace = GetLinkedRef()
    if enlace == None
        Debug.Trace("AstraGuardiaNPC SIN_ENLACE: el NPC no tiene linked ref a la ballesta (¿ESP sin regenerar?)")
        return None
    endif
    return enlace as AstraGuardiaAuto
EndFunction

Event OnInit()
    ; Traza de armado: si el linked ref falta, se ve en el log al primer load.
    AstraGuardiaAuto torre = Torre()
    if torre == None
        Debug.Trace("AstraGuardiaNPC enlace no resuelve a AstraGuardiaAuto")
    endif
EndEvent

Event OnLoad()
    ; Save a mitad de combate: el estado de combate no re-dispara eventos,
    ; la torre se despierta a mano desde aquí.
    if IsInCombat()
        AstraGuardiaAuto torre = Torre()
        if torre
            torre.AlertaCombat(GetCombatTarget())
        endif
    endif
EndEvent

Event OnCombatStateChanged(Actor akTarget, int aeCombatState)
    AstraGuardiaAuto torre = Torre()
    if torre == None
        return
    endif
    if aeCombatState == 1 || aeCombatState == 2
        ; Buscar/pelear: la torre engancha al objetivo del guardia.
        torre.AlertaCombat(akTarget)
    elseif aeCombatState == 0
        ; Fin del combate: la torre termina su ciclo en curso y duerme.
        torre.CalmaCombat()
    endif
EndEvent

Event OnDeath(Actor akKiller)
    ; Sin guardia no hay sensor: la torre cesa (las reglas de enganche de la
    ; propia torre degradan a un modo corto si igualmente llega un aviso).
    AstraGuardiaAuto torre = Torre()
    if torre
        torre.CalmaCombat()
    endif
EndEvent
