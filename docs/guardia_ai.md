# IA del guardia — torre autónoma híbrida (v1)

Modo **híbrido** elegido por el usuario: un NPC real (clon de un guardia vanilla) vive en la
torre con su IA vanilla de presencia, y la ballesta se defiende sola mientras ese guardia esté
en combate. El disparo automático usa el **virote real de asedio** (mismo `Weapon`/`Ammo`/`PROJ`
que el jugador, con su daño de asedio), frenado con reglas de enganche conservadoras.

División de responsabilidades:

| Pieza | Script | Rol |
|---|---|---|
| Sensor | `AstraGuardiaNPC.psc` (en el NPC) | Puente del combate vanilla: `OnCombatStateChanged` → avisa a la torre por linked ref. Sin properties. |
| Arma | `AstraGuardiaAuto.psc` (2.º script de la ballesta ACTI) | Torreta: apunta nodos, resuelve balística, valida seguridad, dispara. 26 properties. |
| Árbitro | `GlobalVariable AstraGuardiaOcupada` | 1 mientras el jugador opera la máquina o corre la demo; la torre cede siempre. |
| Cerrojo | hooks en `AstraAsedioActi.psc` | Sube el global al abrir sesión/demo y lo baja al cerrar (con ventana para la demo). |

## Archivos

Nuevos:
- `mod/scripts/source/AstraGuardiaAuto.psc` — el cerebro (fases 0–6, sin bucles ni states de
  Papyrus; `RegisterForSingleUpdate` por fase, save-safe).
- `mod/scripts/source/AstraGuardiaNPC.psc` — el sensor.
- `scripts/verify_guardia_ai.py` — suite de verificación sin Papyrus Compiler (ver abajo).

Modificados:
- `mod/scripts/source/AstraAsedioActi.psc` — 5 hooks del global (grep `OcupadaGuardia`:
  property l.7, demo l.151, sesión l.294, cierre de demo en `OnUpdate` l.1205, ventana de demo
  en `EndSession` l.1747).
- `scripts/build_plugin.py` — genera todo el wiring nuevo en el ESP.
- `config.json` — sección `guardia` (17 claves).

## Qué genera el build (v22: `patch_plugin_v12.py` + `build_modular_v13.py`)

> **Corrección de integración (v22).** Este documento decía que el core lo regeneraba
> `scripts/build_plugin.py`. Es **falso** y rompía el producto: `build_plugin.py` arma un ESP
> desde cero con la celda de pruebas, y **sin** las formas modulares
> `0x030009C0` / `0x03000B00-03` que los tres addons referencian como master 03
> (Atalaya → `03000801`/`03000808`/`030009C0`; Whiterun → `030009C0`/`03000B02`/`03000B03`;
> WhiterunTorres → `03000B02`). Correrlo sobre el repo dejaba los addons con masters
> colgantes. El core embarcado sale de `patch_plugin_v12.py` (sobre el baseline v11 inmutable)
> + `build_modular_v13.py` (formas modulares), y es ahí donde vive el guardia.

IDs del guardia (mismos en los dos builders, para que `validate_plugin` sirva de gate único):
- `0x0300080E` GLOB `AstraGuardiaOcupada` (float, arranca 0.0).
- `0x0300080F` NPC_ `AstraGuardiaNPC` — clon del primer donante de `guardia.donores_npc`
  que exista en `Skyrim.esm`. La lista es una **prioridad**, no un conjunto: el donante es
  `donores_npc[0]` (`GuardWhiterunCityGeneric`). Si ningún candidato existe, el build falla
  con error explícito: revisar los EDID en xEdit (`Skyrim.esm` → NPC_).
- `0x03000940` ACHR del NPC en la celda de pruebas, en `guardia.posicion`, mirando a la
  ballesta, con XLKR recíproco ballesta↔guardia. En el linaje v11 esa dirección queda libre
  porque el parche borra las 64 piezas vanilla que empiezan en `VANILLA_FIRST` (mismo valor).
  El record tiene que ser **ACHR**: el engine solo instancia actores desde ACHR.
- La ballesta ACTI pasa a llevar **dos** scripts: `AstraAsedioActi` + `AstraGuardiaAuto`
  (VMAD multi-script), con todas las properties llenas desde `config.json`.

