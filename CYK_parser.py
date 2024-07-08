import json

from Item import Item

debug = False

def load_grammar_from_json(path: str) -> list:
    print(f"Loading {path}") if debug else ""
    with open(path) as f:
       productions = (json.load(f))
    print(f"\tproductions: {productions}") if debug else ""
    grammar = []
    for key, values in productions.items():
        for value in values:
            if type(value) == dict:
                for name, result in value.items():
                    print(f"name: {name}, result: {result}") if debug else ""
                    item = Item(start=key, result=tuple(result), state=0, error_metric=0, next_symbol=result[0] if result else (), name=name)
                    grammar.append(item)
            else:
                item = Item(start=key, result=tuple(value), state=0, error_metric=0, next_symbol=value[0] if value else ())
                grammar.append(item)
    print(f"\tGrammar: {grammar}") if debug else ""
    return grammar

def saturate(row: int, col: int, grammar: list, symbol_chart: list, item_chart: list) -> None:
    add_to_symbols = True
    while add_to_symbols:
        add_to_symbols = False
        for item in grammar:
            print(f"\tItem: {item}") if debug else ""
            symbol_cell = symbol_chart[row][col]
            if item.next_symbol in symbol_cell:
                if item.completes() and item.start not in symbol_cell:
                    print(f"\t\tItem Completes, adding {item.start} to symbol chart") if debug else ""
                    symbol_chart[row][col][item.start] = 0
                    add_to_symbols = True
                    print(f"\t\t\tSymbol Chart: {symbol_chart}") if debug else ""
                elif item.signature not in item_chart[row][col] and not item.completes():
                    new_item = Item(item.start, item.result, item.state + 1, item.error_metric, item.result[item.state + 1], item.name)
                    print(f"\t\tItem progressing, adding {new_item} to item chart") if debug else ""
                    item_chart[row][col][new_item.signature] = new_item
                    print(f"\t\t\tItem Chart: {item_chart}") if debug else ""

def fill_diagonal(n: int, sentence: str, grammar: list, symbol_chart: list, item_chart: list) -> None:
    for row in range(n):
        col = row + 1
        curr_token = sentence[row]
        symbol_chart[row][col][curr_token] = 0
        print(f"Saturating: {(row, col)}") if debug else ""
        saturate(row, col, grammar, symbol_chart, item_chart)

def fill_rest(n: int, grammar: list, symbol_chart: list, item_chart: list) -> None:
    for length in range(1, n):
        print(f"\tlength: {length}") if debug else ""
        for row in range(0, n - length):
            col = row + length + 1
            print(f"\t\trow, col: {row, col}") if debug else ""
            for split in range(1, length + 1):
                print(f"\t\t\tsplit: {split}") if debug else ""
                item_row = row
                item_col = col - split
                sym_row = col - split
                sym_col = col
                for item in item_chart[item_row][item_col].values():
                    print(f"\t\t\t\tItem: {item}") if debug else ""
                    symbol_cell = symbol_chart[sym_row][sym_col]
                    if item.next_symbol in symbol_cell:
                        if item.completes(): 
                            print(f"\t\t\t\tItem Completes, adding {item.start} to symbol chart") if debug else ""
                            symbol_chart[row][col][item.start] = item.error_metric + symbol_cell[item.next_symbol]
                            print(f"\t\t\t\tSymbol Chart: {symbol_chart}") if debug else ""
                        else:
                            new_item = Item(item.start, item.result, item.state + 1, item.error_metric, item.result[item.state + 1])
                            item_chart[row][col][new_item.signature] = new_item
                            print(f"\t\tItem progressing, adding {new_item} to item chart") if debug else ""
                            print(f"\t\tItem Chart: {item_chart}") if debug else ""
                saturate(row, col, grammar, symbol_chart, item_chart)

def parse(sentence: str, grammar: list) -> tuple:
    print(f"{'*'*30}\nParsing \"{sentence}\" with {grammar}\n{'*'*30}") if debug else ""
    n = len(sentence)
    item_chart = [[{} for _ in range(n + 1)] for _ in range(n + 1)]
    symbol_chart = [[{} for _ in range(n + 1)] for _ in range(n + 1)]

    fill_diagonal(n, sentence, grammar, symbol_chart, item_chart)
    if debug:
        print("first diagonal filled")
        print(f"\titem_chart: {item_chart}")
        print(f"\tsymbol_chart: {symbol_chart}")

    fill_rest(n, grammar, symbol_chart, item_chart)
    if debug:
        print("rest filled")
        print(f"\titem_chart: {item_chart}")
        print(f"\tsymbol_chart: {symbol_chart}")

    return (symbol_chart, item_chart)
