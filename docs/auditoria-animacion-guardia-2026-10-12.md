# Auditoría técnica — animación del guardia operador de ballesta (voladizos de Carrera Blanca)

**Fecha:** 2026-10-12 · **Alcance:** solo análisis y diagnóstico. No se modificó código, scripts, ESP, NIF ni binarios.

**Repositorio auditado:** `FacundoSu1986/Ballesta-Astra-SkyrimSE`

- Rama `main` (base de esta sesión: `7397197`): **no contiene** todavía ningún trabajo de guardias; solo llega hasta v21 + IA híbrida del guardia.
- Rama `astra-v29-guardia-simple` (tag `v29`, HEAD `a4ffddb`, snapshot previo `5ce9947` = v23–v28): **aquí vive todo el asunto** (`addons/GuardAnim`, `native/src/GuardRuntime.cpp`, `GuardPolicy.cpp`, docs QA v22–v29, logs de diagnóstico en `reports/`).
- Todo lo que sigue se verificó leyendo artefactos reales de esa rama: fuentes C++/Papyrus, `config.json` de OAR, registros de los ESP parseados con el propio parser del repo, y los JSON de diagnóstico medidos en partidas del usuario (`diagnosis_v24_scale.json`, `diagnosis_v25_context.json`, `diagnosis_v26_context.json`, `diagnosis_v27_grip.json`).

> **Aclaración previa imprescindible (cambia el marco del problema).** En este mod **los guardias no empuñan ni apuntan una ballesta personal**. No hay `WEAP` de ballesta equipada, ni `Attack Data`, ni subgrafo `weap_behavior`/`crossbow_direction_behavior.hkx`, ni eventos `BowDraw`/`AttackStart`. El guardia es un **operador de estación estática**: se lo coloca en una órbita de 151 u frente a la ballesta (ACTI `0xB04`), se le reproduce un *idle* vanilla (`IdleHandsBehindBack`) reemplazado por OAR y el disparo lo hace el motor con `Projectile::Launch` nativo. Por lo tanto, todas las hipótesis sobre “animación de ballesta equipada” son inaplicables a este síntoma. Si lo que se quiere es *otra cosa* (que el NPC desenfunde una ballesta `WEAP` y la apunte como el jugador), eso es una funcionalidad distinta, no un bug de este sistema — ver §8.

---

## 1. Modelo real del sistema (mapa de piezas verificado)

| Pieza | FormID / ruta | Función | Verificación |
|---|---|---|---|
| Ballesta-operador (base) | `AstraAsedio.esp` `0x0B04` (ACTI) | Malla `ballesta_guardia.nif`, nodos `CTRL_GIRO_360`, `CTRL_ELEVACION`, `ProjectileNode`, `VIROTE_VISUAL` | `GuardRuntime.cpp::station()` exige base `0xB04` |
| Estación Este / Oeste | `AstraAsedio_WhiterunTorres.esp` `0x0B70` / `0x0B80` + operadores `0x0B71` / `0x0B81` | Los dos puestos de los voladizos | `guardStation(0xB70,0xB71)`, `(0xB80,0xB81)` |
| NPC operador (base) | `…Torres.esp` `0x0B00` / `0x0B01` (`AstraWhiterunVoladizoArtilleroEste/Oeste`) | Clones propios, derivados del guardia donante `Skyrim.esm:0002AC7B` | `reports/bridge_v24.json`; parseo del ESP (§3) |
| Paquete de puesto | `…Torres.esp` `0x0B90` `AstraGuardStayAtBallista` | Clon de `DefaultStayAtCurrentLocation` (`Skyrim.esm:0002AC7B`, PACK) con flags de aislamiento | parseo del ESP, §3 |
| Facciones OAR | `AstraAsedio_GuardAnim.esp` `0x800`, `0x801`, `0x804`, `0x805` | Compuertas de los submods OAR (pose, disparo, giro izq./der.) | parseo del ESP |
| Idles propios | `…GuardAnim.esp` `0x802` `AstraGuardOperateIdle` (ENAM `IdleHandsBehindBack`), `0x803` `AstraGuardExitIdle` (ENAM `IdleForceDefaultState`) | Eventos de grafo que dispara el runtime | parseo del ESP, §1.1 |
| Quest de sensores | `…GuardAnim.esp` `0x806` `AstraGuardOperatorSensorsQuest` | Aliases `East`/`West` con `ALFR 0xB71/0xB81`, `ALPC 0xB90`, `FNAM 0x92` | parseo del ESP |
| Clips propios | `meshes\actors\character\animations\AstraAsedio\Guard\astra_guard_{operate,fire,turn_left,turn_right}.hkx` | 4 clips de 99 tracks, 2,0 s / 1,0 s / 0,8 s / 0,8 s | `reports/hkx_validation_v23.json` |
| Reemplazos OAR | `…\animations\OpenAnimationReplacer\AstraAsedioGuard\{Operate,Fire,TurnLeft,TurnRight}\IdleHandsBehindBack{,_Enter}.hkx` + `config.json` | Reemplazo por ruta de `IdleHandsBehindBack.hkx` | 12 copias HKX en el ZIP v29 |
| Runtime nativo | `AstraSight.dll` 3.6.0 (API jugador 4 / **NPC 1**) | `GuardRuntime`: adquisición, pose rígida, apuntado, disparo | `mod/SKSE/Plugins/AstraSight.dll` de la rama v29 |
| Puente Papyrus | `AstraAsedioGuard.psc` (v28: reintento acotado) + `AstraGuardNative.psc` + alias `AstraGuardOperatorAlias.psc` | Solicita/procesa la operación, reintentos | `mod/scripts/source/` de la rama v29 |

