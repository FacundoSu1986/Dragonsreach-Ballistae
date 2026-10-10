# Revisión técnica: Ballesta de asedio Astra v07

Fecha: 2026-10-04. Revisión técnica, estética y funcional para combate antiaéreo (caza de dragones), en cuatro ejes: mecánica, física y balística, lore, y Creation Kit con optimización.

**Qué se revisó.** Hashes SHA-256, iguales a los de `reports/assets_verified.json` y `reports/plugin_build.json`:

| Archivo | SHA-256 |
|---|---|
| `mod/AstraAsedio.esp` | `047849cb…c335` |
| `mod/meshes/AstraAsedio/torre.nif` | `2eef365d…e402` |
| `mod/meshes/AstraAsedio/ballesta.nif` | `bddd2c48…045d` |
| `mod/meshes/AstraAsedio/virote.nif` | `f27c96e4…1969` |

También se revisaron `AstraAsedioActi.psc`, `native/src/*.cpp` y los scripts de build. **No se modificó nada del mod.**

**Alcance.** El encargo hablaba de una ballesta de mano (empuñadura, encare, retroceso, `1stPerson*.nif`). Astra v07 es otra cosa:
- una ballesta de asedio fija sobre una torre, hecha con un activador (ACTI), Papyrus y el SKSE `AstraSight.dll`;
- gira 360° y eleva de −5° a +80°;
- dispara con `Weapon.Fire` desde el activador y consume virotes de acero del jugador.

Cada criterio se tradujo al emplazamiento: manivela y puesto del operador, cámara de mira y respuesta al disparo. Lo que no aplica se marca N/A. El anexo A cubre una posible variante de mano.

**Cómo leerla.**
- Cada afirmación lleva su origen:
  - **[MEDIDO]**: leído en los archivos, con los scripts de `docs/revision/medicion/`;
  - **[MODELO]**: cálculo con supuestos explícitos;
  - **[HEURÍSTICA]**: regla práctica, no medida;
  - **[A VERIFICAR EN JUEGO]**.
- Prioridades:
  - **P0**: bloquea el objetivo "caza de dragones";
  - **P1**: importante;
  - **P2**: mejora.
- Unidades: 1 m = 70 u (`config.json`) y 1 unidad Havok = 69,99 u.

## Resumen ejecutivo

1. **P0. El daño no sirve para cazar dragones.** El daño nominal es 20 por golpe (WEAP 10 + AMMO 10). Un dragón básico necesita 40 golpes y uno legendario, 165–175, contando su salud base (cota inferior).
   - La balista dwemer vanilla, un virote pesado disparado por un objeto, hace 80–250 de daño con una explosión.
   - Propuesta: ≈195 por golpe → 5 a 18 golpes, según el dragón.
2. **P1. La caja Havok del virote es la de un virote de mano.** Cubre el 20 % de sus 4,07 m (en los vanilla, la caja cubre el 84–97 %) y su tensor de inercia quedó girado 90° respecto de la caja.
3. **P1. Virotes recogibles.** El proyectil es recogible y la munición es jugable, así que los virotes de asedio terminan en el inventario y sirven en cualquier ballesta de mano.
4. **P1. La cabeza barre el puesto del operador.** Entre +15° y +45° de elevación, la parte trasera del carro pasa por el lugar donde está parado el operador.
5. **P1. La mira apunta alto.** La cámara está 20,4 u por encima del ánima y paralela a ella [MEDIDO]. Según el modelo de caída, el impacto cae 22 u bajo la retícula a 10 m y 222 u a 100 m. Inclinar la cámara −1,38° deja el cero a 75 m. Se contrasta con los blancos de 10 y 30 m que ya tiene la celda.
6. **P1. El disparo es mudo.** El arma clonada de la trampa no tiene sonido de disparo [A VERIFICAR EN JUEGO].
7. Bien resuelto:
   - virote con la punta en el origen;
   - plugin estructuralmente limpio (`verificar_plugin.py`: `ok`);
   - texturas 100 % vanilla;
   - cadena de nodos clara;
   - secuencias Gamebryo correctas para un activador;
   - pruebas de contrato extensas.

---

## 1. Resumen de diseño y arquitectura mecánica

### Ficha medida [MEDIDO]

| | `torre.nif` | `ballesta.nif` | `virote.nif` |
|---|---|---|---|
| Triángulos / vértices | 18.020 / 20.769 | 19.754 / 16.227 | 480 / 530 |
| Shapes | 4 | 17 | 1 |
| Tamaño (u) | 649 × 563 × 549 | 269 × 361 × 180 | 14,7 × 284,6 × 11,9 |
| BSXFlags | 10 (Havok, Complex) | 139 (Animated, Havok, Complex, Articulated) | 194 (Havok, Dynamic, Articulated) |
| Colisión | MOPP + CompressedMesh, STATIC/FIXED, WOOD | solo la base fija (una caja como malla) | `bhkBoxShape` del virote de acero DLC1 |
| Animación | — | Fire 0,30 s (suelta a los 0,10 s), Reset 1,20 s; CLAMP, sin text keys | — |

