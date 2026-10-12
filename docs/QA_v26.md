# Comprobación de Astra Asedio v26

Entrega candidata para Skyrim SE 1.6.1170. Se trabaja en una copia independiente; la instalación MO2 y el proceso Skyrim del usuario no se modifican.

## Evidencia observada en Skyrim v25

`47015.mp4` dura 3,301211 s, tiene 99 frames y muestra al operador con un escudo en el brazo izquierdo. Su SHA-256 es `0435aa87f1bce2c9c0118ff3f0cd1a65a9f70530cf5befae96c4ad999a1e3b47`. Se inspeccionaron frames del comienzo, medio y final. El escudo es visible; eso no demuestra por sí solo que cause la cancelación nativa.

El fragmento conservado de `AstraSight.log` tiene **57450 bytes**, SHA-256 `d8fd019cee97d42cbc7f6da406eecebb923261a2ddfe1d5deac85cc7474f16eb`. Contiene **134 adquisiciones y 134 cancelaciones** con motivo agregado `death/stagger/unload/owner/context`, sin hold confirmado por OAR ni agarre confirmado. Las primeras cancelaciones llegan aproximadamente 35 ms después de adquirir. La escala natural 1,03 ya pasa la adquisición v25.

La cláusula precisa de v25 permanece desconocida. No se atribuye retrospectivamente a paquete, escudo, arma, escena, célula o interrupción. El diagnóstico y snapshot están en `reports/diagnosis_v25_context.json` y `build/guard-v26/observed_v25_AstraSight.log`. No se empaquetan registros personales.

## Corrección y límites

En CommonLib, `Actor::GetCurrentPackage()` consulta `AIProcess::GetRunningPackage()`, que prioriza `middleHigh->runOncePackage.package` frente a `currentPackage.package`. Se revisó la implementación local fijada. Esto fundamenta separar el paquete asignado de la ejecución temporal; la persistencia efectiva de `high->currentProcessIdle` durante estos idles requiere comprobarse en Skyrim. No se presenta como causa medida del fallo v25.

La admisión exige paquete asignado B90 y ejecución normal B90. Tras adquirir, solo puede aceptarse un override identificado como el idle propio 802; un paquete asignado ajeno, un idle ajeno o datos incompletos revocan el puesto. El control OAR y el agarre antes de Fire y Launch permanecen intactos.

Papyrus prepara únicamente los dos artilleros propios. Consulta el escudo, lo desequipa con `UnequipItem(shield,true,true)`, conserva inventario, espera 0,2 s y vuelve a consultar antes de BeginOperation. No basta el transcurso de la espera. La DLL comprueba también el escudo en adquisición y contexto; cambios de equipamiento o escena durante la propiedad cancelan efectos pendientes. El escudo queda guardado mientras el NPC mantiene este rol permanente; no se promete reequiparlo automáticamente al descargar.

El contexto ahora identifica la primera condición inválida y registra la información asociada antes de cancelar. Se conservan sector, altura, radio visual 2100, órbita 151, soporte, límites de IK, prioridad y protección de trayectoria e impacto.

## Comprobaciones externas vigentes

| Comprobación | Evidencia |
| --- | --- |
| Reproducción aislada previa | 1 fallo esperado en 9 aserciones nuevas nativas; 2 fallos esperados en 7 tests Python por migración/preparación ausentes |
| IA, escudo y migración | 7 tests Python: propiedades, paquetes, aliases, persistencia, escudo y snapshots v24/v25 |
| Nativo | 13 targets CTest, incluidos contratos v23, v25 y 9 aserciones v26 de admisión/override/arma/datos ausentes |
| Jugador | 84 regresiones de cámara, entrada y propiedad; recursos altos preservados frente a v22 |
| Scripts | 10 PEX desde staging nuevo, fuentes y desensamblados vinculados por SHA-256; preparación y bindings comprobados en bytecode |
| DLL | AstraSight 3.5.7 AMD64, API jugador 4/NPC 1; metadatos y correspondencia fuentes/binario |
| Plugins y animaciones | Referencias y propiedades de cuatro ESP; 4 HKX canónicos decodificados independientemente; contratos de raíz, escala, duración y continuidad |
| Paquete | Cuatro plugins, 10 PEX, 12 copias HKX; CRC, nombres, inventario completo y SHA-256; dos empaquetados idénticos |
| Preservación | Recursos ESP/HKX/NIF/SEQ/OAR iguales a v25; `.blend`, preview y ZIP v23/v24/v25 sin cambios |

Los resultados finales se registran en `verification_v26.json`, `native_build_receipt.json`, `plugin_compile.json`, `package_v26.json` y `zip_independent_v26.json`, dentro de `reports`. Las dependencias externas y el SDK se comparan por SHA-256 antes y después de la compilación. La revisión independiente y su alcance se registran en `reports/review_v26.json`.

Las pruebas históricas v23/v24/v25 se conservan separadamente. Solo se ejecutan las rutas vigentes para v26, además de contratos previos aún aplicables; los constructores históricos no se ejecutan durante la verificación final.

## Pruebas pendientes en Skyrim v26

- [ ] Cargar copia de partida v25: migración 26, escudo guardado, paquete asignado B90, hold OAR y agarre continuos.
- [ ] Permanecer sin objetivos disponibles: pose de operación estable y sin arma personal.
- [ ] Pasar por delante con jugador y visitante: seguimiento horizontal; habitantes/guardias locales no hostiles ignorados.
- [ ] Agredir a un vendedor: no arcos personales ni disparos contra el jugador.
- [ ] Enemigo NPC visible alcanzable: prioridad, gesto Fire, un virote normal por ciclo e impacto.
- [ ] Objetivo fuera de sector, altura no alcanzable, obstáculos, aliado o neutral cruzando: cancelar disparos.
- [ ] Arco completo −60°/0°/+60°: manos, codos, pies, apoyo y cercado; altura del arma fija.
- [ ] Muerte, stagger, descarga, guardar/cargar y cambio de equipamiento: cancelar, limpiar y recuperar el estado válido.
- [ ] Atalaya y torreta principal: cámara y disparo del jugador conservados.
- [ ] xEdit Check for Errors con todos los masters.

No se ha probado v26 en Skyrim. Compilar, verificar el ZIP y revisar estructuras no certifica reproducción OAR, agarre, orden efectivo de hooks/IK, impacto ni cámara en el motor. La vista previa corresponde a la escena aprobada anterior.
