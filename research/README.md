# Forschungsprotokoll

Dieses Verzeichnis enthält die experimentelle Untersuchung der Skriptsprache von MonKey Office.

Ziel ist eine nachvollziehbare und reproduzierbare Sprachreferenz. Aussagen in der eigentlichen Dokumentation sollen auf dokumentierte Tests zurückgeführt werden können.

## Kennzeichnungen

- 📖 offiziell dokumentiert
- 🧪 experimentell verifiziert
- 💡 praktische Empfehlung
- ⚠️ gefährliches Verhalten oder bekannter Fehler
- ❓ noch nicht abschließend untersucht

## Testumgebung

- Anwendung: MonKey Office 2025
- Build: 249
- Betriebssystem: macOS
- Testzeitraum: 2026
- Region und Zahlenformat: deutschsprachige Umgebung mit Komma als Dezimaltrennzeichen

Die genaue Systemregion sollte bei Tests gebietsschemaabhängiger Funktionen zusätzlich festgehalten werden.

## Forschungsindex

| ID | Funktion oder Thema | Status | Zentrale Erkenntnis |
|---|---|---:|---|
| MO-001 | `Middle()` | 🧪 | Positionen sind 1-basiert; Position 0 verhält sich abweichend |
| MO-002 | `Replace()` | 🧪 | Ersetzt nur den ersten Treffer |
| MO-003 | `ReplaceAll()` | 🧪 | Ersetzt alle nicht überlappenden Treffer |
| MO-004 | `NumToText()` | 🧪 | Funktion existiert unter diesem Namen |
| MO-005 | `Position()` | 🧪 | Vier Parameter; case-insensitiv; 1-basiert |
| MO-006 | `PatternCount()` | 🧪 | Zählt überlappende Treffer |
| MO-007 | `StrComp()` | 🧪 | Case-sensitiver Drei-Wege-Vergleich |
| MO-008 | `Length()` | 🧪 | Zählt alle Zeichen einschließlich Leerzeichen |
| MO-009 | `Left()` | 🧪 | Begrenzung über die Textlänge hinaus ist zulässig |
| MO-010 | `Right()` | 🧪 | Verhalten analog zu `Left()` |
| MO-011 | `Trim()`, `LTrim()`, `RTrim()` | 🧪 | Entfernen äußere Leerzeichen |
| MO-012 | `Lower()`, `Upper()` | 🧪 | Verarbeiten deutsche Umlaute |
| MO-013 | `Proper()` | 🧪 | Wortanfang groß, restliche Buchstaben klein |
| MO-014 | `CountFields()` | 🧪 | Nicht überlappende, case-insensitive Trennung |
| MO-015 | `NthField()` | 🧪 | 1-basierte Feldauswahl; leere Felder bleiben erhalten |
| MO-018 | `Position()` – Randfälle | 🧪 | Überlappende Treffer werden berücksichtigt |
| MO-022 | `PatternCount()` – leerer Suchtext | ⚠️ | Leerer Suchtext kann MonKey Office aufhängen |
| MO-023 | `Replace()` – Randfälle | 🧪 | Leerer Suchtext lässt den Ausgangstext unverändert |
| MO-024 | `ReplaceAll()` – Randfälle | 🧪 | Leerer Suchtext lässt den Ausgangstext unverändert |
| MO-025 | `TextToNumber()` | 🧪 | Liest den ganzzahligen Anfang eines Textes |
| MO-026 | `FTextToNumber()` | 🧪 | Gebietsschemaabhängige Zahlenkonvertierung |

## Noch nicht vergebene IDs

Die Lücken in der Nummerierung bleiben zunächst bestehen. Forschungs-IDs werden nicht nachträglich verschoben, da sie als dauerhafte Referenzen dienen sollen.

## Aufbau einer Experimentdatei

Jede Untersuchung sollte nach Möglichkeit folgende Abschnitte enthalten:

1. Fragestellung
2. Testumgebung
3. Testcode
4. Rohresultate
5. Interpretation
6. Verifizierte Aussagen
7. Gefahren und Empfehlungen
8. Offene Fragen
9. Status

## Grundsatz

Eine einzelne Beobachtung wird nur dann als allgemeines Sprachverhalten dokumentiert, wenn der Test eindeutig ist. Gebietsschema-, Versions- oder datentypabhängige Ergebnisse werden entsprechend eingeschränkt beschrieben.