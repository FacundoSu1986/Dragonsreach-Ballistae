# Astra Asedio v28

Esta versión corrige una espera infinita de v27 y conecta la comprobación de manos con el controlador principal de la estación. En tu prueba v27 OAR reconocía la animación, pero nunca se confirmaba el agarre y el apuntado permanecía bloqueado. Tras fallar, Papyrus repetía su espera de cinco segundos sin volver a intentar la operación.

## Instalación y primera prueba

Cierra Skyrim, instala `AstraAsedio_QA_v28_Unificado_MO2.zip` como mod nuevo en MO2 y desactiva el paquete Astra anterior. Activa estos cuatro plugins, conservando su orden relativo:

1. AstraAsedio.esp
2. AstraAsedio_WhiterunTorres.esp
3. AstraAsedio_Atalaya.esp
4. AstraAsedio_GuardAnim.esp

Requiere Skyrim SE 1.6.1170, SKSE 2.2.8, Address Library correspondiente y OAR con API Animations V1. Incluye AstraSight **3.5.9**, API jugador 4 / NPC 1. No requiere regenerar behaviors.

Carga una copia de tu partida y acércate por delante de los puestos. Primero comprueba que ambos operadores sostienen los mandos incluso sin un objetivo; después recorre su sector frontal. Los guardias locales y habitantes no hostiles se ignoran para el apuntado visual; jugador y visitantes pueden recibir seguimiento. El jugador, aliados y neutrales permanecen protegidos frente al disparo. Para probar un virote utiliza un enemigo NPC válido.

El giro sigue siendo horizontal, −60° a +60°, con elevación 0°, altura del operador fija y radio visual 2100 unidades (unos 30 metros). Solo se dispara cuando un enemigo resulta alcanzable mediante la trayectoria validada, hasta 6000 unidades. El virote no persigue al enemigo durante el vuelo. Las armas personales quedan guardadas y el escudo permanece en el inventario. La atalaya y torreta del jugador conservan sus recursos altos y cámara.

## Cambios

- El controlador principal comprueba OAR, pies y manos antes de permitir apuntar o disparar. La rutina de actualización del NPC solo aporta contadores de diagnóstico; ya no es la única vía para habilitar el agarre.
- La espera tras un fallo se consume una sola vez y permite reintentar. Los fallos consecutivos se reinician cuando la operación alcanza un estado saludable, en vez de reiniciarse al aceptar una solicitud todavía pendiente.
- Una muestra de pose inválida durante más de 1,5 s cancela la operación y activa el reintento acotado. Las manos demasiado alejadas, geometría inválida y obstrucciones siguen impidiendo disparar.

La migración de colocación sigue siendo 26: no hace falta volver a mover los operadores de una partida v27. Se mantienen los campos guardados y se añade una bandera de espera. Los cuatro ESP, NIF, HKX y configuración OAR son idénticos a v27.

## Registro para comprobar el resultado

`AstraSight.log` debe indicar `AstraSight 3.5.9`. Las trazas heredadas de adquisición y OAR todavía llevan `guard v26`; eso no identifica por sí solo la versión de la DLL.

- `guard v28 pose pump`: se ejecutó la comprobación principal; muestra clip, fase, muestra OAR, llamadas de NPC por hilo y distancia de las manos a los mandos.
- `guard v28 grip confirmed on main pump`: manos verificadas por el controlador principal.
- `guard real projectile`: virote real lanzado con enemigo válido.
- `guard cancel ... reason=...`: condición que impidió continuar.

La telemetría de postura se limita a una línea cada dos segundos por puesto. Si el motor sobrescribe el ajuste entre fotogramas, el error previo a la siguiente corrección ayudará a localizarlo.

La DLL, los scripts y el ZIP se validaron fuera del juego. **La pose visible, su persistencia, el giro y el disparo v28 todavía requieren prueba en Skyrim.** Ver `QA_v28.md` para el alcance exacto. El `.blend` y el preview anteriores siguen disponibles por separado y no representan una captura de la IA v28 en juego.

Rutas vigentes: `prepare_guard_scripts_v28.py`, `compile_papyrus.py`, `build_native.py`, `verify_v28_release.py`, `package_v28.py` y `verify_zip_v28.py`. No ejecutar constructores históricos para generar esta entrega. Manifiesto SHA-256 y licencias incluidos.
