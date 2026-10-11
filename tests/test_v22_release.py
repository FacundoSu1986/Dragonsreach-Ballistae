"""Contrato de release v22: dos torretas, addon de animacion y puente de pose.

Ancla: el ZIP v21 publicado (`dist/AstraAsedio_QA_v21_Completo_MO2.zip`, sha
`0a60c61f...`, pinneado en `reports/base_archive.json`). No se compara contra un
directorio hermano porque el arbol vivo ya es v22.

Reemplaza a `test_v21_release.py::test_core_and_city_payload_preserved`, que
comparaba `mod/` contra el hermano v20 y deja de poder sostenerse en cuanto el
arbol avanza de version.
"""
import hashlib, json, sys, unittest, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'scripts/vendor')]

import verify_core_v22
import verify_torreta_baja_v22


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


# El ZIP v21 es un arbol MO2 plano; el repo separa core y addons. Esta tabla dice
# donde vive cada entrada del ZIP dentro del repo.
V21_MAP = {
    'AstraAsedio.esp': 'mod/AstraAsedio.esp',
    'AstraAsedio_WhiterunTorres.esp': 'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp',
    'AstraAsedio_Atalaya.esp': 'addons/Atalaya/AstraAsedio_Atalaya.esp',
    'SKSE/Plugins/AstraSight.dll': 'mod/SKSE/Plugins/AstraSight.dll',
    'seq/AstraAsedio.seq': 'mod/seq/AstraAsedio.seq',
    'meshes/AstraAsedio/voladizo_este.nif': 'addons/WhiterunTorres/meshes/AstraAsedio/voladizo_este.nif',
    'meshes/AstraAsedio/voladizo_oeste.nif': 'addons/WhiterunTorres/meshes/AstraAsedio/voladizo_oeste.nif',
    'meshes/AstraAsedio/torre_atalaya_v20.nif': 'addons/Atalaya/meshes/AstraAsedio/torre_atalaya_v20.nif',
    'Docs/AstraAsedio/README_v21.md': 'docs/README_v21.md',
}

# Los unicos archivos del ZIP v21 que v22 puede haber tocado.
CAMBIADAS = {
    'mod/AstraAsedio.esp',                                   # tres ACTI: alta del jugador, tombstones y baja del guardia
    'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp',  # los voladizos pasan a puestos solo-guardia
    'mod/scripts/source/AstraAsedioActi.psc',                # OcupadaGuardia, para la IA del guardia
    'mod/scripts/source/AstraAsedioGuard.psc',               # puente de pose del guardia
    # PEX: el compilador de Papyrus NO es determinista, asi que cualquier recompilacion
    # cambia los bytes. Estos seis son el sello de la recompilacion de v21/v22.
    'mod/scripts/AstraAsedioActi.pex',
    'mod/scripts/AstraAsedioGuard.pex',
    'mod/scripts/AstraAsedioPlayerAlias.pex',
    'mod/scripts/AstraAsedioSession.pex',
    'mod/scripts/AstraAsedioStation.pex',
    'mod/scripts/AstraSightNative.pex',
}

