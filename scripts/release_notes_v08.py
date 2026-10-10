import json
def make_validation(root,assets,count,profile,camera,elevation,build):
    native=json.loads((root/'reports/native_artifacts_verified.json').read_text())
    sound=json.loads((root/'reports/v08_shot_sound_behavior.json').read_text())
    zero=json.loads((root/'reports/v08_sight_zero_behavior.json').read_text())
    body=json.loads((root/'reports/projectile_body.json').read_text())
    siege=build['siege']
    return f'''# Validación v08

Esta revisión aplica B1, B2, B3, B4, B6 y B7 del backlog de docs/revision/2026-10-04-revision-tecnica-astra-v07.md. B5 (la cabeza que gira barre el puesto del operador) queda documentada como limitación visual: acortar el voladizo exige rediseñar el torno, el trinquete y las empuñaduras. B12 (LOD) no aplica sin emplazamiento exterior.

Pasan {count} tests Python, incluidos {sound['test_count']} de sonido de disparo y {zero['test_count']} de cero de mira, y {native['assertions_passed']} aserciones C++ portables en tres suites. Cuatro PSC compilados con Bethesda y PEX desensamblados: el PEX final contiene el Play del sonido y el gate de AstraSight 3.1. DLL AMD64 3.1.0/API 3 para 1.6.1170, SKSE mínimo 2.2.8; PE, exports e inputs sellados por SHA. Revisión independiente en reports/v08_code_review.json. Los tests del PSC usan natives simulados; la matemática del cero no ejecuta hooks de Skyrim.

Daño en records: arma {siege['weapon_damage']}, virote {siege['ammo_damage']:.0f}, explosión {siege['explosion_damage']:.0f} (radio {siege['explosion_radius']:.0f} u, fuerza {siege['explosion_force']:.0f}, clonada de {siege['explosion_donor']}), impacto {siege['impact_force']:.0f}, tambaleo {siege['weapon_stagger']}. Proyectil no recogible, munición no jugable, radio de colisión {siege['projectile_collision_radius']} u (semieje del astil). No se midió cómo compone el motor el daño cuando dispara un objeto.

Cuerpo del virote: caja de {2*body['half_extents_units'][1]:.1f} × {2*body['half_extents_units'][0]:.2f} × {2*body['half_extents_units'][2]:.2f} u, cobertura {body['box_coverage']:.0%} del largo visual, masa {body['mass']} y restitución {body['restitution']} (heurística), inercia {[round(v,2) for v in body['inertia']]} con el mínimo sobre el eje largo; cumple las reglas vanilla de radio y masa↔inercia. {assets['visual_triangles_total']:,} triángulos visuales y {assets['collision_triangles_total']:,} de colisión; ningún NIF del mod tiene NiAlphaProperty. Las mismas comprobaciones reprueban los NIF sellados de v07 y mutaciones sintéticas.

Cero de mira: vista bajada δ(θ) = atan((20,4 + 113,589·cos θ)/5554) en la DLL. Las tres constantes se vuelven a derivar en los tests desde config.json, el ballesta.nif final y el PROJ del ESP final. El modelo de caída (gravedad 0,35·9,81 m/s², v0 5400 u/s) no está confirmado en el motor: PRUEBAS_EN_JUEGO.md lo contrasta con los blancos de 10 y 30 m.

Perfil {profile['profile']}; Address Library y Astra v08. Los archivos instalados coinciden con mod/. Se conservó la selección {profile['previous_selected_profile']}, sus archivos y ModOrganizer.ini. Original Blender y v07 intactos; no se inició Skyrim.

Casos v08 de motor ejecutados por el agente: **0**. Pendiente: cámara y cero en Skyrim, daño real y atribución, explosión, sonido, recogida, cuerpo físico del virote al caer y al lanzar a +80°, FPS, guardar y cargar.

Entregas MO2 y fuentes separadas; sin DDS/ESM/SDK/cache. Los informes históricos no sustituyen los recibos v08 actuales.
'''
