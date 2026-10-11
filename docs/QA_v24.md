# Comprobación de Astra Asedio v24

Entrega QA del 11 de octubre de 2026 para Skyrim SE 1.6.1170. Se trabaja en una copia independiente; no se modifica la instalación de MO2 ni se publica en remoto.

## Evidencia del fallo en v23

El usuario observó guardias sin la pose prevista y disparando con sus arcos personales después de agredir a un vendedor. La lectura de `AstraSight.log`, Papyrus y el mod instalado confirmó DLL v23, API OAR disponible y migración B71/B81, junto con rechazos del contrato agregado de adquisición. Los NPC B00/B01 no tenían PKID propios del puesto.

La falta del paquete es comprobable y permite el comportamiento de combate personal al restaurarse el estado anterior. El log agregado **no demuestra cuál de las comprobaciones físicas, de graph o solicitud de idle falló**, ni que el rechazo haya ocurrido antes de llamar a OAR. La orientación previa, el margen de soporte y la identidad adicional de userData eran restricciones que se revisaron; no se presentan como una causa física medida en esa partida.

## Comprobaciones fuera del juego

| Comprobación | Resultado |
| --- | --- |
| Contratos de IA y migración v24 | 4/4 pasan: PACK privado, PKID, ALPC, prioridad, aliases opcionales y bootstrap |
| Contratos conservados de colocación, clips y plugins | 5/5 pasan |
| Regresiones de cámara, entrada y propiedad del jugador | 84/84 pasan |
| PEX Bethesda desde staging nuevo | 10/10 compilados, desensamblados y con hashes fuente/binario coincidentes |
| DLL MSVC AMD64 | AstraSight 3.5.5, API jugador 4, API NPC 1; runtime y exportaciones comprobados |
| CTest nativo | 11/11 pasan; contrato del guardia con 59 aserciones y cero fallos |
| HKX independiente | 4/4: duración, esqueleto, raíz, escala, continuidad y transiciones |
| Referencias y propiedades | Cuatro ESP; VMAD, aliases, PKID y ALPC resuelven a sus registros y tipos del mod |
| Preservación del jugador | Ballesta alta, atalaya y propiedades coinciden con v22 |
| Revisión independiente | Sin bloqueos; revisó paquete, adquisición, soporte fijo, migración, recuperación y protección del jugador |

Los casos añadidos fueron observados fallando antes de la corrección: IA ausente, migración anterior, adquisición condicionada a la orientación, pequeño desfase de controlador rechazado, y refresco de aliases ausente. Después se verificaron las fuentes, ESP y binarios actuales. El soporte ahora conserva su altura capturada y rechaza suelo diferente, pendiente elevada, altura excesiva o datos no finitos. Las dependencias y SDK externos se compararon por SHA-256 antes y después de compilar, sin cambios.

Los ocho grupos de comprobación vigentes están en `reports/verification_v24.json`. Los informes de compilación, PE, puente y paquete contienen los hashes de los archivos finales. El manifiesto incluido cubre cada archivo del ZIP, vincula la verificación y el `.blend`/MP4 aprobados. Se comprueban CRC, inventario, bytes originales contra archivados y dos empaquetados reproducibles. El ZIP original v23 y su manifiesto permanecen intactos. Sus comprobaciones históricas no se cuentan como pruebas jugables de esta corrección.

La inspección de referencias es estructural y de los registros propios; no sustituye xEdit Check for Errors con todos los masters. La compilación y los tests portables tampoco demuestran selección efectiva del paquete, comportamiento del controlador Havok u OAR dentro de Skyrim.

## Pruebas pendientes en Skyrim v24

- [ ] Cargar copia de la partida v23: observar migración v24, paquete del puesto, brazos bajos, pies sobre el suelo y operador dentro del cercado.
- [ ] Pasar con el jugador y con un neutral dentro del sector: seguimiento horizontal estable, sin elevación ni disparo.
- [ ] Agredir a un vendedor: ambos artilleros permanecen en el puesto sin sacar arcos personales; la ballesta no dispara contra el jugador. Las otras guardias pueden responder de manera normal.
- [ ] Introducir un enemigo NPC hostil, en combate y alcanzable: prioridad enemiga y un virote normal por ciclo; comprobar que el virote no persigue al objetivo en vuelo.
- [ ] Probar aliado cruzando, neutral junto al impacto, obstáculo, sector no alcanzable y objetivo a otra altura: cancelar tiro cuando corresponda.
- [ ] Recorrer −60°, 0°, +60° y todo el arco; confirmar pasos, agarre y retorno a la postura con la armadura real.
- [ ] Interrupción legítima, muerte, descarga, regreso y guardar/cargar durante el ciclo: cancelar efectos pendientes y recuperar solamente estados válidos.
- [ ] Comprobar cámara, control y disparo del jugador en atalaya y torreta principal.
- [ ] Ejecutar xEdit Check for Errors con los masters.

Para certificar reproducción real, el log debe contener `guard v24 hold confirmed by OAR`, además de la adquisición. Un mensaje de adquisición solo confirma una solicitud de idle. Para certificar lanzamiento, se requiere `guard real projectile` y observación jugable. Estas pruebas continúan pendientes.
