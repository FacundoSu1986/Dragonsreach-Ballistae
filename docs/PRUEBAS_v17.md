# Pruebas en Skyrim v17

Usar una copia de la partida de pruebas y reiniciar Skyrim al cambiar la DLL. Estas pruebas están pendientes; no son resultados de ejecución del motor.

1. En las dos torres, comprobar que sólo hay un puesto visible por plataforma y que la ballesta queda en el voladizo. Pulsar E desde la manivela y esperar la preparación: guardia en espera, jugador en mira, sin quedar con controles bloqueados. Repetir en una partida nueva si falla la copia anterior.
2. En Atalaya y en ambos puestos, apuntar horizontalmente y disparar a terreno despejado. El virote debe avanzar, con caída gradual; no caer a los pies de la ballesta. Comprobar también elevación −20° y +80°.
3. Confirmar un virote de acero consumido por disparo, daño e impacto. Hacer clics sucesivos y probar Individual/Continuo. Abrir un menú antes del disparo y salir con E: no debe salir un disparo pendiente ni quedar el jugador inmovilizado.
4. Salir de la mira, guardar la copia de pruebas, cargar y repetir E en ambas torres. Revisar que no reaparezcan los puestos antiguos ni queden guardias duplicados. Comprobar circulación en el piso original y acceso al voladizo.

Registros en `My Games/Skyrim Special Edition`: `Logs/Script/Papyrus.0.log` y `SKSE/AstraSight.log`. Conservarlos antes de reiniciar otra vez, porque el juego los rota o sobrescribe.

El inicio nativo debe indicar 3.5.2/API4. Buscar `AstraAsedioStation activate`, `entering player sight`, `reservation rejected` o `entry cancelled`. Para la trayectoria buscar `shot ballistics` (base, velocidad previa y asignada, dirección) y `shot flight sample` (distancia y velocidad después de al menos 50 ms). Una muestra ausente por impacto inmediato debe distinguirse de velocidad cero; probar una dirección despejada.

Para volver a v16, reinstalar ambos paquetes anteriores y cargar la copia original anterior a v17.
