#!/usr/bin/env python3
"""Validate the machine-readable diagnostic registry."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print(
        "Fehlende Abhängigkeit: jsonschema\n"
        "Bitte zuerst die Projektabhängigkeiten installieren:\n"
        "  python -m pip install -r requirements.txt",
        file=sys.stderr,
    )
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "diagnostics" / "registry.json"
SCHEMA_PATH = ROOT / "data" / "diagnostics" / "schema.json"

CODE_RE = re.compile(r"^MO-(LEX|PAR|SEM|FMT|RUN|CFG)-([0-9]{4})$")
PHASE_BY_PREFIX = {
    "LEX": "lexer",
    "PAR": "parser",
    "SEM": "semantic",
    "FMT": "formatter",
    "RUN": "runtime",
    "CFG": "configuration",
}


class ValidationFailure(Exception):
    """Raised when a registry invariant is violated."""


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise ValidationFailure(f"Datei fehlt: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationFailure(
            f"{path.relative_to(ROOT)}:{exc.lineno}:{exc.colno}: "
            f"ungültiges JSON: {exc.msg}"
        ) from exc


def json_path(parts: list[Any]) -> str:
    result = "$"
    for part in parts:
        if isinstance(part, int):
            result += f"[{part}]"
        else:
            result += f".{part}"
    return result


def validate_schema(registry: Any, schema: Any) -> list[str]:
    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(registry),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    return [
        f"{json_path(list(error.absolute_path))}: {error.message}"
        for error in errors
    ]


def validate_invariants(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    diagnostics = registry.get("diagnostics", [])

    codes = [entry.get("code") for entry in diagnostics]
    duplicates = sorted(
        code for code, count in Counter(codes).items()
        if code is not None and count > 1
    )
    for code in duplicates:
        errors.append(f"doppelter Diagnosecode: {code}")

    previous_code: str | None = None
    previous_sort_key: tuple[int, int] | None = None
    for index, entry in enumerate(diagnostics):
        code = entry.get("code")
        location = f"$.diagnostics[{index}]"

        if not isinstance(code, str):
            continue

        match = CODE_RE.fullmatch(code)
        if not match:
            continue

        prefix = match.group(1)
        expected_phase = PHASE_BY_PREFIX[prefix]
        actual_phase = entry.get("phase")
        if actual_phase != expected_phase:
            errors.append(
                f"{location}.phase: {code} verlangt Phase "
                f"{expected_phase!r}, gefunden {actual_phase!r}"
            )

        status = entry.get("status")
        deprecated_in = entry.get("deprecatedIn")
        if status == "deprecated" and not deprecated_in:
            errors.append(
                f"{location}: deprecated-Diagnose {code} benötigt deprecatedIn"
            )
        if status != "deprecated" and deprecated_in:
            errors.append(
                f"{location}: deprecatedIn ist nur bei Status "
                f"'deprecated' zulässig ({code})"
            )

        documentation = entry.get("documentation")
        if isinstance(documentation, str):
            target = ROOT / documentation
            if not target.is_file():
                errors.append(
                    f"{location}.documentation: Ziel fehlt: {documentation}"
                )

        sort_key = (
            list(PHASE_BY_PREFIX).index(prefix),
            int(match.group(2)),
        )

        if previous_sort_key is not None and sort_key < previous_sort_key:
            errors.append(
                "Diagnosen sind nicht deterministisch nach Subsystem und Nummer "
                f"sortiert: {previous_code} vor {code}"
            )

        previous_code = code
        previous_sort_key = sort_key

    return errors


def main() -> int:
    try:
        schema = load_json(SCHEMA_PATH)
        registry = load_json(REGISTRY_PATH)
    except ValidationFailure as exc:
        print(f"Diagnostikvalidierung fehlgeschlagen:\n- {exc}", file=sys.stderr)
        return 1

    errors = validate_schema(registry, schema)
    if not errors and isinstance(registry, dict):
        errors.extend(validate_invariants(registry))

    if errors:
        print("Diagnostikvalidierung fehlgeschlagen:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    count = len(registry["diagnostics"])
    print(f"Diagnostikvalidierung erfolgreich: {count} Diagnose(n)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
