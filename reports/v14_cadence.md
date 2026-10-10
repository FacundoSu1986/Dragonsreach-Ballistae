# Cierre de integración v14

La integración final ya está verificada: 359 pruebas y 162 subtests, VMAD temporal nuevo y cinco PSC/PEX/desensamblados Bethesda coherentes. `verification_v14.json` describe la entrega; `v14_cadence_verification_initial.json` conserva el recibo de la etapa inicial. El texto de abajo describe esa etapa histórica (incluidas sus comprobaciones entonces pendientes). Después se agregaron los sectores medidos YawCenter/YawHalfSector.

# Cadencia v14

Cadencia implementada en fuente y NIF. El agente principal integra VMAD final
y compila los cinco PEX; este trabajo no escribió PEX ni modificó ESP.

| Valor | Jugador | Guardia |
|---|---:|---:|
| FireSeconds | 0.2 s | 0.2 s |
| ReleaseSeconds | 1/15 s | 1/15 s |
| ResetSeconds | 0.8 s | 0.8 s |
| CycleSeconds / CadenceSeconds | 1 s nominal | >= 2.5 s entre lanzamientos |

La fuente Papyrus representa 1/15 como `0.0666667`, dentro de la precisión
de float. El jugador agrega un tick de preparación y latencia de Papyrus/motor.
El fixture midió 1.05 s entre lanzamientos nominales; no es una garantía de
frecuencia en juego. Los ciclos personalizados válidos mayores al mínimo
se respetan en continuo.

`timingRevision=14` migra una sola vez valores v13 guardados, con rangos que
incluyen sus representaciones float. OnLoad invalida la sesión del jugador
antes de migrar; BeginRecovery invalida generation/token del NPC antes de
migrar. Un nuevo BeginShot del jugador también normaliza antes de preparar
el ciclo. Se conservan valores personalizados finitos compatibles. Luego
de la primera migración, incluso valores personalizados iguales a los viejos
defaults se conservan. En la primera migración no existe evidencia para
distinguir un default guardado de una personalización numéricamente idéntica.

Cotas: Fire [0.2, 2], Release [aproximadamente 1/15, 1] y no mayor que Fire,
Reset [0.8, 5], Cycle [1, 7] y no menor que Fire+Reset, Cadence [2.5, 60].
Valores inválidos se normalizan a los nuevos defaults; una Cycle insuficiente
se eleva a Fire+Reset sin borrar Fire/Reset personalizados válidos.

El NPC usa la misma Cadence validada para la espera inicial de recuperación,
BeginShot y CommitShot. Conserva el reloj posterior a Launcher.Fire, tokens,
mutex pinBusy/sceneBusy y compensación de efectos nativos pendientes. El
fixture midió 2.6 s entre disparos nominales. Con preflight 2 s y Fire 3 s,
midió 5.6 s entre lanzamientos y 2.6 s desde el retorno de Fire hasta el
lanzamiento siguiente. No agregó bucles de espera ni updates mientras busy.

## Pruebas y alcance

TDD rojo: 26 fallas y 11 éxitos en 37 pruebas nuevas, antes de implementar.
Verificación verde fresca: 282 pruebas y 122 subtests exitosos; incluye las
69 regresiones NPC y 37 pruebas nuevas de cadencia. Se excluyeron solamente
los dos contratos de integración finales que corresponden al agente
principal: VMAD/config y hash de fuente/compilación Bethesda.

Las adaptaciones conservan la intención de las tres pruebas de cadencia
NPC anteriores: sus mínimos de 4 s ahora son 2.5 s y se comprueban los
lanzamientos reales del fixture. Continúan todas las pruebas de unload/load,
hide tardío, matrices tardías, Fire tardío, pin pendiente, reloj, preflight,
target/LOS, desplazamiento y seguridad del jugador.

Estos fixtures evalúan las ramas reales de PSC con interrupciones nativas
explícitas. No ejecutan la VM de Papyrus ni demuestran entrega de eventos,
migración persistente, animación NPC o daño en el motor. Esas verificaciones
siguen en la prueba de juego acordada.

## NIF e integridad

`scripts/retime_v14.py` mide primero versión 20.2.0.7, user 12, BS 100 y
secuencias v13 Fire 0.3000000119 / Reset 1.2000000477. Luego reutiliza
`retime_v07.retime` desde el NIF original v13 y retima Fire a 0.2 / Reset a 0.8.

Registró 1.978 offsets float de tiempo. Cambiaron 6.415 bytes dentro de ellos;
al restaurar esos offsets, el binario coincide byte por byte con v13. Se
conserva longitud, geometría, pose, shaders y colisión. No hubo exportación.

- NIF antes: `e6fcf2a64cfeca82f186bc7f4b76ce4f47a4371577cb6e037bf8ba094fc483b2`
- NIF después: `bcee401b79a3708ec16452ba23dd7e6364eb421bab310a218595232fac5d9e17`
- DLL sin cambios: `7cf962b1b16c14033ae62e36261b75a26a1212d4f7e0c692d24131e364cffb2d`
- Torre sin cambios: `1dc1ca22e03357cb292f6a122cd504914885cc540b21990dccf31c7b5d0a2679`

Dos recorridos SHA-256 completos comprobaron que los 1.000 archivos de v13
siguen idénticos. Los receipts detallados están en
`v14_cadence_baseline.json`, `v14_cadence_retime.json`,
`v14_cadence_verification.json` y `v14_cadence_tests.xml`.

Sólo se editaron cuatro campos de tiempo existentes de config.json,
AstraAsedioActi.psc, AstraAsedioGuard.psc, el NIF ballesta retimado, el nuevo
script de retiming, las pruebas correspondientes y estos reports. Native
API 3 y AstraSight 3.4 permanecen intactos. No se tocó runtime ni perfil.
