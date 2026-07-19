#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
FUNCTION_DIR = ROOT / "data" / "functions"
OUTPUT_DIR = ROOT / "docs" / "generated" / "functions"

def render(data: dict) -> str:
    params = data["signature"].get("parameters", [])
    signature = f'{data["name"]}(' + ", ".join(p["name"] for p in params) + ")"

    lines = [
        f'# `{data["name"]}()`',
        "",
        f'**SDK-ID:** `{data["id"]}`  ',
        f'**Status:** `{data["status"]}`  ',
        f'**Kategorie:** `{data["category"]}`',
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

    lines.extend([
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

def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generated = 0

    for path in sorted(FUNCTION_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        target = OUTPUT_DIR / f"{path.stem}.md"
        target.write_text(render(data), encoding="utf-8")
        generated += 1

    print(f"Dokumentation erzeugt: {generated} Datei(en)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
