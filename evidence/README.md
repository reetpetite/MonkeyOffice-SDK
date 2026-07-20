# Consolidated Evidence

This directory contains consolidated support for language claims. Sources may
be reproducible experiments, identified primary documentation, or both.

Evidence documents are not raw laboratory notes and are not themselves the
normative language specification. They form the traceable bridge between
`research/` or primary documentation and `spec/`.

## Evidence levels

The canonical definitions are maintained in
[`data/evidence-levels/registry.json`](../data/evidence-levels/registry.json)
and explained in
[`model/evidence-classification.md`](../model/evidence-classification.md).

- `documented` — explicitly stated in an identified primary source
- `verified` — confirmed by a reproducible experiment against the target build
- `inferred` — supported but not directly established
- `hypothesis` — testable proposal without sufficient evidence

`documented` and `verified` are different source classes, not interchangeable
maturity stages. A documented claim may still require runtime verification.

## Practical classifications

- `recommendation`
- `warning`
- `known-bug`

Evidence strength and practical classification are independent.

## Validation

Registry evidence references are checked for valid levels and existing paths:

```bash
python tools/validate_evidence.py
```

## Current evidence

- [`expressions/operator-precedence.md`](expressions/operator-precedence.md)
- [`expressions/logical-operators.md`](expressions/logical-operators.md)
- [`expressions/not-scope.md`](expressions/not-scope.md)
- [`runtime/numeric-model.md`](runtime/numeric-model.md)
- [`runtime/special-numeric-values.md`](runtime/special-numeric-values.md)
- [`statements/dim-set.md`](statements/dim-set.md)
