"""Evidence-derived release notes; portable tests are not engine validation."""
import json
def make_validation(root,assets,count,profile,camera,elevation,build):
    anchor=json.loads((root/'reports/sight_anchor_verified.json').read_text())
    native=json.loads((root/'reports/native_build_receipt.json').read_text())
    sight=json.loads((root/'reports/native_sight_behavior.json').read_text())
    compiler=json.loads((root/'reports/plugin_compile.json').read_text())
    return f'''# Validación v05 — cámara de mira

Estado: **alpha preparada para prueba interactiva**. Casos v05 ejecutados en Skyrim: **0**. Los hooks, clipping real y compatibilidad con otros mods requieren la matriz PRUEBAS_EN_JUEGO.md.

## Comprobaciones actuales

Pasan {count} tests Python de archivos/contratos, incluidos {sight['test_count']} de integración con la API de mira. Los {len(compiler['scripts'])} PSC compilan con el compilador Bethesda instalado; PEX finales desensamblados y comprobados contra casts None→array y pérdida de eventos. Los fixtures interpretan ramas reales PSC; no ejecutan la VM.

DLL AMD64 AstraSight para runtime {native['runtime']}, SKSE mínimo {native['skse_minimum']}, exportaciones y metadata inspeccionadas. CTest y pruebas portables C++ pasan, con regresiones RED/GREEN de base óptica, freeze, reconciliación e invalidación de tickets antiguos; consultar native_core_toolchain.log, native_freeze_red.log, native_reconcile_red.log y native_invalidation_red.log. Estos tests no ejecutan los hooks del motor. Los scripts fijan versiones CommonLib/spdlog/rapidcsv y registran hashes de fuentes/DLL y licencias.

NIF SE20.2.0.7/BS100: {assets['visual_triangles_total']:,} triángulos visuales y {assets['collision_triangles_total']:,} de colisión; torre {assets['files']['torre']['shapes']} shapes y ballesta {assets['files']['ballesta']['shapes']}. UV finitas y DDS vanilla locales confirmadas. Fire0.6s/Reset4.4s sin pistas de giro/elevación/cámara. Cuerda comprobada en 152 poses; catorce amarres ajustados al contorno. DDS/ESM no incluidos.

Anclaje AstraSightCameraNode, hijo directo de CTRL_ELEVACION, local [0,80,40] y Rz180°, +Y hacia la dirección de ProjectileNode. Se reimportó el NIF final en 24 poses (tres rumbos y ocho elevaciones): dot mínimo {anchor['minimum_direction_dot']:.8f}, distancia mínima a la malla {anchor['minimum_mesh_distance']:.5f} unidades y al piso {anchor['minimum_floor_clearance']:.5f}. El rayo central no cruza la propia malla en las poses medidas. Esto mide geometría en reposo, no colisiones ópticas/near clip reales ni animaciones del personaje. La envolvente móvil tiene {elevation['floor_minimum_clearance']:.5f} unidades de holgura mínima sobre el disco de azotea.

ESP con masters Skyrim/Update/Dawnguard y registros44 propios; celda AstraAsedioTest, clones WEAP/AMMO/PROJ, UseSightCamera=true, elevación máxima80°. Comprobaciones binarias de referencias, VMAD, conectividad y clearance navmesh pasan. SSEEdit Check for Errors y ajuste/finalización CK **pendientes**; el navmesh generado no se considera finalizado. No se modificó Tamriel.

## Operación y límites

E entra directamente en la mira. La DLL actualiza giro y cámara desde FP, valida handle/token/epoch/identidad3D y publica una pose coherente. Originales fuera del mutex; aplicación de matrices, world update y snapshot serializados con freeze/End. Los getters sólo leen snapshot; la cámara usa un adaptador obtenido de la FP original y respeta espacio/parent/escala. Se reconcilia mirada lógica para descartar exceso en límites, menús y congelación. No se mueve al jugador ni se cambia FOV global.

Papyrus adquiere controles, espera readiness con plazo finito, usa CaptureAim(freeze) para preparar el disparo y termina la cámara antes de liberar sesión. No hay fallback silencioso a v04 si falla la dependencia o la cámara. E sale por eventos y no depende del tick de apuntado. Mantener Ataque no repite; recarga cinco segundos. RemoveItem/Weapon.Fire son llamadas externas sin transacción reversible: hashes/tests no demuestran lanzamiento, daño o atribución del atacante.

Cámara y muzzle tienen distintos orígenes; la dirección se alinea, sin prometer convergencia exacta del retículo a corta distancia. El render de mira usa Blender/FOV75° y es una previsualización del anclaje. No prueba la convención del getter, orden de frames ni HUD real de Skyrim.

## Conservación y entrega

Perfil aislado: {profile['profile']}. Habilita AstraAsedio_QA_v05 y Address Library All in One; hashes de copia instalada coinciden con proyecto. Perfil previo {profile['previous_selected_profile']}, sus archivos y ModOrganizer.ini conservados. No se seleccionó v05 ni se lanzó el juego. Original Blender y archivos v04 permanecen intactos.

Los informes heredados de versiones anteriores son históricos salvo los regenerados y sellados por delivery_status/package. reports/v05_baseline.json identifica el origen v04 y la solicitud aprobada. Pruebas del usuario anteriores no se trasladan a v05. Las fuentes incluyen diseño/plan, Blender, PSC, C++, scripts, licencias, informes y seis renders de los NIF actuales; build/native y recursos/executables del juego se excluyen.
'''
