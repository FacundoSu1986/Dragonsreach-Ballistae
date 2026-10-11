# Comprobación de Astra Asedio v27

Derivada de v26. No se ha probado en Skyrim. Esta copia de trabajo no toca la instalación MO2 ni el árbol v23 original.

## Base de evidencia

- **Sesión v26 real, 2026-10-11 17:12–17:14** (`AstraSight.log`, 81 893 bytes, verificado leyendo el archivo): **93 adquisiciones y 93 cancelaciones**, todas con `clause=running package has no owned idle override`; en cada ciclo `assignedPackage=14000B90`, `runningPackage=FF000F64/FF000F65` (el wrapper run-once de PlayIdle), `idle=00000000`, `weaponState=0`, `shield=00000000`. Cero `hold confirmed by OAR`.
- Conclusión medida: en 1.6.1170 `PlayIdle` desplaza permanentemente al paquete en ejecución con su wrapper run-once y **nunca puebla** `high->currentProcessIdle`; el predicado v26 `running||ownIdle` era por tanto **insatisfacible**, no transitorio. La suposición v26 queda falsada por medición; la iteración inicial de esta copia (re-emisión acotada del idle) se descartó por la misma evidencia: reintentar no puede satisfacer un predicado siempre falso.
- `reports/diagnosis_v25_context.json`: 134/134 adquisiciones-cancelaciones ≈35 ms — el mismo fallo subyacente sin cláusula nombrada.
- README v21: una instalación inspeccionada carecía de `AstraAsedio_WhiterunTorres.esp` y el fallo era **silencioso** en ambos registros.
- Auditoría de este árbol (binarios PE/ESP leídos, fuentes nativas y Papyrus leídas): la vía de animación del guardia es idle OAR + IK nativo; WeapType/Combat Style/Attack Data no intervienen.

## Cambios v27 (corrección de fondo + diagnóstico; ningún contrato de seguridad se relaja)

1. **Nativo — predicado de admisión corregido** (`GuardPolicy.cpp`): para un lease adquirido ya no se exige `GetRunningPackage()==B90` ni `currentProcessIdle==0x802` (el motor no puede proveer ninguno en esta ruta). Se exige paquete **asignado** B90, arma envainada y actor no interrumpido; la identidad del idle propio queda arbitrada por el árbitro más fuerte ya existente: la observación OAR en el hook de `hkbClipGenerator` (proyecto+subgrafo+ruta física exacta del clip, duración y peso), con su timeout acotado (`hold replacement not observable`) intacto. El disparo sigue exigiendo agarre fresco observado — nada de esto autoriza disparos. Antes de adquirir, el requisito `running==B90` se mantiene idéntico.
2. **Nativo — diagnóstico OAR en `install()`**: el registro distingue `OAR Animations V1={}` de `module loaded={}`, separando "OAR no instalado/cargado" de "API rechazada".
3. **Papyrus — traza de refs ausentes** (`AstraAsedioGuard.psc`): una sola por carga cuando `ResolveV23Operator()` no puede resolver B70/B71/B80/B81 → `Astra guard v27: operator refs missing; enable AstraAsedio_WhiterunTorres.esp (...)`.
4. **Papyrus — backoff tras fallo nativo**: tras drenar un `status == -2`, el pump espera **5 s** (y **30 s** desde el cuarto fallo consecutivo) antes de reintentar `BeginOperation`, con traza `Astra guard v27: backoff ...`. Además de evitar el batido de reintentos, esto da ventana a la observación OAR (cada ciclo de 1 s reenviaba `IdleForceDefaultState` y `ClearConditionStateData`, interrumpiendo cualquier clip en curso). Un fin limpio (-1) o un begin aceptado restauran el contador.
5. **Versión DLL 3.5.8** (API jugador 4 / NPC 1 sin cambios de firma): `Plugin.cpp`, `CMakeLists.txt`, `build_native.py` (recibo) y `verify_binary.py` alineados; tabla de aserciones nativas v26 actualizada a la semántica medida.

ESP, HKX, NIF, SEQ y configuración OAR: **idénticos a v26** (no editados en esta copia).

## Comprobaciones externas ejecutadas aquí

| Comprobación | Resultado |
| --- | --- |
| `tests/test_v27_guard_resilience.py` (7 contratos nuevos) | PASS |
| `tests/test_v26_guard_ai.py` y suites v24/v25 heredadas | mismos 2 fallos preexistentes y documentados (`v23PlacementVersion < 24/26` en las clases históricas); idénticos en árbol original |
| `native/tests/guard_binding_tests.py` (binding contra ESP reales y bajo NIF) | PASS |
| Compilación Papyrus (10 PEX, staging nuevo, desensamblado de control) | 0 errores, 0 warnings |
| Build nativo Release x64 + CTest (vendor pineado inmutable, SHA-256 antes/después) | ver `reports/native_build_receipt.json` |
| `native/verify_binary.py` (PE, exports, versión 0x03050080, strings NPC) | ver `reports/native_binary_checks.json` |

## Pruebas pendientes en Skyrim v27

- [ ] `AstraSight.log` muestra, al arrancar: `AstraSight 3.5.8 ...` y `OAR Animations V1=True (module loaded=True)`.
- [ ] En orden: `guard v26 acquired` → `guard v26 hold confirmed by OAR` → `guard v26 grip confirmed` → `guard real projectile` con enemigo válido. **Ya no debe aparecer** `clause=running package has no owned idle override`.
- [ ] Si aun así el hold no se confirma en ~2 s, la siguiente capa a medir es la activación del reemplazo OAR (visor/console de OAR sobre el guardia o traza de `GetCurrentReplacementAnimationInfo`); hoy estaba bloqueada por la cláusula.
- [ ] Sin `AstraAsedio_WhiterunTorres.esp`: Papyrus ya no calla — debe aparecer la traza v27 de refs ausentes.
- [ ] Con OAR desinstalado: `NPC runtime/OAR unavailable` en Papyrus y `module loaded=False` en el nativo.
- [ ] Los pendientes v26 (xEdit, muerte/stagger/descarga, guardar/cargar, atalaya y torreta del jugador) siguen en `docs/QA_v26.md`.

## Lo que v27 no afirma

Que el reemplazo OAR del clip ocurra y complete el hold/agarre/disparo **sigue sin certificar en el motor**: la corrección elimina el bloqueo medido; la evidencia de aceptación es la secuencia ordenada de líneas del registro en una sesión nueva. La persistencia de `currentProcessIdle` queda aclarada como **ausente** en esta ruta y ya no forma parte del contrato.
