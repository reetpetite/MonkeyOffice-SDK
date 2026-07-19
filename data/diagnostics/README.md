# Diagnostic data

The canonical diagnostic registry is stored in:

- `registry.json`
- `schema.json`

Validate it with:

```bash
python tools/validate_diagnostics.py
```

The validator checks both JSON Schema conformance and repository invariants:

- unique diagnostic codes
- prefix/phase consistency
- deterministic code ordering
- lifecycle-field consistency
- existing documentation targets

The command exits with status `0` on success and `1` on invalid data.
Missing Python dependencies produce status `2`.
