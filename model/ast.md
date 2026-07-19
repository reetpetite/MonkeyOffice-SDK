# Abstract Syntax Tree

> **Status:** Working model  
> **Scope:** Parser output, source locations, node invariants, and future tooling interfaces

## 1. Purpose

The abstract syntax tree (AST) is the canonical structural representation of a
parsed MonKey Office script.

It is intended to serve as the shared input for:

- semantic validation,
- diagnostics,
- formatting,
- linting,
- conformance testing,
- documentation tooling,
- and future language-server functionality.

The AST describes program structure, not concrete source formatting. Whitespace,
comments, and exact token spelling belong to the concrete syntax layer unless a
future formatter requires them to be preserved separately.

---

## 2. Design Principles

### 2.1 Stable semantic representation

Parser implementation details must not leak into the AST. Different parsers
should be able to produce equivalent trees for the same source program.

### 2.2 Explicit source ranges

Every node should carry a source range so that diagnostics and editor features
can point to the corresponding source text.

### 2.3 No implicit precedence in consumers

Precedence and associativity are resolved by the parser. AST consumers must not
need to re-parse operator order.

For example:

```text
1 + 2 * 3
```

is represented as:

```text
BinaryExpression(+)
├── NumberLiteral(1)
└── BinaryExpression(*)
    ├── NumberLiteral(2)
    └── NumberLiteral(3)
```

### 2.4 Parentheses remain observable

Parentheses may be semantically redundant, but they are relevant for:

- preserving author intent,
- explaining unusual precedence,
- formatting,
- and the scope of `NOT`.

Therefore parenthesized expressions are represented explicitly.

### 2.5 Unknown syntax is not guessed

The AST model should grow only when syntax has been documented or sufficiently
verified. Provisional nodes must be clearly marked.

---

## 3. Common Node Structure

All nodes share a common base structure.

```text
Node
├── kind: NodeKind
├── range: SourceRange
└── metadata: NodeMetadata?
```

### `kind`

A stable discriminator identifying the concrete node type.

Examples:

```text
Program
NumberLiteral
BinaryExpression
FunctionCallExpression
```

### `range`

The half-open source range occupied by the node.

```text
SourceRange
├── start: SourcePosition
└── end: SourcePosition
```

```text
SourcePosition
├── offset: integer
├── line: integer
└── column: integer
```

Recommended conventions:

- `offset` is zero-based and measured in Unicode code points or bytes; the
  implementation must choose one convention and document it.
- `line` is one-based.
- `column` is one-based.
- `end` points immediately after the final character of the node.

A future machine-readable schema must select one precise offset convention.

### `metadata`

Optional non-semantic information attached by tooling.

Examples:

- parser recovery state,
- originating token references,
- evidence/debug information,
- implementation-specific annotations.

Consumers must not require metadata for normal semantic processing.

---

## 4. AST Root

## `Program`

Represents one complete script.

```text
Program
├── kind: "Program"
├── range: SourceRange
└── statements: Statement[]
```

### Invariants

- `statements` preserves source order.
- The range covers the complete parsed input.
- An empty script is represented by an empty `statements` array.
- Parser recovery nodes, if introduced later, must be explicitly typed.

---

## 5. Abstract Categories

The AST currently distinguishes two major abstract categories.

```text
Node
├── Program
├── Statement
└── Expression
```

### `Statement`

A construct evaluated for control flow, declaration, assignment, or side effects.

The complete statement hierarchy remains provisional until all statement forms
have been documented.

### `Expression`

A construct that evaluates to a value.

Current expression hierarchy:

```text
Expression
├── NumberLiteral
├── StringLiteral
├── BooleanLiteral
├── IdentifierExpression
├── FunctionCallExpression
├── UnaryExpression
├── BinaryExpression
└── ParenthesizedExpression
```

---

## 6. Literal Expressions

## `NumberLiteral`

Represents a numeric literal as written in source.

```text
NumberLiteral
├── kind: "NumberLiteral"
├── range: SourceRange
├── raw: string
└── value: number
```

### Fields

- `raw` preserves the original source spelling.
- `value` contains the parsed runtime value.

### Invariants

- `raw` is not normalized.
- `value` reflects the verified parser rounding behaviour.
- A machine-readable representation must be able to preserve:
  - finite binary64 values,
  - positive zero,
  - negative zero,
  - positive infinity,
  - negative infinity,
  - and `Na`.

Because JSON cannot represent all of these values directly, serialized ASTs
should use an explicit numeric-value representation rather than plain JSON
numbers.

Recommended model:

```text
NumericValue
├── category: "finite" | "positive-infinity" | "negative-infinity" | "nan"
├── decimal?: string
└── negativeZero?: boolean
```

The exact schema remains to be finalized.

---

## `StringLiteral`

Represents a string literal.

```text
StringLiteral
├── kind: "StringLiteral"
├── range: SourceRange
├── raw: string
└── value: string
```

