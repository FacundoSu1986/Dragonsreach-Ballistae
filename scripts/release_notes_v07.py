import json
def make_validation(root,assets,count,profile,camera,elevation,build):
    native=json.loads((root/'reports/native_artifacts_verified.json').read_text())
    fire=json.loads((root/'reports/v07_firing_behavior.json').read_text())
    retime=json.loads((root/'reports/animation_retime.json').read_text())
    return f'''# Validación v07

La auditoría previa fue contrastada, sin aplicar entonces sus propuestas. Esta revisión aplica preflight nativo por snapshot, retiming coherente y corrección de composición final de cámara. No migra inventario/Weapon.Fire al código nativo ni baja la mira a Z19,6: ese cambio mostró intersecciones en el análisis anterior.

Logs del usuario en v06: cuatro freeze→thaw entre 4,126 y 4,209 s. El usuario confirmó cámara/ratón y mejora parcial, reportó deriva más allá de 180° y lentitud de salida/recarga. Son evidencia del baseline, no resultados de esta revisión.

Pasan {count} tests Python, incluidos {fire['test_count']} de nuevo tiro y cableado, y {native['assertions_passed']} assertions C++ portables. Cuatro PSC compilados con Bethesda y PEX desensamblados. DLL AMD64 3.0.0/API3 compilada para 1.6.1170, SKSE mínimo2.2.8; PE, exports e inputs sellados por SHA. Revisión independiente en reports/v07_code_review.json. Tests del PSC usan natives simulados; matemáticas y mutex no ejecutan hooks de Skyrim.

{assets['visual_triangles_total']:,} triángulos visuales, {assets['collision_triangles_total']:,} de colisión; Fire0,30/Reset1,20 reimportados. {assets['rope_poses_sampled']} poses verifican extremos de cuerda; 14 amarres reimportados. Retimer cambió {retime['timing_floats']} floats temporales y verifica por máscara que todos los demás bytes, incluida geometría/shaders/colisión, son iguales. Fuente editable retimada y reconstrucción desde config comprobada en proyecto temporal. Renders estáticos heredados con igualdad espacial explícita. ESP reconstruido/validado contra config, registros44, masters Skyrim/Update/Dawnguard y celda AstraAsedioTest; Check for Errors de SSEEdit y finalización CK pendientes.

Perfil {profile['profile']}; Address Library y Astra v07. Archivos instalados coinciden con mod. Se conservó selección {profile['previous_selected_profile']}, sus archivos y ModOrganizer.ini. Original Blender y v06 intactos; no se inició Skyrim.

Casos v07 de motor ejecutados por agente: **0**. Pendiente confirmar cámara real al cruzar180°, latencia, FPS, continuo, release/menú, impactos, daño y guardar/cargar. Cadencia nominal1,50s más0,05s preparación, release0,10s desde Fire; no son mediciones del motor. Actor permanece junto a manivela mientras opera. Weapon.Fire devuelve void; un commit consume una unidad y llama una vez, sin prometer atomicidad de llamadas externas ni atribución sin prueba.

Entregas MO2/fuentes separadas; sin DDS/ESM/GameCameraPEX/SDK/cache. Los informes históricos no sustituyen recibos v07 actuales.
'''
