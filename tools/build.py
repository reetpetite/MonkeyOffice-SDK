#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def run(script: str) -> None:
    command = [sys.executable, str(ROOT / "tools" / script)]
    subprocess.run(command, cwd=ROOT, check=True)

def main() -> int:
    run("validate_data.py")
    run("generate_docs.py")
    print("Build erfolgreich.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
