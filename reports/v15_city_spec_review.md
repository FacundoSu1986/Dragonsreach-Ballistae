# Revisión independiente de integración de ciudad v15

Fecha: 2026-10-09. Revisión de sólo lectura del ESP final WhiterunTorres, VMAD, fuentes Station/Guard, archivos propios y certificados geométricos. Únicas escrituras del revisor: los tres informes SPEC autorizados. No se modificaron plugins, PSC/PEX, NIF, runtime, MO2 ni vendor. No se lanzó Skyrim ni se volvió a exportar geometría.

## Dictamen

**APROBADO el alcance estático de integración revisado, sin hallazgos P1/P2 abiertos después de corregir el límite del solver Guard.** Hay dos puestos de ciudad propios con control compartido, referencias coherentes y límites por sesión. El certificado no acredita paso real del jugador/patrulla, animación, navegación AI, latencia o disparo en Skyrim. El acceso este usa una aproximación de subir escalones que requiere prueba de motor.

Las aprobaciones nativa y de coordinación corresponden a v15_native_spec_review.md y v15_station_spec_review.md. La API final es 4 y la DLL 3.5.0; la fuente Station preflight y la recuperación Guard consultan esa barrera antes de tomar/escribir la escena.

## Plugin y VMAD reales

Se parseó el ESP entregable, además de revisar el generador. Sus masters son, en orden, Skyrim.esm, Update.esm, Dawnguard.esm y AstraAsedio.esp. Contiene 16 records: dos NPC_, dos STAT, dos ACHR, ocho REFR, un WRLD y un CELL. Los únicos FormID ajenos al índice propio 04 son WRLD 0000003C y CELL 00000D74, usados como contexto. No contiene LAND/NAVM/NAVI/PACK ni overrides de referencias vanilla. Los destinos de patrulla 00078784 y 0007878A y las torres existentes no están entre los records escritos.

Ambas armas, 04000B40 y 04000B50, usan base ACTI 03000B02 y scripts hermanos AstraAsedioStation/AstraAsedioGuard. Station.Guard apunta al mismo Self; Artillero, Puesto y Standby apuntan respectivamente a Self+1, +2 y +3. Son referencias propias persistentes, como las armas y plataformas. Las plataformas apuntan a los STAT propios 04000B60/61 con rutas exactas `AstraAsedio\voladizo_este.nif` y `AstraAsedio\voladizo_oeste.nif`; ambos archivos existen en el complemento.

Las propiedades Session/Launcher/ShotAmmo/SteelBolt/ShotSound del jugador coinciden con el núcleo. Se comprobó además que las referencias de núcleo resuelven a QUST/WEAP/AMMO/SOUN/ACTI del tipo esperado. El guardia conserva su ShotAmmo dedicado 03000B01, válido en el core, y CadenceSeconds=2,5. El jugador conserva CycleSeconds=1, ReleaseSeconds≈1/15 y UseSightCamera=true. El coste SteelBolt y el éxito por ProjectileHandle se verifican en la revisión nativa.

Cada VMAD asigna tanto al jugador como al guardia YawCenter=0, YawHalfSector=60 y PitchMin/PitchMax=−20/80. AllowPlayerTakeover=true habilita la validación extendida del guardia. El núcleo y Atalaya, incluidos ballesta.nif y torre.nif, son byte por byte iguales a v14; el sector de ciudad se pasa a la sesión, por lo que no limita globalmente el giro 360 del núcleo.

Las posiciones DATA del ESP coinciden con las mediciones, con error máximo menor que 0,003 unidades por float. Armas y plataformas tienen rotación cero y escala unitaria; NPC/markers se orientan 180°. Artillero y Puesto coinciden con operator_local_foot y Standby con standby_local_foot.

