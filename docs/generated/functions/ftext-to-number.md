# `FTextToNumber()`

**SDK-ID:** `MOF-NUM-003`  
**Status:** ✅ `verified`  
**Kategorie:** `Number`  
**Getestete Builds:** 249

Liest eine localeabhängig formatierte Zahl aus einem Text.

## Signatur

```monkeyoffice
FTextToNumber(text)
```

**Rückgabewert:** `number`

## Beispiele

```monkeyoffice
FTextToNumber("123")
```

Ergebnis: `123`

```monkeyoffice
FTextToNumber("123,45")
```

Ergebnis: `123.45`

```monkeyoffice
FTextToNumber("123.45")
```

Ergebnis: `12345`

```monkeyoffice
FTextToNumber("")
```

Ergebnis: `0`

## Qualitätsstatus

- **documentation:** `complete`
- **experiments:** `complete`
- **edge_cases:** `complete`
- **regression:** `partial`
- **confidence:** `high`

## Forschungsgrundlage

`MO-026`

## Warnungen

- ⚠️ Das Ergebnis hängt vom eingestellten Zahlenformat bzw. der Locale ab.
- ⚠️ Ein Punkt wurde im getesteten deutschen Zahlenformat als Tausendertrennzeichen interpretiert.

## Empfehlungen

- 💡 Für Geldbeträge nur verwenden, wenn das Eingabeformat zur aktiven Locale passt.
