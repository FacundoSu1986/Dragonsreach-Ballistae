# Guardia de los voladizos — seguir con la mira y disparar (v29.2, DLL 3.6.3)

Estado: **no probado en Skyrim y no compilado** (la DLL requiere MSVC + CommonLibSSE-NG). Lo verificado fuera del juego está en "Qué se comprobó".

## Pedido

Con la pose resuelta (v29.1): que el guardia siga con la mira a quien pasa por Carrera Blanca, y que dispare a lo hostil — jugador hostil, NPC, dragón.

## Qué ya existía (v29)

`targets()`/`selectGuardTarget` ya elegían blanco (jugador visible ≤ 2100 u en ±60°; enemigos hasta 6000 u), `guardTrackYaw` giraba la montura a 20°/s y `shoot()` lanzaba el proyectil nativo con anillo de seguridad. Nada de eso se había visto funcionar porque la pose no se sostenía.

## Qué lo impedía (leído en el código)

1. **Sin elevación.** `pose()` fijaba `CTRL_ELEVACION` y `shoot()` exigía `bore.z≈0` + `horizontalFlight`: solo era alcanzable un blanco cuyo desnivel igualara la caída del proyectil. Casi nada abajo en la calle ni en el aire.
2. **El jugador nunca era enemigo** (`!player` en `enemy()` y `selectGuardTarget`) y `shoot()` lo protegía siempre.
3. **Sin diagnóstico**: ~15 `return false` mudos.

## Cambios

| Pieza | Dónde | Detalle |
|---|---|---|
| Solución balística | `guardAimSolution` (`GuardPolicy`) | Arco bajo; resuelve la `tan(pitch)` de una cuadrática e itera el giro del cañón (el muzzle se desplaza `along`/`up` respecto del pivote). `nullopt` fuera de alcance, de `[−30°,+30°]` o con entradas no finitas. |
| Seguimiento de elevación | `guardTrackPitch`, `pose()` | 25°/s, mismo patrón que el yaw; `pitch->local.rotate = rx(−pitch)·pitchBase`, igual que el visor del jugador (`Plugin.cpp`). |
| Geometría viva | `aimAt()` (`GuardRuntime.cpp`) | Pivote = `CTRL_ELEVACION`, boca = `ProjectileNode`; descompone el desfase a pitch 0 con el pitch actual. |
| Disparo | `shoot()` | `bore` real del nodo debe coincidir con la solución (`GuardBoreTolerance` .008); trayectoria `guardArcTrajectory`; tiempo de vuelo por la componente horizontal del `bore`; verificación de impacto y anillo de seguridad **sin cambios**. |
| Seguimiento visual | `tick()` | Quien no es enemigo se sigue por línea de visión (clamp a ±30°); el enemigo recibe la elevación balística. |
| Jugador hostil | `playerHunted()`, `enemy(…, hunted)`, `GuardCandidate::hunted`, `GuardAllowPlayerTarget` | El jugador es enemigo solo si está en combate **y** algún guardia de la facción de Whiterun (`0x28172`/`0x2BE39`), cargado y no operador, está en combate y es hostil al jugador. Interruptor de política `GuardAllowPlayerTarget`. En `shoot()` el jugador no se añade a los protegidos cuando es el blanco; el resto sigue protegido. |
| Alcance de enemigos lejanos | `selectGuardTarget(…, ballistic=true)` | Pasados 2100 u se exige solución balística en vez de tiro plano. Con `ballistic=false` (por defecto) la conducta v25 se conserva. |
| Diagnóstico | `shoot()` → `s.shotRefusal`; `tick()` | `guard v29.2 shot refused … reason=` (≤ 1 cada 5 s), `guard v29.2 player-hostile`, y en la pose `pitch`, `desiredPitch`, `hunted`. |

Versión 3.6.3 en `Plugin.cpp`, `GuardRuntime.cpp`, `CMakeLists.txt`, `verify_binary.py`, `build_native.py`; `verify_zip_v29.py` acepta 3.6.0/3.6.2/3.6.3.

## Límites conocidos (decisiones, no olvidos)

- **Las manos no suben con el arma.** El clip de pose (HKX) es fijo; al elevarse el cañón, las muñecas quedan en la posición de reposo. Por eso el rango es ±30°. Solución real: clips por nivel de elevación o IK (fuera de alcance; HKX binarios).
- **Sin adelanto de puntería.** El proyectil va a la posición actual del blanco y la verificación exige impacto en su collider actual. Un dragón en pasada rápida se falla; un NPC en combate cuerpo a cuerpo o un dragón posado, no. Añadir adelanto exige relajar esa verificación: decisión de seguridad aparte (fase 2).
- Giro ±60° y 20°/s por el contrato del puesto (`guardOrbit`).
- Solo los dos voladizos (`0xB70/0xB80`); la ballesta de la puerta (`0xB10`) no usa el runtime nativo.
- **Orientación visual del virote**: el miembro de pitch de `ProjectileRot` se deja en 0 (se desconoce su signo). La velocidad lineal sí se fija desde el `bore`, y el log compara `velocityZ` con `expectedZ`.

## Qué no está verificado

1. Que `playerHunted()` refleje "los guardias están en combate contra el jugador" (el operador tiene IA aislada y no sirve de señal).
2. Que el motor conserve la velocidad elevada tras `Projectile::Launch`.
3. Que la pose siga limpia con la ballesta elevada (el análisis de manos mide contra el reposo: `handErrorL/R` seguirá siendo ≈ 3 u aunque el cañón suba).
4. Que `GuardRuntime.cpp` compile.

## Qué se comprobó

- `native/tests/guard_aim_tests.cpp` (55 aserciones): el pitch resuelto, integrando la trayectoria de forma independiente, deja el virote a < 1 u del punto de mira en 7 geometrías (abajo, a nivel, arriba; 800–5000 u; con y sin palanca de la boca); arco bajo; límites y alcance; NaN; seguimiento de pitch; `guardBore`; trayectoria plana = `guardTrajectory`; jugador solo como enemigo con `hunted`; alcance balístico.
- CTest 17/17 (línea base v29.1: 16/16). Los tests v23–v29 de política no cambian.
- `tests/test_guard_aim_contracts.py` (16 contratos de estructura, incluida la correspondencia de marcadores de `spdlog`), `tests/test_analyze_guard_log.py` (15) y la suite completa: el mismo conjunto de 65 fallos heredados que antes (faltan `dist/` y módulos fuente), sin fallos nuevos.
- `test_v29_guard_simple.py::test_shoot_keeps_safety_…` actualizado: el contrato plano de v29 (`enemy(target,guard)`, `horizontalFlight(`) queda superado por v29.2; se conservan `guardProjectileContract`, `guardPathSafe`, `visible` y el `Launch` como piezas de seguridad.
- **No** se compiló `GuardRuntime.cpp`/`Plugin.cpp`; **no** se probó nada en Skyrim.

## Si ya compilás una v30 local

Estos cambios tocan `GuardRuntime::pose` (firma con pitch), `targets`, `shoot` (reescrito), `tick` y `Slot`. Tu `tick` de v30 (reloj/hitch, pose soportada antes de disparar, mundo activo) hay que fusionarlo a mano; conservá de v30 lo que ya probaste.
