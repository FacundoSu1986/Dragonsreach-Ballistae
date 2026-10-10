# Astra Asedio — 0.19.0-rc.1

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