Cadena cinemática de `ballesta.nif`: `AstraBallesta` (fija) → `CTRL_GIRO_360` (pivote en z 135,5) → `CTRL_ELEVACION` (pivote en z 153). De la elevación cuelgan:
- los brazos `CTRL_BRAZO_I/D`, que giran ±0,24 rad (13,75°) entre armado y suelto;
- las cuerdas `Cuerda_I/D`, que se estiran por escala (la cuerda recorre 2,42 m);
- `VIROTE_VISUAL`, que se oculta por escala;
- `ProjectileNode` en (0, −224, 19,6);
- `AstraSightCameraNode` en (0, 80, 40).

`OperatorNode` (73,5, 101,5, 119) cuelga de la raíz **fija** (`build_assets.py:380`).

El disparo hace `player.RemoveItem(SteelBolt, 1, true)` y luego `Launcher.Fire(Self, ShotAmmo)` (`AstraAsedioActi.psc:1587–1588`).

### Ergonomía, encare y retroceso, traducidos al emplazamiento

- **Empuñadura → puesto y mandos.**
  - E entra y sale; el ratón apunta; Ataque dispara; Sprint alterna individual y continuo.
  - Los mandos respetan las reasignaciones y el contrato de entrada está muy probado.
  - El punto débil es el puesto (ver el primer hallazgo).
- **Encare → imagen de mira.**
  - La cámara está 304 u detrás de la boca y 20,4 u por encima, paralela al ánima.
  - La retícula vanilla queda centrada y el arma sigue al ratón 1:1.
  - El paralaje y la caída se tratan en §2 (cero de mira).
- **Retroceso → respuesta al disparo.**
  - En un arma montada el retroceso lo absorbe el montaje; la sensación de impacto tiene que venir de la respuesta.
  - Propuesta:
    - sacudida de cámara de ≈0,2 s, que termine antes del Reset;
    - `Game.ShakeController` en el commit;
    - **sin** desplazar la mira entre disparos, porque el modo continuo depende de que la puntería se mantenga.
- **Combate móvil o estático.** Es estático. La "movilidad" es la velocidad de giro y elevación, que hoy es instantánea (ver hallazgos).

### Hallazgos

**P1 [MEDIDO]. La cabeza que gira barre el puesto del operador.** Lo mide `medicion/medir_barrido_operador.py`.

El puesto nominal es la manivela, en `OperatorNode`, a r = 125,3 u del eje de giro. Con la cápsula del jugador (18 u, la misma holgura del navmesh en `build_plugin.py`), su cuerpo ocupa r 107–143 y z ≤ 125. Vértices que giran y entran en ese volumen, según la elevación:

| Elevación | −5° | 0° | +15° | +30° | +45° | +60° | +80° |
|---|---|---|---|---|---|---|---|
| Vértices dentro de la cápsula | 12 | 0 | 2.592 | 2.741 | 526 | 0 | 0 |
| Radio máximo bajo z 125 | 108,7 | 105,7 | 147,1 | 130,9 | 113,4 | 92,1 | 72,4 |

- Entre +15° y +45° de elevación, que es la banda típica de tiro antiaéreo, la culata, la madera, la cuerda y el virote del carro atraviesan al operador en algún ángulo de giro. Llegan a r 147 a la altura del pecho (z 107).
- Desde la mira no se ve. En tercera persona y para los NPC, sí.
- Si algún día la cabeza tiene colisión, empujaría al jugador fuera de la torre.

Opciones:
- **(a) Recomendada.** Acortar el voladizo trasero para que todo lo que gira por debajo de z 125 quede en r ≤ 95 u. Se hace con un script de corrección del `.blend`, siguiendo el patrón de `scripts/mechanism_source_fixes.py`.
- (b) Llevar el puesto a r ≥ 170 u. Exige ampliar el disco transitable, que hoy mide r 150,5.
- (c) Hacer la manivela solidaria al carro y reubicar al jugador **solo al salir**, según el giro final. Respeta la regla de la spec v05 de no mover al jugador en cada frame.

**P1 [A VERIFICAR EN JUEGO]. Disparo mudo.**
- El WEAP clonado de `DLC1TrapCrossbowWeapon01` no tiene `SNAM` ni `XNAM`; la trampa vanilla tampoco [MEDIDO].
- La ballesta de mano de Dawnguard (`DLC1CrossBow`) usa `WPNCrossbowFire` y `WPNCrossbowFire2D`.
- Hoy solo suena el vuelo del proyectil (`WPNBowProjectileSD`).
- Ideal: un SNDR propio más grave, más un trinquete que suene durante el Reset.

**P2 [MEDIDO]. El giro no tiene inercia.**
- En modo mira, el movimiento del ratón pasa 1:1 a la ballesta (`native/src/Core.cpp:35`).
- `YawSpeed` y `PitchSpeed` (40 y 20 °/s) solo actúan en el camino por teclas (`AstraAsedioActi.psc:1340–1351`).
- Así, una cabeza de 3,84 m de envergadura gira de golpe.
- Propuesta opcional y configurable: limitar la velocidad angular (≈90 °/s de giro y 45 °/s de elevación) con suavizado críticamente amortiguado en `Session::update`.
- Contrapartida: el ratón se siente "pesado". Por eso debe ser opcional.

