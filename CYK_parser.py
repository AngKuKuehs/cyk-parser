import json

from Item import Item
from Production import Production

def load_productions_from_json(path: str, debug: bool=False, tabs: int=0) -> dict:
    """Loads a dictionary of productions from a json file.

    Parameters:
        path (str): path to the json file with productions

    Returns:
        tuple:
            productions (dict): productions specified from json file, key: lhs, value: rhs
            init_items (list): list of initial items
    """
    print(f"{'  ' * tabs}Loading {path}") if debug else ""
    with open(path) as f:
       production_file = (json.load(f))
    print(f"{'  ' * tabs}Production File: {production_file}") if debug else ""
    productions = {}
    init_items = []
    for lhs, values in production_file.items():
        for rhs in values:
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


def parse(sentence: str, productions: dict, init_items: list, debug: bool=False, tabs: int=0) -> tuple:
    print(f"{'*'*30}\nParsing \"{sentence}\" with {productions}\n{'*'*30}") if debug else ""
    n = len(sentence)
    item_chart = [[set() for _ in range(n + 1)] for _ in range(n + 1)] # set of items
    symbol_chart = [[{} for _ in range(n + 1)] for _ in range(n + 1)] # key: symbol, value: error metric

    fill_epsilon_diagonal(n, init_items, symbol_chart, item_chart, debug=debug, tabs=tabs)

    if debug:
        print(f"{'  ' * (tabs + 0)}Epsilon Diagonal Filled:")
        print(f"{'  ' * (tabs + 1)}item_chart: {item_chart}")
        print(f"{'  ' * (tabs + 1)}symbol_chart: {symbol_chart}")

    fill_diagonal(n, sentence, symbol_chart, item_chart, debug=debug, tabs=tabs)

    if debug:
        print(f"{'  ' * (tabs + 0)}First Diagonal Filled:")
        print(f"{'  ' * (tabs + 1)}item_chart: {item_chart}")
        print(f"{'  ' * (tabs + 1)}symbol_chart: {symbol_chart}")

    fill_rest(n, symbol_chart, item_chart, debug=debug, tabs=tabs)

    if debug:
        print(f"{'  ' * (tabs + 0)}rest filled")
        print(f"{'  ' * (tabs + 1)}item_chart: {item_chart}")
        print(f"{'  ' * (tabs + 1)}symbol_chart: {symbol_chart}")

    return (symbol_chart, item_chart)

def fill_epsilon_diagonal(n: int, init_items: list, symbol_chart: list, item_chart: list, debug: bool=False, tabs: int=0) -> None:
    print(f"{'  ' * (tabs + 0)}Filling epsilon:") if debug else ""
    print(f"{'  ' * (tabs + 1)}Adding ():") if debug else ""
    closure_on_symbol(0, 0, item_chart, symbol_chart, (), 0, debug=debug, tabs=tabs+2)
    print(f"{'  ' * (tabs + 1)}Adding inital items:") if debug else ""
    for item in init_items:
        closure_on_item(0, 0, item_chart, symbol_chart, item, debug=debug, tabs=tabs+2)

    symbol_cell = symbol_chart[0][0]
    item_cell = item_chart[0][0]
    for row in range(n + 1):
        symbol_chart[row][row] = symbol_cell
        item_chart[row][row] = item_cell

    print(f"{'  ' * (tabs + 1)}symbol_chart: {symbol_chart}") if debug else ""
    print(f"{'  ' * (tabs + 1)}item_chart: {item_chart}") if debug else ""

def closure_on_symbol(row: int, col: int, item_chart: list[list[Item]],
                      symbol_chart: list[list[dict]], symbol: str, error: int, debug: bool=False, tabs: int=0) -> None:
    if debug:
        print(f"{'  ' * (tabs + 0)}Closure on '{symbol}' at {row}, {col}")
        print(f"{'  ' * (tabs + 1)}Symbol Chart: {symbol_chart}")
        print(f"{'  ' * (tabs + 1)}Symbol Chart Cell: {symbol_chart[row][col]}")

    if symbol in symbol_chart[row][col]:
        print(f"{'  ' * (tabs + 1)}symbol in cell already") if debug else ""
        return

    symbol_chart[row][col][symbol] = error
    print(f"{'  ' * (tabs + 1)}Symbol added to cell") if debug else ""
    new_items = list(filter(lambda x: x is not None, map(lambda x: x.progress(symbol, error), item_chart[row][row])))
    print(f"{'  ' * (tabs + 1)}New items from closure: {new_items}") if debug else ""
    for item in new_items:
        print(f"{'  ' * (tabs + 2)}Item: {item}") if debug else ""
        print(f"{'  ' * (tabs + 3)}Item completed: {item.completed()}") if debug else ""
        if item.completed():
            print(f"{'  ' * (tabs + 3)}Completes") if debug else ""
            item_chart[row][col].add(item)
            closure_on_symbol(row, col, item_chart, symbol_chart, item.production.lhs, item.metric + error, debug=debug, tabs=tabs+4)
        else:
            print(f"{'  ' * (tabs + 3)}Progresses") if debug else ""
            closure_on_item(row, col, item_chart, symbol_chart, item, debug=debug, tabs=tabs+4)

