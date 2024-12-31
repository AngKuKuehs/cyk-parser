import os

from cyk_parser import load_productions_from_json, parse
from lark_parser import LarkParser
from lark.tree import Tree
from utils import *

parser = LarkParser()

python_productions, init_items_python = load_productions_from_json("grammars/python.json", debug=False)

# generate parse trees for all small python example files
def generate_small_file_trees():
    directory = "references/example_small_files"

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        # generate tree from lark
        lark_tree = None
        try:
            lark_tree = parser.parse(read(file_path) + "\n")
            lark_tree = convert_lark_tree(lark_tree)
            lark_tree = Tree(lark_tree.data, trim_children(lark_tree.children))
            save_tree(lark_tree, path=f"./outputs/trees/small_files/{file_name[:-3]}_tree_lark")
        except Exception as e:
            print(f"lark: {file_name} failed: {e}")

        # generate tree from own parser
        cyk_tree = None
        try:
            tokens = parser.lex(read(file_path) + "\n")
            symbol_chart, _ = parse(tokens, python_productions, init_items_python)
            cyk_tree = symbol_chart[0][-1]["file_input"][1]
            cyk_tree = Tree(cyk_tree.data, trim_children(cyk_tree.children))
            save_tree(cyk_tree, path=f"./outputs/trees/small_files/{file_name[:-3]}_tree")
        except Exception as e:
            print(f"cyk: {file_name} failed: {e}")

        # ensure trees are equal
        assert(lark_tree == cyk_tree)

if __name__ == "__main__":
    generate_small_file_trees()
