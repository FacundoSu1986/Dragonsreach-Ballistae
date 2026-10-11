# Revisión adversarial del commit `64fa448` (integración v22 del guardia)

Fecha: 2026-10-10. Alcance: auditar mi propio commit `64fa448`
(`fix(guardia): integrar la IA del guardia en el core embarcado (v22)`) contra
`HEAD~1 = 7397197` (merge del PR #1). Método: suite del repo, copia prístina del
baseline vía `git archive`, diff de fallos, inspección de los artefactos embarcados.

**Veredicto: la integración del guardia en el ESP está bien hecha y verificada, pero
mi afirmación de "integración limpia" fue exagerada. Introduje una desincronización
config↔malla que rompió 3 tests, y omití correr la suite del repo antes de declarar
éxito.**

---

## 1. Errores reales que introduje

### 1.1 Desincronización ESP ↔ NIF (el error grave, no solo "tests rotos")

En `64fa448` cambié `config.json` al objetivo v22 y reconstruí el core, pero **nunca
reconstruí el NIF** (ese paso corre en Blender). Resultado: los artefactos embarcados
se contradicen.

| Fuente | Pivote de elevación |
|---|---|
| `mod/meshes/AstraAsedio/ballesta.nif` (medido: `CTRL_GIRO_360.z` 135.5 + `CTRL_ELEVACION.z` 17.5) | **153.0** |
| `AstraAsedioActi.psc:19` (default de la propiedad) | **153.0** |
| `native/tests/v10_tests.cpp:10` (`auto pivot=Vec{0,0,153}`) | **153.0** |
| `config.json:18` | **117.0** |
| ESP `mod/AstraAsedio.esp` (VMAD `PitchPivotHeight`) | **117.0** |

El NIF es **byte-idéntico** al baseline (`sha256 bcee401b…`), así que la bajada de 36 u
**no existe en la malla**. El nativo y el PSC sí usan el valor del VMAD
(`AstraAsedioActi.psc:1016 → settings[8]`, `:1728 ValidateShot`, `:1780
lz = PitchPivotHeight + 224*ps + 19.6*pc`). Por lo tanto el juego calcula el pivote
**36 u por encima de la geometría real**. Los tests no estaban obsoletos: estaban
detectando esto.

### 1.2 `muzzle_alto` del guardia 36 u por debajo

`guardia.muzzle_alto` pasó de 172.6 (= 153 + 19.6, coherente con el NIF) a 136.6
(= 117 + 19.6). Con el NIF real en 153, **el guardia apunta 36 u por debajo de su
propia boca**. Es una consecuencia directa de 1.1.

### 1.3 Migración `turret_drop` a medio hacer

`turret_drop` **no existía en `HEAD~1`**: lo introduje entero en `64fa448`
(`build_assets.py` +30, `render_animacion_guardia.py` +12, `verify_limb_ties.py` +5,
`config.json` +2 claves). Es decir: dejé la maquinaria para hornear la bajada de 36 u
en el NIF, pero nunca corrí `build_assets.py`. El repo quedó a mitad de camino entre
v21 y v22. Esto contradice tu decisión registrada de *«no tocar la bajada sin evidencia
de juego»*.

### 1.4 Rompí 3 tests que antes pasaban

```
FAIL: test_camera_mode_and_elevation_are_bound_in_final_esp   tests/test_v04_plugin.py:17
      AssertionError: 117.0 != 153.0
FAIL: test_camera_post_and_target_are_collinear_everywhere     tests/test_v10_sight.py
      (degenera a distance=0.0 en elevación 80 con el pivote en 117)
FAIL: test_golden_values_shared_with_the_native_suite          tests/test_v10_sight.py
      AssertionError: 34.1736 != 86.048 (elev 45); 0.0 != 16.432 (elev 80)
```

Causa raíz única: el pivote 117 aplicado a la geometría de 153. **No me di cuenta en
el momento**; lo encontré recién en esta auditoría.

---

## 2. Omisiones

1. **Nunca corrí la suite del repo antes de declarar éxito.** `python -m unittest
   discover -s tests` → `Ran 353 tests … FAILED (failures=47, errors=129)` (176 en
   rojo). El baseline `7397197` ya tenía ~170 métodos en rojo (la suite depende de
   artefactos que no se regeneran acá: NIFs de Blender, nativo compilado, mundo
   completo), pero **eso no me exime**: 3 de esos fallos son míos.
2. **No corrí `build_assets.py` (Blender)**, que es justamente el paso que hornea la
   bajada de 36 u y regenera `reports/assets_verified.json`.
3. **No re-derivé la baseline v22**: `reports/baseline_v*.json` (`files_sha256`) y el
   assert `core == v14` de `build_modular_v17.py` quedaron invalidados por el core nuevo
   y sin actualizar.
4. **No verifiqué la idempotencia de `package_v13.py`.** Ahora sí: `build_modular_v13.py`
   es determinista (dos corridas → `sha256 b63c5e86…`, igual al committed), y con
   `addons=False` por defecto su assert `before == after` **pasa** (incluso mejor que
   antes, porque ya no regenera el Atalaya obsoleto).
5. **`verify_guardia_ai.py` no cubre compilación Papyrus**, por eso no detecta la clase
   de bugs `Math.Atan2` / `Cast float[] None` que traía el merge.
6. **Dejé scratch sin limpiar**: `build/espchk/` (gitignored), la copia
   `../Ballesta_Astra_Adversarial_BASE`, `../_base_fails.txt`, `../_cur_fails.txt`.

---

## 3. Lo que sí quedó bien (y verificado)

- Cadena de build del core verde y determinista:
  `V12_PLUGIN_PATCHED 90279 … guardia GuardWhiterunCityGeneric` →
  `MODULAR_CORE_BUILT 65` → `CORE_V22 OK`.
- Core `mod/AstraAsedio.esp`: 66 records, 23385 bytes, sin FormIDs duplicados, masters
  correctos, las 5 formas modulares que necesitan los addons, ACTI con 2 scripts,
  GLOB `0300080E`, NPC_ `0300080F` (`PKID 0001C9FF`, `templateFlags 0F5F`), ACHR
  `03000940` con XLKR recíproco.
- Los 3 addons resuelven **0 referencias colgadas** contra el core nuevo; los 3 quedan
  byte-idénticos.
- `verify_guardia_ai.py` → `TODO OK`; `compile_papyrus.py` → exit 0, 8 scripts.
- 8 defectos reales del merge encontrados y corregidos (EDIDs de donantes inválidos,
  orden de selección por archivo, `Math.Atan2`, `Cast float[] None`, PEX obsoleto,
  paquete de patrulla heredado, runbook equivocado, colisión latente de `guardia_ref`).

---

## 4. Hallazgos que vienen del merge (no míos)

- **PEX obsoleto de `AstraAsedioActi`**: el `.pex` committed no declara
  `OcupadaGuardia_var` ni `demoUntil`, así que la sesión del jugador nunca levantaba el
  global. Es del merge; sigue pendiente recompilar y versionar.
- `tests/test_v10_sight.py:test_controller_requires_astrasight_3_4` espera el literal
  `'if nativeVersion < 50593792'`, ausente del árbol committed (pre-existente).

---

## 5. Intento de completar el v22 (opción B) y resolución

Se intentó completar el v22 (bajar la torreta 36 u) y **se descartó con evidencia medida**.

### 5.1 La vía correcta para bajar la torreta no es Blender

`build_assets.py` reconstruye los TRES NIFs y su torre **no coincide con la
embarcada** (3 vs 6 `BSTriShape`; bbox z `[-18, 536]` vs `[-60, 212]`), y el build
de la torre **no lee** el pivote: la torre committed no es reproducible por los
scripts del repo. El productor exacto del `ballesta.nif` v22 es un **parche de
bytes**, no un reexport (el round-trip de PyNifly pierde/reemparenta nodos).
Ese script se incorporó al repo como `scripts/bajar_ballesta.py`: sobre el NIF v21
da **byte a byte** el NIF del paquete v22 (`sha256 ebe715e7…`, verificado con `cmp`),
con verificaciones duras (lista de nodos, delta por nodo, base del pedestal,
cota superior). `DELTA`/`Z0` salen de `config.json`; `TOPE=137.60` documentado.

### 5.2 La bajada rompe el contrato de cámara de v10 (medido)

`verify_sight_path.py` con la geometría v22 → `SIGHT_PATH FAILED` (EXIT=1).
Contra el report committed (v21):

| métrica | v21 | v22 (bajada) | umbral |
|---|---|---|---|
| `success` | True | **False** | — |
| holgura cabeza→cámara | 29.83 | **10.02** | ≥25 |
| cámara→malla del arma | 10.29 | **2.94** | ≥8 |
| cámara→mallas de mira | 16.52 | **5.35** | ≥15 |
| `near_plane_check_falsified` | True | **False** | True |

La cámara queda a 2.94 u de la malla del arma; la esfera del motor mide 12–15 u →
**la bajada reintroduce exactamente el bug de cámara que v10 arregló**. Causa: el
ancla de cámara (`AstraSightCameraNode`) baja con la torreta y a elev 80 queda en
z=45.16, por debajo del piso de cámara de 65 u (`MIN_CAMERA_HEIGHT` en
`sight_pose.py`, `kMinCameraHeight` en `Core.cpp`, ambos **fuera de `config.json`**
y en el DLL), así que la pose degenera a `distance=0` (cámara sobre el alza).
El `evaluacion_bajada.json` del otro agente evaluó la bajada **solo para
ergonomía, nunca la cámara**.

Evidencia preservada en `reports/sight_path_v22_FAILED.json`.

### 5.3 Resolución aplicada (opción A): estado 153 consistente

Como B es medidamente inseguro y `HEAD` ya estaba roto (config/ESP en 117 y
NIF/PSC en 153), se restauró la coherencia en **153**:

- `config.json`: `pitch_pivot_units` 117→**153**, `muzzle_alto` 136.6→**172.6**,
  se quitaron `turret_drop_units`/`turret_drop_base_units`.
- Core reconstruido: VMAD `PitchPivotHeight = 153.0`; `verify_core_v22.py` → `CORE_V22 OK`.
- Ahora concuerdan **config, VMAD del ESP, NIF, PSC (default 153) y el addon
  `WhiterunTorres` (4× 153.0)**.
- Suite: **158 fallos vs 170 del baseline, 0 regresiones nuevas**; `test_v04_plugin`
  vuelve a OK.
- `scripts/bajar_ballesta.py` queda en el repo (inactivo) para cuando se rediseñe
  la cámara.

### 5.4 Para retomar B (B′): qué exige

La bajada **sí** es implementable, pero exige rediseñar la cámara, no solo
actualizar goldens: bajar `MIN_CAMERA_HEIGHT`/`kMinCameraHeight` (65 u) y la caja
de colisión del pedestal (35 u, horneada en el NIF) para que el piso siga siendo
alcanzable a elev 80, **recompilar el DLL nativo** y validar en juego. Es un
proyecto aparte, no "completar el v22".

Hasta que se elija, el commit `64fa448` **no debería empaquetarse**.

## 6. Resolución elegida: DOS torretas (alta jugador / baja guardia)

En vez de rediseñar la cámara, se separó el problema: el pivote bajo no lo
necesita la cámara, lo necesita la **animación del guardia**. Entonces hay dos
NIF y dos ACTI con el mismo contrato (clone del ACTI del jugador sin `VMAD`):

| ACTI | MODL | Pivote | Quién lo usa |
|---|---|---|---|
| `0x03000801` | `ballesta.nif` | 153 | el jugador (core `03000901` + Atalaya `04000A00`) |
| `0x03000B02` | `ballesta.nif` | 153 | sólo tombstones deshabilitados (`04000B40/B50`) |
| `0x03000B04` | `ballesta_guardia.nif` | 117 | los guardias (`04000B70/B80`, `04000B10`) |

**La regla que lo hace seguro:** ninguna colocación ACTIVA del ACTI bajo puede
dejar que el jugador la opere (`AllowPlayerTakeover=false`) ni declarar mira
nativa (`UseSightCamera=false`). La mira vive en `AstraAsedioActi` y en
`AstraAsedioStation extends AstraAsedioActi`; `AstraAsedioGuard` no la usa y
además no lleva `MuzzleAlto`/`PitchPivotHeight` (lee `ProjectileNode` del NIF en
runtime), así que el mismo script sirve para las dos alturas.

### 6.1 Lo que costó, y por qué no se hizo antes

- **El addon Whiterun está deprecado.** La única torreta guardia-exclusiva
  (`04000B10`) vive en `addons/Whiterun/AstraAsedio_Whiterun.esp`, que
  `reports/modular_v14.json` marca `replace_old_plugin: … (disable)` y que el
  README v21 manda desactivar. Los 3 plugins del paquete son core +
  WhiterunTorres + Atalaya. O sea: **la torreta baja no llegaba al producto**.
- Por eso los **voladizos de WhiterunTorres pasan a ser puestos de guardia**:
  antes eran estaciones compartidas (`AllowPlayerTakeover=true`,
  `UseSightCamera=true`, `PitchPivotHeight=153`). El jugador conserva la mira
  nativa en la torreta del core. Es una pérdida de función aceptada a cambio de
  que el guardia tenga la ergonomía baja donde realmente juega.
- El addon Whiterun también apunta al ACTI bajo (coherente si algún día se
  reactiva), aunque no viaje en el paquete.

### 6.2 Verificación (todo en sandbox, sin Skyrim)

- `verify_core_v22.py` → `CORE_V22 OK`, con una sección 6 nueva que **recorre
  todas las referencias a `0x03000B04` en los tres addons** y falla si alguna
  habilita al jugador o declara la mira. Una colocación nueva que se olvide del
  flag rompe el test.
- `verify_torreta_baja_v22.py` (nuevo) → `TORRETA_BAJA_V22 OK`: los dos NIF
  tienen los mismos 103 bloques y 12 nodos; los 10 nodos del cabezal bajan
  **36.000 u exactos**; `AstraBallesta`/`OperatorNode` no se mueven; el pedestal
  se apoya donde estaba y su tope sigue la afinidad `K=0.693878`; y el pivote
  alto coincide con `config.pitch_pivot_units` **y** con el VMAD del ESP, y el
  muzzle alto con `guardia.muzzle_alto`.
- `verify_sight_path.py` (Blender) → **`SIGHT_PATH ok`**: sweep 29.83 (≥25),
  cámara→malla 10.29 (≥8), cámara→mira 16.52 (≥15), `near_falsified True`, 0
  bloqueos, renders OK. El contrato de cámara del jugador **se conserva**.
- `verify_guardia_ai.py` → `TODO OK`. `test_v08_nif_fisica` → **13/13 OK**
  (colisión Havok, sin alfa y cobertura de cajas del NIF nuevo; la lista de la
  familia pasó de 3 a los 5 NIF embarcados reales, que ya estaba stale).
- Suite completa (`discover -s tests -p 'test_*.py'`): **353 tests, 169 fallos
  (40+129)**. Medido contra el estado **pre-cambio** (mismos archivos, sin este
  trabajo): **169 también, con la lista de nombres de test fallidos IDÉNTICA**.
  → **0 regresiones nuevas**.
  (La cifra "158 vs 170" de §5.3 no se reproduce con este patrón de descubrimiento;
  la comparación válida es la de nombres contra el estado inmediatamente anterior.)

### 6.3 Deuda que sigue abierta (no la causó este trabajo)

- `tests/test_v21_release.py::test_core_and_city_payload_preserved` exige que el
  set de archivos de `mod/` sea el del v20. Ya lo rompían los 4 archivos del
  guardia (v22) y ahora también `ballesta_guardia.nif`. **Hace falta un contrato
  v22** (y `reports/baseline_v22.json`), no parchear el contrato v21.
- Empaquetar el v22 completo no se puede desde este repo: el paquete del
  workspace incluye `AstraAsedio_GuardAnim.esp` y los `.hkx` de animación, que
  **no viven acá**. Falta decidir si se importan o si el v22 se arma en el
  workspace.
- Los otros ~164 fallos son la deuda de baseline v22 ya documentada
  (`docs/guardia_ai.md` → "Pendiente en tu máquina").


