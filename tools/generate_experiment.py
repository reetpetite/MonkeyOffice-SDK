#!/usr/bin/env python3
from pathlib import Path
import argparse
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_experiment(experiment_id: str) -> dict:
    path = ROOT / "research" / experiment_id / "experiment.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Experiment nicht gefunden: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Ungültige Experimentdatei: {path}")
    return data

def escape_monkey_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')

def generate_script(data: dict) -> str:
    experiment_id = data["id"]
    tests = data.get("tests", [])
    if not tests:
        raise ValueError(f"{experiment_id}: keine Tests definiert")

    parts = [f'"{escape_monkey_string(experiment_id)}"']
    for test in tests:
        test_id = test["id"]
        expression = test["expression"]
        parts.append(f'"|{escape_monkey_string(test_id)}=["+{expression}+"]"')

    # MonKey Office accepts this expression only on one script line.
    msgbox_line = "msgBox(" + "+".join(parts) + ")"
    return msgbox_line + "\nexit\n"

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Erzeugt ein MonKey-Office-Testskript aus experiment.yaml."
    )
    parser.add_argument("experiment_id", help="z. B. MO-029")
    parser.add_argument(
        "-o", "--output",
        help="Ausgabedatei; Standard: research/<ID>/script.monkey"
    )
    args = parser.parse_args()

    data = load_experiment(args.experiment_id)
    script = generate_script(data)

    target = (
        Path(args.output)
        if args.output
        else ROOT / "research" / args.experiment_id / "script.monkey"
    )
    if not target.is_absolute():
        target = ROOT / target
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(script, encoding="ascii")
    print(target.relative_to(ROOT))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
