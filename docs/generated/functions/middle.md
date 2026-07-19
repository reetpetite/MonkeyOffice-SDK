# `Middle()`

**SDK-ID:** `MOF-STR-002`  
**Status:** ✅ `verified`  
**Kategorie:** `String`  
**Getestete Builds:** 249

Gibt einen Teilstring ab einer angegebenen Position zurück.

## Signatur

```monkeyoffice
Middle(text, start, length)
```

**Rückgabewert:** `string`

## Beispiele

```monkeyoffice
Middle("ABCDE", 2, 2)
```

Ergebnis: `BC`

## Qualitätsstatus

- **documentation:** `complete`
- **experiments:** `complete`
- **edge_cases:** `partial`
- **regression:** `partial`
- **confidence:** `high`

## Forschungsgrundlage

`MO-001`

## Warnungen

- ⚠️ Position 0 verhält sich nicht wie die reguläre 1-basierte Indizierung.

## Empfehlungen

- 💡 Startpositionen explizit ab 1 verwenden.
