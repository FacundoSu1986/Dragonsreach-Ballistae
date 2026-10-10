# Validación v18

Fuentes, PEX, DLL y ZIP se verifican por SHA256. Se compilaron los seis scripts con el compilador y ensamblador de Bethesda, sin errores ni advertencias. La DLL 3.5.3/API4 declara versión 0x03050030, runtime 1.6.1170 y SKSE mínimo 2.2.8. Los 6.012 archivos del proveedor externo no cambiaron.

Las ocho suites C++ pasan 2.368 aserciones. La regresión nueva reproduce el cálculo medido 756 → 5.400 y comprueba velocidades normales, multiplicadores existentes e inputs inválidos. Las pruebas de fuentes y datos pasan 275 casos y 107 subtests. Los 42 casos antiguos que exigían recolocar las estaciones se conservan como históricos, fuera de esta ejecución: ese comportamiento se eliminó. Sus fixtures se reutilizan para probar que la cesión y recuperación no mueven la ballesta. El evaluador PSC no ejecuta la máquina virtual de Skyrim.

Se conservan los tres ESP y todos los NIF de v17. El complemento de ciudad mantiene 26 registros y sus puestos B70/B80; se verifican 172 propiedades VMAD con tipos y destinos y la reproducción idéntica del complemento. No se agregan LAND, NAVM, NAVI, PACK ni cambios a patrullas vanilla. La certificación geométrica v15 se conserva porque mallas y entradas coinciden. Se verifican los 608 archivos de la base v17 preservada.

Los registros reales de v17 se copiaron y sellaron en `reports/runtime_evidence_v18`. La DLL y los seis PEX instalados, además del ESP de ciudad, coincidían con v17. Dos disparos mostraron velocidad inicial asignada de 5.400, velocidad compuesta de 756 y una muestra posterior con velocidad 756. El retardo medido de esos disparos fue de 100,774 y 128,168 ms; no es una medición de v18.

Papyrus mostró activación de B80 a las 15:56:45 y cambios de generación/cancelación a las 15:56:47, antes del límite de diez segundos. La operación de recolocación en las fuentes podía mover Self y cancelar una cesión mediante OnUnload; esa regresión falla en la fuente anterior y pasa al conservar posiciones fijas. El registro anterior no identifica directamente la llamada que provocó la descarga en ese intento. Los nuevos eventos de diagnóstico permiten comprobarlo en juego.

La normalización se aplica exclusivamente al proyectil que Astra acaba de crear. Conserva el jugador como shooter y no cambia power, daño, gravedad, munición ni formularios globales. La velocidad compuesta y sus multiplicadores se comprobaron en el SDK fijado y en las [fuentes de CommonLibSSE-NG](https://github.com/CharmedBaryon/CommonLibSSE-NG/blob/main/src/RE/P/Projectile.cpp). La asignación inicial del vector se conserva; también se corrige el escalar que utiliza el cálculo de velocidad.

No se cargó esta DLL en Skyrim. La entrada a la cámara, el vuelo, el daño y la continuidad de la partida quedan pendientes. La revisión final es del agente principal y cubre código y evidencias locales; no es una revisión independiente.
