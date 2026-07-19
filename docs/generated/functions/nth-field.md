# `NthField()`

**SDK-ID:** `MOF-STR-017`  
**Status:** ✅ `verified`  
**Kategorie:** `String`  
**Getestete Builds:** 249

Gibt ein bestimmtes, durch einen Separator getrenntes Feld zurück.

## Signatur

```monkeyoffice
NthField(text, separator, index)
```

**Rückgabewert:** `string`

## Beispiele

```monkeyoffice
NthField("A,,B", ",", 2)
```

Ergebnis: ``

## Qualitätsstatus

- **documentation:** `complete`
- **experiments:** `complete`
- **edge_cases:** `complete`
- **regression:** `partial`
- **confidence:** `high`

## Forschungsgrundlage

`MO-015`
