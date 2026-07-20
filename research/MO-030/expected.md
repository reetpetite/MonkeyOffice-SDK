# MO-030 – Erwartung vor Ausführung

## Fragestellung

Welche grundlegenden Formen einer `DIM`-Deklaration akzeptiert MonKey Office?

## Einordnung

- Klassifikation: `hypothesis`, soweit nicht anders angegeben
- Bezug: `Q-001`, Kandidat `SPEC-DECL-001`

## Erwartungen

| Fall | Erwartung | Grundlage |
|---|---|---|
| D01 | akzeptiert | `documented`: bisher dokumentierte Grundsyntax `DIM name AS type` |
| D02 | akzeptiert | `inferred`: zwei einzeln gültige Anweisungen sollten nacheinander zulässig sein |
| D03 | offen | `hypothesis`: gemeinsame Typangabe könnte unterstützt werden |
| D04 | offen | `hypothesis`: kommaseparierte vollständige Deklarationen könnten unterstützt werden |

Ein Parserfehler, eine Laufzeitmeldung und das Ausbleiben des Erfolgssignals sind getrennt zu protokollieren.