**Herencia del donante**: hay que borrar dos bits de `templateFlags` (ACBS +18) o el clon no
obedece al config: `0x0080` BaseData (sin esto el `FULL` inyectado se ignora y el guardia se
llama como el donante) y `0x0020` AIPackages (sin esto hereda el paquete del donante y se va
caminando a su ciudad). Con `guardia.paquete_torre` se reemplaza el `PKID` por un PACK anclado
a la ubicación del editor (`PLDT type=3`, sin `CTDA`) — `GuardPost` (`0001C9FF`).

El validador del propio build (`validate_plugin`) verifica: 2 scripts en el ACTI, forms y
valores del `AstraGuardiaAuto`, GLOB bien formado, VMAD del NPC sin properties, XLKR
recíprocos y NAME del ref → NPC. Los reportes JSON (`reports/plugin_v12.json`) incorporan la
sección `guardia`.

## Runbook (máquina Windows del usuario, sobre v21)

> Desde el merge con v21 este sistema convive con las torres de ciudad de los addons
> (`AstraAsedioGuard` en `addons/Whiterun*`, estaciones autónomas): este híbrido es para
> LA BALLESTA DEL JUGADOR en la celda de pruebas. **Sí comparten el core** `mod/AstraAsedio.esp`
> (los addons lo referencian como master 03), así que el core se reconstruye una sola vez y los
> addons no se tocan.

1. `python scripts/build_assets.py` (y el resto del pipeline v21, como siempre).
2. `python scripts/build_modular_v13.py` — corre en cadena `patch_plugin_v12.py` (baseline v11
   → core con estructura, escudos, Z de la ballesta, navmesh, **y el guardia**) y después
   agrega las formas modulares `0x03000B00-04`. Salida esperada:
   `V12_PLUGIN_PATCHED … guardia GuardWhiterunCityGeneric` + `MODULAR_CORE_BUILT 66`.
   **Los addons no se generan acá**: `place_atalaya_v20/v21.py` copian el Atalaya de la
   revisión anterior y `build_modular_v17.py` arma WhiterunTorres.
   **No correr `scripts/build_plugin.py`**: pisa `mod/AstraAsedio.esp` con un ESP sin las
   formas modulares y deja los tres addons con masters colgantes.
2b. **Torreta baja (v22)**: `python scripts/bajar_ballesta.py mod/meshes/AstraAsedio/ballesta.nif mod/meshes/AstraAsedio/ballesta_guardia.nif`
   produce el NIF del guardia (pivote 117, −36 u) parcheando bytes. Después:
   `python scripts/build_modular_v13.py` con `main(addons=True)` para regenerar el addon
   Whiterun (reproduce el embarcado byte a byte y **no toca el Atalaya**), y
   `python scripts/build_modular_v17.py` para los voladizos. Verificar con
   `python scripts/verify_core_v22.py` y `python scripts/verify_torreta_baja_v22.py`.
3. `python scripts/compile_papyrus.py` — compila TODOS los `.psc` por glob (los dos nuevos
   entran solos). El nativo NO cambia: la IA usa solo Papyrus + SKSE (NetImmerse).
4. **Demo del guardia (animación `GuardiaCiclo`)**: la secuencia NO viaja en el NIF del
   repo — se hornea en tu máquina con `blender --python scripts/build_guardia.py`
   (después de build_assets). Luego de regenerar el NIF, activar la ballesta **en sigilo**
   dispara la demo (~22 s); activación normal = operar la ballesta como siempre. Si el
   log muestra `GUARDIA_CICLO_MISSING`, falta ese paso. **Advertencia v21**: build_guardia
   fue escrito contra el NIF de v10; si la torre nueva cambió los nodos que recorta
   (torno/palanca), puede requerir ajuste.
5. En juego: `coc AstraAsedioTest`, agredir al guardia de la torre (o soltar un dragón/lobos
   cerca) y NO operar la ballesta: el guardia entra en combate → la torre apunta sola,
   espera ~1 frame de asiento y dispara el virote real contra el blanco del guardia.

## Dos torretas: alta para el jugador, baja para el guardia (v22)

