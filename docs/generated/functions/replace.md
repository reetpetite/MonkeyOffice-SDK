# `Replace()`

**SDK-ID:** `MOF-STR-001`  
**Status:** `verified`  
**Kategorie:** `String`

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

## Forschungsgrundlage

`MO-002`, `MO-023`

## Empfehlungen

- 💡 Leere Suchtexte sollten vor dem Aufruf geprüft werden, auch wenn sie im getesteten Build ungefährlich waren.
