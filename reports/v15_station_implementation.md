# Estación compartida v15

Implementado `AstraAsedioStation extends AstraAsedioActi` para las nuevas armas
compartidas de ciudad. La propiedad `AstraAsedioGuard Guard` debe enlazar al
script hermano del mismo `Self` en VMAD. La integración de VMAD y las posiciones
de guardia/espera pertenecen al trabajo del coordinador.

## Comportamiento

- La estación comprueba SKSE, AstraSight 3.5.0, API 4 y disponibilidad antes de
  reservar al guardia. Un binding de limpieza ausente no puede dejar una reserva
  nueva esperando una consulta que nunca devuelve verdadero.
- Un slot `stationBusy` impide reservas simultáneas y reentrada durante Reserve,
  Prepare, queries del padre, activación, actualización y liberación. La estación
  conserva el coordinador capturado aunque cambie la propiedad `Guard`.
  Si un update llega antes de retornar la entrada del padre, mantiene un nuevo
  update pendiente para no perder la única solicitud de actualización.
- `ReservePlayerLease` precede toda entrada del padre. Prepare se consulta con
  updates únicos de 0.05 s y un plazo de tiempo real de 3 s desde el retorno de
  Reserve. Se revalidan revisión, carga, menú, muerte y reloj antes y después de
  Prepare y de ResetStationAim. El plazo es una condición del código; no promete
  que Papyrus programe eventos ni que una llamada nativa retorne en 3 segundos.
- Solo la preparación vigente y válida permite `Parent.ResetStationAim()` y
  `Parent.OnActivate(player)`. Una activación antigua que retorna después de una
  cancelación vuelve a drenar el padre antes de devolver la concesión.
- `EndSession` invalida primero la revisión de la estación y ejecuta la limpieza
  completa del padre. La reserva permanece retenida hasta que no haya operación
  ni limpieza del padre y `IsEffectsQuiescent(Self, 0)` sea verdadero. Release
  recibe únicamente el coordinador y número de concesión capturados.
- Unload, CellDetach, destrucción, menú durante entrada, fallos de validación,
  muerte y carga invalidan o drenan la entrada. La limpieza de muerte del alias
  existente llega al override de la estación a través de la sesión.
- OnLoad evita `Parent.OnLoad` y toda escritura de nodos. Ejecuta recuperación
  del padre y normalización de tiempos bajo un slot de estación. Si hay un stack
  suspendido guardado, mantiene su slot hasta su retorno; limpiar ese slot a la
  fuerza permitiría que sus efectos tardíos alcanzasen una concesión nueva.

## Cambio mínimo autorizado en el padre

Se añadió `RecoverStationLoad()` en `AstraAsedioActi.psc`. Extrae la recuperación
de un EndSession suspendido: limpia `endingSession`, incrementa `generation`,
ejecuta `Session.EmergencyCleanup()` y drena una operación/mira activa. OnLoad del
padre reutiliza el helper y conserva su comprobación anterior a CaptureMatrices.
El helper no captura matrices, no aplica aim y no escribe la escena.

## Verificación

Las pruebas ejecutan los cuerpos de las fuentes PSC reales de Station, Acti,
Guard y Session mediante el evaluador escalar existente. Las llamadas nativas
son fixtures deterministas, incluyendo controles de la sesión real. Se añadió
únicamente el tipo local `AstraAsedioGuard` al evaluador compartido.

TDD observado:

1. 34 fallos iniciales por ausencia de la fuente Station.
2. Cinco regresiones añadidas fallaron por contexto/deadline tardíos y query
   antigua de OnUpdate; se corrigieron manteniendo revisión y slot.
3. Cuatro regresiones fallaron por reservar sin requisitos nativos; una falló por
   aceptar activación durante OnLoad. Se corrigieron con preflight y slot de carga.
4. Una regresión falló al entregar el primer update antes del retorno de la entrada;
   se corrigió manteniendo un update pendiente mientras hay slot y concesión.

Última ejecución enfocada:

```powershell
python -m pytest tests/test_v15_station.py tests/test_v15_takeover.py tests/test_v13_guard.py tests/test_control_lease.py tests/test_session_contract.py -q --tb=short -k 'not all_scripts_compiled_by_real_bethesda_compiler'
```

Resultado: **183 passed, 1 deselected, 80 subtests passed**. Station contiene 50
casos, incluyendo interrupciones en Reserve/Prepare/Reset/entrada real del padre,
compensación de DisablePlayerControls, reserva nueva tras Guard.OnLoad,
coordinador reemplazado, barrera nativa, muerte, reloj inválido y slots guardados.
La exclusión es el recibo global de compilación, que debe regenerar el coordinador
tras los cambios de todas las fuentes; no se sobrescribió ese recibo aquí.

Compilación enfocada de Station con `PapyrusCompiler.exe` Bethesda y disassembly
con `PapyrusAssembler.exe`: **exit 0, 0 errors, 0 warnings**. Inspección del
bytecode: 18 funciones, cero ArrayCreate, ningún cast None a array. Recibo en
`reports/v15_station_compile.json`; PEX en `mod/scripts/AstraAsedioStation.pex`;
disassembly en `reports/papyrus_bytecode/AstraAsedioStation.disassemble.pas`.
El recibo incluye hashes SHA-256 de la fuente y los artefactos. Acti requiere la
compilación global posterior del coordinador.

Durante un chequeo más amplio de fixtures heredados, se observaron ocho fallos:
uno por el recibo global aún antiguo y siete en `test_camera_aim.py` configurado
con plugin 3.4/API 3 frente a los requisitos actuales 3.5/API 4. Se informó al
coordinador; esos fixtures están fuera del ownership de esta implementación.

## Pendiente en Skyrim

No se ejecutó Skyrim ni se modificó v14, runtime, MO2, plugins, geometría o Guard.
El compilador solo leyó imports del runtime. Se necesita validar VMAD del arma,
orden real de eventos de los scripts hermanos, persistencia/reanudación de
stacks, descarga/carga, guardado durante entrada/salida, menú, muerte, cámara y
cola de limpieza nativa. También quedan para el motor la posición de espera,
colisión y retorno del guardia. Un slot suspendido que nunca vuelva no se libera
por un timeout arbitrario: hacerlo permitiría efectos antiguos sobre un dueño
nuevo. Las pruebas no establecen latencia, daño ni comportamiento del motor.