La v22 nació de bajar la torreta 36 u (pivote 153 → 117) para que la animación del guardia
quede a la altura de las manos. La bajada se hacía sobre el `ballesta.nif` **global**, y eso
rompió la **mira nativa del jugador**: medido en `reports/sight_path_v22_FAILED.json`, la
holgura cámara→malla del arma cae de 10,29 u a 2,94 u (el mínimo es 8; la esfera del motor
mide 12–15 u) y se pierde `near_plane_check_falsified`. El pivote en 117 deja el anclaje de
cámara por debajo del piso de 65 u que exigen `scripts/sight_pose.py` y `kMinCameraHeight`
de `native/src/Core.cpp`.

La solución es **dos NIF y dos ACTI**, con el MISMO contrato (clone del ACTI del jugador sin
`VMAD`: los scripts los pone el REFR que coloca):

| ACTI | EDID | MODL | Pivote | Quién lo usa |
|---|---|---|---|---|
| `0x03000801` | `AstraAsedioBallesta` | `ballesta.nif` | 153 | el jugador (core `03000901` + Atalaya `04000A00`) |
| `0x03000B02` | `AstraGuardBallista` | `ballesta.nif` | 153 | sólo tombstones deshabilitados (`04000B40/B50`) |
| `0x03000B04` | `AstraGuardBallistaBaja` | `ballesta_guardia.nif` | 117 | los guardias (`04000B70/B80` y `04000B10`) |

La regla que hace segura la torreta baja: **ninguna colocación activa del ACTI bajo puede
dejar que el jugador la opere** (`AllowPlayerTakeover=false`) ni declarar mira nativa
(`UseSightCamera=false`). La mira vive en `AstraAsedioActi` y en
`AstraAsedioStation extends AstraAsedioActi`; `AstraAsedioGuard` **no** la usa, y además no
lleva `MuzzleAlto` ni `PitchPivotHeight`: lee `ProjectileNode` del NIF en runtime, así que el
mismo script sirve para las dos alturas. `verify_core_v22.py` (sección 6) recorre **todas**
las referencias a `0x03000B04` en los tres addons y falla si alguna habilita al jugador —una
colocación nueva que se olvide del flag rompe el test.

Consecuencia de diseño aceptada: los **voladizos de WhiterunTorres pasan a ser puestos de
guardia** (antes eran estaciones compartidas: `AllowPlayerTakeover=true`,
`UseSightCamera=true`). El jugador conserva la mira nativa en la torreta del core. El addon
`AstraAsedio_Whiterun.esp` (torreta guardia-exclusiva `04000B10`) también apunta al ACTI bajo,
aunque ese addon está deprecado (`reports/modular_v14.json` →
`replace_old_plugin: AstraAsedio_Whiterun.esp (disable)`).

### Estado de la integración (2026-10-10, v22)

Verificado en el sandbox, sin Skyrim:
- Cadena verde: `patch_plugin_v12.py` → `build_modular_v13.py` (`MODULAR_CORE_BUILT 65`), con
  `validate_plugin` pasando sobre el ESP final.
- Core `mod/AstraAsedio.esp`: 66 records, sin FormIDs duplicados, masters
  `[Skyrim.esm, Update.esm, Dawnguard.esm]`, formas modulares presentes, ACTI con dos scripts,
  `PitchPivotHeight = 117.0` (sigue la bajada de 36 u), GLOB/NPC_/ACHR y XLKR recíprocos.
- Los tres addons (incluido el Atalaya v21 restaurado, sha `7491276e…`) resuelven todas sus
  referencias a master 03 contra el core nuevo: 0 colgantes.
- `python scripts/verify_guardia_ai.py` → TODO OK. `python scripts/compile_papyrus.py` →
  exit 0, los 8 scripts compilan (incluidos `AstraGuardiaAuto` y `AstraGuardiaNPC`).
- **Pendiente en tu máquina**: `build_assets.py` (Blender), `build_guardia.py`, y la prueba
  in-game. El core v22 invalida los `files_sha256` de `reports/baseline_v*.json` y el assert
  de `build_modular_v17.py` (que exige el core == v14): hay que re-derivar la baseline v22
  antes de volver a empaquetar con `package_v21.py`.

### Bugs reales que traía el merge (corregidos en v22)

1. `donores_npc` apuntaba a cinco EDID inexistentes (`GuardWhiterun`, `GuardSolitude`, …):
   el build moría con "Guard NPC donor not found". Reemplazados por cinco EDID verificados
   contra `Skyrim.esm`.
