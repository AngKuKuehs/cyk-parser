import time

from utils import *
from error_inserter import load_error_file
from cyk_parser import load_productions_from_json
from patience_parser import patience_parse
from lark_parser import LarkParser

from error_config import custom_cost_correction_config

lparser = LarkParser()

python_productions, init_items_python = load_productions_from_json("grammars/python.json", debug=False)

# rnd_files = load_error_file("references/error_test_set/5/std_lib_3-80.pkl")
rnd_files = load_error_file("references/error_test_set/10/std_lib_2-60.pkl")

print("limit: 6 retry, file size < 50")
header = "file, num_tokens, patience duration, success, retries"
print(header)

for tp in rnd_files:
    print_ls = [tp[0], len(tp[1])] # file and num_tokens
    tokens = convert_lark_tokens_for_cyk(tp[1])
    patience_config = custom_cost_correction_config(error_limit=1) # adjust error limit here

    start_time = time.time()
    err_trees = patience_parse(tokens, python_productions, init_items_python, error_config=patience_config, hard_limit=6, start_token="file_input")
    end_time = time.time()

    print_ls.append(end_time - start_time) # patience duration
    if len(err_trees[-1]) == 3 and "complete" in err_trees[-1][2]:
        print_ls.append("true")
    else:
        print_ls.append("false")

    print_ls.append(len(err_trees))
    print(print_ls)
