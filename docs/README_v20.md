# Astra Asedio QA v20 — Atalaya reubicada

Esta revisión mueve la Atalaya con su ballesta, cofre y doce escudos a X 4665.54, Y -14922.81, Z -5217.81, ángulo Z 187.63, en Tamriel. Conserva los quince FormID de las referencias existentes.

El modelo de esta ubicación tiene pilotes ajustados al terreno y a los escombros vanilla, y seis peldaños adicionales en el acceso. El cofre apoya en la superficie existente. El addon deja de aplanar el LAND 0000A63D y deja de desplazar los cuatro objetos vanilla que se ajustaban en la ubicación anterior. No escribe LAND, NAVM, NAVI, paquetes de IA ni misiones.

El core, la DLL AstraSight 3.5.4/API 4, todos los scripts compilados, la cadencia y el proyectil son idénticos a v19. WhiterunTorres también conserva sus archivos de v19; el cambio experimental de los voladizos se descartó tras la prueba del usuario. No se incluye configuración de SPS ni se atribuye una causa definitiva al problema resuelto del piso.

## Instalación en MO2

Salí del juego. Instalá AstraAsedio_QA_v20_MO2.zip como reemplazo del paquete QA principal anterior. Mantené activos AstraAsedio.esp y AstraAsedio_Atalaya.esp, con el segundo después del primero. Conservá tu paquete WhiterunTorres v19 y su plugin si lo usás. No mantengas dos copias activas del paquete principal.

El paquete alternativo AstraAsedio_Atalaya_QA_v20_MO2.zip contiene sólo la colocación y su NIF. Requiere AstraAsedio.esp del core v19; en MO2 debe ganar el conflicto de archivos de AstraAsedio_Atalaya.esp sobre la copia anterior. Usá una de estas dos formas de instalar la actualización.

No es necesario borrar partidas para instalar este paquete. Para una prueba de actualización, guardá en un interior separado de la ubicación, cerrá el juego, instalá el paquete y volvé al exterior. Las referencias conservan sus identificadores; la migración de cualquier posición almacenada por una partida concreta todavía requiere comprobarse en el juego.

## Comprobación en el juego

Buscá la torre en las coordenadas indicadas. La Z indicada es el origen de construcción, debajo de la plataforma. Si usás setpos para llegar, esa posición puede quedar bajo el piso; para inspeccionar la plataforma, subí temporalmente Z a -5069.

Comprobá que la escalera permite subir y bajar sobre los escombros, que los pilotes apoyan sin huecos visibles, que el cofre es accesible y que los escudos siguen sujetos a la baranda. Activá la ballesta, probá cámara, giro, inclinación y disparo; comprobá también salida y regreso a la ubicación después de cargar una partida.

Repetí Dragon Rising / El ascenso del dragón (MQ104) con los NPC de la misión cerca de Atalaya. No editar un NAVM evita sobrescribirlo, pero una estructura nueva puede obstruir físicamente partes de la malla existente: esta revisión no certifica rutas de NPC ni compatibilidad universal con modificaciones de la zona.

## Alcance de QA

Las verificaciones offline comprueban los ESP, los identificadores y dependencias, las coordenadas y rotaciones, el modelo escrito reimportado con su Havok, el acceso geométrico, los apoyos y una rejilla de apuntado estático cada 5 grados. El contenido de los ZIP se comprueba por CRC y SHA-256. La fuente de la malla es propia; las mallas vanilla cercanas se leen sólo para medición y no se incluyen en los paquetes.

Es una actualización QA para probar. Falta comprobar en Skyrim la escalera, las animaciones, las rutas de actores, MQ104 y las partidas existentes; tampoco se anuncia validación completa en xEdit/Creation Kit ni publicación estable en Nexus.
