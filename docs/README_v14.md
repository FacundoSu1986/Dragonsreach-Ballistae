# Astra Asedio QA v14

El jugador tiene un ciclo nominal de **1 segundo** y los artilleros un intervalo mínimo de **2,5 segundos** entre lanzamientos. Fire dura 0,2 s, liberación 1/15 s y Reset 0,8 s; la preparación, giro y programación del motor pueden ampliar el intervalo. Las animaciones del arma se retimaron en esa proporción. Se conserva el apuntado del jugador de −20° a +80°, la torre baja a 2 m, 11 peldaños y 12 escudos apoyados; no hay habitación ni puerta inferior.

El complemento nuevo coloca dos ballestas con guardias propios sobre las dos torres exteriores indicadas por Facu. La escala y el sector de cada puesto se ajustan al espacio medido bajo sus techos. La ballesta del jugador conserva su tamaño. Ambos pisos tienen triángulos NAVM vanilla al mismo nivel; esto comprueba presencia geométrica, y no una ruta de IA ejecutada en Skyrim.

## Instalación en MO2

1. Conservar v13 y su partida para volver atrás. Instalar `AstraAsedio_QA_v14_MO2.zip` como mod nuevo; desactivar la versión anterior del núcleo para que carguen los scripts y el NIF v14.
2. Activar `AstraAsedio.esp`. `AstraAsedio_Atalaya.esp` conserva la colocación del jugador junto a la atalaya y puede activarse por separado.
3. Instalar `AstraAsedio_WhiterunTorres_QA_v14_MO2.zip` y activar **`AstraAsedio_WhiterunTorres.esp` después del núcleo**. Desactivar **`AstraAsedio_Whiterun.esp`**, el complemento anterior con la torre independiente.
4. Usar una partida de prueba nueva para las colocaciones. No se promete migrar las referencias persistentes del viejo complemento de ciudad. Los valores temporales conocidos de v13 sí se migran de forma idempotente en los controladores; sus callbacks antiguos se invalidan.

Skyrim SE 1.6.1170, SKSE64 2.2.8 mínimo y Address Library del perfil que ya funcionaba. DLL AstraSight **3.4.0/API 3 idéntica a v13**, reutilizada de su compilación verificada. Son ESP normales, sin compactar IDs. No se modificó el runtime ni el perfil MO2 durante la construcción.

## Ubicación y controles

| Torre | X | Y | Z base | Escala | Giro frontal | Elevación |
|---|---:|---:|---:|---:|---|---|
| Este | 17777.740 | -8308.610 | -3616.014 | 0.75 | -10° a 10° | -20° a 20° |
| Oeste | 15201.560 | -8338.520 | -4128.014 | 0.65 | -10° a 2° | -20° a 0° |

- Este: `cow Tamriel 4 -3`, celda WhiterunExterior01 (0000961B), piso cercano a Z −3616.
- Oeste: `cow Tamriel 3 -3`, celda WhiterunExterior14 (0000961C), piso cercano a Z −4128.
- Laboratorio: `coc AstraAsedioTest`. Atalaya: `cow Tamriel 1 -4`.

Las coordenadas son los centros de las bases definitivas; el ajuste XY permite despejar refuerzos y barandas. Los guardias y marcadores están sobre los pisos existentes. `TORRES_v14.json` contiene alturas, apoyo y límites de las mediciones.

Jugador: activar manivela, E para salir, ratón para apuntar, Ataque para disparar y Sprint para alternar Individual/Continuo. Los puestos nuevos están reservados a sus guardias y no toman los controles ni la cámara del jugador.

## Guardias y compatibilidad

Cada artillero es un NPC propio basado en la plantilla imperial vanilla. Se mantiene en su puesto y dirige la ballesta hacia su objetivo de combate hostil y visible, descartando jugador y compañeros como blancos. La munición NPC no tiene explosión. El controlador calcula el arco bajo desde la posición mundial real de la boca; la escala no cambia la velocidad/gravedad del proyectil.

Se utilizan Fire/Reset del arma. Todavía falta la animación humana propia de operar/cargar: el NPC conserva arco, espada y combate normal vanilla. También quedan por probar su postura, daño y comportamiento en el motor. Hay LOS desde el guardia y comprobación del jugador en la trayectoria; falta un raycast Havok desde la boca y detección incidental de todos los otros NPC. Los sectores medidos sólo cubren las geometrías vanilla incluidas en la inspección.

El complemento incorpora referencias propias persistentes y dos NPC nuevos. Usa WRLD Tamriel (0000003C) y su CELL persistente (00000D74) como contenedores; no modifica LAND, NAVM, NAVI, puertas, paquetes, actores vanilla ni modelos/posiciones de las torres. Se reubican además los destinos de patrulla 00078784, 0007878A sobre puntos vecinos medidos, para que no queden dentro de las bases. Sólo cambia DATA de posición; se conservan rotación, NAME, flags y vínculos. Los destinos tienen piso/NAVM/cápsula inspeccionados; el recorrido real de las patrullas requiere prueba en el motor. Las celdas físicas son 0000961B y 0000961C. Un mod que reemplace las torres, techos, murallas o destinos de patrulla puede necesitar un parche; el complemento separado permite hacerlo después.

Atalaya permanece idéntico a v13 y conserva los cambios de terreno y cuatro referencias vanilla heredadas de v11. No se integraron aún relevos, rutas nuevas ni estados de Guerra Civil. `COMPATIBILIDAD_v14.json` enumera IDs/masters/posiciones exactos para futuros parches.

Esta entrega está verificada en archivos, compilación, fixtures y geometría fuera del motor. Los renders son vistas estáticas de los archivos. **La nueva cadencia y los dos puestos aún requieren prueba en Skyrim**; la mejora de apuntado de v13 fue confirmada por Facu.
