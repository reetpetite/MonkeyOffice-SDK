# MO-032 – Erwartung vor Ausführung

## Fragestellung

Welche Initialisierungsformen akzeptiert MonKey Office, und liefert die getrennte `SET`-Zuweisung den erwarteten Wert?

## Einordnung

- I01: `documented` gemäß der bisher erfassten Syntax `DIM name AS type [= value]`
- I02: `hypothesis`
- I03: `documented` für `DIM` und `SET variable TO expression`

## Erwartungen

| Fall | Erwartung |
|---|---|
| I01 | akzeptiert; Ausgabe enthält `[5]` |
| I02 | offen; prüft mögliche Typinferenz |
| I03 | akzeptiert; Ausgabe enthält `[5]` |

Die Darstellung der Zahl ist exakt zu übernehmen; insbesondere dürfen Dezimaltrennzeichen oder zusätzliche Nachkommastellen nicht normalisiert werden.
