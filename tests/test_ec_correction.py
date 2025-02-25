from lark.tree import Tree

from utils import *
from cyk_parser import load_productions_from_json
from error_parser import ec_parse
from error_config import basic_correction_config, custom_cost_correction_config

productions_4, init_items_4 = load_productions_from_json("grammars/square_brackets.json", debug=False)

error_config = basic_correction_config(error_limit=5)
error_config = custom_cost_correction_config(error_limit=1, deletion_cost=1, insertion_cost=2)

def test_cyk_correction():
    cyk_tree = ec_parse("(])", productions_4, init_items_4, error_config=error_config, hard_limit=5, start_token="Start", debug=False)
    assert cyk_tree
    save_tree(cyk_tree, path=f"./outputs/trees/test_ec_correction_brackets/1_tree")

    cyk_tree = ec_parse("[))]", productions_4, init_items_4, error_config=error_config, hard_limit=5, start_token="Start", debug=False)
    assert cyk_tree
    save_tree(cyk_tree, path=f"./outputs/trees/test_ec_correction_brackets/2_tree")

    cyk_tree = ec_parse("[))[]]", productions_4, init_items_4, error_config=error_config, hard_limit=5, start_token="Start", debug=False)
    assert cyk_tree
    save_tree(cyk_tree, path=f"./outputs/trees/test_ec_correction_brackets/3_tree")

    cyk_tree = ec_parse("(", productions_4, init_items_4, error_config=error_config, hard_limit=5, start_token="Start", debug=False)
    assert cyk_tree
    save_tree(cyk_tree, path=f"./outputs/trees/test_ec_correction_brackets/4_tree")

    cyk_tree = ec_parse("", productions_4, init_items_4, error_config=error_config, hard_limit=5, start_token="Start", debug=False)
    assert cyk_tree
    save_tree(cyk_tree, path=f"./outputs/trees/test_ec_correction_brackets/5_tree")

    cyk_tree = ec_parse(")()", productions_4, init_items_4, error_config=error_config, hard_limit=5, start_token="Start", debug=False)
    assert cyk_tree
    save_tree(cyk_tree, path=f"./outputs/trees/test_ec_correction_brackets/6_tree")

test_cyk_correction()