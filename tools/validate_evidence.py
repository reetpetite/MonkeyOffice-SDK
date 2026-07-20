#!/usr/bin/env python3
"""Validate the canonical evidence levels and cross-registry evidence links."""

from __future__ import annotations

import json
import sys
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
LEVELS_PATH = ROOT / "data" / "evidence-levels" / "registry.json"
SCHEMA_PATH = ROOT / "data" / "evidence-levels" / "schema.json"
EXPECTED_ORDER = ["documented", "verified", "inferred", "hypothesis"]
REGISTRIES = (
    (ROOT / "data" / "language-symbols" / "registry.json", "symbols"),
    (ROOT / "data" / "operators" / "registry.json", "operators"),
    (ROOT / "data" / "statements" / "registry.json", "statements"),
)


class ValidationFailure(Exception):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
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
        result += f"[{part}]" if isinstance(part, int) else f".{part}"
    return result


def validate_schema(instance: Any, schema: Any) -> list[str]:
    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    return [
        f"{json_path(list(error.absolute_path))}: {error.message}"
        for error in errors
    ]


def validate_level_registry(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    levels = registry.get("levels", [])
    ids = [entry.get("id") for entry in levels]
    ranks = [entry.get("rank") for entry in levels]

    if ids != EXPECTED_ORDER:
        errors.append(
            "Evidenzstufen müssen in kanonischer Reihenfolge stehen: "
            + ", ".join(EXPECTED_ORDER)
        )
    if ranks != list(range(len(EXPECTED_ORDER))):
        errors.append("Evidenzränge müssen fortlaufend 0, 1, 2, 3 sein")
    return errors


def validate_registry_links(
    path: Path, collection_name: str, allowed_levels: set[str]
) -> tuple[list[str], int]:
    errors: list[str] = []
    registry = load_json(path)
    entries = registry.get(collection_name, []) if isinstance(registry, dict) else []
    checked = 0

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or "status" not in entry:
            continue
        checked += 1
        try:
            display_path = path.relative_to(ROOT)
        except ValueError:
            display_path = path
        location = f"{display_path}:$.{collection_name}[{index}]"
        status = entry.get("status")
        if status not in allowed_levels:
            errors.append(f"{location}.status: unbekannte Evidenzstufe {status!r}")

        evidence = entry.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{location}.evidence: mindestens ein Verweis erforderlich")
            continue

        for evidence_index, reference in enumerate(evidence):
            if not isinstance(reference, str) or not reference:
                errors.append(
                    f"{location}.evidence[{evidence_index}]: ungültiger Verweis"
                )
                continue
            candidate = Path(reference)
            if candidate.is_absolute() or ".." in candidate.parts:
                errors.append(
                    f"{location}.evidence[{evidence_index}]: "
                    "nur repository-relative Pfade ohne '..' sind erlaubt"
                )
                continue
            if not (ROOT / candidate).is_file():
                errors.append(
                    f"{location}.evidence[{evidence_index}]: "
                    f"Datei fehlt: {reference}"
                )

    return errors, checked


def main() -> int:
    try:
        schema = load_json(SCHEMA_PATH)
        level_registry = load_json(LEVELS_PATH)
    except ValidationFailure as exc:
        print(f"Evidenzvalidierung fehlgeschlagen:\n- {exc}", file=sys.stderr)
        return 1

    errors = validate_schema(level_registry, schema)
    if not errors and isinstance(level_registry, dict):
        errors.extend(validate_level_registry(level_registry))

    allowed_levels = {
        entry.get("id")
        for entry in level_registry.get("levels", [])
        if isinstance(entry, dict) and isinstance(entry.get("id"), str)
    }
    checked = 0
    for path, collection_name in REGISTRIES:
        try:
            registry_errors, count = validate_registry_links(
                path, collection_name, allowed_levels
            )
        except ValidationFailure as exc:
            errors.append(str(exc))
            continue
        errors.extend(registry_errors)
        checked += count

    if errors:
        print("Evidenzvalidierung fehlgeschlagen:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Evidenzvalidierung erfolgreich: "
        f"{len(allowed_levels)} Stufe(n), {checked} Registry-Eintrag/Einträge"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
