"""Sello de verificacion de v22: contrato + los dos verificadores + compilacion del puente.

Es el unico punto de entrada que dice "v22 esta bien". `package_v22.py` lo exige antes
de archivar. Escribe `reports/verification_v22.json`.

Dependencia externa: G:/Modding/Skyrim_Runtime_1.6.1170 (Papyrus Compiler + Skyrim.esm).
"""
import datetime, hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'scripts/vendor')]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run_module(name):
    """Corre `python -m <name>` y devuelve (ok, salida)."""
    r = subprocess.run([sys.executable, '-m', name], cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr)


def run_script(path):
    r = subprocess.run([sys.executable, str(ROOT / path)], cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr)


def main():
    checks = {}

    ok, out = run_module('tests.test_v22_release')
    checks['contrato_v22'] = {'ok': ok, 'detalle': 'tests/test_v22_release.py'}
    if not ok:
        print(out[-4000:])

    ok, out = run_script('scripts/verify_core_v22.py')
    checks['core_v22'] = {'ok': ok and 'CORE_V22 OK' in out, 'detalle': 'CORE_V22 OK'}
    if not checks['core_v22']['ok']:
        print(out[-4000:])

    ok, out = run_script('scripts/verify_torreta_baja_v22.py')
    checks['torreta_baja_v22'] = {'ok': ok and 'TORRETA_BAJA_V22 OK' in out, 'detalle': 'TORRETA_BAJA_V22 OK'}
    if not checks['torreta_baja_v22']['ok']:
        print(out[-4000:])

    ok, out = run_script('scripts/compile_bridge.py')
    checks['guard_compile'] = {'ok': ok and 'GUARD_VERIFIED' in out, 'detalle': 'el .pex congelado es un compilado fiel'}
    if not checks['guard_compile']['ok']:
        print(out[-4000:])

    ok, out = run_script('scripts/reconcile_plugin_compile.py')
    checks['plugin_compile'] = {'ok': ok and 'PLUGIN_COMPILE_RECONCILED' in out,
                                'detalle': 'la entrada del guardia refleja el .pex congelado'}
    if not checks['plugin_compile']['ok']:
        print(out[-4000:])

    compile_report = json.loads((ROOT / 'reports/guard_compile.json').read_text())
    inputs = ['config.json', 'reports/base_archive.json', 'reports/bridge_v22.json',
              'reports/guard_compile.json', 'reports/torreta_baja_v22.json',
              'reports/plugin_compile.json',
              'mod/AstraAsedio.esp', 'mod/meshes/AstraAsedio/ballesta.nif',
              'mod/meshes/AstraAsedio/ballesta_guardia.nif',
              'mod/scripts/source/AstraAsedioGuard.psc', 'mod/scripts/AstraAsedioGuard.pex',
              'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp',
              'addons/Atalaya/AstraAsedio_Atalaya.esp',
              'addons/GuardAnim/AstraAsedio_GuardAnim.esp',
              'scripts/build_bridge.py', 'scripts/compile_bridge.py', 'scripts/guard_pose.pscinc',
              'scripts/bajar_ballesta.py', 'scripts/verify_core_v22.py',
              'scripts/verify_torreta_baja_v22.py', 'scripts/build_guard_bajada.py',
              'scripts/verify_suite_v22.py', 'reports/tests_v22_diff.json',
              'scripts/reconcile_plugin_compile.py']

    success = all(c['ok'] for c in checks.values())
    report = {
        'revision': 22,
        'success': success,
        'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'checks': checks,
        'design': {
            'torreta_alta': {'acti': '03000801', 'nif': 'AstraAsedio\\ballesta.nif',
                             'pivote_u': 153.0, 'muzzle_u': 172.6, 'uso': 'jugador, con mira nativa'},
            'torreta_baja': {'acti': '03000B04', 'nif': 'AstraAsedio\\ballesta_guardia.nif',
                             'pivote_u': 117.0, 'muzzle_u': 136.6, 'uso': 'guardias, sin mira'},
            'regla_de_seguridad': 'ninguna colocacion ACTIVA del ACTI bajo activa AllowPlayerTakeover ni UseSightCamera',
        },
        'guard_pex_frozen': compile_report['pex_sha256'],
        'guard_pex_recompiled': compile_report['pex_recompiled_sha256'],
        'papyrus_compiler_deterministic': compile_report['compiler_deterministic'],
        'requires_open_animation_replacer': True,
        'bundles_open_animation_replacer': False,
        'known_debt': [
            'La entrada del guardia en reports/plugin_compile.json esta CONGELADA '
            '(frozen: true) y la mantiene scripts/reconcile_plugin_compile.py. No correr '
            'compile_papyrus.py sobre esa entrada: escribe los .pex en el lugar y pisaria '
            'el .pex congelado.',
            'La suite completa arrastra fallos heredados: ver reports/tests_v22_diff.json. '
            'Ninguno es nuevo respecto de HEAD.',
            'Los hashes fijados sobre .json y .psc valen para la forma canonica del repo '
            '(.gitattributes: text eol=lf) tal como la materializa core.autocrlf=true en '
            'Windows. Un clon en otro sistema, con LF, no reproduce esos hashes. Es una '
            'propiedad heredada de todo el repo, no de v22.',
        ],
        'external_dependencies': ['G:/Modding/Skyrim_Runtime_1.6.1170',
                                  'Blender 4.4 (solo para rehornear clips o bajar el NIF)'],
        'game_tested': False,
        'nexus_uploaded': False,
        'live_installation_modified': False,
        'inputs_sha256': {n: sha(ROOT / n) for n in inputs},
    }
    (ROOT / 'reports/verification_v22.json').write_text(json.dumps(report, indent=2))

    print()
    for name, c in checks.items():
        print(('OK   ' if c['ok'] else 'FALLA') + ' ' + name)
    print('VERIFICATION_V22 ' + ('OK' if success else 'FALLIDA'))
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
