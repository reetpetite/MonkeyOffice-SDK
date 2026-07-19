# Parser Architecture

> Status: Working design

## Goals

The parser is the reference implementation for the documented language grammar.

Responsibilities:

- consume lexer tokens
- produce an AST
- preserve source locations
- recover from syntax errors
- remain independent from semantic analysis

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
Semantic analysis
  │
Diagnostics
```

## Parser strategy

A handwritten recursive-descent parser is recommended.

Reasons:

- grammar is compact
- verified precedence is unusual
- NOT has custom scope rules
- excellent diagnostics
- easy future maintenance

## Components

- TokenStream
- Parser
- AST builder
- Diagnostic collector

## Lookahead

One-token lookahead should be sufficient for verified constructs.

The parser owns token consumption.

## Expression parsing

Use precedence climbing (or Pratt-like precedence handling) while preserving the verified precedence table.

The NOT rule is handled explicitly rather than treating NOT as a conventional unary-primary operator.

## Error recovery

Recovery should synchronize on statement boundaries and closing parentheses.

The parser should continue after recoverable syntax errors so that multiple diagnostics can be produced from one source file.

## Diagnostics

Each diagnostic should contain:

- stable diagnostic code
- severity
- source range
- message
- optional fix-it

## AST creation

Nodes are constructed during parsing.

No semantic information should be stored in the parser.

## Separation of concerns

Lexer:
- characters → tokens

Parser:
- tokens → AST

Semantic analyzer:
- AST → meaning

Formatter:
- AST → source text

Language server:
- AST + semantic model → editor features

## Testing

Parser tests should include:

- successful parses
- syntax failures
- recovery behaviour
- source ranges
- unusual NOT cases
- precedence
- numeric literals

## Future work

- parser package
- formatter
- linter
- language server
- reference interpreter
