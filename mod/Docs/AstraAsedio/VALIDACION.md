# Validación de archivos — v12 baja

Controles vigentes del proyecto v12:

| Control | Resultado |
|---|---|
| Geometría | Piso 140 u, escalera 11 peldaños, sin habitación ni puerta |
| Escudos | 12 por torre, frente afuera, agarres apoyados (<0,1 u al soporte) |
| Ruta física | 162 muestras desde escalera hasta puesto, sin bloqueos de cuerpo de 128 u y radio 18 u |
| Error máximo de piso reimportado | 0,032 u |
| Navegación del laboratorio | 234 vértices, 313 triángulos, un componente; ruta cubierta |
| Navegación/colisión reimportada | Muestreo de cuerpo en vértices, medios de arista y centro de cada triángulo |
| Barrido de tiro | 360 giros × 86 inclinaciones = 30.960; cero choques; control falsificado detecta poste artificial |
| ESP | 128 referencias altas eliminadas; 14 escudos nuevos (7 por ubicación); resto de registros fuera de lista permitida intactos |
| Identificadores | Se conservan ballesta, cofre y cinco escudos anteriores en cada ubicación |
| Recursos de v11 | Ballesta, virote, DLL, PEX, PSC y SEQ idénticos por SHA-256 |
| Terreno y overrides vanilla | Conservados byte a byte |

Los controles geométricos no equivalen a ejecutar el motor. La v11 fue probada por el usuario; **v12 todavía requiere prueba en Skyrim**, incluyendo reactivación, partida/carga, física y apuntado.

El ZIP es una entrega QA, sin el sello histórico de release público v11. La información de hashes, CRC, idempotencia y pruebas actuales se incluye en `reports/package_qa_v12.json` del proyecto; dentro del ZIP se incluye `Docs/AstraAsedio/RECIBO_v12.json` con hashes de los recursos.
