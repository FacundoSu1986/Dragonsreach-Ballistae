# Astra v07 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Corregir la composición de la mira 360°, reducir esperas y añadir tiro continuo cancelable.

**Architecture:** Snapshot nativo coherente y transacciones por época protegen las escrituras de cámara y preflight; Papyrus mantiene controles e inventario. El NIF y las propiedades del plugin se retiman juntos. Proyecto independiente fuera de Git; no se inventan commits.

**Tech Stack:** CommonLibSSE-NG/MSVC C++23, Papyrus/SKSE, PyNifly 27/Blender 4.4, parser ESP/NIF local.

## Task 1: aislamiento y tests RED
- [ ] Sellar v06 con scripts/start_v07.py, copiar sólo caches locales y logs, no CMake release cache.
- [ ] Añadir native/tests/CoreTests.cpp tests de visitSnapshot(Ticket), preflight de snapshot congelado, conversión post-camera con padre actual y cruces 180/240. Ejecutar scripts/build_native.py --core-only: RED por API faltante.
- [ ] Añadir tests/test_v07_firing.py sobre NativeSightFixture que ejecuta PSC real: continuo, single, release, menú, cambio de modo, munición agotada, doble input, stale epoch. Ejecutar python -m unittest tests.test_v07_firing: RED por falta de repetición/API3/cadencia.

## Task 2: cámara/preflight nativo
- [ ] Modificar native/include/Astra/Core.h y native/src/Core.cpp: Snapshot mundial/root/muzzle; visitSnapshot bajo mutex; validateShot(Key,pose,pivot) exige frozen, ready y coherencia.
- [ ] Modificar native/src/Plugin.cpp: operador/bolt en Binding; comprobar distancia en Update; publicar transforms; PlayerCamera slot2 hook llama original fuera del mutex y reaplica worldCamera con padre actual dentro de visitor, actualiza transform-only sin controllers. El cambio de padre no invalida por identidad; se lee su transformación actual, manteniendo sólo guardas de raíz/3D/estado. Invalidar sólo ticket propio. Test de integración source-contract del hook confirma que el adapter lee padre actual y no retiene el guarda antiguo; prueba completa de motor sigue pendiente.
- [ ] Registrar ValidateShot NoWait, bump API3 y metadata 0x03000000; mod/Scripts/Source/AstraSightNative.psc refleja firma. Correr core tests: GREEN. Build real con scripts/build_native.py y receipt de hashes.

## Task 3: control/cadencia PSC
- [ ] Modificar AstraAsedioActi.psc: mínimo API3, CanOperate rápido nativo sin NetImmerse, ShotTransformReady->ValidateShot. Mantener los guardas generación/token después de límites externos.
- [ ] Añadir ContinuousFire=false, mapped Sprint key/control y toggle latch; repeatFire independiente de heldFire. ClearHeldInput, menu, salida, ammo y modo desarman. Al final Reset invocar TryRepeatShot(gen) una sola vez; no while/catchup. Preparar Fire tras un tick nativo.
- [ ] Tests reales del PSC: GREEN, sin debilitar los tests heredados de cleanup/leases. Ajustar fixtures a API3 y tests anteriores que esperaban API2/3settle nativo preservando las regresiones.

## Task 4: retime y assets reproducibles
- [ ] scripts/retime_v07.py: leer NIF v06 sellado, cambiar sólo tiempos y visibilidad: Fire factor .5, Reset 1.2/4.4. Parser verifica todos los tiempos/controller/keys y datos espaciales iguales. No tocar ancla/cuerda.
- [ ] config.json fuente v07 y tiempos .3/.1/1.2/1.5/API3; build_plugin.py liga ContinuousFire=false y valida duraciones. source/Astra_export.blend actions retimadas y guardadas en v07. scripts/build_assets.py conserva reconstrucción desde config.
- [ ] Blender scripts/verify_assets.py reimporta NIF, comprueba shapes/materiales/colisiones/anchors/endpoint poses. scripts/build_plugin.py y compile_papyrus.py terminan sin errores. Recalcular manifests de assets y renders (geometría sin cambios, render de pose cero verificable).

## Task 5: integración, revisión y entrega
- [ ] Actualizar verificadores v07, recibos y docs de controles/cadencia/evidencia; retirar afirmaciones heredadas v06 como v07.
- [ ] Ejecutar python scripts/verify_input_contracts.py y native build tests; revisión independiente code-review con archivos concretos y resultados. Corregir y repetir sólo afectados.
- [ ] Preparar perfil AstraAsedio_QA_v07 con scripts/prepare_test_profile.py; comprobar perfil seleccionado e ini sin cambios y hashes exactos de archivos instalados.
- [ ] scripts/package_release.py crea ZIP MO2 y fuentes v07 sin DDS/masters/caches. Verificar CRC, entradas/hashes, v06 y fuente original intactas. Informe distingue user v06 de checks v07 y game v07 pendiente; checklist manual de 360°, E, continuo, menú, ammo, guardar/cargar.
