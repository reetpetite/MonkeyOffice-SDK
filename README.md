# MonKeyOffice SDK

> A community-driven reverse engineering project documenting the MonKey Office
> Bankimport scripting language.

## Project Goals

The MonKeyOffice SDK aims to provide a precise, implementation-independent
description of the scripting language used by the MonKey Office Bankimport
engine.

The long-term objective is to build a complete language ecosystem consisting of

- a formal language specification,
- an abstract syntax tree (AST),
- a parser,
- validation tools,
- a formatter,
- a linter,
- and, eventually, language-server support.

This project is **not** affiliated with the original software vendor.

---

## Repository Structure

```
data/           Function metadata
docs/           Project documentation
evidence/       Consolidated research results
model/          Language models (AST, evidence model, ...)
research/       Individual experiments
spec/           Formal language specification
tests/          Conformance tests
tools/          Build and research tooling
```

The repository intentionally separates three different concerns:

| Directory | Purpose |
|-----------|---------|
| `research/` | Experimental work and raw observations |
| `evidence/` | Consolidated conclusions derived from experiments |
| `spec/` | Normative language specification |

---

## Research Workflow

```
Experiment
      │
      ▼
Observation
      │
      ▼
Evidence
      │
      ▼
Language Specification
      │
      ▼
Future Parser / Tooling
```

Experiments never become part of the specification directly.
Every normative statement should be supported by documented evidence.

---

## Current Status

Current work includes research on

- expression parsing
- operator precedence
- logical expressions
- string handling
- floating-point behaviour
- IEEE-754 edge cases
- runtime behaviour

The project is still under active reverse engineering.

---

## Building

Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python tools/build.py
```

---

## Contributing

Contributions are welcome.

Please prefer small, reproducible experiments over undocumented assumptions.

Every new language feature should ideally follow this lifecycle:

1. Research experiment
2. Observation
3. Evidence
4. Specification

---

## License

See the repository license.
