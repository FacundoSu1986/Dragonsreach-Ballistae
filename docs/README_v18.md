# Astra Asedio QA v18

Versión de prueba para el virote que cae al salir y las estaciones de Whiterun que recargan y parpadean sin entrar a la mira. DLL **AstraSight 3.5.3/API4**. La instalación examinada coincidía con v17; reinstalar esa misma versión no resolvía estos fallos.

El registro de v17 mostró que, después de asignar 5.400 unidades/s, el motor recalculaba 756 unidades/s. V18 normaliza el multiplicador del proyectil recién creado, además de asignar su velocidad inicial en la dirección del cañón. Usa la velocidad del PROJ de la munición, sin cambiar el daño, la gravedad ni la atribución al jugador. Registra muestras de vuelo a partir de 50, 250 y 500 ms.

En Whiterun se elimina la recolocación de la ballesta y sus marcadores durante la carga y la cesión al jugador. Las referencias B70/B80 ya están colocadas en los voladizos desde el ESP. Mover la propia ballesta podía descargar su modelo e invalidar la entrada. El registro real mostró cancelaciones a los dos segundos, pero no identificó qué operación provocó la descarga; v18 registra también OnLoad, OnUnload y OnCellDetach. El guardia sigue moviéndose a su puesto de espera al ceder el control.

## Instalación

1. Cerrar Skyrim completamente; la DLL requiere reinicio.
2. Instalar **AstraAsedio_QA_v18_MO2.zip** y **AstraAsedio_WhiterunTorres_QA_v18_MO2.zip**, desactivando los paquetes anteriores. AstraSight.dll y los seis PEX del núcleo deben ganar los conflictos en MO2.
3. Activar AstraAsedio.esp y AstraAsedio_WhiterunTorres.esp, ciudad después del núcleo. Atalaya es opcional. Mantener desactivado el antiguo AstraAsedio_Whiterun.esp.
4. Probar con una copia de la partida, guardada fuera de la mira. Conservar la original para volver a v17.

Durante la preparación no se modificaron MO2, el runtime ni partidas. Requisitos: Skyrim SE 1.6.1170, SKSE64 2.2.8 mínimo y Address Library. No compactar los IDs.

## Prueba principal

En ambas torres de Whiterun, pulsar E una vez desde la manivela. El guardia debe retirarse y debe entrar la cámara de mira sin que desaparezca la ballesta. Después, disparar horizontalmente hacia terreno despejado: el virote debe avanzar con caída gradual. Repetir el disparo en Atalaya.

| Puesto | X | Y | Z |
|---|---:|---:|---:|
| Este | 17801,740 | −8824,610 | −3544,014 |
| Oeste | 15225,560 | −8726,520 | −4128,014 |

Este: `cow Tamriel 4 -3`; oeste: `cow Tamriel 3 -3`. Ratón para apuntar; Ataque para disparar; Sprint para cambiar Individual/Continuo; E para salir. Soltar Ataque después de entrar y hacer un clic nuevo. Laboratorio: `coc AstraAsedioTest`; Atalaya: `cow Tamriel 1 -4`.

Se conserva la recarga nominal de 1 s para el jugador y 2,5 s para guardias, la liberación nativa a 66,7 ms después de preparar Fire, la elevación −20° a +80°, el giro completo del núcleo/Atalaya y ±60° en ciudad. Las extensiones, escudos, torre baja, escaleras, NIF y los tres ESP son idénticos a v17. Se conserva la retirada de B40/B50; no se crean otros puestos nuevos. Las plataformas conservan Havok y no añaden NAVM. Los parches para otros mods de ciudades siguen pendientes.

Verificación fuera del motor: seis scripts compilados, ocho ejecutables con 2.368 aserciones C++, 275 pruebas y 107 subtests. **Esta DLL aún no fue probada en Skyrim**: la cámara, trayectoria e impactos requieren la prueba en juego descrita en PRUEBAS_EN_JUEGO.md.
