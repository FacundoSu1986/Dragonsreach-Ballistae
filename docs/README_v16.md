# Astra Asedio QA v16

V16 corrige la mira de v15 que terminaba con CAMERA_ENTRY_FAILED y las ballestas de ciudad que permanecían sobre el piso anterior en una partida guardada. Las extensiones que confirmó Facu se conservan sin cambios.

El disparo nativo se actualiza desde FirstPersonState, la llamada que aparece ejecutándose en los registros reales. Antes dependía exclusivamente de PlayerCamera::Update, sin ejecuciones registradas; por eso no llegaba a armarse aunque la cámara de apuntado funcionara. La DLL nueva es **AstraSight 3.5.1/API4**. El marcador de lanzamiento sigue siendo 1/15 s después de iniciar Fire, con recarga nominal mínima de 1 s y guardias de 2,5 s. Falta medir la latencia con la DLL corregida dentro de Skyrim.

El controlador de ciudad ahora verifica la posición al cargar o preparar el puesto para el jugador. Si conserva una posición antigua, mueve la ballesta y sus dos marcadores propios a la plataforma existente, luego coloca al guardia en el puesto o en espera. Lo hace con el control del guardia suspendido y sin propietario/limpieza nativa. Una operación cancelada debe terminar antes de que otro dueño pueda entrar. Los IDs y ESP se preservan; no se mueven referencias vanilla ni estaciones personalizadas.

## Instalación

1. Cerrar Skyrim. Conservar v15 para volver atrás.
2. Instalar **AstraAsedio_QA_v16_MO2.zip** y **AstraAsedio_WhiterunTorres_QA_v16_MO2.zip** en MO2, desactivando sus versiones anteriores. Deben ganar la DLL y los seis scripts nuevos del núcleo.
3. Mantener activos AstraAsedio.esp y AstraAsedio_WhiterunTorres.esp, con ciudad después del núcleo. AstraAsedio_Atalaya.esp es opcional. Dejar desactivado el antiguo AstraAsedio_Whiterun.esp.
4. Probar primero con una copia de la partida de pruebas de v15. Salir de la mira antes de guardar y cargar esa copia con v16. Al cargar la celda, el guardia repara la colocación; también se verifica antes de ceder el puesto al jugador. No hace falta borrar referencias con la consola ni limpiar la partida.

Esta reparación de posición está implementada y probada con fuentes PSC y efectos simulados; no se garantiza toda migración de scripts de v13/v14 ni una partida habitual. Si la partida de pruebas conserva un estado suspendido que no termina, usar una partida de prueba nueva para comparar.

Requisitos: Skyrim SE 1.6.1170, SKSE64 2.2.8 mínimo y Address Library del perfil que ya funcionaba. Son ESP normales; no compactar IDs. La preparación de v16 no modificó MO2, runtime ni partidas.

## Puestos y uso

| Puesto | X ballesta | Y ballesta | Z ballesta |
|---|---:|---:|---:|
| Este | 17801,740 | −8824,610 | −3544,014 |
| Oeste | 15225,560 | −8726,520 | −4128,014 |

Este: `cow Tamriel 4 -3`. Oeste: `cow Tamriel 3 -3`. Las ballestas deben quedar en los voladizos exteriores, con giro de referencia 0°. El guardia propio se retira a su punto de espera al activar la manivela.

Ratón: apuntar; Ataque: disparar; Sprint: Individual/Continuo; Activar/E: salir. Soltar Ataque después de entrar y hacer un clic nuevo. Se respetan los controles de teclado/ratón; no se agregó entrada de mando. Laboratorio: `coc AstraAsedioTest`; Atalaya: `cow Tamriel 1 -4`.

Se conservan apuntado −20° a +80°, giro completo de núcleo/Atalaya y sector frontal ±60° en ciudad. También se conserva la torre baja, la escalera y los escudos de la Atalaya. Las plataformas tienen Havok y no añaden NAVM; los NPC propios se colocan directamente. El complemento no modifica el navmesh ni los destinos de patrulla originales. Los parches para otros mods de ciudad siguen pendientes.

Compilación y verificación fuera del motor: seis scripts, DLL real nueva, 304 pruebas con 107 subtests y 2.337 aserciones C++. La recolocación real, el disparo, el guardado/carga y los accesos requieren confirmación en Skyrim; ver PRUEBAS_EN_JUEGO.md.
