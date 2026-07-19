# Semantic Analysis Model

> Status: Working design

## Purpose

Semantic analysis assigns meaning to the abstract syntax tree after parsing.

It is responsible for:

- declaration collection
- name resolution
- scope handling
- type checking
- function-call validation
- assignment validation
- semantic diagnostics

The semantic analyzer must not reinterpret syntax or depend on formatter output.

## Pipeline

```text
Source
  │
Lexer
  │
Tokens
  │
Parser
  │
AST
  │
Semantic analyzer
  │
Semantic model + diagnostics
```

## Semantic phases

Recommended order:

1. collect declarations
2. create scopes
3. resolve identifiers
4. infer or verify expression types
5. validate assignments
6. validate function calls
7. validate control-flow conditions
8. emit deterministic diagnostics

Separating phases avoids order-dependent behaviour and improves diagnostics.

## Symbol model

```text
Symbol
├── name
├── canonicalName
├── kind
├── declaredType
├── declarationRange
├── scope
└── metadata
```

Initial symbol kinds:

- variable
- built-in function
- host-provided value
- host-provided function

Names should preserve original spelling while using a canonical form for lookup.

## Case sensitivity

Identifier comparison is expected to be case-insensitive unless contrary evidence is
found.

Recommended canonicalization:

```text
Unicode-aware uppercase
```

Original spelling remains available for formatter and diagnostic output.

This rule is currently an implementation recommendation and must be aligned with
future evidence.

## Scope model

```text
Scope
├── kind
├── parent
├── symbols
└── sourceRange
```

Initial scope kinds:

- script
- branch
- expression

Only scopes demonstrated by the language should become normative.

Until block-local declaration behaviour is verified, script-level declarations
should be treated conservatively and implementation behaviour documented.

## Variable declarations

A declaration creates a variable symbol with:

- name
- declared type
- declaration location
- default value policy

Known syntax includes `dim`.

The semantic analyzer validates:

- duplicate declarations
- unsupported types
- invalid declaration names
- references before or without declaration

## Assignment

Known assignment syntax includes `set`.

Assignment validation checks:

- target resolves to a variable
- assigned expression is type-compatible
- target is writable
- special numeric values are accepted where the numeric type permits them

## Type system

The initial canonical types are:

- `number`
- `string`
- `boolean`
- `unknown`
- `error`

`unknown` represents information not yet available.

`error` prevents cascaded diagnostics after an earlier semantic failure.

The machine-readable type registry lives at:

```text
data/types/registry.json
```

## Number type

The numeric runtime model is IEEE-754 binary64.

The semantic type is `number`; runtime values may include:

- finite values
- positive zero
- negative zero
- positive infinity
- negative infinity
- NaN

Semantic analysis should not reject these values merely because they are
non-finite.

## String type

The string type supports verified string operations and functions.

Encoding and indexing behaviour remain evidence-driven.

## Boolean type

Boolean expressions are used by logical operators and conditions.

Verified logical behaviour includes:

- `AND` and `OR` share precedence
- evaluation is not short-circuited
- `NOT` has unusual wide-scope parsing

These are primarily parser/runtime rules, but semantic analysis must still require
boolean-compatible operands where supported by evidence.

## Type compatibility

Initial strict compatibility rule:

| Target | Source |
|---|---|
| number | number |
| string | string |
| boolean | boolean |

No implicit conversion should be assumed without evidence.

An implementation may carry an `unknown` type to continue analysis after unresolved
host values.

## Expressions

Each expression receives a semantic result:

```text
ExpressionInfo
├── type
├── constantValue
├── referencedSymbol
└── diagnostics
```

Constant evaluation is optional and must reproduce verified runtime semantics.

## Function calls

Function-call validation checks:

- function exists
- argument count
- argument types
- return type
- build compatibility

Function metadata should come from the existing function-data files rather than
being duplicated in parser code.

## Host environment

Bank-import scripts may depend on values or functions supplied by MonKey Office.

Host symbols must be represented separately from language-defined declarations.

Recommended metadata:

- name
- kind
- type
- availability by build
- evidence level
- mutability

Unknown host behaviour must not be silently treated as verified language behaviour.

## Diagnostics

Initial semantic diagnostics:

- `MO-SEM-0001`: unknown identifier
- `MO-SEM-0002`: duplicate declaration
- `MO-SEM-0003`: type mismatch

Future diagnostics should cover:

- invalid assignment target
- unsupported declared type
- wrong function arity
- invalid argument type
- unavailable host symbol

## Error suppression

When an expression has type `error`, parent expressions should usually avoid
emitting additional type-mismatch diagnostics caused solely by that error.

Independent errors must still be reported.

## Determinism

Semantic output must not depend on:

- dictionary iteration order
- filesystem order
- locale-sensitive sorting
- incidental traversal order

Diagnostics follow the project-wide diagnostic ordering rules.

## Semantic model API

Recommended result:

```text
SemanticResult
├── rootScope
├── symbols
├── expressionInfo
├── diagnostics
└── languageVersion
```

AST nodes should be addressable through stable node identifiers or object identity
within one analysis run.

## Testing

Semantic tests should cover:

- declaration and lookup
- duplicate declarations
- case handling
- assignment compatibility
- function arity
- function argument types
- host symbols
- error suppression
- deterministic diagnostics
- signed zero, infinity, and NaN
- non-short-circuit logical expressions

## Evidence status

This document combines:

- verified language behaviour
- implementation architecture
- conservative assumptions

Normative statements must eventually link to evidence or documented source
material. Unverified scope and conversion behaviour remains explicitly open.
