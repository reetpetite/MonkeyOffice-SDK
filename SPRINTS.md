# Entwicklungszyklen

## Sprint 1 – Infrastruktur

### Ziel

Eine reproduzierbare Build- und Qualitätssicherung für strukturierte Sprachdaten.

### Definition of Done

- [x] GitHub Actions führt den Build bei Push und Pull Request aus
- [x] SDK-IDs und Kategorien werden validiert
- [x] doppelte IDs und Funktionsnamen werden erkannt
- [x] Qualitätsfelder sind verpflichtend
- [x] Funktionsindex wird automatisch erzeugt
- [x] Kategorienübersicht wird automatisch erzeugt
- [x] Forschungsindex wird automatisch erzeugt
- [x] Statistik und Abdeckung werden automatisch erzeugt

### Bekannte Grenzen

- Forschungsdateien werden noch nicht auf physische Existenz geprüft
- interne Markdown-Links werden noch nicht separat validiert
- Testskripte werden noch nicht aus YAML erzeugt
