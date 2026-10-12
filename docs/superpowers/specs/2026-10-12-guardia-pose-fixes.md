# Guardia de los voladizos — pose trabada (v29.1, DLL 3.6.2)

Estado: **no probado en Skyrim y no compilado** (la DLL requiere MSVC + CommonLibSSE-NG). Lo que se verificó fuera del juego está en "Qué se comprobó".

## Síntoma

Con v29/v30 instaladas, el operador de los voladizos de Whiterun (`0xB70/0xB71`, `0xB80/0xB81`) queda en una *pose bugeada, como intentando levantar los brazos*, y no reacciona a un golpe de espada.

## Qué se comprobó (solo lectura de los adjuntos)

- ZIP `QA_v29`: DLL 3.6.0. `mod.7z`: DLL **3.6.1 ("v30")**; sus `.psc` son idénticos a la rama v29 y sus `.pex` solo difieren en la fecha de compilación. **La única diferencia real entre v29 y v30 es la DLL.**
- Diff de v30 contra v29 (46 de 1 823 funciones, desensamblado normalizado): cambian `GuardRuntime::tick`, el tamaño de `Slot` (+8 B) y la versión. `tick` pasa el resultado de `pose()` a `guardShouldFire` (no disparar sin pose soportada) y añade un reinicio por mundo activo. **No cambian `requestClip`, `acquire` ni `observe`**: lo que pide el clip es idéntico en v29 y v30, de modo que el fallo está antes de lo que v30 toca. El fuente de v30 no está en ningún PR.
- Datos sin defectos: maestros y FormIDs de los cuatro ESP; `Launcher`/`ShotAmmo`/`ShotSound` asignados en ambas estaciones; quest de sensores *Start Game Enabled* con SEQ válido (el FormID local `03000806` coincide en `AstraAsedio.esp` y `GuardAnim.esp`); OAR a 4 niveles, con nombres de mod y submod que coinciden con `guardClipKind`; HKX `hk_2010.2.0-r1` de 64 bits (el formato de SSE), 99 pistas, esqueleto `NPC Root [Root]`; el ABI de `IAnimationsInterface1` coincide con el header oficial de OAR; el parche de EDID del PR #2 solo cambia 10 EDID.
- Evidencia real previa (`reports/diagnosis_v26_context.json`, `diagnosis_v27_grip.json`): en Whiterun las adquisiciones ocurren y OAR sustituye el clip. No hay ningún log de v29/v30.

**Causa raíz no demostrada.** Las hipótesis son del runtime, no de los datos.

## Hipótesis y qué log las confirma

| # | Hipótesis | Qué esperaría en `AstraSight.log` |
|---|---|---|
| H1 | `pose()` escribía `SetPosition`/`SetRotationX`/`SetRotationZ` **en cada tick** aunque el actor ya estuviera en su sitio: un teletransporte por frame que puede impedir que el grafo termine la mezcla y procese eventos. | `guard v29 pose … writesPos=` y `writesRot=` en cientos por 2 s con `target=00000000` (v29) → cerca de 0 (v29.1). |
| H2 | `IdleForceDefaultState` y `PlayIdle` en el mismo frame, y re-solicitud cada ≥6 s si OAR no emite muestras. QA_v27 ya decía que esa pareja "interrumpe cualquier clip en curso". | `guard v29 hold re-request …` repetido; brazos que suben y bajan. |
| H3 | Las muñecas no llegan a las empuñaduras (escala, esqueleto, ancla). | `handErrorL/R` ≫ 3 u. |
| H4 | Otra animación gana (otro submod de OAR, motor de comportamiento). `observe()` descartaba en silencio cualquier clip ajeno. | `guard v29.1 unexpected clip … mod= submod= animation=`; ruta vacía = clip vanilla (el reemplazo no se aplicó). |

"Sin reacción al golpe" **no es un síntoma de H1–H4 por sí solo**: el paquete `0xB90` lleva *Ignore Combat / No Combat Alert*, el NPC tiene agresión 0 y el runtime fija `kMovementBlocked`. Es consecuencia del aislamiento de IA de v24. Si se quiere que el operador reaccione al ser golpeado, es un cambio de diseño aparte.

