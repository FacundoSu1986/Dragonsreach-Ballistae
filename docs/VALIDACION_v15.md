# Evidencia de QA v15

La entrega se verificó fuera del motor. No se ejecutó Skyrim ni el planificador real de Papyrus; `in_game_verified=false` en los recibos actuales.

| Comprobación | Resultado / alcance |
|---|---|
| DLL real | Compilación MSVC x64 nueva, AstraSight 3.5.0/API 4, runtime 1.6.1170, SKSE mínimo 2.2.8, PE/exports revisados |
| C++ portable | Seis ejecutables, 2.337 aserciones sin fallos; 56 específicas de v15 |
| Papyrus | Seis PSC compilados en staging nuevo por Bethesda; PEX y disassembly vinculados por SHA256 |
| Control y colocación | Fuentes PSC reales con nativas simuladas; reservas, cancelación, menús, callbacks antiguos, salida y barrera de limpieza; tipos y destinos VMAD revisados |
| Plugins | Núcleo y Atalaya idénticos a v14; ciudad con 16 registros, build idempotente, sin overrides de patrulla ni LAND/NAVM/NAVI/PACK |
| Plataformas | Dos NIF propios reimportados, piso/base apoyados y operador/guardia en operación/espera; 525 poses estáticos por puesto, en incrementos de 5° |
| Paso original | 2.259 centros utilizables muestreados en Este y 1.641 en Oeste; 0 centros perdidos, incluidos ambos marcadores vanilla |
| Arma y Atalaya | NIF conservados de v14; revisión de materiales/texturas, nodos, secuencias y colisión sobre archivos actuales; 39.262 triángulos visuales y 1.256 de colisión en los tres NIF del núcleo |
| ZIP | Inventario exacto, CRC, ausencia de rutas duplicadas y SHA256 de cada entrada contra el payload final |

El registro del disparo distingue evento admitido, secuencia y lanzamiento; cuenta el coste sólo cuando se retira exactamente un virote y el handle de salida resuelve a un proyectil. Un fallo de lanzamiento intenta compensar el consumo y registra el resultado. Las pruebas de inventario son simuladas; las funciones del motor provienen de la CommonLib fijada, no de un stub de DLL.

La limpieza nativa devuelve el arma a pose neutral, espera a que terminen los efectos sobre su escena original y sólo entonces permite liberar controles y devolver el puesto al guardia. La adquisición de escena anterior al armado también queda vinculada al ticket para limpiarse. Las revisiones independientes de especificación y calidad resolvieron los casos de cancelación durante inventario, descarga de 3D, congelación tras un fallo de Fire y salida anterior al armado.

La revisión de ciudad detectó además un traslado de recuperación del guardia que podía terminar después de admitir al jugador. Ahora mantiene la exclusión hasta retornar. Cuatro regresiones nuevas fallaron antes del cambio y pasan después. La pasada independiente de ciudad se interrumpió por límite de uso tras comunicar el hallazgo; el agente principal realizó la corrección y el cierre final documentado en `v15_city_quality_closure.md`. El paquete no presenta ese cierre como una aprobación independiente final de todo el mod.

El acceso Este usa una subida de escalones de hasta 20 unidades y peldaños laterales cortos. La prueba geométrica interpola una maniobra de subida y registra contacto con los propios risers; **no es un certificado de cápsula libre en todos los puntos ni una prueba de tránsito real**. El acceso Oeste tiene margen positivo contra la colisión exportada. Ambas plataformas tienen Havok y no añaden NAVM. La IA propia se coloca directamente; el paso de las patrullas existentes sigue pendiente de motor.

También quedan pendientes: clic físico→imagen, dirección/origen/daño/autoría reales del proyectil, Fire/Reset/sonido, animaciones y postura del guardia, guardado/carga durante transferencias y compatibilidad con geometrías de otros mods. La geometría estática vanilla y los renders no cubren barridos de toda la animación ni obstáculos añadidos por otros mods.

Recibos actuales: `verification_v15.json`, `native_build_receipt.json`, `native_artifacts_verified.json`, `native_binary_checks.json`, `plugin_compile.json`, `assets_verified.json`, `platforms_v15_build.json`, `platforms_v15.json`, `modular_v15.json` y `package_qa_v15.json` en el proyecto. Los informes v11–v14 conservados son históricos y no sirven como evidencia nueva de v15. El recibo enfocado de Station fue reemplazado por la compilación global final.
