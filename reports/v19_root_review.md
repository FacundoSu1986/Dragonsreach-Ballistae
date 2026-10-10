# Revisión adversarial de Astra Asedio v19

**Resultado: candidata aprobada para QA fuera del juego. No aprobada todavía como publicación estable de Nexus.** No se publicó contenido ni se modificaron la instalación, el perfil MO2 o los saves del usuario. Los paquetes públicos son candidatos limpios, separados del QA.

## Cambio del parpadeo

La cesión guardia/jugador deja de reproducir el Reset de la referencia completa mediante PlayGamebryoAnimation. DLL 3.5.4/API 4 aporta ResetIdleScene, que asienta la secuencia existente al final, protege identidad de escena y rechaza propietarios o limpieza pendientes. Papyrus espera ese resultado antes de entregar el puesto. La función no se permite desde tasklets. Una DLL anterior no recibe la llamada nueva: el chequeo de versión la bloquea antes.

Esto es una hipótesis dirigida al momento de la cesión; los logs no demuestran la causa visual exacta. **El parpadeo de v19 no fue comprobado en Skyrim.** El usuario ya confirmó funcionamiento de cámara y vuelo de v18, y sus logs muestran proyectiles a velocidad inicial 5.400 y movimiento posterior. Esa evidencia no corresponde a una ejecución de v19 ni certifica el disparo Papyrus de los NPC.

## Hallazgos y decisiones

| Severidad | Hallazgo | Estado y evidencia |
| --- | --- | --- |
| Alta | Launcher.Fire del guardia podía terminar después de entregar el puesto al jugador | Corregido: sceneBusy abarca la llamada y su compensación. Regresión roja reprodujo preparación prematura; las pruebas actuales impiden preparación hasta que drene Fire y rechazan la reserva anterior si ocurre OnLoad/OnUnload. |
| Media | PEX exponía usuario y equipo del compilador | Corregido: se anonimizan sólo esos campos; cabecera/timestamp y tablas ejecutables se conservan. Los seis PEX finales se desensamblaron y los ZIP vuelven a validar su cabecera. |
| Media | README nativo mezclaba versiones históricas y exigía rutas privadas | Corregido: 3.5.4/API 4, receta CMake con dependencias fijadas, límites y alcance C++/PSC. El ZIP de fuente no promete regenerar ESP/NIF/BLEND. |
| Media | CMake imponía el prefijo español de MSVC a cualquier equipo | Corregido: autodetección por defecto y override explícito sólo en el helper local. Compilación y nueve CTest posteriores aprobados. |
| Media | Atalaya cambia LAND sin adaptar NAVM exterior | Contenido excluido de los paquetes públicos. 59 centros de triángulos difieren más de 15 unidades; ejemplo: un triángulo quedó 89,53 unidades bajo el terreno. QA conserva el addon experimental por continuidad. Requiere ajustar y finalizar la navegación en CK. |
| Media | WhiterunTorres conserva WRLD Tamriel 0000003C y CELL persistente 00000D74 con ajustes vanilla | Pendiente. Puede revertir clima, agua, mapa y ajustes de celda de otros mods. No se improvisó una eliminación de padres que pudiera borrar referencias hijas. Hace falta limpieza soportada por xEdit, recarga y verificación de hijos/FormIDs; documentado en los candidatos públicos. |
| Media | Mínimo SKSE 2.2.8 excluye instalaciones 2.2.6 del mismo runtime | Restricción de soporte retenida y documentada. Las interfaces existen en 2.2.6, pero esa versión no se probó con esta DLL. No se presenta como necesidad de una interfaz nueva. El log local confirma 2.2.8; se identifica el archivo Steam anterior de la página oficial de SKSE. |

Revisores independientes: lógica nativa/corrección, API/compatibilidad y documentación/publicación. Sus informes individuales se conservan en esta carpeta; el cuadro registra la disposición final del responsable sobre los hallazgos de esa ronda.

## Verificación actual

