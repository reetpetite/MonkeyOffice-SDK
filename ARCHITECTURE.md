# Project Architecture

> **Status:** Working architecture  
> **Scope:** Repository organization, evidence flow, generated artifacts, and planned language tooling

## 1. Purpose

The MonKeyOffice SDK is a specification-driven reverse-engineering project for
the scripting language used by MonKey Office bank-import definitions.

The repository is designed to keep four kinds of information separate:

1. raw experiments,
2. consolidated evidence,
3. normative language descriptions,
4. machine-readable models and generated documentation.

This separation is essential because observed runtime behaviour is not
automatically a language rule. A result first has to be reproduced, evaluated,
and assigned an evidence level before it may become part of the specification.

---

## 2. Architectural Principles

### 2.1 Evidence before specification

Normative statements should be backed by documented evidence. Experimental
observations remain in `research/`; consolidated conclusions belong in
`evidence/`; stable language rules belong in `spec/`.

### 2.2 Human-readable and machine-readable sources

Markdown documents explain behaviour to readers. Structured files under
`data/` describe functions in a form that can be validated and used to generate
reference documentation.

Generated documentation must not become an independent source of truth.

### 2.3 Reproducibility

A language claim should be reproducible with a minimal script, documented input,
expected output, observed output, and the tested MonKey Office build.

### 2.4 Incremental formalization

The project proceeds from observations to a formal grammar and AST. Parser,
validator, formatter, linter, and language-server work should depend on those
models instead of duplicating language rules.

### 2.5 Explicit uncertainty

Unknown or weakly supported behaviour must remain explicitly marked as
`inferred` or `hypothesis`. Missing knowledge must not be silently converted
into specification text.

---

## 3. Repository Map

```text
.
├── data/                 Machine-readable language and function metadata
├── docs/                 Project and contributor documentation
├── evidence/             Consolidated conclusions from experiments
├── model/                Shared formal models and classifications
├── research/             Reproducible reverse-engineering experiments
├── spec/                 Normative language specification
├── tests/                Validation and future conformance tests
├── tools/                Build, validation, import, and report tooling
├── README.md             Project entry point
├── SPRINTS.md            Development history and planned work
└── requirements.txt      Python dependencies
```

### `research/`

The laboratory of the project.

Each experiment should be independently understandable and should normally
contain:

```text
research/MO-NNN/
├── README.md or metadata
├── script.monkey
├── expected.*
├── observed.*
└── report-buildNNN.md
```

Exact filenames may evolve, but the experiment must preserve enough information
to repeat and assess the test.

Research files may contain incomplete interpretations. They are historical
records, not normative specification.

### `evidence/`

Contains consolidated findings derived from one or more experiments.

An evidence document should state:

- the conclusion,
- its evidence level,
- the affected language feature,
- supporting experiments,
- tested builds,
- unresolved questions,
- and known contradictions.

Evidence documents bridge the gap between raw experiments and normative rules.

### `spec/`

Contains the implementation-independent language specification.

The specification describes externally observable language behaviour, including:

- lexical structure,
- types and values,
- expressions,
- statements,
- functions,
- runtime behaviour,
- errors,
- and formal grammar.

The specification should not contain laboratory logs or unresolved guesses.

### `model/`

Contains formal structures used across the project.

Planned and current models include:

- evidence levels,
- AST node definitions,
- semantic classifications,
- source ranges,
- diagnostics,
- and conformance-test metadata.

### `data/`

Contains structured, validated descriptions of built-in functions and related
language entities.

These files are source data for generated reference documentation. Schema
validation belongs in the build pipeline.

### `docs/`

Contains project-level documentation that is neither raw evidence nor normative
language specification, for example:

- research workflow,
- contribution guidance,
- architecture,
- release process,
- and tooling documentation.

### `tests/`

Contains repository tests and, later, language conformance tests.

The intended structure is:

```text
tests/
├── schema/
├── tooling/
└── conformance/
    ├── lexical/
    ├── expressions/
    ├── statements/
    ├── functions/
    └── runtime/
```

### `tools/`

Contains deterministic project tooling such as:

- schema validation,
- research validation,
- experiment generation,
- result import,
- report generation,
- documentation generation,
- build comparison,
- and the top-level build runner.

---

## 4. Information Flow

```text
┌──────────────────────┐
│ MonKey Office runtime│
└──────────┬───────────┘
           │ execute controlled scripts
           ▼
┌──────────────────────┐
│ research/MO-NNN      │
│ raw observations     │
└──────────┬───────────┘
           │ reproduce, compare, interpret
           ▼
┌──────────────────────┐
│ evidence/            │
│ consolidated claims  │
└──────────┬───────────┘
           │ promote when sufficiently supported
           ▼
┌──────────────────────┐
│ spec/ and model/     │
│ normative rules      │
└──────────┬───────────┘
           │ implement
           ▼
┌────────────────────────────────────────┐
│ parser · validator · formatter · linter│
│ conformance suite · language server    │
└────────────────────────────────────────┘
```

