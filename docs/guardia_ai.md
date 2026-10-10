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

## Qué genera build_plugin.py

IDs nuevos (dinámicos terminaban en `0x925`, luces `0x930–33`):
- `0x0300080E` GLOB `AstraGuardiaOcupada` (float, arranca 0.0).
- `0x0300080F` NPC_ `AstraGuardiaTorre` — clon del primer donante de `guardia.donores_npc`
  que exista en `Skyrim.esm` (orden por defecto: GuardWhiterun, GuardSolitude, GuardWindhelm,
  GuardMarkarth, GuardRiften). Conserva packages/facciones/combate del donante (v1); solo
  cambia EDID/FULL y se le agrega el VMAD de `AstraGuardiaNPC`. Si ningún candidato existe,
  el build falla con error explícito: revisar los EDID en xEdit (`Skyrim.esm` → NPC_) y
  ajustar `donores_npc`.
- `0x03000940` REF del NPC en la celda de la torre, en `guardia.posicion`, mirando a la
  ballesta, con XLKR recíproco ballesta↔guardia (así `GetLinkedRef()` funciona de ambos lados).
- La ballesta ACTI pasa a llevar **dos** scripts: `AstraAsedioActi` + `AstraGuardiaAuto`
  (VMAD multi-script), con todas las properties llenas desde `config.json`.

El validador del propio build (`validate_plugin`) ahora verifica: 2 scripts en el ACTI, forms
y valores del `AstraGuardiaAuto`, GLOB bien formado, VMAD del NPC sin properties, XLKR
recíprocos y NAME del ref → NPC. El reporte JSON incorpora la sección `guardia`.

## Runbook (máquina Windows del usuario)

1. `python scripts/build_plugin.py` — regenera `mod/AstraAsedio.esp` con el guardia.
   Requiere `build/Dawnguard.esm.donors.json` (se genera con el parser del repo); si pide
   donante de NPC, revisar `guardia.donores_npc` en xEdit.
2. `python scripts/compile_papyrus.py` — compila TODOS los `.psc` por glob (los dos nuevos
   entran solos). Requiere el Skyrim Papyrus Compiler configurado como en las builds previas.
3. Instalar/reemplazar el ESP + scripts compilados en el perfil MO2 de QA (como siempre).
   El nativo (`AstraSight.dll`) NO cambia: la IA usa solo Papyrus + SKSE (NetImmerse).
4. En juego: `coc AstraAsedioTest`, agredir al guardia de la torre (o soltar un dragón/lobos
   cerca) y NO operar la ballesta: el guardia entra en combate → la torre apunta sola,
   espera ~0,1 s de asiento y dispara el virote real contra el blanco del guardia.

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

- **Packages del donante**: el clon conserva el sandbox/paquetes del guardia original. Si en
  juego el NPC intenta caminar a su ciudad, reemplazar sus packages por uno de "stay" anclado
  a la torre con xEdit (packages del NPC_ o un `Package` propio con editor location = la
  celda de la torre). Es el ajuste más probable tras la primera prueba.
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

Queda para la máquina del usuario: compilar los PSC (el compilador es la palabra final en
sintaxis), correr `build_plugin.py` con los donors reales, y la prueba in-game.
