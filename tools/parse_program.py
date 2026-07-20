#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
TOOLS=Path(__file__).resolve().parent;ROOT=TOOLS.parent
if str(TOOLS) not in sys.path:sys.path.insert(0,str(TOOLS))
from monkey_tokenize import Token,TokenizeError,tokenize
from parse_expression import Node as ExpressionNode,ParseError as ExpressionParseError,Parser as ExpressionParser,node_to_dict
STATEMENT_REGISTRY=ROOT/'data/statements/registry.json'
@dataclass(frozen=True)
class StatementNode:
 kind:str;start:int;end:int;name:str|None=None;expression:ExpressionNode|None=None
@dataclass(frozen=True)
class ProgramNode:
 kind:str;start:int;end:int;body:tuple[StatementNode,...]
class ProgramParseError(ValueError):
 def __init__(self,message:str,token:Token):super().__init__(message);self.token=token
def load_statements(path:Path=STATEMENT_REGISTRY)->dict[str,dict[str,Any]]:
 d=json.loads(path.read_text(encoding='utf-8'));return {x['symbolId']:x for x in d['statements']}
def eof_after(ts:list[Token])->Token:
 if ts:
  t=ts[-1];return Token('eof','',t.end,t.end,t.line,t.column+len(t.lexeme))
 return Token('eof','',0,0,1,1)
def split_lines(ts:list[Token])->list[list[Token]]:
 lines=[];cur=[]
 for t in ts:
  if t.kind=='eof':break
  if t.kind=='newline':lines.append(cur);cur=[]
  else:cur.append(t)
 if cur:lines.append(cur)
 return lines
def parse_statement(ts:list[Token],defs:dict[str,dict[str,Any]])->StatementNode:
 first=ts[0]
 if first.kind=='symbol' and first.symbol_id in defs:
  d=defs[first.symbol_id]
  if d['form']!='keyword-identifier':raise ProgramParseError(f"nicht unterstützte Statementform {d['form']!r}",first)
  if len(ts)<2:raise ProgramParseError('Bezeichner nach Schlüsselwort erwartet',first)
  name=ts[1]
  if name.kind!='identifier':raise ProgramParseError('Bezeichner erwartet',name)
  if len(ts)>2:raise ProgramParseError('unerwartetes Token nach Bezeichner',ts[2])
  return StatementNode(d['astKind'],first.start,name.end,name=name.lexeme)
 try:expr=ExpressionParser([*ts,eof_after(ts)]).parse()
 except ExpressionParseError as e:raise ProgramParseError(str(e),e.token) from e
 return StatementNode('expression_statement',expr.start,expr.end,expression=expr)
def parse_program(source:str)->ProgramNode:
 defs=load_statements();body=tuple(parse_statement(line,defs) for line in split_lines(tokenize(source)) if line)
 return ProgramNode('program',body[0].start if body else 0,body[-1].end if body else 0,body)
def statement_to_dict(n:StatementNode)->dict[str,Any]:
 r={'kind':n.kind,'start':n.start,'end':n.end}
 if n.name is not None:r['name']=n.name
 if n.expression is not None:r['expression']=node_to_dict(n.expression)
 return r
def program_to_dict(n:ProgramNode)->dict[str,Any]:return {'kind':n.kind,'start':n.start,'end':n.end,'body':[statement_to_dict(x) for x in n.body]}
def main(argv=None):
 ap=argparse.ArgumentParser(description='Parst einen zeilenorientierten MonKey-Office-Programmkern.');ap.add_argument('path',nargs='?');ap.add_argument('--compact',action='store_true');a=ap.parse_args(sys.argv[1:] if argv is None else argv)
 src=Path(a.path).read_text(encoding='utf-8') if a.path else sys.stdin.read()
 try:p=parse_program(src)
 except TokenizeError as e:print(f'Tokenisierung fehlgeschlagen bei {e.line}:{e.column}: {e}',file=sys.stderr);return 1
 except ProgramParseError as e:print(f'Parserfehler bei {e.token.line}:{e.token.column}: {e}',file=sys.stderr);return 1
 print(json.dumps(program_to_dict(p),ensure_ascii=False,indent=None if a.compact else 2));return 0
if __name__=='__main__':raise SystemExit(main())
