import json

from lark.tree import Tree

from item import Item
from production import Production

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

def parse(sentence: str, productions: dict, init_items: list, init_error: int=0, debug: bool=False, tabs: int=0) -> tuple:
    """
    Parses a string according to the provided productions and returns the corresponding symbol chart and item chart.

    Parameters:
        sentence (str): The text to parse.
        productions (dict[str, list[Production]]): dictionary of productions
        init_items (list[Item]): list of items (partially completed productions)
        debug (bool): whether or not to print a debug trace
        tabs (int): indentation for debug trace

    Returns:
        tuple:
            symbol_chart (list[list[dict[str, int]]]): chart of symbols after parsing
            item_chart (list[list[dict[item, int]]]): chart of items after parsing
    """
    print(f"{'*'*30}\nParsing \"{sentence}\" with {productions}\n{'*'*30}") if debug else ""
    n = len(sentence)
    item_chart = [[{} for _ in range(n + 1)] for _ in range(n + 1)] # key: item, value: error metric
    symbol_chart = [[{} for _ in range(n + 1)] for _ in range(n + 1)] # key: symbol, value: error metric, tree

    fill_epsilon_diagonal(n, init_items, symbol_chart, item_chart, debug=debug, tabs=tabs)

    if debug:
        print(f"{'  ' * (tabs + 0)}Epsilon Diagonal Filled:")
        print(f"{'  ' * (tabs + 1)}Item Chart: {item_chart}")
        print(f"{'  ' * (tabs + 1)}Symbol Chart: {symbol_chart}")

    fill_diagonal(n, sentence, symbol_chart, item_chart, init_error=init_error, debug=debug, tabs=tabs)

    if debug:
        print(f"{'  ' * (tabs + 0)}First Diagonal Filled:")
        print(f"{'  ' * (tabs + 1)}Item Chart: {item_chart}")
        print(f"{'  ' * (tabs + 1)}Symbol Chart: {symbol_chart}")

    fill_rest(n, symbol_chart, item_chart, debug=debug, tabs=tabs)

    if debug:
        print(f"{'  ' * (tabs + 0)}rest filled")
        print(f"{'  ' * (tabs + 1)}Item Chart: {item_chart}")
        print(f"{'  ' * (tabs + 1)}Symbol Chart: {symbol_chart}")

    return (symbol_chart, item_chart)

def fill_epsilon_diagonal(n: int, init_items: list, symbol_chart: list, item_chart: list, debug: bool=False, tabs: int=0) -> None:
    """
    Fill in the first diagonal of the symbol and item charts inplace.

    Parameters:
        n (int): length of the sentence
        init_items (list[Item]): list of items (partially completed productions)
        symbol_chart (list[list[dict[str, int]]]): chart of symbols
        item_chart (list[list[dict[item, int]]]): chart of items
        debug (bool): whether or not to print a debug trace
        tabs (int): indentation for debug trace

    Returns:
        None
    """
    print(f"{'  ' * (tabs + 0)}Filling epsilon:") if debug else ""

    # add empty string as a symbol
    print(f"{'  ' * (tabs + 1)}Adding ():") if debug else ""
    closure_on_symbol(row=0, col=0, item_chart=item_chart, symbol_chart=symbol_chart, symbol=(), item=None, error=0, debug=debug, tabs=tabs+2)

    # add initial items and try to progress on the spot
    print(f"{'  ' * (tabs + 1)}Adding inital items:") if debug else ""
    for item in init_items:
        closure_on_item(row=0, col=0, item_chart=item_chart, symbol_chart=symbol_chart, item=item, error=0, debug=debug, tabs=tabs+2)

    # copy cell to the rest of the diagonal
    symbol_cell = symbol_chart[0][0]
    item_cell = item_chart[0][0]
    for row in range(n + 1):
        symbol_chart[row][row] = symbol_cell
        item_chart[row][row] = item_cell

    print(f"{'  ' * (tabs + 1)}Symbol Chart: {symbol_chart}") if debug else ""
    print(f"{'  ' * (tabs + 1)}Item Chart: {item_chart}") if debug else ""