Geometría medida (clave para entender el síntoma): el clip de sostener deja las **muñecas a 0,02 u de (±33,6; 143,8; 100,5)** en espacio ballesta, y las empuñaduras de `ballesta_guardia.nif` están en **(±33,6; 137,9; 101,67)**; con escala nórdica 1,03 el error esperado en juego es de **≈3 u** (`QA_v29.md`, `docs/README_v29.md`).

### 1.1 Capa Havok / grafo / variables de animación

- **Evento de entrada.** `PlayIdle(0x802)` → el motor envía el evento de grafo **`IdleHandsBehindBack`** (está en el `ENAM` del registro, no en un script), que entra a su estado con una mezcla de **0,5 s** (`0.5secondBlendToAnimDriven`); `IdleForceDefaultState` (idle `0x803`, también en `ENAM`) vuelve al reposo con **0,2 s**. Ambas cifras fueron medidas sobre `mt_behavior.hkx` vanilla (`docs/QA_v29.md`).
- **El subgrafo es solo máquinas de estado, sin pesos por hueso:** la animación se aplica al cuerpo completo; no hay *blend* parcial que “robe” el agarre.
- **No hay variables de grafo propias.** El único `SetGraphVariableBool` del código es `bHeadTracking=false` durante la posesión, y se restaura al liberar (`GuardRuntime::acquire/cleanup`). No se escriben `iRightHandType`, `weapType`, `Pitch`, `aimPitch` ni similares: no hacen falta, porque no hay arma equipada en la mano.
- **`Fire` y `Reset` no son clips de actor.** En `GuardRuntime::shoot()/reload()` se activan **secuencias Gamebryo del NIF de la estación** (`GetSequence("Fire")` a los 0,0 s y `GetSequence("Reset")` a los 0,2 s). No hay `weaponFire`, `ReloadStart` ni estado de recarga en el grafo del actor.
- **Descartado explícitamente:** corrupción de `0_master.hkx`/behaviors por FNIS/Nemesis/Pandora, ramas Dawnguard ausentes, subgrafo `crossbow_direction_behavior.hkx`, nodos aditivos `AimPitch`/`AimHeading`. Nada de eso interviene en esta ruta.
- **Lo que sí falló en el grafo (medido):** el envoltorio *run-once* de `PlayIdle`. En la sesión v26 (93/93 ciclos) el log registra siempre `runningPackage=FF000F64/FF000F65`, `idle=00000000`, `assignedPackage=14000B90`. Es decir: mientras corre el idle propio, `GetRunningPackage()` devuelve el paquete envoltorio y `currentProcessIdle` queda nulo **todo el tiempo**, no de forma transitoria. Cualquier contrato interno que exija “paquete corriente = B90 e idle corriente = 0x802” es insatisfacible en esta vía (1.6.1170).

### 1.2 Capa Creation Kit (registros reales, parseados)