| Sitio | Arma en mundo | Operador local, pies | Espera local, pies |
|---|---|---|---|
| Este | 17801,74; −8824,61; −3544,014 | 124; −356; 71,646 | −210; −280; 71,646 |
| Oeste | 15225,56; −8726,52; −4128,014 | 124; −276; −0,354 | −210; −220; −0,354 |

El artillero propio se retira al Standby propio antes de admitir al jugador y vuelve al Puesto al liberar el lease. No se crea una ruta AI nueva ni se mueve la patrulla vanilla. Una consulta adicional a los triángulos NAVM del contexto original, para el centro y ocho puntos del perímetro de radio 18 de cada huella operador/Standby, no encuentra superficie original del corredor superior en ninguno de los cuatro emplazamientos. Esta consulta es muestreada; no prueba una ruta de motor.

## Hallazgo de integración corregido

**P1 corregido:** el VMAD final configuraba PitchMax=80 mientras AstraAsedioGuard sólo aceptaba valores −20..45 al resolver un objetivo. Eso rechazaba todos los objetivos de ambos puestos, incluso objetivos de suelo dentro del sector. La fuente final calcula certifiedPitchMax=80 únicamente con AllowPlayerTakeover; mantiene 45 en legacy. El test nuevo ejecuta el solver Guard real con PitchMax=80 después de reservar/preparar/liberar al jugador y acepta el objetivo de suelo. Se revisaron fuente y compilación global actuales; no queda abierto este hallazgo.

## Evidencia geométrica y límites

Se inspeccionó verify_platforms_v15.py y su certificado final. El proceso registrado reimporta los NIF exportados y mide sus mallas visuales/Havok. Los hashes de ambos NIF, todos los inputs identificados por el certificado y el enlace modular→certificado coinciden con los archivos actuales. Las tablas NPZ reimportadas contienen 5040/396 triángulos visuales/Havok para este y 4030/228 para oeste, coherentes con el certificado. El revisor no repitió el export/reimport de Blender.

El muestreo de cápsula usa radio 18 y altura 128. Compara los centros NAVM a 4 unidades que ya eran utilizables antes de añadir la plataforma y conserva el destino original de cada patrulla. La evidencia registra 2259 centros originales utilizables en este y 1641 en oeste, **3900 en total, cero pérdidas**. No prueba todos los puntos continuos de NAVM ni el movimiento de actores reales.

En cada plataforma se verifican 525 poses estáticas a intervalos de 5°: yaw −60..60 y pitch −20..80. El certificado registra cero contactos del arma y cero intersecciones del segmento inicial de proyectil con plataforma/entorno en esas poses. La holgura mínima de ese segmento es 6,038 unidades en este y 6,056 en oeste, frente al umbral de 2,205 del comprobador. No se midió la envolvente continua entre muestras, las fases Fire/Reset ni la trayectoria balística completa. El margen mínimo de la cápsula frente al arma es 22,201 para el operador y 62 para Standby en ambos sitios.

| Medida registrada | Este | Oeste |
|---|---:|---:|
| Altura añadida del deck sobre piso original | 72 u | 0 u |
| Gap máximo de los 81 apoyos de base fija | 0,00434 u | 0,02536 u |
| Muestras de ruta de acceso | 181 | 119 |
| Margen mínimo frente al entorno original | 2,381 u | 43,472 u |
| Margen mínimo frente a colisión propia | −13,615 u | 8,005 u |
| Desnivel máximo de la aproximación de paso | 20,008 u | 0,02536 u |

El margen negativo este es una excepción expresa de la cápsula frente a las contrahuellas; no significa una ruta libre de contactos. Sus cuatro elevaciones son 20/20/20/12 unidades y las primeras huellas tienen sólo 10 unidades de profundidad. El comprobador admite esos contactos en la región de escalera y exige soporte dentro de ±20,15 u. Es un candidato geométrico de subida de escalones pendiente de probar en Skyrim, no una certificación de acceso usable. Oeste ofrece una ruta geométrica plana con margen positivo en las muestras registradas.

