# Lexer Architecture

> Status: Working design

## Purpose

The lexer transforms source text into a deterministic stream of tokens without
performing semantic analysis.

## Responsibilities

- UTF-8 input handling
- source position tracking
- tokenization
- whitespace handling
- comment handling
- literal recognition
- lexical diagnostics

## Pipeline

```text
Characters
    │
Lexer
    │
Tokens
    │
Parser
```

## Token Categories

- identifiers
- keywords
- numeric literals
- string literals
- punctuation
- operators
- end-of-file

## Keywords

Initially verified keywords include:

- DIM
- SET
- IF
- THEN
- ELSE
- AND
- OR
- NOT
- TRUE
- FALSE

Future keywords should be versioned explicitly.

## Identifiers

Recommended rules:

- case-insensitive
- preserve original spelling
- canonical uppercase comparison

## Numeric literals

Lexer responsibilities:

- integer literals
- floating-point literals
- exponent notation
- preserve original spelling
- report malformed literals

The parser—not the lexer—assigns syntactic meaning.

## String literals

The lexer should preserve the exact contents while decoding escape sequences only
if verified by evidence.

Unknown behaviour should remain unspecified until experimentally verified.

## Whitespace

Whitespace separates tokens but otherwise carries no semantic meaning except for
accurate source locations.

## Comments

Comment handling should:

- ignore comment contents
- preserve source offsets
- allow diagnostic mapping

Comment syntax remains evidence-driven.

## Source locations

Every token should contain:

- start offset
- end offset
- line
- column

## Diagnostics

Lexical diagnostics should use stable codes.

Examples:

- invalid character
- unterminated string
- malformed number
- unexpected end of input

## Token API

Recommended immutable token model:

```text
Token
├── kind
├── spelling
├── normalized
├── range
└── trivia
```

## Trivia

Leading and trailing trivia should be preserved for future formatter support.

## Versioning

Future MonKey Office builds may introduce new keywords or operators.

The lexer should expose language-version switches rather than hard-coded behaviour.

## Testing

Lexer tests should cover:

- keywords
- identifiers
- whitespace
- numbers
- strings
- comments
- source locations
- malformed input
- Unicode
