# Entwicklungszyklen

## Sprint 3 – Number Library

### Ziel

Die bereits experimentell verifizierten Zahlenfunktionen in das strukturierte Datenmodell überführen.

### Enthalten

- NumToText
- TextToNumber
- FTextToNumber

### Definition of Done

- [x] jede bekannte Zahlenfunktion besitzt eine YAML-Datei
- [x] jede Aussage verweist auf Forschungs-IDs
- [x] getesteter Build ist dokumentiert
- [x] localeabhängige Risiken sind markiert
- [x] Beispiele und Qualitätsstatus sind vorhanden
- [x] ein manueller Regressionstest ist vorhanden
- [ ] Locale-Matrix vollständig getestet
- [ ] Präzision, Rundung und Grenzwerte vollständig untersucht

### Bewusste Grenzen

`NumToText()` ist grundsätzlich verifiziert, aber Formatierungsdetails und Grenzfälle sind noch nicht vollständig erforscht.
