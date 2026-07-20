#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry"
EXP_RE = re.compile(r"^MO-\d{3}$")
EVD_RE = re.compile(r"^EVD-\d{4}$")
SPEC_RE = re.compile(r"^SPEC-[A-Z]+-\d{3}$")
ALLOWED_CLASSIFICATIONS = {"documented", "verified", "inferred", "hypothesis"}


def load_yaml(path: Path, errors: list[str]):
    if not path.is_file():
        errors.append(f"{path}: Datei fehlt")
        return None
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"{path}: kann nicht gelesen werden: {exc}")
        return None


def safe_repo_path(value: str, owner: Path, errors: list[str]) -> Path | None:
    candidate = (ROOT / value).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        errors.append(f"{owner}: Pfad außerhalb des Repositorys: {value}")
        return None
    if not candidate.is_file():
        errors.append(f"{owner}: referenzierte Datei fehlt: {value}")
        return None
    return candidate


def main() -> int:
    errors: list[str] = []
    experiments_data = load_yaml(REGISTRY / "experiments.yaml", errors) or {}
    evidence_data = load_yaml(REGISTRY / "evidence.yaml", errors) or {}
    specification_data = load_yaml(REGISTRY / "specification.yaml", errors) or {}

    experiment_ids: set[str] = set()
    experiment_cases: dict[str, set[str]] = {}
    for entry in experiments_data.get("experiments", []):
        if not isinstance(entry, dict):
            errors.append("registry/experiments.yaml: Eintrag muss ein Mapping sein")
            continue
        item_id = str(entry.get("id", ""))
        if not EXP_RE.fullmatch(item_id):
            errors.append(f"registry/experiments.yaml: ungültige ID {item_id!r}")
        if item_id in experiment_ids:
            errors.append(f"registry/experiments.yaml: doppelte ID {item_id}")
        experiment_ids.add(item_id)
        path = safe_repo_path(str(entry.get("path", "")), REGISTRY / "experiments.yaml", errors)
        if path:
            payload = load_yaml(path, errors)
            if not isinstance(payload, dict) or payload.get("id") != item_id:
                errors.append(f"{path}: ID stimmt nicht mit Registry überein")
            else:
                rows = payload.get("cases") if payload.get("kind") == "script-matrix" else payload.get("tests")
                experiment_cases[item_id] = {
                    str(row.get("id")) for row in (rows or []) if isinstance(row, dict) and row.get("id")
                }

    evidence_ids: set[str] = set()
    for entry in evidence_data.get("evidence", []):
        if not isinstance(entry, dict):
            errors.append("registry/evidence.yaml: Eintrag muss ein Mapping sein")
            continue
        item_id = str(entry.get("id", ""))
        if not EVD_RE.fullmatch(item_id):
            errors.append(f"registry/evidence.yaml: ungültige ID {item_id!r}")
        if item_id in evidence_ids:
            errors.append(f"registry/evidence.yaml: doppelte ID {item_id}")
        evidence_ids.add(item_id)
        path = safe_repo_path(str(entry.get("path", "")), REGISTRY / "evidence.yaml", errors)
        if not path:
            continue
        payload = load_yaml(path, errors)
        if not isinstance(payload, dict):
            errors.append(f"{path}: Wurzel muss ein Mapping sein")
            continue
        if payload.get("id") != item_id:
            errors.append(f"{path}: ID stimmt nicht mit Registry überein")
        classification = payload.get("classification")
        if classification not in ALLOWED_CLASSIFICATIONS:
            errors.append(f"{path}: ungültige Evidenzklasse {classification!r}")
        if not str(payload.get("statement", "")).strip():
            errors.append(f"{path}: atomare Aussage fehlt")
        origin = payload.get("origin") or {}
        experiment_id = origin.get("experiment")
        if experiment_id not in experiment_ids:
            errors.append(f"{path}: unbekanntes Ursprungsexperiment {experiment_id!r}")
        known_cases = experiment_cases.get(str(experiment_id), set())
        for case_id in origin.get("cases", []):
            if str(case_id) not in known_cases:
                errors.append(f"{path}: unbekannter Fall {experiment_id}/{case_id}")
        for source in payload.get("source_files", []):
            safe_repo_path(str(source), path, errors)

    rule_ids: set[str] = set()
    for entry in specification_data.get("rules", []):
        if not isinstance(entry, dict):
            errors.append("registry/specification.yaml: Eintrag muss ein Mapping sein")
            continue
        item_id = str(entry.get("id", ""))
        if not SPEC_RE.fullmatch(item_id):
            errors.append(f"registry/specification.yaml: ungültige ID {item_id!r}")
        if item_id in rule_ids:
            errors.append(f"registry/specification.yaml: doppelte ID {item_id}")
        rule_ids.add(item_id)
        path = safe_repo_path(str(entry.get("path", "")), REGISTRY / "specification.yaml", errors)
        support = entry.get("supported_by", [])
        if not isinstance(support, list) or not support:
            errors.append(f"registry/specification.yaml: {item_id} ohne Evidenz")
        for evidence_id in support:
            if evidence_id not in evidence_ids:
                errors.append(f"registry/specification.yaml: {item_id} referenziert unbekannte Evidenz {evidence_id}")
        if path:
            text = path.read_text(encoding="utf-8")
            if item_id not in text:
                errors.append(f"{path}: Regel-ID {item_id} fehlt im Dokument")
            for evidence_id in support:
                if evidence_id not in text:
                    errors.append(f"{path}: Evidenzreferenz {evidence_id} fehlt im Dokument")

    if errors:
        print("Evidence-Graph-Validierung fehlgeschlagen:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Evidence-Graph-Validierung erfolgreich: "
        f"{len(experiment_ids)} Experiment(e), "
        f"{len(evidence_ids)} Evidenzsatz/-sätze, "
        f"{len(rule_ids)} Spezifikationsregel(n)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
