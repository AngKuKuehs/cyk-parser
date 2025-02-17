import json

from lark.tree import Tree

from item import Item
from symbol import Symbol
from production import Production
from error_combiners import simple_del_addition, simple_ins_addition, simple_prog_addition

make_tree = True

def load_productions_from_json(path: str, debug: bool=False, tabs: int=0) -> dict:
    """
    Loads a dictionary of productions from a json file.

    Parameters:
        path (str): path to the json file with productions

    Returns:
        tuple:
            productions (dict[str, list[Production]]): productions specified from json file, key: lhs, value: rhs
            init_items (list[Item]): list of initial items
    """
    print(f"{'  ' * tabs}Loading {path}") if debug else ""
    
    # load the grammar as a python dictionary
    with open(path) as f:
       production_file = (json.load(f))
    print(f"{'  ' * tabs}Production File: {production_file}") if debug else ""

    # get the production rules and initial items (rules where dots are in position 0)
    productions = {}
    init_items = []
    # for each rule (which consists of a lhs and rhs)
    for lhs, values in production_file.items():
        for rhs in values:
            # append the correponding productions and items to their collections
            if type(rhs) == dict: 
                for name, result in rhs.items():
                    print(f"{'  ' * tabs}name: {name}, result: {result}") if debug else ""
                    result = list(map(lambda x: () if x == [] else x, result))
                    production = Production(lhs, result, name)
                    init_items.append(production.create_init_item())
                    if lhs in productions:
                        productions[lhs].append(production)
                    else:
                        productions[lhs] = [production]
            else:
                # replace empty list with empty tuple
                rhs = list(map(lambda x: () if x == [] else x, rhs))
                production = Production(lhs, rhs)
                init_items.append(production.create_init_item())
                if lhs in productions:
                    productions[lhs].append(production)
                else:
                    productions[lhs] = [production]

    print(f"{'  ' * tabs}Productions: {productions}") if debug else ""
    print(f"{'  ' * tabs}Init Items: {init_items}") if debug else ""
    return productions, init_items

error_config = {
    "error_correct": False,
    "init_error": 0,
    "del_error_combiner": simple_del_addition,
    "ins_error_combiner": simple_ins_addition,
    "progress_error_combiner": simple_prog_addition,
    "init_ins_error": 1,
    "init_del_error": 1,
    "error_limit": 1
}

def parse(sentence: str, productions: dict, init_items: list, error_config=error_config, debug: bool=False, tabs: int=0) -> tuple:
    """
    Parses a string according to the provided productions and returns the corresponding symbol chart and item chart.

    Parameters:
        sentence (str): The text to parse.
        productions (dict[str, list[Production]]): dictionary of productions
        init_items (list[Item]): list of items (partially completed productions)
        error_config (dict):
            error_correct (bool): whether or not to error_correct
            init_error (int): initial error given terminals symbols in string
            del_error_combiner (callable): function that combines errors when del occurs
            ins_error_combiner (callable): function that combines errors when ins occurs
            progress_error_combiner (callable): function that combines errors when item is progressed normally
            init_ins_error (int): initial error given to inserted symbols in epsilon diagonal
            error_limit (int): skips items and symbols with errors greater than this
        debug (bool): whether or not to print a debug trace
        tabs (int): indentation for debug trace

    Returns:
        tuple:
            symbol_chart (list[list[dict[str, tuple(int, Tree)]]]): chart of symbols after parsing
                key: string repr of symbol
                value:
                    0: error metric
                    1: tree the symbol is the root node of
            item_chart (list[list[dict[item, int]]]): chart of items after parsing
    """
    print(f"{'*'*30}\nParsing \"{sentence}\" with {productions}\n{'*'*30}") if debug else ""
    n = len(sentence)
    item_chart = [[{} for _ in range(n + 1)] for _ in range(n + 1)] # key: item, value: error metric
    symbol_chart = [[{} for _ in range(n + 1)] for _ in range(n + 1)] # key: symbol, value: error metric, tree

    fill_epsilon_diagonal(n, init_items, symbol_chart, item_chart, error_config=error_config, debug=debug, tabs=tabs)

    if debug:
        print(f"{'  ' * (tabs + 0)}Epsilon Diagonal Filled:")
        print(f"{'  ' * (tabs + 1)}Item Chart: {item_chart}")
        print(f"{'  ' * (tabs + 1)}Symbol Chart: {symbol_chart}")

    fill_diagonal(n, sentence, symbol_chart, item_chart, error_config=error_config, debug=debug, tabs=tabs)

    if debug:
        print(f"{'  ' * (tabs + 0)}First Diagonal Filled:")
        print(f"{'  ' * (tabs + 1)}Item Chart: {item_chart}")
        print(f"{'  ' * (tabs + 1)}Symbol Chart: {symbol_chart}")

    fill_rest(n, symbol_chart, item_chart,  sentence=sentence, error_config=error_config, debug=debug, tabs=tabs)

    if debug:
        print(f"{'  ' * (tabs + 0)}rest filled")
        print(f"{'  ' * (tabs + 1)}Item Chart: {item_chart}")
        print(f"{'  ' * (tabs + 1)}Symbol Chart: {symbol_chart}")

    return (symbol_chart, item_chart)

