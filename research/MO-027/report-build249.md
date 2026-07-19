# MO-027 – Left, Right und Middle - Grenzwerte

**Status:** `completed`  
**Build:** `249`  
**Plattform:** `macOS`

## Ergebnisse

| Test | Ausdruck | Beobachtung |
|---|---|---|
| `L01` | `Left("ABCDE",0)` | `` |
| `L02` | `Left("ABCDE",-1)` | `` |
| `L03` | `Left("ABCDE",1)` | `A` |
| `L04` | `Left("ABCDE",2)` | `AB` |
| `L05` | `Left("ABCDE",5)` | `ABCDE` |
| `L06` | `Left("ABCDE",10)` | `ABCDE` |
| `R01` | `Right("ABCDE",0)` | `` |
| `R02` | `Right("ABCDE",-1)` | `` |
| `R03` | `Right("ABCDE",1)` | `E` |
| `R04` | `Right("ABCDE",2)` | `DE` |
| `R05` | `Right("ABCDE",5)` | `ABCDE` |
| `R06` | `Right("ABCDE",10)` | `ABCDE` |
| `M01` | `Middle("ABCDE",0,2)` | `A` |
| `M02` | `Middle("ABCDE",-1,2)` | `` |
| `M03` | `Middle("ABCDE",1,2)` | `AB` |
| `M04` | `Middle("ABCDE",2,2)` | `BC` |
| `M05` | `Middle("ABCDE",2,0)` | `` |
| `M06` | `Middle("ABCDE",2,-1)` | `` |
| `M07` | `Middle("ABCDE",10,2)` | `` |
| `M08` | `Middle("ABCDE",2,10)` | `BCDE` |

## Rohdaten

```text
MO-027|L01=[]|L02=[]|L03=[A]|L04=[AB]|L05=[ABCDE]|L06=[ABCDE]|R01=[]|R02=[]|R03=[E]|R04=[DE]|R05=[ABCDE]|R06=[ABCDE]|M01=[A]|M02=[]|M03=[AB]|M04=[BC]|M05=[]|M06=[]|M07=[]|M08=[BCDE]
```
