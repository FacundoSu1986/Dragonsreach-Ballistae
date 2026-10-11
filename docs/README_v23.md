# Astra Asedio v23 — paquete unificado QA

Esta versión reúne los cuatro plugins y los recursos del jugador con los operadores de Whiterun. Se preparó desde `46bfbf7` y la v22 entregada. Las ramas remotas revisadas ya estaban integradas en esa base.

## Instalación en MO2

Instala `AstraAsedio_QA_v23_Unificado_MO2.zip` como un mod nuevo y desactiva el paquete Astra v22 que reemplaza. Activa los cuatro plugins, en este orden relativo:

1. `AstraAsedio.esp`
2. `AstraAsedio_WhiterunTorres.esp`
3. `AstraAsedio_Atalaya.esp`
4. `AstraAsedio_GuardAnim.esp`

Requiere Skyrim SE 1.6.1170, SKSE64 2.2.8, Address Library para esa versión y Open Animation Replacer con API de animaciones V1. Estos requisitos no se incluyen en el ZIP. La instalación local inspeccionada utiliza OAR 3.2.1. Los clips sustituyen idles existentes; no añaden un behavior que deba generarse.

## Uso

Las dos ballestas bajas de Whiterun son exclusivas de sus guardias. La atalaya y la estación principal conservan el arma alta, la cámara y el control del jugador.

Los guardias permanecen detrás de los mandos, dentro del cercado. Siguen a actores visibles en un radio de 2100 unidades y en un sector de −60° a +60°. Conservan su objetivo mientras siga siendo válido. Un enemigo en combate tiene prioridad. Apuntar al jugador o a un transeúnte es un gesto visual y no inicia combate.

La elevación del operador es 0°. El controlador acepta enemigos hasta 6000 unidades si la trayectoria horizontal los alcanza. Antes del disparo verifica postura, enemigo, alineación, ocupación, obstáculos y actores protegidos, incluida el área de impacto. Una comprobación no certificada cancela el tiro. Un ciclo autoriza un solo proyectil real. La recarga corporal queda pendiente.

## Animación y colocación

- Referencias persistentes: `000B71` Este y `000B81` Oeste, resueltas en `AstraAsedio_WhiterunTorres.esp`. Los prefijos de carga y los BaseID `FF…` de una partida no se utilizan.
- Pie del operador: posición local `(0,151,0)` desde el eje de la ballesta; Z del suelo de cada plataforma; orientación inicial del arma +180°. Escala 1.
- `astra_guard_operate.hkx`: bucle de 2 s.
- `astra_guard_fire.hkx`: gesto de 1 s, liberación en 2/30 s ≈0,067 s.
- `astra_guard_turn_left.hkx` y `astra_guard_turn_right.hkx`: pasos de 0,8 s; 12° nominales. El componente nativo adapta los pasos menores mediante IK y usa la fase observada del clip.

La migración de una partida v22 recoloca a los dos operadores y sus marcadores al cargarse, limpia las facciones privadas anteriores y retira los temporizadores antiguos. No modifica guardias vanilla ni el script vanilla de la ballista enana. Una nueva sesión v23 puede recuperar el ángulo guardado del operador sobre su órbita.

## Comprobaciones y límites de esta entrega

**Realizadas fuera del juego:** compilación fresca de PEX y DLL; pruebas nativas y contratos de los archivos finales; lectura independiente de los cuatro HKX; continuidad entre clips; comprobación de agarre, pies y espacio del cercado en la escena de Blender 5.2.2 LTS; lectura de referencias y VMAD; comparación del arma alta, propiedades del jugador y atalaya con la v22; CRC, inventario y SHA-256 del ZIP.

**Pendientes dentro de Skyrim:** comprobar la reproducción final de OAR y el orden del IK con la armadura real; jugador y neutrales pasando; prioridad enemiga; aliado cruzando; obstáculos; alturas o sectores no alcanzables; muerte, descarga y carga de partida v22; cámara y disparo del jugador en la atalaya y estación principal. La vista previa de Blender no sustituye estas pruebas. No se ha completado una pasada de xEdit Check for Errors sobre esta v23.

El ZIP es un candidato QA para esas pruebas. Los registros del nuevo controlador aparecen en `AstraSight.log`; Papyrus registra migración y cambios de estado con `Astra guard v23`. Si falta OAR, un clip válido, suelo o colisión observable, el operador deja de autorizar disparos.

## Fuentes y reconstrucción

El `.blend` editable y el MP4 de la vista previa acompañan al ZIP en la entrega local. El ZIP contiene los recursos del juego, PSC, instrucciones y manifiesto. No contiene rigs originales, conversores, SDK, recursos vanilla ni OAR.

Rutas vigentes del repositorio: `build_guard_v23.py` para autoría, `prepare_guard_scripts_v23.py` y `build_guard_bridge_v23.py` para scripts y plugin, `compile_papyrus.py` para PEX, `build_native.py` para DLL y CTest, `verify_v23_release.py` y `package_v23.py` para comprobación y paquete. Los constructores y verificadores v22 son históricos y pueden sobrescribir sus propios recursos: no forman parte de la ruta v23.

Los informes históricos siguen separados. El contrato antiguo v22 mostró una discrepancia de hashes por finales de línea al materializar la copia de trabajo; la v23 verifica los bytes actuales y su correspondencia fuente/binario. Las 84 pruebas vigentes de cámara, entrada y propiedad del jugador pasan tras actualizar sus actores simulados con `IsSneaking`, ya presente en el controlador v22. No se presenta la suite histórica completa como una prueba de esta versión.

La integración usa la [API pública de animaciones de OAR](https://github.com/ersh1/OpenAnimationReplacer/blob/main/src/API/OpenAnimationReplacerAPI-Animations.h) y conserva los argumentos reales del hook según [Hooks.cpp de OAR](https://github.com/ersh1/OpenAnimationReplacer/blob/main/src/Hooks.cpp). Las licencias de las dependencias nativas se incluyen en `Docs/AstraAsedio/Licenses`.
