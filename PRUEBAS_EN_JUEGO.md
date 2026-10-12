# Pruebas en juego — Astra Asedio v29

> Actualizado el 2026-10-12 para v29. El texto anterior de este archivo era de v22: describía otro paquete y trazas que ya no existen. Lo vigente del paquete está en `docs/README_v29.md` y `docs/QA_v29.md`.

Paquete: `dist/AstraAsedio_QA_v29_Unificado_MO2.zip`
**sha256 `ac8b04d42c0d4a4dd50f319281fd9efea826ca93aa05d1205674bc53bba6cee3`**, 3 068 559 bytes, 60 entradas.

> ⚠️ **Ese ZIP es anterior al renombrado de EDID del juego legacy de los voladizos** (`AstraAsedio_WhiterunTorres.esp`, ver `docs/2026-10-12-edid-legacy-voladizos.md`). Si vas a probar ahora, volvé a correr `python scripts/package_v29.py` y usá el sha que imprima: el contenido es el mismo salvo ese ESP, que cambió de `fabe09b28a3b…` a `cfccc9cd6bd2…`. En juego no cambia nada (solo nombres de editor de referencias que nacen desactivadas).

**Nada de esto está probado en el juego todavía.** Los informes lo declaran (`game_tested: false`). Lo que existe es verificación *fuera* del juego — contrato de release, NIF, ESP, clips y tests portables. Los renders y las mediciones geométricas no prueban la cámara real ni la puntería en Skyrim.

---

## Antes de abrir el juego

1. Cerrá Skyrim por completo —también desde el administrador de tareas—. Un script nuevo **no entra** con una recarga de partida.
2. Copiá tu partida.
3. Instalá el ZIP en MO2 y **desactivá las instalaciones anteriores** de Astra Asedio (paquete principal, atalaya, Whiterun, WhiterunTorres).
4. Activá **CUATRO** plugins, en este orden relativo:
   - `AstraAsedio.esp`
   - `AstraAsedio_WhiterunTorres.esp`
   - `AstraAsedio_Atalaya.esp`
   - `AstraAsedio_GuardAnim.esp`
5. **Open Animation Replacer no viene en el paquete.** Instalalo aparte, con la API *Animations V1*, y comprobá que SKSE lo cargue.
6. Requisitos: Skyrim SE 1.6.1170, SKSE 2.2.8, Address Library AE 1170. El paquete incluye **AstraSight 3.6.0** (API jugador 4 / NPC 1).
7. Activá el log de Papyrus (`bEnableLogging=1`). El camino del guardia **sólo** escribe trazas ahí.

> **El cuarto plugin es el sospechoso número uno si el guardia no anima.** Sin `AstraAsedio_GuardAnim.esp` ningún submod de OAR puede aplicar; el resto del mod funciona igual.
>
> `AstraAsedio_Whiterun.esp` (la ballesta baja de la puerta de Carrera Blanca) **no es parte de este paquete** y su guardia no puede animar: el sistema de operadores está cableado a los dos puestos de los voladizos. No lo actives.

## Qué capturar antes de cerrar el juego

- **Los carteles en pantalla que empiecen con `Astra:`** (sólo camino del jugador).
- **`AstraSight.log`** y **`Papyrus.0.log`**.

| Camino | Dónde avisa |
|---|---|
| **Jugador** (torreta, atalaya) | Cartel en pantalla: `Astra: <motivo>` **y** log |
| **Guardia** (voladizos) | **Sólo `Papyrus.0.log` y `AstraSight.log`** |

Si el guardia no anima, **no esperes cartel**. Buscá `AstraAsedioGuard` y `guard v29` en los logs.

### Lectura del log del guardia

Orden esperado en una sesión sana:

| Línea | Qué significa |
|---|---|
| `AstraSight 3.6.0 …` | Está cargada la DLL correcta. Si dice 3.5.x, hay paquete viejo instalado. |
| `AstraGuardNative API1 frame pump … OAR Animations V1=True (module loaded=True)` | OAR cargó y concedió la API. Con `False` el guardia nunca animará. |
| `guard v26 acquired gun=… actor=… package=14000B90 … holdRequested=true` | El runtime tomó el puesto. La traza conserva el prefijo `v26` por historia. |
| `guard v29 holding gun=… actor=… yaw=…` | Entró en la pose (≈0,6 s tras la solicitud). |
| `guard v29 pose … handErrorL= handErrorR=` | Telemetría cada 2 s por puesto. Lo esperado son **≈3 u** (estatura nórdica 1,03). **20 u o más = la pose no se está aplicando.** No bloquea nada. |
| `moveRefused=` (dentro de `guard v29 pose`) | Por qué no pudo girar más (baranda, falta de apoyo). `none` = nada lo impidió. |
| `guard real projectile gun=… speed=5400 blast=…` | Se lanzó un virote real y el NIF hizo su `Fire`. |
| `guard v29 hold re-request …: no own clip sample for 3 s` | El clip dejó de muestrear (normal fuera de cámara). Se reemite una vez; **no cancela**. |
| `AstraAsedio city retired legacy=… replacement=…` | Reparación de partida vieja: desactivó el puesto v13/v17 de un voladizo. Debe aparecer una vez por voladizo tras cargar. |
| `guard cancel … reason=…` | Fin de la operación. |

