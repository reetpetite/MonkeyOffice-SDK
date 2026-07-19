# Testplan: String-Randfälle

Dieser Plan enthält noch offene Prüfungen und ist keine Dokumentation verifizierter Spracheigenschaften.

## Gemeinsame Testgruppen

- leerer String
- ein Zeichen
- Suchtext länger als Quelltext
- Treffer am Anfang und Ende
- Umlaute und ß
- kombinierende Unicode-Zeichen
- Emoji und Zeichen außerhalb der BMP
- Tabulatoren
- CR, LF und CRLF
- sehr lange Eingaben
- negative und übergroße Längen
- Position 0 und negative Positionen

## Priorität

1. Middle, Left, Right
2. Trim, LTrim, RTrim
3. Lower, Upper, Proper
4. StrComp
5. CountFields und NthField
