from CYK_parser import load_grammar_from_json, parse

grammar_1 = load_grammar_from_json("grammars/simple_CNF_grammar.json")
grammar_2 = load_grammar_from_json("grammars/simple_nonCNF_grammar.json")
grammar_3 = load_grammar_from_json("grammars/epsilon_grammar.json")

def test_parser_on_grammar_1():
    assert 'Start' in parse('abc', grammar_1)[0][0][3]
    assert 'Start' in parse('ab', grammar_1)[0][0][2]
    assert 'Start' in parse('bc', grammar_1)[0][0][2]

    assert 'Start' not in parse('cba', grammar_1)[0][0][3]
    assert 'Start' not in parse('a', grammar_1)[0][0][1]
    assert 'Start' not in parse('b', grammar_1)[0][0][1]
    assert 'Start' not in parse('c', grammar_1)[0][0][1]

def test_parser_on_grammar_2():
    assert 'Start' in parse('abc', grammar_2)[0][0][3]
    assert 'Start' in parse('bcbb', grammar_2)[0][0][4]
    assert 'Start' in parse('bcbbcb', grammar_2)[0][0][6]
    assert 'Start' in parse('aa', grammar_2)[0][0][2]

    assert 'Start' not in parse("abg", grammar_2)[0][0][3]
    assert 'Start' not in parse("bbb", grammar_2)[0][0][3]

def test_parser_on_grammar_3():
    assert 'Start' in parse('b', grammar_3)[0][0][1]
    assert 'Start' in parse('ce', grammar_3)[0][0][2]
    assert 'Start' in parse('cde', grammar_3)[0][0][3]

# test_parser_on_grammar_1()
# test_parser_on_grammar_2()
test_parser_on_grammar_3()