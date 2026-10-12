# Comprobación de Astra Asedio v23

Entrega del 11 de octubre de 2026. Candidato local para pruebas en Skyrim SE 1.6.1170. No se ha instalado esta v23 en el perfil del juego ni publicado en remoto.

## Evidencia fuera del juego

| Comprobación | Resultado |
| --- | --- |
| Compilación Bethesda desde staging nuevo | 10 PSC/PEX; hashes de fuentes, binarios y desensamblado coincidentes |
| Compilación MSVC de AstraSight | DLL AMD64; API jugador 4 y API NPC 1 |
| Pruebas nativas CTest | 11/11 pasan; el ejecutable v23 incluye 51 aserciones |
| Contratos de colocación, animación y plugins v23 | 5/5 pasan |
| Regresiones de cámara, entrada y propiedad del jugador | 84/84 pasan |
| Decodificación independiente de HKX comprimidos | 4/4 pasan; esqueleto, escala, raíz, duración y transiciones |
| Plugins y VMAD | Cuatro ESP; referencias del mod, propiedades y aliases resueltos; sin FormID duplicados |
| Recursos del jugador preservados | Arma alta, atalaya y propiedades del jugador coinciden con v22 |
| PE y metadatos SKSE | Exportaciones, runtime 1.6.1170 y mínimo SKSE 2.2.8 verificados sin cargar la DLL |
| Vista previa de Blender | Agarre bajo, apoyo y recorrido completo −60° a +60° revisados; giro y disparo en MP4 |

Los informes completos están en `reports/verification_v23.json`, `plugin_compile.json`, `native_build_receipt.json`, `native_binary_checks.json`, `authoring_v23.json` y `hkx_validation_v23.json` del repositorio. El manifiesto del ZIP identifica sus recursos por SHA-256 y vincula la comprobación final, el `.blend` y el MP4. El empaquetador comprueba CRC, igualdad entre archivos originales y archivados, metadatos de PEX e igualdad de dos empaquetados del mismo inventario.

La revisión independiente de especificación sobre los artefactos y Papyrus terminó sin observaciones bloqueantes. El componente nativo recibió revisión manual del agente principal; no se presenta como una revisión independiente terminada. Entre las correcciones revisadas están los cinco argumentos reales de Generate, el plugin propietario de las estaciones, el centro físico de los objetivos, las dimensiones de aliados grandes, el primer impacto real, el contrato del proyectil y el acceso a OAR fuera del mutex de observaciones.

## Pruebas dentro de Skyrim

Todas las casillas siguientes están **pendientes**. La evidencia de PE y Address Library identifica las entradas de vtable, pero no demuestra la cadencia ejecutada, el orden del IK ni la reproducción de OAR en el juego.

- [ ] Cargar una copia de partida v22: guardias Este B71 y Oeste B81 dentro del cercado, detrás de sus mandos; brazos bajos y pies sobre el suelo.
- [ ] Pasar como jugador y observar seguimiento estable dentro del sector; comprobar lo mismo con un neutral. No debe iniciarse combate ni salir ningún virote.
- [ ] Introducir un enemigo en combate, visible y alcanzable a altura fija: debe tomar prioridad y producir un solo proyectil por ciclo.
- [ ] Cruzar un aliado por la trayectoria y aproximarlo al impacto: debe cancelarse el disparo antes de liberar el virote.
- [ ] Probar un obstáculo, un objetivo fuera de ±60° y uno a altura no alcanzable: no deben autorizar disparo.
- [ ] Recorrer todo el arco y revisar las manos con la armadura real, los pasos y la transición de vuelta al bucle.
- [ ] Interrumpir legítimamente la pose, matar al operador, alejarse para descargar el puesto y volver: deben cancelarse efectos y recuperarse los estados válidos.
- [ ] Guardar y recargar una partida v23 durante un giro o disparo; comprobar que no se duplica un proyectil ni queda un estado antiguo.
- [ ] Comprobar que los puestos bajos rechazan al jugador y que atalaya y estación principal conservan cámara, control y disparo del jugador.
- [ ] Ejecutar xEdit Check for Errors sobre los cuatro plugins con sus masters.

Para registrar un fallo, conservar `AstraSight.log` y, si está habilitado, el registro Papyrus. Anotar el puesto, el estado mostrado por `Astra guard v23`, la acción y una captura. El controlador cancela tiros cuando no puede certificar la postura, el suelo, la trayectoria o la protección de actores.

## Evidencia histórica

Las comprobaciones v22 se conservan por separado. No se ejecutan sus constructores sobre los recursos v23. La antigua discrepancia de hashes por finales de línea de esa copia de trabajo no certifica ni invalida los bytes de esta entrega. Las pruebas actuales usan fuentes y binarios v23, y las pruebas dentro del juego realizadas con versiones anteriores no se cuentan como pruebas v23.
