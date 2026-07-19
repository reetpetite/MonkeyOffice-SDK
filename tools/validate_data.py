#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
FUNCTION_DIR = ROOT / "data" / "functions"
CATEGORY_FILE = ROOT / "data" / "categories.yaml"

REQUIRED = {
    "id", "name", "category", "status", "summary", "signature",
    "returns", "research", "verified_builds", "examples", "quality"
}
ALLOWED_STATUS = {
    "planned", "testing", "observed", "verified",
    "dangerous", "inconclusive", "hypothesis"
}
QUALITY_FIELDS = {
    "documentation", "experiments", "edge_cases",
    "regression", "confidence"
}
SDK_ID_PATTERN = re.compile(r"^MOF-[A-Z]{3}-\d{3}$")
RESEARCH_ID_PATTERN = re.compile(r"^MO-\d{3}$")

def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def main() -> int:
    errors = []
    warnings = []
    seen_ids = {}
    seen_names = {}

    categories_data = load_yaml(CATEGORY_FILE) or {}
    categories = {
        item["name"]: item["sdk_prefix"]
        for item in categories_data.get("categories", [])
    }

    paths = sorted(FUNCTION_DIR.glob("*.yaml"))
    if not paths:
        errors.append("Keine Funktionsdateien unter data/functions/ gefunden.")

    for path in paths:
        try:
            data = load_yaml(path)
        except Exception as exc:
            errors.append(f"{path}: YAML-Fehler: {exc}")
            continue

        if not isinstance(data, dict):
            errors.append(f"{path}: Wurzel muss ein Mapping sein")
            continue

        missing = REQUIRED - data.keys()
        if missing:
            errors.append(f"{path}: fehlende Felder: {', '.join(sorted(missing))}")

        status = data.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"{path}: ungültiger Status: {status!r}")

        sdk_id = data.get("id")
        if sdk_id:
            if not SDK_ID_PATTERN.fullmatch(str(sdk_id)):
                errors.append(f"{path}: ungültige SDK-ID: {sdk_id!r}")
            if sdk_id in seen_ids:
                errors.append(f"{path}: doppelte ID {sdk_id}; bereits in {seen_ids[sdk_id]}")
            seen_ids[sdk_id] = path

        name = data.get("name")
        if name:
            key = str(name).casefold()
            if key in seen_names:
                errors.append(f"{path}: doppelter Funktionsname {name}; bereits in {seen_names[key]}")
            seen_names[key] = path

        category = data.get("category")
        if category not in categories:
            errors.append(f"{path}: unbekannte Kategorie: {category!r}")
        elif sdk_id:
            expected_prefix = f"MOF-{categories[category]}-"
            if not str(sdk_id).startswith(expected_prefix):
                errors.append(
                    f"{path}: SDK-ID {sdk_id} passt nicht zur Kategorie {category} "
                    f"(erwarteter Präfix {expected_prefix})"
                )

        research = data.get("research", [])
        if not isinstance(research, list) or not research:
            errors.append(f"{path}: mindestens eine Forschungs-ID erforderlich")
        else:
            for research_id in research:
                if not RESEARCH_ID_PATTERN.fullmatch(str(research_id)):
                    errors.append(f"{path}: ungültige Forschungs-ID: {research_id!r}")

        examples = data.get("examples", [])
        if not isinstance(examples, list) or not examples:
            errors.append(f"{path}: mindestens ein Beispiel erforderlich")
        else:
            for index, example in enumerate(examples, start=1):
                if not isinstance(example, dict):
                    errors.append(f"{path}: Beispiel {index} muss ein Mapping sein")
                    continue
                for field in ("expression", "expected"):
                    if field not in example:
                        errors.append(f"{path}: Beispiel {index} ohne Feld {field!r}")

        builds = data.get("verified_builds", [])
        if status == "verified" and (not isinstance(builds, list) or not builds):
            errors.append(f"{path}: verifizierte Funktion ohne getesteten Build")

        quality = data.get("quality")
        if not isinstance(quality, dict):
            errors.append(f"{path}: quality muss ein Mapping sein")
        else:
            missing_quality = QUALITY_FIELDS - quality.keys()
            if missing_quality:
                errors.append(
                    f"{path}: fehlende Qualitätsfelder: "
                    f"{', '.join(sorted(missing_quality))}"
                )

        if status == "verified" and not data.get("warnings"):
            warnings.append(f"{path}: keine Warnungen dokumentiert")

    if warnings:
        print("Hinweise:")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("Validierung fehlgeschlagen:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validierung erfolgreich: {len(seen_ids)} Funktionsdatei(en)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
