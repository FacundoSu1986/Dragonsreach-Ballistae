# Política de Propiedad Intelectual y Contenido de Terceros

## Deslinde de Responsabilidad Legal
*Skyrim, The Elder Scrolls, Skyrim Special Edition, Creation Kit, Bethesda Game Studios y Bethesda Softworks son marcas comerciales registradas y propiedad de ZeniMax Media Inc.*

Este proyecto es una creación original de la comunidad técnica y no está afiliado, respaldado, auspiciado ni aprobado de ninguna manera por Bethesda Softworks ni ZeniMax Media Inc.

---

## Regla de Cero Tolerancia para Archivos de Terceros / Bethesda

1. **Sin redistribución de archivos protegidos:**
   - Queda estrictamente prohibido incluir en este repositorio cualquier archivo perteneciente a Bethesda (`.esm`, `.bsa`, `.ba2`, `.dds`, `.hkx`, `.fuz`, etc.).
   - Toda textura visual utilizada por los modelos del mod hace referencia a rutas estándar del motor vanilla de Skyrim SE en tiempo de ejecución (referencias relativas en los bloques de materiales NIF), de modo que el mod requiere una copia legítima del juego instalada y **no redistribuye contenido bajo copyright**.

2. **Código y Artefactos Originales:**
   - Los modelos 3D (`source/*.blend`) son de autoría original propia.
   - Los scripts Papyrus (`mod/scripts/source/*.psc`) y scripts de soporte Python (`scripts/*.py`) son código abierto y original del proyecto.
   - La librería nativa C++ SKSE (`native/`) es código original desarrollado con dependencias licenciadas bajo MIT/BSD (CommonLibSSE-NG, spdlog, fmt, rapidcsv) cuyos avisos de licencia residen en `native/licenses/` y `mod/Docs/AstraAsedio/Licenses/`.
   - **Excepción acotada de animación:** los clips del guardia (`source/anim/*.hkx` y `addons/GuardAnim/**/*.hkx`) son de autoría original propia. Se hornean con `scripts/build_guard_bajada.py` a partir de poses autoradas sobre el rig de terceros *NickNak Rig 5* (que **no** se redistribuye) y se retargetean al `skeleton.hkx` de ese mismo rig; no contienen datos extraídos de Skyrim. Se versionan pese a la extensión `.hkx` por ser contenido propio en formato de Bethesda, exactamente igual que los `.esp`, `.pex` y `.dll` del proyecto. La prohibición general sobre `.hkx` (§1) sigue vigente para cualquier otro archivo.

3. **Verificación Automatizada:**
   - Este repositorio cuenta con un hook de pre-commit y verificación defensiva en `.gitignore` para bloquear de forma inmediata cualquier intento accidental de añadir activos de Bethesda.
