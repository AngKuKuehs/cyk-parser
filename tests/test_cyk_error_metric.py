
from cyk_parser import load_productions_from_json, parse
from lark_parser import LarkParser
from error_combiners import *
from error_config import *
from utils import *

productions_1, init_items_1 = load_productions_from_json("grammars/simple_CNF_grammar.json")
productions_2, init_items_2 = load_productions_from_json("grammars/simple_nonCNF_grammar.json")
productions_3, init_items_3 = load_productions_from_json("grammars/epsilon_grammar.json", debug=False)
productions_4, init_items_4 = load_productions_from_json("grammars/square_brackets.json", debug=False)
productions_5, init_items_5 = load_productions_from_json("grammars/ambigious.json", debug=False)
python_productions, init_items_python = load_productions_from_json("grammars/python.json", debug=False)

error_config = no_correction_config()
error_config["error_limit"] = 10
error_config["init_error"] = 1

def test_parser_on_grammar_1():
    assert parse("abc", productions_1, init_items_1, error_config=error_config)[0][0][3]["Start"][0] == len("abc")
    assert parse("ab", productions_1, init_items_1, error_config=error_config)[0][0][2]["Start"][0] == len("ab")
    assert parse("bc", productions_1, init_items_1, error_config=error_config)[0][0][2]["Start"][0] == len("bc")

def test_parser_on_grammar_2():
    assert parse("abc", productions_2, init_items_2, error_config=error_config)[0][0][3]["Start"][0] == len("abc")
    assert parse("bcbb", productions_2, init_items_2, error_config=error_config)[0][0][4]["Start"][0] == len("bcbb")
    assert parse("bcbbcb", productions_2, init_items_2, debug=False, error_config=error_config)[0][0][6]["Start"][0] == len("bcbbcb")
    assert parse("aa", productions_2, init_items_2, error_config=error_config)[0][0][2]["Start"][0] == len("aa")

def test_parser_on_grammar_3():
    assert parse("b", productions_3, init_items_3, debug=False, error_config=error_config)[0][0][1]["Start"][0] == len("b")
    assert parse("ce", productions_3, init_items_3, error_config=error_config)[0][0][2]["Start"][0] == len("ce")
    assert parse("cde", productions_3, init_items_3, error_config=error_config)[0][0][3]["Start"][0] == len("cde")
    assert parse("ef", productions_3, init_items_3, error_config=error_config)[0][0][2]["Start"][0] == len("ef")

def test_parser_on_gramamr_4():
    assert parse("()", productions_4, init_items_4, debug=False, error_config=error_config)[0][0][2]["Start"][0] == 2
    assert parse("()[]", productions_4, init_items_4, debug=False, error_config=error_config)[0][0][4]["Start"][0] == 4
    assert parse("([])", productions_4, init_items_4, debug=False, error_config=error_config)[0][0][4]["Start"][0] == 4
    assert parse("[()]", productions_4, init_items_4, debug=False, error_config=error_config)[0][0][4]["Start"][0] == 4
    assert parse("[[[]]]", productions_4, init_items_4, debug=False, error_config=error_config)[0][0][6]["Start"][0] == 6

def test_parser_on_gramamr_5():
    assert parse("X", productions_5, init_items_5, debug=False, error_config=error_config)[0][0][1]["Start"][0] == len("X")
    assert parse("XX", productions_5, init_items_5, debug=False, error_config=error_config)[0][0][2]["Start"][0] == len("XX")
    assert parse("XXX", productions_5, init_items_5, debug=False, error_config=error_config)[0][0][3]["Start"][0] == len("XXX")
    assert parse("XXXX", productions_5, init_items_5, debug=False, error_config=error_config)[0][0][4]["Start"][0] == len("XXXX")
    assert parse("XXXXX", productions_5, init_items_5, debug=False, error_config=error_config)[0][0][5]["Start"][0] == len("XXXXX")

def test_parser_on_python_grammar():
    parser = LarkParser()
    tokens = parser.lex(read("references/python-3.0-library/encodings/ascii.py") + "\n")
    tokens = convert_lark_tokens_for_cyk(tokens)
    assert(parse(tokens, python_productions, init_items_python, error_config=error_config))[0][0][-1]["file_input"][0] == len(tokens)

test_parser_on_grammar_1()
test_parser_on_grammar_2()
test_parser_on_grammar_3()
test_parser_on_gramamr_4()
test_parser_on_gramamr_5()
error_config["error_limit"] = 250
test_parser_on_python_grammar()
