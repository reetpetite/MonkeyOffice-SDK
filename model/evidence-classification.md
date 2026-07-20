# Evidence Classification

> **Status:** Normative project model  
> **Scope:** Classification of claims about the MonKey Office scripting language

## 1. Purpose

This model defines the only evidence classes used for language claims in the
repository. The class describes how strongly a claim is supported; it does not
describe how important, complete, or broadly applicable the claim is.

A claim must use exactly one of these identifiers:

```text
documented
verified
inferred
hypothesis
```

## 2. Classes

### `documented`

The claim is stated by an official MonKey Office source applicable to the
feature being described.

Required traceability:

- source title or identifier,
- source location such as page, section, or heading,
- relevant MonKey Office version or publication date when known,
- a faithful paraphrase or a copyright-compliant excerpt.

Official documentation can be incomplete or ambiguous. A documented claim must
not be broadened beyond what the source actually supports.

**Normative use:** allowed.

### `verified`

The claim has been reproduced in the real MonKey Office interpreter by a
controlled experiment.

Required traceability:

- experiment identifier,
- exact script and relevant input,
- observed compiler or runtime result,
- tested MonKey Office version and build,
- enough procedure detail to repeat the experiment.

A single successful example verifies only the behaviour it actually exercises.
Generalization beyond the tested cases requires further experiments or remains
an inference.

**Normative use:** allowed.

### `inferred`

The claim is a reasoned conclusion derived from one or more `documented` or
`verified` claims, but is not itself directly stated or experimentally tested.

Required traceability:

- supporting claim or evidence references,
- the reasoning connecting them to the inference,
- the untested boundary or assumption.

An inference remains visibly marked. It must not be presented as confirmed
syntax or runtime behaviour.

**Normative use:** not as a confirmed rule. It may appear in explicitly
provisional or informative material.

### `hypothesis`

The claim is a plausible idea that still requires documentary support or a
controlled experiment.

Required traceability:

- the question being investigated,
- motivation for the hypothesis,
- a proposed way to test or resolve it when practical.

A hypothesis may guide research, but it must not constrain the grammar, AST,
parser, validator, or conformance suite as supported behaviour.

**Normative use:** prohibited.

## 3. Promotion and Demotion

Evidence classes are not quality scores and do not form a simple linear ladder.
The following transitions are valid when new information is recorded:

```text
hypothesis ──experiment──▶ verified
hypothesis ─documentation▶ documented
inferred   ──experiment──▶ verified
inferred   ─documentation▶ documented
```

Claims may also be demoted when their support is found to be insufficient,
version-specific, ambiguous, or contradicted. A change of class must preserve
historical references and explain why the classification changed.

`documented` and `verified` are independent forms of support. When both apply,
the claim should retain one primary class and cite the other support as
corroboration rather than inventing a fifth class.

## 4. Contradictions

Contradictory evidence is preserved rather than averaged away.

When official documentation and observed runtime behaviour disagree, the record
must identify:

- the exact documented statement,
- the exact experiment and build,
- the scope of the disagreement,
- whether version differences could explain it,
- and the unresolved status.

No implementation choice resolves an evidence contradiction by itself.

## 5. Minimum Claim Metadata

A structured evidence record should provide at least:

- a stable claim identifier,
- a concise claim,
- one evidence class,
- affected language feature or scope,
- source or experiment references,
- applicable MonKey Office version/build when known,
- known limitations or contradictions,
- and the date of the latest assessment.

The detailed storage schema may evolve independently, but it must preserve these
semantics.

## 6. Repository Rules

1. Only the four identifiers defined here are project-wide evidence classes.
2. Registries and schemas should reference these identifiers rather than create
   local synonyms such as `confirmed`, `experimental`, or `assumed`.
3. A parser test proves reference-implementation behaviour, not MonKey Office
   behaviour. It cannot by itself create `verified` evidence.
4. A generated document inherits the evidence of its source data and is never a
   new evidence source.
5. Unknown behaviour remains unknown; absence of a contradiction is not
   verification.