### Fields

- `raw` preserves delimiters and source spelling.
- `value` contains the decoded runtime string.

### Open questions

- escape syntax,
- delimiter rules,
- multiline behaviour,
- source encoding edge cases.

These details must remain unspecified until supported by evidence.

---

## `BooleanLiteral`

Represents a Boolean literal.

```text
BooleanLiteral
├── kind: "BooleanLiteral"
├── range: SourceRange
├── raw: string
└── value: boolean
```

### Invariants

- `value` is exactly `true` or `false`.
- `raw` preserves the spelling used in source.

---

## 7. Name and Call Expressions

## `IdentifierExpression`

Represents a reference to a named variable or other named runtime entity.

```text
IdentifierExpression
├── kind: "IdentifierExpression"
├── range: SourceRange
└── name: string
```

### Invariants

- `name` preserves source spelling unless identifier case normalization is later
  proven to be part of the language.
- Name resolution is not performed by the parser.
- Whether the identifier exists is determined during semantic validation or at
  runtime.

---

## `FunctionCallExpression`

Represents a function invocation.

```text
FunctionCallExpression
├── kind: "FunctionCallExpression"
├── range: SourceRange
├── callee: IdentifierExpression
└── arguments: Expression[]
```

### Invariants

- Arguments preserve source order.
- The parser does not determine whether the function exists.
- Arity and argument-type checks belong to semantic validation.
- Evaluation order must be documented in the language specification before
  consumers rely on it.

Example:

```text
Left("abcdef", 3)
```

```text
FunctionCallExpression
├── callee: IdentifierExpression("Left")
└── arguments
    ├── StringLiteral("abcdef")
    └── NumberLiteral(3)
```

---

## 8. Unary Expressions

## `UnaryExpression`

Represents an expression with one operand.

```text
UnaryExpression
├── kind: "UnaryExpression"
├── range: SourceRange
├── operator: UnaryOperator
└── operand: Expression
```

Initial operator model:

```text
UnaryOperator
└── "NOT"
```

Unary minus is intentionally not included until its grammar and interaction with
power expressions have been verified.

### `NOT` invariant

`NOT` remains a unary AST node even though its parser scope is unusual.

For source equivalent to:

```text
NOT (1 = 1 OR TRUE)
```

the resulting tree is:

```text
UnaryExpression(NOT)
└── BinaryExpression(OR)
    ├── BinaryExpression(=)
    │   ├── NumberLiteral(1)
    │   └── NumberLiteral(1)
    └── BooleanLiteral(TRUE)
```

The parser is responsible for selecting the complete operand. AST consumers
should treat the resulting node as an ordinary unary expression.

---

## 9. Binary Expressions

## `BinaryExpression`

Represents an expression with a left and right operand.

```text
BinaryExpression
├── kind: "BinaryExpression"
├── range: SourceRange
├── operator: BinaryOperator
├── left: Expression
└── right: Expression
```

Initial operator set:

```text
BinaryOperator
├── "^"
├── "*"
├── "/"
├── "+"
├── "-"
├── "="
├── "<>"
├── "<"
├── "<="
├── ">"
├── ">="
├── "AND"
└── "OR"
```

### Invariants

- Precedence is already reflected by tree nesting.
- Associativity is already reflected by tree nesting.
- Operators preserve their semantic category.
- No short-circuit behaviour may be inferred from the tree alone; evaluation
  rules belong to the runtime specification.

### Left associativity

Source:

```text
8 / 4 / 2
```

Tree:

```text
BinaryExpression(/)
├── BinaryExpression(/)
│   ├── NumberLiteral(8)
│   └── NumberLiteral(4)
└── NumberLiteral(2)
```

### Equal precedence of `AND` and `OR`

Source:

```text
TRUE OR FALSE AND FALSE
```

With equal precedence and left associativity:

```text
BinaryExpression(AND)
├── BinaryExpression(OR)
│   ├── BooleanLiteral(TRUE)
│   └── BooleanLiteral(FALSE)
└── BooleanLiteral(FALSE)
```

This is intentionally different from languages in which `AND` binds more
strongly than `OR`.

---

## 10. Parenthesized Expressions

## `ParenthesizedExpression`

Represents an expression explicitly enclosed in parentheses.

```text
ParenthesizedExpression
├── kind: "ParenthesizedExpression"
├── range: SourceRange
└── expression: Expression
```

### Invariants

- The range includes both parentheses.
- The child range excludes the parentheses.
- Nested parentheses produce nested nodes.
- Consumers performing semantic evaluation may normally delegate to the child.
- Formatters and diagnostics should preserve or deliberately account for the
  explicit grouping.

Example:

```text
(1 + 2) * 3
```

