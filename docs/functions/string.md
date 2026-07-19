# Stringfunktionen

Diese Referenz dokumentiert die experimentell untersuchten Textfunktionen der MonKey-Office-Skriptsprache.

## Kennzeichnungen

- 📖 offiziell dokumentierte Syntax
- 🧪 experimentell verifiziertes Verhalten
- 💡 praktische Empfehlung
- ⚠️ gefährlicher Randfall
- ❓ noch nicht abschließend untersucht

## Allgemeine Beobachtungen

Mehrere Such- und Ersetzungsfunktionen arbeiten **case-insensitiv**. Davon ausgenommen ist der Vergleich mit `StrComp()`.

Die Funktionen unterscheiden sich darin, ob sie überlappende Treffer berücksichtigen:

| Funktion | Überlappende Treffer |
|---|---:|
| `Position()` | ja |
| `PatternCount()` | ja |
| `Replace()` | nur erster Treffer |
| `ReplaceAll()` | nein |
| `CountFields()` | nein |
| `NthField()` | nein |

---

# `Length()`

## Signatur

```monkeyoffice
Length(Text)
```

## Verhalten

🧪 `Length()` gibt die Anzahl der Zeichen eines Textes zurück.

```monkeyoffice
Length("ABCDE")
```

Ergebnis:

```text
5
```

```monkeyoffice
Length("")
```

Ergebnis:

```text
0
```

Leerzeichen werden mitgezählt:

```monkeyoffice
Length(" A ")
```

Ergebnis:

```text
3
```

## Forschungs-ID

MO-008

---

# `Left()`

## Signatur

```monkeyoffice
Left(Text, Anzahl)
```

## Verhalten

🧪 Gibt die angegebene Anzahl Zeichen vom linken Rand des Textes zurück.

```monkeyoffice
Left("ABCDE", 2)
```

Ergebnis:

```text
AB
```

Bei einer Anzahl von `0` wird ein leerer Text zurückgegeben:

```monkeyoffice
Left("ABCDE", 0)
```

Ergebnis:

```text

```

Ist die Anzahl größer als die Textlänge, wird der vollständige Text zurückgegeben:

```monkeyoffice
Left("ABCDE", 10)
```

Ergebnis:

```text
ABCDE
```

## Forschungs-ID

MO-009

---

# `Right()`

## Signatur

```monkeyoffice
Right(Text, Anzahl)
```

## Verhalten

🧪 Gibt die angegebene Anzahl Zeichen vom rechten Rand des Textes zurück.

Das Verhalten bei `0` und bei einer Anzahl oberhalb der Textlänge entspricht `Left()`.

## Forschungs-ID

MO-010

---

# `Middle()`

## Signatur

```monkeyoffice
Middle(Text, Position, Anzahl)
```

## Verhalten

🧪 Die reguläre Zeichenpositionierung ist 1-basiert.

```monkeyoffice
Middle("ABCDE", 1, 2)
```

Ergebnis:

```text
AB
```

```monkeyoffice
Middle("ABCDE", 2, 2)
```

Ergebnis:

```text
BC
```

## Position 0

⚠️ Position `0` erzeugt keinen normalen Fehler, verhält sich aber abweichend:

```monkeyoffice
Middle("ABCDE", 0, 2)
```

Ergebnis:

```text
A
```

💡 Position `0` sollte nicht verwendet werden.

## Forschungs-ID

MO-001

---

# `Trim()`

## Signatur

```monkeyoffice
Trim(Text)
```

## Verhalten

🧪 Entfernt Leerzeichen am linken und rechten Rand.

```monkeyoffice
Trim("  ABC  ")
```

Ergebnis:

```text
ABC
```

❓ Das Verhalten bei Tabulatoren, Zeilenumbrüchen und anderen Leerraumzeichen wurde noch nicht geprüft.

## Forschungs-ID

MO-011

---

# `LTrim()`

## Signatur

```monkeyoffice
LTrim(Text)
```

## Verhalten

🧪 Entfernt Leerzeichen am linken Rand.

Leerzeichen am rechten Rand bleiben erhalten.

## Forschungs-ID

MO-011

---

# `RTrim()`

## Signatur

```monkeyoffice
RTrim(Text)
```

## Verhalten

🧪 Entfernt Leerzeichen am rechten Rand.

Leerzeichen am linken Rand bleiben erhalten.

## Forschungs-ID

MO-011

---

# `Lower()`

## Signatur

```monkeyoffice
Lower(Text)
```

## Verhalten

🧪 Wandelt Buchstaben in Kleinbuchstaben um.

```monkeyoffice
Lower("ÄBC XYZ")
```

Ergebnis:

```text
äbc xyz
```

