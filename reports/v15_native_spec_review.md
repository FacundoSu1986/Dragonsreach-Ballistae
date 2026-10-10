# Revisión independiente de especificación nativa v15

Fecha: 2026-10-09. Revisión de sólo lectura de FastShot, FastShotRuntime, Plugin/Core, AstraSightNative, AstraAsedioActi y AstraAsedioSession; consulta del handoff de AstraAsedioGuard y del diseño aprobado. Únicas escrituras del revisor: los tres informes SPEC autorizados. No se modificaron mod, runtime, MO2 ni vendor v11; no se lanzó Skyrim. Esta versión incluye la recompilación final y el receipt regenerado tras actualizar la documentación nativa, con código/DLL idénticos.

## Dictamen

**APROBADO el alcance nativo revisado, con los límites de evidencia indicados abajo. No quedan hallazgos P1/P2 abiertos en ese alcance tras las correcciones de esta pasada.** Esta aprobación no certifica el complemento de ciudad completo, los PEX finales, geometría/Havok/NAVM, latencia ni comportamiento real del motor.

El lanzamiento utiliza input nativo mapeado, Fire y un intervalo nominal de 1/15 s antes de Release, procesados desde el hook de cámara del hilo del juego. No espera fases de disparo de Papyrus. El cooldown se inicia desde el lanzamiento exitoso; por tanto el intervalo entre lanzamientos en continuo incluye además la preparación del tiro siguiente y la cuantización de fotogramas. No se presenta CycleSeconds=1 como latencia del clic ni como cadencia exacta medida.

## Contratos comprobados

- **Entrada y contexto:** registro en kInputLoaded; mappings actuales de teclado/ratón con códigos raw de cada dispositivo, sin fallback silencioso. Estado físico y release gates por dispositivo en entrada/menús; clics ocupados se descartan, dos dispositivos no admiten dos tiros del mismo ciclo. La vía gamepad permanece fuera del alcance. Admisión y compromiso requieren ticket actual, !suspended, FP, jugador vivo, menú permitido, 3D original, nodos/secuencias y operador en rango.
- **Munición y resultado:** SteelBolt paga el coste; ShotAmmo/Launcher alimentan LaunchData. Se verifica una disminución de exactamente un coste antes de Launch. El éxito exige ProjectileHandle no vacío y resolución del handle, no el puntero que devuelve Projectile::Launch. Un fracaso de lanzamiento o cancelación después de RemoveItem solicita una única compensación y registra su resultado. La compensación no se describe como rollback infalible del motor.
- **Cancelación reentrante:** después de inventario se revalida ticket/contexto/pose congelada inmediatamente antes de Launch. Después de Launch se revalida contexto antes de ocultar el virote y antes de reproducir audio. Las secuencias y objetos usados después de llamadas de motor se retienen con NiPointer.
- **Propiedad y limpieza:** EffectsBarrier serializa los efectos; EffectsFence conserva el propietario hasta que la tarea de limpieza termina. BeginFastSight y BeginSight de compatibilidad comparten la barrera. End invalida antes de encolar limpieza, y el retorno/IsEffectsQuiescent no autorizan la liberación mientras quedan efectos. Acti y Session esperan el acuse antes de liberar controles; el wildcard de guardia rechaza tanto propiedad activa como limpieza pendiente.
- **Salida y siguiente entrada:** cleanup retiene raíz y ambas secuencias originales antes del primer Deactivate, restaura Reset/virote y lleva los dos controles propios a identidad. Acti sólo después del acuse pone yaw/pitch a cero e invalida las bases capturadas. La puntería vuelve a neutral al salir; no se mezcla un ángulo Papyrus atrasado con la última matriz nativa al volver a entrar.
- **Entrada todavía sin armar:** Session registra la identidad adquirida bajo el mismo mutex que la primera escritura de pose. invalidateScene consume esa identidad exactamente una vez y cancela el ticket en esa transacción; requestEnd usa esa raíz incluso si el primer apply falló o FastShot todavía no se armó. Una preparación Fire fallida también descongela el aim cuando el mismo ticket permanece actual.
- **Temporización:** Release usa el reloj nativo después de Activate de Fire; Reset calcula su restauración desde el reloj posterior a la llamada de secuencia. No hay cola de clicks ni ráfaga de compensación por un frame lento; el adaptador limita Launch a un proyectil por frame.
- **Papyrus/legacy:** RequestShot, TryRepeatShot, BeginShot y CommitShot salen de inmediato en modo nativo; OnUpdate nativo sólo lee/cachea aim/modo. Fire/Reset, virote, inventario y sonido del ciclo permanecen nativos. La ruta legacy y el ciclo del guardia de 2,5 s permanecen separados.
- **Límites:** AimLimits se valida y aplica por sesión antes de escribir escena. El valor predeterminado conserva yaw 360° y pitch −20..80°; el sector de ciudad se pasa como configuración de esa sesión, sin cambiar globalmente núcleo/Atalaya. La asignación VMAD final de los puestos se verifica en la revisión de integración de ciudad.

## Hallazgos de esta pasada, corregidos

