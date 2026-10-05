"""Build a reversible lighting-only override for the existing Astra test cell."""
from pathlib import Path
import hashlib, json, struct, sys, zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/vendor'))
from parser_esm import Plugin
import escritor_plugin as W

CELL = 0x03000807
MASTERS = ['Skyrim.esm', 'Update.esm', 'Dawnguard.esm', 'AstraAsedio.esp']
PATCH = 'AstraAsedio_Despejado.esp'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def records(path):
    p = Plugin(path)
    return p, {p.form_id(off): (typ, off, dict(p.subrecords(p.datos(off))))
               for typ, off, n, d in p.recorrer() if typ != 'GRUP'}


def main():
    base = ROOT / 'mod/AstraAsedio.esp'
    before = sha(base)
    source, r = records(base)
    typ, off, original = r[CELL]
    assert typ == 'CELL' and original['EDID'] == b'AstraAsedioTest\0'
    assert len(original['XCLL']) == 92 and original['LTMP'] == bytes(4)

    # Confirm the neutral vanilla ImageSpace from the installed master itself.
    cfg = json.loads((ROOT / 'config.json').read_text())
    master = Plugin(Path(cfg['runtime']) / 'Data/Skyrim.esm')
    image = None
    for t, o, n, d in master.recorrer():
        if t == 'IMGS' and master.form_id(o) == 0x167:
            image = dict(master.subrecords(master.datos(o)))
            break
    assert image is not None and image['EDID'] == b'DefaultImageSpace\0'
    assert struct.unpack('<4f', image['TNAM']) == (0., 1., 1., 1.)

    lighting = bytearray(original['XCLL'])
    # XCLL layout: official xEdit wbDefinitionsTES5.pas, 92-byte SSE variant.
    # Neutral fill keeps the whole asset legible in this isolated interior.
    lighting[0:4] = bytes((72, 72, 72, 0))  # Ambient Color
    lighting[4:8] = bytes((0, 0, 0, 0))    # no directional source in this test cell
    lighting[8:12] = bytes((64, 64, 64, 0))
    for i in range(6):
        lighting[40 + i*4:44 + i*4] = bytes((72, 72, 72, 0))
    lighting[64:68] = bytes((72, 72, 72, 0))  # ambient specular color
    lighting[72:76] = bytes((64, 64, 64, 0))  # Fog Color Far
    struct.pack_into('<2f', lighting, 12, 100000., 200000.)
    struct.pack_into('<f', lighting, 36, 1.)  # Fog Power
    struct.pack_into('<f', lighting, 76, 0.)  # Fog Max
    struct.pack_into('<I', lighting, 88, 0)   # use this cell's local lighting
    changed = {'XCLL': bytes(lighting), 'XCIM': struct.pack('<I', 0x167)}
    subs = [W.sub(k, changed.get(k, v)) for k, v in source.subrecords(source.datos(off))]
    rec = W.record('CELL', CELL, subs, banderas=struct.unpack_from('<I', source.d, off+8)[0])
    local = CELL & 0xffffff
    subblock = W.grupo(struct.pack('<i', (local//10) % 10), [rec], 3)
    block = W.grupo(struct.pack('<i', local % 10), [subblock], 2)
    folder = ROOT / 'patches/AstraAsedio_Despejado'
    folder.mkdir(parents=True, exist_ok=True)
    esp = folder / PATCH
    W.escribir(esp, MASTERS, [W.grupo('CELL', [block])], [], autor='Astra', esl=False,
               descripcion='Neutral lighting and no visible distance fog in AstraAsedioTest.')

    # Read actual output and ensure the patch changes only two cell subrecords.
    final, rr = records(esp)
    assert set(rr) == {0, CELL}
    typ, o, out = rr[CELL]
    assert out == {k: changed.get(k, v) for k, v in original.items()}
    assert [v.rstrip(b'\0').decode() for k, v in final.subrecords(final.datos(0)) if k == 'MAST'] == MASTERS
    assert all(struct.unpack_from('<H', final.d, o+20)[0] == 44 for t, o, ss in rr.values())
    assert struct.unpack_from('<I', final.d, 8)[0] == 0
    assert struct.unpack_from('<f', out['XCLL'], 76)[0] == 0.
    assert struct.unpack_from('<2f', out['XCLL'], 12) == (100000., 200000.)
    assert sha(base) == before

    instructions = '''# AstraAsedio — celda despejada

Parche opcional para la celda interior AstraAsedioTest. Suprime la niebla de distancia dentro del recinto, cambia el tono ambiental a gris neutro y sustituye el ImageSpace de cueva heredado por DefaultImageSpace vanilla sin tinte.

Cerrar Skyrim. Instalar este ZIP como un mod separado en MO2. Activar AstraAsedio_Despejado.esp y colocarlo después de AstraAsedio.esp en el orden de carga. Iniciar con SKSE y entrar con `coc AstraAsedioTest`.

Contiene una sola anulación CELL. Conserva la geometría, navmesh, referencias, munición y scripts del mod base. Para revertir, desactivar este parche con el juego cerrado. No se modifican climas de Tamriel.

Verificado sobre el binario: cuatro masters, versión de registro 44, sólo XCLL y XCIM modificados; ImageSpace vanilla 00000167 comprobado sin tinte. No se realizó prueba visual dentro del juego en esta sesión.

Formato de iluminación: https://github.com/TES5Edit/TES5Edit/blob/dev-4.1.6/Core/wbDefinitionsTES5.pas
'''
    (folder / 'README.md').write_text(instructions, encoding='utf-8')
    archive = ROOT / 'dist/AstraAsedio_Despejado_MO2.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, strict_timestamps=False) as z:
        z.write(esp, PATCH)
        z.write(folder / 'README.md', 'Docs/AstraAsedio_Despejado/README.md')
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and z.read(PATCH) == esp.read_bytes()
    report = {'patch': str(esp), 'zip': str(archive), 'sha256': sha(esp),
              'zip_sha256': sha(archive), 'masters': MASTERS,
              'changed_record': 'CELL AstraAsedioTest', 'changed_subrecords': ['XCLL', 'XCIM'],
              'fog_max': 0., 'fog_near': 100000., 'fog_far': 200000.,
              'neutral_vanilla_imagespace': '00000167 DefaultImageSpace',
              'file_checks_pass': True, 'base_plugin_unchanged': sha(base) == before,
              'installed_in_mo2': False, 'in_game_verified': False}
    (ROOT / 'reports/clear_test_patch.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
