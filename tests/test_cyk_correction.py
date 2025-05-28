from lark.tree import Tree

from utils import *
from cyk_parser import load_productions_from_json, parse
from error_config import custom_cost_correction_config
from error_parser import ec_parse

productions_4, init_items_4 = load_productions_from_json("grammars/square_brackets.json", debug=False)

error_config = custom_cost_correction_config(error_limit=5, deletion_cost=1, insertion_cost=2)

def test_cyk_correction():
    symbol_chart = parse("(])", productions_4, init_items_4, error_config=error_config, debug=False)[0]
    assert "Start" in symbol_chart[0][-1]
    cyk_tree = symbol_chart[0][-1]["Start"][1]
    cyk_tree = Tree(cyk_tree.data, trim_children(cyk_tree.children))
    save_tree(cyk_tree, path=f"./outputs/trees/test_correction_brackets/1_tree")

    symbol_chart = parse("[))]", productions_4, init_items_4, error_config=error_config, debug=False)[0]
    assert "Start" in symbol_chart[0][-1]
    cyk_tree = symbol_chart[0][-1]["Start"][1]
    cyk_tree = Tree(cyk_tree.data, trim_children(cyk_tree.children))
    save_tree(cyk_tree, path=f"./outputs/trees/test_correction_brackets/2-1_tree")

    symbol_chart = parse("[))[]]", productions_4, init_items_4, error_config=error_config, debug=False)[0]
    assert "Start" in symbol_chart[0][-1]
    cyk_tree = symbol_chart[0][-1]["Start"][1]
    cyk_tree = Tree(cyk_tree.data, trim_children(cyk_tree.children))
    save_tree(cyk_tree, path=f"./outputs/trees/test_correction_brackets/3_tree")

    symbol_chart = parse(")", productions_4, init_items_4, error_config=error_config, debug=False)[0]
    assert "Start" in symbol_chart[0][-1]
    cyk_tree = symbol_chart[0][-1]["Start"][1]
    cyk_tree = Tree(cyk_tree.data, trim_children(cyk_tree.children))
    save_tree(cyk_tree, path=f"./outputs/trees/test_correction_brackets/4_tree")

    symbol_chart, _ = parse("", productions_4, init_items_4, error_config=error_config, debug=False)
    assert "Start" in symbol_chart[0][-1]
    cyk_tree = symbol_chart[0][-1]["Start"][1]
    cyk_tree = Tree(cyk_tree.data, trim_children(cyk_tree.children))
    save_tree(cyk_tree, path=f"./outputs/trees/test_correction_brackets/5_tree")

    symbol_chart, _ = parse(")()", productions_4, init_items_4, error_config=error_config, debug=False)
    assert "Start" in symbol_chart[0][-1]
    cyk_tree = symbol_chart[0][-1]["Start"][1]
    cyk_tree = Tree(cyk_tree.data, trim_children(cyk_tree.children))
    save_tree(cyk_tree, path=f"./outputs/trees/test_correction_brackets/6_tree")

test_cyk_correction()
