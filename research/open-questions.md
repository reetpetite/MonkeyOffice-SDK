# Open language questions

This file is the project-wide index of unresolved questions about the MonKey
Office scripting language. It prevents plausible assumptions from silently
entering the specification or reference implementation.

## Workflow

Each question receives a permanent `Q-NNN` identifier and one status:

- `open` — not yet scheduled,
- `planned` — assigned to an experiment,
- `partially-answered` — some cases are supported, but the scope remains open,
- `answered` — resolved by documented or verified evidence,
- `blocked` — cannot currently be tested safely or reproducibly.

When a question is answered, keep the entry and add links to the experiment,
evidence record, or official source. Do not delete historical questions.

## Entry template

```markdown
## Q-NNN — Concise question

- **Status:** open
- **Area:** declarations | expressions | types | control-flow | functions | runtime
- **Raised:** YYYY-MM-DD
- **Related evidence:** none
- **Planned experiment:** none

### Question

State one falsifiable question.

### Current basis

- `documented`: …
- `verified`: …
- `inferred`: …
- `hypothesis`: …

### Resolution criteria

Describe which observation or source would answer the question.
```

---

## Q-001 — Can one `DIM` declaration introduce multiple variables?

- **Status:** open
- **Area:** declarations
- **Raised:** 2026-07-20
- **Related evidence:** none
- **Planned experiment:** none

### Question

Does MonKey Office accept comma-separated variable names or declarations in one
`DIM` statement, and if so, how is the type applied?

Candidate forms include:

```monkeyoffice
DIM a, b AS Number
DIM a AS Number, b AS String
```

### Current basis

- `documented`: no supporting claim recorded yet.
- `verified`: no controlled experiment recorded yet.
- `hypothesis`: declarations may be limited to one variable per statement.

### Resolution criteria

Execute isolated syntax tests for each candidate form and preserve both accepted
output and exact rejection messages.

## Q-002 — Which declaration types are accepted after `AS`?

- **Status:** open
- **Area:** types
- **Raised:** 2026-07-20
- **Related evidence:** none
- **Planned experiment:** none

### Question

Which type names are valid in a `DIM name AS type` declaration, and are type
names case-sensitive?

### Current basis

- `documented`: individual type names exist elsewhere in the repository, but a
  complete declaration-specific set has not yet been consolidated here.
- `verified`: no declaration matrix has been executed in the real interpreter.
- `hypothesis`: type keywords are case-insensitive, like other language words.

### Resolution criteria

Run a generated matrix containing one isolated declaration per candidate type,
including capitalization variants and one unknown control name.

## Q-003 — What happens when `SET` assigns an incompatible value?

- **Status:** open
- **Area:** types
- **Raised:** 2026-07-20
- **Related evidence:** none
- **Planned experiment:** none

### Question

Does `SET variable TO expression` reject incompatible values, convert them, or
store them with dynamic typing?

### Current basis

- `documented`: no consolidated rule recorded yet.
- `verified`: no controlled assignment matrix recorded yet.
- `hypothesis`: behaviour may depend on the declared variable type and source
  value.

### Resolution criteria

Test a small cross-type matrix while separating parse acceptance, execution,
resulting value, and exact error behaviour.

## Q-004 – Sind Schlüsselwörter und Typnamen case-sensitive?

- Status: Experiment vorbereitet
- Experiment: `MO-031`
- Ziel: Trennung der Groß-/Kleinschreibung von Bezeichnerfragen

## Q-005 – Welche Initialisierungsformen unterstützt DIM?

- Status: Experiment vorbereitet
- Experiment: `MO-032`
- Abgrenzung: Typkompatibilität bleibt Gegenstand von `Q-003`

## Q-006 – Welche Leerraumzeichen dürfen Tokens einer Deklaration trennen?

- Status: Experiment vorbereitet
- Experiment: `MO-033`
- Schwerpunkt: Leerzeichen, Tabulator und Zeilenumbruch