**P2 [MEDIDO]. La recarga no muestra el mecanismo.**
- Reset anima brazos, cuerdas y virote; el torno, el trinquete y la garra son geometría estática, sin nodo propio.
- Propuesta:
  - separar `CTRL_TORNO` (da vueltas durante Reset) y `CTRL_TRINQUETE` (el linguete oscila);
  - una garra que acompañe al centro de la cuerda, que recorre 2,42 m.
- El ciclo de 1,5 s lo pidió el usuario en v07. Un torno con engranaje dwemer lo justifica dentro del lore (§4).

**Observación [MEDIDO]. No hay animación vanilla de operador humano.** Los `IDLE Ballista*` de Dragonborn pertenecen al centurión dwemer (`BCBehavior.hkx`) y `DLC2BallistaGroundAmbush01` es su mueble de emboscada. Una animación de manivela en tercera persona tendría que ser propia.

**[MODELO]. Coherencia física del virote.** Se suponen un astil de roble de 6 cm y una punta de hierro.
- El virote de 4,07 m pesaría ≈9–10 kg. A 77 m/s (5400 u/s) lleva ≈28 kJ.
- Con 2,5–3 m (≈3 kg) a 70 m/s son ≈7 kJ: cuatro veces menos energía para la misma máquina, con brazos de 13,75° y 3,84 m de envergadura.
- Ese largo además iguala la escala vanilla: `LargeBolt01`, el virote de la balista dwemer, mide 177,8 u = 2,54 m [MEDIDO].
- Recomendación: virote de 2,5–3,0 m.

---

## 2. Parámetros matemáticos y de balística

### Valores actuales contra vanilla [MEDIDO en los ESM del runtime]

| | Astra v07 | Flechas | Virotes DLC1 | Balista dwemer (trampa) | Balista centurión DLC2 | Catapulta CW |
|---|---|---|---|---|---|---|
| Tipo de PROJ | Arrow | Arrow | Arrow | Missile + explosión | Arrow | Missile + explosión |
| speed (u/s) | 5400 | 3600 | 5400 | 2800 | 3600 | 4000 |
| Gravedad (mult.) | 0,35 | 0,35 | 0,35 | 0,80 | 0,35 | 1,00 |
| Radio de colisión | 0,5 | 0,5 | 0,5 | 1,0 | 0,5 | n/m |
| Impact force | 1,0 | 1,0 | 1,0–1,5 | 50 | 1,0 | 0 |
| ¿Recogible? | sí | sí | sí | no | no | n/m |
| Daño | WEAP 10 + AMMO 10 | AMMO 7–25 | AMMO 10 (acero), 14 (dwemer) | EXPL 80/150/175/200/225/250, radio 320; AMMO 0, WEAP 0 | AMMO 12 + arco 16/24/32 | EXPL 30, radio 320 |

Notas:
- "n/m" significa no medido.
- La ballesta de mano de Dawnguard tiene 19 de daño (la dwemer, 22).
- Las armas de trampa `DLC1TrapCrossbowWeapon01–06` van de 10 a 35; Astra clona la 01.
- La munición de la balista del centurión no es jugable (flags 0x7) y su proyectil no se puede recoger.

### Daño contra dragones

Salud base [MEDIDO]: 500 de `DragonRace` más el offset del NPC.

| NPC | Nivel | Salud base | Golpes hoy (20) | Golpes con la propuesta (195) |
|---|---|---|---|---|
| EncDragon01 | 10 | 800 | 40 | 5 |
| EncDragon02 | 20 | 1.200 | 60 | 7 |
| EncDragon03 Frost | 30 | 1.522 | 77 | 8 |
| EncDragon04 | 40 | 1.800 | 90 | 10 |
| EncDragon05 | 50 | 2.500 | 125 | 13 |
| DLC1EncDragon06 | 62 | 2.800 | 140 | 15 |
| DLC2EncDragon06 | 58 | 2.900 | 145 | 15 |
| DLC1EncDragon07 | 75 | 3.300–3.500 | 165–175 | 17–18 |

- Estos NPC tienen el **autocálculo** activado: la salud real es mayor y las cifras son una **cota inferior**. Hay que medirla con `getav health`.
- Defensas medidas:
  - la piel (`SkinDragon`, `skinDragonPurple`) tiene armadura 0;
  - `AbDragonFire` da resistencia al fuego de 50 % y debilidad a la escarcha de 25 %;
  - no tienen resistencia física racial.
  - Para atravesar escamas no hace falta un mecanismo de penetración de armadura: lo que falta es daño.
- **P0. Hoy, con 20 por golpe y un ciclo de 1,5 s, hacen falta entre 1 y 4,4 minutos de impactos perfectos.** Además no se midió cómo compone el motor el daño cuando el tirador es un objeto (el propio repo lo declara: "in-game damage not verified").

**Fórmula de daño proporcional.**

```
D_golpe = (daño_WEAP + daño_AMMO) · k_motor + daño_EXPL
N_golpes = ceil(HP / D_golpe)
```

`k_motor` es la composición del motor para un tirador que no es actor. Se mide en juego; mientras tanto se toma como 1.

