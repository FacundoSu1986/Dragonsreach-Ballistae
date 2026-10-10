# Astra Asedio QA v17

Versión de prueba para los dos fallos informados: E recarga los puestos de Whiterun sin entrar a la mira, y el virote del jugador cae inmediatamente tras el disparo rápido. La DLL es AstraSight **3.5.2/API4**.

El lanzamiento ahora asigna una velocidad inicial en la dirección real del cañón, tomada del PROJ de la munición (5.400 unidades/s en este mod). Se valida antes de consumir munición y nuevamente al lanzar. Se conserva el jugador como origen del daño, la gravedad, el alcance y la explosión. El registro incluye la velocidad que entregó el motor, la velocidad asignada y una muestra de movimiento posterior. La causa interna exacta de la caída no está medida todavía; la corrección y ese registro requieren prueba en Skyrim.

Whiterun utiliza referencias nuevas B70/B80, con todos los enlaces del jugador y del guardia inicializados desde el complemento. Se mantienen las mismas posiciones y las plataformas que confirmó Facu. Las diez referencias anteriores B40–B44/B50–B54 están desactivadas en el ESP; el alias del jugador también retira sus instancias guardadas después de terminar sus efectos y liberar al guardia. Una partida puede conservar propiedades y enlaces de una versión anterior: no dependemos de que esos enlaces se reescriban. No pudimos inspeccionar la partida de esta prueba, por lo que esa explicación sigue siendo una hipótesis.

El límite de preparación del guardia aumenta de tres a diez segundos. Una prueba de las fuentes reproduce que una preparación que termina a los cuatro segundos se cancelaba con v16; ahora puede continuar. Se mantienen las comprobaciones de muerte, menú, descarga de la celda y cambios de propietario. El registro indica en qué etapa se cancela una entrada.

## Instalación

1. Cerrar Skyrim completamente; la DLL requiere reinicio.
2. Instalar **AstraAsedio_QA_v17_MO2.zip** y **AstraAsedio_WhiterunTorres_QA_v17_MO2.zip**, desactivando las versiones anteriores. Deben ganar AstraSight.dll y los seis PEX del núcleo.
3. Activar AstraAsedio.esp y AstraAsedio_WhiterunTorres.esp, con ciudad después del núcleo. Atalaya es opcional. Mantener desactivado el antiguo AstraAsedio_Whiterun.esp.
4. Probar con una copia de la partida de pruebas, fuera de la mira. Conservar la partida original para volver a v16: guardar con v17 puede conservar la retirada de las referencias antiguas.

No se modificaron MO2, el runtime ni partidas durante la preparación. Requisitos: Skyrim SE 1.6.1170, SKSE64 2.2.8 mínimo y Address Library. No compactar los IDs.

## Prueba principal

En Whiterun, acercarse a la manivela del puesto nuevo y pulsar E una vez. El guardia debe retirarse y debe entrar la cámara de mira. La preparación puede tardar algunos segundos; el disparo sigue usando el camino rápido nativo.

| Puesto | X | Y | Z |
|---|---:|---:|---:|
| Este | 17801,740 | −8824,610 | −3544,014 |
| Oeste | 15225,560 | −8726,520 | −4128,014 |

Este: `cow Tamriel 4 -3`; oeste: `cow Tamriel 3 -3`. Ratón para apuntar; Ataque para disparar; Sprint para cambiar Individual/Continuo; E para salir. Soltar Ataque después de entrar y hacer un clic nuevo. Laboratorio: `coc AstraAsedioTest`; Atalaya: `cow Tamriel 1 -4`.

La recarga nominal mínima sigue siendo 1 s para el jugador y 2,5 s para los guardias. Se conserva la elevación −20° a +80°, el giro completo del núcleo/Atalaya y ±60° en ciudad. Se conservan los escudos, la torre baja y las escaleras. Las plataformas tienen Havok y no añaden NAVM. Los parches para otros mods de ciudades siguen pendientes.

Verificación fuera del motor: seis scripts compilados, siete ejecutables con 2.352 aserciones C++, 313 pruebas y 107 subtests. La entrada real, la trayectoria, el daño y la migración de la partida aún requieren confirmación en Skyrim.
