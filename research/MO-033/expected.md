# MO-033 – Erwartung vor Ausführung

## Fragestellung

Welche Leerraumformen trennt der MonKey-Office-Interpreter innerhalb einer Deklaration, und beendet ein Zeilenumbruch die Anweisung?

## Einordnung

- W01: dokumentierter Kontrollfall
- W02 und W03: `inferred`
- W04: `hypothesis`

## Erwartungen

W01 sollte akzeptiert werden. W02 und W03 werden voraussichtlich wie W01 behandelt. W04 wird voraussichtlich abgelehnt, weil die vorhandenen Skripte Anweisungen zeilenweise strukturieren; dies ist vor der Ausführung jedoch nicht verifiziert.
