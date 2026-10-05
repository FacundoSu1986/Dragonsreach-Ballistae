"""Editable instructions; engine verification is explicitly separate from file checks."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
README=r'''# Ballesta Astra v05 — mira sobre el arma

Activar (E por defecto) entra directamente en primera persona con la cámara anclada detrás del mecanismo. Ratón: giro de 360° y elevación de −5° a +80°. Ataque principal dispara; Activar sale. El personaje permanece en el puesto de la manivela. El retículo es el normal de Skyrim; esta revisión no añade zoom ni modifica el FOV global.

AstraSight.dll actualiza apuntado y cámara desde el estado de primera persona del motor. Papyrus conserva sesión, entrada, munición y Fire/Reset. El anclaje sigue CTRL_ELEVACION y no tiene pistas de disparo/recarga. Se congela la pose al preparar el lanzamiento; la recarga sigue siendo de cinco segundos. Cámara y boca del virote tienen orígenes distintos: comprobar paralaje a corta distancia.

## Instalación y prueba

Requiere **Skyrim SE 1.6.1170.0, SKSE64 2.2.8, Dawnguard y Address Library para 1.6.1170**. La DLL rechaza otros runtimes. Ya se preparó el perfil aislado **AstraAsedio_QA_v05** en MO2 con esta versión y la Address Library existente. El perfil previamente seleccionado se conserva.

Con Skyrim cerrado, seleccionar AstraAsedio_QA_v05, iniciar mediante SKSE y usar un personaje de prueba nuevo. Mantener desactivadas otras copias de AstraAsedio y AstraAsedio_Despejado.esp. El ZIP MO2 contiene la DLL, NIF, ESP, PEX, fuentes PSC, SEQ e instrucciones; Address Library es una dependencia externa y no se redistribuye.

```text
coc AstraAsedioTest
```

Tomar virotes de acero del contenedor, subir a la azotea y acercarse a la manivela. Pulsar Activar y soltar la tecla. La vista debe pasar a la mira, mostrar el arma y acompañar su giro. Pulsar Activar de nuevo para salir. Ataque y Activar respetan teclas reasignadas. Si falta AstraSight o falla la adquisición de cámara, la sesión debe terminar y devolver los controles adquiridos, mostrando el motivo; no continuar con una cámara de jugador desalineada.

La perspectiva previa se restaura al salir cuando Astra la cambió y la cámara sigue siendo elegible. No se fuerzan cámaras de muerte, carga o mobiliario. Movimiento, combate y cambio de perspectiva se restauran sólo si esta sesión los bloqueó. Looking debe estar disponible al entrar.

La celda es un interior de pruebas independiente, con luz neutra y blancos. No hay colocación en Tamriel ni dragones añadidos. Los catorce amarres y la circulación exterior de la torre se conservan.

**v05 está preparada para prueba interactiva; aún no se ha validado dentro de Skyrim.** Las comprobaciones de NIF, compilación, contratos PSC y núcleo C++ no prueban los hooks reales de cámara, la entrega de eventos o el daño en juego. SSEEdit Check for Errors y ajuste/finalización del navmesh en CK también siguen pendientes. Ver VALIDACION.md y PRUEBAS_EN_JUEGO.md.

## Diagnóstico

En esta máquina:

- Papyrus: C:/Users/Facu2/OneDrive/Documentos/My Games/Skyrim Special Edition/Logs/Script/Papyrus.0.log.
- Nativo: C:/Users/Facu2/OneDrive/Documentos/My Games/Skyrim Special Edition/SKSE/AstraSight.log.

El log nativo registra runtime y calibración del espacio/basis de cámara. Una traza de Ataque o de Weapon.Fire no demuestra proyectil, impacto o daño.

## Reconstrucción

source/Torre_Ballesta_lowpoly_v04.blend conserva el original; source/Astra_export.blend es la escena editable. native contiene C++, CMake y licencias; docs/superpowers contiene diseño y plan aprobados. Se requieren Blender 4.4.1/PyNifly 27, fuentes Papyrus vanilla/SKSE, corpus vanilla extraído y MSVC/CMake/Ninja. scripts/build_native.py fija versiones de dependencias. El SDK local de build/native se obtuvo de paquetes oficiales ya cacheados debido a los headers instalados corruptos; no se reparó la instalación global. No distribuir build/native ni DDS/ESM.

```powershell
$taskRoot = 'E:\Sectores\Sector_Modelado_3D\Ballesta_Astra_Vanilla_SE_v05'
$blenderExe = 'C:\Program Files\Blender Foundation\Blender 4.4\blender.exe'
$pythonExe = 'C:\Users\Facu2\AppData\Local\Programs\Python\Python311\python.exe'
& $blenderExe --background --factory-startup --disable-autoexec --python-exit-code 1 --python "$taskRoot\scripts\build_assets.py"
& $blenderExe --background --factory-startup --disable-autoexec --python-exit-code 1 --python "$taskRoot\scripts\verify_assets.py"
& $blenderExe --background --factory-startup --disable-autoexec --python-exit-code 1 --python "$taskRoot\scripts\verify_limb_ties.py"
& $blenderExe --background --factory-startup --disable-autoexec --python-exit-code 1 --python "$taskRoot\scripts\inspect_elevation.py"
& $blenderExe --background --factory-startup --disable-autoexec --python-exit-code 1 --python "$taskRoot\scripts\inspect_sight_anchor.py"
& $pythonExe "$taskRoot\scripts\build_native.py"
& $pythonExe "$taskRoot\scripts\verify_native_artifacts.py"
& $pythonExe "$taskRoot\scripts\build_plugin.py"
& $pythonExe "$taskRoot\scripts\compile_papyrus.py"
& $pythonExe "$taskRoot\scripts\verify_input_contracts.py"
& $pythonExe "$taskRoot\scripts\write_v05_docs.py"
& $blenderExe --background --factory-startup --disable-autoexec --python-exit-code 1 --python "$taskRoot\scripts\render_assets.py"
& $pythonExe "$taskRoot\scripts\prepare_test_profile.py"
& $pythonExe "$taskRoot\scripts\package_release.py"
```

No reconstruir el ESP sobre una finalización manual de CK que se quiera conservar. Regenerar informes y paquetes después de editar. El sellado exige también un recibo vigente de las revisiones de especificación y calidad en reports/v05_final_review.json; reconstruir archivos que cambien sus hashes requiere renovar esa revisión antes de empaquetar. Los renders son Blender; el render de mira sólo muestra la posición óptica propuesta, sin ejecutar la cámara de Skyrim.
'''
QA='''# Prueba v05 en Skyrim

Todos estos casos están pendientes en v05. Usar AstraAsedio_QA_v05 con Address Library, SKSE2.2.8/runtime1.6.1170 y un personaje nuevo. coc AstraAsedioTest. Registrar por separado resultados observados y logs; los tests de archivo no los sustituyen.

1. Entrar con E desde primera y tercera persona. La vista debe estar detrás de la ballesta, con el arma bajo el retículo, sin cámara en la cabeza/manivela. Confirmar que E sale mirando en cualquier dirección y devuelve controles/perspectiva adquiridos.
2. Girar 360° en ambos sentidos, cruzar 359/0 y mover ratón lento/rápido. Cámara, arma y dirección del proyectil deben acompañarse. Comprobar sensibilidad/inversión vanilla y ausencia de retraso visual apreciable.
3. Llegar a −5° y +80°, seguir moviendo contra el límite y luego invertir: respuesta inmediata sin recorrido muerto. Verificar visibilidad/piso/barandas/amarres en reposo y Fire/Reset. La comprobación de 24 poses Blender no valida clipping real del motor.
4. Con veinte virotes, cada pulsación consume uno y lanza un único proyectil. Mantener Ataque no crea ráfaga. Sin munición, rechazo sin bloqueo. Medir impactos y daño sobre un actor controlado, y paralaje del retículo a distancias cortas y largas. Los blancos STAT no prueban daño.
5. Durante preparación, disparo y recarga, abrir/cerrar inventario, mapa, diario, consola y favoritos. Ratón pausado sin deltas acumulados ni saltos al volver. Cancelar antes del commit no consume ni dispara. Al comprometer RemoveItem/Weapon.Fire no se promete deshacer llamadas externas ya realizadas.
6. E repetida y salida durante cada fase: sin disparos tardíos, doble consumo o cámara retenida. Reasignar Activar/Ataque y repetir. Si Looking ya estaba bloqueado, entrada rechazada sin habilitar controles de otro sistema.
7. Guardar/cargar, morir y descargar celda. Cancelar durante la transición inicial. La DLL debe perder readiness al salir del estado FP o cambiar 3D; no forzar una cámara de muerte/carga/mobiliario. El plazo de entrada debe devolver controles ante un fallo.
8. Con el juego cerrado, hacer una prueba separada sin AstraSight.dll habilitada: E debe mostrar error y no dejar controles bloqueados. Restaurar después. Verificar AstraSight.log y Papyrus.0.log sin arrays inválidos, referencias perdidas o readiness retenida.
9. Recorrer escaleras, suelo y azotea; revisar iluminación/blancos/colisión. En SSEEdit ejecutar Check for Errors y en CK ajustar navmesh al disco transitable, finalizar y probar acompañantes. Revalidar el plugin editado antes de empacarlo.

Registrar especialmente compatibilidad con otros mods que enganchan la cámara. El perfil aislado sólo habilita Astra y Address Library; la prueba del perfil habitual es posterior. La celda es interior; Tamriel y combate contra dragones reales quedan para la ampliación.
'''
def main():
    (ROOT/'README.md').write_text(README,encoding='utf-8')
    (ROOT/'PRUEBAS_EN_JUEGO.md').write_text(QA,encoding='utf-8')
if __name__=='__main__': main()