Deutsche Umlaute werden verarbeitet.

## Forschungs-ID

MO-012

---

# `Upper()`

## Signatur

```monkeyoffice
Upper(Text)
```

## Verhalten

🧪 Wandelt Buchstaben in Großbuchstaben um.

```monkeyoffice
Upper("äbc xyz")
```

Ergebnis:

```text
ÄBC XYZ
```

Deutsche Umlaute werden verarbeitet.

## Forschungs-ID

MO-012

---

# `Proper()`

## Signatur

```monkeyoffice
Proper(Text)
```

## Verhalten

🧪 Wandelt den ersten Buchstaben eines Wortes in einen Großbuchstaben und die übrigen Buchstaben in Kleinbuchstaben um.

```monkeyoffice
Proper("hALLO wELT")
```

Ergebnis:

```text
Hallo Welt
```

❓ Noch nicht geprüft sind Wortgrenzen bei Bindestrichen, Apostrophen, Ziffern und mehrfachen Leerzeichen.

## Forschungs-ID

MO-013

---

# `StrComp()`

## Signatur

```monkeyoffice
StrComp(Text1, Text2)
```

## Verhalten

🧪 `StrComp()` führt einen case-sensitiven Drei-Wege-Vergleich aus.

| Ausdruck | Ergebnis |
|---|---:|
| `StrComp("ABC", "ABC")` | `0` |
| `StrComp("ABC", "abc")` | `-1` |
| `StrComp("ABC", "ABD")` | `-1` |
| `StrComp("ABD", "ABC")` | `1` |

Die Rückgabewerte bedeuten:

| Rückgabe | Bedeutung |
|---:|---|
| kleiner als `0` | erster Text sortiert vor dem zweiten |
| `0` | Texte sind identisch |
| größer als `0` | erster Text sortiert nach dem zweiten |

💡 Für Gleichheit sollte auf `0` geprüft werden. Es sollte nicht vorausgesetzt werden, dass alle kleineren oder größeren Ergebnisse immer exakt `-1` beziehungsweise `1` sind, solange dies nicht umfassender getestet wurde.

## Forschungs-ID

MO-007

---

# `Position()`

## Signatur

```monkeyoffice
Position(Text, Suchtext, Startposition, Vorkommen)
```

## Parameter

| Parameter | Bedeutung |
|---|---|
| `Text` | zu durchsuchender Ausgangstext |
| `Suchtext` | gesuchte Zeichenfolge |
| `Startposition` | Position, ab der gesucht wird |
| `Vorkommen` | welches Vorkommen zurückgegeben werden soll |

## Verhalten

🧪 Die Funktion benötigt vier Parameter.

🧪 Die zurückgegebene Position ist 1-basiert.

🧪 Die Suche ist case-insensitiv.

🧪 Die Startposition ist inklusiv.

```monkeyoffice
Position("ABC ABC", "ABC", 2, 1)
```

Ergebnis:

```text
5
```

Wird kein Treffer gefunden, lautet das Ergebnis `0`.

## Randfälle

Eine Startposition kleiner als `1` verhält sich wie Position `1`.

Eine Startposition hinter dem Textende ergibt `0`.

Ein Vorkommen kleiner oder gleich `0` ergibt `0`.

Ein nicht vorhandenes Vorkommen ergibt `0`.

Ein leerer Suchtext ergibt `0`:

```monkeyoffice
Position("ABC", "", 1, 1)
```

Ergebnis:

```text
0
```

## Überlappende Treffer

🧪 `Position()` berücksichtigt überlappende Treffer.

```monkeyoffice
Position("AAAA", "AA", 1, 1)
```

Ergebnis:

```text
1
```

```monkeyoffice
Position("AAAA", "AA", 1, 2)
```

Ergebnis:

```text
2
```

Auch:

```monkeyoffice
Position("ABABA", "ABA", 1, 2)
```

ergibt:

```text
3
```

## Forschungs-IDs

MO-005, MO-018

---

# `PatternCount()`

## Signatur

```monkeyoffice
PatternCount(Text, Suchtext)
```

## Verhalten

🧪 Zählt die Anzahl der Vorkommen des Suchtextes.

🧪 Die Suche ist case-insensitiv.

🧪 Überlappende Treffer werden gezählt.

```monkeyoffice
PatternCount("AAAA", "AA")
```

Ergebnis:

```text
3
```

Die Treffer beginnen an den Positionen `1`, `2` und `3`.

```monkeyoffice
PatternCount("ABABA", "ABA")
```

Ergebnis:

```text
2
```

```monkeyoffice
PatternCount("AaAa", "aa")
```

Ergebnis:

```text
3
```

