#!/usr/bin/env python3
from pathlib import Path
import argparse
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_observation(experiment_id: str, build: int) -> dict:
    path = (
        ROOT / "research" / experiment_id /
        f"observed-build{build}.yaml"
    )
    if not path.exists():
        raise FileNotFoundError(path)
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def main() -> int:
    parser = argparse.ArgumentParser(description="Vergleicht zwei beobachtete Builds.")
    parser.add_argument("experiment_id")
    parser.add_argument("build_a", type=int)
    parser.add_argument("build_b", type=int)
    args = parser.parse_args()

    left = load_observation(args.experiment_id, args.build_a)
    right = load_observation(args.experiment_id, args.build_b)
    left_results = left.get("results", {})
    right_results = right.get("results", {})

    ids = sorted(set(left_results) | set(right_results))
    changed = 0

    print(f"# {args.experiment_id}: Buildvergleich")
    print()
    print("| Test | Build " + str(args.build_a) + " | Build " + str(args.build_b) + " | Status |")
    print("|---|---|---|---|")
    for test_id in ids:
        a = left_results.get(test_id, "<fehlt>")
        b = right_results.get(test_id, "<fehlt>")
        status = "gleich" if a == b else "GEÄNDERT"
        if a != b:
            changed += 1
        print(f"| {test_id} | `{a}` | `{b}` | {status} |")

    print()
    print(f"Geänderte Tests: {changed}")
    return 1 if changed else 0

if __name__ == "__main__":
    raise SystemExit(main())
