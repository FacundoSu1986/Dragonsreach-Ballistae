# Astra Asedio v29

Desde esta versión, las manos de los guardias quedan sobre las empuñaduras gracias a la animación, sin correcciones posteriores. En v23–v28, apuntar y disparar dependían de una «confirmación de agarre» que nunca se cumplió en juego. Además, ante cualquier desfase la pose se relanzaba o se cancelaba, y por eso los brazos empezaban a subir y nunca terminaban de agarrar la ballesta.

## Qué se midió antes de cambiar

- **La animación.** Aplicado al esqueleto vanilla, el clip de sostener deja las muñecas a 0,02 u de las empuñaduras.
- **La ballesta.** `ballesta_guardia.nif` tiene las empuñaduras exactamente donde la animación pone las manos.
- **La instalación.** Lo que hay en MO2 coincide byte a byte con el repositorio.
- **La entrada a la pose.** Al iniciar `IdleHandsBehindBack`, el juego hace una mezcla de 0,5 s. v28 cancelaba si las manos estaban a más de 16 u durante esa mezcla, lo que ocurre siempre al empezar.

## Instalación

Cierra Skyrim. Instala `AstraAsedio_QA_v29_Unificado_MO2.zip` en MO2 como mod nuevo y desactiva el paquete Astra anterior (`AstraAsedio_QA_v`). Activa estos cuatro plugins en este orden relativo:

1. AstraAsedio.esp
2. AstraAsedio_WhiterunTorres.esp
3. AstraAsedio_Atalaya.esp
4. AstraAsedio_GuardAnim.esp

Requisitos: Skyrim SE 1.6.1170, SKSE 2.2.8, Address Library y Open Animation Replacer con la API Animations V1. Incluye AstraSight **3.6.0** (API jugador 4, NPC 1). Los ESP, NIF, HKX y la configuración OAR son idénticos a v27/v28, así que no necesitas mover a los guardias de lugar en una partida existente.

## Qué esperar

- **Agarre.** En menos de un segundo, cada operador sube las manos y las deja sobre las empuñaduras. No vuelve a bajarlas al abrir la consola, el inventario o un diálogo.
- **Seguimiento.** Siguen al jugador y a cualquier NPC que no sea residente ni guardia de Whiterun, dentro del sector de ±60° y a menos de 30 m. Giran ballesta y cuerpo juntos a 20°/s como máximo y ninguno de los dos suelta las manos. Los pies se deslizan durante el giro.
- **Disparo.** Solo a enemigos hostiles en combate, alcanzables con tiro horizontal (hasta 6000 u) y con la trayectoria libre. El jugador, sus aliados y los neutrales siguen protegidos.
- **Obstáculos.** Si una baranda u otro obstáculo impide girar más, el guardia se queda en el último ángulo válido sin soltar la pose.

## Comprobar en el log

En `AstraSight.log`:

- `AstraSight 3.6.0`: está cargada la DLL correcta.
- `guard v29 holding`: el operador entró en la pose.
- `guard v29 pose ... handErrorL= handErrorR=`: aparece cada 2 s por puesto e indica a cuántas unidades están las muñecas de las empuñaduras. Lo esperado es unas 3 u, por la estatura nórdica 1,03. Si ves valores de 20 o más, la pose no se está aplicando. Este número solo se mide; no bloquea nada. En esa misma línea, `moveRefused` indica por qué no se pudo girar más, por ejemplo por una baranda o falta de apoyo; `none` significa que nada lo impidió.
- `guard real projectile`: se lanzó un virote real.
- `guard v29 hold re-request`: el clip estuvo 3 s sin muestras y se volvió a pedir. Es normal si el guardia queda fuera de cámara.
- `guard cancel ... reason=`: el motivo de una cancelación.

## Límites

Esta versión **no se probó en Skyrim**. Para disparar no hay gesto corporal: la ballesta dispara y se recarga con su propia animación mientras las manos siguen sobre las empuñaduras. Los clips de giro y de disparo siguen instalados, pero el runtime ya no los usa. Ver `QA_v29.md` para el alcance exacto de lo verificado.
