#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from collections import Counter
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
def load(p:Path):
 try:return json.loads(p.read_text(encoding='utf-8'))
 except FileNotFoundError:raise SystemExit(f"Datei fehlt: {p.relative_to(ROOT)}")
 except json.JSONDecodeError as e:raise SystemExit(f"{p.relative_to(ROOT)}:{e.lineno}:{e.colno}: {e.msg}")
def jp(parts):
 s='$'
 for x in parts:s+=f'[{x}]' if isinstance(x,int) else f'.{x}'
 return s
def main():
 schema=load(ROOT/'data/statements/schema.json');reg=load(ROOT/'data/statements/registry.json');symbols=load(ROOT/'data/language-symbols/registry.json')
 msgs=[f"{jp(list(e.absolute_path))}: {e.message}" for e in sorted(Draft202012Validator(schema).iter_errors(reg),key=lambda e:(list(e.absolute_path),e.message))]
 entries=reg.get('statements',[]); keywords={x.get('id') for x in symbols.get('symbols',[]) if x.get('kind')=='keyword'}
 for label,vals in [('Statement-ID',[x.get('id') for x in entries]),('Symbolreferenz',[x.get('symbolId') for x in entries]),('AST-Knotenart',[x.get('astKind') for x in entries])]:
  for value,count in Counter(vals).items():
   if value is not None and count>1:msgs.append(f'doppelte {label}: {value}')
 ids=[x.get('id') for x in entries]
 if ids!=sorted(ids):msgs.append('Statements müssen nach ID sortiert sein')
 for i,e in enumerate(entries):
  if e.get('symbolId') not in keywords:msgs.append(f"$.statements[{i}].symbolId: unbekanntes Schlüsselwortsymbol {e.get('symbolId')!r}")
 if msgs:
  print('Statementvalidierung fehlgeschlagen:',file=sys.stderr)
  for m in msgs:print(f'- {m}',file=sys.stderr)
  return 1
 print(f'Statementvalidierung erfolgreich: {len(entries)} Statement(s)');return 0
if __name__=='__main__':raise SystemExit(main())
