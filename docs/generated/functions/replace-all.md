# `ReplaceAll()`

**SDK-ID:** `MOF-STR-003`  
**Status:** ✅ `verified`  
**Kategorie:** `String`  
**Getestete Builds:** 249

Ersetzt alle nicht überlappenden Treffer eines Suchtexts.

## Signatur

```monkeyoffice
ReplaceAll(text, search, replacement)
```

**Rückgabewert:** `string`

## Beispiele

```monkeyoffice
ReplaceAll("AAAA", "AA", "X")
```

Ergebnis: `XX`

```monkeyoffice
ReplaceAll("AaAa", "aa", "X")
```

Ergebnis: `XX`

```monkeyoffice
ReplaceAll("ABC", "", "X")
```

Ergebnis: `ABC`

## Qualitätsstatus

- **documentation:** `complete`
- **experiments:** `complete`
- **edge_cases:** `complete`
- **regression:** `partial`
- **confidence:** `high`

## Forschungsgrundlage

`MO-003`, `MO-024`
