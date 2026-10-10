"""Evidence-derived v06 notes without importing historical engine claims."""
import json

def make_validation(root, assets, count, profile, camera, elevation, build):
    native=json.loads((root/'reports/native_artifacts_verified.json').read_text())
    binding=json.loads((root/'reports/runtime_bindings_behavior.json').read_text())
    diagnosis=json.loads((root/'reports/fire_runtime_diagnosis.json').read_text())
    return f'''# Validación v06 — disparo y binding de cámara

El usuario confirmó cámara sobre el arma y giro con ratón en v05. Informó lentitud/bugs al disparar. Los logs preservados registran {diagnosis['observed_unbound_get_camera_state_calls']} llamadas GetCameraState sin binding, incluidas rutas de preparación/commit. Game.pex instalado redirige al mismo Camera.GetCameraState; se inspeccionó su bytecode sólo en build y no se distribuye.

v06 usa su getter AstraSightNative, rechaza metadata anterior a 2.0.0 y verifica API 2 antes de adquirir controles. Si falta la DLL, la limpieza libera controles propios sin llamar a las funciones nuevas. Las llamadas de sesión protegidas por mutex se registran NoWait; los writes de nodos y cámara siguen exclusivamente en FirstPersonState::Update. Dos trazas por disparo permiten medir freeze/thaw; no se registra por frame. No se modifica Game/Camera.pex ni la configuración global de Papyrus.

## Evidencia actual

Pasan {count} tests Python, incluidos {binding['test_count']} de regresión del binding/versionado/limpieza. Cuatro PSC compilados con Bethesda y PEX finales desensamblados: ausencia de importaciones Camera/Game.GetCameraState y casts None→array. Los fixtures ejecutan ramas PSC con natives simulados, sin ejecutar VM ni inputs del motor.

DLL AMD64 versión 2.0.0, API 2, runtime exclusivo 1.6.1170, SKSE mínimo 2.2.8. Build y PE verificados por hashes; CTest y {native['assertions_passed']} assertions C++ portables pasan. Revisión independiente del código registrada en reports/v06_code_review.json; el sellado registra su alcance e inputs. Estos checks no ejecutan hooks del motor.

NIF y ESP idénticos a v05: {assets['visual_triangles_total']:,} triángulos visuales y {assets['collision_triangles_total']:,} de colisión. Geometría, UV, cámara anclada, amarres, celda iluminada y blancos conservados por SHA. Los informes geométricos y seis renders se reutilizan porque las mallas no cambiaron. Fire0.6s/Reset4.4s, recarga5s, consumo y estado de disparo conservados. Las comprobaciones binarias de ESP/navmesh se conservan por igualdad de bytes; SSEEdit Check for Errors y finalización manual CK continúan pendientes.

## Prueba y límites

Casos v06 ejecutados en Skyrim por el agente: **0**. No hay mediciones de FPS ni tiempos de lanzamiento posteriores a la corrección. La causa de toda la lentitud no queda demostrada sólo por el error de binding. Weapon.Fire devuelve void: no se afirma proyectil visible, daño ni atribución del atacante sin observarlos. Seguir PRUEBAS_EN_JUEGO.md y comparar freeze/thaw/FPS/consumo/salida con E.

Perfil preparado: {profile['profile']}; sólo AstraAsedio_QA_v06 y Address Library All in One habilitados. Copia instalada coincide con mod. Se conservó el perfil seleccionado {profile['previous_selected_profile']}, sus archivos y ModOrganizer.ini; no se inició Skyrim ni se seleccionó v06. Original Blender, entregas v05 y recursos BAE permanecen intactos.

Fuentes, C++, PSC, scripts, informes, renders y Blender editables incluidos. Dependencias compiladas, SDK, ejecutables, ESM, DDS y Game/Camera.pex vanilla excluidos. Informes de versiones anteriores son históricos salvo los reutilizados por igualdad de bytes y los regenerados/sellados en v06. reports/v06_baseline.json identifica la confirmación del usuario y los hashes de entrega anteriores.
'''
