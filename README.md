# Astra Asedio — QA v21

> **Esta carpeta es la copia de trabajo v27.** Documentos vigentes: `docs/README_v27.md` y `docs/QA_v27.md`. Cambios respecto a v26: diagnóstico y resiliencia acotada del guardia (DLL 3.5.8, Papyrus recompilado; ESP/HKX/NIF/OAR sin tocar). Sin probar en Skyrim. El texto de abajo queda como historial v21.

Paquete de prueba completo para Skyrim SE Steam 1.6.1170, SKSE 2.2.8 y Address Library AE 1170. Mantiene AstraSight 3.5.4/API 4, el disparo, el proyectil y las ballestas de Whiterun. El script de la ballesta conserva el blanco de combate al montar.

## Qué corrige

- El paquete incluye ahora AstraAsedio_WhiterunTorres.esp y sus dos voladizos. Ese addon faltaba en la instalación inspeccionada; el registro del juego confirmó que no estaba cargado.
- Reubica la atalaya en el origen X 4665,54 / Y −14922,81 / Z −5217,81, orientación 187,63°, celda 0000963D (1,−4). La ballesta queda en la misma X/Y, 151,55 unidades más arriba. La malla es `torre_atalaya_v20.nif`, la que se ajustó a ese suelo.
- Conserva los FormID de las quince referencias: torre, ballesta, cofre y doce escudos. No edita NAVM, misiones, guardias vanilla ni marcadores de aterrizaje.
- Al montar, el juego envaina al jugador y el dragón pierde el blanco. El script guarda ese blanco antes de tomar la ballesta y lo reafirma una vez por segundo. Hay que entrar en combate con el dragón y después montar. Un dragón que aparece recién después de montar no queda agarrado. Salir es la misma activación de siempre.
- La escalera apoyaba sobre dos escombros (ImpExtRubble03 e ImpExtRubble02). Esos dos quedan desactivados y el suelo del pie de la escalera sube hasta el primer peldaño, un escalón de entre 7 y 16 unidades. El resto del terreno de la celda no cambia.

## Instalación en MO2

1. Cerrá Skyrim y conservá una copia de tu partida antes de probar una actualización.
2. Instalá AstraAsedio_QA_v21_Completo_MO2.zip como un mod nuevo llamado **AstraAsedio v21 completo**. Si ya había un v21 instalado, reemplazalo con este zip: el anterior no traía el script del dragón.
3. Desactivá las instalaciones anteriores de Astra Asedio en el panel izquierdo: paquete principal, addon de la atalaya y addon de Whiterun, si existe. Activá solo este paquete completo.
4. En el panel derecho activá estos tres plugins, con el principal primero:
   - AstraAsedio.esp
   - AstraAsedio_WhiterunTorres.esp
   - AstraAsedio_Atalaya.esp
5. Comprobá que MO2 no muestre masters faltantes. La prueba debe usar los ESP y NIF del mismo paquete v21.
6. Abrí Skyrim desde MO2. Si el juego ya estaba abierto, cerralo por completo —también en el administrador de tareas si el proceso sigue— y volvé a abrirlo. Un script nuevo no entra con una recarga de partida.

No hace falta borrar tus partidas. La actualización de referencias que ya se usaron necesita una comprobación dentro del juego; no se certificó la migración de una partida concreta.

## Cómo encontrar y probar la atalaya

Estas coordenadas son el origen de la torre. La Z queda debajo del piso. La ballesta está en la misma X/Y, con Z −5066,26.

```text
player.setpos x 4665.54
player.setpos y -14922.81
player.setpos z -5217.81
player.setangle z 187.63
```

Para quedar junto a la ballesta, repetí X, Y y el ángulo con `player.setpos z -5066`.

Probá subir por la escalera, activar la mira, disparar a tierra y salir de la mira. Para el dragón, entrá en combate primero y recién ahí montá. El cofre de virotes está debajo del piso. En Whiterun deben aparecer las dos estaciones y los dos voladizos.

Para la prueba de MQ104, usá una partida previa al combate y avanzá la misión jugando normalmente. Observá el aterrizaje, el combate y las patrullas; forzar etapas por consola no verifica esa secuencia.

## Verificación y límites

La malla de este sitio se reimportó en su revisión: 244 puntos de acceso y 1.512 poses estáticas de apuntado. El proxy de navegación de esta misma colocación registró obstrucciones; no es el claro del afloramiento del noreste. Otros órdenes de carga y mods que cambien roca, terreno o navmesh necesitan su propia revisión.

Estos controles son geométricos. Falta la prueba en Skyrim de MQ104, la IA, el guardado y la recuperación de las estaciones de Whiterun.

Sigue siendo QA: no es una versión estable lista para Nexus. Quedan pendientes la validación formal en xEdit/Creation Kit y la prueba de juego. Los registros WRLD/CELL que sirven de contenedores todavía requieren revisión de compatibilidad antes de publicar. No se distribuye geometría vanilla extraída ni una animación corporal nueva para los guardias.
