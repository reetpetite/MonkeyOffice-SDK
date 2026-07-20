# DDD-0005: Machine-readable evidence graph

**Status:** accepted

## Context

Experiments, consolidated evidence, and normative specification documents were
stored separately, but their relationships were not machine-checkable. This
made it possible for a specification statement to lose its research origin or
for an evidence record to reference a nonexistent experiment case.

## Decision

The repository maintains three small registries under `registry/`:

1. experiments and their source files,
2. atomic evidence records,
3. specification rules and their supporting evidence.

Permanent identifiers use the forms `MO-NNN`, `EVD-NNNN`, and
`SPEC-TOPIC-NNN`. Evidence records contain one concise statement and identify
the experiment build and cases from which the statement was derived.

`tools/validate_evidence_graph.py` verifies identifiers, repository-local
paths, experiment cases, evidence classifications, and all graph edges. The
validator is part of the normal build.

## Consequences

- Every registered specification rule has a machine-checkable research trail.
- Missing and stale references fail the build.
- Contradictory evidence can later be represented without overwriting earlier
  observations.
- Existing prose evidence can be migrated incrementally rather than all at once.
