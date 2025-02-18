import sys
import time

from cyk_parser import load_productions_from_json, parse
from lark_parser import LarkParser
from lark.tree import Tree
from utils import *
from error_combiners import *

parser = LarkParser()

python_productions, init_items_python = load_productions_from_json("grammars/python.json", debug=False)

error_config = {
    "error_correct": False,
    "init_error": 0,
    "del_error_combiner": simple_del_addition,
    "ins_error_combiner": simple_ins_addition,
    "std_error_combiner": simple_std_addition,
    "init_ins_error": 0,
    "init_del_error": 0,
    "error_limit": 0
}

# generate parse trees for python std library
def cmp_file(file_path):
    file_name = file_path.split("/")[-1][:-3]

    # generate tree from lark
    lark_tree = None
    try:
        tokens = parser.lex(read(file_path) + "\n")

        lark_start = time.time()
        lark_tree = parser.parse_from_tokens(tokens)
        lark_end = time.time()
        print(f"lark parsed in {lark_end - lark_start}")

        lark_tree = convert_lark_tree(lark_tree)
        lark_tree = Tree(lark_tree.data, trim_children(lark_tree.children))
        save_tree(lark_tree, path=f"./outputs/trees/cmp_file/{file_name}_tree_lark")
    except Exception as e:
        print(f"lark: {file_name} failed: {e}")

    # generate tree from own parser
    cyk_tree = None
    try:
        tokens = convert_lark_tokens_for_cyk(parser.lex(read(file_path) + "\n"))

        cyk_start = time.time()
        symbol_chart, _ = parse(tokens, python_productions, init_items_python, error_config=error_config)
        cyk_end = time.time()
        print(f"cyk parsed in {cyk_end - cyk_start}")

        cyk_tree = symbol_chart[0][-1]["file_input"][1]
        cyk_tree = Tree(cyk_tree.data, trim_children(cyk_tree.children))
        save_tree(cyk_tree, path=f"./outputs/trees/cmp_file/{file_name}_tree")
    except Exception as e:
        print(f"cyk: {file_name} failed: {e}")

    # ensure trees are equal
    assert(lark_tree == cyk_tree)
    print("trees equal")

if __name__ == "__main__":
    file_path = sys.argv[1]
    cmp_file(file_path)