**Propuesta.**
- WEAP 35 (igual que `DLC1TrapCrossbowWeapon06`) + AMMO 10 + una EXPL nueva clonada de `TrapBallistaBoltExplosion02`, con daño 150, radio 128 (bajado de 320) y fuerza 20. Total: ≈195 por golpe.
- **Por qué una explosión.** Es el patrón medido de Bethesda para un virote pesado que dispara un objeto: la balista dwemer pone todo su daño en la EXPL, con el arma y la munición en 0. Así el daño no depende de quién figure como tirador.
- **Control [HEURÍSTICA].** Escalar la ballesta de mano (19 + 10 = 29) por √energía, con un virote de 3 kg a 70 m/s (≈7 kJ, contra ≈0,14 kJ de un virote de mano), da 29·√51 ≈ 207. Las dos referencias coinciden en ≈200.
- **Alternativa sin daño en área.** Subir solo el WEAP (≈185). Es más simple, pero queda atada a `k_motor`.
- **Variante por niveles.** Como las trampas vanilla 01–06: tres tiers de EXPL (80 / 150 / 250), elegidos por el nivel del jugador al iniciar la sesión.

### Trayectoria y caída [MODELO]

Supuestos: g = 0,35 · 9,81 m/s² = 240,3 u/s² y v0 = 5400 u/s, sin multiplicadores del motor.

| Distancia | Tiempo de vuelo | Caída | Impacto bajo la retícula hoy (paralaje 20,4 u + caída) |
|---|---|---|---|
| 10 m (700 u) | 0,13 s | 2 u | 22 u (0,32 m) |
| 30 m (2100 u) | 0,39 s | 18 u | 39 u (0,55 m) |
| 50 m (3500 u) | 0,65 s | 50 u | 71 u (1,01 m) |
| 75 m (5250 u) | 0,97 s | 114 u | 134 u (1,91 m) |
| 100 m (7000 u) | 1,30 s | 202 u | 222 u (3,18 m) |
| 150 m (10500 u) | 1,94 s | 454 u | 475 u (6,78 m) |

**Prueba falsable** con la celda actual:
- Apuntando al centro, el blanco de 10 m tiene que recibir el impacto ≈22 u más abajo y el de 30 m, ≈39 u más abajo.
- El de 10 m valida sobre todo el paralaje; el de 30 m, la gravedad.
- Si no da eso, el modelo de gravedad del motor es otro: recalibrar antes de tocar nada.

### Cero de mira (P1)

El paralaje es geométrico [MEDIDO]: la cámara está en (0, 80, 40) y la boca en (0, −224, 19,6), las dos con la misma orientación Rz180. Inclinar `AstraSightCameraNode` **−1,38°** pone el cero a 75 m:

```
δ = atan((20,4 + caída(75 m)) / (5250 + 304)) = atan(134,0 / 5554) = 1,382°
```

Error restante con el cero fijo (u; + = el impacto queda alto):

| Elevación | 10 m | 30 m | 50 m | 100 m | 150 m |
|---|---|---|---|---|---|
| 0° | +2 | +19 | +21 | −46 | −214 |
| 45° | +2 | +25 | +36 | +13 | −81 |
| 80° | +3 | +34 | +63 | +121 | +161 |

- **Refinamiento opcional en el nativo.** Para tiro elevado, la caída perpendicular a la línea de mira se reduce por cos θ (regla del tirador). Aplicar δ(θ) = atan((20,4 + 113,6·cos θ)/5554) da 1,38° a 0°, 1,04° a 45° y 0,41° a 80°, y anula el error a 75 m en cualquier elevación.
- **Ojo con los tests.** El preflight nativo tolera hasta 2,56° entre direcciones (dot ≥ 0,999). Aun así, `tests/test_v07_camera_contract.py` y `tests/test_native_sight.py` deben actualizarse, y la calibración se confirma en juego.
- **Adelanto.** Adelanto = velocidad del objetivo × tiempo de vuelo. A 100 m, son 1,3 m por cada m/s que se mueva el dragón. La retícula vanilla no lo indica.

### Dispersión (opcional)

- Sin dispersión el disparo es determinista, que es lo mismo que hace el motor con un tirador no-actor.
- Propuesta para dar "precisión mecánica" y penalizar el abuso del modo continuo:
  - σ base de 0,15° (≈26 cm a 100 m);
  - +0,1° por cada disparo encadenado, hasta 0,6° (≈1,05 m a 100 m);
  - recuperación a 0,3 °/s.
- Se aplicaría en el nativo al congelar la pose (`CaptureAim(freeze=true)`), con una semilla fija en los tests. Entra en la tolerancia de 2,56° del preflight.

### Otros parámetros recomendados

| Parámetro | Hoy | Recomendado | Referencia vanilla |
|---|---|---|---|
| speed / gravedad | 5400 / 0,35 | juego: 5400 / 0,35; realista: 4200–4500 / 0,5 con un virote de 2,5–3 m | virotes DLC1: 5400 / 0,35; balista dwemer: 2800 / 0,8 |
| Radio de colisión del PROJ | 0,5 | ≈ radio del astil (2–4 u; medirlo en el `.blend`) | balista dwemer: 1,0 |
| Impact force | 1,0 | 20–50 | balista dwemer: 50 |
| Stagger del WEAP (DNAM+96) | 0,0 | 1,0 contra blancos terrestres | — |
| Flags del PROJ | CanBePickedUp + Supersonic | Supersonic + Explosion, **sin** CanBePickedUp | centurión DLC2: sin CanBePickedUp |

