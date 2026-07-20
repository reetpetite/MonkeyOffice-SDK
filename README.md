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
runner/         Human-operated interpreter execution harness
tools/          Build and research tooling
```

The repository intentionally separates research, evidence, specification, and
implementation concerns:

| Directory | Purpose |
|-----------|---------|
| `research/` | Experimental work and raw observations |
| `evidence/` | Consolidated conclusions derived from documentation and experiments |
| `spec/` | Normative, implementation-independent language specification |
| `model/` and `data/` | Shared formal and machine-readable representations |
| `runner/` | Build-specific execution manifests, observation templates, and reports |
| `tools/` | Reference implementations and deterministic project tooling |

The authoritative dependency direction is:

```text
research and official documentation
                ↓
             evidence
                ↓
       specification and models
                ↓
 reference implementation and tests
```

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the repository boundaries and
[`docs/design-decisions/`](docs/design-decisions/) for recorded design decisions.
The project-wide evidence classes are defined in
[`model/evidence-classification.md`](model/evidence-classification.md).

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
Machine-readable relationships between experiments, evidence records, and specification rules are maintained in [`registry/`](registry/README.md) and checked during every build.

Interpreter experiments follow [`research/experiment-protocol.md`](research/experiment-protocol.md). Unresolved questions are tracked in [`research/open-questions.md`](research/open-questions.md). The declaration probe matrices are executed and recorded through the human-operated [`runner/`](runner/README.md) harness.

---

## Repository Principles

1. **Evidence precedes specification.** Language claims originate in official
   documentation or reproducible observations.
2. **The specification is implementation-independent.** Parser behaviour does
   not become normative merely because the reference parser implements it.
3. **Uncertainty stays explicit.** Unsupported behaviour remains an open
   question, inference, or hypothesis rather than silently entering code.
4. **Generated artifacts are not sources of truth.** They must be reproducible
   from versioned source data.
5. **Changes remain traceable.** Grammar, models, registries, tests, and tools
   should identify the evidence or specification rule they implement.

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

### Erste Interpreter-Testmatrix

Die Experimente `MO-030` bis `MO-033` untersuchen isoliert grundlegende `DIM`-Formen, Groß-/Kleinschreibung, Initialisierung mit `SET` sowie Leerraum. Jeder potenziell fehlschlagende Syntaxfall besitzt ein eigenes ausführbares MonKey-Office-Skript.


### Build-specific declaration test execution

Sprint 29 adds a human-operated execution harness for `MO-030` through `MO-033`. It initializes explicit `not-run` observations, records one manually observed case at a time, generates deterministic reports, and validates partial as well as complete build-specific result sets.
