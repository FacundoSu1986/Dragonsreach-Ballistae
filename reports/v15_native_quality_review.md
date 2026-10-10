# Revisión independiente de calidad nativa v15

Fecha: 2026-10-09. Alcance: `FastShot`, `FastShotRuntime`, `Core`, `Plugin`, interfaz `AstraSightNative` y pegamento de adquisición/salida de `AstraAsedioActi` y `AstraAsedioSession`. Se tomó como contrato el diseño aprobado y `reports/v15_native_spec_review.md`; se volvió a revisar la fuente final después de las dos correcciones descritas abajo.

Esta revisión sólo leyó fuentes, dependencias fijadas, binarios e informes, y ejecutó directamente los seis EXE portables existentes. La única escritura del revisor es este archivo. No recompiló ni modificó el mod, v14, vendor, runtime o MO2; no cargó la DLL ni lanzó Skyrim. El implementador realizó las correcciones y el build final.

## Dictamen

**APROBADO el alcance nativo revisado. No quedan hallazgos P1/P2 abiertos en este alcance, con los límites de evidencia indicados al final.** Los dos problemas concretos encontrados durante esta pasada se corrigieron y la fuente/build finales se verificaron de nuevo. La aprobación cubre corrección de la implementación y coherencia de sus artefactos offline; no certifica la entrega de ciudad completa ni su funcionamiento en Skyrim.

## Hallazgos encontrados y resolución comprobada

| Prioridad | Caso concreto | Resolución final |
|---|---|---|
| P2 | Con contexto válido, `capture(true)` congelaba aim antes de Fire. Si `Activate` de Fire devolvía false pero Reset funcionaba, la máquina recorría Reset/Restore sin pasar por Launch; no había thaw y la mira podía permanecer congelada hasta otro tiro o salida. | `FastShotRuntime.cpp:107` descongela la sesión al fallar preparación, usando `r.ticket.key` y comprobando que sigue el mismo ticket. Reset/Restore ya no dejan esta congelación residual. La corrección se comprobó por flujo de control; no se simuló una devolución real de `NiControllerSequence::Activate` en Skyrim. |
| P2 | La cámara podía haber adquirido/escrito escena antes de que `tick()` armara FastShot. Un End tasklet entre ambas operaciones encontraba `rootIdentity_ == 0` y reconocía quiescencia sin neutralizar esa escena; Acti luego ponía su cache a cero. También podía ocurrir si el primer apply escribía parcialmente y terminaba rechazado. | `Session::update` registra el ticket/identidad de escena antes del apply bajo el mutex de Session (`Core.cpp:98`); `invalidateScene` invalida y devuelve/consume esa identidad en la misma transacción (`:87`). Plugin pasa la raíz real (`Plugin.cpp:229`) y `requestEnd` usa la identidad adquirida aunque FastShot todavía no esté armado (`FastShotRuntime.cpp:76`). El registro sobrevive a un apply rechazado; la compensación no afecta un ticket distinto. Tres aserciones nuevas cubren End antes de armar, consumo único e identidad tras primer apply rechazado. |

La segunda corrección conserva el orden de locks EffectsBarrier → Session. No añade un callback de Session hacia EffectsBarrier ni consultas de escena desde el tasklet de End. El fence conserva al propietario hasta que la limpieza en la cola del hilo del juego termina.

## Revisión del flujo final

- **Entrada:** registro del sink en `kInputLoaded`; mappings actuales raw de teclado/ratón; gates de release por dispositivo al entrar o pausar; clicks ocupados descartados; segundo dispositivo no duplica una admisión. `ButtonEvent::IsPressed/IsDown` y el acceso a las teclas se cotejaron con CommonLib local. No hay fallback silencioso de códigos ni vía gamepad certificada.
- **Preparación y tiempos:** el hook de `PlayerCamera::Update` llama `tick()` en el hilo del juego. Fire/Reset son nativos; Release se agenda desde el reloj posterior a Activate y Reset desde el reloj posterior a su llamada de secuencia. Un frame lento no dispara varios proyectiles. El cooldown de 1 s empieza en Launch exitoso; el siguiente lanzamiento incluye preparación y cuantización de frames. No es una garantía de cadencia exacta de 1 Hz ni latencia medida del click.
- **Compromiso:** coste `SteelBolt` separado de `ShotAmmo`/`Launcher`; descuento de exactamente una unidad antes de Launch; revalidación del mismo ticket, contexto y pose congelada después de inventario. El resultado exige handle válido y resolución. Si falla Launch/cancelación posterior al descuento, solicita una sola devolución y registra el resultado. Esa compensación no es una transacción infalible del motor.
- **Contexto y vida útil:** cámara FP, jugador vivo, menús, rango del operador, snapshot finito, 3D original y nodos/secuencias se validan. Las secuencias que cruzan Deactivate/Activate se retienen; los efectos posteriores al lanzamiento vuelven a validar y retienen la escena/objetos usados. Cleanup retiene la raíz y ambas secuencias antes de Deactivate y limita restauración a la escena correspondiente a la identidad adquirida.
- **Salida:** End invalida el ticket antes de la limpieza encolada. BeginFastSight y BeginSight de compatibilidad comparten barrera. Acti/Session esperan el acuse antes de liberar controles; el wildcard del guardia rechaza propiedad activa y limpieza pendiente. Cleanup restaura Reset/virote y lleva los controles propios a identidad; Acti sólo después pone yaw/pitch a cero e invalida sus bases, evitando reconstruir la base desde un cache atrasado.
- **Papyrus:** RequestShot, TryRepeatShot, BeginShot y CommitShot salen inmediatamente con `UseSightCamera`. OnUpdate nativo lee/cachea aim y modo; no consume munición ni duplica Fire/Reset, visibilidad o sonido del tiro. La adquisición tiene plazo finito y rechazo visible, con nueva comprobación del plazo después de Begin/readiness. La espera de limpieza no tiene timeout de liberación: conserva propiedad mientras el acuse no llega. La ruta legacy permanece separada.

