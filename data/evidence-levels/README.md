# Evidence levels

`registry.json` is the canonical machine-readable vocabulary for evidence
strength used by language claims in the SDK.

The four levels are deliberately not a maturity progression. `documented` and
`verified` describe different sources of knowledge: vendor documentation and
runtime experiments. A claim can therefore be documented without being
experimentally verified.

The cross-registry validator checks that language-symbol, operator, and
statement registries use only these values and that every referenced evidence
path exists.

```bash
python tools/validate_evidence.py
```

Lifecycle values such as diagnostic `active`/`deprecated` and internal
implementation markers are not evidence levels.
