# Prueba en Skyrim: QA v15

Usar una partida nueva descartable, iniciar con SKSE, núcleo v15 y WhiterunTorres v15 ganando en MO2. Los complementos viejos de ciudad deben estar desactivados.

1. En laboratorio (`coc AstraAsedioTest`) o Atalaya, activar la manivela y disparar un clic corto contra un blanco móvil. Revisar que el proyectil sale al inicio de Fire, sin la espera anterior de varios segundos. Comprobar puntería, cuerda, virote visual, sonido y daño. Repetir con teclado/ratón y un control remapeado.
2. Probar Individual y Continuo, clics durante recarga y botón mantenido al entrar/abrir/cerrar menú. No debe aparecer un tiro viejo al cerrar menú o terminar recarga. Comprobar que cada lanzamiento cobra un virote y que sin munición no dispara. La recarga mínima programada empieza en el lanzamiento y es de 1 s; no mide por sí sola latencia de entrada.
3. Encontrar ambas torres con `cow Tamriel 4 -3` y `cow Tamriel 3 -3`. Recorrer el paso original, observar sus patrullas y destinos intactos. Caminar hasta la plataforma desde el piso vanilla sin usar `tcl`. Revisar especialmente los escalones cortos y el giro alrededor del poste Este. La extensión Oeste debe coincidir con su piso.
4. Activar cada ballesta como jugador: el guardia pasa al punto de espera y el jugador obtiene la mira. Salir con Activar/E: controles y cámara vuelven, arma neutral, guardia al puesto. Repetir y comprobar que no hay dos operadores, un guardia en la base o reserva atascada. Si el guardia murió, el jugador debe poder usarla igualmente.
5. Probar todo el sector −60°/+60° y −20°/+80° contra blancos exteriores. Revisar techo, postes, barandas, cámara, operador y trayectoria real. Los 525 poses estáticos de archivo no cubren todos los movimientos de animación del motor.
6. Abrir menú, guardar/cargar y descargar zona durante entrada, Fire, Reset y salida. No deben quedar controles bloqueados, virote invisible, tiros retrasados, scripts viejos ni guardias duplicados. Probar un fallo de entrada saliendo del acceso o abriendo menú durante la reserva.
7. Provocar combate exterior en esta partida descartable. Los guardias recuperan operación después del jugador y respetan al menos 2,5 s entre lanzamientos. Observar blancos hostiles, postura vanilla, atribución/daño y munición sin explosión. Cruzar durante preparación para revisar cancelación ante el jugador.

## Medir la respuesta

Después de una sesión, buscar en `Documents/My Games/Skyrim Special Edition/SKSE/AstraSight.log`:

```text
shot input admitted ... epoch=... token=... seq=...
shot launch ... input_to_launch_ms=... valid=true charged=true refund=false
```

Comparar la misma combinación epoch/token/seq. `input_to_launch_ms` mide desde la admisión nativa del evento hasta el retorno del lanzamiento; incluye la liberación de ~67 ms y la espera de fotogramas. No mide desde el interruptor físico del ratón ni el primer píxel del proyectil. En Continuo, `repeated=true` corresponde a una repetición admitida después de recarga.

Si falta `shot armed`, registrar los mensajes `fast sight begin`, `sight dropped` y el motivo de rechazo que aparece al activar. Si un lanzamiento tiene `valid=false`, revisar `preflight`, munición y reintegro. Adjuntar ese fragmento de log y una captura de la colocación para ajustar el fallo concreto.

Para conflictos con mods de ciudad, registrar nombre/versión, orden de carga, torre/coordenadas y captura. Se puede desactivar solamente WhiterunTorres para aislarlos; el núcleo y la Atalaya siguen siendo independientes.