## Evidencia fresca final

Recibo final: `reports/native_build_receipt.json`, UTC `2026-10-09T11:29:18.188483+00:00`, SHA256 `d6b08efc2c8448540cbece1b6cb657a21436702c8004a9dd5629bfde6a587072`. **Los 27 archivos listados coinciden con sus hashes actuales**, incluidos fuente, tests y DLL.

Se ejecutaron directamente, sin regenerar logs de CTest, los EXE de `build/native/release-v15`: Core 147, v07 302, v08 86, v09 51, v10 1695 y v15 56 aserciones: **2337 aserciones, cero fallos, seis exit codes 0**. El build final del implementador también registra CTest 6/6. Estos tests ejecutan Core/FastShot/Fence; no ejecutan el adaptador CommonLib dentro del juego.

El parseo PE independiente confirma DLL entregable y compilada idénticas, SHA256 `efe94edda8c9455899a675b49f1f6521b37223c545acd2a0ef08562de4d89e5c`, 695808 bytes, AMD64, exports SKSEPlugin_Load/Query/Version, versión 3.5.0, runtime único 1.6.1170.0 y SKSE mínimo 2.2.8. API 4 se cotejó en la fuente; el PE no acredita por sí solo la ejecución de esa API.

La lectura del NIF final con el parser/medidor local confirma SHA256 `bcee401b79a3708ec16452ba23dd7e6364eb421bab310a218595232fac5d9e17`, Fire `0.20000000298023224` s y Reset `0.800000011920929` s, con 1978 offsets de tiempo registrados coherentes con sus límites. No se exportó ni reescribió el NIF.

Identidad de las fuentes finales principales:

| Archivo | SHA256 |
|---|---|
| native/include/Astra/Core.h | 8cbde6a555f8bb9950166baedfd65265783b76ef84b0eac51614433f91712272 |
| native/src/Core.cpp | 6632551962e7b9a2f7df839ba23b0083f1b273e8c76a95276c7593f93a4c421b |
| native/src/FastShotRuntime.cpp | 50123be9c3ffc3bb9e1173645a941dc484e04d6b73749576772d805687e8af14 |
| native/src/Plugin.cpp | 02ec7105e2e2ee9f06bfceb56bbf0362935d065bde997d611f68d44083035cd0 |
| native/tests/v15_tests.cpp | 759c21115d33254839190b157d48f83514f1b232accd267721cba0bb455eff97 |
| mod/scripts/source/AstraAsedioActi.psc | a23b1d2288cd85826b25f67e96c632f61b57fd7772daf37751ea6c76acbba856 |
| mod/scripts/source/AstraAsedioSession.psc | b762659b8b339eb99080627371f124aa07acb1fe98e861075c47cf9a51e06d27 |

Se excluyeron como evidencia actual los informes heredados `native_artifacts_verified.json` (cinco EXE/2281 aserciones y hash de otra DLL), `assets_verified.json` (otro hash de ballesta y tiempos 0.3/1.2), y portable-v15 anterior. Los resultados frescos de esta sección y el recibo final identifican los artefactos revisados. La higiene/etiquetado de informes históricos en los ZIP pertenece a la verificación de entrega.

## Límites

Las operaciones nuevas de inventario, Launch, animación/audio están fuera del mutex Session, bajo EffectsBarrier. La cámara heredada conserva UpdateWorldData/SetRotationX/Z dentro de `Session::update/visitSnapshot`; la revisión no afirma ausencia de toda reentrancia posible o compatibilidad con hooks externos. La vida útil y cancelación se revisaron en fuente y contra CommonLibSSE-NG local fijada a `b93280e832f263dbef44e44cbe2936622a02f91a`, no mediante callbacks reales del motor.

Requieren Skyrim: latencia input→Launch/imagen, dirección/origen/daño/autoría/perks, Fire/Reset y audio, remappings y dispositivos reales, menús/cámara/muerte/carga, limpieza con hooks externos, salida/reentrada neutral y toma/devolución de puestos. Esta revisión no verifica PEX finales, ESP/VMAD, geometría, Havok, NAVM ni rutas AI. No se ejecutó ningún caso de motor.