## Cambios (v29.1)

Solo fuente nativa y herramientas. ESP, NIF, HKX, OAR y Papyrus no cambian (no hay `.pex` que recompilar).

1. **`guardPoseWrites`** (`GuardPolicy`): decide si hace falta escribir posición (> 0,05 u) o rotación (> 0,001 rad, módulo una vuelta; también si queda cabeceo). Entradas no finitas fallan hacia escribir. `pose()` escribe solo lo que cambió y conserva todas sus comprobaciones (apoyo, barrido, desplazamiento del controlador, "no se asentó").
2. **Solicitud del idle partida**: la primera solicitud solo hace `ClearConditionStateData` + `PlayIdle` (`playHold`). Una re-solicitud manda `IdleForceDefaultState` y reproduce el idle `GuardReplayDelay` = 0,35 s después, en otro tick; el reloj de entrada vuelve a empezar al reproducirlo.
3. **Pose sostenida demostrada por las manos**: cada 0,25 s se miden las muñecas contra las empuñaduras; ≤ 12 u en ambas cuentan como "visto" para el vigilante (no se re-solicita una pose que ya se ve bien). Máximo `GuardMaxReissues` = 3 re-solicitudes por lease; luego `guard v29.1 hold unresolved` (aviso, **sin cancelar**: la telemetría sigue sin cancelar nunca).
4. **`observe()`** registra, como máximo cada 10 s por clip, lo que suena en un actor vigilado cuando no es uno de los cuatro clips propios. Solo toca `observationsMutex_` y el logger.
5. **`poseLog`** añade `writesPos`, `writesRot`, `maxDrift`, `reissues` y `held`; el prefijo `guard v29 pose` se mantiene.
6. **Versión 3.6.2** (`Plugin.cpp`, `GuardRuntime.cpp`, `CMakeLists.txt`, `verify_binary.py`, `build_native.py`): la primera línea del log prueba qué DLL cargó. Es el fallo que ya se vio entre v27 y v29.

## Cómo leer el resultado

```
python scripts/analyze_guard_log.py "%USERPROFILE%\Documents\My Games\Skyrim Special Edition\SKSE\AstraSight.log"
```

Imprime los conteos y un veredicto por hipótesis (`H1-…`, `H2-…`, `H3-…`, `H4-…`, `NEVER-ACQUIRED`, `DLL`, `OAR`, `LOOKS-HEALTHY`). Con OAR abierto (Shift+O) sobre el guardia se ve qué submod gana.

## Qué se comprobó de v29.1

- `AstraCore` + los ejecutables de prueba con g++ (CTest 16/16; línea base de v29: 15/15). `native/tests/guard_pose_tests.cpp`: 42 aserciones sobre escritura mínima, evidencia de manos, tope de re-solicitudes y temporización en dos fases.
- `tests/test_guard_pose_fixes.py` (11 contratos de estructura; 9 fallan contra el `GuardRuntime.cpp` de v29) y `tests/test_analyze_guard_log.py` (13 casos, uno con líneas reales de la sesión v26).
- **No** se compiló `GuardRuntime.cpp` ni `Plugin.cpp`; los cambios usan solo llamadas ya presentes en el archivo (salvo capturar el `bool` de `NotifyAnimationGraph`). **No** se probó nada en Skyrim.

## Si ya compilás una v30 local

Estos cambios tocan `GuardRuntime::pose`, `requestClip`, `observe`, `poseLog`, el tramo de re-solicitud de `tick` y los campos de `Slot`/`GuardHoldWatch`. Tu v30 cambia `tick` (reloj/hitch, pose soportada antes de disparar, mundo activo) y añade un campo a `Slot`: habrá que fusionar a mano esos tramos. Conviene conservar de v30 lo que ya probaste y quedarse con la versión 3.6.2 solo si ambos conjuntos conviven.
