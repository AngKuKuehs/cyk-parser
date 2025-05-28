from cyk_parser import load_productions_from_json, parse
from lark_parser import LarkParser
from error_config import no_correction_config
from utils import read, save_tree, convert_lark_tokens_for_cyk

# Instantiate config for parser
config = no_correction_config()

# Load initial items and productions from relevant grammar
python_productions, init_items_python = load_productions_from_json("grammars/python.json", debug=False)

# Load file and lex into tokens
lexer = LarkParser()
file_path = "references/example_small_files/basic_api.py"
lark_tokens = lexer.lex(read(file_path))
print(lark_tokens)
cyk_tokens = convert_lark_tokens_for_cyk(lark_tokens)

# Parse tokens
symbol_chart, item_chart = parse(cyk_tokens, python_productions, init_items_python, config)

# Save parse tree from symbol chart
start_symbol = "file_input"
error_metric, parse_tree = symbol_chart[0][-1][start_symbol]
save_tree(parse_tree, "basic_api_tree")
