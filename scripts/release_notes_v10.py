import json
def make_validation(root,assets,count,profile,camera,elevation,build):
    native=json.loads((root/'reports/native_artifacts_verified.json').read_text())
    sight=json.loads((root/'reports/v10_sight_behavior.json').read_text())
    path=json.loads((root/'reports/sight_path_verified.json').read_text())
    route=json.loads((root/'reports/stair_route_verified.json').read_text())
    sights=json.loads((root/'reports/iron_sights.json').read_text())
    return f'''# Validación v10

Origen: la prueba de v09 del usuario el 2026-10-05 (reports/user_evidence_v09.json): todo funcionó salvo la cámara; el registro de cámara de AstraSight 3.2 dio la causa.

Pasan {count} tests Python, incluidos {sight['test_count']} de la mira v10, y {native['assertions_passed']} aserciones C++ portables en cinco suites. PSC compilados con Bethesda y PEX desensamblados. DLL AMD64 3.3.0/API 3 para 1.6.1170, SKSE mínimo 2.2.8; PE, exports e inputs sellados por SHA. Revisión independiente en reports/v10_code_review.json.

Causa de la cámara a 180° (posiciones medidas en el log v09; el radio de la esfera está ajustado a ese log): en los cuatro desvíos grandes la cámara quedó a 129,9–131,3 u de los ojos, sobre la línea ojos→mira; una esfera de 12–15 u barrida por esa línea toca la caja de colisión del pedestal (137,6 u, sobre los ojos a ~109 u) a 115–127 u. Sin la caja en el camino (giro ~313°) no hubo desvío. La escritura posterior de cámara de v07 sigue instalada pero no se ejecutó nunca (0 escrituras); la cámara la dan los getters de primera persona.

Arreglo, verificado sobre los NIF escritos en {path['poses']} poses (cada 15° de giro, 9 elevaciones) y {path['operator_positions']} posiciones del operador sobre colisión transitable ({path['operator_positions_on_pedestal']} encima del pedestal, al que se sube de un salto): caja del pedestal a {path['pedestal_collision_top_above_root']:.1f} u; despeje de la línea ojos→cámara a la colisión ≥ {path['min_head_to_camera_collision_clearance']:.1f} u (cota inferior garantizada sobre cada segmento; exigido {path['required_sweep_clearance']:.0f}); cámara a ≥ {path['min_camera_to_weapon_mesh']:.1f} u del arma y a ≥ {path['min_camera_to_sight_meshes']:.1f} u de las miras (plano cercano 15 u), sin geometría visible cortada por ese plano; línea cámara→blanco libre; centro del anillo y punta del guion escritos sobre la línea (error {path['max_sight_alignment_error_units']:.1e} u, con el nodo del guion puesto como lo pone la DLL). Frente al pedestal el despeje de 30 u vale por construcción (cámara ≥ 65 u, ojos ≥ 109 u). Es geometría muestreada, no el motor.

Mira: alza en {sights['rear_sight_local']}, guion en y {sights['front_post_tip_flat_local'][1]:.0f} (punta {sights['front_post_tip_flat_local'][2]:.2f} u en tiro horizontal, 38,30 u a +80°), cámara en la cola {[round(v,1) for v in sights['flat_camera_local']]} que avanza al elevar (86,0 u detrás del alza a +45°, 16,4 u a +80°). El cero a 75 m usa la caída del PROJ (gravedad hacia abajo en el mundo) en forma general y no se escala con el modelo. Predicción del modelo en tiro horizontal: +3 cm a 10 m, +28 cm a 30 m, +32 cm hacia 40 m, 0 a 75 m, −66 cm a 100 m. Las funciones de cero de v08 (sightZeroRadians, sightCameraRotation) quedan como registro y no están en el camino de la cámara.

Torre: colisión de escalera idéntica a la referencia; recorrido de {route['route_samples']} muestras sin choques; {assets['visual_triangles_total']:,} triángulos visuales y {assets['collision_triangles_total']:,} de colisión; ningún NIF tiene NiAlphaProperty.

Límites aceptados (reports/v10_code_review.json): al pedestal de 35 u se sube de un salto (el jugador queda dentro de la base, solo visual); la base no tiene colisión por encima de 35 u; con fNearDistance > 16 el anillo se recorta a +80°; fuera de la mira el guion conserva la última pose; la holgura entre el poste del alza y la cuerda tensa (~4,6 u en y) sale de las cotas de la fuente y no está verificada a lo largo de Fire/Reset.

Perfil {profile['profile']}; Address Library y Astra v10. Los archivos instalados coinciden con mod/. Se conservó la selección {profile['previous_selected_profile']}, sus archivos y ModOrganizer.ini. Original Blender y v09 intactos; no se inició Skyrim.

Casos v10 de motor ejecutados por el agente: **0**. Pendiente: cámara en 360° y a +80° desde varias posiciones, puntería con alza y guion, y los casos que siguen de v08/v09.

Entregas MO2 y fuentes separadas; sin DDS/ESM/SDK/cache.
'''
