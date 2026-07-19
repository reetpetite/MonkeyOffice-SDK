#!/usr/bin/env python3
from collections import defaultdict
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
FUNCTION_DIR = ROOT / "data" / "functions"
OUTPUT_ROOT = ROOT / "docs" / "generated"
FUNCTION_OUTPUT = OUTPUT_ROOT / "functions"
COVERAGE_FILE = ROOT / "data" / "coverage.yaml"

STATUS_ICON = {
    "verified": "✅",
    "observed": "👁️",
    "testing": "🧪",
    "dangerous": "⚠️",
    "hypothesis": "💭",
    "planned": "📝",
    "inconclusive": "❓",
}

def load_functions():
    items = []
    for path in sorted(FUNCTION_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["_slug"] = path.stem
        items.append(data)
    return items

def build_list(data):
    builds = data.get("verified_builds", [])
    return ", ".join(str(item.get("build", "?")) for item in builds) or "–"

def render_function(data: dict) -> str:
    params = data["signature"].get("parameters", [])
    signature = f'{data["name"]}(' + ", ".join(p["name"] for p in params) + ")"
    icon = STATUS_ICON.get(data["status"], "")

    lines = [
        f'# `{data["name"]}()`',
        "",
        f'**SDK-ID:** `{data["id"]}`  ',
        f'**Status:** {icon} `{data["status"]}`  ',
        f'**Kategorie:** `{data["category"]}`  ',
        f'**Getestete Builds:** {build_list(data)}',
        "",
        data.get("summary", ""),
        "",
        "## Signatur",
        "",
        "```monkeyoffice",
        signature,
        "```",
        "",
        f'**Rückgabewert:** `{data["returns"]}`',
        "",
        "## Beispiele",
        "",
    ]
    for example in data.get("examples", []):
        lines.extend([
            "```monkeyoffice",
            example["expression"],
            "```",
            "",
            f'Ergebnis: `{example["expected"]}`',
            "",
        ])

    lines.extend(["## Qualitätsstatus", ""])
    for key, value in data.get("quality", {}).items():
        lines.append(f"- **{key}:** `{value}`")

    lines.extend([
        "",
        "## Forschungsgrundlage",
        "",
        ", ".join(f'`{item}`' for item in data.get("research", [])),
        "",
    ])

    if data.get("warnings"):
        lines.extend(["## Warnungen", ""])
        lines.extend(f'- ⚠️ {item}' for item in data["warnings"])
        lines.append("")

    if data.get("recommendations"):
        lines.extend(["## Empfehlungen", ""])
        lines.extend(f'- 💡 {item}' for item in data["recommendations"])
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"

def write_index(functions):
    lines = [
        "# Funktionsindex",
        "",
        "| Funktion | Kategorie | Status | Build |",
        "|---|---|---|---|",
    ]
    for data in sorted(functions, key=lambda item: item["name"].casefold()):
        icon = STATUS_ICON.get(data["status"], "")
        lines.append(
            f'| [`{data["name"]}()`](functions/{data["_slug"]}.md) '
            f'| {data["category"]} | {icon} {data["status"]} | {build_list(data)} |'
        )
    (OUTPUT_ROOT / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def write_categories(functions):
    grouped = defaultdict(list)
    for data in functions:
        grouped[data["category"]].append(data)

    lines = ["# Kategorien", ""]
    for category in sorted(grouped):
        lines.extend([f"## {category}", ""])
        for data in sorted(grouped[category], key=lambda item: item["name"].casefold()):
            lines.append(f'- [`{data["name"]}()`](functions/{data["_slug"]}.md)')
        lines.append("")
    (OUTPUT_ROOT / "categories.md").write_text("\n".join(lines), encoding="utf-8")

def write_research_index(functions):
    mapping = defaultdict(list)
    for data in functions:
        for research_id in data.get("research", []):
            mapping[research_id].append(data)

    lines = [
        "# Forschungsindex",
        "",
        "| Experiment | Funktionen |",
        "|---|---|",
    ]
    for research_id in sorted(mapping):
        links = ", ".join(
            f'[`{item["name"]}()`](functions/{item["_slug"]}.md)'
            for item in sorted(mapping[research_id], key=lambda entry: entry["name"])
        )
        lines.append(f"| `{research_id}` | {links} |")
    (OUTPUT_ROOT / "research-index.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

def write_statistics(functions):
    statuses = defaultdict(int)
    categories = defaultdict(int)
    builds = set()

    for data in functions:
        statuses[data["status"]] += 1
        categories[data["category"]] += 1
        for build in data.get("verified_builds", []):
            builds.add(str(build.get("build")))

    coverage = {}
    if COVERAGE_FILE.exists():
        coverage = yaml.safe_load(COVERAGE_FILE.read_text(encoding="utf-8")) or {}

    lines = [
        "# Statistik",
        "",
        f"**Funktionen insgesamt:** {len(functions)}  ",
        f"**Erfasste Builds:** {', '.join(sorted(builds)) or '–'}",
        "",
        "## Status",
        "",
        "| Status | Anzahl |",
        "|---|---:|",
    ]
    for status in sorted(statuses):
        lines.append(f"| {STATUS_ICON.get(status, '')} {status} | {statuses[status]} |")

    lines.extend([
        "",
        "## Kategorien und Abdeckung",
        "",
        "| Kategorie | Erfasst | Bekannter Gesamtumfang | Abdeckung |",
        "|---|---:|---:|---:|",
    ])

    declared = coverage.get("categories", {})
    all_categories = sorted(set(categories) | set(declared))
    for category in all_categories:
        present = categories.get(category, 0)
        total = declared.get(category, {}).get("known_total")
        if total:
            percent = f"{present / total * 100:.1f} %"
            total_text = str(total)
        else:
            percent = "–"
            total_text = "unbekannt"
        lines.append(f"| {category} | {present} | {total_text} | {percent} |")

    (OUTPUT_ROOT / "statistics.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

def main() -> int:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    FUNCTION_OUTPUT.mkdir(parents=True, exist_ok=True)
    functions = load_functions()

    for data in functions:
        target = FUNCTION_OUTPUT / f'{data["_slug"]}.md'
        target.write_text(render_function(data), encoding="utf-8")

    write_index(functions)
    write_categories(functions)
    write_research_index(functions)
    write_statistics(functions)

    print(f"Dokumentation erzeugt: {len(functions)} Funktionsdatei(en) plus Indizes")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
