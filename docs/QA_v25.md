# Comprobación de Astra Asedio v25

Entrega QA para Skyrim SE 1.6.1170, realizada en la copia independiente del proyecto. La instalación MO2 y la partida no se modifican automáticamente.

## Fallo v24 confirmado en Skyrim

El usuario observó que los guardias ya no sacaban sus armas personales, pero no operaban el arma. Se conservó un fragmento completo del registro v24: **101143 bytes**, SHA-256 `88f38c0595a2b1b200e4b5728c4217c0f877c69073192506a4f7d86860cbd41d`. Contiene **230 rechazos**, todos por `station / actor scale differs from 1`, con escala efectiva **1,03**, escala del arma 1, paquete `14000B90` activo y `weaponDrawn=false`, para B71/B81.

Ese veto ocurre antes de solicitar el idle/OAR y explica por qué no se animan en esta prueba. No demuestra el funcionamiento de las comprobaciones posteriores. La copia y su resumen están en `build/guard-v25/observed_v24_AstraSight.log` y `reports/diagnosis_v24_scale.json`; no se incluyen registros personales en el ZIP.

La corrección distingue `refScale` de `GetScale()` y de `TESNPC::GetHeight()` (raza/sexo por altura de base). Exige referencia 1, altura natural humana acotada y coincidencia de escala efectiva; no encoge al actor para superar el veto. Durante la propiedad la escala debe permanecer estable. `guardOrbit` recibe la escala de referencia certificada y no vuelve a vetar la altura natural.

Los rechazos v23 anteriores eran agregados. No se les atribuye retrospectivamente esta cláusula específica: el diagnóstico exacto corresponde a la prueba v24.

## Comprobaciones externas vigentes

| Comprobación | Evidencia |
| --- | --- |
| Reproducción antes de corregir | 23 aserciones nativas: 12 fallos esperados; migración v25 ausente observada fallando |
| Políticas v25 | Escala natural, referencia alterada, datos desconocidos, agarre en −60°/0°/+60°, fase Fire, frescura, residentes, prioridad y altura |
| ESP y partidas anteriores | 5 tests de IA/migración/diagnóstico; PACK, PKID, ALPC y aliases opcionales conservados |
| Colocación y animación aprobadas | 5 tests conservados; radio, suelo, cercado, OAR, agarre y pies authored |
| Jugador | 84 regresiones de cámara, entrada y propiedad; recursos altos comparados con v22 |
| Scripts | 10 PEX desde staging nuevo, sin errores ni advertencias; fuentes, PEX y desensamblados vinculados por SHA-256 |
| DLL | AstraSight 3.5.6 AMD64; API jugador 4, NPC 1; metadatos SKSE/runtime y correspondencia fuente/binario |
| Nativo | 12 targets CTest, incluidos contratos guardia de 59 + 23 aserciones |
| Clips | 4 HKX decodificados de forma independiente; duración, esqueleto, raíz, escala, continuidad y transiciones |
| Paquete | Cuatro plugins, 10 PEX, 12 copias HKX; CRC, inventario y SHA-256; dos empaquetados idénticos |

Los resultados finales y hashes se registran en `reports/verification_v25.json`, `native_build_receipt.json`, `plugin_compile.json`, `package_v25.json` y `zip_independent_v25.json`. Los ZIP v23/v24 previos se comparan con sus hashes entregados. Las dependencias y SDK externos se comparan antes y después de compilar por SHA-256 para comprobar que no cambiaron.

El controlador reafirma la pose tanto en el tick principal como después de la actualización del actor, manteniendo soporte y altura capturados y los límites de desplazamiento/colisión. El IK de manos solo actúa sobre la observación OAR canónica esperada del contrato vigente, con frame, peso y duración válidos. Durante entrada/transición espera la observación; no intenta sujetar una pose vanilla. Conserva las rotaciones de manos, longitudes y escalas de huesos; una corrección mayor de 16 unidades, inalcanzable o que no asiente la muñeca cancela efectos. Fire y Launch exigen agarre reciente.

El filtro local usa facciones vanilla resueltas por plugin, sin deducir residencia del prefijo FormID. Los operadores propios se excluyen y protegen. El seguimiento visual de un enemigo cercano a otra altura no autoriza el tiro: la posibilidad de trayectoria horizontal se comprueba antes de Fire y otra vez antes de Launch. Se conserva el proyectil real, el reloj único y la protección de trayectoria e impacto.

La revisión independiente aprobó los cambios sin bloqueos demostrables: adquisición, OAR, bloqueo/recuperación, escala, IK, selección y protección. Ejecutó además las 23 aserciones v25, 59 v23, 5 tests Python y binding real, todos pasando. Se conserva su alcance en `reports/review_v25.json`; esta revisión externa tampoco certifica el orden efectivo de renderizado dentro del motor.

## Pruebas pendientes en Skyrim v25

- [ ] Cargar copia de partida v24: migración 25, paquete privado, clip OAR real y manos en los mandos.
- [ ] Recorrer el frente con jugador/visitante: seguimiento horizontal estable; locales no hostiles ignorados.
- [ ] Agredir a un vendedor: artilleros en su puesto sin arco personal y sin tiro de ballesta contra el jugador.
- [ ] Enemigo NPC en combate alcanzable: prioridad, gesto Fire, un virote normal por ciclo, impacto y daño.
- [ ] Enemigo a otra altura: seguimiento visual cercano, sin tiro cuando la trayectoria horizontal no alcanza.
- [ ] Aliado/neutral cruzando, obstáculo, cercanía al impacto y objetivo fuera del sector: cancelación segura.
- [ ] Giro completo con armadura real: −60°, 0°, +60°, manos, codos, pies, plataforma y cercado; ningún movimiento vertical del arma.
- [ ] Muerte, stagger, descarga, guardar/cargar e interrupción durante Fire: cancelación, limpieza y recuperación válida.
- [ ] Atalaya y torreta principal: cámara y disparo del jugador conservados.
- [ ] xEdit Check for Errors con todos los masters.

No se ha ejecutado Skyrim para certificar OAR, agarre, orden del hook/IK, impacto, cámara o disparo de v25. Los tests portables, compilación y revisión estructural de ESP no reemplazan esas pruebas del motor. La vista previa corresponde a la escena aprobada; no es una captura de la IA nueva funcionando en Skyrim.
