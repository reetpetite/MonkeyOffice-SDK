# Conformance Test Model

> **Status:** Working model  
> **Scope:** Test metadata, evidence traceability, parser fixtures, runtime results,
> and future compatibility testing

## 1. Purpose

The conformance-test model defines a stable, machine-readable format for tests
that verify a MonKey Office language implementation against the documented
language behaviour.

The same model should support:

- parser acceptance tests,
- AST comparison,
- semantic validation tests,
- runtime result tests,
- diagnostic tests,
- regression tests across MonKey Office builds,
- and compatibility tests for future SDK tooling.

A conformance test is not automatically evidence. Evidence is established by
running controlled experiments against the original runtime and documenting the
result. Conformance tests encode the accepted conclusion so that compatible
implementations can reproduce it.

---

## 2. Test Categories

Initial categories:

```text
lexical
syntax
ast
semantic
runtime
diagnostic
regression
```

### `lexical`

Tests tokenization and literal recognition.

### `syntax`

Tests whether source text is accepted or rejected by the grammar.

### `ast`

Tests the structural interpretation of accepted source.

### `semantic`

Tests name resolution, operand types, function arity, and related validation.

### `runtime`

Tests evaluation results or runtime errors.

### `diagnostic`

Tests stable diagnostic codes and source ranges produced by SDK tooling.

### `regression`

Preserves behaviour associated with a specific bug, ambiguity, or runtime build.

---

## 3. Test Identity

Each test has a stable identifier.

Recommended format:

```text
MO-CF-<AREA>-<NUMBER>
```

Examples:

```text
MO-CF-EXPR-001
MO-CF-NUM-004
MO-CF-NOT-002
```

The identifier must not be reused after publication, even if a test is retired.

---

## 4. Required Metadata

```text
ConformanceTest
├── schemaVersion
├── id
├── title
├── category
├── status
├── source
├── expectation
└── evidence
```

### `schemaVersion`

Version of the conformance-test file format.

### `id`

Stable test identifier.

### `title`

Short human-readable description.

### `category`

One of the supported test categories.

### `status`

Recommended values:

```text
draft
verified
deprecated
```

A test should become `verified` only when its expected result is supported by
consolidated evidence.

### `source`

The exact script or expression under test.

### `expectation`

The required parser, semantic, runtime, or diagnostic result.

### `evidence`

Links the test to supporting experiment IDs and evidence documents.

---

## 5. Expected Outcomes

A test may define one or more expectation sections.

```text
Expectation
├── parse?
├── ast?
├── semantic?
├── runtime?
└── diagnostics?
```

### Parse expectation

```text
parse
├── accepted: boolean
└── entryPoint: program | statement | expression
```

### AST expectation

The AST may be represented either:

1. inline as structured JSON, or
2. by a relative fixture path.

Inline AST data is preferred for small tests.

### Semantic expectation

May include:

- resolved type,
- expected validation success,
- expected symbol information,
- or semantic diagnostic codes.

### Runtime expectation

```text
runtime
├── outcome: value | error
├── value?
├── valueType?
└── errorCode?
```

Special numeric values must use an explicit representation.

Examples:

```json
{ "category": "nan" }
```

```json
{ "category": "positive-infinity" }
```

```json
{
  "category": "finite",
  "decimal": "0",
  "negativeZero": true
}
```

### Diagnostic expectation

Diagnostics should be identified primarily by stable codes rather than exact
English wording.

```text
diagnostics
└── items[]
    ├── code
    ├── severity
    ├── range?
    └── messageContains?
```

---

## 6. Evidence Traceability

Each verified conformance test should reference:

- one or more research experiments,
- one or more consolidated evidence documents,
- and tested MonKey Office builds where known.

Example:

```json
{
  "evidence": {
    "level": "verified",
    "experiments": ["MO-081", "MO-082"],
    "documents": ["evidence/expressions/not-scope.md"],
    "builds": [249]
  }
}
```

A missing repository experiment may temporarily be referenced by historical ID,
but should be marked as unresolved until imported.

---

## 7. Host-Language Independence

Expected values must not depend on host-language defaults.

The format must explicitly preserve:

- `Na`,
- positive and negative infinity,
- positive and negative zero,
- exact string contents,
- Boolean values,
- and runtime errors.

Tests must not rely on JSON's unsupported `NaN` or `Infinity` tokens.

---

## 8. Comparison Modes

AST tests should declare a comparison mode:

```text
exact
structural
semantic
```

### `exact`

Compares every serialized field, including raw spellings and ranges.

### `structural`

Compares node structure and source-relevant distinctions while ignoring optional
metadata.

### `semantic`

Compares meaning while allowing non-semantic distinctions such as redundant
parentheses to be ignored.

The default should be `structural`.

---

## 9. Runtime Build Matrix

Observed behaviour may vary between MonKey Office builds.

A runtime result may therefore include:

```text
observations[]
├── build
├── platform
├── locale
├── outcome
└── notes?
```

The canonical expectation should represent the currently accepted specification.
Build-specific deviations belong in observations and may be classified as
regressions or known bugs.

---

## 10. File Layout

Recommended layout:

```text
tests/conformance/
├── README.md
├── schema.json
├── lexical/
├── expressions/
├── statements/
├── functions/
├── runtime/
└── examples/
```

Each test should live in one JSON file unless external fixtures are required.

Recommended filename:

```text
<lowercase-test-id>-<short-description>.json
```

Example:

```text
mo-cf-not-001-wide-not-scope.json
```

---

## 11. Validation Lifecycle

```text
Research experiment
        │
        ▼
Consolidated evidence
        │
        ▼
Draft conformance test
        │
        ▼
Schema validation
        │
        ▼
Implementation execution
        │
        ▼
Verified conformance result
```

A future build step should validate every test file against
`tests/conformance/schema.json`.

---

## 12. Initial Implementation Plan

1. Adopt the JSON Schema.
2. Add a conformance-file validator.
3. Convert verified expression behaviour into test files.
4. Add AST fixtures after the parser interface is stable.
5. Add runtime adapters for manually imported MonKey Office results.
6. Produce a build-by-build compatibility report.
