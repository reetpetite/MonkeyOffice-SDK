# MonKey Office experiment protocol

This document defines the minimum requirements for experiments executed in the
real MonKey Office interpreter. Experiments are research artifacts; they do not
become normative language rules until their observations have been consolidated
as evidence.

## 1. Purpose

Each experiment should answer one narrowly scoped question. Prefer several small
experiments over one script that mixes unrelated syntax, type, and runtime
behaviour.

A useful question is falsifiable, for example:

> Does `DIM name AS type = value` accept an initializer in build 249?

A weak question is too broad to interpret reliably, for example:

> How do variables work?

## 2. Required experiment files

Each experiment uses a permanent identifier and its own directory:

```text
research/MO-NNN/
├── experiment.yaml
├── script.monkey
├── expected.md
├── observed-buildNNN.yaml
└── report-buildNNN.md
```

The generated or imported files may be absent while an experiment is still
planned. The experiment identifier must never be reused for a different
question.

### `experiment.yaml`

The machine-readable experiment definition. It records the title, status,
relevant language features, individual test cases, and known safety exclusions.

### `script.monkey`

The exact script executed in MonKey Office. Generated scripts must remain
reviewable and versioned so that an observation can be reproduced later.

### `expected.md`

The pre-execution expectation. It must distinguish between documented behaviour,
inference, and hypothesis. Recording the expectation before execution reduces
retrospective interpretation.

### `observed-buildNNN.yaml`

The raw, structured output from one concrete MonKey Office build. Preserve values
exactly; do not silently normalize whitespace, decimal separators, errors, or
empty results.

### `report-buildNNN.md`

A human-readable report derived from the experiment definition and observation.
Interpretation belongs here, but must not claim more than the test cases support.

## 3. Test design rules

1. Change one relevant variable at a time.
2. Include a normal case and meaningful boundary cases.
3. Separate syntax acceptance from runtime semantics where possible.
4. Include a control case when output formatting or environment settings could
   affect the result.
5. Do not include a known crash, hang, destructive action, or persistent data
   mutation in a routine test script.
6. Record locale, operating system, MonKey Office version/build, and relevant
   import settings whenever they may affect the result.
7. Preserve rejected programs and error messages as observations; a failed
   program may still provide useful syntax evidence.

## 4. Expected-result classification

Every expectation uses the canonical evidence vocabulary:

- `documented` — predicted directly from an official source,
- `verified` — predicted from a previously reproduced experiment,
- `inferred` — reasoned from supported findings but not directly tested here,
- `hypothesis` — an unsupported candidate explanation.

See [`../model/evidence-classification.md`](../model/evidence-classification.md).

## 5. Observation rules

An observation records only what happened in the tested environment. It should
answer:

- Was the script accepted?
- Did it execute?
- What exact value or message appeared?
- Did the application remain responsive?
- Were there visible side effects?

Avoid phrases such as “always”, “never”, or “the language requires” unless the
experiment actually supports that scope. Prefer:

> In MonKey Office 2025 build 249 on macOS, test V03 was rejected with …

## 6. Promotion path

```text
question
   ↓
pre-registered expectation
   ↓
real interpreter experiment
   ↓
raw observation
   ↓
consolidated evidence
   ↓
normative specification
   ↓
reference implementation and conformance tests
```

A successful parser test does not replace execution in MonKey Office. A single
interpreter observation may establish behaviour for the tested build, but wider
claims require suitable replication or explicit version scope.

## 7. Completion checklist

An experiment is ready for evidence review when:

- the question is narrow and explicit,
- the exact script is versioned,
- the tested environment is recorded,
- raw output is preserved,
- expected and observed behaviour are separated,
- dangerous or excluded cases are listed,
- conclusions do not exceed the observed cases,
- related open questions and earlier experiments are linked.

## 8. Isolierte Script-Matrizen

Für Syntax- und Statementfragen, bei denen ein Parserfehler den gesamten Testlauf verhindert, ist `kind: script-matrix` zu verwenden. Jeder Fall liegt unter `cases/` in einer eigenen `.monkey`-Datei und wird separat ausgeführt. Ein Fall muss ein eindeutiges Erfolgssignal aus Experiment- und Fall-ID enthalten. Wird dieses Signal nicht erreicht, sind Parsermeldung, Laufzeitmeldung und Anwendungszustand getrennt zu erfassen.

Mehrere Varianten dürfen nur dann in derselben Matrix stehen, wenn sie dieselbe eng begrenzte Forschungsfrage beantworten. Die Matrix darf keine Schlussfolgerung vorwegnehmen; erwartete Ergebnisse bleiben in `expected.md` klassifiziert.
