import sys

from CYK_parser import load_productions_from_json, parse

productions_1, init_items_1 = load_productions_from_json("grammars/simple_CNF_grammar.json")
productions_2, init_items_2 = load_productions_from_json("grammars/simple_nonCNF_grammar.json")
productions_3, init_items_3 = load_productions_from_json("grammars/epsilon_grammar.json", debug=False)
productions_4, init_items_4 = load_productions_from_json("grammars/square_brackets.json", debug=False)
productions_5, init_items_5 = load_productions_from_json("grammars/ambigious.json", debug=False)

def test_parser_on_grammar_1():
    assert "Start" in parse("abc", productions_1, init_items_1)[0][0][3]
    assert "Start" in parse("ab", productions_1, init_items_1)[0][0][2]
    assert "Start" in parse("bc", productions_1, init_items_1)[0][0][2]

    assert "Start" not in parse("cba", productions_1, init_items_1)[0][0][3]
    assert "Start" not in parse("a", productions_1, init_items_1)[0][0][1]
    assert "Start" not in parse("b", productions_1, init_items_1)[0][0][1]
    assert "Start" not in parse("c", productions_1, init_items_1)[0][0][1]

def test_parser_on_grammar_2():
    assert "Start" in parse("abc", productions_2, init_items_2)[0][0][3]
    assert "Start" in parse("bcbb", productions_2, init_items_2)[0][0][4]
    assert "Start" in parse("bcbbcb", productions_2, init_items_2, debug=False)[0][0][6]
    assert "Start" in parse("aa", productions_2, init_items_2)[0][0][2]

    assert "Start" not in parse("abg", productions_2, init_items_2)[0][0][3]
    assert "Start" not in parse("bbb", productions_2, init_items_2)[0][0][3]

def test_parser_on_grammar_3():
    assert "Start" in parse("b", productions_3, init_items_3, debug=False)[0][0][1]
    assert "Start" in parse("ce", productions_3, init_items_3)[0][0][2]
    assert "Start" in parse("cde", productions_3, init_items_3)[0][0][3]
    assert "Start" in parse("ef", productions_3, init_items_3)[0][0][2]

def test_parser_on_gramamr_4():
    assert "Start" in parse("", productions_4, init_items_4, debug=False)[0][0][0]
    assert "Start" in parse("()", productions_4, init_items_4, debug=False)[0][0][2]
    assert "Start" in parse("()[]", productions_4, init_items_4, debug=False)[0][0][4]
    assert "Start" in parse("([])", productions_4, init_items_4, debug=False)[0][0][4]
    assert "Start" in parse("[()]", productions_4, init_items_4, debug=False)[0][0][4]

    assert "Start" not in parse("[(])", productions_4, init_items_4, debug=False)[0][0][4]
    assert "Start" not in parse("(])", productions_4, init_items_4, debug=False)[0][0][3]

def test_parser_on_gramamr_5():
    assert "Start" in parse("", productions_5, init_items_5, debug=False)[0][0][0]
    assert "Start" in parse("XX", productions_5, init_items_5, debug=False)[0][0][2]
    assert "Start" in parse("X", productions_5, init_items_5, debug=False)[0][0][1]
    assert "Start" in parse("XXXX", productions_5, init_items_5, debug=False)[0][0][4]

    assert "Start" not in parse("XXX", productions_5, init_items_5, debug=False)[0][0][3]
    assert "Start" not in parse("XXXXX", productions_5, init_items_5, debug=False)[0][0][3]

test_parser_on_grammar_1()
test_parser_on_grammar_2()
test_parser_on_grammar_3()
