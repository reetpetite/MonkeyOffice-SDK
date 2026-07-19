# Reference tokenizer

## Purpose

`tools/monkey_tokenize.py` is the first executable language-processing component in the
SDK. It converts source text into a deterministic token stream and resolves
verified keywords and operators through the machine-readable language-symbol
registry.

It is a reference implementation, not yet a normative lexer specification.

## Registry-driven symbols

The tokenizer does not hard-code the spelling of registered language symbols.
It loads:

```text
data/language-symbols/registry.json
```

Word-like entries are matched case-insensitively when the registry declares
`caseInsensitive: true`. Punctuation operators are matched longest-first.

Currently recognized verified symbols:

- `DIM`
- `SET`
- `AND`
- `OR`
- `NOT`
- `^`

## Token kinds

- `symbol`
- `identifier`
- `number`
- `string`
- `newline`
- `eof`

Whitespace other than line breaks is discarded.

Every token contains:

- original lexeme
- start and end byte-independent Python string offsets
- one-based line and column
- optional language-symbol registry ID

## Conservative lexical rules

Identifiers currently use an ASCII-oriented implementation rule:

```text
[A-Za-z_][A-Za-z0-9_]*
```

Numbers support decimal integer, fractional, and exponent notation.

Strings use double quotes. Two consecutive double quotes inside a string are
accepted as an escaped quote.

These identifier, numeric-literal, and string-escaping rules are implementation
proposals until verified by experiments or documentation. They must not be
reported as verified language behaviour merely because the reference tokenizer
implements them.

## Usage

```bash
printf 'dim amount\nset result' | python tools/monkey_tokenize.py
python tools/monkey_tokenize.py path/to/script.monkey
python tools/monkey_tokenize.py --json path/to/script.monkey
```

## Tests

```bash
python -m unittest discover -s tests/lexer -p 'test_*.py'
```

## Next step

The next executable component should consume this token stream and implement the
already documented expression precedence rules. In particular, it must preserve:

- left-associative power
- equal precedence for `AND` and `OR`
- wide-scope parsing of `NOT`
