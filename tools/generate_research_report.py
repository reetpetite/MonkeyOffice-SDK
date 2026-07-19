#!/usr/bin/env python3
from pathlib import Path
import argparse
import yaml

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    parser = argparse.ArgumentParser(description="Erzeugt einen Forschungsbericht.")
    parser.add_argument("experiment_id")
    parser.add_argument("--build", required=True, type=int)
    args = parser.parse_args()

    base = ROOT / "research" / args.experiment_id
    experiment = yaml.safe_load(
        (base / "experiment.yaml").read_text(encoding="utf-8")
    )
    observation = yaml.safe_load(
        (base / f"observed-build{args.build}.yaml").read_text(encoding="utf-8")
    )

    expressions = {
        item["id"]: item["expression"]
        for item in experiment.get("tests", [])
    }

    lines = [
        f'# {experiment["id"]} – {experiment["title"]}',
        "",
        f'**Status:** `{experiment.get("status", "unknown")}`  ',
        f'**Build:** `{observation["build"]["build"]}`  ',
        f'**Plattform:** `{observation["build"]["platform"]}`',
        "",
        "## Ergebnisse",
        "",
        "| Test | Ausdruck | Beobachtung |",
        "|---|---|---|",
    ]
    for test_id, value in observation.get("results", {}).items():
        expression = expressions.get(test_id, "<unbekannt>")
        lines.append(f"| `{test_id}` | `{expression}` | `{value}` |")

    lines.extend([
        "",
        "## Rohdaten",
        "",
        "```text",
        observation.get("raw", ""),
        "```",
        "",
    ])

    target = base / f"report-build{args.build}.md"
    target.write_text("\n".join(lines), encoding="utf-8")
    print(target.relative_to(ROOT))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
