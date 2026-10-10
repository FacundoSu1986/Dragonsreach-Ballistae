# Alcance de los informes v05

Los informes copiados desde v04 documentan el historial. No demuestran que la cámara v05 se haya ejecutado en Skyrim. `v05_baseline.json` conserva hashes del padre y la aprobación de entrada directa por E.

La entrega actual se sella con `delivery_status.json` y `package.json`. Sus verificadores comprueban las fuentes y archivos actuales frente a `assets_verified`, `limb_ties_verified`, `elevation_diagnosis`, `sight_anchor_verified`, `plugin_build`, `plugin_compile`, `input_behavior`, `control_lease_behavior`, `camera_aim_behavior`, `native_sight_behavior`, `native_build_receipt`, `native_binary_checks`, `native_artifacts_verified`, `v05_final_review`, `renders` y `test_profile`. Si cambia un archivo, hay que regenerar la evidencia correspondiente antes de empaquetar.

`sight_candidates` y `sight_clearance_search` son estudios geométricos intermedios; sólo `sight_anchor_verified` mide el NIF final. `final_source_review` pertenece a v04; `v05_final_review` identifica las revisiones actuales y sus hashes. `camera_aim_revision` y los informes de revisiones anteriores permanecen como historial; el camino operativo v05 se documenta en el plan, las fuentes, los contratos nativos y las instrucciones actuales.

Ninguna de estas comprobaciones sustituye los casos de juego, SSEEdit o finalización de navmesh en Creation Kit. `in_game_verified` y sus equivalentes siguen en false para v05.
