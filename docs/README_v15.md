# Astra Asedio QA v15

V15 corrige el control de las dos ballestas de las torres exteriores de Whiterun: ahora el jugador puede usarlas. Sus bases, operadores y guardias en espera se trasladan a dos plataformas voladizas propias, con piso Havok, acceso y refuerzos apoyados sobre la muralla. El complemento retira los dos cambios de posición de destinos de patrulla de v14.

El disparo del jugador pasa al controlador nativo AstraSight 3.5.0/API 4. El clic admitido inicia Fire en el siguiente fotograma válido y libera el proyectil tras el marcador de **1/15 s, unos 67 ms**, más la programación del motor. Ya no espera las fases OnUpdate de Papyrus. Esta es la programación implementada; todavía falta medir clic real → proyectil dentro de Skyrim. Recarga nominal mínima desde el lanzamiento: **1 s**. Los guardias conservan un intervalo mínimo de **2,5 s**.

Se preservan el núcleo y la Atalaya de v14: torre baja, habitación y puerta inferior retiradas, escalera corta y 12 escudos ajustados. La mejora de apuntado anterior fue confirmada por Facu. El laboratorio y la Atalaya mantienen giro completo y elevación −20° a +80°. Los puestos exteriores usan giro frontal −60° a +60° y elevación −20° a +80°, para respetar el entorno medido.

## Instalación en MO2

1. Conservar v14 y su partida para volver atrás. Instalar **AstraAsedio_QA_v15_MO2.zip** como mod nuevo y desactivar el núcleo anterior. Deben ganar los scripts y la DLL de v15.
2. Activar **AstraAsedio.esp**. Activar **AstraAsedio_Atalaya.esp** si se desea la colocación junto a la atalaya.
3. Instalar **AstraAsedio_WhiterunTorres_QA_v15_MO2.zip**, desactivar el complemento de torres v14 y activar **AstraAsedio_WhiterunTorres.esp después del núcleo**. Desactivar también el antiguo **AstraAsedio_Whiterun.esp**.
4. Usar una **partida de prueba nueva** para las referencias persistentes de ciudad. No se promete migrar los guardias, scripts o puestos guardados por v13/v14. No limpiar ni sobrescribir la partida habitual para esta prueba.

Requisitos: Skyrim SE **1.6.1170**, SKSE64 **2.2.8** mínimo y Address Library del perfil que ya funcionaba. Son ESP normales; no compactar sus IDs. La construcción no instaló nada en el runtime ni modificó MO2.

## Ubicación

| Puesto | X base | Y base | Z base | Escala |
|---|---:|---:|---:|---:|
| Este | 17801.740 | -8824.610 | -3544.014 | 1 |
| Oeste | 15225.560 | -8726.520 | -4128.014 | 1 |

- Este: `cow Tamriel 4 -3`, torre exterior cercana a las coordenadas originales X 17801.74 / Y −8324.61 / Z −3615.66. El acceso sale por un lateral y sube cuatro escalones cortos antes de rodear el poste existente.
- Oeste: `cow Tamriel 3 -3`, torre cercana a X 15225.56 / Y −8306.52 / Z −4127.66. Tiene una extensión plana al nivel de su piso.
- Laboratorio: `coc AstraAsedioTest`. Atalaya: `cow Tamriel 1 -4`.

Las bases definitivas están desplazadas hacia el exterior para dejar libre el paso original. `PLATAFORMAS_v15.json` incluye posiciones, referencias, colisión y mediciones. Las vistas Blender son estáticas de los NIF, no capturas del juego.

## Controles y guardias

Acercarse a la manivela y activar. El guardia propio suspende su control, espera a terminar cualquier operación pendiente y se coloca en el punto de espera de la plataforma. El jugador entra en la mira. Ratón: apuntar; Ataque: disparar; Sprint: alternar Individual/Continuo; Activar/E: salir. Las acciones siguen los controles configurados de teclado/ratón. No se implementó entrada de mando.

Un clic durante recarga se descarta. Mantener Ataque en Continuo repite cuando el arma vuelve a estar lista; no acumula disparos tras un menú o un fotograma lento. La munición del jugador se cobra una vez por lanzamiento válido; un lanzamiento fallido intenta devolverla. Al salir, el arma vuelve a una pose neutral y el guardia recupera el puesto después de la limpieza nativa y la devolución de controles. Un guardia muerto, deshabilitado o ausente no impide el uso del jugador.

El NPC conserva su combate y postura vanilla; no hay animación humana nueva de operar o cargar. El arma conserva sus secuencias Fire/Reset. Los guardias disparan a su objetivo de combate hostil y visible, excluyendo jugador y compañeros, con munición sin explosión. Aún requiere prueba en Skyrim la selección de blancos, atribución/daño, comportamiento de combate y postura.

## Compatibilidad y alcance de la prueba

WhiterunTorres agrega únicamente sus dos plataformas, dos NPC y referencias propias. WRLD Tamriel y su CELL persistente son contenedores. **No edita LAND, NAVM, NAVI, PACK, destinos de patrulla ni posiciones/modelos de las torres vanilla.** Las mediciones conservaron 3.900 centros de cápsula muestreados sobre el navmesh original, incluidos ambos destinos de patrulla. Esto no demuestra todas las rutas de IA ni la escalera ejecutada en el motor.

Las plataformas nuevas tienen colisión física y **no añaden navmesh**. El artillero se coloca y mantiene directamente en su puesto; su traslado al punto de espera también es directo. No se prometen relevos o patrullas que caminen por la extensión. El acceso Este incluye una prueba geométrica de subida de escalones de hasta 20 unidades; su tránsito real necesita comprobación en Skyrim.

Mods que cambien las torres, murallas o su entorno pueden requerir un parche de colocación. El complemento separado permite prepararlos después. Atalaya conserva sus modificaciones heredadas de terreno/referencias vanilla. No se implementaron estados ni relevos de Guerra Civil. Tampoco se añadió un raycast Havok dinámico desde la boca ni protección incidental de todos los NPC; la geometría estática inspeccionada corresponde al entorno vanilla.

La entrega tiene compilación, pruebas de fuentes, verificaciones de archivos y geometría fuera del motor. **La activación de ciudad, la latencia real y el acceso/combate todavía requieren prueba dentro de Skyrim.** Ver `PRUEBAS_EN_JUEGO.md`.
