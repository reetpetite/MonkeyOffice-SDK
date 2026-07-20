from __future__ import annotations
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from parse_program import ProgramParseError,parse_program,program_to_dict
class ProgramParserTests(unittest.TestCase):
 def test_empty_program(self):self.assertEqual(program_to_dict(parse_program(''))['body'],[])
 def test_blank_lines_are_ignored(self):self.assertEqual(len(program_to_dict(parse_program('\n\nDIM amount\n\n'))['body']),1)
 def test_dim_statement(self):
  s=program_to_dict(parse_program('DIM amount'))['body'][0];self.assertEqual((s['kind'],s['name']),('dim_statement','amount'))
 def test_set_statement(self):
  s=program_to_dict(parse_program('set Result'))['body'][0];self.assertEqual((s['kind'],s['name']),('set_statement','Result'))
 def test_expression_statement_reuses_expression_parser(self):
  e=program_to_dict(parse_program('a OR b AND c'))['body'][0]['expression'];self.assertEqual(e['operator'],'op-and');self.assertEqual(e['left']['operator'],'op-or')
 def test_multiple_statements(self):
  kinds=[x['kind'] for x in program_to_dict(parse_program('DIM amount\nSET result\nNOT amount AND result\n'))['body']];self.assertEqual(kinds,['dim_statement','set_statement','expression_statement'])
 def test_keyword_requires_identifier(self):
  with self.assertRaises(ProgramParseError):parse_program('DIM 12')
 def test_keyword_rejects_trailing_tokens(self):
  with self.assertRaises(ProgramParseError):parse_program('DIM first second')
if __name__=='__main__':unittest.main()