| Registro | Dato verificado | Lectura |
|---|---|---|
| `PACK 0x0B90` | `PKDT = 0x08301000` → **0x100000 Ignore Combat**, **0x200000 Weapons Unequipped**, **0x8000000 No Combat Alert**; `0x800000 (Weapon Drawn)` **limpio**; residual `0x1000` heredado del donante. `PKCU` = plantilla de paquete `Skyrim.esm:0x16FAA`, versión 3. `ANAM` = `Location`/`Bool`/`Bool` (seguir en el lugar actual). | El aislamiento de IA que suele recomendarse **ya está hecho** (v24). El operador no desenfunda arma personal ni entra en alerta de combate. |
| `QUST 0x806` | `DNAM` prioridad 100; dos aliases con `ALST/ALID East,West`, `FNAM = 0x92` (Optional + Allow Dead + Allow Disabled), `ALFR 0xB71/0xB81`, `ALPC 0x0B90`. | El paquete del puesto se fuerza por alias (`ALPC`) — el bug clásico “el paquete no llega” está cubierto. |
| `NPC_ 0x0B00/0x0B01` | `ACBS` flags `0x08` (Respawn), sin flag de plantilla de **AI Packages** (`0x20` del campo de templateFlags no está puesto). `DNAM` con *height 1.0* implícita de la raza; escala efectiva del actor 1,03. | Los operadores tienen su propia IA; no heredan paquetes del guardia vanilla. |
| `IDLE 0x802/0x803` | `ENAM` = `IdleHandsBehindBack` / `IdleForceDefaultState`; `DNAM` = `Actors\Character\Behaviors\0_Master.hkx`; `ANAM` = raíz (0/0). | Los dos únicos “eventos de grafo” propios del sistema. |
| `FACT 0x800/0x801/0x804/0x805` | Facciones vacías, sin `DATA` relevante; rango guardado/restaurado por el runtime (`s.ranks[]`). | Son compuertas puras para OAR; no son facciones de juego. |
| `WEAP` / `Attack Data` / `Combat Style` / `Race` | **No participan.** El arma que dispara es `Launcher`/`ShotAmmo` pasados a `BeginOperation` y usados por `Projectile::Launch`; los operadores permanecen con **arma envainada** (`WEAPON_STATE::kSheathed`) como condición de validez. El estilo de combate del donante no influye porque el paquete anula combate/alerta. | Toda la línea “WeapTypeCrossbow, Attack Data, munición, combat style” es irrelevante para este síntoma. |

### 1.3 Capa Papyrus / OAR