Las dos diagonales por plataforma conectan anclajes de paredes reales identificados por el contexto con vigas exteriores. Las barandas dejan la apertura de acceso. El apoyo, las uniones y la colisión son evidencia geométrica; no se atribuye capacidad estructural física al NIF.

## Verificación independiente fresca

Se ejecutó pytest con `-B` y `-p no:cacheprovider`, sin escribir bytecode/caché:

- Station + takeover + placements + platforms: **78 passed**.
- Guard + sector legacy + takeover: **109 passed**. Estas suites comparten algunos tests y no se suman como casos únicos.
- Parseo directo de masters, records/VMAD/DATA, tipos de referencias de core y hashes: sin discrepancias.
- Los seis scripts del receipt global plugin_compile.json coinciden en fuente, PEX y disassembly; compiler/assembler exit code 0.

No se usó como evidencia de PEX actual el recibo enfocado Station previo que quedó superado por la compilación global. El dictamen nativo final corresponde a 2337 aserciones y DLL efe94edd…; sus detalles y límites de mutex/reentrancia están en el informe nativo.

## Identidad del resultado revisado

| Archivo | SHA256 |
|---|---|
| addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp | 0c593986e305ea2e88cd0b4885de603e185153b93b90dd0e67633d079db156d0 |
| addons/WhiterunTorres/meshes/AstraAsedio/voladizo_este.nif | 582041e32f52c4392583a62f0193cb9c1c09f6644963093d8b26d89cd7dd65c5 |
| addons/WhiterunTorres/meshes/AstraAsedio/voladizo_oeste.nif | 968da3de9fef848fe7bd7489690a97aee09659e9b43ff1e6e41809b8ca81876c |
| reports/platforms_v15.json | dc9db170a75c68ecd8b53d3da727b17eab0cf24dada81049a4430aec1e3534f4 |
| reports/modular_v15.json | 0e8f5fa1a690970d41cdeaf0c098b47d6dfad6f9db41f4b1086aea66525a31fa |
| scripts/build_modular_v15.py | e654021af8786bb4c2215de787436a74535a948919a3a5b59798dffa47356106 |
| mod/scripts/source/AstraAsedioGuard.psc | 56c35479fc8a0c5a54332dced946da2f6e264c024b7175fd07f4c6fece3630fb |
| mod/scripts/source/AstraAsedioStation.psc | 643d203b5a1b4b2691c13d8c50128aa924b0262b609372f089f711539773b42e |
| reports/plugin_compile.json | 4e2f75b9a89c5babd6f60b645906bd26e8c6f13614679651a080629204a6cc31 |
| reports/platform_este_v15.npz | eaf2ada35d717dc320d86a67e69fe6a53b67f5d716f95fdc91a52c5abd1a3ac3 |
| reports/platform_oeste_v15.npz | 0bf07e380f6127a120653c4c9edd93ea2cd31b113e3c86d8da72a9d6d81fe2fa |
| reports/gun_havok_v14.npz | 8bcf69e0e7bbb72b206153ffc72045eee6f7a39beb2fa0ae13ea8acd3ca1ea7a |
| reports/tower_geometry_este_v14.npz | e7338ffa737ac8ad244cd9528b6b433c5f591f48407d988edbecece09b87d28c |
| reports/tower_geometry_oeste_v14.npz | 562ae0a2677a68dc23bd17cfc3014ad068076ba5b4fd334cff2dbbc06091be44 |

El manifiesto modular declara que la migración de un save con la ciudad anterior no está soportada y requiere un save de prueba nuevo. Patches de ciudades/mods terceros siguen diferidos. Antes de afirmar verificación de motor quedan pendientes: acceso completo de ambas rutas, patrulla original caminando, cápsula real de jugador/NPC, takeover y retorno, guardar/cargar/descargar durante reservas, animaciones, audio, autoría/daño del proyectil y rendimiento/latencia reales.
