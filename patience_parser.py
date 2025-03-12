from lark.tree import Tree

from cyk_parser import parse
from symbol import Symbol
from error_combiners import FrontEndParams
from utils import get_leaves, save_tree

def patience_parse(sentence: str, productions: dict, init_items: list, error_config: dict, hard_limit: int, start_token: str, debug: bool=False, tabs: int=0) -> tuple:
    """
    Wrapper around cyk_parser.parse inspired by the patience diff. 

    Parameters:
        sentence (str): The text to parse.
        productions (dict[str, list[Production]]): dictionary of productions
        init_items (list[Item]): list of items (partially completed productions)
        error_config (dict):
            error_correct (bool): whether or not to error_correct
            init_error (int): initial error given terminals symbols in string
            del_error_combiner (callable): function that combines errors when del occurs
            front_end_del_error_combiner (callable): a function that combines error when del at the start or end of a sentence occurs
            std_error_combiner (callable): function that combines errors when a standard progression happens
            progress_error_combiner (callable): function that combines errors when item is progressed normally
            init_ins_error (int): initial error given to inserted symbols in epsilon diagonal
            error_limit (int): skips items and symbols with errors greater than this
        hard_limit (int): the number of retries after which None is returned
        start_token (str): the string which represents the symbol that indicates the start of a parse tree
        debug (bool): whether or not to print a debug trace
        tabs (int): indentation for debug trace

    Returns:
        parse_tree (Tree) | None : returns a parse tree if a valid parse can be found, None otherwise
    """
    error_config["error_correct"] = True
    counter = 0
    partial_trees = []
    error_cmp = error_config["error_comparator"]
    error_limit_cmp = error_config["limit_comparator"]
    while True:
        sent_len = len(sentence)
        symbol_chart, _ = parse(sentence=sentence, productions=productions, init_items=init_items, error_config=error_config, debug=debug, tabs=tabs)
        if start_token in symbol_chart[0][-1]: # parsed successfully, get tree/metric
            # get tree + metric
            error_metric = symbol_chart[0][-1][start_token][0]
            parse_tree = symbol_chart[0][-1][start_token][1]
            leaves = get_leaves(parse_tree, leaves=[], include_del=True)
            return partial_trees + [parse_tree]
        else: # unsuccessful parse, set generic tree/metric
            parse_tree = None
            error_metric = None

        error_limit = error_config["error_limit"]

        # check for valid whole parses with lower metric by diagonally traversing symbol chart
        for diagonal_length in range(1, sent_len + 2):
            start_col = sent_len - diagonal_length + 1
            for i in range(diagonal_length):
                col = start_col + i
                row = 0 + i
                if start_token in symbol_chart[row][col]:
                    curr_tree = symbol_chart[row][col][start_token][1]
                    curr_symbol = curr_tree.data
                    params = FrontEndParams(front_deletions=row, end_deletions=(sent_len-col), root_error=curr_symbol.error, parse_tree=curr_tree)
                    new_error = error_config["front_end_del_error_combiner"](params)
                    if (not error_cmp(new_error, error_metric) and not error_limit_cmp(new_error, error_limit)):
                        curr_symbol.error = new_error
                        front_deletions = [Tree(data=Symbol(origin="deleted", value=sentence[k], error=0, row=k, col=k+1), children=[]) for k in range(0, row)]
                        end_deletions = [Tree(data=Symbol(origin="deleted", value=sentence[k], error=0, row=k-1, col=k), children=[]) for k in range(col, sent_len)]
                        curr_tree.children = front_deletions + curr_tree.children + end_deletions
                        parse_tree = curr_tree
                        error_metric = new_error

        if parse_tree: # complete parse tree
            return partial_trees + [parse_tree]

        # no lower metric found, proceed to find largest parse
        for diagonal_length in range(1, sent_len + 2):
            start_col = sent_len - diagonal_length + 1
            # find best parse tree within the metric, parse tree within the same diagonal with the best metric?
            for i in range(diagonal_length):
                col = start_col + i
                start = row = 0 + i
                end = col
                if start_token in symbol_chart[row][col] and (not error_cmp(symbol_chart[row][col][start_token][0], error_metric)):
                # if start_token in symbol_chart[row][col]:
                    # print(f"found start token at: {row, col}")
                    parse_tree = symbol_chart[row][col][start_token][1]
                    error_metric = symbol_chart[row][col][start_token][0]
                    # longest best parse

            # partial parse tree found - edit string and retry
            if parse_tree:
                # add parse tree to partial trees
                partial_trees.append(parse_tree)

                # update input string, should exclude deletions
                leaves = get_leaves(parse_tree, leaves=[],include_del=True)
                if isinstance(sentence, str):
                    sentence = sentence[:start] + "".join(leaves) + sentence[end:]
                else:
                    sentence = sentence[:start] + leaves + sentence[end:]
                # retry
                break

        # try again
        counter += 1
        if counter > hard_limit:
            return None
