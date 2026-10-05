# Ballesta Astra v05: cámara de mira montada

El usuario probó v04 y pidió la sensación de apuntar desde el arma, como una mira de ametralladora. Aprobó que **E entre directamente en la mira**. El jugador permanece en el puesto; cámara, giro y elevación deben comportarse como un conjunto. Esta elección autoriza implementar el cambio y preparar una revisión independiente; no se requiere otra confirmación para escribir código, compilar o preparar su perfil QA.

## Resultado

E entra en primera persona desde un anclaje detrás de la ballesta. El ratón controla giro 360° y elevación −5°..80°. La vista sigue la pose real del arma, incluidos sus límites; no puede mirar por separado más allá del límite mecánico. Retículo vanilla centrado y eje de mira alineado con el eje de disparo. Ataque dispara y E devuelve cámara/controles. La cabeza del personaje no es el anclaje de esta vista.

No se añadirá zoom/FOV global en esta revisión. La sensación de concentración procede de la colocación de cámara y la alineación; un zoom puede ajustarse después de probar esta cámara. No se moverá/teletransportará al jugador por cada actualización ni se usará `tfc`.

## Diseño elegido y alternativas

Se elige un pequeño plugin nativo SKSE, `AstraSight.dll`, para actualizar apuntado y leer un `AstraSightCameraNode` de la rama móvil NIF en cada actualización real de primera persona. Papyrus conserva adquisición de sesión, munición, disparo, recarga, menús y salida. La cámara toma posición/rotación de la misma pose aplicada al arma; esto evita la separación entre mirada del jugador y ballesta de v04.

Cambiar sólo FOV o forzar primera persona conserva el origen en la cabeza, y ya resultó insuficiente. Reposicionar al personaje con Papyrus para aproximar la cámara introduce movimiento físico y latencia; se descarta. No se inyectará una cámara especial global ajena a la sesión.

## Contrato nativo

Script oculto `AstraSightNative`, funciones globales nativas:

- `bool IsAvailable()` indica registro y runtime soportado.
- `bool BeginSight(ObjectReference gun, int token, float initialYaw, float initialPitch)` acepta una petición exclusivamente para esa referencia/token. Valida geometría y prepara el anclaje en el hilo de actualización del juego, no en callbacks VM.
- `bool IsSightReady(ObjectReference gun, int token)` confirma anclaje y pose preparados; aceptar Begin no equivale a estar listo.
- `float[] CaptureAim(ObjectReference gun, int token, bool freeze)` devuelve `[yaw, pitch]` de la última pose aplicada. Devuelve un array vacío si no está disponible. `freeze=true` congela esa misma pose de forma coherente antes del preflight/disparo.
- `bool SetFrozen(ObjectReference gun, int token, bool frozen)` cambia el bloqueo de orientación de esa sesión.
- `bool EndSight(ObjectReference gun, int token)` desactiva únicamente la sesión que coincide; repeticiones y tokens antiguos son inocuos.

El identificador nativo siempre incluye referencia + token. Acceso VM se limita a peticiones/lectura de datos protegidos; mutaciones de escena y lectura de nodos ocurren en el hilo del juego. Operaciones ajenas al token actual no modifican la cámara ni una sesión posterior. Begin se rechaza si hay otra sesión pendiente/activa. Tras cargar/revertir, morir, perder referencia/3D o cambiar a una cámara no elegible, el override se invalida; cámara vanilla vuelve a sus funciones originales. Los menús pausan la pose sin acumular deltas. Los ganchos llaman a la función original cuando no son aplicables.

Aplicar nodos, actualizar world transforms y publicar yaw/pitch/cámara forma una transacción serializada con CaptureAim(freeze=true) y EndSight. Ninguna orientación preparada antes del freeze puede escribirse después de congelar. Después de retornar EndSight no puede haber escrituras nativas de esa sesión, de modo que Papyrus pueda restaurar la pose sin competencia. Las llamadas originales de hooks ocurren fuera del mutex; getters sólo leen un snapshot coherente y no aplican escena. Usar ObjectRefHandle, revalidar identidad del 3D y epoch interno para invalidar trabajo tras carga/revert. No retener un puntero crudo a una referencia descargada.

