"""Verificador de compliance fail-closed: Prohíbe subir assets protegidos de Bethesda."""
import sys
import subprocess
from pathlib import Path

FORBIDDEN_EXTENSIONS = {'.esm', '.bsa', '.ba2', '.dds', '.hkx', '.tri', '.fuz', '.xwm'}
FORBIDDEN_KEYWORDS = {'skyrim.esm', 'dawnguard.esm', 'dragonborn.esm', 'hearthfires.esm', 'update.esm'}

def main():
    repo_root = Path(__file__).resolve().parents[1]
    
    # Obtener archivos en el staging area de git
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only'],
        cwd=repo_root,
        capture_output=True,
        text=True
    )
    
    staged_files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    violations = []
    
    for f in staged_files:
        path = Path(f)
        ext = path.suffix.lower()
        name = path.name.lower()
        
        if ext in FORBIDDEN_EXTENSIONS:
            violations.append(f"Extensión prohibida de Bethesda detectada: {f}")
        if name in FORBIDDEN_KEYWORDS:
            violations.append(f"Archivo propietario de Bethesda detectado: {f}")
        if any(part in ('build', 'dist', 'extracted') for part in path.parts):
            violations.append(f"Directorio excluido de artefactos/caches detectado: {f}")

    if violations:
        print("\n" + "=" * 70, file=sys.stderr)
        print("ERROR CRÍTICO DE COMPLIANCE: ACTIVOS NO PERMITIDOS EN STAGING", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        for v in violations:
            print(f"  [X] {v}", file=sys.stderr)
        print("\nOperación abortada para proteger la integridad del repositorio.", file=sys.stderr)
        print("=" * 70 + "\n", file=sys.stderr)
        sys.exit(1)

    print("Compliance check OK: Ningún archivo prohibido de Bethesda detectado.")
    sys.exit(0)

if __name__ == '__main__':
    main()
