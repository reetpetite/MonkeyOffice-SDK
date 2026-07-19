#!/usr/bin/env python3
"""Validate MonKey Office conformance-test files.

The validator checks every JSON file below tests/conformance, excluding the
schema itself, against tests/conformance/schema.json. It also performs a small
set of repository-specific consistency checks that are awkward to express in
JSON Schema alone.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError
except ImportError as exc:  # pragma: no cover - environment failure
    raise SystemExit(
        "Fehlende Abhängigkeit: jsonschema\n"
        "Bitte zuerst die Projektabhängigkeiten installieren:\n"
        "  python -m pip install -r requirements.txt"
    ) from exc


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFORMANCE_ROOT = REPOSITORY_ROOT / "tests" / "conformance"
DEFAULT_SCHEMA = DEFAULT_CONFORMANCE_ROOT / "schema.json"


@dataclass(frozen=True)
class ValidationIssue:
    """One validation problem tied to a source file."""

    path: Path
    message: str

    def format(self, root: Path) -> str:
        try:
            display_path = self.path.relative_to(root)
        except ValueError:
            display_path = self.path
        return f"- {display_path}: {self.message}"


def load_json(path: Path) -> Any:
    """Load one UTF-8 JSON document."""

    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def iter_test_files(root: Path, schema_path: Path) -> Iterable[Path]:
    """Yield conformance JSON files in deterministic order."""

    resolved_schema = schema_path.resolve()
    for path in sorted(root.rglob("*.json")):
        if path.resolve() != resolved_schema:
            yield path


def format_json_path(parts: Iterable[Any]) -> str:
    """Format a jsonschema path in a readable dotted/indexed form."""

    result = "$"
    for part in parts:
        if isinstance(part, int):
            result += f"[{part}]"
        else:
            result += f".{part}"
    return result


def validate_schema(schema: Any, schema_path: Path) -> list[ValidationIssue]:
    """Check that the schema itself is a valid Draft 2020-12 schema."""

    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        return [
            ValidationIssue(
                schema_path,
                f"ungültiges JSON-Schema: {exc.message}",
            )
        ]
    return []


def validate_against_schema(
    document: Any,
    path: Path,
    validator: Draft202012Validator,
) -> list[ValidationIssue]:
    """Return all schema violations for one document."""

    issues: list[ValidationIssue] = []
    errors = sorted(
        validator.iter_errors(document),
        key=lambda error: (list(error.absolute_path), error.message),
    )

    for error in errors:
        location = format_json_path(error.absolute_path)
        issues.append(
            ValidationIssue(path, f"{location}: {error.message}")
        )

    return issues


def validate_repository_rules(
    document: Any,
    path: Path,
    repository_root: Path,
) -> list[ValidationIssue]:
    """Apply cross-file and semantic consistency checks."""

    issues: list[ValidationIssue] = []

    if not isinstance(document, dict):
        return issues

    evidence = document.get("evidence")
    if isinstance(evidence, dict):
        documents = evidence.get("documents", [])
        if isinstance(documents, list):
            for referenced in documents:
                if not isinstance(referenced, str):
                    continue
                target = repository_root / referenced
                if not target.is_file():
                    issues.append(
                        ValidationIssue(
                            path,
                            f"referenziertes Evidenzdokument fehlt: {referenced}",
                        )
                    )

        status = document.get("status")
        level = evidence.get("level")
        if status == "verified" and level in {"inferred", "hypothesis"}:
            issues.append(
                ValidationIssue(
                    path,
                    "Status 'verified' erfordert Evidenzlevel "
                    "'documented' oder 'verified'",
                )
            )

    expectation = document.get("expectation")
    if isinstance(expectation, dict):
        runtime = expectation.get("runtime")
        if isinstance(runtime, dict):
            outcome = runtime.get("outcome")
            if outcome == "value" and "errorCode" in runtime:
                issues.append(
                    ValidationIssue(
                        path,
                        "Runtime-Erwartung mit outcome 'value' darf "
                        "kein errorCode enthalten",
                    )
                )
            if outcome == "error" and "value" in runtime:
                issues.append(
                    ValidationIssue(
                        path,
                        "Runtime-Erwartung mit outcome 'error' darf "
                        "keinen value enthalten",
                    )
                )

        ast = expectation.get("ast")
        if isinstance(ast, dict):
            fixture = ast.get("fixture")
            if isinstance(fixture, str):
                target = path.parent / fixture
                if not target.is_file():
                    issues.append(
                        ValidationIssue(
                            path,
                            f"referenzierte AST-Fixture fehlt: {fixture}",
                        )
                    )

    return issues


def validate_file(
    path: Path,
    validator: Draft202012Validator,
    repository_root: Path,
) -> list[ValidationIssue]:
    """Load and validate one conformance-test file."""

    try:
        document = load_json(path)
    except json.JSONDecodeError as exc:
        return [
            ValidationIssue(
                path,
                f"ungültiges JSON in Zeile {exc.lineno}, "
                f"Spalte {exc.colno}: {exc.msg}",
            )
        ]
    except OSError as exc:
        return [ValidationIssue(path, f"Datei konnte nicht gelesen werden: {exc}")]

    issues = validate_against_schema(document, path, validator)
    if not issues:
        issues.extend(
            validate_repository_rules(document, path, repository_root)
        )
    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Conformance-Testdateien gegen das Projektschema validieren."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_CONFORMANCE_ROOT,
        help="Wurzelverzeichnis der Conformance-Tests",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA,
        help="Pfad zum JSON-Schema",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    schema_path = args.schema.resolve()

    if not root.is_dir():
        print(f"Fehler: Conformance-Verzeichnis fehlt: {root}", file=sys.stderr)
        return 2

    if not schema_path.is_file():
        print(f"Fehler: Schema fehlt: {schema_path}", file=sys.stderr)
        return 2

    try:
        schema = load_json(schema_path)
    except json.JSONDecodeError as exc:
        print(
            f"Fehler: ungültiges Schema-JSON in Zeile {exc.lineno}, "
            f"Spalte {exc.colno}: {exc.msg}",
            file=sys.stderr,
        )
        return 2
    except OSError as exc:
        print(f"Fehler: Schema konnte nicht gelesen werden: {exc}", file=sys.stderr)
        return 2

    schema_issues = validate_schema(schema, schema_path)
    if schema_issues:
        print("Conformance-Schema ungültig:", file=sys.stderr)
        for issue in schema_issues:
            print(issue.format(REPOSITORY_ROOT), file=sys.stderr)
        return 1

    validator = Draft202012Validator(schema)
    test_files = list(iter_test_files(root, schema_path))

    if not test_files:
        print("Hinweis: keine Conformance-Testdateien gefunden.")
        return 0

    issues: list[ValidationIssue] = []
    for path in test_files:
        issues.extend(validate_file(path, validator, REPOSITORY_ROOT))

    if issues:
        print(
            f"Conformance-Validierung fehlgeschlagen: "
            f"{len(issues)} Problem(e) in {len(test_files)} Datei(en)",
            file=sys.stderr,
        )
        for issue in issues:
            print(issue.format(REPOSITORY_ROOT), file=sys.stderr)
        return 1

    print(
        f"Conformance-Validierung erfolgreich: "
        f"{len(test_files)} Testdatei(en)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
