# Alcance de licencias

- `native/` (AstraSight, plugin SKSE del build AE 1.7.104): **GPL-3.0-or-later**, texto en `LICENSE`.
  Se incluye la excepción *Modding Exception* y *GPL-3.0 Linking Exception* de CommonLibSSE-NG
  (ver `Licenses/CommonLibSSE-NG-alandtse-EXCEPTIONS.md`).
- `third_party/CommonLibSSE-NG/` (alandtse, commit `67b201b6fe45241ac5c1e4630ecf847523775b66`, v12.2.0): GPL-3.0-or-later con excepciones. Su código se redistribuye tal cual.
- Resto de las librerías vinculadas (fmt, spdlog, rapidcsv, DirectXTK, DirectXMath, nlohmann-json, SimpleIni, toml11, xbyak): cada una con su licencia en `Licenses/`.
- Scripts Papyrus (`papyrus/`), scripts Python (`scripts/`) y el README: la NOTICE del build 1.7.104 los considera obras separadas no cubiertas por la GPL. Su licencia no está definida en este repositorio.

No se incluye contenido de Bethesda (.esm, .esp, .bsa, .ba2, .dds, .hkx, .nif, .dll precompilada).
