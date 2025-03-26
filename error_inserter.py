import random
import pickle

from lark_parser import LarkParser
from utils import *

parser = LarkParser()

# get tokens
def get_tokens(directory="references/python-3.0-library", max_lines=50):
    """
    Lexes all files in a directory and its subdirectories which have less than max_lines lines.

    Parameters:
        directory (str): directory to read files from
        max_lines (int): maximum number of lines a file can be

    Returns:
        token_dict (dict):
            key (str): file path of file
            value (list[Tokens]): list of tokens from lexed file
    """
    files = get_files_from_dir(directory)
    token_dict = {}
    for file_name, file_path, num_lines in files:
        if num_lines > max_lines or "__init__.py" in file_name or num_lines <= 1:
            continue
        try:
            tokens = parser.lex(read(file_path) + "\n")
            token_dict[file_path] = tokens
        except:
            pass
    return token_dict

# error adding functions
def add_single_deletion_error(tokens, num_errors=1):
    num_tokens = len(tokens)
    del_index = random.randint(0, num_tokens-1)

    return tokens[:del_index] + tokens[del_index+1:]

def add_single_insertion_error(tokens, num_errors=1):
    num_tokens = len(tokens)
    insert_index = random.randint(0, num_tokens-1)
    new_token = tokens[random.randint(0, num_tokens-1)]

    return tokens[:insert_index] + [new_token] + tokens[insert_index:]

def add_n_deletion_error(tokens, num_errors=3):
    for _ in range(num_errors):
        num_tokens = len(tokens)
        del_index = random.randint(0, num_tokens-1)
        tokens = tokens[:del_index] + tokens[del_index+1:]
    return tokens

def add_n_insertion_error(tokens, num_errors=3):
    for _ in range(num_errors):
        num_tokens = len(tokens)
        insert_index = random.randint(0, num_tokens-1)
        new_token = tokens[random.randint(0, num_tokens-1)]
        tokens = tokens[:insert_index] + [new_token] + tokens[insert_index:]
    return tokens

def add_n_errors(tokens, num_errors=3):
    ops = [add_n_deletion_error, add_n_insertion_error]
    return ops[random.randint(0, 1)](tokens, num_errors)

# create error test set with random files in dir
def create_test_set_randomly(operation, count, token_dict, num_errors):
    res = []
    while count != 0:
        file_path = random.choice(list(token_dict.keys()))
        tokens = token_dict[file_path]
        error_tokens = operation(tokens, num_errors)
        try:
            parser.parse_from_tokens(error_tokens)
            continue
        except:
            count -= 1
            res.append((file_path, error_tokens))
    return res

# create error test set containing all files in the dir
def create_test_set_all_files(operation, token_dict, num_errors):
    res = []
    for file_path, tokens in token_dict.items():
        while True:
            error_tokens = operation(tokens, num_errors)
            try:
                parser.parse_from_tokens(error_tokens)
                continue
            except:
                res.append((file_path, error_tokens))
                break
    return res

def save_error_file(directory, error_tuples):
    os.makedirs(os.path.dirname(directory), exist_ok=True)
    with open(f'{directory}.pkl', 'wb') as f:  # open a text file
        pickle.dump(error_tuples, f)

def load_error_file(file_path):
    with open(file_path, 'rb') as f:
        error_tuples = pickle.load(f)
    return error_tuples
