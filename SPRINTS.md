# Entwicklungszyklen

## Sprint 2 – String Library

### Ziel

Die bereits experimentell verifizierten Stringfunktionen in das strukturierte Datenmodell überführen.

### Enthalten

- Replace
- ReplaceAll
- Middle
- Position
- PatternCount
- StrComp
- Length
- Left
- Right
- Trim
- LTrim
- RTrim
- Lower
- Upper
- Proper
- CountFields
- NthField

### Definition of Done

- [x] jede bekannte Stringfunktion besitzt eine YAML-Datei
- [x] jede Aussage verweist auf Forschungs-IDs
- [x] getesteter Build ist dokumentiert
- [x] bekannte Gefahren sind markiert
- [x] Beispiele und Qualitätsstatus sind vorhanden
- [ ] Regressionstests vollständig aus YAML generiert
- [ ] Unicode- und Extremwerttests abgeschlossen

### Bewusste Grenzen

Einige einfache Funktionen sind zwar verifiziert, aber ihre Randfälle sind noch nicht vollständig erforscht. Sie erhalten deshalb bei `quality.edge_cases` den Wert `partial`.
