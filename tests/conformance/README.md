# Conformance Tests

This directory contains machine-readable tests for the documented MonKey Office
language behaviour.

The test format is defined by:

- [`../../model/conformance-test.md`](../../model/conformance-test.md)
- [`schema.json`](schema.json)

## Current status

The format is a working draft. The example files demonstrate the intended
structure but are not yet executed by `tools/build.py`.

## Principles

- Every verified expected result should be traceable to evidence.
- Special numeric values must use explicit JSON-safe representations.
- Tests should be small and isolate one behaviour.
- Exact source text must be preserved.
- Build-specific observations must not silently replace the canonical
  specification expectation.

## Planned directories

```text
lexical/
expressions/
statements/
functions/
runtime/
examples/
```

## Validation

A future tool will validate all conformance files against `schema.json` and will
be added to the normal build pipeline.
