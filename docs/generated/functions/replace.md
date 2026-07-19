# `Replace()`

**SDK-ID:** `MOF-STR-001`  
**Status:** ✅ `verified`  
**Kategorie:** `String`  
**Getestete Builds:** 249

Ersetzt den ersten Treffer eines Suchtexts.

## Signatur

```monkeyoffice
Replace(text, search, replacement)
```

**Rückgabewert:** `string`

## Beispiele

```monkeyoffice
Replace("AAAA", "AA", "X")
```

Ergebnis: `XAA`

```monkeyoffice
Replace("ABABA", "ABA", "X")
```

Ergebnis: `XBA`

```monkeyoffice
Replace("AaAa", "aa", "X")
```

Ergebnis: `XAa`

```monkeyoffice
Replace("ABC", "", "X")
```

Ergebnis: `ABC`

## Qualitätsstatus

- **documentation:** `complete`
- **experiments:** `complete`
- **edge_cases:** `complete`
- **regression:** `partial`
- **confidence:** `high`

## Forschungsgrundlage

`MO-002`, `MO-023`

## Empfehlungen

- 💡 Leere Suchtexte sollten vor dem Aufruf geprüft werden, auch wenn sie im getesteten Build ungefährlich waren.
