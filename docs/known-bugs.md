# Bekannte Fehler und gefährliche Randfälle

Diese Datei dokumentiert Verhaltensweisen, die zu einem Hänger, einem falschen Importergebnis oder einer schwer erkennbaren Fehlinterpretation führen können.

## `PatternCount()` mit leerem Suchtext

**Forschungs-ID:** MO-022  
**Status:** 🧪 experimentell verifiziert  
**Schweregrad:** kritisch

### Problem

Ein Aufruf mit leerem Suchtext kann MonKey Office aufhängen und den macOS-Wartecursor anzeigen.

```monkeyoffice
PatternCount("ABC", "")
```

### Beobachtung

MonKey Office reagierte nach dem Aufruf nicht mehr normal. Der Test wurde deshalb als gefährlich eingestuft.

### Empfehlung

`PatternCount()` darf nur aufgerufen werden, wenn der Suchtext nachweislich nicht leer ist.

```monkeyoffice
if Length(SearchText) > 0 then
    Treffer = PatternCount(SourceText, SearchText)
endif
```

⚠️ Der gefährliche Test sollte nicht als Bestandteil automatischer Regressionstests ausgeführt werden.

---

## Gebietsschemaabhängigkeit von `FTextToNumber()`

**Forschungs-ID:** MO-026  
**Status:** 🧪 experimentell verifiziert  
**Schweregrad:** hoch

### Problem

`FTextToNumber()` interpretiert Zahlen entsprechend dem erwarteten lokalen Zahlenformat.

In der getesteten Umgebung wurde das Komma als Dezimaltrennzeichen und der Punkt als Gruppierungszeichen behandelt.

```monkeyoffice
FTextToNumber("123,45")
```

ergab ungefähr:

```text
123,45
```

Dagegen ergab:

```monkeyoffice
FTextToNumber("123.45")
```

den Wert:

```text
12345
```

### Risiko

Ein englisch formatierter Betrag kann dadurch um den Faktor 100 zu groß importiert werden.

### Empfehlung

Vor der Konvertierung muss das Zahlenformat der Quelldatei eindeutig bekannt sein.

Englische Zahlen dürfen nicht ungeprüft an eine deutsch formatierte `FTextToNumber()`-Auswertung übergeben werden.

---

## `TextToNumber()` verwirft Nachkommastellen

**Forschungs-ID:** MO-025  
**Status:** 🧪 experimentell verifiziert  
**Schweregrad:** hoch bei Geldbeträgen

### Problem

```monkeyoffice
TextToNumber("123,45")
```

ergibt:

```text
123
```

Auch bei einer negativen Zahl wird nur der ganzzahlige Anfang übernommen:

```monkeyoffice
TextToNumber("-123,45")
```

ergibt:

```text
-123
```

### Empfehlung

`TextToNumber()` sollte nur für tatsächlich ganzzahlige Werte verwendet werden, etwa:

- Jahr
- Monat
- Tag
- Positionsnummern
- Zähler

Für Geldbeträge ist stattdessen eine kontrollierte Konvertierung mit `FTextToNumber()` erforderlich.

---

## Leerer oder ungültiger Text kann als Null erscheinen

Sowohl:

```monkeyoffice
TextToNumber("")
```

als auch:

```monkeyoffice
FTextToNumber("")
```

ergaben im Test den Wert `0`.

### Risiko

Anhand des Ergebnisses allein kann nicht unterschieden werden zwischen:

- einer tatsächlichen Null,
- einem leeren Feld,
- möglicherweise weiteren ungültigen Eingaben.

### Empfehlung

Leere Eingabefelder sollten vor der Zahlenkonvertierung ausdrücklich geprüft werden.

```monkeyoffice
if Length(Trim(SourceText)) > 0 then
    Value = FTextToNumber(SourceText)
endif
```

---

## `Middle()` mit Position 0

**Forschungs-ID:** MO-001  
**Status:** 🧪 experimentell verifiziert  
**Schweregrad:** mittel

Die Funktion verwendet grundsätzlich 1-basierte Positionen. Position `0` ist jedoch kein normaler Fehlerfall, sondern liefert ein abweichendes Ergebnis.

```monkeyoffice
Middle("ABCDE", 0, 2)
```

ergab:

```text
A
```

Dagegen:

```monkeyoffice
Middle("ABCDE", 1, 2)
```

ergab:

```text
AB
```

### Empfehlung

Für `Middle()` niemals Position `0` verwenden.

---

## Asymmetrie bei leerem Feldtrenner

**Forschungs-IDs:** MO-014 und MO-015  
**Status:** 🧪 experimentell verifiziert  
**Schweregrad:** mittel

```monkeyoffice
CountFields("ABC", "")
```

ergab:

```text
1
```

Dagegen ergab:

```monkeyoffice
NthField("ABC", "", 1)
```

einen leeren Text.

### Empfehlung

`CountFields()` und `NthField()` sollten nicht mit einem leeren Trenner aufgerufen werden. Insbesondere darf nicht angenommen werden, dass beide Funktionen bei diesem Randfall symmetrisch arbeiten.