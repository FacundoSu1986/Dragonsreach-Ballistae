# Pruebas en Skyrim v18

Usar una copia de la partida, fuera de la mira, y reiniciar Skyrim al cambiar la DLL. Estas pruebas están pendientes; no son resultados de ejecución de v18 en el motor.

1. En ambas torres, comprobar que la ballesta queda en la extensión. Pulsar E desde la manivela: guardia en espera, jugador en mira y modelo visible durante toda la entrada. Salir con E y repetir. La preparación tiene un límite de diez segundos y puede tardar algunos segundos.
2. En Atalaya y ambos puestos, disparar horizontalmente hacia terreno despejado y observar el virote al menos medio segundo. Debe avanzar y caer gradualmente. Probar también −20° y +80°.
3. Confirmar un virote de acero consumido por disparo, impacto y daño. Probar clics sucesivos y modo Continuo. Abrir un menú antes del lanzamiento y salir con E: no debe quedar un disparo pendiente ni controles bloqueados.
4. Salir de la mira, guardar la copia, cargar y repetir E en ambas torres. Revisar que no reaparezcan puestos antiguos, que el guardia recupere su puesto y que pueda circular por el piso original.

Registros en `My Games/Skyrim Special Edition`: `Logs/Script/Papyrus.0.log` y `SKSE/AstraSight.log`. Conservarlos antes de reiniciar otra vez, porque el juego los rota o sobrescribe.

El inicio nativo debe indicar **3.5.3/API4**. Para Whiterun buscar `AstraAsedioStation activate`, `entering player sight` y los eventos `OnLoad`, `OnUnload`, `OnCellDetach`. Una descarga entre la activación y la entrada permite localizar una cancelación restante. Las comprobaciones de menú, muerte y celda descargada siguen activas.

Para el virote buscar `shot speed normalization`: con este PROJ, `calculated_after` debe ser aproximadamente 5.400. El caso observado en v17 era `calculated_before=756` y multiplicador 1; su corrección esperada es aproximadamente 7,142857. Revisar también `shot flight sample`: etapas 0/1/2 desde 50/250/500 ms, velocidad, distancia, loaded3D y distance_moved. Una muestra inicial sin movimiento no prueba un fallo por sí sola. Un proyectil que impacta o se descarga puede quedar unavailable; por eso la prueba debe apuntar hacia terreno despejado. El retardo real de v18 se mide con `input_to_launch_ms`.

Si continúa un fallo, conservar ambos registros de esa sesión; permiten distinguir velocidad recalculada, impacto temprano y cancelación de entrada. Para volver a v17, reinstalar sus dos paquetes y cargar la copia original anterior a v18.
