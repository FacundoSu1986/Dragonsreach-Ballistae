# v26: conservar el puesto durante el idle y liberar el escudo

El usuario muestra `47015.mp4`: entrada/salida de pose y escudo en antebrazo izquierdo. Autoriza corregir el comportamiento exclusivo de los dos artilleros. Se conserva yaw ±60, pitch0, virote normal, prioridad enemiga, filtro de locales y protección del jugador.

## Evidencia

En la prueba v25 el log confirma adquisición, suelo aceptado, referencia1 y altura natural1.03; cancela al tick siguiente (~35ms) por `death/stagger/unload/owner/context`, sin confirmaciones OAR o grip. El resumen y copia inmutable están en reports/diagnosis_v25_context.json y build/guard-v26/observed_v25_AstraSight.log. La cláusula específica no fue registrada. No se presenta el cambio de paquete como medido dentro del motor.

La implementación CommonLib de GetCurrentPackage devuelve GetRunningPackage, que prioriza middleHigh.runOncePackage sobre currentPackage.package. PlayIdle usa SetupSpecialIdle, y high.currentProcessIdle identifica el idle del proceso. La validación v25 mezcla la IA permanente con el paquete temporal: exige que el paquete que corre sea B90 durante todo el idle. Se corregirá esa semántica con un permiso acotado y certificado al idle propio; ningún override ajeno queda autorizado.

## Diseño

Para adquirir se exige el paquete base propio y su ejecución normal, armas guardadas y brazo izquierdo sin escudo. Durante la propiedad se sigue exigiendo el paquete base propio; se permite su ejecución normal o el idle temporal identificado por high.currentProcessIdle == el IDLE propio 802. La coincidencia se acepta únicamente tras solicitud del controlador (acquired). Otros paquetes, falta de proceso, armas desenfundadas, muerte, interrupciones o cambios físicos siguen cancelando. OAR y grip conservan todas sus barreras antes de Fire y Launch.

Antes de comenzar cada nuevo token, Papyrus retira el escudo equipado mediante UnequipItem(shield,true,true), sin eliminarlo del inventario. Se espera al siguiente pump para que asiente la actualización de equipo y esqueleto. Solo aplica al operador resuelto B71/B81; mientras conserve ese puesto el escudo permanece en el inventario. No se retiran otras piezas de armadura ni se toca la raza/escala. Se conserva la IA exclusiva que evita sus armas personales.

context emitirá una cláusula específica y snapshot de paquetes base/running/runOnce, idle, weaponState, shield, cell, root y altura; esos diagnósticos se propagaran a la cancelación. No se relajarán contexto físico, visibilidad o seguridad de tiro para superar una falta de animación.

Migración26 preserva campos v23 y recursos aprobados. DLL3.5.7 conserva APIs4/1. Radio visual2100 y órbita151 se mantienen: el fallo ocurre antes de seleccionar objetivos y el video no justifica agrandar la órbita alejando al actor del mando.

## Verificación y entrega

RED: helper real de admisión de paquete rechaza en v25 una reproducción certificada del idle propio; datos incompletos y overrides ajenos siguen rechazados. Tests de artefactos deben detectar migración26 y retirada exclusivamente del escudo antes del BeginOperation con espera de un pump. GREEN, revisión independiente, scripts y DLL nuevos, ocho gates de release, ZIP v26 separado y CRC/manifiesto. La prueba v25 acredita adquisición y cancelación; la pose/IK y tiro de v26 en Skyrim quedan pendientes.
