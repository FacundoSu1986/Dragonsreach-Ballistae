"""Write only current user instructions and explicit evidence limits."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
README='''# Ballesta Astra v08 — daño de asedio, cero de mira y virote físico

Para Skyrim SE 1.6.1170, SKSE64 2.2.8 y Address Library para ese runtime. Instalar AstraAsedio_v08_MO2.zip en MO2. Usar el perfil independiente AstraAsedio_QA_v08 y desactivar otras versiones Astra: la v08 rechaza la DLL 3.0 de v07. La preparación no cambia el perfil seleccionado ni inicia Skyrim. Probar con una partida nueva del perfil, evitando estados Papyrus de pruebas anteriores.

Abrir consola y usar `coc AstraAsedioTest`. La torre está en esa celda de prueba; todavía no tiene emplazamiento en Tamriel. Tomar virotes de acero del cofre, subir y activar la manivela.

E (o tu tecla de Activar) entra directamente en la mira; el ratón gira 360° y eleva de −5° a +80°. Activar de nuevo sale y restaura los controles. Ataque respeta su reasignación y consume un virote de acero por lanzamiento. Sprint alterna Individual/Continuo, como en v07.

Cambios v08, del backlog P0/P1 de docs/revision/2026-10-04-revision-tecnica-astra-v07.md:
- Daño de asedio: arma 35 + virote 10 + explosión de impacto 150 (radio 128 u, fuerza 20), clonada de la balista dwemer vanilla. Fuerza de impacto 50, tambaleo 1,0.
- El virote ya no se puede recoger y su munición no es jugable. Nombres en castellano.
- Cuerpo Havok del virote ajustado al virote real: caja de 284,6 u de largo con la sección del astil (4,4 u), masa 15, restitución 0,1, inercia en el marco de la caja.
- Cero de mira a 75 m en la DLL (AstraSight 3.1.0, API 3): la vista baja δ(θ) = atan((20,4 + 113,6·cos θ)/5554), 1,38° en tiro horizontal y 0,41° a +80°. El NIF conserva la cámara paralela al ánima. Supone la ballesta nivelada: θ es la elevación respecto de la base, que en la celda de prueba tiene rotación 0. Una colocación inclinada desplazaría el cero.
- Sonido de disparo: WPNCrossbowFire de Dawnguard, una vez por virote lanzado.
- Pisos sin alpha-test (la textura no tiene transparencias) y chequeos nuevos de caja, inercia y alfa sobre los NIF escritos.

Daño, caída (modelo g = 0,35·9,81 m/s², v0 = 5400 u/s), cero, explosión y sonido son valores de los records y del modelo: deben confirmarse en Skyrim (ver PRUEBAS_EN_JUEGO.md y VALIDACION.md). Limitación conocida (B5): entre +15° y +45° la parte trasera del carro pasa por el puesto del operador; no se ve desde la mira y la cabeza no tiene colisión. SSEEdit Check for Errors y finalización de navmesh en CK siguen pendientes.

Fuentes: source/Torre_Ballesta_lowpoly_v04.blend es la copia intacta; source/Astra_export.blend es la escena de exportación. Reconstrucción desde config: Blender 4.4/PyNifly27 scripts/build_assets.py (usa el corpus BAE local; parchea el cuerpo del virote con scripts/nif_fisica.py), verify_assets.py; Python scripts/build_plugin.py, compile_papyrus.py y build_native.py. check_rebuild_v08.py verifica la reconstrucción desde v04 en un proyecto temporal. No distribuir DDS/ESM/cache/SDK.

Los informes v01–v07 conservados son históricos. Los archivos vigentes se identifican por SHA en los recibos v08. No se cambian fuentes originales, v07, plugins externos ni configuración global de Skyrim.
'''
QA='''# Pruebas Skyrim v08

Seleccionar AstraAsedio_QA_v08 en MO2, iniciar SKSE y una partida nueva. `coc AstraAsedioTest`. Comprobar AstraSight.log: "AstraSight 3.1 API 3 … sight zero 75 m". No mezclar DLL/PSC/PEX/ESP de versiones: con la DLL 3.0 la activación se rechaza con NATIVE_SIGHT_MISSING.

1. Activar desde tercera persona con E: vista de mira alineada. Girar despacio y rápido pasando 179°, 180°, 181°, 240° y 359° y varias vueltas en ambos sentidos. Anotar si la mira se separa, el arma se ve lateral o hay salto al límite. Elevar a −5°, 35° y 80° y repetir. E siempre permite salir.
2. Individual: diez clics separados y varios clics durante recarga. Debe consumir y lanzar una vez por ciclo aceptado. Registrar tiempo clic→virote, FPS antes y durante el disparo, y separación entre lanzamientos.
3. Sprint cambia a Continuo; mantener Ataque durante cinco ciclos. Munición consumida = proyectiles. Soltar durante Fire y durante Reset: no empezar otro ciclo.
4. Abrir inventario, consola o mapa manteniendo Ataque y durante preparación y recarga. Al cerrar no disparar hasta soltar y presionar de nuevo.
5. Con un único virote, mantener Ataque: un proyectil y una unidad consumida. Salir con E en preparación, disparo y recarga; confirmar movimiento y perspectiva restaurados.
6. Guardar y cargar en cada fase, salir de celda, morir: sin controles bloqueados ni disparos tardíos. Probar escaleras y azotea.
7. Cero y caída (nuevo): apuntar al centro del blanco de 10 m y luego al de 30 m, casi en horizontal. El modelo predice el impacto unas 2 u (10 m) y 19 u (30 m) por encima del punto de mira; sin cero estaría 22 y 39 u por debajo. Anotar la diferencia real: si no coincide, la gravedad del motor difiere del modelo y el cero se recalibra.
8. Daño (nuevo): colocar un NPC hostil frente a la torre (`help <nombre> 4` da su FormID; `player.placeatme <FormID>`), medir `getav health` antes y después de un impacto. Nominal: arma 35 + virote 10 + explosión 150, antes de armadura, resistencias y multiplicadores. Anotar si la muerte se atribuye al jugador.
9. Explosión (nuevo): efecto visual y sonido en el impacto, radio aproximado de 1,8 m, empuje a cuerpos y objetos cercanos. Confirmar si el virote sigue clavado después de explotar.
10. Virote (nuevo): no debe ofrecer "recoger" una vez clavado, y el inventario del blanco abatido no debe contener virotes de asedio.
11. Sonido (nuevo): cada lanzamiento suena una sola vez, también en modo Continuo.
12. Cuerpo físico (nuevo): si un virote rebota o cae, debe quedar apoyado en todo su largo sin atravesar el piso. Disparar a +80° y confirmar que el cuerpo largo no interfiere con la base al salir. El cuerpo usa el sistema de movimiento esférico estabilizado del virote vanilla; si Havok aplica ahí una inercia uniforme, el giro al caer depende de la masa y del tamaño de la caja, no del eje de la inercia. Anotar si cae girando de forma rara.
13. Cuando la ballesta tenga emplazamiento exterior: un dragón con Fuerza Implacable (EncDragon05Fire o DLC1EncDragon07Fire) durante la sesión; el ragdoll del operador debe cerrar la sesión y devolver los controles.

Copiar AstraSight.log, Papyrus.0.log y skse64.log antes de la próxima sesión; se sobrescriben. Cero casos de motor v08 ejecutados por el agente. No interpretar renders, tests portables o ausencia de errores como prueba de FPS, daño, caída o ángulos reales.
'''
def main():
    (ROOT/'README.md').write_text(README,encoding='utf-8')
    (ROOT/'PRUEBAS_EN_JUEGO.md').write_text(QA,encoding='utf-8')
if __name__=='__main__':main()