def fill_epsilon_diagonal(n: int, init_items: list, symbol_chart: list, item_chart: list, error_config=error_config, debug: bool=False, tabs: int=0) -> None:
    """
    Fill in the first diagonal of the symbol and item charts inplace.

    Parameters:
        n (int): length of the sentence
        init_items (list[Item]): list of items (partially completed productions)
        symbol_chart (list[list[dict[str, tuple(int, Tree)]]]): chart of symbols
        item_chart (list[list[dict[item, int]]]): chart of items
        error_config (dict): refer to parse doc string
        debug (bool): whether or not to print a debug trace
        tabs (int): indentation for debug trace

    Returns:
        None
    """
    print(f"{'  ' * (tabs + 0)}Filling epsilon:") if debug else ""

    # add empty string as a symbol
    print(f"{'  ' * (tabs + 1)}Adding ():") if debug else ""
    empty_symbol = Symbol("epsilon", (), 0, 0, 0,)
    closure_on_symbol(row=0, col=0, item_chart=item_chart, symbol_chart=symbol_chart, symbol=empty_symbol, item=None, error=0, error_config=error_config, debug=debug, tabs=tabs+2)

    # add initial items and try to progress on the spot
    print(f"{'  ' * (tabs + 1)}Adding inital items:") if debug else ""
    for item in init_items:
        # insert symbols from completed items
        if item.completed():
            new_sym = Symbol(origin="epsilon", value=item.production.lhs, error=0, row=0, col=0)
            closure_on_symbol(0, 0, item_chart=item_chart, symbol_chart=symbol_chart, symbol=new_sym, item=item, error=0) 
        closure_on_item(row=0, col=0, item_chart=item_chart, symbol_chart=symbol_chart, item=item, error=0, error_config=error_config, debug=debug, tabs=tabs+2)
    
    # insertion corrections, goes through all items and add lhs and rhs to epislon cell
    if error_config["error_correct"]: #TODO: two points of truth here: symbol chart error and error contained in Sym
        for item in init_items:
            lhs_sym = Symbol(origin="inserted", value=item.production.lhs, error=error_config["init_ins_error"], row=0, col=0)
            closure_on_symbol(row=0, col=0, item_chart=item_chart, symbol_chart=symbol_chart, symbol=lhs_sym, item=None, error=error_config["init_ins_error"], error_config=error_config, debug=debug, tabs=tabs)
            rhs_ls = item.production.rhs
            for rhs in rhs_ls:
                rhs_sym = Symbol(origin="inserted", value=rhs, error=0, row=0, col=0)
                closure_on_symbol(row=0, col=0, item_chart=item_chart, symbol_chart=symbol_chart, symbol=rhs_sym, item=None, error=error_config["init_ins_error"], error_config=error_config, debug=debug, tabs=tabs)

    # copy cell to the rest of the diagonal
    symbol_cell = symbol_chart[0][0]
    item_cell = item_chart[0][0]
    for row in range(n + 1):
        symbol_chart[row][row] = symbol_cell
        item_chart[row][row] = item_cell

    print(f"{'  ' * (tabs + 1)}Symbol Chart: {symbol_chart}") if debug else ""
    print(f"{'  ' * (tabs + 1)}Item Chart: {item_chart}") if debug else ""

