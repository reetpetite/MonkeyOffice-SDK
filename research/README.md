# Forschungslabor

Jedes Experiment liegt in einem eigenen Verzeichnis:

```text
research/MO-xxx/
├── experiment.yaml
├── script.monkey
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
