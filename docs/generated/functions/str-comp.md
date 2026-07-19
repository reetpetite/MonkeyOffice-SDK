# `StrComp()`

**SDK-ID:** `MOF-STR-006`  
**Status:** ✅ `verified`  
**Kategorie:** `String`  
**Getestete Builds:** 249

Vergleicht zwei Strings unter Beachtung der Groß- und Kleinschreibung.

## Signatur

```monkeyoffice
StrComp(left, right)
```

**Rückgabewert:** `number`

## Beispiele

```monkeyoffice
StrComp("A", "a")
```

Ergebnis: `experimentell verschieden`

## Qualitätsstatus

- **documentation:** `complete`
- **experiments:** `complete`
- **edge_cases:** `partial`
- **regression:** `partial`
- **confidence:** `high`

## Forschungsgrundlage

`MO-007`
