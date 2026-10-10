# Validación v17

Fuentes, PEX, DLL y ZIP se verifican por SHA256. Se compilaron los seis scripts con el compilador y ensamblador de Bethesda, sin errores ni advertencias. La DLL nueva 3.5.2/API4 se compila con dependencias fijadas de CommonLibSSE-NG; su PE declara versión 0x03050020, runtime 1.6.1170 y SKSE mínimo 2.2.8. Los 6.012 archivos del proveedor externo no cambiaron.

Las siete suites C++ pasan 2.352 aserciones, incluidas normalización del impulso, elevación/depresión y rechazo de dirección o velocidad inválida. Las pruebas de fuentes y datos pasan 313 casos y 107 subtests. El evaluador PSC es una simulación de ramas y efectos especificados; no ejecuta la máquina virtual de Skyrim.

El complemento de ciudad tiene 26 registros: los diez originales desactivados, diez referencias nuevas y las bases/mundo existentes. Se verifican 172 propiedades VMAD con tipos y destinos, enlaces de guardia y jugador, posiciones y reproducción idéntica del complemento. No se modifican LAND, NAVM, NAVI, PACK ni referencias de patrulla vanilla.

Los NIF, el núcleo ESP y Atalaya ESP son idénticos a v16. Se conserva la certificación geométrica v15 porque las mallas y sus entradas son idénticas; no es evidencia de activación o migración en el motor. Se verifican los 576 archivos de la base v16 preservada.

Diagnóstico: los archivos instalados coinciden con v16. Papyrus conserva activación/adquisición del jugador en Atalaya y cancelaciones previas a la entrada en ciudad; no proporciona el motivo de estas últimas. No había una partida reciente accesible en las ubicaciones inspeccionadas. Los enlaces guardados son una hipótesis; los puestos nuevos evitan depender de su actualización. La regresión de preparación tardía sí se reproduce con la fuente PSC. La velocidad del motor antes de la corrección no fue medida; v17 la registra.

La API usada para crear el proyectil, leer sus datos de movimiento y su velocidad compuesta se comprobó en el SDK local fijado y en las [fuentes de CommonLibSSE-NG](https://github.com/CharmedBaryon/CommonLibSSE-NG/blob/main/src/RE/P/Projectile.cpp). La asignación se limita al proyectil que acaba de lanzar Astra; no altera velocidades globales.

No se cargó esta DLL en Skyrim ni se ejecutaron las pruebas en juego. La revisión final es del agente principal y cubre construcción, código y evidencias locales; no es una revisión independiente.
