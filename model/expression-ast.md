# Reference expression parser

## Scope

`tools/parse_expression.py` is a registry-driven Pratt parser for the verified
core of MonKey Office expressions.

Supported primary expressions:

- identifiers
- number literals
- string literals
- parenthesized expressions

Supported operators:

- prefix `NOT`
- infix `^`
- infix `AND`
- infix `OR`

## Executable precedence model

The parser loads binding information from:

```text
data/operators/registry.json
```

The current executable ordering is:

```text
^          precedence 30, left-associative
NOT        precedence 20, prefix
AND / OR   precedence 10, left-associative
```

Consequences:

```text
2 ^ 3 ^ 2       => (2 ^ 3) ^ 2
a OR b AND c    => (a OR b) AND c
NOT a AND b     => (NOT a) AND b
NOT a ^ b       => NOT (a ^ b)
```

## AST nodes

The JSON AST uses these node kinds:

- `identifier`
- `number`
- `string`
- `group`
- `unary`
- `binary`

Operator nodes reference stable language-symbol IDs such as `op-power` and
`op-not`, not source spelling.

## Usage

```bash
python tools/parse_expression.py 'NOT a AND b ^ c'
printf 'a OR b AND c' | python tools/parse_expression.py
```

## Tests

```bash
python -m unittest discover -s tests/parser -p 'test_*.py'
```

## Boundary

Literal syntax and identifier syntax remain reference-implementation proposals
until supported by direct evidence. The parser does not yet parse declarations,
assignments, function calls, comparisons, arithmetic other than power, or full
scripts.
