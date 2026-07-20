# DDD-0002: Evidence classification

- **Status:** Accepted
- **Date:** 2026-07-20

## Context

The repository combines official documentation, runtime experiments, logical
interpretation, and unresolved ideas. Without one shared vocabulary, equivalent
labels can acquire different meanings across evidence documents, registries,
specification text, and implementation work. That would make it unclear which
claims may support normative language rules.

## Decision

All claims about the MonKey Office scripting language use exactly one of four
evidence classes:

- `documented` — directly supported by an official MonKey Office source,
- `verified` — reproduced by a controlled experiment in the real interpreter,
- `inferred` — reasoned from documented or verified claims but not directly
  confirmed,
- `hypothesis` — a research idea awaiting documentation or experiment.

The complete definitions, traceability requirements, transitions, and handling
of contradictions are normative project rules in
[`model/evidence-classification.md`](../../model/evidence-classification.md).

Only `documented` and `verified` claims may directly support confirmed normative
language rules. `inferred` and `hypothesis` remain explicitly non-confirmed.

## Consequences

- Local evidence synonyms should be migrated to the four canonical identifiers.
- Structured registries and schemas should validate evidence classes against a
  shared source rather than duplicate divergent enumerations.
- Parser tests cannot by themselves count as verification of MonKey Office
  behaviour.
- Evidence may be promoted or demoted when its support changes, but the reason
  and historical references must remain traceable.
- Contradictory documentation and experiments are recorded explicitly instead
  of being resolved by implementation preference.
- A later sprint can add machine-readable validation without changing these
  semantics.
