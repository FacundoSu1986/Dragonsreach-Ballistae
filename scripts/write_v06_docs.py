"""Current delivery instructions; preserve earlier generators as history."""
from pathlib import Path
from write_v05_docs import README, QA
ROOT = Path(__file__).resolve().parents[1]

def main():
    text = README.replace('v05', 'v06')
    text = text.replace('# Ballesta Astra v06 — mira sobre el arma', '# Ballesta Astra v06 — corrección del disparo')
    old = '**v06 está preparada para prueba interactiva; aún no se ha validado dentro de Skyrim.**'
    text = text.replace(old, '**El usuario confirmó en v05 la cámara alineada y el giro con ratón. La corrección v06 del disparo está compilada y comprobada en archivos; su respuesta en Skyrim está pendiente.**')
    text = text.replace('El log nativo registra runtime y calibración del espacio/basis de cámara.',
        'El log nativo registra API 2/runtime, calibración y dos trazas por ciclo: `shot freeze` y `shot frozen=false`. Sus timestamps permiten medir la inmovilización del apuntado; no hay trazas por frame.')
    text = text.replace('las revisiones de especificación y calidad', 'la revisión de código y las comprobaciones de esta revisión')
    text = text.replace('Original Blender y archivos v04', 'Original Blender y entregas anteriores')
    prefix = '''Los logs v05 registran 132 llamadas a GetCameraState sin binding. El Game.pex instalado redirige a esa misma función Camera, por lo que cambiar sólo el nombre no lo resolvía. v06 usa AstraSightNative.GetCameraState y exige DLL 2.0.0/API 2 antes de bloquear controles. Las funciones de sesión protegidas pueden ejecutarse como tasklets (NoWait); las matrices siguen actualizándose sólo en el hilo del juego. No se modifican los scripts Game/Camera de tu instalación ni los presupuestos globales de Papyrus.

Esta corrección elimina esa dependencia fallida y las esperas evitables de la API propia. No hay medición de FPS de v06 ni prueba de daño/proyectil en juego. La cámara, NIF, controles y recarga de cinco segundos se conservan.

'''
    text = text.replace('## Instalación y prueba', prefix+'## Instalación y prueba', 1)
    text = text.replace('& $pythonExe "$taskRoot\\scripts\\write_v06_docs.py"', '& $pythonExe "$taskRoot\\scripts\\write_v06_docs.py"')
    (ROOT/'README.md').write_text(text, encoding='utf-8')
    qa = QA.replace('v05', 'v06')
    qa += '''
## Comparación del disparo v06

Antes de probar, comprobar en AstraSight.log `AstraSight 2 API 2` y en skse64.log pluginVersion `02000000`. No mezclar PSC/PEX/DLL de versiones distintas. Probar diez clics separados, cada uno después de terminar la recarga, y salir con E durante preparación, lanzamiento y recarga. El giro debe recuperarse después del lanzamiento; la recarga sigue siendo de cinco segundos.

Registrar por separado: FPS antes/durante el clic, tiempo desde clic hasta virote visible, intervalo entre `shot freeze` y `shot frozen=false`, respuesta de E, consumo e impactos. Verificar que Papyrus.0.log no contiene nuevas llamadas unbound GetCameraState desde Astra. Un log vacío de errores no prueba por sí solo FPS, trayectoria o daño. Guardar copia de los logs antes de la siguiente sesión, porque se sobrescriben.

La cámara y ratón fueron confirmados por el usuario en v05; los casos v06 siguen pendientes hasta ejecutarlos. Los renders reutilizados corresponden exactamente a los mismos NIF, sin demostrar el comportamiento del disparo.
'''
    (ROOT/'PRUEBAS_EN_JUEGO.md').write_text(qa, encoding='utf-8')

if __name__ == '__main__':
    main()
