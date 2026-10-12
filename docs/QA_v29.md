# Verificación v29

Trabajo en la rama `astra-v29-guardia-simple` del worktree `Ballesta_Astra_v28`, sobre la instantánea `5ce9947` (v23–v28). La instalación MO2 y la partida del usuario no se modificaron.

## Diagnóstico medido

- **HKX.** Con la cinemática directa sobre el `skeleton.hkx` vanilla, en todos los frames, las muñecas quedan a 0,026 u de `(±33,6; 143,8; 100,5)` en el espacio de la ballesta con el clip de sostener, y a 0,027 u con los de giro. El de disparo se aparta hasta 1,11 u en el gesto del gatillo, por diseño (0,75 u adelante y 0,8 u abajo).
- **NIF.** La geometría de `ballesta_guardia.nif` (ACTI 0xB04) llega exactamente a `(±33,6; 137,9; 101,67)`.
- **MO2.** El mod `AstraAsedio_QA_v` coincide en SHA-256 con el repositorio en ESP, NIF y HKX; solo la DLL es la de v27. Ningún otro mod activo reemplaza `IdleHandsBehindBack`.
- **`mt_behavior.hkx` vanilla.** El evento `IdleHandsBehindBack` (id 482) entra con `0.5secondBlendToAnimDriven`, e `IdleForceDefaultState` sale con 0,2 s. El subgrafo está hecho solo de máquinas de estado, sin pesos por hueso. Vanilla trae además `_exit`, que OAR no reemplaza.
- **Log de v27.** Registra 7 confirmaciones OAR, 0 agarres y 0 virotes, y dos cancelaciones por `hold replacement not observable`.
- **Causa.** Apuntar y disparar dependían de `gripConfirmed`. El runtime relanzaba el idle pasando por el reposo o cancelaba ante muestras tardías. En v28, la tolerancia de 16 u se incumple siempre durante la mezcla de entrada de 0,5 s.

## Cambio

El diseño está en `docs/superpowers/specs/2026-10-11-guardias-v29-design.md`.

- **Agarre.** El clip de sostener resuelve el agarre. Se eliminaron la IK de manos y pies, `settleGrip` y la confirmación de agarre.
- **Telemetría OAR.** Las muestras son solo telemetría. Si faltan durante 3 s, se pide de nuevo el idle, como máximo una vez cada 6 s, y nunca se cancela por eso.
- **Seguimiento.** `guardTrackYaw` acota el giro a 20°/s y ±60°. `pose()` distingue tres resultados: `ok`; `blocked`, que conserva el yaw anterior y cancela recién tras 2 s seguidos; e `invalid`, que cancela.
- **Disparo.** Lo decide `guardShouldFire`: enemigo, tiro alcanzable, error de 0,25° como máximo y enfriamiento de 2,5 s. `shoot()` mantiene todas las comprobaciones de seguridad, pero ya no sincroniza con el clip corporal. `Fire` del NIF arranca con el lanzamiento y `Reset` a los 0,2 s.
- **Menús y pausas.** Solo `Loading Menu`, la carga, la partida nueva y el revert invalidan. Antes lo hacía cualquier menú, registrado con el motivo engañoso `load/new game/revert`. Un `dt` mayor que 0,1 s ya no cancela.
- **Sin cambios.** Papyrus (reintento acotado de v28), los ESP, NIF, HKX y la configuración OAR.

## Comprobaciones externas

- **CTest.** 15/15, con `AstraV29GuardTests` (36 aserciones de seguimiento, vigilancia del clip y decisión de disparo).
- **Contratos Python.** `test_v29_guard_simple` cubre estructura, versión 3.6.0 y recursos idénticos a v27. `test_v23_release`, `test_v26_guard_ai` y `test_v28_runtime` siguen activos. Los tres contratos v27/v28 que exigían las compuertas retiradas o la DLL 3.5.x se marcaron explícitamente como reemplazados.
- **Suite completa.** Se comparó contra la instantánea v28 y no hay fallos nuevos. Los fallos heredados (por ejemplo, el hash de `verify_sight_path.py` y donantes de Dawnguard ausentes) existen igual en v28.
- **Release.** `verify_v29_release.py` pasa sus 8 compuertas: regresiones de cámara y entrada del jugador, HKX, plugins, bytecode, compilación nativa con CTest y metadatos PE.
- **ZIP.** Es reproducible y se verificó de forma independiente (`verify_zip_v29.py`).

La revisión de código se hizo en la misma sesión; no es independiente (`reports/review_v29.json`).

## Pendiente en Skyrim

- Que ambos operadores mantengan las manos sobre las empuñaduras de forma continua, con `handErrorL/R` en torno a 3 u.
- Seguimiento del jugador y de visitantes a lo largo de −60°/+60°, ignorando a residentes y guardias de Whiterun que no sean hostiles.
- Disparo a un enemigo válido. Que se bloquee ante aliados cruzando, obstáculos, objetivos a otra altura o fuera del sector.
- Comportamiento junto a barandas al girar, con muerte, stagger, carga/descarga, el jugador tomando el puesto y menús abiertos.
