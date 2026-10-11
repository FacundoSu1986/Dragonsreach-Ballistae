# Astra Asedio — QA v22

Paquete de prueba completo para Skyrim SE Steam 1.6.1170, SKSE 2.2.8 y Address Library AE 1170. Mantiene AstraSight 3.5.4/API 4, el disparo, el proyectil y las ballestas de Whiterun. Es el primer paquete que trae **dos torretas** y el **addon de animación del guardia**.

## Qué trae de nuevo

- **Dos torretas, dos alturas.** La torreta del jugador queda como estaba (pivote 153, boca 172,6) y conserva la mira nativa. Se agrega una torreta baja (pivote 117, boca 136,6) para los guardias, que no usan la mira. El motivo está medido: bajar 36 u la torreta del jugador rompe el contrato de la cámara de mira — la cámara baja a 10 u cuando el mínimo es 65, y la comprobación de plano cercano pasa de verdadera a falsa (`reports/sight_path_v22_FAILED.json`). Por eso no se baja: se duplica.
- **Los voladizos de Carrera Blanca son puestos de guardia.** Las cuatro referencias de `AstraAsedio_WhiterunTorres.esp` quedan como puestos exclusivos del guardia (`AllowPlayerTakeover=False`, `UseSightCamera=False`, pivote 117). El jugador conserva la mira en la torreta principal y en la atalaya.
- **El guardia anima.** `AstraAsedio_GuardAnim.esp` y sus clips hacen que el operador NPC se apoye en la ballesta y dispare. Los clips están horneados con las muñecas 36 u más abajo, que es exactamente el puesto bajo: la altura de las manos está **escrita** en el clip, no se deduce del NIF, así que bajar sólo la malla habría dejado al guardia estirando los brazos hacia donde ya no hay empuñadura.

## Requisito nuevo: Open Animation Replacer

El addon de animación **no incluye** Open Animation Replacer y no funciona sin él. Instalalo aparte y comprobá que SKSE lo cargue. Sin OAR el guardia avisa por consola (`enable OAR and AstraAsedio_GuardAnim.esp to operate the NPC.`) y no opera la ballesta; el resto del mod funciona igual.

## Instalación en MO2

1. Cerrá Skyrim y conservá una copia de tu partida antes de probar.
2. Instalá `AstraAsedio_QA_v22_Completo_MO2.zip` como un mod nuevo llamado **AstraAsedio v22 completo**. Reemplazá cualquier v21 anterior: este paquete cambia el ESP del núcleo y el de los voladizos.
3. Desactivá las instalaciones anteriores de Astra Asedio en el panel izquierdo: paquete principal, addon de la atalaya y addon de Whiterun, si existe.
4. En el panel derecho activá **cuatro** plugins, con el principal primero:
   - AstraAsedio.esp
   - AstraAsedio_WhiterunTorres.esp
   - AstraAsedio_Atalaya.esp
   - AstraAsedio_GuardAnim.esp
5. Comprobá que MO2 no muestre masters faltantes. `AstraAsedio_GuardAnim.esp` depende de Skyrim.esm y de AstraAsedio.esp.
6. Abrí Skyrim desde MO2. Si el juego ya estaba abierto, cerralo por completo —también desde el administrador de tareas— y volvé a abrirlo. Un script nuevo no entra con una recarga de partida.

## Qué probar

- **La mira del jugador sigue bien.** Montá la torreta principal y la atalaya: la cámara de mira debe entrar, apuntar y disparar como en v21. Esto es lo que v22 no debía tocar.
- **El guardia baja las manos.** Acercate a un voladizo de Carrera Blanca con un guardia apostado: debe apoyarse en la ballesta con las manos a la altura del puesto bajo, sin subir los brazos por encima del hombro, y disparar con el gesto de disparo.
- **El jugador no puede tomar los voladizos.** Activá un voladizo como jugador: no debe entrar a la mira ni dejarte operar.

## Deuda conocida

- **No hay prueba en juego.** Este paquete está verificado fuera del juego (contrato de release, NIF, ESP, clips) pero nadie lo cargó en Skyrim todavía. Los informes lo declaran: `game_tested: false`.
- **El compilador de Papyrus no es determinista.** Dos compilaciones del mismo `.psc` dan `.pex` distintos (se reordena la tabla de variables y se renumeran las etiquetas). Por eso el repo **congela** el `.pex` del guardia y `scripts/compile_bridge.py` verifica que sea un compilado fiel en vez de reproducirlo byte a byte. Ver `reports/guard_compile.json`.
- **Los clips no se pueden rehornear desde este repo solo.** `scripts/build_guard_bajada.py` necesita Blender, el conversor `blender-hkx.exe` (que no se redistribuye) y el rig de terceros NickNak. El repo versiona los clips ya horneados en `source/anim/`.
- **`.hkx` es una excepción acotada a la política.** Los clips del guardia son de autoría propia, así que se versionan pese a la extensión; ver `THIRD_PARTY_POLICY.md` §2.
- **`reports/plugin_compile.json` trae la entrada del guardia congelada.** Ese reporte es la salida de `scripts/compile_papyrus.py`, que compila los ocho scripts y escribe los `.pex` **en el lugar**. Para el guardia eso es destructivo — el compilador no es determinista y una corrida nueva cambiaría el sha del `.pex` congelado y con él el del paquete. Por eso esa única entrada se marca `frozen: true` y la mantiene `scripts/reconcile_plugin_compile.py`, que propaga los hechos medidos de `reports/guard_compile.json` sin tocar las otras siete. El script **falla** si alguna de las otras siete está desfasada: eso sería un problema mayor, no algo para parchear por encima. **No corras `compile_papyrus.py` sobre esta entrada.**

- **Los hashes fijados dependen de los finales de línea.** `.gitattributes` declara `*.json text eol=lf` y `*.psc text eol=lf`, así que la forma canónica del repo es LF; en Windows, `core.autocrlf=true` la materializa como CRLF en el árbol de trabajo. Los hashes de este paquete corresponden a esa forma. Un clon en Linux o macOS, con LF, no los reproduce y varios tests fallan por eso. Es una fragilidad heredada de todo el repo, no de v22.

## Trazabilidad

- Ancla: el ZIP v21 publicado (`dist/AstraAsedio_QA_v21_Completo_MO2.zip`, sha `0a60c61f…`), pinneado en `reports/base_archive.json`.
- Sello: `python scripts/verify_v22_release.py` → `reports/verification_v22.json`.
- Paquete: `python scripts/package_v22.py` → `reports/package_v22.json` y `dist/MANIFEST_v22.json`. El sha del ZIP vive ahí, no acá: el README viaja dentro del ZIP y sería autorreferencial.
- Contrato: `python -m unittest tests.test_v22_release`.
- No-regresión: `python scripts/verify_suite_v22.py` → `reports/tests_v22_diff.json`.

El ZIP es **reproducible byte a byte**: `package_v22.py` empaqueta con un sello de tiempo fijo (`1980-01-01`), reconstruye y exige el mismo sha. Sin ese sello el hash cambiaba en cada corrida, porque el sello de verificación corre `build_bridge.py`, que reescribe el `.psc` del guardia y el `.esp` del addon con el mismo contenido pero mtime nuevo, y el empaquetador guardaba el mtime. Los empaquetadores históricos (`package_v19.py` y compañía) conservan el comportamiento viejo: sus ZIP ya están pinneados y no se reconstruyen.