Ein leerer Ausgangstext oder ein Suchtext, der länger als der Ausgangstext ist, ergibt `0`.

## Kritischer Randfall

⚠️ Ein leerer Suchtext kann MonKey Office aufhängen:

```monkeyoffice
PatternCount("ABC", "")
```

Dieser Aufruf darf nicht ungeschützt verwendet werden.

💡 Sichere Verwendung:

```monkeyoffice
if Length(SearchText) > 0 then
    Count = PatternCount(SourceText, SearchText)
endif
```

Der gefährliche Test sollte nicht in automatische Testsuites aufgenommen werden.

## Forschungs-IDs

MO-006, MO-022

---

# `Replace()`

## Signatur

```monkeyoffice
Replace(Text, Suchtext, Ersatztext)
```

## Verhalten

🧪 Ersetzt nur den ersten Treffer.

🧪 Die Suche ist case-insensitiv.

```monkeyoffice
Replace("ABC ABC", "ABC", "X")
```

Ergebnis:

```text
X ABC
```

```monkeyoffice
Replace("AAAA", "AA", "X")
```

Ergebnis:

```text
XAA
```

```monkeyoffice
Replace("ABABA", "ABA", "X")
```

Ergebnis:

```text
XBA
```

Die nicht ersetzten Textbereiche behalten ihre ursprüngliche Groß- und Kleinschreibung.

```monkeyoffice
Replace("AaAa", "aa", "X")
```

Ergebnis:

```text
XAa
```

Ein leerer Ersatztext entfernt den ersten Treffer:

```monkeyoffice
Replace("AAAA", "A", "")
```

Ergebnis:

```text
AAA
```

Kein Treffer lässt den Ausgangstext unverändert.

Ein leerer Ausgangstext ergibt einen leeren Text.

Ein leerer Suchtext lässt den Ausgangstext unverändert:

```monkeyoffice
Replace("ABC", "", "X")
```

Ergebnis:

```text
ABC
```

## Forschungs-IDs

MO-002, MO-023

---

# `ReplaceAll()`

## Signatur

```monkeyoffice
ReplaceAll(Text, Suchtext, Ersatztext)
```

## Verhalten

🧪 Ersetzt alle nicht überlappenden Treffer.

🧪 Die Suche ist case-insensitiv.

```monkeyoffice
ReplaceAll("ABC ABC", "ABC", "X")
```

Ergebnis:

```text
X X
```

```monkeyoffice
ReplaceAll("AAAA", "AA", "X")
```

Ergebnis:

```text
XX
```

## Keine überlappende Ersetzung

```monkeyoffice
ReplaceAll("ABABA", "ABA", "X")
```

Ergebnis:

```text
XBA
```

Obwohl `"ABA"` an Position `1` und überlappend erneut an Position `3` beginnt, wird nur der erste Treffer ersetzt. Nach einem Treffer wird die Verarbeitung hinter dem vollständig gefundenen Suchtext fortgesetzt.

## Weitere Randfälle

```monkeyoffice
ReplaceAll("AaAa", "aa", "X")
```

Ergebnis:

```text
XX
```

Ein leerer Ersatztext entfernt alle Treffer:

```monkeyoffice
ReplaceAll("AAAA", "A", "")
```

Ergebnis:

```text

```

Ein leerer Suchtext lässt den Ausgangstext unverändert:

```monkeyoffice
ReplaceAll("ABC", "", "X")
```

Ergebnis:

```text
ABC
```

Kein Treffer lässt den Ausgangstext unverändert.

## Forschungs-IDs

MO-003, MO-024

---

# `CountFields()`

## Signatur

```monkeyoffice
CountFields(Text, Trenner)
```

## Verhalten

🧪 Gibt die Anzahl der durch einen Trenner entstehenden Felder zurück.

```monkeyoffice
CountFields("A;B;C", ";")
```

Ergebnis:

```text
3
```

Leere Felder werden mitgezählt:

```monkeyoffice
CountFields("A;;C", ";")
```

Ergebnis:

```text
3
```

Auch führende und abschließende leere Felder werden berücksichtigt:

| Ausdruck | Ergebnis |
|---|---:|
| `CountFields(";A;B", ";")` | `3` |
| `CountFields("A;B;", ";")` | `3` |
| `CountFields(";A;", ";")` | `3` |

Ein leerer Ausgangstext ergibt `0`.

Enthält der Text keinen Trenner, ergibt die Funktion `1`:

```monkeyoffice
CountFields("ABC", ";")
```

Ergebnis:

```text
1
```

## Mehrteilige Trenner

🧪 Mehrteilige Trenner werden unterstützt:

```monkeyoffice
CountFields("A--B--C", "--")
```

Ergebnis:

