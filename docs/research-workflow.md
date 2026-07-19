# Forschungsworkflow

## Statusstufen

- `planned`: definiert, aber noch nicht ausgeführt
- `running`: teilweise ausgeführt
- `completed`: vollständig beobachtet
- `dangerous`: enthält blockierende oder potenziell schädliche Tests
- `inconclusive`: Ergebnisse erlauben noch keine belastbare Aussage

## Rohdaten vor Interpretation

Die kopierte `msgBox`-Ausgabe wird unverändert im Feld `raw` gespeichert. Die geparsten Werte unter `results` sind eine maschinenlesbare Ableitung dieser Rohdaten.

## Buildvergleich

```bash
python3 tools/compare_builds.py MO-029 249 301
```

Der Prozess liefert Exit-Code `1`, sobald mindestens ein Ergebnis abweicht. Dadurch kann er später auch in CI verwendet werden.
