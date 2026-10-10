"""Write only current user instructions and explicit evidence limits."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
README='''# Ballesta Astra v10 — cámara en la cola y mira de alza y guion

Para Skyrim SE 1.6.1170, SKSE64 2.2.8 y Address Library para ese runtime. Instalar AstraAsedio_v10_MO2.zip en MO2 y usar el perfil independiente AstraAsedio_QA_v10 (solo Astra y Address Library). Desactivar otras versiones Astra: v10 rechaza las DLL 3.1 (v08) y 3.2 (v09). La preparación no cambia el perfil seleccionado ni inicia Skyrim. Probar con una partida nueva del perfil.

`coc AstraAsedioTest`, tomar virotes de acero del cofre, subir por la escalera lateral y activar la manivela. E entra y sale de la mira; el ratón gira 360° y eleva de −5° a +80°; Ataque dispara; Sprint alterna Individual/Continuo.

Cambios v10, a partir de tu prueba de v09 del 2026-10-05 (reports/user_evidence_v09.json):
- Cámara a 180°, causa encontrada: el registro de cámara de v09 mostró que Skyrim acerca la cámara a tu cabeza cuando hay colisión entre tus ojos y la cámara (el tamaño de la esfera con que el motor lo comprueba está ajustado a ese registro, no medido en el motor). La caja de colisión del pedestal llegaba a 137,6 u, más alta que tus ojos (~109 u); con la ballesta mirando al lado opuesto, la línea ojos→mira la rozaba. Ahora esa caja llega a 35 u y la cámara nunca baja de 65 u, así que la línea ojos→cámara pasa al menos 30 u por encima de ella. Contra toda la colisión (pedestal y torre) se midió cada 15° de giro, en 9 elevaciones y desde todas las posiciones del operador de una grilla de 20 u, incluida la parte de arriba del pedestal (reports/sight_path_verified.json). Pendiente de prueba en juego.
- Cámara en la cola: en tiro bajo y medio va 120 u detrás del alza, sobre la línea de mira, detrás del torno (donde marcaste el círculo rojo). Al elevar se desliza hacia adelante sobre esa línea; a +80° queda a unos 16 u del alza. Las miras siempre quedan alineadas.
- Mira fija: alza (anillo de hierro) sobre la caja y guion (poste con punta) sobre un arco en la punta de la caja, por encima del virote. El guion sube hasta 3,9 u (unos 5,5 cm) entre tiro horizontal y +80° para mantener el cero a 75 m: apuntá poniendo la punta del guion en el centro del anillo, sobre el blanco. Con cero a 75 m, entre 10 y 75 m el virote pega algo por encima del guion (hasta ~32 cm hacia los 40 m) y más allá de 75 m, por debajo.
- Verificado también: la segunda escritura de cámara que agregó v07 nunca se ejecutaba (el registro de v09 lo mostró); la cámara la dan los getters de primera persona.

Siguen de v09: arreglos de ráfaga, menús (la mira queda en pausa y se retoma), primera activación, mensaje del operador, torre rústica con escalera directa. De v08: daño de asedio, virote no recogible, caja Havok del virote, sonido. Limitaciones conocidas: (B5) entre +15° y +45° la parte trasera del carro pasa por el puesto del operador. La caja del pedestal (35 u) frena al caminar, pero de un salto se puede subir: ahí quedás dentro de la base (solo visual; la mira funciona igual y esa posición está medida). Por encima de 35 u la base no tiene colisión: flechas y hechizos la atraviesan. A +80° el anillo del alza queda a ~16,6 u de la cámara: con un fNearDistance mayor que 16 (INI o ENB) se recorta. Fuera de la mira el guion queda donde lo dejó la última pose (hasta 3,9 u) hasta que se recargue la celda.

Fuentes: source/Torre_Ballesta_lowpoly_v04.blend es la copia intacta; source/Torre_escalera_rustica.blend es la torre editable; source/Astra_export.blend es la escena de exportación. Reconstrucción: Blender 4.4/PyNifly27 scripts/build_assets.py (incluye las miras y la colisión del pedestal), build_stairs.py y verify_assets.py; Python scripts/build_plugin.py, compile_papyrus.py y build_native.py. check_rebuild_v10.py verifica la reconstrucción desde v04 en un proyecto temporal. No distribuir DDS/ESM/cache/SDK.

Los informes v01–v09 conservados son históricos. Los archivos vigentes se identifican por SHA en los recibos v10. No se cambian fuentes originales, v09, plugins externos ni configuración global de Skyrim.
'''
QA='''# Pruebas Skyrim v10

Seleccionar AstraAsedio_QA_v10 en MO2, iniciar SKSE y una partida nueva. `coc AstraAsedioTest`. AstraSight.log debe empezar con "AstraSight 3.3 API 3 … tail sight camera with iron sights". Con DLL 3.1 o 3.2 la activación se rechaza con NATIVE_SIGHT_MISSING.

## Cámara y mira (lo principal)
1. Entrar con E: la vista sale desde la cola de la ballesta, con el arma delante, el anillo del alza y el guion dentro.
2. Girar despacio una vuelta completa a cada lado, en tiro horizontal. La cámara no debe saltar a tus ojos en ningún giro (en v09 pasaba entre ~130° y ~240°).
3. Repetir la vuelta parado en otro lugar del puesto (más cerca del pedestal, más atrás) y a +35° y +80°. Al elevar, la cámara avanza hacia el alza; a +80° el anillo se ve grande alrededor del guion. Si querés, subí de un salto al pedestal y operá desde ahí: la cámara tampoco debe saltar.
4. AstraSight.log: anotar cualquier "camera deviation start" con dev de más de ~10 u que dure más de un instante (en v09 eran de 140–178 u y duraban 2–3 s). Copiar AstraSight.log y Papyrus.0.log antes de volver a abrir el juego.

## Puntería
5. Apuntar casi en horizontal con la punta del guion en el centro del anillo, sobre el blanco de 10 m y sobre el de 30 m. Con el cero a 75 m, el modelo predice que el virote pega por encima del punto de mira: unos 3 cm a 10 m y unos 28 cm a 30 m (el máximo, ~32 cm, cae hacia los 40 m; a 75 m, en el punto; a 100 m, ~66 cm por debajo). Eso es lo correcto, no una falla. Anotar la diferencia real.
6. Disparar a +35° y +80° a algo lejano y comprobar que el guion sigue marcando dónde cae.

## Siguen pendientes
7. Daño con `getav health` (nominal 35 + 10 + explosión 150), atribución de la muerte.
8. Virote: no recogible; si cae o rebota, apoyado en todo su largo.
9. Sonido una vez por virote; ráfaga con clics rápidos; Tab con un disparo en curso; Sprint.
10. Guardar y cargar en cada fase, salir de celda, morir: sin controles bloqueados.

Cero casos de motor v10 ejecutados por el agente. Los renders y las mediciones geométricas no prueban la cámara real ni la puntería en Skyrim.
'''
def main():
    (ROOT/'README.md').write_text(README,encoding='utf-8')
    (ROOT/'PRUEBAS_EN_JUEGO.md').write_text(QA,encoding='utf-8')
if __name__=='__main__':main()