```text
3
```

## Groß- und Kleinschreibung

🧪 Der Trennervergleich ist case-insensitiv:

```monkeyoffice
CountFields("AxxBXXC", "xx")
```

Ergebnis:

```text
3
```

## Keine überlappenden Trenner

```monkeyoffice
CountFields("AAAA", "AA")
```

Ergebnis:

```text
3
```

Das entspricht zwei nicht überlappenden Trennern und damit drei Feldern.

```monkeyoffice
CountFields("ABABA", "ABA")
```

Ergebnis:

```text
2
```

## Leerer Trenner

```monkeyoffice
CountFields("ABC", "")
```

Ergebnis:

```text
1
```

```monkeyoffice
CountFields("", "")
```

Ergebnis:

```text
0
```

⚠️ Dieses Verhalten ist nicht symmetrisch zu `NthField()`.

💡 Ein leerer Trenner sollte vermieden werden.

## Forschungs-ID

MO-014

---

# `NthField()`

## Signatur

```monkeyoffice
NthField(Text, Trenner, Feldnummer)
```

## Verhalten

🧪 Gibt das angeforderte Feld eines getrennten Textes zurück.

Die Feldnummerierung ist 1-basiert.

```monkeyoffice
NthField("A;B;C", ";", 1)
```

Ergebnis:

```text
A
```

```monkeyoffice
NthField("A;B;C", ";", 2)
```

Ergebnis:

```text
B
```

## Leere Felder

Leere Felder bleiben erhalten:

```monkeyoffice
NthField("A;;C", ";", 2)
```

Ergebnis:

```text

```

Auch führende und abschließende leere Felder werden erhalten:

```monkeyoffice
NthField(";A;B", ";", 1)
```

Ergebnis:

```text

```

```monkeyoffice
NthField("A;B;", ";", 3)
```

Ergebnis:

```text

```

## Ungültige Feldnummern

Folgende Feldnummern ergeben einen leeren Text:

- `0`
- negative Werte
- Werte oberhalb der vorhandenen Feldzahl

## Mehrteilige Trenner

```monkeyoffice
NthField("A--B--C", "--", 2)
```

Ergebnis:

```text
B
```

## Groß- und Kleinschreibung

Der Trennervergleich ist case-insensitiv:

```monkeyoffice
NthField("AxxBXXC", "xx", 3)
```

Ergebnis:

```text
C
```

## Leerer Trenner

```monkeyoffice
NthField("ABC", "", 1)
```

Ergebnis:

```text

```

Auch weitere Feldnummern ergeben einen leeren Text.

⚠️ Dieses Verhalten unterscheidet sich von:

```monkeyoffice
CountFields("ABC", "")
```

das den Wert `1` ergibt.

💡 `NthField()` sollte nicht mit einem leeren Trenner aufgerufen werden.

## Forschungs-ID

MO-015

---

# Übersicht der leeren Suchtexte und Trenner

| Funktion | Leerer Suchtext beziehungsweise Trenner |
|---|---|
| `Position("ABC", "", 1, 1)` | `0` |
| `PatternCount("ABC", "")` | ⚠️ Anwendung kann hängen |
| `Replace("ABC", "", "X")` | `"ABC"` |
| `ReplaceAll("ABC", "", "X")` | `"ABC"` |
| `CountFields("ABC", "")` | `1` |
| `NthField("ABC", "", 1)` | `""` |

Es existiert kein einheitliches Verhalten für leere Suchtexte oder Trenner. Jeder Funktionsaufruf muss daher separat abgesichert werden.

---

# Praktische Empfehlungen

## Suchtexte und Trenner prüfen

```monkeyoffice
if Length(SearchText) > 0 then
    Result = PatternCount(SourceText, SearchText)
endif
```

## Positionen 1-basiert behandeln

Für `Middle()`, `Position()` und `NthField()` sollten reguläre Positionen beziehungsweise Feldnummern stets bei `1` beginnen.

## Case-insensitive Verarbeitung beachten

Bei folgenden Funktionen wurde eine case-insensitive Verarbeitung nachgewiesen:

- `Position()`
- `PatternCount()`
- `Replace()`
- `ReplaceAll()`
- `CountFields()`
- `NthField()`

`StrComp()` arbeitet dagegen case-sensitiv.

## Überlappungen nicht verallgemeinern

Die Trefferzahl aus `PatternCount()` kann größer sein als die Zahl der von `ReplaceAll()` ersetzten Textstellen.

Beispiel:

```monkeyoffice
PatternCount("AAAA", "AA")
```

ergibt `3`, während:

```monkeyoffice
ReplaceAll("AAAA", "AA", "X")
```

den Text `"XX"` erzeugt.