```text
BinaryExpression(*)
├── ParenthesizedExpression
│   └── BinaryExpression(+)
│       ├── NumberLiteral(1)
│       └── NumberLiteral(2)
└── NumberLiteral(3)
```

---

## 11. Provisional Statement Model

Statement syntax is not yet sufficiently consolidated for a complete hierarchy.

The initial target model is:

```text
Statement
├── VariableDeclaration
├── AssignmentStatement
├── ExpressionStatement
└── ConditionalStatement?
```

Only nodes supported by documented syntax should be added to a machine-readable
schema.

### `VariableDeclaration`

Provisional structure:

```text
VariableDeclaration
├── kind: "VariableDeclaration"
├── range: SourceRange
├── name: string
├── declaredType: TypeReference?
└── initializer: Expression?
```

This node is expected to represent `dim` declarations, but exact grammar,
multiple-declaration behaviour, and type syntax must be specified first.

### `AssignmentStatement`

Provisional structure:

```text
AssignmentStatement
├── kind: "AssignmentStatement"
├── range: SourceRange
├── target: IdentifierExpression
└── value: Expression
```

This node is expected to represent `set` assignments.

### `ExpressionStatement`

Provisional structure:

```text
ExpressionStatement
├── kind: "ExpressionStatement"
├── range: SourceRange
└── expression: Expression
```

Whether all function calls or bare expressions are valid as statements remains
to be verified.

---

## 12. Type References

AST syntax types and runtime value types are distinct concepts.

A future `TypeReference` node may represent an explicitly written type:

```text
TypeReference
├── kind: "TypeReference"
├── range: SourceRange
└── name: string
```

Runtime type information should not be written into the parser AST unless it is
produced by a separate semantic-analysis phase.

Recommended separation:

```text
Parsed AST
    │
    ▼
Semantic analysis
    │
    ├── symbol table
    ├── inferred/resolved types
    └── diagnostics
```

---

## 13. Diagnostics and Recovery

The initial parser should prefer precise failure over silently invented syntax.

A later error-tolerant parser may introduce:

```text
InvalidExpression
InvalidStatement
MissingToken
```

Recovery nodes must:

- carry a source range,
- preserve enough information for diagnostics,
- never be mistaken for valid semantic nodes,
- and remain excluded from normative runtime evaluation.

Diagnostics should be separate objects:

```text
Diagnostic
├── severity: "error" | "warning" | "information"
├── code: string
├── message: string
├── range: SourceRange
└── relatedInformation: RelatedInformation[]
```

---

## 14. AST Equality

Two ASTs are structurally equivalent when:

- node kinds match,
- semantic fields match,
- child order matches,
- operators match,
- and literal values match.

The following may be ignored for semantic equality:

- source ranges,
- parser metadata,
- raw literal spelling,
- redundant parenthesized nodes, depending on the comparison mode.

Recommended comparison modes:

```text
exact
structural
semantic
```

### `exact`

Compares all fields.

### `structural`

Ignores metadata but preserves explicit parentheses and raw spellings.

### `semantic`

Ignores source-only distinctions that do not change runtime meaning.

The conformance suite should state which comparison mode each test uses.

---

## 15. Serialization

A future machine-readable AST schema should support deterministic JSON
serialization.

Requirements:

- stable `kind` discriminators,
- explicit source ranges,
- ordered child arrays,
- safe representation of non-finite numbers and negative zero,
- schema versioning,
- and forward-compatible optional metadata.

Proposed envelope:

```json
{
  "schemaVersion": "0.1",
  "program": {
    "kind": "Program",
    "range": {
      "start": { "offset": 0, "line": 1, "column": 1 },
      "end": { "offset": 0, "line": 1, "column": 1 }
    },
    "statements": []
  }
}
```

This example is illustrative, not yet normative.

---

## 16. Relationship to the Grammar

The grammar answers:

> Which source sequences are syntactically valid?

The AST model answers:

> Which structured representation is produced for valid source?

The specification answers:

> How is that structure evaluated?

These documents must agree but should not duplicate each other unnecessarily.

Examples:

- operator precedence belongs primarily in the grammar and expression
  specification;
- resolved nesting belongs in the AST;
- numeric results belong in runtime semantics;
- supporting experiments belong in `research/` and `evidence/`.

---

## 17. Open Questions

The following areas require further specification before the AST can be frozen:

- complete statement hierarchy,
- exact variable declaration syntax,
- conditional and block syntax,
- comments and trivia preservation,
- string escape representation,
- identifier case rules,
- unary minus,
- source-offset convention,
- parser recovery nodes,
- function-call evaluation order,
- and machine-readable schema format.

---

## 18. Planned Next Steps

1. Align expression nodes with `spec/expressions.md`.
2. Finalize source-position conventions.
3. Consolidate statement syntax evidence.
4. Define a versioned JSON Schema for the AST.
5. Add hand-written AST fixtures for verified expressions.
6. Use those fixtures as parser acceptance tests.