## Apuntado y anclaje

Convertir la orientación de mirada del jugador en dirección world, luego en local por la transpuesta de la raíz. Preservar convenciones v04: forward del arma −Y, yaw atan2(localX, −localY), pitch asin(localZ), unidades de grados en Papyrus. C++ utiliza radianes explícitos y cálculos finitos. Conservar bases/pivotes de los nodos al aplicar yaw/pitch; ninguna animación Fire/Reset escribe esos canales.

No acumular mirada oculta al superar límites o mover el ratón durante freeze/menú. Reconciliar orientación lógica del jugador con la pose aplicada en el hilo del juego, o consumir incrementos y rebasar su muestra al reanudar. La inversión inmediata del ratón tras exceder 80° debe empezar a bajar inmediatamente; no debe provocar un salto al descongelar. Probar ambos comportamientos.

El anclaje hereda giro y elevación. Su orientación local debe convertir el eje de cámara del motor al forward del arma. Elegir posición detrás del mecanismo con vistas comprobadas del NIF; validar que no queda dentro de mallas/piso entre los límites. No afirmar que la cámara y el virote comparten origen: su dirección coincide y su parallax debe medirse en juego. Las matrices del anclaje y ProjectileNode deben verificarse tras actualizar world transforms.

El nodo expresa una base **lógica**, forward +Y hacia el −Y del arma y up +Z. No copiar su quaternion Rz180 directamente al getter de primera persona. Derivar y conservar el adaptador entre la salida original FP y la base lógica de mirada del jugador, normalizar/validar la composición y aplicarlo a la base mundial del anclaje. Tratar explícitamente el espacio de GetTranslation/GetRotation; convertir respecto al parent de cameraRoot con escala cuando corresponda. NiCamera y TESCameraState no prueban por sus declaraciones una equivalencia world/local o de eje óptico. La calibración/composición se registra y su verificación visual en Skyrim sigue pendiente.

Papyrus no escribirá a la vez los mismos nodos mientras el controlador nativo posea la sesión. Fuera de ella puede restaurar la pose guardada. Un snapshot congelado alimenta los actuales guards de ProjectileNode y el consumo único antes de Weapon.Fire. El bloqueo se libera al comenzar recarga, salvo pausa/menú, conservando la lógica v04.

## Dependencias y fallos

Runtime objetivo 1.6.1170 + SKSE64 2.2.8. CommonLibSSE-NG y Address Library existentes; compilar con BuildTools instaladas, fijar revisiones/licencias de dependencias y no distribuir recursos vanilla. El perfil QA v05 habilitará sólo esta revisión y la Address Library requerida. No cambiar perfil seleccionado, guardados o runtime. Ausencia de DLL/anclaje/ready debe explicar el motivo y devolver los controles adquiridos; no degradar silenciosamente a la vista v04.

## Validación y límites

Tests del núcleo matemático y ciclo de sesión en C++, pruebas dirigidas PSC con fixtures, compilación Bethesda de todos los scripts, DLL x64 y export/version checks. Reimportar NIF, verificar anclaje/poses/pivotes/animaciones, shaders y geometría. Revisión de spec y calidad antes de entregar. ZIPs MO2/fuentes con CRC y hashes coherentes con la copia QA instalada.

La aceptación en Skyrim incluye entrar desde primera/tercera persona, vista fija respecto al arma al girar 360°/elevar, límites/menus/recarga, disparo e impactos, E mirando en cualquier dirección, muerte/carga/salida y control de cámara restaurado. Las pruebas de archivos no validan hooks/visibilidad/frame order dentro del motor. CK/navmesh y SSEEdit siguen pendientes según v04. No se colocará la ballesta en Tamriel en este cambio.
