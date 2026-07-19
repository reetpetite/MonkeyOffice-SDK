# Architektur

## Leitidee

Strukturierte Daten sind die primäre Wissensquelle. Dokumentation und Testartefakte werden daraus erzeugt.

```text
Experiment
    ↓
data/functions/*.yaml
    ├── docs/functions/*.md
    ├── generierte Testübersichten
    ├── JSON-Export
    └── spätere Entwicklerwerkzeuge
```

## Verzeichnisse

- `data/` – strukturierte Sprachdaten
- `research/` – Experimente und Rohbeobachtungen
- `tests/` – ausführbare MonKey-Office-Testskripte
- `docs/` – erzeugte und redaktionelle Dokumentation
- `tools/` – Generatoren und Prüfwerkzeuge
- `sdk/` – späterer Parser und Interpreter
- `examples/` – reale Importdefinitionen

## Single Source of Truth

Verifizierte Funktionseigenschaften werden in `data/functions/*.yaml` gepflegt. Dateien unter `docs/generated/` werden ausschließlich durch `tools/build.py` erzeugt.
