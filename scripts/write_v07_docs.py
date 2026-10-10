"""Write only current user instructions and explicit evidence limits."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
README='''# Ballesta Astra v07 — mira 360° y tiro continuo

Para Skyrim SE 1.6.1170, SKSE64 2.2.8 y Address Library para ese runtime. Instalar AstraAsedio_v07_MO2.zip en MO2. Usar el perfil independiente AstraAsedio_QA_v07; desactivar otras versiones Astra. La preparación no cambia el perfil seleccionado ni inicia Skyrim. Probar con una partida nueva del perfil, evitando estados Papyrus de pruebas anteriores.

Abrir consola y usar `coc AstraAsedioTest`. La torre está en esa celda de prueba; todavía no tiene emplazamiento en Tamriel. Tomar virotes de acero del cofre, subir y activar la manivela.

E (o tu tecla de Activar) entra directamente en la mira; el ratón gira 360° y eleva de −5° a +80°. El operador permanece junto a la manivela. Activar de nuevo sale y restaura los controles adquiridos por la sesión. Ataque respeta su reasignación y consume un virote de acero por lanzamiento.

Modo inicial Individual: un disparo por press. Sprint (normalmente Mayús izquierda; respeta reasignación) alterna Individual/Continuo. En Continuo, mantener Ataque repite al completar cada recarga; soltarlo impide programar otro disparo. Un disparo ya aceptado puede terminar. Menús, cambio de modo, salida y munición agotada desarman la repetición; después de un menú soltar y volver a presionar Ataque.

Fire 0,30 s; release nominal 0,10 s desde Fire; Reset 1,20 s. El ciclo completo nominal es 1,50 s más un tick de preparación de 0,05 s. Son valores programados: no son una medición de latencia/FPS del motor.

La v07 reaplica el ancla de cámara después de TESCamera::Update, convierte con el padre actual y valida la boca del arma desde un snapshot nativo congelado. Reduce lecturas de nodos/matrices y sondeos de inventario en Papyrus. Mantiene daño y balística de Dawnguard, la altura de mira anterior, geometría, amarres, UV, shaders y colisiones.

Código nativo y Papyrus compilados; mallas reimportadas y contratos de entrada/cancelación comprobados. Cámara 360° real, ritmo del motor y tiro continuo deben validarse en Skyrim. Ver PRUEBAS_EN_JUEGO.md y VALIDACION.md. No se afirma que los tests simulados ejecuten hooks, VM, impactos o daño. SSEEdit Check for Errors y finalización de navmesh en CK siguen pendientes.

Fuentes: source/Torre_Ballesta_lowpoly_v04.blend es la copia intacta; source/Astra_export.blend contiene las acciones aceleradas. Native, PSC, scripts, tests e informes incluidos. Reconstrucción desde config: Blender 4.4/PyNifly27 scripts/build_assets.py (usa corpus BAE local), verify_assets.py; Python scripts/build_plugin.py, compile_papyrus.py y build_native.py. El retimer alternativo retime_v07.py usa el NIF v06 sellado; check_rebuild_v07.py verifica la reconstrucción desde v04 en un proyecto temporal. No distribuir DDS/ESM/cache/SDK.

Los informes v01–v06 conservados son históricos. Los archivos vigentes se identifican por SHA en los recibos v07. Los seis renders estáticos se reutilizan con prueba binaria de igualdad espacial; no muestran el nuevo comportamiento del motor. No se cambian fuentes originales, v06, plugins externos ni configuración global de Skyrim.
'''
QA='''# Pruebas Skyrim v07

Seleccionar AstraAsedio_QA_v07 en MO2, iniciar SKSE y una partida nueva. `coc AstraAsedioTest`. Comprobar AstraSight.log: AstraSight 3 API 3; no mezclar DLL/PSC/PEX/ESP de versiones.

1. Activar desde tercera persona con E: vista de mira alineada. Girar despacio y rápido pasando 179°,180°,181°,240°,359° y varias vueltas en ambos sentidos. Anotar si la mira se separa, el arma se ve lateral o hay salto al límite. Elevar a −5°,35°,80° y repetir. E siempre permite salir.
2. Individual: diez clics separados y varios clics durante recarga. Debe consumir/lanzar una vez por ciclo aceptado. Registrar tiempo clic→virote, freeze→thaw, FPS antes/durante disparo y separación entre lanzamientos. Fire/Reset acortados deben completar sin desajustar cuerda, brazos o virote.
3. Sprint cambia a Continuo; mantener Ataque durante cinco ciclos. Cuenta de munición = número de proyectiles. Soltar durante Fire y durante Reset: no empezar otro ciclo. Cambiar a Individual mientras se sostiene Ataque: requiere nuevo press para repetir.
4. Abrir inventario/consola/mapa al mantener Ataque y durante preparación/recarga. Al cerrar no disparar hasta soltar y presionar nuevamente. No recuperar una ráfaga de disparos después de una pausa.
5. Con un único virote, mantener Ataque: un proyectil y una unidad consumida; ningún bucle de avisos/disparos adicionales. Reponer y presionar nuevamente. Salir con E en preparación, disparo y recarga; confirmar movimiento y perspectiva restaurados.
6. Confirmar proyectil visible, posición/dirección y colisiones sobre blancos en cuatro orientaciones; medir daño real y atribución. Guardar/cargar en cada fase, salir de celda, morir: sin controles bloqueados ni disparos tardíos. Probar escaleras y azotea.

Copiar AstraSight.log, Papyrus.0.log y skse64.log antes de la próxima sesión; se sobrescriben. Los logs conservados en reports/baseline_v06_runtime son pruebas del usuario en v06, no validación de v07. Cero casos de motor v07 ejecutados por el agente. No interpretar renders, tests portables o ausencia de errores como prueba de FPS/daño/ángulos reales.
'''
def main():
    (ROOT/'README.md').write_text(README,encoding='utf-8')
    (ROOT/'PRUEBAS_EN_JUEGO.md').write_text(QA,encoding='utf-8')
if __name__=='__main__':main()
