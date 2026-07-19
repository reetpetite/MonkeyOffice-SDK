# Semantic type data

The canonical semantic type registry is stored in:

- `registry.json`
- `schema.json`

Validate it with:

```bash
python tools/validate_types.py
```

The validator checks JSON Schema conformance and repository invariants:

- unique type identifiers
- deterministic canonical type ordering
- valid status values for language and analysis types
- no runtime model on internal analysis types
- presence of the required internal `unknown` and `error` types

The command exits with status `0` on success and `1` on invalid data.
Missing Python dependencies produce status `2`.
