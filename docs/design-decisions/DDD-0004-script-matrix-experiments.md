# DDD-0004 – Isolierte Script-Matrizen für Syntaxexperimente

- Status: angenommen
- Datum: 2026-07-20

## Kontext

Die bisherigen Forschungsexperimente berechnen mehrere Ausdrücke in einem einzigen Skript. Dieses Format eignet sich für Funktionswerte, aber nicht für Syntaxfragen: Ein einziger Parserfehler verhindert die Ausführung aller nachfolgenden Fälle und macht die Ursache mehrdeutig.

## Entscheidung

Syntax- und Statement-Experimente dürfen den Typ `script-matrix` verwenden. Jeder Fall besitzt eine eigene, unverändert versionierte `.monkey`-Datei. Die Fälle werden einzeln in MonKey Office ausgeführt. Ein Erfolgssignal enthält Experiment- und Fall-ID; Ablehnung, Fehlermeldung und Anwendungszustand werden je Fall protokolliert.

Die Experiment-ID bleibt unabhängig von späteren Spezifikations-IDs. `spec_candidates` bezeichnet nur mögliche Zielregeln und ist noch keine normative Zuordnung.

## Folgen

- Parserfehler eines Falls beeinflussen keine Kontrollfälle.
- Negative Syntaxergebnisse werden reproduzierbar.
- Die Zahl manueller Ausführungen steigt.
- Das Forschungsvalidierungswerkzeug muss sowohl Ausdrucksexperimente als auch Script-Matrizen prüfen.
