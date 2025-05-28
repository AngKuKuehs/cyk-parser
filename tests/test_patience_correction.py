from utils import *
from cyk_parser import load_productions_from_json, parse
from patience_parser import patience_parse
from error_parser import ec_parse
from error_config import basic_correction_config, custom_cost_correction_config

bracket_productions, bracket_init_items = load_productions_from_json("grammars/square_brackets.json", debug=False)
# productions_5, init_items_5 = load_productions_from_json("grammars/test.json", debug=False)

# error_config = basic_correction_config(error_limit=5)
error_config = custom_cost_correction_config(error_limit=2, deletion_cost=1, insertion_cost=1)

def test_patience_correction():
    cyk_tree = patience_parse("()", bracket_productions, bracket_init_items, error_config=error_config, hard_limit=5, start_token="Start", debug=False)
    assert cyk_tree[0]
    for i in range(len(cyk_tree)):
        save_tree(cyk_tree[i][0], path=f"./outputs/trees/patience_correction_brackets/0-{i}_tree", text=f"{cyk_tree[i][2]}")

    cyk_tree = patience_parse("(]])", bracket_productions, bracket_init_items, error_config=error_config, hard_limit=5, start_token="Start", debug=False)
    assert cyk_tree
    for i in range(len(cyk_tree)):
        save_tree(cyk_tree[i][0], path=f"./outputs/trees/patience_correction_brackets/1-{i}_tree", text=f"{cyk_tree[i][2]}")

    cyk_tree = patience_parse("[)))]", bracket_productions, bracket_init_items, error_config=error_config, hard_limit=5, start_token="Start", debug=False)
    for i in range(len(cyk_tree)):
        save_tree(cyk_tree[i][0], path=f"./outputs/trees/patience_correction_brackets/2-{i}_tree", text=f"{cyk_tree[i][2]}")

    cyk_tree = patience_parse("[))]]", bracket_productions, bracket_init_items, error_config=error_config, hard_limit=5, start_token="Start", debug=False)
    assert cyk_tree
    for i in range(len(cyk_tree)):
        save_tree(cyk_tree[i][0], path=f"./outputs/trees/patience_correction_brackets/3-{i}_tree", text=f"{cyk_tree[i][2]}")

    cyk_tree = patience_parse("(", bracket_productions, bracket_init_items, error_config=error_config, hard_limit=5, start_token="Start", debug=False)
    assert cyk_tree
    for i in range(len(cyk_tree)):
        save_tree(cyk_tree[i][0], path=f"./outputs/trees/patience_correction_brackets/4-{i}_tree", text=f"{cyk_tree[i][2]}")

    cyk_tree = patience_parse("", bracket_productions, bracket_init_items, error_config=error_config, hard_limit=5, start_token="Start", debug=False)
    assert cyk_tree
    for i in range(len(cyk_tree)):
        save_tree(cyk_tree[i][0], path=f"./outputs/trees/patience_correction_brackets/5-{i}_tree", text=f"{cyk_tree[i][2]}")

    cyk_tree = patience_parse(")))()", bracket_productions, bracket_init_items, error_config=error_config, hard_limit=5, start_token="Start", debug=False)
    assert cyk_tree
    for i in range(len(cyk_tree)):
        save_tree(cyk_tree[i][0], path=f"./outputs/trees/patience_correction_brackets/6-{i}_tree", text=f"{cyk_tree[i][2]}")

    cyk_tree = patience_parse("[()0[", bracket_productions, bracket_init_items, error_config=error_config, hard_limit=5, start_token="Start", debug=False)
    assert cyk_tree
    for i in range(len(cyk_tree)):
        save_tree(cyk_tree[i][0], path=f"./outputs/trees/patience_correction_brackets/7-{i}_tree", text=f"{cyk_tree[i][2]}")

    cyk_tree = patience_parse("[()()]", bracket_productions, bracket_init_items, error_config=error_config, hard_limit=5, start_token="Start", debug=False)
    assert cyk_tree
    for i in range(len(cyk_tree)):
        save_tree(cyk_tree[i][0], path=f"./outputs/trees/patience_correction_brackets/8-{i}_tree", text=f"{cyk_tree[i][2]}")

test_patience_correction()