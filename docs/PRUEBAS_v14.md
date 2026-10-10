# Prueba en Skyrim SE 1.6.1170: QA v14

Usar una partida nueva descartable con el núcleo v14 y el nuevo WhiterunTorres; el viejo Whiterun debe estar desactivado. Arrancar por SKSE.

1. Laboratorio: repetir giro 360° y elevación −20°/+80°, tiros al suelo, escalera/escudos y salida de la mira. En Continuo medir al menos diez lanzamientos: ciclo nominal 1 s, más preparación/programación. Comprobar que cuerda, virote y Fire/Reset se sincronizan y no se duplica munición/sonido.
2. Abrir menú y guardar/cargar durante Fire y Reset; comprobar vuelta de cámara/controles, ausencia de callbacks viejos y valores temporales migrados. Para evaluar las colocaciones seguir usando partida nueva.
3. Localizar Este con `cow Tamriel 4 -3` y Oeste con `cow Tamriel 3 -3`. Revisar contacto de bases, cuerpo del guardia, techo/postes, barandas y entrada. Recorrer cada sector contra blancos hacia el acceso exterior; observar colisión real del proyectil.
4. Provocar combate exterior en esa partida descartable. Cada ballesta debe apuntar sólo al objetivo hostil de su artillero y lanzar con separación ≥2,5 s; fuera del sector debe rechazar el blanco. Verificar daño, atribución y munición sin explosión. Registrar si el NPC usa además arco/espada o cambia de postura.
5. Cruzar delante durante preparación: comprobar cancelación de tiros peligrosos al jugador. Observar otros NPC cruzando porque su detección incidental aún no está implementada.
6. Descargar/recargar zona, guardar/cargar y matar el guardia durante un ciclo. No deben quedar disparos sin operador ni NPC duplicados. El controlador no resucita al artillero.
7. Probar fases de Guerra Civil y los mods de ciudad que se quieran conservar. La navegación de relevos y cambio de facción no están implementados. Para conflictos, desactivar sólo WhiterunTorres y registrar mod/versión, orden de carga, torre/coordenadas, captura y logs.

La presencia de NAVM encontrada en archivos no demuestra que un guardia camine por la escalera: este prototipo se coloca directamente en su puesto y fija su movimiento. No contiene una animación humana propia de operación.