2. `find_guard_npc` devolvía el primer candidato **en orden de archivo**, así que
   `donores_npc[0]` era decorativo (`Skyrim.esm` lista `GuardWindhelmImperial` antes).
3. `Math.Atan2(...)` en `AstraGuardiaAuto.psc` (líneas 584 y 590): `Math.psc` no tiene `Atan2`
   (solo `Atan`); el script define su propio `Atan2` y los otros dos call sites ya lo llamaban
   sin calificar. **No compilaba.**
4. `float[] Function ResolverBlanco(...)` con `return None`: el compilador emitía
   `Cast float[] None`, que el gate de `compile_papyrus.validate_assembly` rechaza
   (`BYTECODE_REJECTED: None cast into array temporary`). Reescrito como `bool` + array de
   salida (`new float[0]` no es opción: Papyrus exige 1..128 elementos).
   La suite `verify_guardia_ai.py` no vio ninguno de los dos últimos porque porta el código a
   Python y **nunca invoca el compilador**.
5. El runbook mandaba regenerar el core con `build_plugin.py`, que borra las formas modulares
   que los addons necesitan (ver arriba).


## Comportamiento esperado (qué verificar in-game)

- Al entrar el guardia en combate, la torre gira suave (`yaw_speed`/`pitch_speed` °/s) hacia
  el blanco, engancha a <1,5° de error, y dispara ráfagas de hasta `max_rafaga` virotes con
  `enfriamiento` entre ráfagas.
- El blanco lo decide SIEMPRE el combate del guardia (`GetCombatTarget`), y cada disparo
  revalida TODAS las reglas (`ReglaEnganche`): hostil al jugador, detectado por el guardia
  (LOS), dentro de arco/alcance, elevación posible, y geometría de seguridad (el jugador y el
  guardia fuera de la línea de fuego con margen `margen_linea`, nadie a menos de
  `margen_impacto` del punto de impacto). Si algo falla, no dispara y lo dice por traza.
- Si el jugador activa la ballesta a mitad de una maniobra, la torre cede al instante
  (lee `AstraGuardiaOcupada`) y reintenta a los ~8,5 s si el guardia sigue peleando.
- Al terminar el combate del guardia (o morir), la torre queda DURMIENDO sin consumir
  updates. Tras cargar partida, recupera el rumbo leyendo la rotación de los propios nodos.
- Para QA: `guardia.qa_log: true` en config → traza Papyrus con prefijo `AstraGuardiaAuto`
  (motivo de cada no-disparo, blanco nuevo, etc.). Ver con el log de MO2.

## Calibración (config.json → sección `guardia`)

| Clave | Efecto | Default |
|---|---|---|
| `yaw_speed` / `pitch_speed` | Velocidad de giro de la torreta (°/s). Subir si llegan tarde a blancos rápidos. | 40 / 20 (top-level) |
| `arc_max` | Ángulo máximo respecto del rumbo 0 (adelante) que la torre acepta. | 60° |
| `alcance_min` / `alcance_max` | Distancias mínima/máxima de disparo (unidades). | 900 / 8400 |
| `max_rafaga` / `enfriamiento` | Virotes por ráfaga / pausa entre ráfagas (s). | 3 / 8.0 |
| `margen_linea` / `margen_impacto` | Márgenes de seguridad de la línea de fuego y del punto de impacto (u). | 320 / 384 |
| `anticipacion` | Adelanto del apuntado según la velocidad medida del blanco (0 = desactivado). | 0.5 |
| `tick_segundos` | Paso del loop de fases (define el granulado del slew: `yaw_speed·tick`). | 0.08 |
| `muzzle_alto` / `muzzle_adelante` | Offset del ProjectileNode sobre la raíz (z / y). | 172.6 / −224.0 |
| `velocidad_proyectil` / `gravedad_proyectil` | Balística: 5400 u/s y 0.35·9.81·70 = 240.345 u/s² (PROJ donante, igual que `native/src/Core.cpp`). | — |

La balística es la misma del registro v08: a 5250 u en nivel, elevación 1,24° y caída
113,589 u (`kSightZeroDrop`). El solver usa la solución baja del ángulo (tiro tenso, mismo
comportamiento que la mira del jugador).

## Limitaciones conocidas v1 (y su salida)

