# `NumToText()`

**SDK-ID:** `MOF-NUM-001`  
**Status:** ✅ `verified`  
**Kategorie:** `Number`  
**Getestete Builds:** 249

Wandelt einen numerischen Wert in Text um.

## Signatur

```monkeyoffice
NumToText(number)
```

**Rückgabewert:** `string`

## Beispiele

```monkeyoffice
NumToText(123)
```

Ergebnis: `123`

## Qualitätsstatus

- **documentation:** `complete`
- **experiments:** `complete`
- **edge_cases:** `partial`
- **regression:** `partial`
- **confidence:** `high`

## Forschungsgrundlage

`MO-004`

## Empfehlungen

- 💡 Formatierungsdetails wie Dezimal- und Tausendertrennzeichen sollten build- und localeabhängig getestet werden.
