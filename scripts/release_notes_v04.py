"""Validation notes derived from sealed artifacts, with explicit engine limits."""
import json

def make_validation(root, assets, count, profile, camera, elevation, build):
    mount=json.loads((root/'reports/mount_revision.json').read_text())
    return f'''# Validación v04 — primera persona y ratón

Estado: **alpha preparada para prueba interactiva**. No se ha ejecutado v04 dentro de Skyrim.

## Archivos comprobados

{count} comprobaciones de archivos/contrato pasan. Los tres PSC compilan con el compilador Bethesda instalado, 0 errores/0 advertencias, y sus PEX finales se desensamblan. Se rechazan casts None a arrays y un controlador sin eventos de entrada. La compilación y los fixtures PSC no ejecutan la VM ni prueban entrega de eventos en el motor.

NIF SE20.2.0.7/BS100, {assets['visual_triangles_total']:,} triángulos visuales y {assets['collision_triangles_total']:,} de colisión. Torre{assets['files']['torre']['shapes']} shapes y ballesta{assets['files']['ballesta']['shapes']}. UV finitas, shaders donantes y rutas DDS vanilla locales confirmadas; no se redistribuyen DDS/ESM. Fire0.6s y Reset4.4s sin pistas de yaw/pitch. Cuerda reimportada y claves de escala binarias, separación máxima{assets['rope_reimport_max_gap']:.6f} unidades en152 poses. Catorce amarres cerrados, siete por brazo, ajustados al contorno y comprobados en el NIF actual.

El soporte sube{mount['raise_units']} unidades, unos29cm, conservando base Z{mount['fixed_base_after']:.6f}; el pedestal fijo se alarga hasta su nueva unión. Yaw pivot Z{mount['yaw_pivot_z']}, pitch pivot Z{mount['pitch_pivot_z']}. A +80°, mínimo móvil Z3.02039 relativo a la base de la ballesta; disco de piso Z{elevation['floor_relative_z']:.2f}. Holgura mínima de las poses medidas: {elevation['floor_minimum_clearance']:.5f} unidades. Posición/vector ProjectileNode coinciden con el cálculo independiente del NIF para ocho ángulos entre−5°/+80°. Esto verifica envolvente vertical en reposo; contacto detallado entre piezas móviles y visibilidad del operador todavía requieren prueba en motor.

Plugin regular con Skyrim/Update/Dawnguard, registros propios versión44, clones WEAP/AMMO/PROJ, celda AstraAsedioTest, propiedades UseMouseAim=true/PitchMax80/PitchPivotHeight153 y muzzle en reposo{build['muzzle_rest_world']}. No se cambian FormIDs. Daño/balística iniciales son vanilla; crear daño/atribuir atacante mediante Weapon.Fire no se demuestra mediante estas verificaciones.

## Entrada y cámara

E/Activar entra en primera persona y el ratón apunta360°, elevación−5°/+80°. La dirección world de mirada se transforma por la inversa de rotación de la raíz NIF. Se comprueban fórmulas y guards reales PSC con fixtures de cámara/control: {camera['test_count']} casos en la suite de cámara. Hay tests para direcciones, límites, raíz girada, entrada/salida/rollback y cancelación. Confirmar el contenido concreto en los informes de tests; no extenderlo a scheduling arbitrario.

Session captura perspectiva0/8/9, movimiento/combate/cambio de cámara y sólo restaura bloqueos adquiridos. Looking queda activo; una cámara especial o Looking previamente bloqueado rechaza entrada. ForceFirstPerson devuelve void, por lo que se comprueba estado0 con plazo finito y cancelación. La perspectiva anterior se restaura cuando corresponde, con ForceThirdPerson para8/9 sin elegir su subestado exacto. Muerte, carga y cámaras de otros sistemas se respetan. No se modifica FOV ni configuración global.

Se conservan menú/recarga/cancelación v03. Activar sale sin depender de OnUpdate, devuelve controles antes de limpieza visual y evita reentrada del mismo pulso. El disparo revalida generación después de preflight. RemoveItem y Weapon.Fire son llamadas externas sin atomicidad: después de comprometer un disparo no se promete deshacerlo. La cadencia0.05s es una solicitud Papyrus; no garantiza20Hz o tres frames de motor. El guard de matrices comprueba el resultado real disponible antes del lanzamiento.

La mirada y la boca del virote tienen orígenes distintos: a corta distancia no se garantiza convergencia exacta del retículo. La cámara es la del personaje junto a la manivela. Visibilidad, suavidad, compatibilidad con mods de cámara y seguimiento real de GetAngleX/Z necesitan prueba en este runtime.

## Evidencia anterior y pendientes

El usuario confirmó funcionamiento general de v03. Su log registra recepción de E, cancelación y EndSession; también recibe Ataque. Una traza fire input no prueba proyectil/impacto/daño. reports/user_evidence_v03.json conserva sólo extractos Astra y preferencias de la nueva operación; los guardados no se copiaron. v01/v02 se mantienen como evidencia histórica separada.

**Casos v04 ejecutados en Skyrim:0.** PRUEBAS_EN_JUEGO.md contiene la matriz de prueba. SSEEdit Check for Errors y ajuste/finalización de navmesh en CK siguen pendientes; los intentos de v01 fueron inconclusos. El navmesh tiene comprobaciones binarias/conectividad/capsule clearance del constructor, que no sustituyen CK. La superficie debe ajustarse al disco transitable de azotea. La celda es interior, sin colocación en Tamriel ni prueba contra dragones reales.

Renders: cinco vistas Blender de los NIF actuales, cuatro en reposo y una a+80°. No son capturas Skyrim. Una copia NIF alterada intencionalmente debe invalidar la aceptación por hash; originales y producción no se alteran por esa prueba.

## Instalación aislada

Mod/perfil propios AstraAsedio_QA_v04 ya preparados. Los hashes de su copia coinciden con el proyecto. Perfil previamente seleccionado:{profile['previous_selected_profile']}; sus archivos y ModOrganizer.ini se conservaron. No se seleccionó v04 ni se inició Skyrim. No se modificaron runtime, guardados, fuentes originales ni v03.

Con juego cerrado, seleccionar AstraAsedio_QA_v04, iniciar Skyrim 1.6.1170 mediante SKSE64 y usar un personaje de prueba nuevo; coc AstraAsedioTest. Desactivar otras copias y AstraAsedio_Despejado.esp. Las teclas de activación y ataque respetan las reasignaciones.

Referencias de API: PSC vanilla/SKSE instalados y [Camera de SKSE](https://raw.githubusercontent.com/ianpatt/skse64/master/skse64/PapyrusCamera.cpp). El código registra GetCameraState y puede devolver−1 si no obtiene cámara. Las funciones trigonométricas del Math.psc instalado usan grados.
'''
