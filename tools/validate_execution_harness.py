#!/usr/bin/env python3
"""Validate the interpreter execution manifest and recorded observations."""

from __future__ import annotations

from pathlib import Path
import re
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "runner" / "execution-manifest.yaml"
ID_RE = re.compile(r"^MO-\d{3}$")
CASE_RE = re.compile(r"^[A-Z]\d{2}$")
ALLOWED_STATUSES = {
    "not-run", "accepted", "parser-error", "runtime-error",
    "unexpected-output", "crash", "hang", "skipped",
}


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    try:
        manifest = load_yaml(MANIFEST)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"Execution-harness validation failed: {exc}", file=sys.stderr)
        return 1

    if manifest.get("schema_version") != 1:
        fail(errors, "runner manifest must use schema_version: 1")
    if not isinstance(manifest.get("default_build"), int):
        fail(errors, "default_build must be an integer")

    seen_experiments: set[str] = set()
    result_files = 0
    cases_total = 0
    for experiment in manifest.get("experiments", []):
        experiment_id = experiment.get("id")
        if not isinstance(experiment_id, str) or not ID_RE.fullmatch(experiment_id):
            fail(errors, f"invalid experiment id: {experiment_id!r}")
            continue
        if experiment_id in seen_experiments:
            fail(errors, f"duplicate experiment id: {experiment_id}")
        seen_experiments.add(experiment_id)

        directory_value = experiment.get("directory")
        if not isinstance(directory_value, str):
            fail(errors, f"{experiment_id}: directory must be a string")
            continue
        directory = ROOT / directory_value
        if not directory.is_dir():
            fail(errors, f"{experiment_id}: missing directory {directory_value}")

        for key in ("result_pattern", "report_pattern"):
            pattern = experiment.get(key)
            if not isinstance(pattern, str) or "{build}" not in pattern:
                fail(errors, f"{experiment_id}: {key} must contain {{build}}")

        seen_cases: set[str] = set()
        manifest_cases = experiment.get("cases", [])
        if not manifest_cases:
            fail(errors, f"{experiment_id}: no cases declared")
        for case in manifest_cases:
            case_id = case.get("id")
            if not isinstance(case_id, str) or not CASE_RE.fullmatch(case_id):
                fail(errors, f"{experiment_id}: invalid case id {case_id!r}")
                continue
            if case_id in seen_cases:
                fail(errors, f"{experiment_id}: duplicate case {case_id}")
            seen_cases.add(case_id)
            cases_total += 1
            script_value = case.get("script")
            if not isinstance(script_value, str):
                fail(errors, f"{experiment_id}/{case_id}: script must be a string")
            elif not (directory / script_value).is_file():
                fail(errors, f"{experiment_id}/{case_id}: missing script {script_value}")

        result_pattern = experiment.get("result_pattern")
        if not isinstance(result_pattern, str):
            continue
        result_parent = ROOT / result_pattern.split("{build}")[0]
        search_root = directory / "results"
        if not search_root.exists():
            continue
        for observed in search_root.glob("build*/observed.yaml"):
            result_files += 1
            try:
                data = load_yaml(observed)
            except (OSError, ValueError, yaml.YAMLError) as exc:
                fail(errors, f"{observed.relative_to(ROOT)}: {exc}")
                continue
            if data.get("experiment") != experiment_id:
                fail(errors, f"{observed.relative_to(ROOT)}: experiment mismatch")
            if not isinstance(data.get("build"), int):
                fail(errors, f"{observed.relative_to(ROOT)}: build must be integer")
            observed_cases = data.get("cases")
            if not isinstance(observed_cases, dict):
                fail(errors, f"{observed.relative_to(ROOT)}: cases must be mapping")
                continue
            if set(observed_cases) != seen_cases:
                missing = seen_cases - set(observed_cases)
                unknown = set(observed_cases) - seen_cases
                if missing:
                    fail(errors, f"{observed.relative_to(ROOT)}: missing cases {sorted(missing)}")
                if unknown:
                    fail(errors, f"{observed.relative_to(ROOT)}: unknown cases {sorted(unknown)}")
            for case_id, result in observed_cases.items():
                if not isinstance(result, dict):
                    fail(errors, f"{observed.relative_to(ROOT)}: {case_id} must be mapping")
                    continue
                status = result.get("status")
                if status not in ALLOWED_STATUSES:
                    fail(errors, f"{observed.relative_to(ROOT)}: invalid status {status!r}")
                if status == "accepted" and not result.get("success_signal"):
                    fail(errors, f"{observed.relative_to(ROOT)}: accepted {case_id} lacks success_signal")
                if status == "skipped" and not result.get("notes"):
                    fail(errors, f"{observed.relative_to(ROOT)}: skipped {case_id} lacks notes")
            calculated_complete = bool(observed_cases) and all(
                isinstance(item, dict) and item.get("status") != "not-run"
                for item in observed_cases.values()
            )
            if data.get("complete") is not calculated_complete:
                fail(errors, f"{observed.relative_to(ROOT)}: complete flag is inconsistent")

    for template in ("observed-build.yaml", "report.md"):
        if not (ROOT / "runner" / "templates" / template).is_file():
            fail(errors, f"missing runner template: {template}")

    if errors:
        print("Execution-harness validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Execution-harness validation successful: "
        f"{len(seen_experiments)} experiment(s), {cases_total} case(s), "
        f"{result_files} recorded result file(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
