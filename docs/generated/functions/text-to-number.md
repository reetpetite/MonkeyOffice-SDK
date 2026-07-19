# `TextToNumber()`

**SDK-ID:** `MOF-NUM-002`  
**Status:** ✅ `verified`  
**Kategorie:** `Number`  
**Getestete Builds:** 249

Liest aus einem Text einen ganzzahligen numerischen Wert.

## Signatur

```monkeyoffice
TextToNumber(text)
```

**Rückgabewert:** `number`

## Beispiele

```monkeyoffice
TextToNumber("123")
```

Ergebnis: `123`

```monkeyoffice
TextToNumber("123,45")
```

Ergebnis: `123`

```monkeyoffice
TextToNumber("-123,45")
```

Ergebnis: `-123`

```monkeyoffice
TextToNumber("")
```

Ergebnis: `0`

## Qualitätsstatus

- **documentation:** `complete`
- **experiments:** `complete`
- **edge_cases:** `complete`
- **regression:** `partial`
- **confidence:** `high`

## Forschungsgrundlage

`MO-025`

## Warnungen

- ⚠️ Nachkommastellen werden im getesteten Build nicht übernommen.

## Empfehlungen

- 💡 Für Geldbeträge mit Nachkommastellen stattdessen FTextToNumber() verwenden.
