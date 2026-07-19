#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def run(script: str, *args: str) -> None:
    command = [sys.executable, str(ROOT / "tools" / script), *args]
    subprocess.run(command, cwd=ROOT, check=True)

def main() -> int:
    run("validate_data.py")
    run("validate_research.py")
    run("generate_docs.py")

    # Reproducible research artifacts
    for experiment_id in ("MO-027", "MO-028", "MO-029"):
        run("generate_experiment.py", experiment_id)

    for experiment_id in ("MO-027", "MO-028"):
        run("generate_research_report.py", experiment_id, "--build", "249")

    print("Build erfolgreich.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
