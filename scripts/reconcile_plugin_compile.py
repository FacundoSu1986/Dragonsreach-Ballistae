"""Reconcilia la entrada del guardia en `reports/plugin_compile.json` con el .pex congelado.

## Por que existe

`scripts/compile_papyrus.py` compila los 8 scripts y escribe cada `.pex` **en el lugar**
(`shutil.copy2(staged, q)`). Para el guardia eso es destructivo: el compilador de Papyrus
no es determinista (dos corridas del mismo `.psc` dan `.pex` distintos), asi que una
corrida nueva cambiaria el sha del `.pex` congelado y, con el, el del paquete.

Por eso el guardia no se recompila: se **congela** y se **verifica**
(`scripts/compile_bridge.py` -> `reports/guard_compile.json`). Consecuencia: la entrada
del guardia en `reports/plugin_compile.json` queda anclada al ultimo `compile_papyrus`
completo (hoy, el de v21: `.psc` `46f4e833…`, `.pex` `c54fed80…`) y no refleja el
artefacto que realmente se embarca.

## Que hace

Propaga a esa unica entrada los hechos **medidos** del guardia congelado, tomados de
`reports/guard_compile.json` y de los archivos en disco. No inventa valores: lo que no
se midio, no se escribe.

Si alguna de las otras siete entradas estuviera desfasada respecto del disco, **falla**.
Reescribirlas seria tapar un problema mayor (un `compile_papyrus` viejo o un `.psc`
editado a mano), no arreglarlo.

Idempotente: correrlo dos veces deja el mismo archivo.

Escribe `reports/plugin_compile.json`. Imprime `PLUGIN_COMPILE_RECONCILED <psc> <pex>`.
"""
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from pex_metadata import metadata

REPORT = ROOT / 'reports/plugin_compile.json'
FACTS = ROOT / 'reports/guard_compile.json'
PSC = ROOT / 'mod/scripts/source/AstraAsedioGuard.psc'
PEX = ROOT / 'mod/scripts/AstraAsedioGuard.pex'
PAS = ROOT / 'reports/papyrus_bytecode/AstraAsedioGuard.disassemble.pas'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    report = json.loads(REPORT.read_text(encoding='utf-8'))
    facts = json.loads(FACTS.read_text(encoding='utf-8'))

    assert facts['success'] and facts['frozen_pex_is_faithful_compile'], \
        'el .pex congelado no esta verificado como compilado fiel; no se reconcilia'
    assert not facts['compiler_deterministic'], \
        'si el compilador fuese determinista, la politica de congelar no haria falta'

    # Anclar la reconciliacion a los artefactos que realmente estan en disco.
    assert sha(PSC) == facts['source_sha256'], 'el .psc en disco no es el que se verifico'
    assert sha(PEX) == facts['pex_sha256'], 'el .pex en disco no es el congelado verificado'
    assert sha(PAS) == facts['disassembly_sha256'], 'el .pas en disco no es el verificado'

    guard = [s for s in report['scripts'] if Path(s['source']).name == PSC.name]
    assert len(guard) == 1, f'se esperaba una entrada para {PSC.name}, hay {len(guard)}'
    guard = guard[0]

    # Las otras entradas son de compile_papyrus: si alguna no coincide con el disco,
    # el problema es mas grande y hay que verlo, no parchear por encima.
    for s in report['scripts']:
        if s is guard:
            continue
        assert s['source_sha256'] == sha(ROOT / s['source']), \
            f"entrada ajena desfasada: {s['source']} (corre compile_papyrus.py)"
        assert s['sha256'] == sha(ROOT / s['pex']), \
            f"entrada ajena desfasada: {s['pex']} (corre compile_papyrus.py)"

    header, _ = metadata(PEX.read_bytes())
    safety = dict(facts['bytecode_safety'])   # lo medido en la compilacion real
    safety['anonymized_header'] = header      # leido del .pex congelado
    safety['disassembly'] = str(PAS.relative_to(ROOT))
    safety['disassembly_sha256'] = facts['disassembly_sha256']

    guard.update({
        'source_sha256': facts['source_sha256'],
        'sha256': facts['pex_sha256'],
        'exit_code': 0,
        'assembler_exit_code': 0,
        'success': True,
        'bytecode_safety': safety,
        'frozen': True,
        'compiler_deterministic': False,
        'verified_by': str(FACTS.relative_to(ROOT)),
        'output': (
            'ENTRADA CONGELADA. El .pex embarcado no se recompila: el compilador de Papyrus '
            'no es determinista, asi que se congela y se verifica. La fidelidad del .pex '
            'respecto de este .psc la prueba reports/guard_compile.json, que compara el '
            'desensamblado normalizado de una compilacion real contra el .pas congelado. '
            'No correr compile_papyrus.py sobre esta entrada: pisaria el .pex congelado.'
        ),
    })
    report['frozen_entries'] = [PSC.name]

    REPORT.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('PLUGIN_COMPILE_RECONCILED', facts['source_sha256'], facts['pex_sha256'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
