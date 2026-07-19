# Testplan: Zahlenkonvertierung

Dieser Plan enthält offene Prüfungen und keine bereits verifizierten Spracheigenschaften.

## NumToText()

- negative Werte
- Nachkommastellen
- sehr große Zahlen
- Rundung
- wissenschaftliche Schreibweise
- Tausendertrennzeichen
- localeabhängige Ausgabe

## TextToNumber()

- führende und nachgestellte Leerzeichen
- Pluszeichen
- führende Nullen
- Buchstaben vor und nach der Zahl
- mehrere Minuszeichen
- Punkt als Dezimal- oder Tausendertrennzeichen
- sehr große Zahlen
- Überlauf und Fehlerverhalten

## FTextToNumber()

- deutsche und andere Locale-Einstellungen
- Leerzeichen als Gruppentrenner
- mehrere Tausendertrennzeichen
- gemischte Punkt-/Komma-Formate
- Währungssymbole
- Vorzeichen
- Rundung und Präzision
- ungültige Eingaben
