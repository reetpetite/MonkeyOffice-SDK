# `CountFields()`

**SDK-ID:** `MOF-STR-016`  
**Status:** ✅ `verified`  
**Kategorie:** `String`  
**Getestete Builds:** 249

Zählt durch einen Separator getrennte Felder.

## Signatur

```monkeyoffice
CountFields(text, separator)
```

**Rückgabewert:** `number`

## Beispiele

```monkeyoffice
CountFields("A,,B", ",")
```

Ergebnis: `3`

## Qualitätsstatus

- **documentation:** `complete`
- **experiments:** `complete`
- **edge_cases:** `complete`
- **regression:** `partial`
- **confidence:** `high`

## Forschungsgrundlage

`MO-014`