### Havok, cajas de impacto e incrustación

- **[MEDIDO] Punta en el origen ✓.** En `virote.nif` la punta está en el origen y el avance es +Y (Y va de −284,55 a 0). Se clava por la punta, como los vanilla.
- **Cajas de impacto contra el dragón.** La detección usa los cuerpos Havok del esqueleto vanilla del dragón (sin cambios) y el radio de colisión del PROJ. Subir el radio al del astil hace que el virote visible y el impacto coincidan.
- **P1 [MEDIDO]. La caja Havok del virote es la del virote de acero DLC1** (`build_assets.py:437–447` la copia sin escalar).
  - Mide 57,2 × 3,26 × 0,25 u y está centrada en Y −29,3: **cubre el 20,1 %** de un virote de 284,6 u.
  - En los vanilla esa misma caja cubre el 96,9 % de `boltprojectile.nif` y `dwarvenboltprojectile.nif` (virote visible de 21 u) y el 83,9 % de `bolts.nif` de la balista DLC2 (68 u).
  - **El tensor de inercia quedó girado 90°.** El cuerpo se reescribió con otra rotación (cuaternión 0, 0,707, 0,707, 0; el donante usa 0, 0, 1, 0) y los semiejes permutados, pero la inercia (1,328 / 0,044 / 1,336) se copió tal cual.
    - En Havok, la caja y la inercia comparten el espacio del cuerpo. Por eso el eje de menor inercia ya no es el largo del virote sino el de 0,25 u de espesor.
    - Los valores crudos están [MEDIDO]; la lectura sigue la semántica estándar de Havok.
    - `colision_caja.py` lo deja ver: la razón contra la fórmula de caja da 0,16 y 1.471, fuera del rango vanilla de 1,2 a 471.
  - **Cuándo importa.** No en vuelo ni con el virote clavado. Sí cuando rebota, cae o se suelta del inventario: el 80 % trasero atraviesa el suelo y gira de forma incoherente.
  - **Arreglo:**
    - caja ajustada al **astil** (no a las plumas), de largo completo y centrada en Y −142,3;
    - inercia expresada en el mismo marco que la caja;
    - `bhkRadius = min(semieje menor, 0,1)` (regla medida en 2.667 de 2.684 cajas);
    - masa > 0 ⇔ inercia > 0 (regla medida en 1.194 de 1.194 cuerpos);
    - masa 15–20 y restitución 0,1 en vez de 0,4 [HEURÍSTICA: no existe un donante vanilla dinámico de ese tamaño; la escala de la inercia por la fórmula de caja también es heurística, mediana vanilla ×7,1];
    - mantener la capa PROJECTILE, `MATERIAL_ARROW` y SPHERE_STABILIZED, como el vanilla.
- **[MEDIDO] La cabeza que gira no tiene colisión** (`build_assets.py:428`: una caja sobre la parte fija). Es lo correcto mientras el operador esté dentro del barrido (§1). Resuelto eso, la referencia es la catapulta vanilla:
  - un cuerpo ANIMSTATIC en el nodo móvil, con `bhkCollisionObject` flags 0x89, y otro STATIC en la base;
  - en Astra convendría solo en los brazos, por encima de la cabeza del operador y fuera de la trayectoria del proyectil.
- **P2 [MEDIDO]. Inercia en cuerpos FIXED.** Los cuerpos de la torre y la ballesta tienen masa 0 e inercia [1, 0, 0]. Havok no la usa en cuerpos FIXED, pero en las cajas vanilla masa 0 va con inercia 0 en 383 de 383. Ponerla en cero.
- **Incrustación en terreno y mallas dinámicas.** Es el comportamiento vanilla de los proyectiles Arrow. Debería mantenerse si el PROJ sigue siendo Arrow aunque lleve explosión, como los virotes de fuego DLC1 (Arrow + EXPL), pero que el virote siga clavado después de explotar está [A VERIFICAR EN JUEGO]. Con el modo continuo se acumulan virotes clavados: hay que probar 50 o más disparos y mirar los FPS.

---

## 3. Pipeline técnico de integración (Havok, NifSkope y Creation Kit)

### Records

`verificar_plugin.py` (skill `asset-nuevo-skyrim`) devuelve `ok` con EXIT 0 [MEDIDO]:
- 44 records;
- formVersion 44 en todos;
- WEAP con DATA de 10 y DNAM de 100;
- WNAM → STAT;
- 30 referencias colocadas correctas.

| Record | Hoy [MEDIDO] | Cambio propuesto (backlog v08) | Dónde |
|---|---|---|---|
| PROJ `AstraAsedioProjectile` 03000802 | clon de `DLC1BoltSteelProjectile`: Arrow, 5400 / 0,35, radio 0,5, fuerza 1, flags CanBePickedUp + Supersonic | sin CanBePickedUp; Explosion → EXPL nueva; radio y fuerza de §2; FULL en castellano | `scripts/build_plugin.py:390` |
| AMMO `AstraAsedioNativeBolt` 03000803 | clon de `DLC1BoltSteel`: daño 10, flags 0 (jugable), FULL "Astra Siege Bolt" | Non-Playable (0x2) | `:392–393` |
| WEAP `AstraAsedioNativeLauncher` 03000804 | clon de `DLC1TrapCrossbowWeapon01`: daño 10, stagger 0, sin SNAM/XNAM, NNAM `ProjectileNode` | daño 35, stagger 1,0, SNAM `WPNCrossbowFire` + XNAM `WPNCrossbowFire2D` | `:394` |
| EXPL nueva | — | clon de `TrapBallistaBoltExplosion02`: daño 150, radio 128, fuerza 20; revisar su efecto visual (si no encaja, partir de `CWCatapultExp` con el daño ajustado) | nuevo |
| ACTI, CONT, QUST, CELL, NAVM, LIGH, STAT | correctos para el alcance actual | sin cambios | — |

