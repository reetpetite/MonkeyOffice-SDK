# Abstract Syntax Tree

Dieses Dokument beschreibt das sprachunabhängige Zielmodell des zukünftigen Parsers.

## Grundstruktur

```text
Program
└── statements: Statement[]
```

## Expression

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
