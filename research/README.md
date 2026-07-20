# Forschungslabor

Jedes Experiment liegt in einem eigenen Verzeichnis:

```text
research/MO-xxx/
├── experiment.yaml
├── script.monkey
├── expected.md
├── observed-buildNNN.yaml
└── report-buildNNN.md
```

## Ablauf

1. Experiment in `experiment.yaml` definieren.
2. Testskript erzeugen:

```bash
python3 tools/generate_experiment.py MO-029
```

3. `script.monkey` in MonKey Office ausführen.
4. Den vollständigen Text aus der `msgBox` kopieren.
5. Ausgabe importieren:

```bash
python3 tools/import_results.py --build 249 --text 'MO-029|P01=[...]'
```

6. Bericht erzeugen:

```bash
python3 tools/generate_research_report.py MO-029 --build 249
```

## Wichtige Syntaxgrenze

Der komplette `msgBox()`-Ausdruck muss in MonKey Office auf genau einer Scriptzeile stehen. Der Generator berücksichtigt dies automatisch.

## Verbindliche Forschungsregeln

- [`experiment-protocol.md`](experiment-protocol.md) definiert Planung, Durchführung und Auswertung.
- [`open-questions.md`](open-questions.md) führt ungeklärte Sprachfragen mit dauerhaften IDs.
- [`expected-template.md`](expected-template.md) dient zur Vorab-Dokumentation der Erwartung.

Eine Beobachtung aus MonKey Office wird erst nach Konsolidierung in `evidence/` zu einer Grundlage für die normative Spezifikation.

## Syntax- und Statement-Matrizen

Fälle, die bereits beim Parsen scheitern können, werden nicht in ein gemeinsames Skript gepackt. Dafür dient `kind: script-matrix`:

```text
research/MO-NNN/
├── experiment.yaml
├── expected.md
└── cases/
    ├── D01-control.monkey
    └── D02-variant.monkey
```

Jede Datei wird einzeln ausgeführt. Das Erfolgssignal muss `MO-NNN|FALL-ID` enthalten. Sprint 27 stellt mit MO-030 bis MO-033 die erste Deklarationsmatrix bereit.
