# Pruebas Skyrim v10

Seleccionar AstraAsedio_QA_v10 en MO2, iniciar SKSE y una partida nueva. `coc AstraAsedioTest`. AstraSight.log debe empezar con "AstraSight 3.3 API 3 … tail sight camera with iron sights". Con DLL 3.1 o 3.2 la activación se rechaza con NATIVE_SIGHT_MISSING.

## Cámara y mira (lo principal)
1. Entrar con E: la vista sale desde la cola de la ballesta, con el arma delante, el anillo del alza y el guion dentro.
2. Girar despacio una vuelta completa a cada lado, en tiro horizontal. La cámara no debe saltar a tus ojos en ningún giro (en v09 pasaba entre ~130° y ~240°).
3. Repetir la vuelta parado en otro lugar del puesto (más cerca del pedestal, más atrás) y a +35° y +80°. Al elevar, la cámara avanza hacia el alza; a +80° el anillo se ve grande alrededor del guion. Si querés, subí de un salto al pedestal y operá desde ahí: la cámara tampoco debe saltar.
4. AstraSight.log: anotar cualquier "camera deviation start" con dev de más de ~10 u que dure más de un instante (en v09 eran de 140–178 u y duraban 2–3 s). Copiar AstraSight.log y Papyrus.0.log antes de volver a abrir el juego.

## Puntería
5. Apuntar casi en horizontal con la punta del guion en el centro del anillo, sobre el blanco de 10 m y sobre el de 30 m. Con el cero a 75 m, el modelo predice que el virote pega por encima del punto de mira: unos 3 cm a 10 m y unos 28 cm a 30 m (el máximo, ~32 cm, cae hacia los 40 m; a 75 m, en el punto; a 100 m, ~66 cm por debajo). Eso es lo correcto, no una falla. Anotar la diferencia real.
6. Disparar a +35° y +80° a algo lejano y comprobar que el guion sigue marcando dónde cae.

## Siguen pendientes
7. Daño con `getav health` (nominal 35 + 10 + explosión 150), atribución de la muerte.
8. Virote: no recogible; si cae o rebota, apoyado en todo su largo.
9. Sonido una vez por virote; ráfaga con clics rápidos; Tab con un disparo en curso; Sprint.
10. Guardar y cargar en cada fase, salir de celda, morir: sin controles bloqueados.

Cero casos de motor v10 ejecutados por el agente. Los renders y las mediciones geométricas no prueban la cámara real ni la puntería en Skyrim.