- **Packages del donante** (resuelto en v22): el clon heredaba el sandbox/paquetes del guardia
  original porque el único paquete del donante elegido (`GuardWhiterunCityGeneric`) era
  `CWPatrolAndGuardWhileHoldContested` (`000587E1`), una patrulla atada a los holds: el
  guardia se iba caminando de la torre. Ahora `guardia.paquete_torre` (`GuardPost`, `0001C9FF`,
  `PLDT type=3` sin `CTDA`) reemplaza el `PKID` y se borra el bit `AIPackages` de
  `templateFlags`. Poner `null` para volver al comportamiento v1.
- **Muzzle**: el offset del ProjectileNode se aplica asumiendo la raíz de la ballesta a 0° en
  la celda (así está colocada). Si algún día la ballesta se coloca girada, hay que rotar el
  offset con el yaw de la raíz.
- La torre dispara con el virote REAL: el daño de asedio es alto. Los márgenes de seguridad
  son conservadores a propósito; si el usuario quiere más agresividad, bajar `margen_linea` y
  `margen_impacto` gradualmente y probar.
- No hay IA de "elegir mejor blanco": dispara al `GetCombatTarget()` del guardia, punto. Si
  el guardia pelea contra varios, la torre sigue al objetivo del guardia (coherente con el
  rol: el guardia es el cerebro táctico).
- La GLOB `AstraGuardiaOcupada` es una por plugin: pensada para UNA torre en el mundo. Con
  dos torres, la sesión del jugador en una dormiría también la otra (validar por distancia
  o GLOB por instancia si algún día hay más).
- La liberación del disparo usa timer (`ReleaseSegundos`), no eventos de animación: es
  exactamente lo que hace la vía del jugador (`elapsed >= ReleaseSeconds`), y no hay
  `RegisterForAnimationEvent` en todo el mod. Si se quiere precisión por frame en el futuro,
  sería la vía v2.

## Verificación hecha en sandbox (sin Papyrus Compiler ni Skyrim)

`python scripts/verify_guardia_ai.py` — todo verde a 2026-10-10 (incluye la revisión
externa aplicada, ver abajo):
1. Lint estructural de los 4 PSC (bloques Function/Event/If balanceados, sin `Utility.Wait`,
   sin `GetVelocity*` — esa API no existe en Papyrus y fue reemplazada por muestreo entre
   ticks). Este lint encontró y corrigió dos bugs reales antes del handoff: un `EndFunction`
   cerrando un `Event`, y la llamada inexistente `GetVelocityX`.
2. Solver balístico (puerto Python del PSC) con **física independiente**: cada caso se
   verifica integrando el vuelo (Euler fino) y comprobando que el proyectil pasa por el
   blanco (error < 2 u). Casos: nivel a 75 m (reproduce `kSightZeroDrop` = 113.589 exacto,
   sag 0), blanco 40 u debajo a 30 m (pitch −0.59°), blanco 300 u debajo a 75 m (pitch
   −2.03°), blanco 150 u arriba (dragón), blanco debajo ⇒ pitch menor que a nivel
   (regresión anti-signo). El yaw coincide con `gunDirection` del nativo; fuera de alcance
   devuelve `None`.
3. `Atan2` del PSC vs `math.atan2`: 20.000 casos.
4. Roundtrip `vmad_multi` ↔ `read_vmad` (2 scripts, properties tipo 1/3/4/5) + serialización
   de GLOB y XLKR.
5. Consistencia `config.guardia` ↔ claves leídas por `build_plugin.py` en ambas direcciones,
   y constantes == `Core.cpp`.

### Revisión externa aplicada (2026-10-10)

Una revisión independiente del código detectó un bug balístico real y tres riesgos, todos
corregidos y cubiertos por tests:
- **Signo invertido en el discriminante** (el bug grave): el solver usaba la altura de la
  boca sobre el blanco donde la fórmula pide la altura del **blanco sobre la boca**
  (`dzRel = tz − mz`). Con h=0 (los únicos tests originales) ambos signos coinciden, así
  que pasaba; con la torre elevada (blanco debajo), apuntaba ~2–5° demasiado alto y el
  virote caía cientos de unidades lejos. Corregido + tests con integración del vuelo.
- **Virote visual**: las anim Gamebryo no restauran la escala del nodo (en la vía del
  jugador la sube el script del ACTI). La torre ahora restaura `VisualBoltNode` a 1.0 en
  `FaseRecarga`, en la cesión al jugador y en `OnLoad` (defensa post-save).
