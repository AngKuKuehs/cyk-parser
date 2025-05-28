from utils import *
from cyk_parser import load_productions_from_json
from patience_parser import patience_parse
from error_config import custom_cost_correction_config

# Instantiate config for parser
bracket_productions, bracket_init_items = load_productions_from_json("grammars/square_brackets.json", debug=False)

# Load initial items and productions from relevant grammar
error_config = custom_cost_correction_config(error_limit=2, deletion_cost=1, insertion_cost=1)

# Instantiate tokens/Load file and lex into tokens
tokens = "[)))]"

# Parse tokens
parse_tree = patience_parse(tokens, bracket_productions, bracket_init_items, error_config=error_config, hard_limit=5, start_token="Start", debug=False)

# Save parse trees
for i in range(len(parse_tree)):
    save_tree(parse_tree[i][0], path=f"fb_bracket_tree_{i}", text=f"{parse_tree[i][2]}")
