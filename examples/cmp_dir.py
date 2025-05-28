import time

from cyk_parser import load_productions_from_json, parse
from lark_parser import LarkParser
from lark.tree import Tree
from utils import *
from error_combiners import *
from error_config import no_correction_config

parser = LarkParser()

python_productions, init_items_python = load_productions_from_json("grammars/python.json", debug=False)

error_config = no_correction_config()

# generate parse trees for all files in a directory
def cmp_dir(directory):
    print(",".join(["file", "num lines", "lark time", "cyk time", "num tokens", "trees equal"]))
    files = get_files_from_dir(directory)
    for file_name, file_path, num_lines in files:
            if num_lines > 200:
                continue
            entry = [file_path, f"{num_lines}"] # file path, num lines

            # generate tree from lark
            lark_tree = None
            try:
                lark_start = time.time()
                lark_tree = parser.parse(read(file_path) + "\n")
                lark_end = time.time()

                entry.append(f"{lark_end - lark_start}") # lark time
                lark_tree = convert_lark_tree(lark_tree)
                lark_tree = Tree(lark_tree.data, trim_children(lark_tree.children))
                save_tree(lark_tree, path=f"./outputs/trees/tmp/{file_name[:-3]}_tree_lark")
            except Exception as e:
                continue
                # print(f"lark: {file_name} failed: {e}")

            # generate tree from own parser
            cyk_tree = None
            try:
                tokens = convert_lark_tokens_for_cyk(parser.lex(read(file_path) + "\n"))

                cyk_start = time.time()
                symbol_chart, _ = parse(tokens, python_productions, init_items_python, error_config=error_config)
                cyk_end = time.time()

                entry.append(f"{cyk_end - cyk_start}") # cyk time
                entry.append(f"{len(tokens)}") # num tokens
                cyk_tree = symbol_chart[0][-1]["file_input"][1]
                cyk_tree = Tree(cyk_tree.data, trim_children(cyk_tree.children))
                save_tree(cyk_tree, path=f"./outputs/trees/tmp/{file_name[:-3]}_tree")
            except Exception as e:
                continue

            # check if trees are equal
            if lark_tree == cyk_tree:
                entry.append("true") # trees equal
            else:
                entry.append("false")
            print(",".join(entry))

if __name__ == "__main__":
    cmp_dir("references/python-3.0-library")