# El addon de animacion del guardia, con los clips REHORNEADOS 36 u mas abajo.
GUARDANIM = {
    'addons/GuardAnim/AstraAsedio_GuardAnim.esp':
        'eea4d177a39a3d0b18435214f16c719023a2d691ab4d3ec18aa12e23ae4b9ff2',
    'addons/GuardAnim/meshes/actors/character/animations/AstraAsedio/Guard/astra_guard_fire.hkx':
        '006a551c76aa8dd69ebc99009e0e0aebe06f69b8874050a98e63dbff757a1c69',
    'addons/GuardAnim/meshes/actors/character/animations/AstraAsedio/Guard/astra_guard_operate.hkx':
        'ead96439eb23f3a895f4cf218b056bb0c780c96e74fbeb8635f14b2ee7151d06',
    'addons/GuardAnim/meshes/actors/character/animations/OpenAnimationReplacer/AstraAsedioGuard/config.json':
        '1c36bf42bfd828617c9e96f1893447df2accf306606ccc15ae3dac64316aa135',
    'addons/GuardAnim/meshes/actors/character/animations/OpenAnimationReplacer/AstraAsedioGuard/Fire/config.json':
        '3f323c8b0c25619deefb9889b89b1a2e664d3b798b2dc40d3eb3d3069645dbbb',
    'addons/GuardAnim/meshes/actors/character/animations/OpenAnimationReplacer/AstraAsedioGuard/Fire/IdleHandsBehindBack.hkx':
        '006a551c76aa8dd69ebc99009e0e0aebe06f69b8874050a98e63dbff757a1c69',
    'addons/GuardAnim/meshes/actors/character/animations/OpenAnimationReplacer/AstraAsedioGuard/Fire/IdleHandsBehindBack_Enter.hkx':
        '006a551c76aa8dd69ebc99009e0e0aebe06f69b8874050a98e63dbff757a1c69',
    'addons/GuardAnim/meshes/actors/character/animations/OpenAnimationReplacer/AstraAsedioGuard/Operate/config.json':
        'c91e08fc79c45d1e84a510794393b371030bd4007de909b419c76c5220fcbd27',
    'addons/GuardAnim/meshes/actors/character/animations/OpenAnimationReplacer/AstraAsedioGuard/Operate/IdleHandsBehindBack.hkx':
        'ead96439eb23f3a895f4cf218b056bb0c780c96e74fbeb8635f14b2ee7151d06',
    'addons/GuardAnim/meshes/actors/character/animations/OpenAnimationReplacer/AstraAsedioGuard/Operate/IdleHandsBehindBack_Enter.hkx':
        'ead96439eb23f3a895f4cf218b056bb0c780c96e74fbeb8635f14b2ee7151d06',
}

# Los clips de autoria propia que alimentan al addon (fuente, no copia).
CLIPS_FUENTE = {
    'source/anim/astra_guard_fire.hkx':
        '006a551c76aa8dd69ebc99009e0e0aebe06f69b8874050a98e63dbff757a1c69',
    'source/anim/astra_guard_operate.hkx':
        'ead96439eb23f3a895f4cf218b056bb0c780c96e74fbeb8635f14b2ee7151d06',
}

NIF_ALTO_SHA = 'bcee401b79a3708ec16452ba23dd7e6364eb421bab310a218595232fac5d9e17'
NIF_BAJO_SHA = 'ebe715e73d90b136c8d7880f1a230e37bd4bf13e864f24acca384910210aabae'
GUARD_PSC_SHA = '43a146aa163cb4ee84c1b4b012740d412cbd6a41689e5d29bdfe2e40c24fcd29'
GUARD_PEX_SHA = '3aa60a9d1f3b782004fe0de88b1b3731d8590b5b12a6b8345367f32d461a1352'


def v21_entries():
    base = json.loads((ROOT / 'reports/base_archive.json').read_text())
    with zipfile.ZipFile(Path(base['path'])) as z:
        return base, {n.replace('\\', '/'): hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()}


def repo_path(name):
    if name in V21_MAP:
        return V21_MAP[name]
    if name.startswith('meshes/AstraAsedio/') or name.startswith('scripts/'):
        return 'mod/' + name
    if name.startswith('Docs/AstraAsedio/Licenses/'):
        return 'native/licenses/' + Path(name).name
    raise KeyError('entrada del ZIP v21 sin mapear: ' + name)


