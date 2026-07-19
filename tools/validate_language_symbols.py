#!/usr/bin/env python3
"""Validate the machine-readable language symbol registry."""

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
REGISTRY_PATH = ROOT / "data" / "language-symbols" / "registry.json"
SCHEMA_PATH = ROOT / "data" / "language-symbols" / "schema.json"

KIND_ORDER = {"keyword": 0, "operator": 1}


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
    symbols = registry.get("symbols", [])

    ids = [entry.get("id") for entry in symbols]
    for symbol_id, count in sorted(Counter(ids).items()):
        if symbol_id is not None and count > 1:
            errors.append(f"doppelte Symbol-ID: {symbol_id}")

    canonical_spellings = [entry.get("canonicalSpelling") for entry in symbols]
    for spelling, count in sorted(Counter(canonical_spellings).items()):
        if spelling is not None and count > 1:
            errors.append(f"doppelte kanonische Schreibweise: {spelling}")

    previous_key: tuple[int, str] | None = None
    by_id: dict[str, dict[str, Any]] = {}

    for index, entry in enumerate(symbols):
        location = f"$.symbols[{index}]"
        symbol_id = entry.get("id")
        kind = entry.get("kind")
        spelling = entry.get("spelling")
        canonical = entry.get("canonicalSpelling")

        if isinstance(symbol_id, str):
            by_id[symbol_id] = entry

        if kind in KIND_ORDER and isinstance(symbol_id, str):
            key = (KIND_ORDER[kind], symbol_id)
            if previous_key is not None and key < previous_key:
                errors.append(
                    "Symbole sind nicht deterministisch nach Art und ID sortiert: "
                    f"{previous_key[1]} vor {symbol_id}"
                )
            previous_key = key

        if isinstance(spelling, str) and isinstance(canonical, str):
            if entry.get("caseInsensitive") and canonical != spelling.upper():
                errors.append(
                    f"{location}.canonicalSpelling: erwartet {spelling.upper()!r}"
                )
            if not entry.get("caseInsensitive") and canonical != spelling:
                errors.append(
                    f"{location}.canonicalSpelling: muss der Schreibweise entsprechen"
                )

        if kind == "keyword":
            for forbidden in ("arity", "precedenceGroup", "associativity"):
                if forbidden in entry:
                    errors.append(
                        f"{location}.{forbidden}: Schlüsselwort darf "
                        f"{forbidden!r} nicht deklarieren"
                    )

        if kind == "operator":
            for required in ("arity", "precedenceGroup", "associativity"):
                if required not in entry:
                    errors.append(
                        f"{location}.{required}: Operator benötigt {required!r}"
                    )

    and_entry = by_id.get("op-and")
    or_entry = by_id.get("op-or")
    if and_entry and or_entry:
        if and_entry.get("precedenceGroup") != or_entry.get("precedenceGroup"):
            errors.append("AND und OR müssen dieselbe Präzedenzgruppe verwenden")
        if and_entry.get("evaluation") != "eager":
            errors.append("AND muss als eager/nicht-kurzschließend registriert sein")
        if or_entry.get("evaluation") != "eager":
            errors.append("OR muss als eager/nicht-kurzschließend registriert sein")

    power = by_id.get("op-power")
    if power and power.get("associativity") != "left":
        errors.append("Der Potenzoperator muss linksassoziativ registriert sein")

    not_entry = by_id.get("op-not")
    if not_entry and not_entry.get("precedenceGroup") != "logical-wide-not":
        errors.append("NOT muss die Präzedenzgruppe 'logical-wide-not' verwenden")

    return errors


def main() -> int:
    try:
        schema = load_json(SCHEMA_PATH)
        registry = load_json(REGISTRY_PATH)
    except ValidationFailure as exc:
        print(f"Symbolvalidierung fehlgeschlagen:\n- {exc}", file=sys.stderr)
        return 1

    errors = validate_schema(registry, schema)
    if not errors and isinstance(registry, dict):
        errors.extend(validate_invariants(registry))

    if errors:
        print("Symbolvalidierung fehlgeschlagen:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Symbolvalidierung erfolgreich: "
        f"{len(registry['symbols'])} Symbol(e)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
