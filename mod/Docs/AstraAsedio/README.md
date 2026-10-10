# Astra Asedio QA v12 — plataforma baja y 12 escudos

Variante de la v11 probada por el usuario. Piso a **2 m** (140 unidades), antes 6,485 m. Habitación, puerta, paredes y techo inferior eliminados. Escalera corta de 11 peldaños con la pendiente anterior; fundación y riostras nuevas, sin aplastar ni adelgazar los troncos. Ballesta y puesto bajan 313,95 unidades junto al piso.

**12 escudos** en cada torre (laboratorio y mundo), antes cinco. La cara decorada mira hacia afuera y los agarres quedan apoyados contra madera medida del NIF final. Distribuidos fuera del desembarco de la escalera.

La ballesta, virote, DLL, PEX, PSC y SEQ conservan exactamente los bytes del paquete v11. El ESP conserva los IDs de las referencias existentes, VMAD, funcionamiento del arma, cofre, terreno y overrides vanilla. Se cambian la torre, referencias de estructura y escudos, altura de las dos referencias de ballesta y NAVM/NAVI del laboratorio.

## Instalación en MO2

1. Instalar `AstraAsedio_QA_v12_Baja_MO2.zip` como un mod nuevo.
2. Desactivar la versión Astra v11/v10 y activar solamente v12. Mantener SKSE y Address Library del perfil que ya funcionaba.
3. Probar con una partida nueva de prueba. Una partida anterior puede conservar posiciones y estado de las referencias cambiadas; el paquete v11 queda conservado para volver atrás.
4. Ejecutar Skyrim SE 1.6.1170 mediante SKSE64. Los masters siguen siendo Skyrim.esm, Update.esm y Dawnguard.esm.

No hace falta modificar Skyrim.esm, archivos del juego ni INI. El ZIP contiene solamente el mod y documentación, sin carpeta contenedora.

## Dónde y cómo probar

- `cow Tamriel 1 -4`: misma ubicación y giro de la v11, cerca de Whiterun.
- `coc AstraAsedioTest`: laboratorio con la misma variante baja.
- Tomar virotes del cofre, subir la escalera y activar la manivela. E entra/sale de la mira, ratón apunta, Ataque dispara y Sprint alterna Individual/Continuo.

Comprobar el contacto de los escudos desde un costado, la subida sin trabas, alcance de la manivela y disparo bajo en diferentes orientaciones.

## Apuntado y límites

Se conserva la inclinación de **−5° a +80°** del mecanismo probado. A −5°, la prolongación recta del eje del virote llega a un suelo plano a unos **53 m** del centro, antes unos **104 m**. Es una comparación geométrica: no incluye gravedad, relieve ni la corrección de la mira a 75 m. La altura nueva ayuda a apuntar a blancos bajos y cercanos, pero no permite apuntar directamente al suelo inmediato bajo la torre.

La navegación nueva corresponde al laboratorio. La ruta física del mundo usa la misma geometría y transformación rígida; la navmesh y LOD vanilla del exterior siguen siendo los de v11.

## Validación

Pasaron controles sobre archivos exportados/reimportados: ruta hasta el puesto (162 muestras), navegación conectada (313 triángulos), contacto y orientación de 12 escudos, 30.960 poses de tiro sin choque y comparación binaria de los registros que debían conservarse. El parche del ESP debe repetirse con resultado idéntico.

**v12 pendiente de prueba en Skyrim.** Estos controles de archivos, colisión y renders no ejecutan el motor del juego. Los informes v01–v11 conservados en el proyecto son históricos; los vigentes para esta variante son `reports/plugin_v12.json`, `route_v12.json`, `shields_v12.json`, `shot_clearance_v12.json`, `aim_height_v12.json` y `package_qa_v12.json`.

## Reconstrucción

En el proyecto v12: Python `scripts/prepare_v12.py --deck 140`; Blender 4.4/PyNifly `scripts/build_tower_v12.py`; Blender `scripts/fit_shields_v12.py`; Python `scripts/patch_plugin_v12.py`; Blender `scripts/verify_route_v12.py`; Python `scripts/verify_shot_clearance_v12.py`; Blender `scripts/render_v12.py`; Python `scripts/package_v12.py`.

El parche toma el ESP intacto de la carpeta hermana v11. `source/Torre_baja_v12.blend` permite editar la torre propia; las mallas/texturas vanilla usadas para medir y renderizar no se distribuyen.
