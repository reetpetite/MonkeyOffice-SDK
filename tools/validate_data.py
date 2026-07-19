#!/usr/bin/env python3
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
FUNCTION_DIR = ROOT / "data" / "functions"

REQUIRED = {
    "id", "name", "category", "status", "signature",
    "returns", "research", "examples"
}
ALLOWED_STATUS = {
    "planned", "testing", "verified", "dangerous", "inconclusive"
}

def main() -> int:
    errors = []
    seen_ids = {}

    for path in sorted(FUNCTION_DIR.glob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
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
            if sdk_id in seen_ids:
                errors.append(f"{path}: doppelte ID {sdk_id}; bereits in {seen_ids[sdk_id]}")
            seen_ids[sdk_id] = path

        research = data.get("research", [])
        if not isinstance(research, list) or not research:
            errors.append(f"{path}: mindestens eine Forschungs-ID erforderlich")

        examples = data.get("examples", [])
        if not isinstance(examples, list) or not examples:
            errors.append(f"{path}: mindestens ein Beispiel erforderlich")

    if errors:
        print("Validierung fehlgeschlagen:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validierung erfolgreich: {len(seen_ids)} Funktionsdatei(en)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
