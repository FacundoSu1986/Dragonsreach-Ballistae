# Revisión local v18

Revisor: root. Sin revisión independiente nueva. Aprobado para empaquetar una candidata de QA fuera del motor, sin afirmar funcionamiento verificado en Skyrim.

## Evidencia y regresiones

Los registros sellados de v17 distinguen una instalación vigente de un fallo de lógica: los archivos instalados coinciden. El lanzamiento asignó 5400, pero GetSpeed y la muestra posterior fueron 756. La corrección normaliza speedMult con desired/calculated sobre su valor actual; no adivina campos desconocidos de LaunchData ni sustituye shooter/power. Se valida finitud, signo y representabilidad float. Una corrección inválida registra el problema conservando el impulso anterior; un handle ya creado cuenta como lanzamiento y no se reembolsa como si no existiera.

Whiterun cancela una entrada por cambios de generación a los dos segundos. El log no identifica el desencadenante exacto. Se reprodujo en el evaluador el efecto de mover Self y recibir OnUnload durante la cesión; el código anterior falló. B70/B80 ya se colocan desde el ESP, por lo que esa migración se elimina para carga y cesión. Los marcadores permanecen fijos y se conservan los movimientos del actor, los slots pinBusy/sceneBusy, los tokens, el drenaje de efectos y las compensaciones de cancelación. Los eventos nuevos registran la causa de ciclo de vida.

Cuatro pruebas de regresión fallaron antes del cambio y pasan después; la prueba C++ inicialmente falló al faltar la función y pasa con su implementación. Se conservan los logs de ambas fases. Los 42 casos históricos de movimiento v16 no se presentan como pasando con el nuevo contrato; se sustituyen por los casos de posición fija, conservando las demás pruebas de toma de control, recuperación y cancelación.

## Revisión del código

Los cambios nativos afectan el helper de velocidad, la normalización por proyectil, tres muestras diagnósticas y la identificación 3.5.3. El bloqueo de efectos mantiene la creación dentro del compromiso validado, fuera del mutex de Session. No se toca la cadencia, el hook de FirstPersonState, la devolución de munición ni la lógica de daño. flightStage empieza en cero al lanzar, se incrementa sólo con handle vigente y limpia el handle al llegar a tres; una sesión terminada lo invalida. El siguiente lanzamiento vuelve a cero.

El Guard PEX recién compilado no contiene MoveTo/SetAngle sobre Self; el actor conserva sus llamadas. Station mantiene todas las comprobaciones de estado y añade trazas de carga/descarga. El límite de preparación sigue en diez segundos. Los ESP, todos los NIF y las posiciones coinciden con v17; la retirada de B40/B50 y los enlaces B70/B80 se mantienen.

## Verificación y límites

Seis PSC compilados y desensamblados; ocho ejecutables nativos, 2368 aserciones; 275 pruebas y 107 subtests; 172 propiedades VMAD; construcción de ESP idempotente; 608 archivos del padre preservados; 6012 archivos del proveedor externo preservados. Informes actuales sellados por SHA256. La geometría conserva evidencia anterior con entradas idénticas, sin repetir un render innecesario.

Las pruebas portables no ejecutan la inicialización real de proyectiles, sus colisiones, la cámara ni la VM. Las muestras de 250/500 ms permitirán distinguir velocidad de movimiento efectivo, impacto y 3D pendiente. Hace falta la prueba descrita en PRUEBAS_v18.md en Skyrim; no se atribuye a v18 el resultado de una ejecución de v17.
