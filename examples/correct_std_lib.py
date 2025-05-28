import time

from utils import *
from error_inserter import load_error_file
from cyk_parser import load_productions_from_json
from lark_parser import LarkParser
from error_parser import ec_parse

from error_config import custom_cost_correction_config

lparser = LarkParser()

python_productions, init_items_python = load_productions_from_json("grammars/python.json", debug=False)

# rnd_files = load_error_file("references/error_test_set/7/std_lib_2-30.pkl")
# rnd_files = load_error_file("references/error_test_set/10/std_lib_2-60.pkl")
rnd_files = load_error_file("references/error_test_set/11/std_lib_3-60.pkl")
header = "file, num_tokens, cyk time, success, num_errors, trees eq"

print(header)
for tp in rnd_files:
    print_ls = [tp[0], len(tp[1])]
    tokens = convert_lark_tokens_for_cyk(tp[1])
    cyk_config = custom_cost_correction_config(error_limit=2) # adjust this

    start_time = time.time() # need to check for None here
    res = ec_parse(tokens, python_productions, init_items_python, error_config=cyk_config, hard_limit=2, start_token="file_input")
    end_time = time.time()

    print_ls.append(end_time - start_time)
    if res:
        succ = "true"
        metric = res.data.error
        lark_tree = lparser.parse(read(tp[0]))
        trees_eq = "true" if lark_tree == res else "false"
        # save_tree(res, f"outputs/trees/correct_std_lib_cyk/{tp[0]}--tree")

    else:
        succ = "false"
        metric = 0
        trees_eq = "false"

    print_ls.append(succ)
    print_ls.append(metric)
    print_ls.append(trees_eq)
    print(print_ls)