* 287 pruebas Python y 107 subpruebas aprobadas; intérprete de fuente PSC, no la VM del juego.
* Nueve ejecutables nativos: 2.376 assertions aprobadas; PE AMD64, exportaciones y metadatos 3.5.4/API 4 comprobados.
* Seis PSC recompilados desde staging, anonimizados, desensamblados y validados. Fuente, PEX y desensamblado asociados por SHA256.
* 172 propiedades VMAD con tipos y referencias comprobados; tres ESP y geometría sin cambios respecto de v18. FormIDs B70/B80 retenidos y referencias antiguas retiradas conservadas.
* Geometría de los dos voladizos validada contra muestras de navegación/collision vanilla; sin centros de navegación perdidos en ese muestreo. No sustituye navegación de CK ni prueba NPC en juego.
* 631 archivos de v18 y 6.012 entradas de dependencias externas preservados por hashes. El gate actual no usa una prueba histórica como evidencia de código cambiado.
* Cinco ZIP comprobados por CRC, inventario y SHA256: dos QA, Core público, Whiterun público y fuente. Públicos sin Atalaya, BLEND, masters, SDKs, saves, logs internos, configuración privada ni versiones documentales anteriores. Licencias CommonLibSSE-NG, spdlog/fmt y rapidcsv conservadas.

## Puertas de salida pendientes

1. Probar v19 en ambas estaciones: desaparición completa al entrar/salir, guardia disparando, repetición, cámara, vuelo, virotes, daño, regreso del guardia, menús, muerte y carga de partida/celda. Validar disparo NPC por separado.
2. Completar Check for Errors y limpieza de padres en xEdit. Dos intentos CLI con copias aisladas no terminaron; **no hay aprobación de xEdit**. Todos los originales permanecieron iguales. El script leído sólo llama Check, sin editar registros.
3. Finalizar y verificar en CK cualquier NAVM custom que se publique como contenido jugable. Core conserva el laboratorio de desarrollo con NAVM pendiente; no se ofrece como destino jugable. Atalaya permanece excluida hasta corregir LAND/NAVM exterior.
4. Probar una instalación limpia y migración de una copia de v18; confirmar descarga oficial SKSE 2.2.8, redistribuible C++ y comportamiento con mods representativos de cámara/Whiterun antes de afirmar compatibilidad.

No se ofrecen parches de city overhauls todavía. Los conflictos de colocación y de WRLD/CELL se distinguen en la documentación; tener voladizos no implica compatibilidad universal.

## Publicación y derechos

Los candidatos tienen disposición Data-root para MO2/Vortex, dependencias e instalación separadas, idioma español declarado, changelog actual y límites. Se identifica el carácter explosivo de los proyectiles y la falta de promesa de protección a aliados. Teclado/ratón requeridos; gamepad no soportado en el disparo rápido. Sprint cambia tiro individual/continuo, no cámara.

Los archivos públicos no incluyen datos personales en cabeceras PEX. La DLL conserva algunas cadenas diagnósticas de rutas del checkout SDK; eso se declara explícitamente y no se promete ausencia absoluta de rutas binarias. No se redistribuyen executables del juego ni SDKs. Mesh/physics/material donors Bethesda deben conservar su alcance Skyrim; no todos los datos son originales.

El autor debe establecer permisos reales de redistribución y etiquetar el uso de IA en código/documentación. El borrador usa [buenas prácticas de Nexus](https://help.nexusmods.com/article/136-best-practices-for-mod-authors) y [reglas de envío](https://help.nexusmods.com/article/28-file-submission-guidelines). No sustituye los derechos del autor por créditos. Requisitos se apoyan en [SKSE oficial](https://www.nexusmods.com/skyrimspecialedition/mods/30379?tab=files), [Address Library](https://www.nexusmods.com/skyrimspecialedition/mods/32444) y [Microsoft C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170).

Artefactos: `reports/verification_v19.json`, `reports/package_v19.json`, `dist/nexus/MANIFEST.json`, `docs/NEXUS_PUBLICACION_v19.md` y `docs/nexus/RELEASE_STATUS.md`.
