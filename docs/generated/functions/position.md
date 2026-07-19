# `Position()`

**SDK-ID:** `MOF-STR-004`  
**Status:** ✅ `verified`  
**Kategorie:** `String`  
**Getestete Builds:** 249

Ermittelt die Position eines Treffers innerhalb eines Texts.

## Signatur

```monkeyoffice
Position(text, search, occurrence, start)
```

**Rückgabewert:** `number`

## Beispiele

```monkeyoffice
Position("AAAA", "AA", 2, 1)
```

Ergebnis: `2`

## Qualitätsstatus

- **documentation:** `complete`
- **experiments:** `complete`
- **edge_cases:** `complete`
- **regression:** `partial`
- **confidence:** `high`

## Forschungsgrundlage

`MO-005`, `MO-018`
