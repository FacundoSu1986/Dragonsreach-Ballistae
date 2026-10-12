# Astra Asedio v24 — operadores exclusivos de ballesta

Corrección de IA sobre la v23. Los operadores Este `000B71` y Oeste `000B81` reciben un paquete propio para permanecer en sus ballestas bajas con las armas personales guardadas. No se borran sus inventarios ni sus armaduras. El controlador exige que ese paquete esté activo y que la postura esté confirmada por OAR antes de autorizar un disparo.

## Instalación en MO2

Instala `AstraAsedio_QA_v24_Unificado_MO2.zip` como un mod nuevo y desactiva el paquete Astra v23 o v22 anterior para evitar que sobrescriba sus archivos. Activa los cuatro plugins en este orden relativo:

1. `AstraAsedio.esp`
2. `AstraAsedio_WhiterunTorres.esp`
3. `AstraAsedio_Atalaya.esp`
4. `AstraAsedio_GuardAnim.esp`

Requiere Skyrim SE **1.6.1170**, SKSE64 **2.2.8**, Address Library correspondiente y OAR con API de animaciones V1. La instalación examinada tiene OAR 3.2.1. El ZIP contiene AstraSight **3.5.5**, API jugador 4 y NPC 1; no incluye esos requisitos externos. Los clips reemplazan idles existentes y no necesitan generar un behavior nuevo.

Cierra Skyrim antes de cambiar el mod. Para la primera prueba, carga una copia de tu partida anterior. Al cargar se refrescan los dos aliases, se cancela cualquier propietario anterior y, una vez completada su recuperación, se recolocan los operadores y marcadores y se limpia su pose antigua. Las variables persistidas conservan sus nombres v23 y la migración se incrementa a 24. Los BaseID `FF…` de esa partida no se utilizan para identificar operadores.

## Comportamiento

Solo esos dos artilleros reciben la IA del puesto. Las demás guardias conservan su comportamiento normal. Si el controlador no puede validar animación, soporte físico o trayectoria, la ballesta no dispara y el paquete del puesto sigue asignado.

La ballesta sigue al objetivo **antes del disparo** y lanza un **virote normal**, con gravedad, sin cambiar de dirección para perseguirlo. Su giro queda en −60° a +60° y la elevación en 0°. Se mantiene el agarre bajo y la animación aprobada: operar 2 s, disparar 1 s, pasos laterales 0,8 s. No se añadió recarga corporal.

Jugador y transeúntes visibles pueden recibir el apuntado visual dentro de 2100 unidades; un enemigo en combate tiene prioridad. El jugador permanece protegido incluso si agrede a un vendedor. Esa agresión sirve para comprobar que los artilleros no sacan sus arcos, pero **no debe provocar un disparo de la ballesta contra el jugador**. Usa un enemigo NPC válido para probar el disparo, con trayectoria horizontal alcanzable, visible y despejada, hasta 6000 unidades. Un aliado, neutral o jugador en la trayectoria o zona de impacto cancela el tiro. La protección de aliados usa `IsPlayerTeammate` y la hostilidad observada por el motor.

El operador gira alrededor del eje con desplazamiento local `(0,151)`. Su altura se captura al adquirir el puesto y se mantiene durante la órbita. El pequeño margen del controlador físico (hasta ocho unidades respecto a la colocación nominal) se valida contra el suelo medido; no produce seguimiento vertical del arma. El virote se libera aproximadamente a 0,067 s del gesto, como máximo uno por ciclo.

La atalaya y la torreta principal conservan la ballesta alta, su cámara y la API del jugador. Los recursos altos y las propiedades del jugador coinciden con la v22. No se modifica el script vanilla de la ballista enana.

## Estado y diagnóstico

Esta es una entrega QA compilada y comprobada **fuera del juego**. La prueba en Skyrim de la v23 confirmó el fallo de adquisición y el uso de arcos personales. Todavía no se ha completado la prueba de esta corrección v24 en Skyrim. La vista previa y el `.blend` anteriores se conservan porque la animación fue aprobada; no certifican el funcionamiento de la IA en el juego.

Los registros nuevos en `AstraSight.log` identifican:

- `AstraSight 3.5.5`: DLL nueva cargada.
- `guard v24 acquired`: paquete, altura y soporte aceptados; idle solicitado.
- `guard v24 hold confirmed by OAR`: reproducción real del clip observada.
- `guard real projectile`: lanzamiento real, objetivo y fase.
- `guard v24 reject`: cláusula concreta rechazada, posición, escala y paquete actual. Los fallos de soporte incluyen filtro, referencia golpeada, normal y altura del suelo.

Papyrus registra `Astra guard v24 migrated` y los cambios de estado. Guarda ambos logs si aparece un rechazo. No se ha ejecutado xEdit Check for Errors ni una prueba jugable de cámara, OAR o disparo en esta v24.

## Fuentes y reconstrucción

Rutas vigentes: `build_guard_bridge_v24.py`, `prepare_guard_scripts_v24.py`, `compile_papyrus.py`, `build_native.py`, `verify_v24_release.py` y `package_v24.py`. La ruta v24 reutiliza de forma explícita la construcción v23 desde la base congelada `46bfbf7` y aplica después la IA privada; no ejecuta constructores históricos v22. El ZIP v23 entregado se conserva por separado.

El manifiesto SHA-256 identifica todos los archivos del paquete y el `.blend` y MP4 sin cambios. Los detalles están en `QA_v24.md`. La asignación de paquetes respeta la estructura [ALPC de xEdit](https://github.com/TES5Edit/TES5Edit/blob/dev-4.1.5/Core/wbDefinitionsTES5.pas); los flags siguen la [definición de TESPackage de CommonLib](https://github.com/CharmedBaryon/CommonLibSSE-NG/blob/main/include/RE/T/TESPackage.h). Las licencias nativas se incluyen en `Docs/AstraAsedio/Licenses`.
