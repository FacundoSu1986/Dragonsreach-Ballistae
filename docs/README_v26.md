# Astra Asedio v26 — preparación de los artilleros

Esta candidata separa la IA asignada al puesto del idle temporal del motor y deja libre el brazo izquierdo de los dos operadores. El video muestra un escudo equipado; el registro v25 muestra adquisiciones canceladas unos 35 ms después, sin confirmación OAR ni agarre. El registro anterior no identifica la cláusula concreta de cancelación. v26 añade ese diagnóstico y necesita una prueba nueva en Skyrim.

## Instalación

Cierra Skyrim. Instala `AstraAsedio_QA_v26_Unificado_MO2.zip` como mod nuevo en MO2 y desactiva el paquete Astra anterior. Activa los cuatro plugins en este orden relativo:

1. `AstraAsedio.esp`
2. `AstraAsedio_WhiterunTorres.esp`
3. `AstraAsedio_Atalaya.esp`
4. `AstraAsedio_GuardAnim.esp`

Requiere Skyrim SE **1.6.1170**, SKSE64 **2.2.8**, Address Library correspondiente y OAR con API Animations V1. Incluye AstraSight **3.5.7**, API jugador 4 y NPC 1. Los requisitos externos no se incluyen. No hace falta generar un behavior nuevo para estos idles.

Carga una copia de tu partida anterior. La migración 26 drena la propiedad anterior, limpia estados antiguos y recoloca una vez las referencias Este `000B71` y Oeste `000B81`, resueltas mediante `AstraAsedio_WhiterunTorres.esp`. Conserva los campos persistidos v23. No utiliza los BaseID `FF…` ni cambia raza o escala.

## Operación

Los dos artilleros mantienen las armas personales guardadas. Su escudo se **desequipa y permanece en su inventario** mientras ejercen este puesto. La preparación espera otra actualización y consulta de nuevo el equipamiento antes de adquirir el control. La DLL cancela si encuentra un escudo equipado durante la operación. Los demás NPC y sus atuendos no se modifican.

La IA asignada debe seguir siendo el paquete privado B90. Durante una propiedad adquirida se acepta el idle propio 802 cuando sustituye temporalmente al paquete en ejecución. Un paquete asignado distinto, un override ajeno, datos incompletos o un arma personal desenvainada impiden continuar. Esta excepción no autoriza disparos: OAR y el agarre reciente siguen siendo obligatorios.

La posición y orientación acompañan a la ballesta alrededor del eje, a **151 unidades**, con los pasos cortos existentes. La altura queda fija. Solo gira horizontalmente de **−60° a +60°**, con elevación **0°**. El radio visual sigue siendo **2100 unidades —aproximadamente 30 metros—**: ampliarlo no resuelve una cancelación anterior a la selección de objetivos.

Apunta al jugador y visitantes visibles dentro del sector. Ignora habitantes y guardias locales no hostiles de Carrera Blanca según sus facciones. Los enemigos NPC en combate tienen prioridad y pueden utilizar el alcance validado hasta 6000 unidades. Solo reciben disparos si la trayectoria horizontal puede alcanzarlos. El virote es normal, con gravedad; no sigue al enemigo durante el vuelo.

El jugador permanece protegido aunque ataque a un vendedor. Para probar disparos utiliza un enemigo NPC válido. Aliados, neutrales y el otro artillero quedan protegidos frente a trayectoria e impacto. Obstáculos, propiedad inválida y comprobaciones inciertas cancelan el tiro. El bucle dura 2 s, Fire 1 s y los pasos 0,8 s; la liberación se sincroniza aproximadamente a 0,067 s, como máximo un proyectil por ciclo. No se añade recarga corporal.

La atalaya y la torreta principal conservan las ballestas altas, cámara y API del jugador. Los cuatro ESP, HKX, NIF, SEQ y configuración OAR son idénticos a los recursos aprobados v25. El script vanilla enano permanece intacto.

## Primera prueba

Comprueba primero que el guardia sin escudo sostiene los mandos de forma continua, incluso sin un objetivo disponible. Después camina **por delante**, dentro del arco frontal. Estar debajo puede quedar oculto por la plataforma o fuera del sector y no constituye por sí solo un objetivo válido.

En `AstraSight.log` deben aparecer, en orden:

- `AstraSight 3.5.7`: DLL cargada.
- `guard v26 acquired`: control adquirido y hold solicitado.
- `guard v26 hold confirmed by OAR`: clip real observado.
- `guard v26 grip confirmed`: agarre confirmado sobre el clip canónico.
- `guard real projectile`: lanzamiento real, únicamente con enemigo válido.

Si la pose se interrumpe, `guard v26 context ... clause=...` identifica el motivo y registra paquetes asignado/en ejecución/run-once, idle, arma, escudo, células, identidad de escenas y escalas. `guard v26 reject` detalla fallos de adquisición, apoyo o agarre. Papyrus registra `Astra guard v26 migrated`. Una adquisición sin OAR y agarre no demuestra reproducción correcta.

## Recursos y reconstrucción

El `.blend` editable y la vista previa aprobados se mantienen por separado. La vista previa no muestra la IA v26 funcionando en Skyrim. `QA_v26.md` distingue la evidencia de juego anterior de las comprobaciones externas actuales y las pruebas pendientes.

Rutas vigentes: `prepare_guard_scripts_v26.py`, `compile_papyrus.py`, `build_native.py`, `verify_v26_release.py`, `package_v26.py` y `verify_zip_v26.py`. Para reconstruir ESP se conserva `build_guard_bridge_v24.py`, que incluye paquetes privados y aliases opcionales. Los ZIP v23, v24 y v25 entregados permanecen intactos.

El manifiesto SHA-256 identifica todos los archivos, la verificación, el diagnóstico anterior y los recursos editables. Las licencias nativas se incluyen en `Docs/AstraAsedio/Licenses`.
