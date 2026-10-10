# Revisión independiente de especificación v14

**Aprobada, sin hallazgos materiales abiertos.** Revisión de los archivos definitivos antes del empaquetado; los hashes están en `spec_review_v14.json`.

- 359 tests y 162 subtests independientes exitosos (321 + 38 tests en dos comandos); 152 checks focalizados previos. El fixture adicional de boca mundial a escala 0,65 también pasó.
- Cinco PSC/PEX/desensamblados finales enlazados por SHA-256. La migración temporal invalida callbacks antiguos, conserva personalizaciones válidas y mantiene límites finitos; jugador 1 s nominal y guardia al menos 2,5 s desde el lanzamiento efectivo.
- Núcleo conserva IDs y bytes salvo las cuatro propiedades temporales VMAD. Atalaya es idéntico a v13. Los 1.000 archivos v13 permanecen idénticos al baseline; DLL y todos los bytes NIF no temporales se conservan.
- Este: escala de referencia 0,75, giro −10°/+10°, elevación −20°/+20°, 861 poses. Oeste: escala 0,65, giro −10°/+2°, elevación −20°/0°, 273 poses. Ambas bases tienen apoyo y NAVM al nivel medido; los actores y marcadores propios no se escalan.
- Dos NPC propios, seis referencias propias persistentes y sólo los overrides de destino 00078784/0007878A. Cada override cambia únicamente XYZ; cabecera, rotación, NAME, flags, vínculos y todos los otros bytes son idénticos a la referencia ganadora. No se editan LAND/NAVM/NAVI/PACK, actores vanilla ni las torres.
- Los destinos de patrulla reubicados tienen piso, NAVM y cápsulas despejadas en el barrido angular de reposo: márgenes mínimos 3,028 u y 2,861 u. Las separaciones respecto a los artilleros propios son 59,453 u y 40,856 u.
- El informe geométrico está enlazado a NIF, contexto, helper, selección, metadata, tres NPZ, fuentes vanilla y barrido de marcadores. Manifest y verificación final enlazan el informe definitivo.
- Builder, reutilización explícita de evidencia, documentación y gates del empaquetador revisados. La documentación exige partida nueva para ciudad y mantiene el complemento separado para futuros parches.

La aprobación corresponde al contrato de archivos y QA acordado. Los certificados geométricos muestrean mallas de reposo con orientación; no certifican todos los keyframes Fire/Reset ni movimiento continuo. Fixtures no ejecutan la VM Papyrus. Postura/animación humana, cadencia percibida, colisión/daño real, guardado/carga, rutas de patrulla, Guerra Civil y mods de ciudad siguen pendientes de prueba en Skyrim. El padre sella los ZIP después de esta revisión.

## Delta de calidad P2 cerrado

El inventario del empaquetador vuelve a incluir `meshes/AstraAsedio/torre_whiterun.nif`, SHA-256 `a9148ea2fa1c4d8692cbb5863425641ac888c6e9f646e443febbfd4b6b7d77b6`: el STAT heredado `03000B03` conservado en el núcleo todavía lo referencia. Se evaluó el inventario actual y se comprobó la ausencia de la exclusión. Sólo se actualizó el enlace SHA de `scripts/package_v14.py`; todos los otros bindings aprobados siguen idénticos. No se alteraron ESP, PSC/PEX, NIF ni geometría, ni se repitieron pruebas amplias. La aprobación de especificación se mantiene.
