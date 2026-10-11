# Astra Asedio v25 — guardias sujetos a los mandos

Esta corrección trata el bloqueo confirmado en la prueba v24: AstraSight rechazaba a los dos guardias por su escala efectiva natural de 1,03 antes de solicitar la animación. Ahora distingue la escala de referencia de la altura natural del NPC, conserva su tamaño y reafirma su posición respecto a la ballesta.

## Instalación

Cierra Skyrim. Instala `AstraAsedio_QA_v25_Unificado_MO2.zip` como mod nuevo en MO2 y desactiva el paquete Astra anterior, incluido v24. Activa estos cuatro plugins en este orden relativo:

1. `AstraAsedio.esp`
2. `AstraAsedio_WhiterunTorres.esp`
3. `AstraAsedio_Atalaya.esp`
4. `AstraAsedio_GuardAnim.esp`

Requiere Skyrim SE **1.6.1170**, SKSE64 **2.2.8**, Address Library correspondiente y OAR con API Animations V1. Incluye AstraSight **3.5.6**, API jugador 4 y NPC 1. Los requisitos externos no se incluyen. Los clips reemplazan idles existentes; no se requiere generar un behavior nuevo.

Carga una copia de tu partida anterior. La migración 25 refresca los aliases y recoloca una vez los operadores Este `000B71` y Oeste `000B81`, identificados mediante `AstraAsedio_WhiterunTorres.esp`. Conserva los campos persistidos v23 y espera a que termine la propiedad anterior antes de recolocar. No usa los BaseID `FF…`, ni altera inventario, armadura, raza o escala del guardia.

## Comportamiento

Los dos operadores mantienen sus armas personales guardadas y su posición y orientación ligadas a los mandos. Al girar acompañan el arma alrededor de su eje a radio 151, con los pasos cortos existentes. La altura permanece fija. El giro es exclusivamente horizontal, **−60° a +60°**, y la elevación del arma es **0°**.

El jugador y visitantes visibles dentro de **2100 unidades** reciben apuntado visual. Se ignoran habitantes y guardias locales no hostiles según las facciones de Carrera Blanca `TownWhiterunFaction` y `GuardFactionWhiterun`. Un enemigo NPC en combate tiene prioridad; el objetivo se conserva mientras siga siendo válido dentro de su prioridad. Los dos operadores quedan excluidos de los objetivos.

Un enemigo a otra altura puede recibir seguimiento visual dentro del radio, pero solo se dispara si la trayectoria horizontal puede alcanzarlo. Los enemigos alcanzables pueden ampliar el alcance hasta **6000 unidades**. El proyectil es un **virote normal**, con gravedad: sigue la dirección que tenía al disparar y no persigue al enemigo en vuelo.

El jugador permanece protegido incluso si agrede a un vendedor. Esa agresión comprueba que los artilleros no sacan sus arcos; para probar disparos hace falta un enemigo NPC válido. Un jugador, aliado o neutral en la trayectoria o zona de impacto cancela el tiro, al igual que obstáculos o comprobaciones inciertas.

OAR debe confirmar el clip real antes de ajustar el agarre. La corrección de brazos está limitada a 16 unidades y no cambia escala de huesos. El gesto de disparo y el lanzamiento requieren agarre confirmado reciente. El bucle dura 2 s, Fire 1 s y los pasos 0,8 s; el virote se libera aproximadamente a **0,067 s**, como máximo uno por ciclo. No se añade recarga corporal.

La atalaya y torreta principal conservan las ballestas altas, cámara y API del jugador. Los cuatro ESP y los HKX aprobados permanecen como en v24; la corrección principal está en DLL y scripts de migración. El script vanilla enano permanece intacto.

## Primera prueba y diagnóstico

Acércate **por delante**, dentro del sector frontal de 120°. Estar directamente debajo puede dejarte oculto por la plataforma o fuera del sector. Primero comprueba la pose y seguimiento del jugador; después prueba un enemigo visible a la altura alcanzable, sin neutrales cerca de su trayectoria o impacto.

Los registros de `AstraSight.log` distinguen:

- `AstraSight 3.5.6`: DLL nueva cargada.
- `guard v25 acquired`: puesto y soporte aceptados; animación solicitada.
- `guard v25 hold confirmed by OAR`: clip real observado.
- `guard v25 grip confirmed`: manos ajustadas al mando sobre el clip canónico.
- `guard real projectile`: lanzamiento real y su fase.
- `guard v25 reject`: cláusula, posición, escala efectiva/de referencia, altura natural y paquete. Los fallos de agarre y suelo incluyen datos específicos.

Papyrus registra `Astra guard v25 migrated`. Una adquisición sin confirmación OAR no demuestra reproducción de la animación. Esta entrega está compilada y validada **fuera del juego**; la prueba jugable v25 sigue pendiente. El `.blend` y la vista previa aprobados se conservan por separado.

## Reconstrucción

Rutas vigentes: `prepare_guard_scripts_v25.py`, `compile_papyrus.py`, `build_native.py`, `verify_v25_release.py` y `package_v25.py`. Para reconstruir ESP se conserva `build_guard_bridge_v24.py`, que incluye los paquetes privados y aliases opcionales. No ejecutar el constructor v23 aislado porque omite esa ampliación. Los ZIP v23/v24 entregados se conservan intactos.

El manifiesto SHA-256 incluido identifica cada archivo del paquete y vincula los recursos editables, vista previa y verificación. `QA_v25.md` separa la evidencia v24 de las pruebas nuevas. Las licencias nativas se incluyen en `Docs/AstraAsedio/Licenses`.
