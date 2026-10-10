"""Measure the immutable v13 SSE NIF, then retime registered time floats only.

Reuses the validated v07 byte retimer. No export, spatial, shader, collision,
native DLL, pose or camera edit is involved.
"""
from pathlib import Path
import hashlib
import json
import math
import struct

from retime_v07 import retime, transform_times, nif_nodos

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.with_name("Ballesta_Astra_Vanilla_SE_v13")
MESH = "mod/meshes/AstraAsedio/ballesta.nif"


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1048576):
            digest.update(chunk)
    return digest.hexdigest()


def measure_sequences(path):
    binary = nif_nodos.leer(str(path))
    raw = binary["datos"]
    user = struct.unpack_from("<I", raw, raw.index(b"\n") + 6)[0]
    assert binary["version"] == "0x14020007" and user == 12 and binary["bs"] == 100, "Unsupported NIF header"
    sequences = {}
    registered = set()
    for kind, off, size in binary["bloques"]:
        if kind != "NiControllerSequence":
            continue
        name = binary["strings"][struct.unpack_from("<I", raw, off)[0]]
        assert name not in sequences, "Duplicate sequence"
        count = struct.unpack_from("<I", raw, off + 4)[0]
        start_offset = off + 12 + count * 29 + 16
        start, stop = struct.unpack_from("<ff", raw, start_offset)
        assert start == 0. and math.isfinite(stop) and stop > 0.
        registered.add(start_offset + 4)
        for i in range(count):
            interp = struct.unpack_from("<i", raw, off + 12 + i * 29)[0]
            it, io, isize = binary["bloques"][interp]
            assert it == "NiTransformInterpolator" and isize == 36
            data = struct.unpack_from("<i", raw, io + 32)[0]
            dt, do, ds = binary["bloques"][data]
            assert dt == "NiTransformData"
            times = transform_times(raw, do, ds)
            assert times
            for offset in times:
                value = struct.unpack_from("<f", raw, offset)[0]
                assert math.isfinite(value) and 0. <= value <= stop + .001
            registered.update(times)
        sequences[name] = stop
    assert set(sequences) == {"Fire", "Reset"}
    return {"version": binary["version"], "user": user, "bs": binary["bs"],
            "sequences": sequences, "registered_timing_offsets": sorted(registered)}


def retime_parent(path, durations):
    # Complete measurement and assertions precede the validated byte retimer.
    measurement = measure_sequences(path)
    assert abs(measurement["sequences"]["Fire"] - .3) < 1e-6
    assert abs(measurement["sequences"]["Reset"] - 1.2) < 1e-6
    assert set(durations) == {"Fire", "Reset"}
    assert all(math.isfinite(value) and value > 0. for value in durations.values())
    output, report = retime(path, durations)
    raw = path.read_bytes()
    masked = bytearray(output)
    for off in measurement["registered_timing_offsets"]:
        masked[off:off + 4] = raw[off:off + 4]
    assert masked == raw, "Unregistered bytes changed"
    assert report["timing_floats"] == len(measurement["registered_timing_offsets"])
    report["baseline_measurement"] = measurement
    report["changed_bytes"] = sum(a != b for a, b in zip(raw, output))
    report["same_file_length"] = len(raw) == len(output)
    return output, report


def main():
    cfg_path = ROOT / "config.json"
    cfg = json.loads(cfg_path.read_text())
    assert cfg["fire_seconds"] == .2 and cfg["reset_seconds"] == .8
    assert abs(cfg["release_seconds"] - 1 / 15) < 1e-8 and cfg["cycle_seconds"] == 1.
    baseline = json.loads((ROOT / "reports/v14_cadence_baseline.json").read_text())
    parent = BASE / MESH
    assert sha(parent) == baseline["v13_sha256"][MESH]
    output, report = retime_parent(parent, {"Fire": cfg["fire_seconds"], "Reset": cfg["reset_seconds"]})
    (ROOT / MESH).write_bytes(output)
    files = sorted(p for p in BASE.rglob("*") if p.is_file())
    after = {p.relative_to(BASE).as_posix(): sha(p) for p in files}
    assert after == baseline["v13_sha256"], "v13 baseline changed"
    report.update({
        "source": str(parent), "destination": str(ROOT / MESH),
        "config_before_sha256": baseline["v14_before_sha256"]["config.json"],
        "config_after_sha256": sha(cfg_path),
        "v13_immutable": True, "v13_files_checked": len(after),
        "v14_before_sha256": baseline["v14_before_sha256"],
        "v14_after_sha256": {p: sha(ROOT / p) for p in baseline["v14_before_sha256"]},
    })
    for preserved in ("mod/meshes/AstraAsedio/torre.nif", "mod/SKSE/Plugins/AstraSight.dll"):
        assert report["v14_before_sha256"][preserved] == report["v14_after_sha256"][preserved]
    (ROOT / "reports/v14_cadence_retime.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "baseline_measurement"}, indent=2))
    return report


if __name__ == "__main__":
    main()