**Por qué es P1 lo del proyectil y la munición.**
- Cada virote clavado se recoge como "Astra Siege Bolt", una munición jugable que sirve en cualquier ballesta de mano.
- `iArrowInventoryChance` vale 33 en `Skyrim.esm` [MEDIDO]. Según la documentación de la comunidad, un tercio de los impactos en actores pasa al inventario de la víctima [A VERIFICAR EN JUEGO].
- Recoger virotes no repone la torre, porque la torre consume `DLC1BoltSteel`.
- El precedente vanilla es la balista del centurión: munición no jugable y proyectil no recogible.

**`1stPerson*.nif`: N/A.**
- El arma nunca se equipa; la "primera persona" es la cámara nativa sobre `AstraSightCameraNode`.
- `WNAM → STAT ballesta.nif` solo cumple la estructura: las 463 armas base vanilla con WNAM apuntan a un STAT.
- Las animaciones del arma son las secuencias Gamebryo del NIF. El operador no tiene animación propia (ver §1).

### NIF: limpieza en NifSkope y en `build_assets.py`

- **P2 [MEDIDO]. Alpha-test inútil en los pisos.**
  - Los pisos de la torre (8.408 tris) y de la ballesta (176 tris) llevan `NiAlphaProperty` 4844 con umbral 200, aunque `build_assets.py:88–91` pretende quitarlo (borra las propiedades del material, pero el nodo de alfa sigue en el árbol del shader).
  - `WoodWalkway01.dds` es DXT1 sin un solo texel transparente (0 de 262.144 bloques): no hay efecto visual, solo el costo del alpha-test.
  - Arreglo: quitar el nodo de alfa del material `floor` y que `verify_assets.py` **exija su ausencia**.
- **P2 [MEDIDO]. Colores de vértice en blanco.** Todas las shapes fusionadas llevan colores de vértice en blanco (`build_assets.py:173–174`, flag `Vertex_Colors`, +4 B por vértice). Opciones:
  - hornear oclusión ambiental en ellos, que ayuda mucho con texturas vanilla;
  - o no exportarlos (`export_colors=False`).
- **Shaders [MEDIDO].**
  - Metal: EnvMap (tipo 1, `ShinyDull_e`, escala 1,0) sin máscara `_m`. Está bien, porque sus UV caen en la zona de hierro del atlas de la catapulta.
  - Madera, cuerda y tablones: receta Default de `lumbermill01`.
  - Virote: receta Default de `plaincrossbowtrap01`.
  - Mejora estética: la punta metálica del virote como shape aparte, con la receta EnvMap del `BoltProjectile` vanilla (máscara `Bolt_m` y escala 1,73).
- **BSXFlags [MEDIDO].**
  - La catapulta vanilla (6.072 tris, 22 shapes) usa 27: Animated, Havok, Complex, Addon, sin Articulated.
  - La trampa de ballesta usa 171, con Articulated.
  - El 139 de la ballesta no contradice ningún precedente: es una observación, no un defecto.
- **Secuencias.** Fire y Reset son CLAMP, sin text keys, y se disparan con `PlayGamebryoAnimation`: es correcto para un ACTI. La trampa vanilla usa behavior graph (`BSBehaviorGraphExtraData`), que aquí no hace falta.
- **Nodos y flags.** `SELECTIVE_UPDATE*`, más `NO_ANIM_SYNC_S` en todos (`build_assets.py:11`), y raíz `BSFadeNode`. Sin observaciones.

### El chequeo verde que no puede fallar por la causa real

- `reports/assets_verified.json` marca `projectile_physics_verified` con capa, material, cuerpo y masa del virote. Pero ese chequeo **no puede fallar** por lo que está mal: el tamaño de la caja y el marco de la inercia.
- Propuesta para `verify_assets.py`:
  - "la caja cubre ≥ 90 % del largo visual" (hoy daría 20,1 % y fallaría);
  - "la inercia mínima está sobre el eje largo de la caja";
  - falsificar los dos chequeos con el NIF actual antes de darlos por buenos.
- Igual que con el alfa de los pisos: exigir **ausencias**, no solo presencias.

### Creation Kit y xEdit

- **Pendientes que ya lista el README.**
  - Check for Errors en SSEEdit.
  - Finalizar el navmesh de la celda de prueba en el CK. El NAVM generado por script lleva `ck_navmesh_surface_adjustment_pending`.
