from lark.tree import Tree

from cyk_parser import parse
from symbol import Symbol
from error_combiners import FrontEndDelParams


def ec_parse(sentence: str, productions: dict, init_items: list, error_config: dict, hard_limit: int, start_token: str, debug: bool=False, tabs: int=0) -> tuple:
    """
    Wrapper around cyk_parser.parse that adds backtracking and checks for other potential parse trees throughout the symbol chart.

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
        hard_limit (int): the error limit at which to stop trying to get a parse tree
        start_token (str): the string which represents the symbol that indicates the start of a parse tree
        debug (bool): whether or not to print a debug trace
        tabs (int): indentation for debug trace

    Returns:
        parse_tree (Tree) | None : returns a parse tree if a valid parse can be found, None otherwise
    """
    error_config["error_correct"] = True
    sent_len = len(sentence)
    error_cmp = error_config["error_comparator"]
    error_limit_cmp = error_config["limit_comparator"]
    while True:
        # parse
        symbol_chart, _ = parse(sentence=sentence, productions=productions, init_items=init_items, error_config=error_config, debug=debug, tabs=tabs)

        # parsed successfully, get tree/metric
        if start_token in symbol_chart[0][-1]:
            # get tree + metric
            error_metric = symbol_chart[0][-1][start_token][0]
            parse_tree = symbol_chart[0][-1][start_token][1]
        # unsuccessful parse, set generic tree/metric
        else:
            parse_tree = None
            error_metric = None

        error_limit = error_config["error_limit"]

        # check for parses with lower metric by diagonally traversing symbol chart top right to bottom left
        for diagonal_length in range(1, sent_len + 2):
            start_col = sent_len - diagonal_length + 1
            for i in range(diagonal_length):
                col = start_col + i
                row = i
                if start_token in symbol_chart[row][col]:
                    curr_tree = symbol_chart[row][col][start_token][1]
                    curr_symbol = curr_tree.data
                    params = FrontEndDelParams(front_deletions=row, end_deletions=(sent_len-col), root_error=curr_symbol.error, parse_tree=curr_tree)
                    new_error = error_config["front_end_del_error_combiner"](params)
                    if not error_cmp(new_error, error_metric) and not error_limit_cmp(new_error, error_limit):
                        curr_symbol.error = new_error
                        curr_tree.children = [Tree(data=Symbol(origin="deleted", value=sentence[k], error=0, row=k, col=k+1), children=[]) for k in range(0, row)] + curr_tree.children + [Tree(data=Symbol(origin="deleted", value=sentence[k], error=0, row=k-1, col=k), children=[]) for k in range(col, sent_len)]
                        parse_tree = curr_tree
                        error_metric = new_error

        if parse_tree:
            return parse_tree

        if error_limit < 1:
            error_config["error_limit"] = 1
        else:
            error_config["error_limit"] = error_limit * 2

        if error_limit > hard_limit:
            return None
