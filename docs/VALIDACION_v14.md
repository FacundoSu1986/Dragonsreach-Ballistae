# Evidencia QA v14

Los recibos `verification_v14.json`, `plugin_compile.json`, `native_reuse_v14.json`, `spatial_reuse_v14.json`, `towers_v14.json` y `package_qa_v14.json` pertenecen a esta entrega. Los reportes v11/v12/v13 que permanecen en el proyecto son históricos.

- Compilación Bethesda desde staging limpio y desensamblado de cinco scripts finales; recibos SHA256 enlazan PSC, PEX y disassembly.
- Pruebas del código PSC con fixtures de API, lifecycle/cancelación/cadencia, intervalos ante retrasos nativos, límites por torre y boca mundial escalada. Estas pruebas no ejecutan la VM Papyrus del juego.
- DLL/entradas nativas idénticas a la compilación v13; cinco ejecutables portables idénticos volvieron a pasar 2.281 assertions. No se afirma una compilación nativa nueva.
- Retiming NIF: sólo 1.978 floats temporales registrados; ningún byte espacial, shader o Havok cambia. Evidencia espacial del jugador v13 reutilizada explícitamente por comparación exacta: 36.360 tiros estáticos y 288 poses de cámara. No son ejecuciones geométricas nuevas v14 ni combates del motor.
- Los records del núcleo conservan bytes/IDs salvo VMAD temporal del jugador. Atalaya queda idéntico. El complemento nuevo registra dos NPC propios y seis referencias arma/artillero/marcador persistentes, CELL/WRLD como contenedores y los ajustes de destino de patrulla detallados en COMPATIBILIDAD_v14.json.
- Para las torres se reimportan modelos visuales/Havok y se mide piso, contacto de base, cápsula de cuerpo, NAVM y recorrido angular estático de reposo. No es un barrido completo de los keyframes Fire/Reset. El reporte distingue muestreo geométrico de verificación en motor.
- ZIP revisados con CRC, inventario único y SHA256 de cada entrada; builder de plugins idempotente. Las cuatro licencias de dependencias nativas se incluyen.

Pendiente en Skyrim: cadencia percibida, sincronización real, colisión/daño del proyectil, postura/combate normal del NPC, eventos de carga/guardado y compatibilidad con Guerra Civil y otros mods. La mira v13 fue probada por Facu; esto no valida automáticamente los nuevos puestos.

Contrato de escala usado: SKSE64 obtiene `m_worldTransform.rot` y `m_worldTransform.pos` por separado; la lectura de rotación no incorpora la escala uniforme. Fuente primaria: https://github.com/ianpatt/skse64/blob/master/skse64/PapyrusNetImmerse.cpp . El fixture prueba la balística desde la boca escalada, pero no sustituye una prueba del NIF en Skyrim.