def closure_on_symbol(row: int, col: int, item_chart: list[list[Item]],
                      symbol_chart: list[list[dict]], symbol: str, item: Item,
                      error: int, error_config=error_config,
                      debug: bool=False, tabs: int=0) -> None:
    """
    Perform a closure on a symbol. This is done by checking if any new items
    can be progressed or completed given the addition of the symbol at the
    given row/col.

    Parameters:
        row (int): row in symbol chart to add symbol
        col (int): int in symbol chart to add symbol
        item_chart (list[list[dict[item, int]]]): chart of items
        symbol_chart (list[list[dict[str, tuple(int, Tree)]]]): chart of symbols
        symbol (str): symbol to add
        item (Item): item which completed into symbol
        error_config (dict): refer to parse doc string
        debug (bool): whether or not to print a debug trace
        tabs (int): indentation for debug trace

    Returns:
        None
    """
    if debug:
        print(f"{'  ' * (tabs + 0)}Closure on '{symbol}' at {row}, {col}")
        print(f"{'  ' * (tabs + 1)}Symbol Chart: {symbol_chart}")
        print(f"{'  ' * (tabs + 1)}Symbol Chart Cell: {symbol_chart[row][col]}")
        print(f"{'  ' * (tabs + 1)}Item Chart: {item_chart}") if debug else ""

    # checks if a symbol with a lower error metric is in place or if error by itself is too high
    if symbol in symbol_chart[row][col] and (error >= symbol_chart[row][col][symbol][0] or error > error_config["error_limit"]): # TODO: make 3 adjustable
        print(f"{'  ' * (tabs + 1)}symbol in cell already") if debug else ""
        return

    if make_tree:
        if item == None: # symbol was not made by an item completion
            if symbol == ():
                symbol_tree = Tree(data="None", children=[])
            else:
                symbol_tree = Tree(data=symbol, children=[])
        else:
            symbol_tree = Tree(data=symbol, children=item.children)
    else:
        symbol_tree = None

    symbol_chart[row][col][symbol] = (error, symbol_tree) # this is a problem, need to be able to change the symbols in here and not just their error metrics

    error_combiner = error_config["progress_error_combiner"]
    # generate list of items from the epsilon diagonal that could progress
    # potentially optimize by storing items as a dict with the key as the symbol that can progress it and the value as a list of items
    new_items_map = map(lambda prev_item: (prev_item[0].progress(symbol=symbol,
                                                                 split=((row, row), (row, col)), 
                                                                 symbol_tree=symbol_tree),
                                                                 error_combiner(item_error=prev_item[1], symbol_error=error)),
                        item_chart[row][row].items())

    new_items = dict(filter(lambda x: x[0] is not None, new_items_map))

    print(f"{'  ' * (tabs + 1)}New items from closure: {new_items}") if debug else ""

    # add new items to the item chart and perform the relevant closure
    for item, item_error in new_items.items():
        print(f"{'  ' * (tabs + 2)}Item: {item}") if debug else ""
        print(f"{'  ' * (tabs + 3)}Item completed: {item.completed()}") if debug else ""
        closure_on_item(row=row, col=col, item_chart=item_chart, symbol_chart=symbol_chart, item=item, error=item_error, error_config=error_config, debug=debug, tabs=tabs+4)
        if item.completed(): # should just call closure on item, that will deal with the item being completed
            print(f"{'  ' * (tabs + 3)}Completes") if debug else ""
            new_sym = Symbol(origin="item completion", value=item.production.lhs, error=item_error, row=row, col=col)
            closure_on_symbol(row, col, item_chart, symbol_chart, symbol=new_sym, item=item, error=item_error, error_config=error_config, debug=debug, tabs=tabs+4)
        else:
            print(f"{'  ' * (tabs + 3)}Progresses") if debug else ""

