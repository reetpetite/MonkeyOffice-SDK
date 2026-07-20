# DDD-0001: Repository architecture and dependency direction

- **Status:** Accepted
- **Date:** 2026-07-20

## Context

The SDK combines vendor documentation, reverse-engineering experiments,
consolidated evidence, a normative specification, machine-readable models, and
reference tools. Without explicit boundaries, assumptions made in a parser or
test can accidentally become treated as language facts. Raw observations can
also be confused with stable conclusions.

## Decision

The repository follows this authoritative dependency direction:

```text
official documentation and research observations
                      ↓
                   evidence
                      ↓
          specification and shared models
                      ↓
       reference implementations and tests
```

The layers have distinct responsibilities:

- `research/` preserves reproducible experiments and raw observations.
- `evidence/` consolidates supported claims and unresolved contradictions.
- `spec/` defines externally observable language behaviour without depending on
  implementation details.
- `model/` and `data/` provide shared formal and machine-readable
  representations derived from supported rules.
- `tools/` and `tests/` implement and check those rules; they are not normative
  sources.
- `docs/` explains repository operation and architecture.

A disagreement between layers is resolved by revisiting the earliest relevant
source. Implementation convenience must not determine a language claim.

## Consequences

- New language features require traceable documentation or evidence before they
  become normative or are implemented as supported behaviour.
- Parser and tokenizer code may remain provisional where the specification is
  incomplete.
- Generated documentation must be reproducible and must not become an
  independent source of truth.
- Cross-layer changes are allowed when they promote one supported finding, but
  the relationship between evidence, specification, model, tests, and code must
  remain visible.
- Future architecture changes require a new decision record rather than editing
  the historical rationale silently.
