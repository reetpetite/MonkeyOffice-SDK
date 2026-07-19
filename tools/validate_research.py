#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_ROOT = ROOT / "research"
ID_RE = re.compile(r"^MO-\d{3}$")

def main() -> int:
    errors = []
    seen = set()

    for path in sorted(RESEARCH_ROOT.glob("MO-*/experiment.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        experiment_id = data.get("id")

        if not ID_RE.fullmatch(str(experiment_id)):
            errors.append(f"{path}: ungültige Experiment-ID {experiment_id!r}")
        if experiment_id in seen:
            errors.append(f"{path}: doppelte Experiment-ID {experiment_id}")
        seen.add(experiment_id)

        if path.parent.name != experiment_id:
            errors.append(
                f"{path}: Verzeichnisname und Experiment-ID stimmen nicht überein"
            )

        tests = data.get("tests", [])
        test_ids = set()
        for test in tests:
            test_id = test.get("id")
            expression = test.get("expression")
            if not test_id:
                errors.append(f"{path}: Test ohne ID")
            elif test_id in test_ids:
                errors.append(f"{path}: doppelte Test-ID {test_id}")
            test_ids.add(test_id)
            if not expression:
                errors.append(f"{path}: Test {test_id} ohne Ausdruck")

        for observed in path.parent.glob("observed-build*.yaml"):
            result_data = yaml.safe_load(observed.read_text(encoding="utf-8"))
            if result_data.get("experiment") != experiment_id:
                errors.append(
                    f"{observed}: falsche Experiment-ID "
                    f"{result_data.get('experiment')!r}"
                )
            observed_ids = set(result_data.get("results", {}))
            missing = test_ids - observed_ids
            unexpected = observed_ids - test_ids
            if missing:
                errors.append(
                    f"{observed}: fehlende Tests: {', '.join(sorted(missing))}"
                )
            if unexpected:
                errors.append(
                    f"{observed}: unbekannte Tests: {', '.join(sorted(unexpected))}"
                )

    if errors:
        print("Forschungsvalidierung fehlgeschlagen:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Forschungsvalidierung erfolgreich: {len(seen)} Experiment(e)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