- **Para llevarla a Tamriel:**
  - una celda exterior con un ancla de lore (§4);
  - recortar el navmesh en un plugin aparte;
  - LOD de la torre;
  - la referencia del ACTI como persistente si el script la necesita desde lejos;
  - y probar a los dragones en ese exterior, porque en una celda interior no vuelan.
- **ESL.** El rango de FormIDs 0x800–0x933 (< 0xFFF) lo permite. Decidirlo después de la prueba en juego, con `scripts/esl.py` de la skill (comprueba el techo y deja `.bak`). Ojo: al pasar a ESL cambian los FormIDs de las partidas guardadas.
- **Nativo.** `AstraSight.dll` solo carga en 1.6.1170 (`native/src/Plugin.cpp:224–227`); SE 1.5.97 y VR quedan fuera. Es una elección consciente, pero hay que decirlo en la página del mod.

### Casos de prueba en juego que faltan

Se proponen; no se agregaron a `PRUEBAS_EN_JUEGO.md`.

1. **Caída.** Impacto contra los blancos de 10 y 30 m, comparado con la tabla de §2.
2. **Daño.** `getav health` de un dragón antes y después de N impactos, para medir `k_motor`. Hacerlo en un exterior.
3. **Recogida.** Recoger un virote clavado y revisar el inventario del blanco abatido.
4. **Sonido.** Comprobar si el disparo suena.
5. **Fus Ro Dah.** El grito Fuerza Implacable del dragón durante la sesión. `EncDragon05Fire` y `DLC1EncDragon07Fire` lo tienen en sus SPLO [MEDIDO]. El ragdoll del operador tiene que cerrar la sesión y devolver los controles.
6. **Acumulación.** 50 o más disparos en modo continuo: mirar FPS y la acumulación de virotes clavados.

---

## 4. Checklist de optimización y coherencia de lore

### Optimización

- [ ] **P2. Ballesta de 19.754 a ≤ 9.000 triángulos.**
  - Las amarras de cuerda son 9.334 triángulos, el **47 %** (3.408 + 3.396 + 2.530). Pasarlas a ≤ 1.500 con bandas low-poly y normal map.
  - El metal son 7.436 triángulos; bajarlo a ≤ 4.000.
  - Referencia: la catapulta CW completa tiene 6.072 triángulos.
- [ ] **P2. Torre de 18.020 a ≤ 10.000 triángulos.** Los pisos son 8.408 y pueden bajar a ≤ 2.500, porque la textura ya dibuja los tablones.
- [ ] **P1 si se coloca en un exterior. LOD de la torre** (xLODGen o DynDOLOD).
  - Orientativo: ≈2.000 / 600 / 200 triángulos.
  - Flag "Has Distant LOD" en el STAT.
  - Silueta estática de la cabeza dentro del LOD de la torre, porque el ACTI no tiene LOD.
- [ ] **P2.** Quitar el alpha-test de los pisos y decidir qué hacer con los colores de vértice (§3).
- [ ] **P2.** Inercia en cero en los cuerpos FIXED (§2).
- [x] **Texturas.** No agrega DDS propios: comparte texturas vanilla, sin VRAM extra propia. Si se hacen texturas propias:
  - dimensionarlas por contenido, no todas a 2048;
  - BC7 para difuso y normal (especular en el alfa del normal);
  - `_m` de 512–1024;
  - un trim sheet para el metal en vez del recorte del atlas de la catapulta;
  - PBR solo con Community Shaders (True PBR): SE vanilla no tiene PBR.
- [x] **Draw calls.** 17 + 4 + 1 shapes, dentro de lo vanilla (la catapulta tiene 22). Cada corte por nodo animado y material está justificado.

### Coherencia con el lore

- [x] **Materiales.** Madera nórdica de aserradero, cuerda de cáñamo y herrajes de la catapulta imperial: encaja con la ingeniería de asedio nórdico-imperial. El precedente es la catapulta de la Guerra Civil. La mira es una cámara invisible: no hay óptica anacrónica.
- [ ] **Sabor cazadragones, sin salir del canon:**
  - puntas de **acero de Forja del Cielo** (Eorlund Gray-Mane y los Compañeros);
  - **torno y trinquete con engranaje dwemer**, del tipo que estudia la Guardia del Alba con Sorine Jurard, que además justifica recargar en 1,2 s;
  - un **tier alto** de hueso de dragón o de ébano (escaso, de final de juego);
  - el **oricalco** es orco: solo encaja en una variante forjada por orcos.
- [ ] **Escala del virote.** De 4,07 m a 2,5–3,0 m. El vanilla de la balista dwemer mide 2,54 m, y así la energía también cierra (§1).
- [ ] **Nombres.**
  - Los FULL mezclan castellano (ACTI "Ballesta de asedio Astra", CONT, CELL) e inglés (PROJ "Astra Siege Projectile", AMMO "Astra Siege Bolt", WEAP "Astra Siege Launcher"). Unificar.
  - "Astra" es latino y no suena nórdico. Para el nombre visible conviene uno nórdico.
- [ ] **Anacronismos a evitar** en futuras iteraciones del modelo: ópticas o miras de anillo, perfiles de acero soldados, tuercas hexagonales, rodamientos, resortes helicoidales y cables metálicos. Torno, trinquete, garra y nuez son medievales ✓.
- [ ] **Emplazamiento con ancla de lore.**
  - La **Atalaya Occidental** de Carrera Blanca, donde ataca el primer dragón.
  - El **Fuerte Guardia del Alba**.
  - El **Templo de Sky Haven**.
  - Dragonsreach ya tiene en el canon una trampa para dragones.

