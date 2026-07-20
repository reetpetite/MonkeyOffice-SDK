# DDD-0006 — Human-operated interpreter execution harness

- **Status:** accepted
- **Date:** 2026-07-20

## Context

The declaration probe matrices contain isolated scripts, but manually executing
and transcribing them without a controlled result format risks missing cases,
normalizing error messages, confusing expected and observed behaviour, and
losing build-specific metadata.

Direct automation of the proprietary MonKey Office user interface is outside
the repository's current scope and could make observations less transparent.

## Decision

The repository provides a human-operated execution harness consisting of:

1. a manifest declaring experiments, cases, scripts, and build-specific output
   locations;
2. a command-line recorder that initializes observations and records one case
   at a time only after manual execution;
3. deterministic Markdown report generation;
4. validation of manifests and any recorded result files.

Every case begins with `not-run`. Expectations are never copied into result
files as observations. Accepted cases must preserve their unique success signal;
skipped cases must include a reason. Completion is calculated from case status
rather than asserted independently.

## Consequences

- Execution remains manual and auditable while transcription becomes uniform.
- Partial test sessions can be committed without being mistaken for complete
  evidence.
- Build-specific results can coexist without overwriting previous observations.
- The harness does not itself establish evidence; observations still require
  review and promotion through the evidence model.
- Changes to case files must be reflected in the execution manifest and pass
  validation.
