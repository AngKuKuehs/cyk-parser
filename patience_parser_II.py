from lark.tree import Tree

from cyk_parser import parse
from symbol import Symbol
from error_combiners import FrontEndDelParams
from utils import get_leaves, trim_nonterminal_leaves

def patience_parse_II(sentence: str, productions: dict, init_items: list, error_config: dict, hard_limit: int, start_token: str, debug: bool=False, tabs: int=0) -> tuple:
    """
    Modified version of patience parse. Finds largest tree regardless of root symbol and edits the original string accordingly.

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
        tuple:
            parse_tree (Tree): parse tree
            sentence (str): original sentence parse tree is derived from
            parse_status (str): whether parse was partial or complete, also start and end index if parse tree was partial

    """
    error_config["error_correct"] = True
    counter = 0
    partial_trees = []
    error_cmp = error_config["error_comparator"]
    error_limit = error_config["error_limit"]
    error_limit_cmp = error_config["limit_comparator"]

    terminals = set()
    nonterminals = set()
    for item in init_items:
        lhs_sym = item.production.lhs
        nonterminals.add(lhs_sym)
        if lhs_sym in terminals:
            terminals.remove(lhs_sym)
        rhs_ls = item.production.rhs
        for rhs in rhs_ls:
            if rhs not in nonterminals and rhs not in terminals:
                terminals.add(rhs)

    while True:
        sent_len = len(sentence)
        symbol_chart, _ = parse(sentence=sentence, productions=productions, init_items=init_items, error_config=error_config, debug=debug, tabs=tabs)
        # print(error_limit)
        if start_token in symbol_chart[0][-1]: # parsed successfully, get tree/metric
            # print("found start root at top")
            # get tree + metric
            error_metric = symbol_chart[0][-1][start_token][0]
            parse_tree = symbol_chart[0][-1][start_token][1]
            parse_tree = Tree(parse_tree.data, trim_nonterminal_leaves(parse_tree.children, terminals)) # remove nonterminal children
            return partial_trees + [(parse_tree, sentence, "complete parse")]
        else: # unsuccessful parse, set generic tree/metric
            parse_tree = None
            error_metric = None

        # check for whole parses with lower metric by diagonally traversing symbol chart
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
                    if (not error_cmp(new_error, error_metric)) and (not error_limit_cmp(new_error, error_limit)):
                        # print(not error_limit_cmp(new_error, error_limit))
                        curr_symbol.error = new_error
                        front_deletions = [Tree(data=Symbol(origin="deleted", value=sentence[k], error=0, row=k, col=k+1), children=[]) for k in range(0, row)]
                        end_deletions = [Tree(data=Symbol(origin="deleted", value=sentence[k], error=0, row=k-1, col=k), children=[]) for k in range(col, sent_len)]
                        curr_tree.children = front_deletions + curr_tree.children + end_deletions
                        parse_tree = curr_tree
                        error_metric = new_error

        if parse_tree: # complete parse tree
            # print("found start root at others")
            parse_tree = Tree(parse_tree.data, trim_nonterminal_leaves(parse_tree.children, terminals)) # remove nonterminal children
            return partial_trees + [(parse_tree, sentence, "complete parse")]

        # no parse tree found, proceed to find parse of largest substring no matter the root
        for diagonal_length in range(1, sent_len + 2):
            start_col = sent_len - diagonal_length + 1
            # find best parse tree within the metric, parse tree within the same diagonal with the best metric?
            start = None
            end = None
            for i in range(diagonal_length):
                col = start_col + i
                row = i
                # print(row, col)
                if len(symbol_chart[row][col]) != 0:
                    # iterate through symbols in position and find the lowest metric
                    for curr_symbol, error_tree_tuple in symbol_chart[row][col].items():
                        if (not error_cmp(symbol_chart[row][col][curr_symbol][0], error_metric) and not error_limit_cmp(symbol_chart[row][col][curr_symbol][0], error_limit)):
                            start = row
                            end = col
                            parse_tree = error_tree_tuple[1]
                            error_metric = error_tree_tuple[0]

                            # print(f"found alt root {curr_symbol}: {error_metric}")

            # partial parse tree found - edit string and retry
            if parse_tree:
                # add parse tree to partial trees
                parse_tree = Tree(parse_tree.data, trim_nonterminal_leaves(parse_tree.children, terminals)) # remove nonterminal children
                if isinstance(sentence, str):
                    partial_trees.append((parse_tree, sentence, f"partial parse, {sentence[:start] + '*' + sentence[start:end] + '*' + sentence[end:]}"))
                else:
                    partial_trees.append((parse_tree, sentence))
                # update input string, should exclude deletions
                leaves = get_leaves(parse_tree, leaves=[],include_del=False) #
                if isinstance(sentence, str):
                    sentence = sentence[:start] + "".join(leaves) + sentence[end:]
                else:
                    sentence = sentence[:start] + leaves + sentence[end:]
                # retry
                break

        # try again
        # print("trying again")
        counter += 1
        if counter > hard_limit:
            return partial_trees