| Prioridad | Riesgo encontrado | Resolución revisada |
|---|---|---|
| P1 | RemoveItem podía invalidar la sesión y aun así ejecutar Launch con el snapshot anterior. | Revalidación posterior a inventario en FastShotRuntime.cpp:119, cancelación/compensación y una aserción nueva de cancelación reentrante. |
| P1 | Launch/Deactivate podían dejar 3D o secuencias descargados/reemplazados antes de efectos posteriores. | NiPointers, revalidación por ticket/contexto y captura de ambas secuencias antes de efectos en FastShotRuntime.cpp:51, :58 y :128. |
| P1 | Salir entre muestras PSC podía dejar aim real distinto del cache; la nueva adquisición quitaba un ángulo incorrecto al calcular la base. | Pose neutral nativa y cache/bases PSC restablecidos sólo después del acuse en AstraAsedioActi.psc:1874. |
| P2 | BeginSight de compatibilidad podía adelantar limpieza pendiente porque llamaba Session::begin directamente. | beginLegacy bajo la misma barrera/fence; Plugin.cpp:287 y FastShotRuntime.cpp:25. |
| P2 | Restore de Reset contaba desde antes de Activate y podía acortar la recarga ante una llamada lenta. | shots_.reset(clockNow()) después de sequence, FastShotRuntime.cpp:140. |
| P2 | Una salida entre la primera escritura de escena y el armado de input podía omitir la limpieza por no tener rootIdentity_. | Identidad conservada junto con la adquisición en Session::update; invalidateScene la consume atómicamente. Tres aserciones nuevas cubren salida antes del armado, consumo único y primer apply rechazado. |
| P2 | Fallar Fire después de capture podía dejar la puntería congelada. | El retorno fallido descongela el ticket todavía actual en FastShotRuntime::tick. |

## Verificación fresca

Se ejecutaron directamente los seis ejecutables finales de `build/native/release-v15`, sin crear nuevos registros de CTest: Core 147, v07 302, v08 86, v09 51, v10 1695 y v15 56 aserciones; **2337 aserciones, cero fallos**, todos con exit code 0. El registro de build del implementador también registra CTest 6/6. El ejecutable anterior de portable-v15 era obsoleto y fallaba cinco comprobaciones de fence: no se usa como evidencia del resultado final.

Los 27 archivos incluidos en el receipt de build coinciden con sus hashes actuales. AstraAsedioSession.psc, revisado aparte, tiene SHA256 `b762659b8b339eb99080627371f124aa07acb1fe98e861075c47cf9a51e06d27`.

Un parseo PE independiente de sólo lectura confirma que la DLL entregable y la recién compilada tienen el mismo SHA256 `efe94edda8c9455899a675b49f1f6521b37223c545acd2a0ef08562de4d89e5c`, 695808 bytes, AMD64, exports SKSEPlugin_Load/Query/Version, versión 3.5.0, runtime único 1.6.1170.0 y SKSE mínimo 2.2.8. El informe native_binary_checks actualizado coincide con ese resultado. La DLL no se cargó para estas comprobaciones.

Identidad de las fuentes principales de este dictamen:

| Archivo | SHA256 |
|---|---|
| native/src/FastShotRuntime.cpp | 50123be9c3ffc3bb9e1173645a941dc484e04d6b73749576772d805687e8af14 |
| native/src/FastShot.cpp | 1932fc884c418cb3bcdc64ef6b589061a947d628d31fb05e0f6e95c37584ad79 |
| native/src/Plugin.cpp | 02ec7105e2e2ee9f06bfceb56bbf0362935d065bde997d611f68d44083035cd0 |
| native/src/Core.cpp | 6632551962e7b9a2f7df839ba23b0083f1b273e8c76a95276c7593f93a4c421b |
| native/include/Astra/Core.h | 8cbde6a555f8bb9950166baedfd65265783b76ef84b0eac51614433f91712272 |
| native/tests/v15_tests.cpp | 759c21115d33254839190b157d48f83514f1b232accd267721cba0bb455eff97 |
| mod/scripts/source/AstraAsedioActi.psc | a23b1d2288cd85826b25f67e96c632f61b57fd7772daf37751ea6c76acbba856 |
| mod/scripts/source/AstraSightNative.psc | 6563578904e6f1e1c88080f9fabcb7166f1685d413dd4972e85fb588fa11cb87 |
| mod/scripts/source/AstraAsedioSession.psc | b762659b8b339eb99080627371f124aa07acb1fe98e861075c47cf9a51e06d27 |
| reports/native_build_receipt.json | 927a1f65df77d6d67ea90da167dd22cb874666fb31098740169db65002152d1b |

## Límites de la aprobación

Inventario, Projectile::Launch, NiControllerSequence y audio nuevos se ejecutan fuera del mutex Session, bajo EffectsBarrier. El orden directo observado es EffectsBarrier → Session; no se encontró un camino directo inverso en el módulo nuevo. El controlador de cámara heredado conserva callbacks de transform-only UpdateWorldData y SetRotationX/Z dentro de sus transacciones Session::update/visitSnapshot para serializar matrices y snapshots. Esta aprobación no afirma que **todas** las llamadas del motor del plugin están fuera de Session ni que las pruebas portables acreditan toda reentrancia posible de los hooks de Skyrim.

La fuente primaria consultada fue CommonLibSSE-NG local fijada a b93280e832f263dbef44e44cbe2936622a02f91a bajo vendor v11, especialmente Projectile::LaunchData/Launch, NiControllerSequence, TESObjectREFR::GetSequence y NiMatrix3. La API confirma useOrigin=true, autoAim=false, arma/ammo explícitas y el contrato de handles; no confirma daño, perks, autoría/crimen o sincronización visual efectiva.

Siguen requiriendo prueba real: latencia input-to-Launch e imagen, origen/dirección/daño/autoría del proyectil, Fire/Reset y audio, menús/cambios de cámara/carga/muerte, quiescencia con hooks externos, salida/reentrada neutral y la toma/devolución completa de ambos puestos. Los fixtures y la DLL compilada no sustituyen esa prueba.