class ReleaseV22(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base, cls.v21 = v21_entries()

    def test_the_baseline_archive_is_the_pinned_one(self):
        self.assertEqual(sha(Path(self.base['path'])), self.base['sha256'])

    def test_drift_from_v21_is_exactly_the_documented_delta(self):
        changed, missing = set(), set()
        for name, digest in self.v21.items():
            p = ROOT / repo_path(name)
            if not p.is_file():
                missing.add(repo_path(name))
                continue
            if sha(p) != digest:
                changed.add(repo_path(name))
        self.assertEqual(missing, set(), 'el ZIP v21 trae archivos que el arbol perdio')
        self.assertEqual(changed, CAMBIADAS)

    def test_the_player_turret_nif_is_untouched(self):
        # El nucleo del diseno v22: la torreta del jugador NO se baja, por eso la
        # mira nativa sigue cumpliendo su contrato de altura.
        self.assertEqual(sha(ROOT / 'mod/meshes/AstraAsedio/ballesta.nif'), NIF_ALTO_SHA)

    def test_the_low_turret_nif_is_the_exact_lowering(self):
        self.assertEqual(sha(ROOT / 'mod/meshes/AstraAsedio/ballesta_guardia.nif'), NIF_BAJO_SHA)
        self.assertEqual(verify_torreta_baja_v22.main(), 0)

    def test_core_and_addons_hold_the_v22_contract(self):
        self.assertEqual(verify_core_v22.main(), 0)

    def test_the_guard_script_carries_the_pose_bridge(self):
        psc = (ROOT / 'mod/scripts/source/AstraAsedioGuard.psc')
        self.assertEqual(sha(psc), GUARD_PSC_SHA)
        self.assertEqual(sha(ROOT / 'mod/scripts/AstraAsedioGuard.pex'), GUARD_PEX_SHA)
        for needle in ('LoadGuardAnimation', 'StartGuardPose', 'SetGuardFirePose', 'ChooseVisualTarget'):
            self.assertIn(needle, psc.read_text(encoding='utf-8'))

    def test_the_frozen_guard_pex_is_a_faithful_compile(self):
        report = json.loads((ROOT / 'reports/guard_compile.json').read_text())
        self.assertTrue(report['success'])
        self.assertEqual(report['source_sha256'], GUARD_PSC_SHA)
        self.assertEqual(report['pex_sha256'], GUARD_PEX_SHA)
        self.assertIs(report['compiler_deterministic'], False)
        self.assertIs(report['frozen_pex_is_faithful_compile'], True)
        self.assertTrue(report['bytecode_safety']['no_none_to_array_casts'])

    def test_the_guardanim_addon_matches_the_shipped_hashes(self):
        for name, digest in {**GUARDANIM, **CLIPS_FUENTE}.items():
            p = ROOT / name
            self.assertTrue(p.is_file(), name)
            self.assertEqual(sha(p), digest, name)

    def test_the_player_keeps_the_high_turret_in_config(self):
        cfg = json.loads((ROOT / 'config.json').read_text())
        self.assertEqual(cfg['pitch_pivot_units'], 153.0)
        self.assertEqual(cfg['guardia']['muzzle_alto'], 172.6)
        self.assertTrue(cfg['use_sight_camera'])
        self.assertNotIn('turret_drop_units', cfg)

    def test_the_bridge_reproduces_the_shipped_source(self):
        # El puente es determinista aunque el compilador no lo sea: sobre el ZIP v21
        # congelado tiene que devolver exactamente el .psc enviado.
        import build_bridge
        base = json.loads((ROOT / 'reports/base_archive.json').read_text())
        before = sha(ROOT / 'mod/scripts/source/AstraAsedioGuard.psc')
        self.assertEqual(before, GUARD_PSC_SHA)
        build_bridge.main()
        self.assertEqual(sha(ROOT / 'mod/scripts/source/AstraAsedioGuard.psc'), GUARD_PSC_SHA)
        report = json.loads((ROOT / 'reports/bridge_v22.json').read_text())
        self.assertEqual(report['baseline_sha256'], base['sha256'])
        self.assertEqual(report['guard_psc_sha256'], GUARD_PSC_SHA)


if __name__ == '__main__':
    unittest.main()
