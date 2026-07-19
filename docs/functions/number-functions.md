# Zahlenfunktionen

## NumToText()
🧪 Experimentell verifiziert.

## TextToNumber()
- `TextToNumber("123,45")` → `123`
- `TextToNumber("-123,45")` → `-123`
- `TextToNumber("")` → `0`

💡 Für Geldbeträge ungeeignet.

## FTextToNumber()
- Gebietsschemaabhängig.
- `FTextToNumber("123,45")` → ca. `123,45`
- `FTextToNumber("123.45")` → `12345`
- `FTextToNumber("")` → `0`

⚠️ Englische Zahlenformate müssen vor der Konvertierung angepasst werden.
