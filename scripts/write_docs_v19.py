"""Current QA instructions and public release-candidate documentation."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

NATIVE='''# AstraSight 3.5.4 — API 4

Target: Steam Skyrim SE 1.6.1170.0, SKSE 2.2.8 and matching Address Library. Runtime checks reject other game versions. SKSE 2.2.6 exposes the interfaces used here, but is untested with this DLL and below the supported minimum. Use the appropriate older Steam build from the official SKSE Nexus files page.

Native code owns player sight, the Fire/Release/Reset cycle and projectile launch. Reference handles and loaded scene identity are validated each update; effects serialize against teardown. Projectile speed is normalized to ShotAmmo's projectile record. A successful projectile handle is required before ammunition cost is committed. No FOV setting changes.

3.5.4 adds ResetIdleScene, a main-thread-only Papyrus binding. It rejects ownership, pending cleanup, missing nodes and scene replacement, and settles the existing Reset sequence at its final phase without replaying the legacy whole-reference animation. Guard handoff waits for restoration and any pending guard Launcher.Fire. API remains 4; check DLL version 3.5.4 before calling this additive binding.

Guard firing uses a separate Papyrus Weapon.Fire path. Player flight measurements do not establish NPC ballistics. Player sight and flight were confirmed with 3.5.3; the 3.5.4 handoff change requires game testing. Portable tests establish math and ordering, not Skyrim rendering or VM scheduling.

## Source build

The source archive includes native C++ and six PSC files. It excludes Bethesda files, SDKs, dependency source trees and the historical ESP/NIF/Blender pipeline. Use an x64 MSVC developer shell, CMake 3.26+, Ninja and C++23. Release toolchain: MSVC 14.51.36231, Windows SDK 10.0.26100.0. Other toolchains are uncertified.

Clone these into a local vendor directory at exactly these commits:

| Directory | Upstream | Commit |
| --- | --- | --- |
| CommonLibSSE-NG | https://github.com/CharmedBaryon/CommonLibSSE-NG | b93280e832f263dbef44e44cbe2936622a02f91a |
| spdlog | https://github.com/gabime/spdlog | 486b55554f11c9cccc913e11a87085b2a91f706f |
| rapidcsv | https://github.com/d99kris/rapidcsv | 03133b59e17ca92ecf886b611d87a03ad2bb2a8f |

From the source archive root:

```powershell
cmake -S native -B out -G Ninja -DCMAKE_BUILD_TYPE=Release -DASTRA_VENDOR="$PWD/vendor"
cmake --build out --parallel 4
ctest --test-dir out --output-on-failure
```

CMake detects the compiler language by default. Only if its include-prefix detection fails, set ASTRA_SHOWINCLUDES_PREFIX to the exact compiler diagnostic prefix. Install out/AstraSight.dll into Data/SKSE/Plugins. For pure tests without Skyrim headers use -DASTRA_BUILD_PLUGIN=OFF. Nine targets cover 2,376 assertions.

Compile PSC files with the Skyrim Creation Kit Papyrus compiler and matching SKSE source imports. Binary PEX was disassembled after anonymizing compiler user/host fields; executable tables remain byte-identical. Changing PSC alone does not update installed PEX. The local build_native.py helper is machine-specific and excluded from the public source archive.

## Notices and limits

Third-party notices, including spdlog's embedded fmt, are in licenses. The DLL links Windows and Microsoft C++ runtime libraries and retains a few compiler diagnostic paths into the SDK checkout. Public packages exclude logs, profiles and machine configuration. The source archive grants no additional game-asset or original-asset rights; publisher permissions apply.

Tests do not establish engine hooks, NPC ballistics, damage, navigation or camera-mod compatibility. Camera transactions retain the existing Session mutex discipline; concurrent engine reentrancy remains a game verification topic.

API evidence: [FirstPersonState](https://github.com/CharmedBaryon/CommonLibSSE-NG/blob/b93280e832f263dbef44e44cbe2936622a02f91a/include/RE/F/FirstPersonState.h), [native marshalling](https://github.com/CharmedBaryon/CommonLibSSE-NG/blob/b93280e832f263dbef44e44cbe2936622a02f91a/include/RE/N/NativeFunction.h), [handle resolution](https://github.com/CharmedBaryon/CommonLibSSE-NG/blob/b93280e832f263dbef44e44cbe2936622a02f91a/include/RE/B/BSPointerHandle.h).
'''

PUBLIC='''# Astra Asedio — 0.19.0-rc.1

Release candidate for Steam Skyrim Special Edition 1.6.1170. In-game interface: Spanish. This version needs final game validation before a stable public release.

The optional Whiterun Towers file places two siege crossbows on extensions outside the city. Guards operate them and the player can request the sight with Activate. The core is a required resource/controller dependency; alone it does not place playable crossbows in the exterior world.

## Requirements

* Steam SkyrimSE.exe 1.6.1170.0 and Dawnguard, HearthFires, Dragonborn.
* [SKSE](https://www.nexusmods.com/skyrimspecialedition/mods/30379?tab=files) 2.2.8 for 1.6.1170. Select the matching older Steam file (20 August 2026), and verify that skse64.log reports 2.2.8. The currently newest SKSE targets another runtime. The older 2.2.6 exposes the used interfaces but is outside this release's supported minimum.
* [Address Library for SKSE Plugins](https://www.nexusmods.com/skyrimspecialedition/mods/32444): Anniversary Edition package containing versionlib-1-6-1170-0.bin.
* [Microsoft Visual C++ v14 x64 Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170), version at least as recent as the MSVC 14.51 toolchain used here. Older redistributables have not been verified with this build.

Only this runtime is supported. Other Steam runtimes, GOG, VR and Game Pass are untested or rejected. SkyUI and PapyrusUtil are not required by this mod. Launch through SKSE.

## Install and update

Install Core with MO2 or Vortex, then install Whiterun Towers if desired. Archives have a Data-root layout. Enable AstraAsedio.esp, followed by AstraAsedio_WhiterunTorres.esp. The addon requires Core. Check that AstraSight.dll and all six Astra scripts come from the same release; remove conflicting older copies from the manager's enabled mods or overwrite directory.

For v18 -> v19, exit the sight with Activate, save a test copy, close the game, replace both packages and launch through SKSE. Existing v17+ city FormIDs are retained. Earlier v16 and older placements were retired in v17; saved orphan references or old script state require testing and are not guaranteed migration support. Do not remove the mod from an ongoing save as a general repair technique. To uninstall, restore a save made before installation and disable both packages.

## Use

Keyboard and mouse are required; gamepad fast firing is unsupported. Approach the back of a station and press Activate (normally E). The guard yields the station; mouse movement aims, Attack fires, Activate exits and Sprint toggles single-shot/held-repeat firing. Player ammunition cost is one steel bolt per successful shot. The nominal player cycle is one second; guard cadence is 2.5 seconds. Holding Attack repeats only in continuous mode; cooldown and animation completion still apply.

The player projectile uses an explosive bolt. Records specify launcher damage 35 and explosion damage 150, radius 128 game units. Final applied damage depends on game behavior and defenses. Nearby allies may be affected; friendly-fire protection and NPC accuracy are not promised.

## Compatibility and known limits

City platforms preserve the sampled vanilla navigation clearance; no city NAVM or existing patrol packages are edited. This is geometric evidence, not finalized new navigation. Guards are assigned to specific vanilla operator/standby positions. City, tower, terrain and navmesh overhauls may need a placement patch; camera plugins may conflict with the first-person hook. Patches for other mods are not included. The city addon retains full vanilla Tamriel WRLD 0000003C settings and identical persistent CELL 00000D74 settings. It can overwrite other mods' climate, water, map or cell changes even without intersecting geometry. Supported xEdit parent cleanup remains a release gate; no broad compatibility is claimed. See RELEASE_STATUS.md.

The separate Atalaya terrain variant is excluded from these public files: its LAND changes need exterior navmesh work. Core retains a developer test interior with a custom NAVM pending Creation Kit finalization. That cell is not a supported gameplay destination and is not advertised as playable content.

v18 player aiming and projectile flight were confirmed in-game. v19 replaces the legacy Reset replay during guard handoff and waits for an in-flight guard shot; the exact reported visibility flicker and the new fix require a game test. NPC firing, damage, save migration, camera-mod interactions and long play sessions require further validation.

If reporting a bug, state game/SKSE/mod versions, station, steps and relevant AstraSight.log lines. Remove personal paths before sharing logs. No telemetry or network feature is included.

## Credits and permissions

Original Astra structure, crossbow modeling and implementation: project author/publisher. Bethesda: Skyrim assets and game record/material/physics donors used in the Skyrim-targeted files. Not all mesh or physics data is original. No standalone Bethesda asset library or executable is bundled.

CommonLibSSE-NG, spdlog, embedded fmt and rapidcsv: upstream authors; license notices are supplied in Licenses. No additional reuse permission for project or game assets is granted by these notes. Nexus publisher permission settings must reflect the author's actual rights. Development included AI-generated code and documentation; disclose this on the Nexus page.
'''

STATUS='''# Release status — 0.19.0-rc.1

Candidate, not a stable release. No Nexus upload has been performed.

Offline verification covers current C++ tests, interpreted PSC lifecycle regressions, fresh compiled/disassembled PEX, VMAD types and references, archive integrity and immutable-parent hashes. These checks do not execute Skyrim's VM, renderer or Creation Kit finalization.

Before publishing as stable:

1. Confirm that guard/player transfer has no whole-weapon disappearance on entry, exit, unload/reload and repeated takeover, including a guard shot pending at activation.
2. Check both Whiterun towers with a fresh test save and a copied v18 save: sight, bolt velocity, ammunition, damage, collision, guard return, menus, death and loading.
3. Verify NPC projectile behavior in combat separately from native player shots.
4. Complete Creation Kit finalization/checks for any playable custom navmesh. Atalaya stays excluded until its altered exterior LAND and NAVM agree.
5. Complete xEdit Check for Errors and supported parent cleanup, then reload and verify all placed-reference IDs and data. Two bounded isolated xEdit scripting attempts did not complete, so there is no xEdit pass. Current Tamriel WRLD 0000003C and persistent CELL 00000D74 headers retain vanilla settings and can affect other mods; placement patches still require testing.
6. Establish redistributable requirements on a clean machine, confirm the official SKSE 2.2.8 download and test representative camera/Whiterun overhauls before claiming compatibility.

This archive contains no test saves, Papyrus runtime logs, build artifacts other than the DLL/PEX, or machine-specific configuration. PEX compiler user/computer names are anonymized. A few SDK diagnostic paths remain inside the DLL; they are disclosed rather than described as absent.
'''

QA='''# Astra Asedio QA v19

DLL 3.5.4, API 4. Candidata para corregir el parpadeo al ceder una ballesta del guardia al jugador: usa el Reset nativo ya asentado y espera que termine cualquier disparo pendiente del guardia. El parpadeo aún debe comprobarse en Skyrim; no se afirma una causa visual definitiva.

La cámara y el vuelo del proyectil de v18 fueron confirmados por el usuario. v19 conserva el apuntado y la velocidad y no mueve las ballestas ni los voladizos. El núcleo y Whiterun Torres se deben actualizar juntos; cerrar Skyrim, salir de la mira y usar una copia del save de prueba. Verificar que ningún PEX/DLL anterior sobrescriba los nuevos.

Instalar AstraAsedio_QA_v19_MO2.zip y AstraAsedio_WhiterunTorres_QA_v19_MO2.zip. Cargar AstraAsedio.esp antes del addon. La variante AstraAsedio_Atalaya.esp sigue incluida sólo por continuidad del QA: su terreno requiere corregir NAVM; desactivarla para probar únicamente las torres de Whiterun. No se modificó la instalación ni los saves del usuario.

Repetir entrada/salida con E en las dos torres, con el guardia disparando y en reposo; comprobar desaparición completa, cámara, flecha, coste de virotes, salida con E, regreso del guardia, cargar/descargar celda y recargar save. Separar prueba del disparo del jugador de la del guardia.

La revisión adversarial y los candidatos públicos limpios están separados del paquete QA. Atalaya queda fuera de los candidatos públicos. Quedan pendientes pruebas de juego de v19 y finalización de navegación en CK antes de anunciar una versión estable.
'''

def main():
    (ROOT/'native/README.md').write_text(NATIVE,encoding='utf-8')
    public=ROOT/'docs/nexus';public.mkdir(parents=True,exist_ok=True)
    (public/'README.md').write_text(PUBLIC,encoding='utf-8')
    (public/'RELEASE_STATUS.md').write_text(STATUS,encoding='utf-8')
    (ROOT/'docs/README_v19.md').write_text(QA,encoding='utf-8')
    (ROOT/'README.md').write_text(QA,encoding='utf-8')
    (ROOT/'docs/NEXUS_PUBLICACION_v19.md').write_text('''# Borrador para publicar Astra Asedio

Título: Astra Asedio — Whiterun Siege Crossbows (1.6.1170)
Versión: 0.19.0-rc.1, release candidate. Interfaz en español.
Archivos: Core obligatorio; Whiterun Towers opcional que necesita Core; Source opcional para C++/PSC, no reproduce los ESP/NIF. Atalaya excluida por LAND/NAVM incompatibles.

Usar README.md y RELEASE_STATUS.md públicos como descripción, requisitos, instalación y límites. Adjuntar capturas reales del juego, registrar changelog y dependencias exactas. No subir logs internos, saves ni datos del equipo. Publicar sólo después de las pruebas pendientes si se pretende etiquetar estable.

Permisos: completar desde los derechos reales del autor; los créditos no sustituyen autorización. Respetar las licencias incluidas y el alcance Skyrim de los donantes Bethesda. No marcar todos los assets como originales ni autorizar usos fuera de ese alcance sin respaldo.

Transparencia: marcar AI-Generated Content por código generado y AI Media por documentación/descripción generada. El autor debe revisar el contenido final y elegir sus permisos. No se ha publicado ni enviado contenido a Nexus.

Fuentes de publicación: [buenas prácticas de Nexus](https://help.nexusmods.com/article/136-best-practices-for-mod-authors) y [reglas de archivos y contenido generado con IA](https://help.nexusmods.com/article/28-file-submission-guidelines).
''',encoding='utf-8')

if __name__=='__main__':main()