---

## Backlog v08 priorizado

Nada de esto se aplicó: es para aprobar aparte.

| ID | P | Cambio | Dónde | Cómo se verifica |
|---|---|---|---|---|
| B1 | P0 | Daño: WEAP 35, EXPL nueva (150, radio 128, fuerza 20), flag Explosion en el PROJ | `build_plugin.py:390,394` + EXPL | `verificar_plugin.py`; `getav health` en un dragón |
| B2 | P1 | PROJ sin CanBePickedUp; AMMO Non-Playable; FULL en castellano | `build_plugin.py:390–394` | no se puede recoger el virote clavado |
| B3 | P1 | Caja Havok del virote: astil completo, inercia en el marco de la caja, masa 15–20, restitución 0,1 | `build_assets.py:437–447` | `medir_nif.py`: cobertura ≥ 90 %; `colision_caja.py`; soltar un virote en juego |
| B4 | P1 | Cero de mira: `AstraSightCameraNode` −1,38° (75 m) | `build_assets.py:376–379` + tests de cámara | blancos de 10 y 30 m |
| B5 | P1 | Barrido del operador: voladizo trasero en r ≤ 95 por debajo de z 125 | script nuevo, patrón de `mechanism_source_fixes.py` | `medir_barrido_operador.py`: 0 vértices en la cápsula |
| B6 | P1 | Sonido de disparo: SNAM y XNAM (o SNDR propio) | `build_plugin.py:394` | en juego |
| B7 | P1 | Chequeos nuevos: cobertura de la caja, eje de inercia, ausencia de alfa en pisos, cada uno falsificado | `verify_assets.py` | fallan con los NIF actuales |
| B8 | P2 | Límite de velocidad angular configurable | `native/src/Core.cpp:35` | tests nativos y juego |
| B9 | P2 | Torno, trinquete y garra animados en Reset | `build_assets.py` (`sequences`) | reimportar y renderizar |
| B10 | P2 | Quitar alfa de los pisos; inercia 0 en cuerpos FIXED; decidir colores de vértice | `build_assets.py:88–91, 173–174, 199` | `medir_nif.py` |
| B11 | P2 | Bajar polígonos (cuerdas, metal, pisos) | `.blend` + presupuesto en `verify_assets.py` | `verify_assets.py` |
| B12 | P1, solo en exterior | LOD de la torre + Has Distant LOD | nuevo | xLODGen / DynDOLOD |

---

## Anexo A: variante de mano (solo si se pide)

Si además se quiere una ballesta pesada **de mano** para cazar dragones, el camino lo marca `references/plugin-weap.md` de la skill:
- clonar `DLC1CrossBow` (tipo de animación 9, daño 19) y cambiar solo los campos declarados;
- `Prn = WeaponBow` en el NIF;
- STAT propio de primera persona apuntado por `WNAM`;
- OBND medido del NIF;
- formVersion 44;
- validar con `verificar_plugin.py` sobre la carpeta del mod, para que compruebe el `Prn`.

Ahí sí aplican empuñadura, encare (cámara de hombro), retroceso (animación y cámara) y el `1stPerson*.nif`.

## Anexo B: evidencia

Todo se corrió con `python -B` (sin escribir caché). La salida completa está en `docs/revision/medicion/salidas/`.

| Comando | EXIT | Qué demuestra |
|---|---|---|
| `python -B docs/revision/medicion/medir_nif.py` | 0 | ficha de los 3 NIF; vanilla de referencia; cobertura de la caja 20,1 % (vanilla 83,9–96,9 %); pisos con alfa 4844/200; DXT1 sin transparencia |
| `python -B docs/revision/medicion/medir_esm.py` | 0 | tablas de PROJ, AMMO, WEAP y GMST; salud de dragones (`DragonRace` 500 + offsets) |
| `python -B docs/revision/medicion/medir_asedio_y_dragones.py` | 0 | EXPL de la balista dwemer (80–250) y de la catapulta (30); defensas del dragón; sonidos; IDLE `Ballista*` del centurión |
| `python -B docs/revision/medicion/medir_barrido_operador.py` | 0 | vértices dentro de la cápsula del operador según la elevación |
| `python -B <skill>/scripts/verificar_plugin.py mod/AstraAsedio.esp` | 0 | `ok`: 44 records, formVersion 44, WEAP 10/100, WNAM → STAT, referencias |
| `python -B <skill>/scripts/colision_caja.py mod/meshes/AstraAsedio/{torre,ballesta,virote}.nif` | 0 | 0 fallas; observación de inercia/fórmula [4,77, 0,16, 1.471,55] en el virote |

Los scripts de medición toman las rutas de `config.json` (`runtime` y `extracted`) y solo leen. Sus layouts binarios están documentados en la cabecera de cada uno:
- offsets de `bhkRigidBody` tomados de `colision_caja.py` de la skill;
- DATA de PROJ de 92 bytes;
- ACBS de NPC de 24 bytes;
- salud inicial de RACE en DATA+36, con `NordRace` = 50 como control.
