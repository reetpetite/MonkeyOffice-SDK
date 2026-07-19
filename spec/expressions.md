# Expressions

> **Status:** Draft specification (based on verified reverse-engineering results)

## Overview

Expressions evaluate to a value. Every expression has a well-defined type and is
evaluated according to the language's precedence and associativity rules.

This document is **normative** where behaviour has been verified. Unknown or
unverified behaviour should be documented in the `evidence/` directory before it
is added here.

---

## Expression Categories

- Literals
- Variable references
- Function calls
- Parenthesized expressions
- Unary expressions
- Binary expressions

---

## Operator Precedence

Highest precedence first.

| Level | Operators | Associativity | Status |
|------:|-----------|---------------|--------|
| 1 | `()` | n/a | verified |
| 2 | `^` | left | verified |
| 3 | `*`, `/` | left | verified |
| 4 | `+`, `-` | left | verified |
| 5 | `=`, `<>`, `<`, `<=`, `>`, `>=` | left | verified |
| 6 | `AND`, `OR` | left, equal precedence | verified |

## Unary `NOT`

Unlike many programming languages, `NOT` does **not** behave like a normal unary
operator during parsing.

Its scope extends to the following logical expression within the current
parenthesized expression.

Example:

```text
NOT 1 = 1 OR TRUE
```

behaves as if written

```text
NOT (1 = 1 OR TRUE)
```

Parentheses terminate the scope of `NOT`.

---

## Floating-Point Behaviour

Current evidence indicates IEEE-754 binary64 semantics.

Verified observations include:

- signed zero
- Na
- positive and negative infinity
- parser rounding
- exact integer range up to 2^53

---

## Division

The `/` operator raises a runtime error on division by zero.

The library function `DIV()` instead returns infinity.

---

## Comparison Semantics

Whenever either operand is `Na`, every comparison operator evaluates to `FALSE`,
including:

```text
Na <> Na
```

---

## Future Work

Remaining topics:

- implicit conversions
- unary minus
- assignment interaction
- function evaluation order