The dependency direction is one-way. Later layers may cite earlier layers, but
research conclusions must not be rewritten merely to fit an implementation.

---

## 5. Evidence Model

Evidence strength and practical guidance are separate dimensions.

### Evidence levels

| Level | Meaning |
|---|---|
| `documented` | Described by an official or vendor-provided source |
| `verified` | Reproduced by controlled experiments |
| `inferred` | Best explanation of observations, not yet directly isolated |
| `hypothesis` | Proposed behaviour awaiting sufficient testing |

### Practical classifications

| Classification | Meaning |
|---|---|
| `recommendation` | Preferred authoring practice |
| `warning` | Behaviour likely to surprise or cause fragile scripts |
| `known-bug` | Behaviour considered an implementation defect |

A rule may therefore be both `verified` and a `warning`, or `documented` and a
`known-bug`.

---

## 6. Specification Boundaries

The specification describes observable language semantics, not presumed internal
implementation details.

For example, evidence may strongly indicate IEEE-754 binary64 arithmetic. The
specification may define the resulting numeric behaviour where verified, while
an internal implementation claim such as “the runtime uses a C `double`” would
remain out of scope unless independently established.

The following terms are used intentionally:

- **normative** — defines required language behaviour,
- **informative** — explains or illustrates a rule,
- **implementation note** — records a useful non-normative observation,
- **open question** — identifies behaviour not yet specified.

---

## 7. AST and Grammar

The AST is the shared semantic representation for future tools.

Initial root:

```text
Program
└── statements: Statement[]
```

Initial expression nodes:

```text
Expression
├── NumberLiteral
├── StringLiteral
├── BooleanLiteral
├── IdentifierExpression
├── FunctionCallExpression
├── UnaryExpression
├── BinaryExpression
└── ParenthesizedExpression
```

The grammar determines how source text becomes this AST. Unusual parsing
behaviour, such as the verified scope of `NOT`, belongs in the parser and grammar
rules; the resulting AST may still represent `NOT` as a unary expression.

Grammar, AST, specification prose, and conformance tests must ultimately agree.
CI should detect divergence where practical.

---

## 8. Build Architecture

`tools/build.py` is the repository-level entry point.

A successful build should run the available deterministic checks in a stable
order, including:

1. structured-data validation,
2. research validation,
3. generated-documentation updates or checks,
4. experiment/report consistency checks,
5. future grammar and conformance validation.

The build must fail on invalid source data or inconsistent required artifacts.
Warnings should remain visible without hiding build failures.

Typical local workflow:

```bash
source .venv/bin/activate
python tools/build.py
```

Generated files should be reproducible from versioned inputs.

---

## 9. Planned Tooling Layers

```text
Source text
    │
    ▼
Lexer
    │ tokens
    ▼
Parser
    │ AST
    ├──────────────► Formatter
    │
    ▼
Semantic validator
    │ diagnostics
    ├──────────────► Linter
    ├──────────────► Editor integration
    └──────────────► Language server
```

### Lexer

Produces tokens and source ranges while preserving enough information for useful
diagnostics and formatting.

### Parser

Applies the formal grammar and creates the AST. It must reproduce verified
precedence, associativity, and scope behaviour.

### Semantic validator

Checks names, argument counts, operand types, and other rules not fully captured
by syntax.

### Formatter

Produces stable source formatting without changing semantics. Parentheses may be
required where the language's unusual precedence rules would otherwise be
unclear.

### Linter

Reports valid but risky constructs, known runtime traps, portability concerns,
and project recommendations.

### Language server

Combines parsing, validation, function metadata, and source locations to provide
diagnostics, completion, hover information, and navigation.

---

## 10. Change Policy

A change belongs in:

- `research/` when it adds or refines an experiment,
- `evidence/` when it consolidates observations,
- `spec/` when it defines language behaviour,
- `model/` when it changes a shared formal representation,
- `data/` when it changes structured language metadata,
- `docs/` when it explains project operation,
- `tools/` when it automates a deterministic workflow.

A single commit may touch several layers when promoting a completed finding, but
the relationship between those changes should remain explicit.

---

## 11. Architectural Roadmap

1. Complete the expression specification.
2. Consolidate existing expression evidence.
3. Define the AST schema in detail.
4. Expand the EBNF to all known statements and declarations.
5. Introduce conformance-test metadata.
6. Implement a lexer and parser against the specification.
7. Add semantic validation and diagnostics.
8. Build formatter, linter, and language-server functionality.

The architecture is intentionally designed so that useful specification and
research work can continue before the parser exists.
