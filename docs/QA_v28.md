# Verificación v28

Trabajo realizado en `Ballesta_Astra_v28`, copia independiente de v27. La instalación MO2 y la partida del usuario no se modificaron.

## Evidencia del fallo v27

La sesión de AstraSight 3.5.8 contiene **6 adquisiciones, 7 confirmaciones OAR, 0 confirmaciones de agarre y 0 proyectiles**. Dos operaciones terminan por `hold replacement not observable`; las demás cancelaciones registradas corresponden a carga/reversión de partida. Snapshot de 3822 bytes, SHA-256 `9194df9d219bbe6bbb927fdac901983224b801e3e6ab781cf813bc584176abb0`, conservado en `build/guard-v28/observed_v27_AstraSight.log`.

El log Papyrus repite `backoff 5.000000s after 1 faulted acquisition(s)`. El código confirma que esa rama vuelve a programar la misma espera sin modificar su condición. Una prueba que ejecuta la condición y sus asignaciones durante dos actualizaciones reproduce dos esperas en v27 y una en v28. El diagnóstico y los hashes de los snapshots están en `reports/diagnosis_v27_grip.json`; no se distribuyen registros personales.

La ausencia de agarre tiene un defecto de arquitectura identificable: solo `postActor` lo habilitaba, esa rutina retornaba silenciosamente fuera del hilo principal y `tick` dependía de ella para apuntar. El registro v27 no mide si ese callback estaba ausente, sobrescrito, ejecutado en otro hilo o fuera de la ventana válida. No se atribuye una de esas causas concretas como demostrada.

## Corrección y límites

La adquisición v27 basada en paquete asignado B90 y observación OAR se conserva. v28 lleva la aplicación y certificación de la pose al controlador principal ya observado. `Character::Update` únicamente cuenta llamadas mediante atómicos; no manipula slots, escena o física. OAR válido no basta para autorizar fuego: las manos deben superar el ajuste limitado a 16 unidades y asentarse a menos de una unidad del mando. Las muestras de otro personaje, epoch, clip, duración, peso, futuro o antigüedad excesiva se rechazan.

El watchdog de postura cancela tras 1,5 s sin una muestra válida. Esta decisión sustituye en esa situación las dos reemisiones de idle de la ruta histórica por una cancelación explícita seguida del reintento Papyrus. Si una muestra OAR es válida pero los huesos aún están en transición y exceden 16 unidades, se cancela inmediatamente; ese caso necesita medirse en juego.

**Límite de sincronización:** observar un generador OAR no demuestra que la mezcla y copia final a los huesos Ni hayan concluido. El hilo principal tampoco certifica por sí solo el orden posterior a la animación. Este candidato elimina la dependencia del callback y añade telemetría; la persistencia visual de la corrección al siguiente frame sigue pendiente de validación en Skyrim. No se ha instalado un hook adicional supuesto como posterior al renderizado.

El reintento usa una bandera persistida: esperar una vez, reintentar, aumentar el contador tras otro fallo, y reiniciarlo solo con estado nativo saludable. La espera pasa de 5 a 30 s a partir del cuarto fallo consecutivo. Cargar o reiniciar el controlador limpia la bandera; se preserva el drenaje del token y el control por generación.

## Comprobaciones externas

- Pruebas previas fallando para el ciclo infinito y la falta de integración del agarre en el controlador principal.
- Contratos Python vigentes de IA, migración, escudo, diagnóstico, reintento y versiones. Las expectativas v27 que exigían el comportamiento defectuoso o la DLL 3.5.8 se mantienen históricas y se sustituyen por contratos v28 al verificar la entrega.
- CTest nativo, incluyendo 14 aserciones nuevas de observación/agarre: identidad, epoch, ausencia de callback, clip correcto, duración, peso, valores desconocidos, frescura e invalidación.
- Compilación de 10 scripts desde staging nuevo; fuentes, bytecode y desensamblados comprobados mediante hashes.
- Compilación AMD64 de AstraSight 3.5.9; metadatos SKSE y correspondencia de fuentes/DLL; dependencias externas comparadas antes/después por SHA-256.
- Regresiones de cámara/entrada/propiedad del jugador; referencias y propiedades de los cuatro plugins; decodificación independiente de cuatro HKX canónicos.
- ZIP reproducible, CRC e inventario completo: cuatro ESP, diez PEX y doce copias HKX. Recursos de escena idénticos a v27 y ZIP v23–v27 preservados.

Resultados y alcance de la revisión en `reports/verification_v28.json`, `native_build_receipt.json`, `plugin_compile.json`, `review_v28.json`, `package_v28.json` y `zip_independent_v28.json`.

## Pendiente en Skyrim v28

- Pose continua, agarre, pies y recorrido completo −60°/0°/+60°; comprobar errores de manos entre fotogramas.
- Jugador y visitantes seguidos, residentes no hostiles ignorados, enemigo prioritario y virote normal sincronizado.
- Obstáculos, aliados cruzando, altura no alcanzable y objetivos fuera de sector: tiro bloqueado.
- Muerte, stagger, cambio de equipamiento, descarga/carga, interrupción y recuperación tras una espera.
- Cámara y disparo de la atalaya y torreta del jugador; xEdit con todos los masters.

No se ha realizado una prueba jugable v28. Los informes externos y el preview anterior no sustituyen estas comprobaciones del motor.
