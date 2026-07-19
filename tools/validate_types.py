#!/usr/bin/env python3
"""Validate the machine-readable semantic type registry."""

from __future__ import annotations

import json
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
REGISTRY_PATH = ROOT / "data" / "types" / "registry.json"
SCHEMA_PATH = ROOT / "data" / "types" / "schema.json"

EXPECTED_ANALYSIS_TYPES = {"unknown", "error"}
CANONICAL_TYPE_ORDER = {
    "number": 0,
    "string": 1,
    "boolean": 2,
    "unknown": 3,
    "error": 4,
}
ALLOWED_LANGUAGE_STATUSES = {"verified", "inferred"}
ALLOWED_ANALYSIS_STATUSES = {"implementation"}


class ValidationFailure(Exception):
    """Raised when a registry file cannot be loaded."""


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
    types = registry.get("types", [])

    ids = [entry.get("id") for entry in types]
    duplicates = sorted(
        type_id
        for type_id, count in Counter(ids).items()
        if type_id is not None and count > 1
    )
    for type_id in duplicates:
        errors.append(f"doppelte Typ-ID: {type_id}")

    previous_id: str | None = None
    previous_sort_key: tuple[int, str] | None = None
    analysis_ids: set[str] = set()

    for index, entry in enumerate(types):
        location = f"$.types[{index}]"
        type_id = entry.get("id")
        kind = entry.get("kind")
        status = entry.get("status")
        runtime_model = entry.get("runtimeModel")

        if not isinstance(type_id, str):
            continue

        if kind == "language" and status not in ALLOWED_LANGUAGE_STATUSES:
            errors.append(
                f"{location}.status: Sprachtyp {type_id!r} darf nicht "
                f"Status {status!r} verwenden"
            )

        if kind == "analysis":
            analysis_ids.add(type_id)
            if status not in ALLOWED_ANALYSIS_STATUSES:
                errors.append(
                    f"{location}.status: Analysetyp {type_id!r} verlangt "
                    "Status 'implementation'"
                )
            if runtime_model is not None:
                errors.append(
                    f"{location}.runtimeModel: Analysetyp {type_id!r} "
                    "darf kein Runtime-Modell deklarieren"
                )

        sort_key = (
            CANONICAL_TYPE_ORDER.get(type_id, len(CANONICAL_TYPE_ORDER)),
            type_id,
        )
        if previous_sort_key is not None and sort_key < previous_sort_key:
            errors.append(
                "Typen sind nicht in kanonischer Reihenfolge sortiert: "
                f"{previous_id} vor {type_id}"
            )
        previous_id = type_id
        previous_sort_key = sort_key

    missing_analysis_types = sorted(EXPECTED_ANALYSIS_TYPES - analysis_ids)
    for type_id in missing_analysis_types:
        errors.append(f"erforderlicher Analysetyp fehlt: {type_id}")

    unexpected_analysis_types = sorted(analysis_ids - EXPECTED_ANALYSIS_TYPES)
    for type_id in unexpected_analysis_types:
        errors.append(
            f"nicht registrierter interner Analysetyp: {type_id}; "
            "EXPECTED_ANALYSIS_TYPES aktualisieren oder Typ entfernen"
        )

    return errors


def main() -> int:
    try:
        schema = load_json(SCHEMA_PATH)
        registry = load_json(REGISTRY_PATH)
    except ValidationFailure as exc:
        print(f"Typvalidierung fehlgeschlagen:\n- {exc}", file=sys.stderr)
        return 1

    errors = validate_schema(registry, schema)
    if not errors and isinstance(registry, dict):
        errors.extend(validate_invariants(registry))

    if errors:
        print("Typvalidierung fehlgeschlagen:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    count = len(registry["types"])
    print(f"Typvalidierung erfolgreich: {count} Typ(en)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
