# Guardias v29 — control simplificado

## Problema

Los guardias levantan los brazos pero no llegan a agarrar la ballesta, y nunca apuntan ni disparan. Se midió lo siguiente:

- **Recursos correctos.** Aplicado al `skeleton.hkx` vanilla, el HKX de sostener deja las muñecas a 0,02 u de `(±33,6; 143,8; 100,5)` en el espacio de la ballesta. `ballesta_guardia.nif` tiene la geometría de las empuñaduras exactamente en `(±33,6; 137,9; 101,67)`. Lo instalado en MO2 coincide byte a byte con el repo.
- **Grafo vanilla.** El evento `IdleHandsBehindBack` (id 482 de `mt_behavior.hkx`) entra a su estado con una mezcla de 0,5 s. `IdleForceDefaultState` vuelve al reposo con 0,2 s. El subgrafo está formado solo por máquinas de estado, sin pesos de hueso, así que la animación se aplica al cuerpo completo.
- **Fallo en runtime.** Apuntar y disparar exigen `gripConfirmed`, que nunca se cumplió en una partida: el log de v27 registra 7 confirmaciones OAR, 0 agarres y 0 virotes. Las muestras OAR deben llegar en menos de 2 frames; si no, se relanza la animación pasando por el reposo, y tras dos intentos se cancela todo. En v28, el agarre cancela si las manos quedan a más de 16 u, algo seguro durante la entrada de 0,5 s, cuando arrancan a unas 29 u.

## Principio

**La animación es la que agarra.** Si el guardia está en `(0, 151, 0)` mirando a −Y respecto de la ballesta y el clip de sostener está activo, las manos quedan sobre las empuñaduras. El runtime solo mueve el conjunto ballesta+guardia como un sólido rígido. La telemetría de animación se registra pero nunca bloquea ni cancela.

## Comportamiento v29

1. **Adquisición.** Sin cambios: paquete B90, armas guardadas, sin escudo, órbita de 151 u, facciones OAR y `PlayIdle(AstraGuardOperateIdle)`.
2. **Entrada.** El estado pasa a 1 (sosteniendo) cuando se cumplen 0,6 s desde la solicitud (0,5 s de mezcla vanilla más margen). No se exige ninguna muestra OAR.
3. **Vigilancia del clip.** Cada muestra OAR del clip propio, con época y personaje correctos, actualiza `lastHoldSeen`. Si pasan más de 3 s sin muestras y no hubo otra reemisión en los últimos 6 s, se reemite el idle una sola vez. Nunca se cancela por este motivo.
4. **Seguimiento.** Para el objetivo elegido por `selectGuardTarget`, el yaw avanza hacia el deseado a 20°/s como máximo, limitado a ±60°. La ballesta y el guardia giran juntos con `pose()`, sin clips de giro ni IK de pies, y los pies se deslizan. Si una pose nueva queda obstruida o sin apoyo, se mantiene el yaw anterior en vez de cancelar.
5. **Disparo.** El objetivo tiene que ser un enemigo hostil en combate, alcanzable con tiro horizontal, con error de yaw ≤ 0,25° y fuera de enfriamiento (2,5 s). En ese caso `shoot()` aplica todas las comprobaciones de seguridad existentes: visibilidad, trayectoria completa, actores protegidos y contrato del proyectil. Si pasan, lanza el virote y activa `Fire` y, a los 0,2 s, `Reset` del NIF. No hay clip corporal de disparo ni sincronización de fase.
6. **Pausa y menús.** Mientras el juego está pausado o hay un menú bloqueante, el slot no se actualiza y no se cancela. Solo `Loading Menu`, la carga, la partida nueva y el revert invalidan.
7. **Hitch.** Un `dt` mayor que 0,1 s ya no cancela. El paso de seguimiento usa `dt` acotado a 0,05 s.

## Se conserva

- Toda la seguridad del disparo y la protección del jugador y los aliados.
- La política de objetivos: sigue al jugador y a los no residentes, ignora a los residentes y guardias de Whiterun que no son hostiles, y dispara solo a enemigos en combate.
- La cesión del puesto al jugador, la cancelación por muerte, stagger, descarga o cambio de celda, y el ciclo Papyrus v28 (reintento acotado).
- Los ESP, NIF, HKX y la configuración OAR, sin cambios. Los clips de giro y de disparo quedan instalados pero el runtime no los usa.

## Telemetría

`guard v29 pose`, una vez cada 2 s por puesto, registra yaw, yaw deseado, objetivo, la última muestra OAR (clip, fase, antigüedad) y la distancia de cada muñeca a su empuñadura. Solo mide y no corrige. Sirve para comprobar en el juego que las manos quedan a unas 3 u de las empuñaduras; la diferencia esperada se debe a la escala 1,03.

## Límites

- Los pies se deslizan al girar. Es lo que aceptaba el contrato original del clip.
- Con escala 1,03 de la raza nórdica, las muñecas quedan a unas 3 u de la empuñadura.
- No hay gesto corporal al disparar; la mano derecha se mueve menos de 1 u en el clip original.
- La prueba en el juego queda pendiente: los tests externos no la reemplazan.
