#!/usr/bin/env python3
"""Validate JSON output produced by the reference parsers."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("Fehlende Abhängigkeit: jsonschema", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "data" / "ast" / "schema.json"


def load_json(path: Path | None) -> Any:
    try:
        if path is None:
            return json.load(sys.stdin)
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Datei fehlt: {path}")
    except json.JSONDecodeError as exc:
        location = str(path) if path else "stdin"
        raise SystemExit(
            f"{location}:{exc.lineno}:{exc.colno}: {exc.msg}"
        )


def json_path(parts: list[Any]) -> str:
    result = "$"
    for part in parts:
        result += f"[{part}]" if isinstance(part, int) else f".{part}"
    return result


def check_spans(node: Any, path: str = "$") -> list[str]:
    messages: list[str] = []
    if isinstance(node, dict):
        start = node.get("start")
        end = node.get("end")
        if isinstance(start, int) and isinstance(end, int) and end < start:
            messages.append(f"{path}: end ({end}) liegt vor start ({start})")
        for key, value in node.items():
            messages.extend(check_spans(value, f"{path}.{key}"))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            messages.extend(check_spans(value, f"{path}[{index}]"))
    return messages


def validate(document: Any) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    messages = [
        f"{json_path(list(error.absolute_path))}: {error.message}"
        for error in errors
    ]
    messages.extend(check_spans(document))
    return messages


def parse_args(argv: list[str]) -> argparse.Namespace:
    cli = argparse.ArgumentParser(
        description="Validiert einen JSON-AST der Referenzparser."
    )
    cli.add_argument("path", nargs="?", help="JSON-Datei; sonst stdin")
    return cli.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    document = load_json(Path(args.path) if args.path else None)
    messages = validate(document)

    if messages:
        print("AST-Validierung fehlgeschlagen:", file=sys.stderr)
        for message in messages:
            print(f"- {message}", file=sys.stderr)
        return 1

    print("AST-Validierung erfolgreich")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
