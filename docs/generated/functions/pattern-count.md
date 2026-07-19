# `PatternCount()`

**SDK-ID:** `MOF-STR-005`  
**Status:** ⚠️ `dangerous`  
**Kategorie:** `String`  
**Getestete Builds:** 249

Zählt Treffer eines Suchtexts innerhalb eines Texts.

## Signatur

```monkeyoffice
PatternCount(text, search)
```

**Rückgabewert:** `number`

## Beispiele

```monkeyoffice
PatternCount("AAAA", "AA")
```

Ergebnis: `3`

## Qualitätsstatus

- **documentation:** `complete`
- **experiments:** `complete`
- **edge_cases:** `complete`
- **regression:** `partial`
- **confidence:** `high`

## Forschungsgrundlage

`MO-006`, `MO-022`

## Warnungen

- ⚠️ Ein leerer Suchtext kann MonKey Office zum Hängen bringen.

## Empfehlungen

- 💡 Vor jedem Aufruf mit `Length(search) > 0` prüfen, dass der Suchtext nicht leer ist.
