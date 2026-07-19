# Conformance Tests

This directory contains machine-readable tests for the documented MonKey Office
language behaviour.

The test format is defined by:

- [`../../model/conformance-test.md`](../../model/conformance-test.md)
- [`schema.json`](schema.json)

## Current status

The format is a working draft. The example files demonstrate the intended
structure and are validated by `tools/validate_conformance.py`.

They are not yet executed by a parser or runtime adapter.

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

Run:

```bash
python tools/validate_conformance.py
```

The validator:

1. validates `schema.json` itself as JSON Schema Draft 2020-12,
2. validates every other JSON file below `tests/conformance/`,
3. checks referenced evidence documents,
4. checks referenced external AST fixtures,
5. enforces selected cross-field consistency rules,
6. exits with a non-zero status when validation fails.

The files are processed in deterministic path order.

## Build integration

Until the repository build runner invokes the validator directly, use:

```bash
python tools/build.py
python tools/validate_conformance.py
```

A later sprint will add this validator to the normal build pipeline after the
existing `tools/build.py` orchestration has been reviewed.
