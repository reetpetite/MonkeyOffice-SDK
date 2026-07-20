#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_ROOT = ROOT / "research"
ID_RE = re.compile(r"^MO-\d{3}$")
CASE_ID_RE = re.compile(r"^[A-Z][A-Z0-9]*\d{2}$")


def validate_expression_experiment(path: Path, data: dict, errors: list[str]) -> set[str]:
    tests = data.get("tests", [])
    if not isinstance(tests, list) or not tests:
        errors.append(f"{path}: Ausdrucksexperiment ohne Tests")
        return set()
    test_ids: set[str] = set()
    for test in tests:
        test_id = test.get("id") if isinstance(test, dict) else None
        expression = test.get("expression") if isinstance(test, dict) else None
        if not test_id:
            errors.append(f"{path}: Test ohne ID")
        elif test_id in test_ids:
            errors.append(f"{path}: doppelte Test-ID {test_id}")
        else:
            test_ids.add(str(test_id))
        if not expression:
            errors.append(f"{path}: Test {test_id} ohne Ausdruck")
    return test_ids


def validate_script_matrix(path: Path, data: dict, errors: list[str]) -> set[str]:
    cases = data.get("cases", [])
    if not isinstance(cases, list) or not cases:
        errors.append(f"{path}: Script-Matrix ohne Fälle")
        return set()
    case_ids: set[str] = set()
    referenced_scripts: set[Path] = set()
    for case in cases:
        case_id = case.get("id") if isinstance(case, dict) else None
        script_name = case.get("script") if isinstance(case, dict) else None
        if not case_id or not CASE_ID_RE.fullmatch(str(case_id)):
            errors.append(f"{path}: ungültige Fall-ID {case_id!r}")
        elif case_id in case_ids:
            errors.append(f"{path}: doppelte Fall-ID {case_id}")
        else:
            case_ids.add(str(case_id))
        if not script_name:
            errors.append(f"{path}: Fall {case_id} ohne Script")
            continue
        script_path = path.parent / str(script_name)
        try:
            script_path.relative_to(path.parent)
        except ValueError:
            errors.append(f"{path}: Script außerhalb des Experiments: {script_name}")
            continue
        if script_path.suffix != ".monkey":
            errors.append(f"{path}: Fall {case_id} verwendet keine .monkey-Datei")
        if not script_path.is_file():
            errors.append(f"{path}: Script fehlt: {script_name}")
            continue
        referenced_scripts.add(script_path.resolve())
        raw = script_path.read_bytes()
        try:
            text = raw.decode("ascii")
        except UnicodeDecodeError:
            errors.append(f"{script_path}: Script ist nicht ASCII-kodiert")
            continue
        marker = f"{data.get('id')}|{case_id}"
        if marker not in text:
            errors.append(f"{script_path}: Erfolgssignal {marker!r} fehlt")
    for script_path in sorted((path.parent / "cases").glob("*.monkey")):
        if script_path.resolve() not in referenced_scripts:
            errors.append(f"{script_path}: nicht in experiment.yaml referenziert")
    expected = path.parent / "expected.md"
    if not expected.is_file():
        errors.append(f"{path}: expected.md fehlt")
    return case_ids


def main() -> int:
    errors: list[str] = []
    seen: set[str] = set()

    for path in sorted(RESEARCH_ROOT.glob("MO-*/experiment.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            errors.append(f"{path}: Wurzel muss ein Mapping sein")
            continue
        experiment_id = data.get("id")

        if not ID_RE.fullmatch(str(experiment_id)):
            errors.append(f"{path}: ungültige Experiment-ID {experiment_id!r}")
        if experiment_id in seen:
            errors.append(f"{path}: doppelte Experiment-ID {experiment_id}")
        seen.add(str(experiment_id))

        if path.parent.name != experiment_id:
            errors.append(f"{path}: Verzeichnisname und Experiment-ID stimmen nicht überein")

        kind = data.get("kind", "expression-batch")
        if kind == "script-matrix":
            expected_ids = validate_script_matrix(path, data, errors)
        elif kind == "expression-batch":
            expected_ids = validate_expression_experiment(path, data, errors)
        else:
            errors.append(f"{path}: unbekannter Experimenttyp {kind!r}")
            expected_ids = set()

        for observed in path.parent.glob("observed-build*.yaml"):
            result_data = yaml.safe_load(observed.read_text(encoding="utf-8"))
            if result_data.get("experiment") != experiment_id:
                errors.append(f"{observed}: falsche Experiment-ID {result_data.get('experiment')!r}")
            observed_ids = set(result_data.get("results", {}))
            missing = expected_ids - observed_ids
            unexpected = observed_ids - expected_ids
            if missing:
                errors.append(f"{observed}: fehlende Fälle: {', '.join(sorted(missing))}")
            if unexpected:
                errors.append(f"{observed}: unbekannte Fälle: {', '.join(sorted(unexpected))}")

    if errors:
        print("Forschungsvalidierung fehlgeschlagen:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Forschungsvalidierung erfolgreich: {len(seen)} Experiment(e)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
