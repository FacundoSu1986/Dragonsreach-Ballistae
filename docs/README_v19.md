# Astra Asedio QA v19

DLL 3.5.4, API 4. Candidata para corregir el parpadeo al ceder una ballesta del guardia al jugador: usa el Reset nativo ya asentado y espera que termine cualquier disparo pendiente del guardia. El parpadeo aún debe comprobarse en Skyrim; no se afirma una causa visual definitiva.

La cámara y el vuelo del proyectil de v18 fueron confirmados por el usuario. v19 conserva el apuntado y la velocidad y no mueve las ballestas ni los voladizos. El núcleo y Whiterun Torres se deben actualizar juntos; cerrar Skyrim, salir de la mira y usar una copia del save de prueba. Verificar que ningún PEX/DLL anterior sobrescriba los nuevos.

Instalar AstraAsedio_QA_v19_MO2.zip y AstraAsedio_WhiterunTorres_QA_v19_MO2.zip. Cargar AstraAsedio.esp antes del addon. La variante AstraAsedio_Atalaya.esp sigue incluida sólo por continuidad del QA: su terreno requiere corregir NAVM; desactivarla para probar únicamente las torres de Whiterun. No se modificó la instalación ni los saves del usuario.

Repetir entrada/salida con E en las dos torres, con el guardia disparando y en reposo; comprobar desaparición completa, cámara, flecha, coste de virotes, salida con E, regreso del guardia, cargar/descargar celda y recargar save. Separar prueba del disparo del jugador de la del guardia.

La revisión adversarial y los candidatos públicos limpios están separados del paquete QA. Atalaya queda fuera de los candidatos públicos. Quedan pendientes pruebas de juego de v19 y finalización de navegación en CK antes de anunciar una versión estable.
