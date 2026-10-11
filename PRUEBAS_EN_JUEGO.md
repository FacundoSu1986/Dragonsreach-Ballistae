# Pruebas en juego — Astra Asedio v22

Paquete: `dist/AstraAsedio_QA_v22_Completo_MO2.zip`
**sha256 `2e5d5791d99f249de16145397a18f9f9254215e027ffba8d0177960fb5cc178b`**, 2 605 744 bytes, 44 entradas. Comprobá que sea el que instalaste.

**Nada de esto está probado en el juego todavía.** Los informes lo declaran (`game_tested: false`). Lo que existe es verificación *fuera* del juego — contrato de release, NIF, ESP, clips. Los renders y las mediciones geométricas no prueban la cámara real ni la puntería en Skyrim.

---

## Antes de abrir el juego

1. Cerrá Skyrim por completo —también desde el administrador de tareas—. Un script nuevo **no entra** con una recarga de partida.
2. Copiá tu partida.
3. Instalá el ZIP en MO2 y **desactivá las instalaciones anteriores** de Astra Asedio (paquete principal, atalaya, Whiterun) en el panel izquierdo.
4. Activá **CUATRO** plugins, el principal primero:
   - `AstraAsedio.esp`
   - `AstraAsedio_WhiterunTorres.esp`
   - `AstraAsedio_Atalaya.esp`
   - `AstraAsedio_GuardAnim.esp`
5. **Open Animation Replacer no viene en el paquete.** Instalalo aparte y comprobá que SKSE lo cargue.
6. Entrá con `coc AstraAsedioTest`.

> **El cuarto plugin es el sospechoso número uno si el guardia no anima.** El README de v21 mandaba activar tres y lo omitía; el de v22 ya lista los cuatro. Si `AstraAsedio_GuardAnim.esp` no está tildado, **ningún** submod de OAR puede aplicar y el guardia no opera la ballesta — el resto del mod funciona igual.

## Qué capturar antes de cerrar el juego

Esto es lo que hace que tu feedback sirva de algo:

- **Los carteles en pantalla que empiecen con `Astra:`.** Son el autodiagnóstico del script: dicen el motivo exacto del rechazo.
- **`Papyrus.0.log`** y **`AstraSight.log`**.

Y una asimetría que importa y no es obvia:

| Camino | Dónde avisa |
|---|---|
| **Jugador** (torreta, atalaya) | Cartel en pantalla: `Astra: <motivo>` |
| **Guardia** (voladizos) | **Sólo `Papyrus.0.log`**, vía `Debug.Trace` |

Si el guardia no anima, **no esperes cartel**. Buscá `AstraAsedioGuard` en `Papyrus.0.log`.

### Tabla de motivos del camino del jugador

| Motivo | Qué significa |
|---|---|
| `SKSE_MISSING` | No arrancaste con SKSE64 |
| `NATIVE_SIGHT_MISSING` | Falta `AstraSight.dll` 3.5.0 de esta versión |
| `NATIVE_API_MISMATCH` | DLL y scripts de versiones distintas: reinstalá el paquete completo |
| `NATIVE_SIGHT_UNAVAILABLE` | La mira nativa no está disponible |
| `PROPERTY_*_NONE` | Falta una property: el ESP no es el de este paquete |
| `SESSION_NOT_RUNNING` | La quest de control no inició |
| `CAMERA_STATE_UNSUPPORTED` | Estás en cámara especial: salí y reintentá |
| `CAMERA_ENTRY_FAILED` | No se pudo alinear la mirada |
| `NATIVE_SIGHT_BEGIN_FAILED` | La mira rechazó la entrada |
| `SESSION_ENTRY_CANCELLED` | Entrada cancelada o sesión ocupada |

Ninguno de estos depende del pivote: bajar o no la torreta no cambia esta lista.

---

## A. El jugador no debía cambiar (control de regresión)

Montá la **torreta principal** y la **atalaya**. La cámara de mira debe entrar, apuntar y disparar **como en v21**. Esto es lo que v22 no debía tocar: la torreta del jugador sigue en pivote 153 y conserva la mira nativa.

1. Entrar con E: la vista sale desde la cola de la ballesta, con el arma delante, el anillo del alza y el guion dentro.
2. Girar despacio una vuelta completa a cada lado, en tiro horizontal. La cámara **no** debe saltar a tus ojos en ningún giro.
3. Repetir la vuelta desde otro punto del puesto y a +35° y +80°. Al elevar, la cámara avanza hacia el alza; a +80° el anillo se ve grande alrededor del guion.
4. `AstraSight.log`: anotar cualquier `camera deviation start` con dev de más de ~10 u que dure más de un instante.

## B. Los voladizos son del guardia

Las cuatro referencias de `AstraAsedio_WhiterunTorres.esp` quedaron como puestos **exclusivos del guardia**.

5. Andá a un voladizo de Carrera Blanca y **activálo como jugador**. No debe entrar a la mira ni dejarte operar. Anotá el texto exacto si aparece algún cartel `Astra:`.
6. La atalaya y la torreta principal **sí** deben seguir siendo tuyas.

## C. El guardia anima

7. Acercate a un voladizo con un guardia apostado. Debe **apoyarse en la ballesta** con las manos a la altura del puesto bajo — sin subir los brazos por encima del hombro — y **disparar** con el gesto de disparo.
8. Si no lo hace, mirá `Papyrus.0.log`. Las dos únicas trazas posibles son:
   - `AstraAsedioGuard: enable OAR and AstraAsedio_GuardAnim.esp to operate the NPC.` → falta OAR o el cuarto plugin.
   - `AstraAsedioGuard: missing or invalid model controls; controller stopped.` → el NPC no tiene los controles de modelo que el clip necesita.

## D. Puntería

9. Apuntá casi en horizontal con la punta del guion en el centro del anillo, sobre el blanco de 10 m y el de 30 m. Con el cero a 75 m, el modelo predice que el virote pega **por encima** del punto de mira: ~3 cm a 10 m y ~28 cm a 30 m (el máximo, ~32 cm, cae hacia los 40 m; a 75 m, en el punto; a 100 m, ~66 cm por debajo). Eso es correcto, no una falla. Anotá la diferencia real.
10. Disparar a +35° y +80° a algo lejano y comprobar que el guion sigue marcando dónde cae.

## E. Pendientes de siempre (ajenos a v22)

11. Daño con `getav health` (nominal 35 + 10 + explosión 150) y atribución de la muerte.
12. Virote: no recogible; si cae o rebota, apoyado en todo su largo.
13. Sonido una vez por virote; ráfaga con clics rápidos; Tab con un disparo en curso; Sprint.
14. Guardar y cargar en cada fase, salir de celda, morir: sin controles bloqueados.

---

## Cómo reportar

Con esto alcanza para diagnosticar sin adivinar:

1. El sha del ZIP que instalaste.
2. Los cuatro plugins activos: sí / no.
3. OAR instalado: sí / no.
4. Qué bloques (A–E) pasaron y cuáles no.
5. Los carteles `Astra:` textuales, y las líneas relevantes de `Papyrus.0.log` y `AstraSight.log`.
