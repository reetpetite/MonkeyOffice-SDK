
# Sprint 22 – Parser Test Corpus

Goal:
- introduce executable parser corpus
- separate verified examples from hypotheses

Layout:

tests/fixtures/
    expressions/
    programs/

Each fixture should eventually contain:
- source.monkey
- ast.json
- metadata.json

metadata.json records:
- status
- evidence
- expected result
