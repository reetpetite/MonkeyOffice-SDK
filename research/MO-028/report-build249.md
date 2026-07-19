# MO-028 – Trim, LTrim und RTrim - Leerzeichen

**Status:** `completed`  
**Build:** `249`  
**Plattform:** `macOS`

## Ergebnisse

| Test | Ausdruck | Beobachtung |
|---|---|---|
| `T01` | `Trim("  ABC  ")` | `ABC` |
| `T02` | `Trim("ABC")` | `ABC` |
| `T03` | `Trim("")` | `` |
| `T04` | `Trim("     ")` | `` |
| `T05` | `Trim("  A B C  ")` | `A B C` |
| `L01` | `LTrim("  ABC  ")` | `ABC  ` |
| `L02` | `LTrim("ABC")` | `ABC` |
| `L03` | `LTrim("")` | `` |
| `L04` | `LTrim("     ")` | `` |
| `L05` | `LTrim("  A B C  ")` | `A B C  ` |
| `R01` | `RTrim("  ABC  ")` | `  ABC` |
| `R02` | `RTrim("ABC")` | `ABC` |
| `R03` | `RTrim("")` | `` |
| `R04` | `RTrim("     ")` | `` |
| `R05` | `RTrim("  A B C  ")` | `  A B C` |

## Rohdaten

```text
MO-028|T01=[ABC]|T02=[ABC]|T03=[]|T04=[]|T05=[A B C]|L01=[ABC  ]|L02=[ABC]|L03=[]|L04=[]|L05=[A B C  ]|R01=[  ABC]|R02=[ABC]|R03=[]|R04=[]|R05=[  A B C]
```