def closure_on_item(row: int, col: int, item_chart: list,
                    symbol_chart: list, item: Item, error: int,
                    error_config=error_config,
                    debug: bool=False, tabs: int=0) -> None:
    """
    Perform a closure on an item. This is done by checking if any symbols in
    the epsilon diagonal can progress the item that is to be added. i.e.
    tries to progress without moving forward in the chart

    Parameters:
        row (int): row in item chart to add item
        col (int): int in item chart to add item
        item_chart (list[list[dict[item, int]]]): chart of items
        symbol_chart (list[list[dict[str, tuple(int, Tree)]]]): chart of symbols
        item (Item): item to add
        error_config (dict): refer to parse doc string
        debug (bool): whether or not to print a debug trace
        tabs (int): indentation for debug trace

    Returns:
        None
    """
    if debug:
        print(f"{'  ' * (tabs + 0)}Closure on '{item}' at {row}, {col}")
        print(f"{'  ' * (tabs + 1)}Item Chart: {item_chart}")
        print(f"{'  ' * (tabs + 1)}Item Chart Cell: {item_chart[row][col]}")
        print(f"{'  ' * (tabs + 1)}Symbol Chart: {symbol_chart}")

    # checks if an item with a lower error metric is in place or if error by itself is too high
    if item in item_chart[row][col] and (error >= item_chart[row][col][item] or error > error_config["error_limit"]):
        print(f"{'  ' * (tabs + 1)}Item in item chart") if debug else ""
        return

    # add item to item chart
    item_chart[row][col][item] = error
    print(f"{'  ' * (tabs + 1)}Item added to item chart") if debug else ""

    cell_on_diagonal = symbol_chart[col][col]

    # check if item can progress on the spot, perform closure if so
    next_symbol = item.get_next_symbol()
    if next_symbol in cell_on_diagonal:
        print(f"{'  ' * (tabs + 1)}Item Can Progress") if debug else ""
        symbol_tree = cell_on_diagonal[next_symbol][1]

        new_item = item.progress(next_symbol, split=((row, col), (col, col)), symbol_tree=symbol_tree)
        new_item_error = error_config["ins_error_combiner"](error, cell_on_diagonal[next_symbol][0]) # this may not be exactly right?? normal progression how?
        closure_on_item(row, col, item_chart, symbol_chart, item=new_item, error=new_item_error, error_config=error_config, debug=debug, tabs=tabs+2)
        if new_item.completed():
            print(f"{'  ' * (tabs + 1)}Item Completes") if debug else ""
            new_sym = Symbol(origin="item completion", value=item.production.lhs, error=new_item_error, row=row, col=col)
            closure_on_symbol(row=row, col=col, item_chart=item_chart, symbol_chart=symbol_chart, symbol=new_sym, item=new_item, error=new_item_error, error_config=error_config, debug=debug, tabs=tabs)
        else:
            print(f"{'  ' * (tabs + 1)}Item does not Completes") if debug else ""
    

def fill_diagonal(n: int, sentence: str, symbol_chart: list, item_chart: list, error_config=error_config, debug: bool=False, tabs: int=0) -> None:
    """
    Fill in the first diagonal after the epsilon diagonal of the symbol and 
    item charts inplace. This is done by putting the initial symbols from
    the sentence into their place in the symbol chart.

    Parameters:
        n (int): length of the sentence
        sentence (str): the sentence to parse
        symbol_chart (list[list[dict[str, int]]]): chart of symbols
        item_chart (list[list[dict[item, int]]]): chart of items
        debug (bool): whether or not to print a debug trace
        tabs (int): indentation for debug trace

    Returns:
        None
    """
    print(f"{'  ' * (tabs + 0)}Filling first diagonal") if debug else ""
    for row in range(n):
        col = row + 1
        symbol = sentence[row]
        # TODO: Add original string values => get list of lark tokens? if have if not use sentence[row] 
        
        new_sym = Symbol(origin="sentence", value=sentence[row], error=error_config["init_error"], row=row, col=col, sentence_val="HUH")
        closure_on_symbol(row, col, item_chart=item_chart, symbol_chart=symbol_chart, symbol=new_sym, item=None, error=error_config["init_error"], error_config=error_config, debug=debug, tabs=tabs+1)

