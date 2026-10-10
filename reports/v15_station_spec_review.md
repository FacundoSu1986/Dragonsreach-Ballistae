# Revisión independiente de especificación Station/Guard v15

Fecha: 2026-10-09. Revisión de sólo lectura de AstraAsedioStation y AstraAsedioGuard, con seguimiento de sus llamadas a AstraAsedioActi, Session y el fence nativo ya revisado. Únicas escrituras de este revisor: los informes de revisión autorizados. No se modificaron PSC/PEX, plugins, geometría, runtime, MO2 ni vendor. No se lanzó Skyrim.

## Dictamen

**APROBADO el código de coordinación revisado, sin hallazgos P1/P2 abiertos.** El dictamen es sobre reservas, cancelación y devolución de propiedad. Las posiciones físicas fuera del corredor original, enlaces VMAD, sectores asignados a las referencias y la activación real de ambos puestos requieren la revisión posterior del plugin/plataformas y la prueba de motor; no quedan acreditados por esta revisión de scripts.

## Contratos comprobados

- La estación hereda el controlador de jugador y sólo acepta al jugador como actor de activación. Comprueba SKSE/AstraSight 3.5.0/API4 antes de reservar al guardia. Un requisito nativo fallido no deja controles deshabilitados ni una reserva esperando un binding inexistente.
- El slot stationBusy se conserva a través de llamadas y consultas externas; revisión, coordinador y lease se capturan juntos. No hay una segunda reserva mientras una entrada/liberación antigua puede regresar. Cambiar la propiedad Guard no redirige la devolución del lease capturado a otro coordinador.
- ReservePlayerLease invalida el seguimiento/disparo del guardia antes de Shutdown. PreparePlayerLease espera pinBusy/sceneBusy, las compensaciones anteriores y ausencia de propiedad/limpieza nativa. Sólo después neutraliza los controles compartidos, traslada el artillero configurado a Standby y completa su pin. El jugador no puede entrar antes de esas llamadas pendientes. Un artillero muerto, deshabilitado o ausente permite el manejo del jugador; el jugador configurado accidentalmente como artillero se rechaza.
- La revisión y el contexto del jugador se validan antes y después de Prepare y ResetStationAim: carga del arma, menú, muerte, plazo y reloj finito/no rebobinado. La ventana de 3 s empieza al retornar Reserve; es una condición de admisión, no una promesa de planificación Papyrus o de duración máxima de las llamadas nativas.
- Un menú durante espera, unload/cell detach, destrucción, muerte observada, timeout o carga drenan la reserva. El lease que retorna después de cancelar Reserve se conserva para liberarlo; una entrada tardía del padre se vuelve a drenar al retornar. Load no ejecuta Parent.OnLoad ni captura/escribe la escena compartida mientras el guardia puede poseerla.
- EndSession invalida primero la revisión de la estación y ejecuta End del padre. PollStationRelease exige que el padre ya no opere, que no tenga cleanup pendiente y que IsEffectsQuiescent(Self,0) confirme ausencia de propietario/efectos nativos. Sólo entonces devuelve el lease capturado y permite otra adquisición. El guardia ignora una devolución antigua después de load o una reserva nueva.
- El guardia mantiene generación/token y slots de mutación durante sus efectos y compensaciones. Un efecto viejo de pin/animación/rotación no libera un slot nuevo ni puede reanudar seguimiento durante playerReserved. Su recuperación consulta también el wildcard nativo antes de escribir sobre el puesto. Los callbacks del jugador y del guardia no comparten un Update que libremente reescriba matrices.
- ScheduleStationPoll conserva la solicitud de actualización cuando el primer Update del padre llega mientras la entrada todavía ocupa stationBusy. Evita dejar una operación sin su única solicitud de seguimiento.
- La devolución retorna al artillero propio mediante el Puesto configurado y recupera su controlador estacionario. No se deduce de SetDontMove/MoveTo que exista una ruta AI o navmesh nuevo. La cadencia legacy del guardia sigue siendo 2,5 s; la estación delega el tiro del jugador a la vía nativa revisada.

## Verificación fresca y artefactos

