#!/usr/bin/env python3
"""Validate the executable operator registry."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("Fehlende Abhängigkeit: jsonschema", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "data" / "operators" / "schema.json"
REGISTRY_PATH = ROOT / "data" / "operators" / "registry.json"
SYMBOLS_PATH = ROOT / "data" / "language-symbols" / "registry.json"


def load(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Datei fehlt: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"{path.relative_to(ROOT)}:{exc.lineno}:{exc.colno}: {exc.msg}"
        )


def json_path(parts: list[Any]) -> str:
    result = "$"
    for part in parts:
        result += f"[{part}]" if isinstance(part, int) else f".{part}"
    return result


def main() -> int:
    schema = load(SCHEMA_PATH)
    registry = load(REGISTRY_PATH)
    symbols = load(SYMBOLS_PATH)

    errors = sorted(
        Draft202012Validator(schema).iter_errors(registry),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    messages = [
        f"{json_path(list(error.absolute_path))}: {error.message}"
        for error in errors
    ]

    entries = registry.get("operators", []) if isinstance(registry, dict) else []
    symbol_entries = symbols.get("symbols", []) if isinstance(symbols, dict) else []
    operator_symbols = {
        entry.get("id")
        for entry in symbol_entries
        if entry.get("kind") == "operator"
    }

    ids = [entry.get("id") for entry in entries]
    refs = [entry.get("symbolId") for entry in entries]

    for value, count in sorted(Counter(ids).items()):
        if value is not None and count > 1:
            messages.append(f"doppelte Operator-ID: {value}")

    for value, count in sorted(Counter(refs).items()):
        if value is not None and count > 1:
            messages.append(f"doppelte Symbolreferenz: {value}")

    expected_order = sorted(ids)
    if ids != expected_order:
        messages.append("Operatoren müssen nach ID sortiert sein")

    by_symbol = {entry.get("symbolId"): entry for entry in entries}
    for index, entry in enumerate(entries):
        symbol_id = entry.get("symbolId")
        if symbol_id not in operator_symbols:
            messages.append(
                f"$.operators[{index}].symbolId: unbekanntes Operatorsymbol "
                f"{symbol_id!r}"
            )
        if entry.get("fixity") == "prefix" and entry.get("associativity") != "none":
            messages.append(
                f"$.operators[{index}].associativity: "
                "Präfixoperator muss 'none' verwenden"
            )
        if entry.get("fixity") == "infix" and entry.get("associativity") == "none":
            messages.append(
                f"$.operators[{index}].associativity: "
                "Infixoperator benötigt links- oder rechtsassoziative Bindung"
            )

    and_entry = by_symbol.get("op-and")
    or_entry = by_symbol.get("op-or")
    if and_entry and or_entry:
        if and_entry.get("precedence") != or_entry.get("precedence"):
            messages.append("AND und OR müssen dieselbe Präzedenz besitzen")
        if and_entry.get("evaluation") != "eager":
            messages.append("AND muss eager ausgewertet werden")
        if or_entry.get("evaluation") != "eager":
            messages.append("OR muss eager ausgewertet werden")

    power = by_symbol.get("op-power")
    if power and power.get("associativity") != "left":
        messages.append("Der Potenzoperator muss linksassoziativ sein")

    not_entry = by_symbol.get("op-not")
    if not_entry and not_entry.get("fixity") != "prefix":
        messages.append("NOT muss als Präfixoperator registriert sein")

    if messages:
        print("Operatorvalidierung fehlgeschlagen:", file=sys.stderr)
        for message in messages:
            print(f"- {message}", file=sys.stderr)
        return 1

    print(f"Operatorvalidierung erfolgreich: {len(entries)} Operator(en)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
