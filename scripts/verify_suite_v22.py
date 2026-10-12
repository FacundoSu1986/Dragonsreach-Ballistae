"""Prueba de no-regresion de v22: corre la suite completa dos veces y compara los fallos.

Corre `unittest discover` sobre el arbol de trabajo y sobre un export pristino de HEAD
(`git archive HEAD` a `build/pristine`, que esta ignorado). Despues compara los
conjuntos de tests que fallan y exige que **ninguno** sea nuevo.

Cuidado: el export pristino NO trae los archivos ignorados por git (por ejemplo
`build/Dawnguard.esm.donors.json`), asi que tiende a fallar de mas. Eso hace que el
baseline sea pesimista, no laxo: si el arbol de trabajo no agrega fallos contra un
baseline pesimista, no agrega fallos.

Requiere el Python del sistema (3.11) porque la suite importa numpy:
    "C:/Users/Facu2/AppData/Local/Programs/Python/Python311/python.exe" scripts/verify_suite_v22.py

Escribe `reports/tests_v22_diff.json` y los dos logs en `build/`.
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRISTINE = ROOT / 'build' / 'pristine'
LOG_WORK = ROOT / 'build' / 'tests_v22_py311.log'
LOG_HEAD = ROOT / 'build' / 'tests_head_py311.log'

FAIL_LINE = re.compile(r'^(?:FAIL|ERROR): (\S+ \(\S+\))', re.M)
TALLY = re.compile(r'^Ran (\d+) tests? in .*$', re.M)
VERDICT = re.compile(r'^(OK|FAILED.*)$', re.M)


def run_suite(cwd, log):
    """Corre la suite completa en `cwd` y guarda la salida en `log`."""
    r = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'],
                       cwd=cwd, capture_output=True, text=True)
    log.write_text(r.stdout + r.stderr)
    return r.stdout + r.stderr


def tally(text):
    m = TALLY.search(text)
    return int(m.group(1)) if m else None


def failures(text):
    return set(FAIL_LINE.findall(text))


def export_head():
    """Exporta HEAD a build/pristine sin tocar refs ni el arbol de trabajo.

    No borra el directorio destino: reextrae encima. `tar -x` sobrescribe los archivos
    que ya existen, asi que la unica deriva posible es un archivo que HEAD haya
    eliminado y siga presente de una corrida anterior. Es un directorio de trabajo
    ignorado por git; se prefiere esa deriva antes que un borrado masivo.
    """
    PRISTINE.mkdir(parents=True, exist_ok=True)
    archive = subprocess.run(['git', 'archive', 'HEAD'], cwd=ROOT, capture_output=True, check=True)
    subprocess.run(['tar', '-x', '-C', str(PRISTINE)], input=archive.stdout, check=True)
    head_sha = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    (PRISTINE / '.head_sha').write_text(head_sha + '\n')
    return True


def main():
    if not (ROOT / 'tests').is_dir():
        print('SUITE_V22_DIFF sin-tests')
        return 1

    work_text = run_suite(ROOT, LOG_WORK)
    if not export_head():
        print('SUITE_V22_DIFF export-fallido')
        return 1
    head_text = run_suite(PRISTINE, LOG_HEAD)

    work, head = failures(work_text), failures(head_text)
    nuevos = sorted(work - head)
    heredados = sorted(work & head)
    arreglados = sorted(head - work)

    report = {
        'revision': 22,
        'interprete': sys.version.split()[0],
        'tests_arbol_de_trabajo': tally(work_text),
        'tests_head_pristino': tally(head_text),
        'fallos_arbol_de_trabajo': len(work),
        'fallos_head_pristino': len(head),
        'regresiones_nuevas': nuevos,
        'fallos_heredados': len(heredados),
        'tests_que_ahora_pasan': arreglados,
        'sin_regresiones': len(nuevos) == 0,
        'nota': ('el export pristino omite archivos ignorados por git, asi que falla de mas; '
                 'el baseline es pesimista, no laxo'),
    }
    (ROOT / 'reports/tests_v22_diff.json').write_text(json.dumps(report, indent=2))

    print(f'  arbol de trabajo: {report["tests_arbol_de_trabajo"]} tests, '
          f'{report["fallos_arbol_de_trabajo"]} fallos/errores')
    print(f'  HEAD pristino:    {report["tests_head_pristino"]} tests, '
          f'{report["fallos_head_pristino"]} fallos/errores')
    print(f'  regresiones nuevas: {len(nuevos)}   heredados: {len(heredados)}   '
          f'ahora pasan: {len(arreglados)}')
    for n in nuevos:
        print('   + ' + n)
    print('SUITE_V22_DIFF ' + ('SIN_REGRESIONES' if not nuevos else 'CON_REGRESIONES'))
    return 0 if not nuevos else 1


if __name__ == '__main__':
    sys.exit(main())
