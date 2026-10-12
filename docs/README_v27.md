# Astra Asedio v27 — corrección del guardia operador

Copia de trabajo derivada de v26. Mantiene la IA asignada al puesto, el agarre canónico y toda la disciplina fail-closed; corrige el bloqueo medido en la sesión v26 y mejora el diagnóstico.

## Qué corrige respecto a lo observado

- La sesión v26 (17:12, 93 ciclos medidos) confirmó la causa raíz: tras adquirir, el paquete en ejecución pasa a ser el wrapper run-once de `PlayIdle` y `currentProcessIdle` queda nulo siempre, así que la cláusula v26 `running==B90 || currentProcessIdle==0x802` era imposible de cumplir. v27 deja de exigirla tras la adquisición; la identidad del idle propio la arbitra la observación OAR del clip (proyecto, submod y ruta exactos), y sin observación canónica el lease sigue cancelándose acotadamente como antes.
- La incidencia v21 (sin `AstraAsedio_WhiterunTorres.esp`) era silenciosa; v27 la traza una vez por carga.
- Los reintentos de adquisición ya no se producen cada segundo tras un fallo nativo: esperan 5 s, y 30 s desde el cuarto consecutivo (además, cada reintento reenviaba `IdleForceDefaultState` y pisaba la observación OAR en curso).
- El registro nativo distingue "OAR ausente" de "API rechazada".

## Instalación

Cierra Skyrim. Instala el paquete como mod nuevo en MO2 y desactiva el Astra anterior. Activa los cuatro plugins en este orden relativo:

1. `AstraAsedio.esp`
2. `AstraAsedio_WhiterunTorres.esp`
3. `AstraAsedio_Atalaya.esp`
4. `AstraAsedio_GuardAnim.esp`

Requiere Skyrim SE **1.6.1170**, SKSE64 **2.2.8**, Address Library correspondiente y OAR con API Animations V1. Incluye AstraSight **3.5.8**, API jugador 4 y NPC 1. No hace falta generar un behavior nuevo para estos idles.

## Operación y registro

Sin cambios respecto a v26: operadores con arma guardada, escudo desequipado y conservado en inventario, sector ±60°, elevación 0°, radio visual 2100, prioridad a enemigos en combate alcanzables.

En `AstraSight.log` deben aparecer, en orden:

- `AstraSight 3.5.8`: DLL cargada.
- `OAR Animations V1=True (module loaded=True)`: puente OAR concedido.
- `guard v26 acquired`: control adquirido y hold solicitado.
- `guard v26 hold confirmed by OAR`: clip real observado.
- `guard v26 grip confirmed`: agarre confirmado sobre el clip canónico.
- `guard real projectile`: lanzamiento real, únicamente con enemigo válido.

La línea `clause=running package has no owned idle override` **ya no debe aparecer**; si aparece `assigned package / weapon-state contract broken`, el paquete asignado o el arma envainada perdió su contrato.

Líneas nuevas de diagnóstico (solo aparecen cuando algo falla):

- `Astra guard v27: operator refs missing ...`: falta `AstraAsedio_WhiterunTorres.esp` (Papyrus.0.log).
- `Astra guard v27: backoff Ns after M faulted acquisition(s) ...`: reintentos espaciados tras fallo nativo; la cláusula primera queda en el contexto/rechazo del propio registro.
- `OAR Animations V1=False (module loaded=False)`: OAR no está cargado por SKSE.

## Estado

No probado en Skyrim. Recursos ESP/HKX/NIF/OAR idénticos a v26; los cambios son DLL 3.5.8, Papyrus del controlador y esta documentación. La lista de aceptación en juego está en `QA_v27.md`; lo heredado permanece en `QA_v26.md`.
