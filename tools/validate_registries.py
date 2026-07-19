#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

VALIDATORS = (
    "validate_types.py",
    "validate_language_symbols.py",
    "validate_diagnostics.py",
    "validate_conformance.py",
)

def main() -> int:
    for script in VALIDATORS:
        subprocess.run(
            [sys.executable, str(ROOT / "tools" / script)],
            cwd=ROOT,
            check=True,
        )
    print("Alle Registry-Validatoren erfolgreich ausgeführt.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
