# Dragonsreach Ballistae 1.0.0

Heavy siege ballistae for Whiterun Hold, built to fight dragons.

Dragonsreach was raised to hold the dragon Numinex. This mod gives Whiterun Hold the weapons to match: a ballista you can
man yourself at the Western Watchtower, guard-crewed ballistae on the Whiterun walls and over the main gate, and bandit
ballistae defending three camps of the hold.

> **Game version — pick the main file that matches your game:**
> * `DragonsreachBallistae-1.0.0-SE1.6.1170.zip` — Skyrim SE/AE **1.6.1170** with SKSE **2.2.6** or **2.2.8**. This is the build the
>   author plays and **the only one tested in game**.
> * `DragonsreachBallistae-1.0.0-AE1.7.104-experimental.zip` — current Steam build **1.7.104** with SKSE **2.3.1**.
>   **Experimental: compiled and checked, but never tested in game.** Please report whether it works.
>
> * `DragonsreachBallistae-1.0.0-SE1.5.97-experimental.zip` — Skyrim SE **1.5.97** with SKSE **2.0.20**.
>   **Experimental: compiled and checked, but never tested in game.**
>
> The three files are identical except the SKSE plugin `AstraSight.dll`. Each DLL refuses to load on the other runtime.

## Features

* **Player ballista at the Western Watchtower.** Activate it to mount. A native first-person sight (SKSE) aims with the
  mouse; arrow keys fine-tune the aim. Attack fires; Sprint toggles single shot / held repeat; Activate dismounts.
  Each shot costs one steel bolt.
* **Dragon fights while mounted (The First Dragon / Mirmulnir and any dragon).** The dragon keeps fighting you instead
  of flying off, lands on open ground in front of the ballista, and its health bar is shown on the vanilla enemy meter
  while you are mounted. On dismount every change to the dragon is given back (its quest landing marker and flight).
* **Whiterun wall towers.** Two ballistae on cantilevered platforms outside the walls, crewed by a guard who rides in
  a hanging basket. They shoot hostile creatures and actors fighting the guards. They follow the player with their
  sights but fire at the player only while the town guards are fighting the player. You can take a tower ballista
  over: the crew stands aside while you use it.
* **Whiterun gate post.** A third guard ballista above the main gate, same rules as the towers.
* **Bandit camp ballistae.** White River Watch, Halted Stream Camp and Silent Moons Camp each have a ballista that
  shoots the player on sight while bandits of that camp are alive nearby. A cleared camp's ballista goes quiet.
* **Light footprint.** All five plugins are ESL-flagged (`.esp` with the light flag): they use no full load-order slot.

## Requirements

* Skyrim Special Edition / Anniversary Edition, Steam, **runtime 1.5.97**, **1.6.1170** or **1.7.104** (matching main file). Other
  runtimes, GOG, VR and Game Pass are not supported. Dawnguard is a master (included in SE/AE).
* [SKSE64](https://skse.silverlock.org/) **2.0.20** for 1.5.97, **2.2.6** or **2.2.8** for 1.6.1170, or **2.3.1** for 1.7.104 — launch the game through SKSE.
* [Address Library for SKSE Plugins](https://www.nexusmods.com/skyrimspecialedition/mods/32444) version matching your
  runtime (the 1.7.104 build needs the Address Library release for 1.7.104).
* [Open Animation Replacer](https://www.nexusmods.com/skyrimspecialedition/mods/92109) (the tested configuration).
* [Microsoft Visual C++ 2015-2022 x64 Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)
  (current version).

SkyUI, PapyrusUtil and other frameworks are not required. Keyboard and mouse are required (no gamepad sight support).

## Installation

Install with Mod Organizer 2 or Vortex; the archive has a Data-root layout. Enable all five plugins (LOOT sorts them):

```
DragonsreachBallistae.esp
DragonsreachBallistae_Watchtower.esp
DragonsreachBallistae_WhiterunTowers.esp
DragonsreachBallistae_GuardAnims.esp
DragonsreachBallistae_Outposts.esp
```

## Updating and uninstalling — read this

* **Start a new game** when installing, and when coming from *Astra Asedio* (the previous name of this mod): the
  plugins were renamed and ESL-flagged, so references in older saves do not carry over. Updating in the middle of a
  playthrough can leave platforms missing or ballistae misbehaving.
* **Do not uninstall mid-playthrough.** Scripts, persistent references and placed objects stay in the save. To remove
  the mod, load a save made before it was installed.
* Dismount the ballista before saving if you can (a save made while mounted is cleaned up on load).

## Compatibility

* **Camera mods** (Improved Camera, SmoothCam, True Directional Movement...) may conflict with the first-person sight.
* **HUD replacers**: the dragon health bar drives the vanilla enemy meter; with a replaced HUD it is simply not shown.
* **Places edited**: the Whiterun walls and the area in front of the main gate, the terrain around the Western
  Watchtower, White River Watch, Halted Stream Camp and Silent Moons Camp. City, landscape or camp overhauls touching
  the same spots may clip with the platforms. No navmesh is edited.
* **Worldspace records**: the plugins carry copies of the Tamriel worldspace and persistent-cell headers (as Update.esm
  has them). Let LOOT sort; mods that change worldspace-wide settings should load after this mod.
* **Difficulty**: bandit ballistae hit hard and fire every few seconds. At low level and high difficulty they can be
  deadly — approach the camps with care.

## Troubleshooting

The SKSE plugin writes `Documents\My Games\Skyrim Special Edition\SKSE\AstraSight.log`. The first lines name the
installed build. When reporting a problem, give your game, SKSE and mod versions, the ballista and the steps, and attach
the relevant log lines (remove personal paths).

The scripts and the SKSE plugin keep their internal *Astra* names (`AstraAsedio*.pex`, `AstraSight.dll`); this is
expected and does not mean an old version is installed.

## Credits and licenses

* Author: FacundoSu1986. Code, guard animations and documentation were generated with AI tools under the author's
  direction; no third-party assets were downloaded.
* Bethesda Game Studios — Skyrim and the vanilla meshes, textures, animations and records the mod builds on. Only
  vanilla textures are referenced; none are redistributed.
* CommonLibSSE-NG, spdlog, fmt and rapidcsv — their upstream authors; license texts are in `Licenses/`. The SKSE plugin
  is built against CommonLibSSE-NG from https://github.com/CharmedBaryon/CommonLibSSE-NG at commit
  `b93280e832f263dbef44e44cbe2936622a02f91a`, distributed under the MIT license (the text shipped in `Licenses/`).
* **1.7.104 build only:** the DLL is built against the maintained fork https://github.com/alandtse/CommonLibSSE-NG at
  commit `67b201b6fe45241ac5c1e4630ecf847523775b66`, licensed GPL-3.0-or-later with modding/linking exceptions. That
  DLL and its C++ source are distributed under GPL-3.0-or-later; see `Licenses/AE1.7.104/NOTICE-1.7.104.md`. The
  complete Corresponding Source is the file `DragonsreachBallistae-1.0.0-source-AE1.7.104-GPL.zip` on the mod page.
* Open Animation Replacer by Ersh (API used for the guard animation set).

Papyrus sources are included under `Source/Scripts`.