def fill_rest(n: int, symbol_chart: list, item_chart: list, sentence: list[str], error_config=error_config, debug: bool=False, tabs: int=0) -> None:
    """
    Fill in remaining diagonals apart from the epsilon and first diagonal.

    Parameters:
        n (int): length of the sentence
        symbol_chart (list[list[dict[str, int]]]): chart of symbols
        item_chart (list[list[dict[item, int]]]): chart of items
        error_config (dict): refer to parse doc string
        debug (bool): whether or not to print a debug trace
        tabs (int): indentation for debug trace

    Returns:
        None
    """
    # iterate up through the charts diagonally
    print(f"{'  ' * (tabs + 0)}Filling rest:") if debug else ""
    for length in range(1, n):
        print(f"{'  ' * (tabs + 1)}length: {length}") if debug else ""
        for row in range(0, n - length):
            col = row + length + 1
            print(f"{'  ' * (tabs + 2)}row, col: {row, col}") if debug else ""

            # iterate through item/symbol splits that can reach the current cell
            for split in range(1, length + 1): # does this need to be in a certain order?
                print(f"{'  ' * (tabs + 3)}split: {split}") if debug else ""
                item_row = row
                item_col = col - split
                sym_row = col - split
                sym_col = col

                # iterate through items that could be progressed in current split
                for item, item_error in item_chart[item_row][item_col].items():
                    print(f"{'  ' * (tabs + 4)}Item: {item}") if debug else ""
                    next_symbol = item.get_next_symbol()
                    deletion_count = 0 # count of deleted symbols
                    # also consider deletions here, make this dependent on some variable
                    deleted_symbols = []
                    for e_sym_row in range(sym_row, sym_col):
                        symbol_cell = symbol_chart[e_sym_row][sym_col]

                        if deletion_count != 0: # in a deletion
                            del_str = sentence[item_col + deletion_count - 1] # should be correct?
                            del_symbol = Symbol(origin="deleted", value=del_str, error=error_config["init_del_error"], row=item_col+deletion_count-1, col=item_col+deletion_count) # TODO: inital error how? doesn't matter? sentence value how to get?
                            deleted_symbols.append(Tree(data=del_symbol, children=[]))
                        if next_symbol in symbol_cell:
                            # custom error combiner
                            new_item_error = error_config["del_error_combiner"](item_error, symbol_cell[next_symbol][0], deletion_count)
                            # error cut-off
                            if new_item_error > error_config["error_limit"]:
                                continue

                            symbol_tree = symbol_cell[next_symbol][1] # is this right? deleted symbols is a list of trees
                            new_item = item.progress(next_symbol, split=((item_row, item_col), (sym_row, sym_col)), symbol_tree=symbol_tree, del_sym_trees=deleted_symbols) # need to pass deleted trees
                            if new_item.completed(): 
                                print(f"{'  ' * (tabs + 4)}Item Completes, adding {item.production.lhs} to symbol chart") if debug else ""
                                origin = "skipped to" if (deletion_count != 0) else "item completion"
                                item_chart[row][col][new_item] = new_item_error
                                new_sym = Symbol(origin=origin, value=item.production.lhs, error=new_item_error, row=row, col=col)
                                closure_on_symbol(row, col, item_chart, symbol_chart, new_sym, new_item, new_item_error, error_config=error_config, debug=debug, tabs=tabs+5)
                                print(f"{'  ' * (tabs + 4)}Symbol Chart: {symbol_chart}") if debug else ""
                                print(f"{'  ' * (tabs + 4)}Item Chart: {item_chart}") if debug else ""
                            else:
                                closure_on_item(row, col, item_chart, symbol_chart, new_item, new_item_error, error_config=error_config, debug=debug, tabs=tabs+5)
                                print(f"{'  ' * (tabs + 4)}Item progressing, adding {new_item} to item chart") if debug else ""
                                print(f"{'  ' * (tabs + 4)}Item Chart: {item_chart}") if debug else ""
                                print(f"{'  ' * (tabs + 4)}Symbol Chart: {symbol_chart}") if debug else ""
                        if not error_config["error_correct"]:
                            break

                        deletion_count += 1
