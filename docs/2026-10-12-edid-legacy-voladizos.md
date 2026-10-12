# EDID propio para el juego legacy de los voladizos — 2026-10-12

Cambio de **datos** sobre `addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp`, más el generador que lo produce. No toca FormID, bases, colocación, VMAD, flags, scripts ni binarios.

## Qué se hizo

Los dos juegos de contenido de cada voladizo (legacy `0xB40–0xB54`, copiado de la baseline v16; vigente `0xB70–0xB84`) se crearon con el mismo literal `AstraVoladizo*`, así que el plugin repetía diez EDID. No era un fallo funcional — el legacy nace `Initially Disabled` (`0x800`), es persistente y sólo existe para desactivarse en partidas anteriores a v17 — pero ensucia el `Check for Errors` de xEdit, que sigue pendiente en `docs/nexus/RELEASE_STATUS.md`.

El juego legacy pasa a llamarse:

| FormID | EDID nuevo |
|---|---|
| `0xB40` / `0xB50` | `AstraLegacyVoladizo{Este,Oeste}Ballesta` |
| `0xB41` / `0xB51` | `AstraLegacyVoladizo{Este,Oeste}Guardia` |
| `0xB42` / `0xB52` | `AstraLegacyVoladizo{Este,Oeste}Puesto` |
| `0xB43` / `0xB53` | `AstraLegacyVoladizo{Este,Oeste}Espera` |
| `0xB44` / `0xB54` | `AstraLegacyVoladizo{Este,Oeste}Plataforma` |

El puesto vigente conserva su nombre: es el que citan los scripts, el runtime nativo (`native/src/GuardRuntime.cpp`) y la documentación vigente.

## Piezas

- `scripts/patch_legacy_edids_v29.py` — reescribe **sólo** el subrecord `EDID` de esos diez refs sobre el ESP publicado, sin volver a correr el pipeline, y verifica que nada más cambia. Uso: `python scripts/patch_legacy_edids_v29.py`.
- `scripts/build_modular_v17.py` — el bloque que preserva el legacy aplica el mismo renombrado, para que una regeneración completa produzca este mismo archivo.
- `tests/test_v29_edid_uniqueness.py` — contrato permanente: ningún plugin empaquetado repite EDID, y el legacy sigue persistente+apagado sobre `0x0B02` mientras el vigente sigue despierto sobre `0x0B04`.
- `reports/legacy_edid_rename_v29.json` — sha256 antes/después y mapa de renombrados.

- ESP antes: `fabe09b28a3b1c3559b965242f85a6f42e95a7f784e5db6e7068be8b0db63b3b`
- ESP después: `cfccc9cd6bd24ff5a2bd8b5a0670b89efc3ff6f87c9428b14d8087e5975de818`

## Por qué no se borró el legacy

Se evaluó y se descartó. Esos refs conservan la reparación de partidas anteriores a v17: `AstraAsedioPlayerAlias.StartCityRetirement()` → `RetireLegacyCity()` corre en `OnInit` y en `OnPlayerLoadGame`, espera a que los efectos nativos estén quietos (`IsEffectsQuiescent`) y a que el controlador viejo drene (`RetireStation()`), y recién entonces desactiva los cinco refs de cada juego. Borrarlos dejaría referencias persistentes colgando en guardados viejos y rompería `tests/test_v17_city_upgrade.py` y `tests/test_effects_quiescent_guard.py`. La convivencia de los dos juegos no es un residuo: es contrato.

## Verificación ejecutada

| Comprobación | Resultado |
|---|---|
| `tests/test_v29_edid_uniqueness.py` antes del cambio | 3 fallos, con el diagnóstico exacto (`EDID repetido AstraVoladizoEsteBallesta en 04000B40 y 04000B70`) |
| El mismo test después | 3/3 OK |
| Paridad generador ↔ parche | 10/10 registros legacy byte a byte idénticos; ningún otro registro del plugin cambia |
| Invariantes del parche | FormID, firma, flags (`0x400|0x800`), base `NAME`, datos y VMAD intactos; cabecera TES4 y orden/conteo de registros intactos; EDID único en todo el plugin |
| Suite `unittest discover` (runner de las puertas de release) | 387 tests, mismos fallos preexistentes que el árbol sin el cambio (diff de ids vacío) |
| Suite con `pytest` | 387 pasan / mismos fallos y errores preexistentes que el árbol sin el cambio (diff de ids vacío) |
| `native/tests/guard_binding_tests.py` | PASS (el binding real del addon con el core sigue resolviendo) |

Nada de esto es prueba en el motor: los cinco ESP, los HKX y el NIF siguen sin validarse en Skyrim. Este cambio tampoco cambia el comportamiento en juego.

## Pendiente al reempaquetar

El ZIP publicado (`AstraAsedio_QA_v29_Unificado_MO2.zip`, sha `ac8b04d4…`) se construyó **antes** de este renombrado, así que su copia del ESP quedó desactualizada: hay que volver a correr `python scripts/package_v29.py` (y `scripts/verify_zip_v29.py`) y anotar el sha nuevo en `docs/README_v29.md` y `PRUEBAS_EN_JUEGO.md`. `reports/modular_v17.json` conserva el sha previo por la misma razón: refleja el build de v17 que se ejecutó en la máquina del autor.
