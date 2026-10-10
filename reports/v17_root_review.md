# Cierre local v17

Cambios revisados: velocidad inicial explícita del único proyectil de Astra recién creado, muestra de movimiento, renovación de referencias de ciudad, retirada diferida del conjunto anterior y límite de preparación de diez segundos.

La munición no se cobra si la dirección/velocidad es inválida o si se cancela antes del lanzamiento; se conservan las compensaciones y la exclusión por propietario. El impulso se aplica fuera del mutex de Session y en la actualización observada de FirstPersonState. Se conserva la atribución al jugador. La muestra conserva un handle y un ticket, y se descarta al terminar la sesión.

La retirada exige que exista el reemplazo en el mismo complemento, ausencia de efectos nativos del puesto anterior y terminación de sus slots de guardia. Invalida sus generaciones antes de desactivar sus cinco referencias propias. El alias mantiene una sola operación y sigue programando consultas si un stack guardado está suspendido. No modifica actores o navegación vanilla. B70/B80 no existían en v16.

El controlador Station ocupa su slot antes del Trace de entrada y revalida la revisión después de las operaciones que ceden ejecución. La preparación permanece acotada y conserva cancelación por menú, muerte, celda descargada o generación vieja. Se conservan los mismos datos y NIF de plataformas, núcleo y torre baja.

Las regresiones se observaron fallando antes de los cambios: falta de impulso explícito, referencias nuevas ausentes, retirada ausente y preparación de cuatro segundos cancelada. Las compilaciones, suites y gate posteriores están vinculados a las fuentes actuales mediante hashes. Los paquetes contienen sólo los payloads actuales y documentos de v17, con CRC y hashes por entrada.

Límites: no hubo ejecución de la DLL ni de la VM en Skyrim. No se confirma el mecanismo interno que produjo velocidad cero ni el estado de los enlaces de la partida. La inspección de bytes del EXE en disco no produjo instrucciones utilizables y no se usó como evidencia causal. La prueba de jugador debe confirmar trayectoria, daño, E en ambos puestos y guardado/carga. Se preservan v16 y la instalación activa sin cambios.
