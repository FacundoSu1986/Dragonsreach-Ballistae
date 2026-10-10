"""Write current installation/QA documents from measured placement metadata."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    towers=json.loads((ROOT/'reports/towers_v14.json').read_text());assert towers['success']
    rows=[]
    for s in towers['sites']:
        x,y,z=s['gun_pos']
        center=s.get('yaw_center',0);half=s.get('yaw_half_sector',60)
        rows.append(f"| {s['name'].title()} | {x:.3f} | {y:.3f} | {z:.3f} | {s.get('scale',1.):.2f} | {center-half:g}° a {center+half:g}° | {s['pitch_min']:g}° a {s['pitch_max']:g}° |")
    table='| Torre | X | Y | Z base | Escala | Giro frontal | Elevación |\n|---|---:|---:|---:|---:|---|---|\n'+'\n'.join(rows)
    moves=[s['patrol_marker_adjustment'] for s in towers['sites'] if s.get('patrol_marker_adjustment')]
    marker_note=('Se reubican además los destinos de patrulla '+', '.join(m['id'] for m in moves)+
                 ' sobre puntos vecinos medidos, para que no queden dentro de las bases. Sólo cambia DATA de posición; se conservan rotación, NAME, flags y vínculos. Los destinos tienen piso/NAVM/cápsula inspeccionados; el recorrido real de las patrullas requiere prueba en el motor.') if moves else 'No se cambian referencias vanilla de las torres ni destinos de patrulla.'
    readme=f'''# Astra Asedio QA v14

El jugador tiene un ciclo nominal de **1 segundo** y los artilleros un intervalo mínimo de **2,5 segundos** entre lanzamientos. Fire dura 0,2 s, liberación 1/15 s y Reset 0,8 s; la preparación, giro y programación del motor pueden ampliar el intervalo. Las animaciones del arma se retimaron en esa proporción. Se conserva el apuntado del jugador de −20° a +80°, la torre baja a 2 m, 11 peldaños y 12 escudos apoyados; no hay habitación ni puerta inferior.

El complemento nuevo coloca dos ballestas con guardias propios sobre las dos torres exteriores indicadas por Facu. La escala y el sector de cada puesto se ajustan al espacio medido bajo sus techos. La ballesta del jugador conserva su tamaño. Ambos pisos tienen triángulos NAVM vanilla al mismo nivel; esto comprueba presencia geométrica, y no una ruta de IA ejecutada en Skyrim.

## Instalación en MO2

1. Conservar v13 y su partida para volver atrás. Instalar `AstraAsedio_QA_v14_MO2.zip` como mod nuevo; desactivar la versión anterior del núcleo para que carguen los scripts y el NIF v14.
2. Activar `AstraAsedio.esp`. `AstraAsedio_Atalaya.esp` conserva la colocación del jugador junto a la atalaya y puede activarse por separado.
3. Instalar `AstraAsedio_WhiterunTorres_QA_v14_MO2.zip` y activar **`AstraAsedio_WhiterunTorres.esp` después del núcleo**. Desactivar **`AstraAsedio_Whiterun.esp`**, el complemento anterior con la torre independiente.
4. Usar una partida de prueba nueva para las colocaciones. No se promete migrar las referencias persistentes del viejo complemento de ciudad. Los valores temporales conocidos de v13 sí se migran de forma idempotente en los controladores; sus callbacks antiguos se invalidan.

Skyrim SE 1.6.1170, SKSE64 2.2.8 mínimo y Address Library del perfil que ya funcionaba. DLL AstraSight **3.4.0/API 3 idéntica a v13**, reutilizada de su compilación verificada. Son ESP normales, sin compactar IDs. No se modificó el runtime ni el perfil MO2 durante la construcción.

## Ubicación y controles

{table}

- Este: `cow Tamriel 4 -3`, celda WhiterunExterior01 (0000961B), piso cercano a Z −3616.
- Oeste: `cow Tamriel 3 -3`, celda WhiterunExterior14 (0000961C), piso cercano a Z −4128.
- Laboratorio: `coc AstraAsedioTest`. Atalaya: `cow Tamriel 1 -4`.

Las coordenadas son los centros de las bases definitivas; el ajuste XY permite despejar refuerzos y barandas. Los guardias y marcadores están sobre los pisos existentes. `TORRES_v14.json` contiene alturas, apoyo y límites de las mediciones.

Jugador: activar manivela, E para salir, ratón para apuntar, Ataque para disparar y Sprint para alternar Individual/Continuo. Los puestos nuevos están reservados a sus guardias y no toman los controles ni la cámara del jugador.

## Guardias y compatibilidad

Cada artillero es un NPC propio basado en la plantilla imperial vanilla. Se mantiene en su puesto y dirige la ballesta hacia su objetivo de combate hostil y visible, descartando jugador y compañeros como blancos. La munición NPC no tiene explosión. El controlador calcula el arco bajo desde la posición mundial real de la boca; la escala no cambia la velocidad/gravedad del proyectil.

Se utilizan Fire/Reset del arma. Todavía falta la animación humana propia de operar/cargar: el NPC conserva arco, espada y combate normal vanilla. También quedan por probar su postura, daño y comportamiento en el motor. Hay LOS desde el guardia y comprobación del jugador en la trayectoria; falta un raycast Havok desde la boca y detección incidental de todos los otros NPC. Los sectores medidos sólo cubren las geometrías vanilla incluidas en la inspección.

El complemento incorpora referencias propias persistentes y dos NPC nuevos. Usa WRLD Tamriel (0000003C) y su CELL persistente (00000D74) como contenedores; no modifica LAND, NAVM, NAVI, puertas, paquetes, actores vanilla ni modelos/posiciones de las torres. {marker_note} Las celdas físicas son 0000961B y 0000961C. Un mod que reemplace las torres, techos, murallas o destinos de patrulla puede necesitar un parche; el complemento separado permite hacerlo después.

Atalaya permanece idéntico a v13 y conserva los cambios de terreno y cuatro referencias vanilla heredadas de v11. No se integraron aún relevos, rutas nuevas ni estados de Guerra Civil. `COMPATIBILIDAD_v14.json` enumera IDs/masters/posiciones exactos para futuros parches.

Esta entrega está verificada en archivos, compilación, fixtures y geometría fuera del motor. Los renders son vistas estáticas de los archivos. **La nueva cadencia y los dos puestos aún requieren prueba en Skyrim**; la mejora de apuntado de v13 fue confirmada por Facu.
'''
    tests='''# Prueba en Skyrim SE 1.6.1170: QA v14

Usar una partida nueva descartable con el núcleo v14 y el nuevo WhiterunTorres; el viejo Whiterun debe estar desactivado. Arrancar por SKSE.

1. Laboratorio: repetir giro 360° y elevación −20°/+80°, tiros al suelo, escalera/escudos y salida de la mira. En Continuo medir al menos diez lanzamientos: ciclo nominal 1 s, más preparación/programación. Comprobar que cuerda, virote y Fire/Reset se sincronizan y no se duplica munición/sonido.
2. Abrir menú y guardar/cargar durante Fire y Reset; comprobar vuelta de cámara/controles, ausencia de callbacks viejos y valores temporales migrados. Para evaluar las colocaciones seguir usando partida nueva.
3. Localizar Este con `cow Tamriel 4 -3` y Oeste con `cow Tamriel 3 -3`. Revisar contacto de bases, cuerpo del guardia, techo/postes, barandas y entrada. Recorrer cada sector contra blancos hacia el acceso exterior; observar colisión real del proyectil.
4. Provocar combate exterior en esa partida descartable. Cada ballesta debe apuntar sólo al objetivo hostil de su artillero y lanzar con separación ≥2,5 s; fuera del sector debe rechazar el blanco. Verificar daño, atribución y munición sin explosión. Registrar si el NPC usa además arco/espada o cambia de postura.
5. Cruzar delante durante preparación: comprobar cancelación de tiros peligrosos al jugador. Observar otros NPC cruzando porque su detección incidental aún no está implementada.
6. Descargar/recargar zona, guardar/cargar y matar el guardia durante un ciclo. No deben quedar disparos sin operador ni NPC duplicados. El controlador no resucita al artillero.
7. Probar fases de Guerra Civil y los mods de ciudad que se quieran conservar. La navegación de relevos y cambio de facción no están implementados. Para conflictos, desactivar sólo WhiterunTorres y registrar mod/versión, orden de carga, torre/coordenadas, captura y logs.

La presencia de NAVM encontrada en archivos no demuestra que un guardia camine por la escalera: este prototipo se coloca directamente en su puesto y fija su movimiento. No contiene una animación humana propia de operación.
'''
    validation='''# Evidencia QA v14

Los recibos `verification_v14.json`, `plugin_compile.json`, `native_reuse_v14.json`, `spatial_reuse_v14.json`, `towers_v14.json` y `package_qa_v14.json` pertenecen a esta entrega. Los reportes v11/v12/v13 que permanecen en el proyecto son históricos.

- Compilación Bethesda desde staging limpio y desensamblado de cinco scripts finales; recibos SHA256 enlazan PSC, PEX y disassembly.
- Pruebas del código PSC con fixtures de API, lifecycle/cancelación/cadencia, intervalos ante retrasos nativos, límites por torre y boca mundial escalada. Estas pruebas no ejecutan la VM Papyrus del juego.
- DLL/entradas nativas idénticas a la compilación v13; cinco ejecutables portables idénticos volvieron a pasar 2.281 assertions. No se afirma una compilación nativa nueva.
- Retiming NIF: sólo 1.978 floats temporales registrados; ningún byte espacial, shader o Havok cambia. Evidencia espacial del jugador v13 reutilizada explícitamente por comparación exacta: 36.360 tiros estáticos y 288 poses de cámara. No son ejecuciones geométricas nuevas v14 ni combates del motor.
- Los records del núcleo conservan bytes/IDs salvo VMAD temporal del jugador. Atalaya queda idéntico. El complemento nuevo registra dos NPC propios y seis referencias arma/artillero/marcador persistentes, CELL/WRLD como contenedores y los ajustes de destino de patrulla detallados en COMPATIBILIDAD_v14.json.
- Para las torres se reimportan modelos visuales/Havok y se mide piso, contacto de base, cápsula de cuerpo, NAVM y recorrido angular estático de reposo. No es un barrido completo de los keyframes Fire/Reset. El reporte distingue muestreo geométrico de verificación en motor.
- ZIP revisados con CRC, inventario único y SHA256 de cada entrada; builder de plugins idempotente. Las cuatro licencias de dependencias nativas se incluyen.

Pendiente en Skyrim: cadencia percibida, sincronización real, colisión/daño del proyectil, postura/combate normal del NPC, eventos de carga/guardado y compatibilidad con Guerra Civil y otros mods. La mira v13 fue probada por Facu; esto no valida automáticamente los nuevos puestos.

Contrato de escala usado: SKSE64 obtiene `m_worldTransform.rot` y `m_worldTransform.pos` por separado; la lectura de rotación no incorpora la escala uniforme. Fuente primaria: https://github.com/ianpatt/skse64/blob/master/skse64/PapyrusNetImmerse.cpp . El fixture prueba la balística desde la boca escalada, pero no sustituye una prueba del NIF en Skyrim.
'''
    for name,value in [('README_v14.md',readme),('PRUEBAS_v14.md',tests),('VALIDACION_v14.md',validation)]:
        (ROOT/'docs'/name).write_text(value,encoding='utf-8')
    print('V14_DOCS_WRITTEN')
if __name__=='__main__':main()
