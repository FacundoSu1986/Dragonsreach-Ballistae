"""Write the editable release instructions, not an in-game validation claim."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

README=r'''# Ballesta Astra — v04, primera persona y ratón

Activar (E por defecto) inicia la operación en primera persona. El personaje permanece junto a la manivela: el ratón dirige la ballesta 360°, con elevación de −5° a +80°. Ataque principal dispara; Activar sale y devuelve los controles adquiridos. UseMouseAim=false conserva el modo alternativo de flechas. La mirada inicial se alinea con el rumbo del arma.

La inmovilidad mantiene al personaje en su puesto. Looking sigue activo; Astra rechaza entrada si otro sistema lo bloqueó o usa una cámara especial. La perspectiva previa se restaura al salir cuando Astra la cambió y la cámara actual sigue siendo elegible. ForceThirdPerson restaura tercera persona, sin elegir exactamente subestado 8/9. No se cambian FOV o preferencias globales ni se fuerza una cámara de muerte/mobiliario/carga.

Se conservan los eventos y protecciones v03. Menús y liberación del virote pausan apuntado; se puede apuntar en recarga. RemoveItem/Weapon.Fire son llamadas externas, sin atomicidad ni resultado booleano de lanzamiento. La cámara está en la cabeza del personaje en la manivela y el virote sale desde ProjectileNode: a corta distancia no se promete coincidencia exacta con el retículo.

La cabeza giratoria sube 20 unidades, unos 29 cm; el pedestal se alarga desde la misma base. El NIF final se comprueba a +80° contra el piso, con sus catorce amarres ajustados y pivotes relativos intactos. Se conservan DDS vanilla, luz neutra, blancos y circulación exterior de la torre.

## Prueba

Requiere Skyrim 1.6.1170, SKSE64 compatible y Dawnguard. Con Skyrim cerrado, seleccionar AstraAsedio_QA_v04 en MO2 y lanzar SKSE. Usar un personaje de prueba nuevo para no conservar propiedades/variables anteriores. Activar sólo esta versión y AstraAsedio.esp; desactivar otras copias y AstraAsedio_Despejado.esp.

```text
coc AstraAsedioTest
```

Tomar virotes de acero del contenedor, subir a la azotea, acercarse a la manivela y pulsar Activar. Soltar esa tecla después de entrar. Ratón: apuntar; Ataque: disparar; Activar: salir. La recarga sigue siendo 5 s. La celda es un interior independiente; no hay colocación en Tamriel ni dragones añadidos.

**Prueba en juego v04 pendiente.** El usuario confirmó funcionamiento general de v03; su log demuestra entrada/salida por E y recepción de Ataque, sin validar todos los casos ni demostrar por sí mismo daño. Los tests PSC con fixtures no ejecutan la VM de Skyrim. SSEEdit Check for Errors y ajuste/finalización de navmesh en CK siguen pendientes. Ver VALIDACION.md y PRUEBAS_EN_JUEGO.md.

Papyrus.0.log está en Documentos/My Games/Skyrim Special Edition/Logs/Script. En esta máquina Documentos es C:/Users/Facu2/OneDrive/Documentos. Las trazas indican cámara/entrada/cancelación/rechazo; una traza de Ataque no prueba proyectil.

## Fuentes y reconstrucción

source/Torre_Ballesta_lowpoly_v04.blend conserva el original; source/Astra_export.blend es la exportación editable. Ajustar config.json. Se requiere Blender 4.4.1/PyNifly 27, corpus vanilla extraído y fuentes Papyrus vanilla/SKSE. No se redistribuyen DDS/ESM. Se incluyen diseño y plan en docs/superpowers.

```powershell
$taskRoot = 'E:\Sectores\Sector_Modelado_3D\Ballesta_Astra_Vanilla_SE_v04'
$blenderExe = 'C:\Program Files\Blender Foundation\Blender 4.4\blender.exe'
$pythonExe = 'C:\Users\Facu2\AppData\Local\Programs\Python\Python311\python.exe'
& $blenderExe --background --factory-startup --disable-autoexec --python-exit-code 1 --python "$taskRoot\scripts\build_assets.py"
& $blenderExe --background --factory-startup --disable-autoexec --python-exit-code 1 --python "$taskRoot\scripts\verify_assets.py"
& $blenderExe --background --factory-startup --disable-autoexec --python-exit-code 1 --python "$taskRoot\scripts\verify_limb_ties.py"
& $blenderExe --background --factory-startup --disable-autoexec --python-exit-code 1 --python "$taskRoot\scripts\inspect_elevation.py"
& $pythonExe "$taskRoot\scripts\build_plugin.py"
& $pythonExe "$taskRoot\scripts\compile_papyrus.py"
& $pythonExe "$taskRoot\scripts\verify_input_contracts.py"
& $blenderExe --background --factory-startup --disable-autoexec --python-exit-code 1 --python "$taskRoot\scripts\render_assets.py"
& $pythonExe "$taskRoot\scripts\prepare_test_profile.py"
& $pythonExe "$taskRoot\scripts\package_release.py"
```

No reconstruir el ESP sobre una finalización manual de CK que se quiera conservar. Regenerar informes/hashes/paquetes después de cualquier edición. Los renders son Blender, no capturas del juego. La cadencia 0.05 s se solicita a Papyrus; no garantiza 20 Hz.
'''

QA='''# Prueba v04 en Skyrim

Todos los casos siguientes están pendientes en v04. reports/user_evidence_v03.json conserva evidencia anterior, separada. Seleccionar AstraAsedio_QA_v04 con juego cerrado, iniciar SKSE, personaje de prueba nuevo y coc AstraAsedioTest. Otras copias y AstraAsedio_Despejado.esp desactivados.

1. Recorrer suelo, escaleras, balcón y azotea. Confirmar luz, blancos, pedestal continuo y siete amarres por brazo. Activar entra en primera persona y muestra instrucciones; soltar E. El personaje permanece en el puesto y el ratón debe apuntar. Una transición fallida debe devolver controles con motivo.
2. Girar 360° en ambos sentidos y cruzar 359/0 repetidamente sin inversión/salto. Probar ratón lento/rápido, sensibilidad e inversión vertical vanilla. Registrar latencia: la actualización 0.05 s no garantiza 20 Hz.
3. Apuntar +35/+60/+80° y −5°. Verificar piso, barandas, pedestal, brazos/cuerda durante Fire/Reset. La cámara puede mirar más allá del límite mecánico; el arma se detiene en el límite. Disparar alto y confirmar virote desde la boca hacia arriba.
4. Con 20 virotes, clic consume exactamente uno y crea un único proyectil; mantener no crea ráfaga. Sin virotes se rechaza. Fire 0.6 s/Reset 4.4 s, apuntado congelado hasta commit, regreso de virote visual. Medir impactos y salud de un actor controlado: los blancos STAT y trazas de Ataque no prueban daño.
5. Salir con E mirando en cualquier dirección. Recuperar caminar/combate/cambio de cámara adquiridos. Desde tercera persona, salir devuelve tercera; desde primera conserva primera. Pulsos repetidos no deben salir y reentrar con la misma tecla.
6. Abrir/cerrar inventario/mapa/diario/consola/favoritos durante cada fase. Pausa sin giro/deltas acumulados. Cancelar antes del commit no consume/lanzará. Salida coincidente con RemoveItem/Weapon.Fire se registra aparte: llamadas externas no atómicas ni reversibles.
7. Reasignar Activar/Ataque y repetir. Looking bloqueado por otro sistema rechaza entrada sin habilitarlo. Movimiento/combate/cambio de cámara previamente bloqueados permanecen así al salir. Cámara de mobiliario/free/dragón rechaza entrada; muerte/carga no debe forzar una cámara ordinaria.
8. Guardar/cargar en entrada/apuntado/recarga, morir y descargar celda. Cancelar entrada durante transición y comprobar restauración. ForceFirstPerson es void: confirmar estado 0 con plazo finito. Registrar cámara/controles y motivos bajo retrasos Papyrus.
9. Revisar Papyrus.0.log/SKSE: entrada/cámara/deadline, teclas, cancelación/rechazo/salida; sin arrays inválidos v01 o controles abandonados. Con QALog registrar matrices/commit; comprobar proyectil y daño por separado. Cámara y muzzle tienen orígenes distintos, evaluar error a corta/larga distancia.

Log en esta máquina: C:/Users/Facu2/OneDrive/Documentos/My Games/Skyrim Special Edition/Logs/Script/Papyrus.0.log.

Antes de marcar validada: SSEEdit Check for Errors v04, CK ajustar navmesh al disco de azotea y finalizar conexiones, prueba de acompañante y repetir SSEEdit. Los intentos v01 fueron inconclusos. No reconstruir después del CK si se quiere conservar esa edición; revalidar/empacar su plugin editado.

La celda es interior: colocación exterior y prueba con dragones de Tamriel quedan para la ampliación posterior, sin simularlas mediante tests matemáticos.
'''

def main():
    (ROOT/'README.md').write_text(README,encoding='utf-8')
    (ROOT/'PRUEBAS_EN_JUEGO.md').write_text(QA,encoding='utf-8')

if __name__=='__main__':main()
