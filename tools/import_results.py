#!/usr/bin/env python3
from pathlib import Path
import argparse
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
TOKEN_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*)=\[(.*)\]$", re.DOTALL)

def parse_output(raw: str) -> tuple[str, dict[str, str]]:
    text = raw.strip()
    parts = text.split("|")
    if not parts or not re.fullmatch(r"MO-\d{3}", parts[0]):
        raise ValueError("Ausgabe beginnt nicht mit einer gültigen Experiment-ID.")

    experiment_id = parts[0]
    results = {}
    for token in parts[1:]:
        match = TOKEN_RE.fullmatch(token)
        if not match:
            raise ValueError(f"Ungültiges Ergebnistoken: {token!r}")
        test_id, value = match.groups()
        if test_id in results:
            raise ValueError(f"Doppelte Test-ID: {test_id}")
        results[test_id] = value
    return experiment_id, results

def load_experiment(experiment_id: str) -> dict:
    path = ROOT / "research" / experiment_id / "experiment.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Experimentdefinition fehlt: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def validate_test_ids(experiment: dict, results: dict[str, str]) -> list[str]:
    expected = [item["id"] for item in experiment.get("tests", [])]
    missing = [item for item in expected if item not in results]
    unexpected = [item for item in results if item not in expected]
    messages = []
    if missing:
        messages.append("Fehlende Ergebnisse: " + ", ".join(missing))
    if unexpected:
        messages.append("Unerwartete Ergebnisse: " + ", ".join(unexpected))
    return messages

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Importiert eine kopierte msgBox-Ausgabe als YAML."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Kopierte Ausgabe direkt übergeben")
    source.add_argument("--file", help="Textdatei mit kopierter Ausgabe")
    parser.add_argument("--build", required=True, type=int)
    parser.add_argument("--application", default="MonKey Office 2025")
    parser.add_argument("--platform", default="macOS")
    parser.add_argument(
        "--allow-partial", action="store_true",
        help="Auch unvollständige Ergebnislisten speichern"
    )
    args = parser.parse_args()

    raw = (
        args.text
        if args.text is not None
        else Path(args.file).read_text(encoding="utf-8")
    )
    experiment_id, results = parse_output(raw)
    experiment = load_experiment(experiment_id)
    problems = validate_test_ids(experiment, results)

    if problems and not args.allow_partial:
        for problem in problems:
            print(f"Fehler: {problem}", file=sys.stderr)
        return 1

    payload = {
        "experiment": experiment_id,
        "build": {
            "application": args.application,
            "build": args.build,
            "platform": args.platform,
        },
        "source": "copied_msgbox_output",
        "raw": raw.strip(),
        "results": results,
    }
    if problems:
        payload["validation_warnings"] = problems

    target = (
        ROOT / "research" / experiment_id /
        f"observed-build{args.build}.yaml"
    )
    target.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(target.relative_to(ROOT))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
