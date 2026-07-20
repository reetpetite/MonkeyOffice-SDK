# Evidence classification model

The SDK separates the **source strength of a language claim** from the
**lifecycle state of an implementation artifact**.

## Canonical evidence levels

| Level | Meaning | Normative use |
|---|---|---|
| `documented` | Explicitly stated in an identified primary source | May enter the specification with a source trail; runtime behaviour remains unverified until tested |
| `verified` | Reproduced against the target MonKey Office build | May enter the specification with experiment and observation trail |
| `inferred` | Best explanation of existing evidence, but not directly established | Must be marked as inferred and should normally remain non-normative |
| `hypothesis` | Testable proposal with insufficient evidence | Must not be presented as language behaviour |

The order above is a classification order, not a claim that documentation is
stronger than experiment or vice versa. Documentation and experiments answer
different questions and may disagree. Such disagreements must be preserved and
investigated rather than silently resolved.

## Traceability

A registry entry carrying an evidence level must reference at least one path in
its `evidence` array. The path must exist in the repository. Consolidated files
under `evidence/` should identify their source documentation or the relevant
research experiment IDs.

The intended flow is:

```text
primary documentation ─┐
                       ├─> consolidated evidence ─> specification
runtime experiment ────┘
```

## Values outside this model

The following are not evidence levels:

- research workflow states such as `planned`, `testing`, and `inconclusive`;
- diagnostic lifecycle states such as `active` and `deprecated`;
- implementation-only markers for internal AST or analysis constructs;
- practical classifications such as `warning`, `recommendation`, and
  `known-bug`.

These concepts must use separate fields and vocabularies so that a lifecycle
state cannot be mistaken for evidence strength.