- **Cesión en fase 4**: si el jugador tomaba la máquina justo tras la anim de fuego, el
  proyectil nunca salía (anim vacía). Ahora la rama de cesión completa la liberación y
  rearma antes de dormir.
- **Jugador como blanco**: si el jugador agredía al guardia, pasaba el filtro de hostilidad
  (es hostil al guardia). Ahora hay un check explícito `BLANCO_JUGADOR` antes de cualquier
  regla, además de la geometría de seguridad.
- Menores: `OnCellDetach` duerme la torre con la celda descargada; `tick_segundos`
  0.12 → 0.08 (slew menos escalonado).
- Desestimados con criterio: cachear `Game.GetPlayer()` (es O(1) en el runtime, es la
  práctica estándar llamarlo directo); suavizar la velocidad medida (el propio slew filtra
  el jitter y el muestreo se resetea al cambiar de blanco); liberar por evento de animación
  (la vía del jugador usa timer: `elapsed >= ReleaseSeconds`).

### Revisión adversarial (2026-10-10, segunda pasada)

Una segunda revisión (esta vez del código final, no de un snapshot) encontró y corrigió:

**Bloqueantes:**
1. **El ref del guardia se escribía como `REFR`** — el engine solo instancia actores
   desde records `ACHR`; un REFR con base NPC_ es ignorado y el guardia **no aparecería
   en el juego**. `reference()` ahora acepta `tipo=` y el guardia_ref sale como ACHR; el
   validador lo exige. (Este bug lo habría descubiertu tu agente local en la primera
   prueba, con el guardia ausente y sin traza que explique nada.)
2. **`LineaSegura` con `||` en vez de `&&`**: un actor *cerca del blanco* quedaba marcado
   como seguro — exactamente el guardia peleando en melee, el caso más común del híbrido.
   Además el guardia no tenía el chequeo de `MargenImpacto` que sí tenía el jugador. Con
   daño de asedio y radio de 128 u, la torre le habría tirado el virote encima. Corregido:
   `seguro = lejos de la línea && lejos del blanco`, más `GUARDIA_CERCA_DEL_BLANCO`
   espejo del chequeo del jugador. Test de regresión en la suite.

**Reales (degradaban el comportamiento):**
3. **Reintento de cesión que moría**: si el update de reintento (8,5 s) caía después de
   que el jugador soltó la máquina, `OnUpdate` con fase 0 no hacía nada y la torre no
   volvía a defender aunque el guardia siguiera en combate (su evento de combate no se
   re-dispara: el estado no cambió). Nueva rama fase 0 → re-despertar.
4. **Signo invertido al leer el pitch del nodo** (`atan2(-m[5], m[4])`): tras cada load el
   pitch se recuperaba negado y el slew saltaba el doble. Ahora `atan2(m[5], m[4])`.
5. **Slew sin clamp de dt**: tras recarga (1,28 s) o enfriamiento (8 s) el paso usaba el
   dt completo → giros de hasta 320° en un update. El avance ahora se mide contra el tick
   nominal (la velocidad de medición del blanco sigue usando el dt real).
6. Menores: `hayPosPrev` no se reseteaba al reemplazar un blanco muerto (lead con
   velocidad cruzada entre dos actores); `rafaga` no se reseteaba al despertar; el Reset
   se lanzaba tarde (el ciclo duraba ~2,4 s en vez de ~1,3 s, con el virote invisible el
   doble de tiempo).

**Verificado y descartado:** firma de `GetNodeLocalRotationMatrix` idéntica a la del ACTI
(compila igual); XLKR con keyword 0 es el "unnamed linked ref" del CK (vale para
`GetLinkedRef()`); el lint sí contaba los `if` del ACTI (usa minúsculas); la cancelación
catastrófica `v²−√disc` en float32 deja ~0,001° de error en el pitch (irrelevante);
`PitchMin=−5` es el mismo límite del jugador (no es un bug que no dispare a blancos bajo
la base); `CalmaCombat` deja terminar la secuencia iniciada a propósito (documentado).

Queda para la máquina del usuario: compilar los PSC (el compilador es la palabra final en
sintaxis), correr `build_plugin.py` con los donors reales, y la prueba in-game.