def closure_on_item(row: int, col: int, item_chart: list, symbol_chart: list, item: Item, debug: bool=False, tabs: int=0) -> None:
    if debug:
        print(f"{'  ' * (tabs + 0)}Closure on '{item}' at {row}, {col}")
        print(f"{'  ' * (tabs + 1)}Item Chart: {item_chart}")
        print(f"{'  ' * (tabs + 1)}Item Chart Cell: {item_chart[row][col]}")

    if item in item_chart[row][col]:
        print(f"{'  ' * (tabs + 1)}Item in item chart") if debug else ""
        return

    item_chart[row][col].add(item)
    print(f"{'  ' * (tabs + 1)}Item added to item chart") if debug else ""
    cell_on_diagonal = symbol_chart[col][col]
    if item.get_next_symbol() in cell_on_diagonal:
        print(f"{'  ' * (tabs + 1)}Item Can Progress") if debug else ""
        new_item = item.progress(item.get_next_symbol(), cell_on_diagonal[item.get_next_symbol()])
        if new_item.completed():
            print(f"{'  ' * (tabs + 1)}Item Completes") if debug else ""
            item_chart[row][col].add(new_item)
            closure_on_symbol(row, col, item_chart, symbol_chart, item.production.lhs, item.metric + cell_on_diagonal[item.get_next_symbol()], debug=debug, tabs=tabs+2)
        else:
            print(f"{'  ' * (tabs + 1)}Item does not Completes") if debug else ""
            closure_on_item(row, col, item_chart, symbol_chart, new_item, debug=debug,tabs=tabs+2)


def fill_diagonal(n: int, sentence: str, symbol_chart: list, item_chart: list, debug: bool=False, tabs: int=0) -> None:
    print(f"{'  ' * (tabs + 0)}Filling first diagonal") if debug else ""
    for row in range(n):
        col = row + 1
        symbol = sentence[row]
        closure_on_symbol(row, col, item_chart, symbol_chart, symbol, 0, debug=debug, tabs=tabs+1)

def fill_rest(n: int, symbol_chart: list, item_chart: list, debug: bool=False, tabs: int=0) -> None:
    print(f"{'  ' * (tabs + 0)}Filling rest:") if debug else ""
    for length in range(1, n):
        print(f"{'  ' * (tabs + 1)}length: {length}") if debug else ""
        for row in range(0, n - length):
            col = row + length + 1
            print(f"{'  ' * (tabs + 2)}row, col: {row, col}") if debug else ""
            for split in range(1, length + 1): # does this need to be in a certain order?
                print(f"{'  ' * (tabs + 3)}split: {split}") if debug else ""
                item_row = row
                item_col = col - split
                sym_row = col - split
                sym_col = col
                for item in item_chart[item_row][item_col]:
                    print(f"{'  ' * (tabs + 4)}Item: {item}") if debug else ""
                    symbol_cell = symbol_chart[sym_row][sym_col]
                    if item.get_next_symbol() in symbol_cell:
                        new_item = item.progress(item.get_next_symbol(), symbol_cell[item.get_next_symbol()])
                        if new_item.completed(): 
                            print(f"{'  ' * (tabs + 4)}Item Completes, adding {item.production.lhs} to symbol chart") if debug else ""
                            item_chart[row][col].add(new_item)
                            closure_on_symbol(row, col, item_chart, symbol_chart, item.production.lhs, item.metric + symbol_cell[item.get_next_symbol()], debug=debug, tabs=tabs+5)
                            print(f"{'  ' * (tabs + 4)}Symbol Chart: {symbol_chart}") if debug else ""
                        else:
                            closure_on_item(row, col, item_chart, symbol_chart, new_item, debug=debug, tabs=tabs+5)
                            print(f"{'  ' * (tabs + 4)}Item progressing, adding {new_item} to item chart") if debug else ""
                            print(f"{'  ' * (tabs + 4)}Item Chart: {item_chart}") if debug else ""
