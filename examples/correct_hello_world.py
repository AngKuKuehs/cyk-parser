from cyk_parser import load_productions_from_json
from error_parser import ec_parse
from lark_parser import LarkParser
from error_config import basic_correction_config
from utils import read, save_tree, convert_lark_tokens_for_cyk

# Instantiate config for parser
config = basic_correction_config(error_limit=2)

# Load initial items and productions from relevant grammar
python_productions, init_items_python = load_productions_from_json("grammars/python.json", debug=False)

# Load file and lex into tokens
lexer = LarkParser()
file_path = "references/incorrect_example_small_files/hello_world.py"
lark_tokens = lexer.lex(read(file_path))
cyk_tokens = convert_lark_tokens_for_cyk(lark_tokens)

# Parse tokens
parse_tree = ec_parse(cyk_tokens, python_productions, init_items_python, config, hard_limit=2, start_token="file_input")

# Save parse tree
save_tree(parse_tree, "corrected_basic_api_tree")