def closure_on_symbol(row: int, col: int, item_chart: list[list[Item]],
                      symbol_chart: list[list[dict]], symbol: str, item: Item, error: int, debug: bool=False, tabs: int=0) -> None:
    """
    Perform a closure on a symbol. This is done by checking if any new items
    can be progressed or completed given the addition of the symbol at the
    given row/col.

    Parameters:
        row (int): row in symbol chart to add symbol
        col (int): int in symbol chart to add symbol
        item_chart (list[list[dict[item, int]]]): chart of items
        symbol_chart (list[list[dict[str, int]]]): chart of symbols
        symbol (str): symbol to add
        error (int): current error metric associated with symbol
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

    if symbol in symbol_chart[row][col]: # TODO: What about ambigious situations?
        print(f"{'  ' * (tabs + 1)}symbol in cell already") if debug else ""
        return

    if make_tree:
        if item == None:
            if symbol == ():
                symbol_tree = Tree(data="None", children=[])
            else:
                symbol_tree = Tree(data=symbol, children=[])
        else:
            symbol_tree = Tree(data=symbol, children=item.children)
    else:
        symbol_tree = None

    symbol_chart[row][col][symbol] = (error, symbol_tree)

    # generate list of productions from the epsilon diagonal that could progress
    new_items = dict(filter(lambda x: x[0] is not None, 
                            (map(lambda prev_item: (prev_item[0].progress(symbol, ((row, row), (row, col)), symbol_tree), prev_item[1] + error),
                                 item_chart[row][row].items()))))
    print(f"{'  ' * (tabs + 1)}New items from closure: {new_items}") if debug else ""

    # add new items to the item chart and perform the relevant closure
    for item, item_error in new_items.items():
        print(f"{'  ' * (tabs + 2)}Item: {item}") if debug else ""
        print(f"{'  ' * (tabs + 3)}Item completed: {item.completed()}") if debug else ""
        if item.completed(): # should just call closure on item, that will deal with the item being completed
            print(f"{'  ' * (tabs + 3)}Completes") if debug else ""
            # TODO: what if item already in chart? this should be taken out and we should do a closure on the item
            closure_on_item(row, col, item_chart, symbol_chart, item, error=item_error, debug=debug, tabs=tabs+4) # this line is new
            closure_on_symbol(row, col, item_chart, symbol_chart, symbol=item.production.lhs, item=item, error=item_error, debug=debug, tabs=tabs+4)
        else:
            print(f"{'  ' * (tabs + 3)}Progresses") if debug else ""
            closure_on_item(row, col, item_chart, symbol_chart, item, error=item_error, debug=debug, tabs=tabs+4)

def closure_on_item(row: int, col: int, item_chart: list, symbol_chart: list, item: Item, error: int, debug: bool=False, tabs: int=0) -> None:
    """
    Perform a closure on an item. This is done by checking if any symbols in
    the epsilon diagonal can progress the item that is to be added. i.e.
    tries to progress without moving forward in the chart

    Parameters:
        row (int): row in item chart to add item
        col (int): int in item chart to add item
        item_chart (list[list[dict[item, int]]]): chart of items
        symbol_chart (list[list[dict[str, int]]]): chart of symbols
        item (Item): item to add
        error (int): current error metric associated with symbol
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

    if item in item_chart[row][col]:
        print(f"{'  ' * (tabs + 1)}Item in item chart") if debug else ""
        # TODO: check if error is less and update? then i'd need to recheck everything?
        return

    # add item to item chart
    item_chart[row][col][item] = error
    print(f"{'  ' * (tabs + 1)}Item added to item chart") if debug else ""

    cell_on_diagonal = symbol_chart[col][col]

    # check if item can progress on the spot, perform closure if so
    # TODO: add empty string to tree in this case??
    next_symbol = item.get_next_symbol()
    if next_symbol in cell_on_diagonal:
        print(f"{'  ' * (tabs + 1)}Item Can Progress") if debug else ""
        symbol_tree = cell_on_diagonal[next_symbol][1]

        new_item = item.progress(next_symbol, split=((row, col), (col, col)), symbol_tree=symbol_tree)
        new_item_error = error + cell_on_diagonal[next_symbol][0]
        if new_item.completed():
            print(f"{'  ' * (tabs + 1)}Item Completes") if debug else ""
            # item_chart[row][col][new_item] = new_item_error
            closure_on_item(row, col, item_chart, symbol_chart, item=new_item, error=new_item_error, debug=debug, tabs=tabs+2)
            closure_on_symbol(row, col, item_chart, symbol_chart, item.production.lhs, new_item, new_item_error, debug=debug, tabs=tabs+2)
        else:
            print(f"{'  ' * (tabs + 1)}Item does not Completes") if debug else ""
            closure_on_item(row, col, item_chart, symbol_chart, item=new_item, error=new_item_error, debug=debug, tabs=tabs+2)

def fill_diagonal(n: int, sentence: str, symbol_chart: list, item_chart: list, init_error: int=0, debug: bool=False, tabs: int=0) -> None:
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

        closure_on_symbol(row, col, item_chart, symbol_chart, symbol, item=None, error=init_error, debug=debug, tabs=tabs+1)

def fill_rest(n: int, symbol_chart: list, item_chart: list, debug: bool=False, tabs: int=0) -> None:
    """
    Fill in remaining diagonals apart from the epsilon and first diagonal.

    Parameters:
        n (int): length of the sentence
        symbol_chart (list[list[dict[str, int]]]): chart of symbols
        item_chart (list[list[dict[item, int]]]): chart of items
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
                    symbol_cell = symbol_chart[sym_row][sym_col]
                    next_symbol = item.get_next_symbol()
                    if next_symbol in symbol_cell:
                        new_item_error = item_error + symbol_cell[next_symbol][0]
                        symbol_tree = symbol_cell[next_symbol][1]
                        new_item = item.progress(next_symbol, split=((item_row, item_col), (sym_row, sym_col)), symbol_tree=symbol_tree)
                        if new_item.completed(): 
                            print(f"{'  ' * (tabs + 4)}Item Completes, adding {item.production.lhs} to symbol chart") if debug else ""
                            item_chart[row][col][new_item] = new_item_error
                            closure_on_symbol(row, col, item_chart, symbol_chart, item.production.lhs, new_item, new_item_error, debug=debug, tabs=tabs+5)
                            print(f"{'  ' * (tabs + 4)}Symbol Chart: {symbol_chart}") if debug else ""
                            print(f"{'  ' * (tabs + 4)}Item Chart: {item_chart}") if debug else ""
                        else:
                            closure_on_item(row, col, item_chart, symbol_chart, new_item, new_item_error, debug=debug, tabs=tabs+5)
                            print(f"{'  ' * (tabs + 4)}Item progressing, adding {new_item} to item chart") if debug else ""
                            print(f"{'  ' * (tabs + 4)}Item Chart: {item_chart}") if debug else ""
                            print(f"{'  ' * (tabs + 4)}Symbol Chart: {symbol_chart}") if debug else ""