**No deben aparecer** (eran los fallos de v23–v28):

- `clause=running package has no owned idle override`
- `hold replacement not observable`
- `Astra guard v27: backoff …` repetido en bucle
- `Astra guard v27: operator refs missing` (falta `AstraAsedio_WhiterunTorres.esp`)

---

## A. El jugador no debía cambiar (control de regresión)

Montá la **torreta principal** y la **atalaya**. La cámara de mira debe entrar, apuntar y disparar como en v21–v28.

1. Entrar con E: la vista sale desde la cola de la ballesta, con el arma delante, el anillo del alza y el guion dentro.
2. Girar despacio una vuelta completa a cada lado, en tiro horizontal: la cámara **no** debe saltar a tus ojos en ningún giro.
3. Repetir a +35° y +80°. Al elevar, la cámara avanza hacia el alza; a +80° el anillo se ve grande alrededor del guion.
4. `AstraSight.log`: anotar cualquier `camera deviation start` con desvío de más de ~10 u que dure más de un instante.

## B. El guardia sostiene la ballesta

Las dos estaciones de los **voladizos** son los únicos puestos de guardia animados (`04000B70/71` al este, `04000B80/81` al oeste, en `AstraAsedio_WhiterunTorres.esp`).

5. Acercate a un voladizo. En menos de un segundo el operador debe **subir las manos y dejarlas sobre las empuñaduras**, sin correcciones visibles. Anotá `handErrorL`/`handErrorR` del primer `guard v29 pose`.
6. La pose **no** debe caerse al abrir consola, inventario o diálogo (en v29 los menús pausan, no cancelan).

## C. Seguimiento y obstáculos

7. Pasá por delante dentro del sector (±60°): ballesta y guardia giran juntos, a 20°/s como máximo. Los pies **se deslizan** durante el giro: es lo aceptado por el contrato del clip, no una falla.
8. Local no hostil / guardia de Whiterun / residente: se ignora para apuntar. Jugador y visitantes sí se siguen.
9. Baranda u obstáculo impidiendo girar: el guardia se queda en el último ángulo válido **sin soltar la pose**; anotá el `moveRefused=` de esos frames.

## D. Disparo

10. Con un **enemigo hostil en combate** dentro del sector y alcance (hasta 6 000 u): un virote real por ciclo, con `guard real projectile` en el log. El virote **no** persigue al objetivo en vuelo.
11. Debe **no** disparar: al jugador, a aliados, a neutrales cruzando la trayectoria, con obstáculo de por medio, fuera del sector o a otra altura no alcanzable. Anotá el caso y la línea `guard v29 pose`/`guard cancel` asociada.
12. Enfriamiento entre disparos: 2,5 s.

## E. Ciclo de vida

13. Muerte, stagger, descarga/carga de celda, salir y volver a entrar, guardar y cargar durante el ciclo: el puesto se recupera o se cancela con motivo nombrado, sin controles bloqueados.
14. Que el jugador tome el puesto del voladizo **no** debe ser posible; si lo logra, anotá con qué referencia (`prid`) y qué cartel apareció.

## F. Pendientes de siempre (ajenos a la pose del guardia)

15. Daño del virote con `getav health` y atribución de la muerte.
16. Virote no recogible; apoyado en todo su largo si cae o rebota.
17. Sonido una vez por virote; ráfaga con clics rápidos; Tab con un disparo en curso; Sprint.

---

## Cómo reportar

Con esto alcanza para diagnosticar sin adivinar:

1. El sha del ZIP que instalaste.
2. Los cuatro plugins activos: sí / no.
3. OAR instalado y versión de OAR: sí / no.
4. Qué bloques (A–F) pasaron y cuáles no.
5. Las líneas **textuales** de `AstraSight.log` y `Papyrus.0.log` del tramo probado, y los carteles `Astra:` si aparecen.
