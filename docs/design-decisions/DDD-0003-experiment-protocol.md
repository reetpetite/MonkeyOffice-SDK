# DDD-0003: Reproducible interpreter experiments

- **Status:** Accepted
- **Date:** 2026-07-20

## Context

The project is approaching direct tests in MonKey Office to determine syntax and
runtime behaviour. Existing experiments already use structured definitions and
build-specific observations, but the repository needs one explicit protocol for
pre-execution expectations, raw observations, safety, environment metadata, and
promotion into evidence. Without it, experiments can become difficult to
reproduce or can overstate what one test established.

## Decision

Experiments in the real MonKey Office interpreter follow the protocol in
[`research/experiment-protocol.md`](../../research/experiment-protocol.md).

Each experiment:

- has a permanent `MO-NNN` identifier,
- answers one narrowly scoped, falsifiable question,
- versions the exact executed script,
- records the expected outcome before execution,
- preserves raw output for a named MonKey Office build,
- records relevant environment and safety constraints,
- separates observation from interpretation,
- links unresolved follow-up questions in
  [`research/open-questions.md`](../../research/open-questions.md).

Experiments establish observations for the tested environment. Promotion to
confirmed evidence and specification requires a separate review step.

## Consequences

- Early language-understanding tests can be small, comparable, and repeatable.
- A rejected script or runtime error remains a useful observation when captured
  exactly.
- Expectations are traceable and cannot be rewritten after seeing the result.
- Build- or locale-specific behaviour remains explicitly scoped.
- Existing experiments may be migrated incrementally; this decision does not
  invalidate older structured observations.
- Future tooling may validate required metadata and generate experiment folders,
  but automation must preserve the human-reviewable source files.
