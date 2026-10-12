# Corrección v24: operadores de ballesta exclusivos

La prueba del usuario y los registros del 11 de octubre confirman que la v23 cargó su DLL, API de OAR y migración de ambos operadores, pero ninguna adquisición superó el contrato de estación/actor/rig/suelo/graph/solicitud de idle. El controlador restauró después el estado anterior; los NPC conservaban la IA y el inventario del guardia vanilla, sin paquete de puesto. Por eso pudieron entrar en combate con sus arcos. El mensaje agregado no identifica la cláusula fallida ni prueba que se rechazó antes de OAR; se debe mejorar esa evidencia sin presentar una hipótesis como una causa medida.

Se conserva la animación aprobada, el giro horizontal ±60°, la altura constante y el virote normal. El jugador sigue protegido incluso si comete un delito: golpear a un vendedor sirve para probar que estos dos artilleros no sacan sus arcos, pero el disparo de la ballesta debe probarse con un enemigo válido que no sea el jugador ni un aliado.

## Diseño elegido

Un paquete privado basado en DefaultStayAtCurrentLocation, con Ignore Combat, Weapons Unequipped y No Combat Alert, sin reacciones ni idles de conversación, se asigna a los dos aliases de operadores. Es preferible a borrar inventarios o desactivar toda su AI, porque conserva armaduras, detección y animación. Vive en el plugin de Whiterun para evitar un ciclo de masters y se añade al principio de los paquetes de los dos NPC propios, sin tocar un registro vanilla. El alias garantiza también el paquete para las bases FF generadas por partidas existentes. El controlador exige observar ese paquete y las manos libres antes de autorizar un tiro.

La migración se incrementa a 24, reevalúa los paquetes y vuelve a colocar a los dos operadores después de drenar cualquier propietario nativo anterior. La orientación de un actor libre no es condición previa para adquirirlo: el propietario nativo establece su orientación al comenzar. La altura inicial admite únicamente el pequeño margen de soporte físico del controlador, lo conserva durante la órbita y comprueba el mismo suelo en cada paso; no añade seguimiento vertical. El controlador no recoloca a un actor ajeno ni fuera del puesto aprobado.

Se conservan las verificaciones de trayectoria, impacto, hostilidad y protección de actores. No se cambian las estaciones del jugador. Se añaden causas específicas y datos físicos a los rechazos de adquisición para que la siguiente prueba en Skyrim pueda confirmar o aislar la causa restante.

## Verificación y entrega

Pruebas de contrato sobre el paquete y los aliases reales; pruebas portables de adquisición con orientación libre, margen pequeño de altura y rechazo de posiciones inválidas; compilación de PEX y DLL; todas las comprobaciones de jugador, HKX y paquete vigentes. Nuevo ZIP v24, sin sustituir el v23 original ni instalar automáticamente sobre MO2. La reproducción de OAR, la selección efectiva del paquete y el soporte físico se certificarán con una nueva prueba en el juego, separada de la evidencia previa del fallo.