Comando independiente ejecutado con bytecode y caché de pytest deshabilitados:

```powershell
& 'C:\Users\Facu2\AppData\Local\Programs\Python\Python311\python.exe' -B -m pytest -q -p no:cacheprovider tests/test_v15_station.py tests/test_v15_takeover.py
```

Resultado final: **68 passed**, exit code 0. Se revisaron los casos de interrupción durante Reserve/Prepare/entrada real del padre, rollback de DisablePlayerControls, timeout/contexto que cambia al retornar, coordinador cambiado, guard load con lease nuevo, muerte, wildcard pendiente, cleanup guardado y consumo del primer Update. Una segunda ejecución de guardia, takeover y sector dio **109 passed**; incluye el objetivo de suelo con PitchMax=80 después de Reserve/Release. El guardia ahora admite hasta 80 únicamente con AllowPlayerTakeover y conserva 45 para legacy. El hallazgo de integración y su cierre figuran en v15_city_spec_review.md.

Los seis scripts del recibo global `reports/plugin_compile.json` tienen fuente, PEX y disassembly que coinciden con los hashes actuales, y registran exit code 0 tanto del compilador Bethesda como del assembler. El revisor no volvió a compilar ni cargó los PEX en el motor. Para Station, el disassembly confirma herencia de AstraAsedioActi, llamadas Parent y las funciones del coordinador; el recibo registra 18 funciones, cero ArrayCreate y ausencia de casts None a array.

El recibo enfocado previo `v15_station_compile.json` tiene la misma fuente pero sus hashes de PEX/disassembly quedaron superados por la compilación global. El dictamen utiliza el recibo global y los artefactos actuales, no ese par de hashes antiguo.

| Entrada revisada | SHA256 |
|---|---|
| mod/scripts/source/AstraAsedioStation.psc | 643d203b5a1b4b2691c13d8c50128aa924b0262b609372f089f711539773b42e |
| mod/scripts/source/AstraAsedioGuard.psc | 56c35479fc8a0c5a54332dced946da2f6e264c024b7175fd07f4c6fece3630fb |
| mod/scripts/source/AstraAsedioActi.psc | a23b1d2288cd85826b25f67e96c632f61b57fd7772daf37751ea6c76acbba856 |
| mod/scripts/source/AstraAsedioSession.psc | b762659b8b339eb99080627371f124aa07acb1fe98e861075c47cf9a51e06d27 |
| mod/scripts/AstraAsedioStation.pex | 677f2d62f172696017760cb1ccaa74557fa7bf1edb3afc7f7d19f7a3859d80d3 |
| reports/papyrus_bytecode/AstraAsedioStation.disassemble.pas | 3f50c5828256f1e32387fc4eff4cc6a55b778807830747deaf8e3307544d18c9 |
| reports/plugin_compile.json | 4e2f75b9a89c5babd6f60b645906bd26e8c6f13614679651a080629204a6cc31 |

## Límites de evidencia

Los tests ejecutan cuerpos PSC reales mediante un evaluador escalar con fronteras nativas simuladas. No ejecutan el planificador de Papyrus, el dispatch real de los scripts hermanos ni Skyrim. Un slot guardado que depende del retorno de una llamada suspendida no se libera mediante timeout arbitrario: hacerlo permitiría efectos viejos sobre un nuevo dueño. La persistencia y reanudación de esos stacks requiere prueba de guardar/cargar durante entrada, salida y compensación.

La revisión complementaria v15_city_spec_review.md inspecciona el plugin/plataformas terminados y confirma los enlaces de hermano Self, referencias propias y sector por sesión. Su alcance geométrico es estático y muestreado; incluye una transición de escalera este pendiente de motor. La aprobación de coordinación de este informe no convierte esos límites en una prueba de navegación real.

La prueba real debe cubrir activación/entrada en ambos puestos, disparo y salida, guardia muerto/ausente, espera del artillero, menús/cámara/muerte, guardar/cargar/descargar con una reserva pendiente, regreso del guardia y ausencia de escrituras tardías después del acuse nativo. No se afirma latencia de motor, daño, ruta AI, colisión o paso de patrulla.