- **OAR (config verificada, 4 submods):** `Operate` prioridad **1185250** (condición `IsInFaction 0x800` **y** `!IsActorBase(Player)`), `TurnLeft` **1185251** (`+0x804`), `TurnRight` **1185252** (`+0x805`), `Fire` **1185253** (`+0x801`). En OAR, mayor número gana y los NPC necesitan que se reemplace la entrada concreta de idle que el motor va a reproducir ([Reddit – OAR priority/npc idles](https://www.reddit.com/r/skyrimmods/comments/1d6scaf/does_anyone_know_of_a_mod_that_allows_you_to/), [Nexus – idles de NPC y OAR](https://forums.nexusmods.com/topic/13499716-animations-not-looping/)). Aquí se reemplazan `IdleHandsBehindBack.hkx` **y** `…_Enter.hkx`; **no** se reemplaza el `_exit` vanilla (asumido y documentado por el propio mod: al interrumpir hay *pop* de pose).
- **El camino NPC es nativo, no Papyrus.** `AstraAsedioGuard.PumpV23()` solo *solicita* la operación (`AstraGuardNative.BeginOperation/GetStatus/EndOperation`) y reintenta. Las funciones de pose Papyrus de v13 (`StartGuardPose`, `SetGuardFirePose`, `PositionOperator`, `PlaySceneAnimation`, `CommitShot`, `RestoreNeutralScene`, `ApplyAim`, …) están **retiradas a propósito desde v22** (`; Retired v22 effects: native NPC operation is the sole owner.`) y devuelven `false`/nada. **`BeginShot` del script del guardia no tiene ningún llamador** en el árbol v29 (solo existe el homónimo de `AstraAsedioActi.psc`, que es el camino del **jugador** y usa `AstraSightNative`).
- **Ciclo de reintento v28:** tras un `status == -2` el pump espera 5 s (30 s desde el 4.º fallo) y reintenta; en v27 esa espera se reprogramaba sin cambiar de condición (bucle; `repeated_backoff_count: 25`, `backoff_bug_reproduced_with_two_updates: true`).
- **Colisiones:** ningún otro mod del perfil reemplaza `IdleHandsBehindBack` (comprobado por el propio proyecto en MO2, `QA_v29.md`). Riesgo residual: un mod de idles/pose de guardia con prioridad **mayor** a 1185250–1185253 ganaría la sustitución; se verifica con la UI de OAR (`Shift+O`) sobre el NPC.

---

## 2. Cronología de la causa raíz (con evidencia medida, no hipótesis)

| Rev. | Evidencia observada en juego | Causa identificada | Corrección |
|---|---|---|---|
| v23 | Guardias sin pose y **sacando sus arcos personales** | Los NPC no tenían paquete de puesto | v24: PACK clon con Ignore Combat / Weapons Unequipped / No Combat Alert + `PKID` + `ALPC` |
| v24 | 230 rechazos, todos `station / actor scale differs from 1` (log 101 143 B) | Contrato confundía `refScale`, `GetScale()` y altura natural (actor 1,03) | v25: separa las tres magnitudes |
| v25 | 134 adquisiciones / 134 cancelaciones a ~35 ms, motivo agregado | Registro no decía **qué cláusula** fallaba | v26: diagnóstico de la primera cláusula inválida |
| v26 | 93/93 cancelaciones, `clause=running package has no owned idle override`, `runningPackage=FF000F64/65`, `idle=00000000` | Predicado de admisión **insatisfacible** (envoltorio run-once de `PlayIdle`; `currentProcessIdle` siempre nulo) | v27: post-adquisición se tolera el envoltorio; identidad del idle arbitrada por la observación OAR |
| v27 | 6 adquisiciones, **7 confirmaciones OAR del clip**, **0 agarres**, **0 virotes**; 2 `hold replacement not observable`; bucle de backoff | El “agarre” solo se habilitaba desde un callback que retornaba en silencio fuera del hilo principal; el backoff se repetía | v28: pose/agarre al controlador principal + bandera de reintento |
| v28 | (diseño) | La compuerta de agarre exigía manos a **≤16 u** muestreadas en ≤2 frames; durante la mezcla de entrada de 0,5 s las muñecas arrancan a **~29 u** ⇒ cancela siempre al entrar | v29 |
| **v29** | **pendiente de prueba en juego** | — | **La animación agarra.** Se elimina la IK/compuerta de agarre; la telemetría OAR solo registra; el conjunto ballesta+guardia se mueve como sólido rígido; el disparo se decide por geometría (`guardShouldFire`); reemisión del idle acotada (3 s / 6 s) sin cancelar |

**Enunciado de la causa raíz (la “solución” correcta del problema del usuario):** el síntoma “levanta los brazos pero no agarra, nunca apunta ni dispara” **no es un problema de assets ni de CK**: es la cadena de **dos compuertas insatisfacibles** (el contrato paquete/idle post-`PlayIdle`, y después la confirmación de agarre por distancia de huesos durante la mezcla de 0,5 s) más un bucle de reintento en Papyrus. La v29 resuelve las tres: el clip horneado es el que agarra (muñecas a 0,02 u de las empuñaduras, empuñaduras del NIF a 0,02 u del mismo punto), y nada bloquea, cancela ni apunta en función de la telemetría.

---

## 3. Veredicto sobre los tres análisis que aportaste

| # | Afirmación central | Veredicto | Evidencia |
|---|---|---|---|
| **A** (“Auditoría técnica” con Havok/CK/AAR genérica) | El problema está en el grafo de ballesta equipada: `BowDraw` vs `AttackStart`, `iRightHandType=12`, `WeapTypeCrossbow`, `Attack Data`, `Combat Style`, `Ammo`, `AimPitch`, corrupción por Nemesis/Pandora | **Inaplicable en su mayor parte.** Es una auditoría “de plantilla” sobre otro sistema. **Acertados**: (1) la mezcla de 0,5 s de `IdleHandsBehindBack` es real y es un factor del fallo; (2) “no usar la telemetría de huesos como compuerta bloqueante” es exactamente lo que hizo v29; (3) el `_exit` no reemplazado es real (el propio mod lo documenta); (4) el aislar la IA con `Weapons Unequipped`/`Ignore Combat` ya estaba hecho (v24); (5) el no acumular backoff, ya corregido (v28). **Falsos**: FormIDs de idle inventados, la exigencia de keyword `WeapTypeCrossbow`/`Animation Type`, la compuerta de munición, el secuestro por “patrullas vanilla” (el paquete por alias lo anula). **No es la solución.** |
| **B** (análisis sobre `GuardRuntime`/`requestClip` y los logs 134/134) | `acquire()` adquiere y el lease se cancela por una cláusula de `operatorFailure`/contexto; falta ver qué cláusula; `PlayIdle` puede fallar o llegar tarde; recomienda **instrumentar la cláusula exacta** y revisar facciones/idles OAR | **Es la línea correcta y la que resolvió el problema.** Su recomendación #1 (log granular de la cláusula) es literalmente lo que produjo el hallazgo de v26 (`running package has no owned idle override`) y, con él, la corrección de fondo de v27. Su marco “la animación no se dispara porque el estado/contrato no se satisface” es el acertado. Sus propuestas #2 (forzar paquete + esperar un frame), #3 (variable de grafo nueva) y #4 (verificar `WeapType=Crossbow`/`Attack Data`) **no** eran la vía: la #2 es imposible de satisfacer en esta ruta, la #3 no hace falta y la #4 es irrelevante. **Su diagnóstico es el bueno; su lista de parches es parcialmente errada.** |
| **C** (“la causa es `PlaySceneAnimation` retirada en la línea 296–299; el runtime solo procesa primera persona”) | `BeginShot` → `PlaySceneAnimation` devuelve `false` → se aborta el ciclo; los guardias third-person nunca llegan a `tick()`/`requestClip()` | **No es la solución: su mecanismo central es falso.** (1) `BeginShot` del guardia **no tiene llamadores**; es código muerto de v22 y su equivalente vivo es el homónimo de `AstraAsedioActi.psc` (camino del jugador). (2) El hook **no** es `FirstPersonState::Update`: `GuardRuntime::install()` engancha `PlayerCharacter::Update` (vtable slot `0xAD`/173, el *frame pump* de todo el sistema), `Character::Update` (`0xAD`, solo contadores) y `hkbClipGenerator::Generate` (`0x17`/23, la observación OAR) — `reports/native_guard_hook_evidence.json` lo confirma. `FirstPersonState` sí aparece en `Plugin.cpp`, pero es el **sistema de cámara del jugador** (AstraSight montado). (3) Los propios logs prueban lo contrario: los dos guardias de los voladizos **sí** llegaron a `acquire()` 93–134 veces y hubo 7 observaciones OAR del clip propio. **Acertados**: que las funciones Papyrus de pose están retiradas (es por diseño, no un fallo) y que el PACK tiene el bit 23 limpio (es `Weapon Drawn`; el flag que el mod limpia, sí, pero su lectura “para no desenfundar el arma personal” es incorrecta: eso lo hace `0x200000 Weapons Unequipped`). También es falso que `Skyrim.esm:0x16FAA` sea un combat style: el `PKCU` del PACK dice explícitamente “Package Template → otro PACK” ([formato PACK, UESP](https://en.uesp.net/wiki/Skyrim_Mod:Mod_File_Format/PACK)). |

**Conclusión de la comparación:** de los tres, **B es el análisis cuya línea de diagnóstico es la solución** (y fue la que efectivamente condujo al hallazgo y a la corrección). A aporta consejos de remediación genéricos, varios ya implementados, dentro de un marco conceptual equivocado. C es una conclusión errónea construida sobre un archivo muerto y un hook mal identificado; si se hubiese aplicado, habría restaurado el puente Papyrus de v13 (el que el mod retiró precisamente porque el control nativo lo reemplaza) sin tocar el fallo real.

---

## 4. Veredicto de viabilidad

| Criterio | Evaluación |
|---|---|
| ¿Es reparable? | **Sí, y ya está reparado en código** en `astra-v29-guardia-simple` (tag `v29`). No requiere rehacer clips, NIF ni ESP. |
| Naturaleza del error | **Lógica de activación/contratos temporales**, no assets corruptos: los 4 HKX validan, el NIF coincide con el clip, los ESP tienen los 7 registros correctos, la instalación en MO2 coincide byte a byte con el repo. |
| Riesgo para partidas | Bajo: sin cambios en ESP/NIF/HKX respecto de v27/v28 (los recursos son idénticos); solo cambia la DLL (3.6.0) y el `.pex` de `AstraAsedioGuard`. La migración de colocación sigue en 26. |
| Incertidumbre restante | La v29 **no se probó en juego** (lo declara su propio QA) y la revisión de su código es *self-review*, no independiente. Falta certificar con el log: pose continua, `handErrorL/R ≈ 3 u`, giro, virote real y protecciones. |
| Confianza en el diagnóstico | Alta: se apoya en mediciones de partidas reales (134/134, 93/93, 7/0/0) y en registros del motor, no en teoría. |

---

## 5. Ruta de corrección sugerida (antes de tocar nada nuevo)

1. **Confirmar qué DLL está cargada.** Primera línea de `AstraSight.log`: debe decir `AstraSight 3.6.0` (v29). Ojo: si el paquete MO2 instalado trae la DLL de v27/v28, el síntoma que ves en juego es el histórico y no el de la v29 (el propio `QA_v29.md` detectó ese desfase en la instalación inspeccionada).
2. **Instalar el ZIP v29** (`AstraAsedio_QA_v29_Unificado_MO2.zip`, 60 entradas, SHA-256 `ac8b04d4…e3`, cuatro plugins en el orden `AstraAsedio.esp` → `AstraAsedio_WhiterunTorres.esp` → `AstraAsedio_Atalaya.esp` → `AstraAsedio_GuardAnim.esp`) desactivando el paquete anterior. No hace falta mover a los guardias: los recursos son los mismos.
3. **Verificar en el log, en este orden:** `OAR Animations V1=True (module loaded=True)` → `guard v26 acquired … holdRequested=true` → `guard v29 holding` → `guard v29 pose … handErrorL=… handErrorR=…` (esperado ≈3 u; si son ≥20 u, la pose no se está aplicando) → `guard real projectile` con un enemigo válido. **Ya no debe aparecer** `running package has no owned idle override` ni cancelaciones `hold replacement not observable`.
4. **Solo si algo sigue fallando**, el árbol de decisión por capa:
   - *Sin `guard acquired`*: el Papyrus no resolvió operadores (falta `AstraAsedio_WhiterunTorres.esp`, traza `operator refs missing`), OAR no cargó, o el actor está fuera de órbita/altura (cláusulas ya nombradas en el log).
   - *Con `holding` pero manos lejos*: sustitución OAR no efectiva sobre el NPC → abrir `Shift+O` con el NPC seleccionado (`prid`) y comprobar que el submod `AstraAsedioGuard/Operate` está verde y con prioridad ganadora; comprobar facción `0x800` en el NPC.
   - *Sin giro*: mirar `moveRefused=` (baranda/suelo/colisión) — ya no cancela, mantiene el ángulo previo.
   - *Sin disparo*: mirar `target=`, cobertura por trayectoria/aliado o `yawError` (tolerancia 0,25°), y enfriamiento 2,5 s.
5. **No** restaurar `PlaySceneAnimation`/`SetGuardFirePose` ni el puente Papyrus de v13 (análisis C): reintroduciría un dueño duplicado de la pose sobre el controlador nativo. **No** tocar `WeapType`/`Attack Data`/`Combat Style` (análisis A): no intervienen. El paquete de IA con `Weapons Unequipped`/`Ignore Combat` **ya está** puesto desde v24.

---

## 6. Riesgos residuales y límites de esta auditoría

- Los pies se deslizan al girar (aceptado por el contrato del clip) y no hay gesto corporal al disparar (la mano derecha se mueve <1 u en el clip original): son decisiones de diseño de v29, no defectos.
- El `_exit` vanilla de `IdleHandsBehindBack` no se reemplaza: una interrupción dura (muerte, stagger, descarga) puede mostrar un *pop* de pose.
- Si otro mod reemplaza el mismo idle con prioridad > 1185250, la sustitución se pierde.
- Esta auditoría leyó fuentes, ESP (parseados), HKX validados y JSON de logs; **no** ejecutó Skyrim. La certificación definitiva sigue siendo la prueba en juego descrita en `docs/QA_v29.md`.

---

## 7. Revisión adicional del árbol v29 — qué más está mal

> Todo lo de esta sección se verificó parseando los ESP con el propio `scripts/vendor/parser_esm.py` del repositorio y leyendo las fuentes nativas. **Es el hallazgo que mejor explica el síntoma reportado.**

### 7.1 En cada voladizo hay **dos puestos superpuestos** y **cuatro guardias** (dos por puesto)

En la misma celda persistente vanilla (`0x00000D74`, la que `docs/nexus/RELEASE_STATUS.md` ya señala como cabecera vanilla retenida) conviven **dos juegos completos** de contenido, con las ballestas en **posiciones idénticas bit a bit**:

| Ref | EDID | Base | Propiedades de la estación | ¿Lo conoce el runtime nativo? |
|---|---|---|---|---|
| `0xB70` / `0xB80` | `AstraVoladizo{Este,Oeste}Ballesta` | `AstraAsedio.esp:0x0B04` `AstraGuardBallistaBaja` (`ballesta_guardia.nif`) | `UseSightCamera=False`, `AllowPlayerTakeover=False`, `PitchPivotHeight=117`, `PitchMin/Max=0` | **Sí** (par `0xB70↔0xB71`, `0xB80↔0xB81`) |
| `0xB40` / `0xB50` | `AstraVoladizo{Este,Oeste}Ballesta` (**EDID duplicado**) | `AstraAsedio.esp:0x0B02` `AstraGuardBallista` (`ballesta.nif`, la malla del jugador; creada en v13 por `build_modular_v13.py`) | `UseSightCamera=True`, **`AllowPlayerTakeover=True`**, `PitchPivotHeight=153`, `PitchMin=-20/PitchMax=80` | **No** (`station()` exige base `0x0B04`; la tabla de pares no lista `0xB40`) |
| `0xB71` / `0xB81` | `AstraVoladizo{Este,Oeste}Guardia` | `Torres.esp:0x0B00/0x0B01` | — | **Sí** (reciben facción `0x800`, `PlayIdle(0x802)`, lease) |
| `0xB41` / `0xB51` | `AstraVoladizo{Este,Oeste}Guardia` (**EDID duplicado**) | **las mismas** bases `0x0B00/0x0B01` | — | **No** |

Consecuencias verificables:

1. **Cuatro actores guardia para dos puestos.** Como el paquete del puesto (`PKID = 0x0B90`) está en la **base NPC**, las dos instancias de cada base lo ejecutan: los gemelos `0xB41/0xB51` quedan plantados en el puesto (armas envainadas, sin alerta de combate) **sin recibir nunca** la facción OAR, el `PlayIdle` ni el lease. Es exactamente la estampa de “guardia junto a la ballesta que no anima”: **el gemelo huérfano**. Los dos ACHR están separados 124 u sobre la misma línea (uno a 17801,7 y otro a 17925,7 para el este).
2. **Dos mallas de ballesta coincidentes** (una `ballesta.nif` y otra `ballesta_guardia.nif` en el mismo punto, sin `XESP`/`XACT` que desactive ninguna) → z-fighting y dos activadores superpuestos con propiedades distintas.
3. La estación legacy sigue siendo **montable por el jugador** (`AllowPlayerTakeover=True`, `UseSightCamera=True`), lo que **contradice el diseño v22** (“los voladizos son puestos exclusivos del guardia”, `docs/README_v22.md`) y el paso 5 de `PRUEBAS_EN_JUEGO.md`. Al montarla, `AstraAsedioStation` mueve al guardia huérfano a su marcador `Standby`.

**Cómo confirmarlo en juego (30 s):** en consola, `prid` sobre el guardia que no anima → si su FormID es `04000B41`/`04000B51`, es el gemelo huérfano; el conducido es `04000B71`/`04000B81`. Para la ballesta: `04000B40`/`0B50` = legacy (base `0x0B02`), `04000B70`/`0B80` = la del guardia (base `0x0B04`).

**Corrección recomendada (sin tocar código):** borrar el juego legacy `0xB40–0xB54` del `AstraAsedio_WhiterunTorres.esp` (2 ballestas + 2 ACHR + 4 marcadores + el VMAD del script retirado). No lo usa ningún sistema: el jugador ya tiene su torreta principal y la atalaya. Si en cambio se quiere conservar una estación alta en el voladizo, hay que migrarla al sistema nativo (§7.2) y decidir explícitamente quién es el dueño del puesto.

### 7.2 El runtime nativo está cableado a **exactamente dos** puestos

Evidencia en `native/src/GuardRuntime.cpp` / `GuardRuntime.h`: `std::array<Slot,2> slots_`, `std::array<...> watchedActors_[2]`, tabla literal `{{{0xB70,0xB71},{0xB80,0xB81}}}`, base fija `0xB04` y `GuardStationPlugin` fijo a `AstraAsedio_WhiterunTorres.esp`. **Cualquier otra estación de guardia queda sin animación por diseño.**

Caso concreto ya presente en el repo: `addons/Whiterun/AstraAsedio_Whiterun.esp` (la ballesta de la **puerta** de Carrera Blanca, REFR `0x0B10` `AstraWhiterunBallesta`, base `0x0B04`, con su guardia `ACHR 0x0B11 AstraWhiterunArtilleroRef`). Ese addon **no se empaqueta** en v29 (el ZIP lleva cuatro plugins: núcleo, Torres, Atalaya, GuardAnim), su NPC no tiene `PKID` y el runtime no conoce su par. Nota histórica importante: en v13–v21 ese puesto **sí** animaba por el puente Papyrus; al retirarse en v22 (“native NPC operation is the sole owner”), ese guardia quedó huérfano. Si el usuario tiene ese addon activo de una instalación previa, **está viendo un guardia junto a una ballesta que jamás va a animar**, sin importar la versión de la DLL.

**Si se quiere un puesto animado en la puerta**, hace falta migrarlo (cambio de código + datos): ampliar las tablas de puestos (arrays de 2 → N, `guardStation`, `ownedOperator`, `stationIdle`), añadir el par en el ESP, `PKID`/`ALPC`/facción y su alias de sensor. No es un cambio de datos.

### 7.3 Documentación desactualizada (riesgo de diagnóstico erróneo)

- `PRUEBAS_EN_JUEGO.md` (raíz) **sigue siendo el de v22**: habla del ZIP `AstraAsedio_QA_v22_Completo_MO2.zip`, sha `2e5d5791…`, 44 entradas, y su tabla de diagnóstico dice que las únicas dos trazas posibles del guardia son `enable OAR and AstraAsedio_GuardAnim.esp…` y `missing or invalid model controls; controller stopped.` **Ninguna de las dos existe en el árbol v23–v29** (las reales son `Astra guard v27: operator refs missing…`, `Astra guard v26 status=…`, `Astra guard v27: backoff …`). Quien siga ese documento va a buscar síntomas que ya no se emiten y a instalar un paquete de v22.
- El `README.md` de raíz sí tiene el aviso de que lo vigente está en `docs/README_v29.md`; el de pruebas no.

### 7.4 Restos muertos del híbrido v1 (limpieza, no bugs)

`GLOB 0x0300080E AstraGuardiaOcupada`, `NPC_ 0x0300080F AstraGuardiaNPC` (con su script sensor) y `ACHR 0x03000940` en la celda `03000807 AstraAsedioTest`. El script consumidor (`AstraGuardiaAuto`) fue retirado del ACTI del núcleo (hoy `0x03000801` lleva sólo `AstraAsedioActi`), así que el global y el NPC quedan sin consumidor. Verificado que **no** queda ningún registro del mod con `AstraGuardiaAuto`. No hace daño; conviene limpiarlos al reempaquetar.

### 7.5 Menor: `blocked()` pausa también con `freezeTime`

`GuardRuntime::blocked()` devuelve `true` para la lista de menús **y** para `!main->freezeTime`. En v29 la pausa ya no cancela (sólo salta el frame), así que el efecto es benigno, pero cualquier congelación de tiempo ajena (algunos menús parciales de otros mods) deja la estación “quieta” sin traza. Vale la pena separar ambas causas en el log antes de la prueba en juego.

## 8. Recomendaciones priorizadas

1. **Prueba v29 con la DLL correcta** (`AstraSight 3.6.0` en la primera línea del log). Es el único paso que certifica la corrección (§5).
2. **Borrar el juego legacy de los voladizos** (`0xB40–0xB54`) o migrarlo. Es un cambio de datos, no de código, y elimina los dos guardias gemelos que nunca pueden animar (§7.1). Es la acción con mejor relación beneficio/riesgo de todo el informe.
3. **No activar `AstraAsedio_Whiterun.esp`** (no se empaqueta en v29). Si se quiere un puesto animado en la puerta, planificarlo como migración nativa (§7.2).
4. **Reemplazar `PRUEBAS_EN_JUEGO.md`** por el protocolo v29 con las trazas reales (§7.3).
5. **Limpiar los restos del híbrido v1** al reempaquetar (§7.4).
6. **Antes de agregar más estaciones**, generalizar el runtime de 2 puestos a N (§7.2); hoy cada puesto nuevo es una trampa silenciosa.

## 9. Referencias externas consultadas

- Formato de registros: [PACK – UESP](https://en.uesp.net/wiki/Skyrim_Mod:Mod_File_Format/PACK) (flags `Ignore Combat 0x100000`, `Weapons Unequipped 0x200000`, `Weapon Drawn 0x800000`, `No Combat Alert 0x8000000`; `PKCU` = plantilla de **PACK**), [IDLE – UESP](https://en.uesp.net/wiki/Skyrim_Mod:Mod_File_Format/IDLE) (`ENAM` = evento de animación, `DNAM` = ruta .hkx, `ANAM` = idle padre/anterior).
- OAR: prioridad por número mayor y necesidad de reemplazar la entrada de idle concreta del NPC: [Reddit r/skyrimmods](https://www.reddit.com/r/skyrimmods/comments/1d6scaf/does_anyone_know_of_a_mod_that_allows_you_to/), [Nexus Forums — idles de NPC que no se quedan](https://forums.nexusmods.com/topic/13499716-animations-not-looping/).
- `PlayIdle`/`IdleForceDefaultState` y sus trampas con paquetes de IA: [Nexus Forums — PlayIdle y estado atascado](https://forums.nexusmods.com/topic/2421344-trouble-using-playidle-with-weapon-getting-stuck-in-an-animation-state/).
