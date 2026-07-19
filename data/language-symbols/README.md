# Language symbol registry

This directory contains the canonical machine-readable registry for language-level
keywords and operators.

Files:

- `registry.json` — registered symbols
- `schema.json` — JSON Schema for the registry

Validation:

```bash
python tools/validate_language_symbols.py
```

The validator checks:

- JSON Schema conformance
- unique IDs and canonical spellings
- deterministic ordering
- keyword/operator field consistency
- case canonicalization
- equal precedence and eager evaluation for `AND` and `OR`
- wide-scope precedence registration for `NOT`
- left associativity of the power operator

The registry intentionally starts with symbols whose behaviour is already
documented or verified. Additional symbols should only be added with evidence.
