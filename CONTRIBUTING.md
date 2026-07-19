# Mitwirken am MonkeyOffice SDK

## Grundsätze

1. Jede neue Erkenntnis beginnt mit einem dokumentierten Experiment.
2. Forschungs-IDs werden niemals umnummeriert oder wiederverwendet.
3. Verifizierte Aussagen verweisen auf mindestens eine Forschungs-ID.
4. Gefährliche Tests werden ausdrücklich gekennzeichnet und nicht automatisiert ausgeführt.
5. Generierte Dokumentation wird nicht direkt bearbeitet.
6. Änderungen am Datenmodell müssen durch die Validierung laufen.

## Arbeitsablauf

1. Experiment unter `research/experiments/` anlegen.
2. Test in MonKey Office ausführen.
3. Rohresultate unverändert dokumentieren.
4. Eintrag unter `data/functions/` ergänzen oder aktualisieren.
5. `python3 tools/build.py` ausführen.
6. Änderungen mit `git diff` kontrollieren.
7. Commit mit beschreibender Nachricht erstellen.

## Statuswerte

- `planned`
- `testing`
- `verified`
- `dangerous`
- `inconclusive`

## Konventionen

- Funktionsdateien: Kleinbuchstaben und Bindestriche, z. B. `replace-all.yaml`
- Forschungsdateien: `MO-023.md`
- SDK-IDs: `MOF-<Kategorie>-<Nummer>`, z. B. `MOF-STR-001`
