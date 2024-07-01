import json

def load_grammar_from_json(path: str) -> dict:
    with open(path) as f:
       productions = (json.load(f))
    result = []
    for key, values in productions.items():
        for value in values:
            result.append((key, value))
    # print(result)
    return result

def parse(sentence: str, grammar: dict) -> bool:
    # print(f"Sentence: {sentence}")
    n = len(sentence)
    item_chart = [[[] for _ in range(n)] for _ in range(n)]
    symbol_chart = [[{} for _ in range(n)] for _ in range(n)]
    # print(f"item_chart: {item_chart}")
    # print(f"symbol_chart: {symbol_chart}")
    for i in range(n):
        symbol_chart[i][i][sentence[i]] = 0
        # print(f"current i: {i}")
        add_to_symbols = True
        while add_to_symbols:
            add_to_symbols = False
            for rule in grammar:
                # print(f"rule: {rule}")
                if rule[1][0] in symbol_chart[i][i]:
                    # print(f"\tCan progress")
                    if len(rule[1]) == 1  and rule[0] not in symbol_chart[i][i]:
                        # print(f"\t\tadding to symbol chart: {rule[0], 0}")
                        symbol_chart[i][i][rule[0]] = 0
                        add_to_symbols = True
                    elif (rule[0], rule[1], 1, 0) not in item_chart[i][i] and len(rule[1]) != 1:
                        item = (rule[0], rule[1], 1, 0)
                        # print(f"\t\titem to append to item_chart at {i, i}")
                        # print(f"\t\t\titem: {item}")
                        item_chart[i][i].append(item)
                        # print(f"\t\tupdated item_chart: {item_chart}")

    for skip in range(1, n):
        # print(f"item_chart: {item_chart}")
        # print(f"symbol_chart: {symbol_chart}")
        # print(f"skip: {skip}")
        for row in range(0, n - skip):
            # print(f"\trow: {row}")
            curr_cell = (row, row + skip)
            # print(f"\tcurr_cell: {curr_cell}")
            for i in range(1, skip + 1):
                # print(f"\t\ti: {i}")
                prev_item_cell = (curr_cell[0], curr_cell[1] - i)
                prev_symbol_cell = (curr_cell[0] + (skip + 1 - i), curr_cell[1])
                # print(f"\t\tprev_item_cell: {prev_item_cell}")
                # print(f"\t\tprev_symbol_cell: {prev_symbol_cell}")
                for item in item_chart[prev_item_cell[0]][prev_item_cell[1]]:
                    # print(f"\t\titem: {item}")
                    progress_char = item[1][item[2]]
                    # print(f"\t\t\tprogress_char: {progress_char}")
                    prev_symbols = symbol_chart[prev_symbol_cell[0]][prev_symbol_cell[1]]
                    if progress_char in prev_symbols:
                        # print(f"\t\t\t\t Progress char found")
                        if item[2] + 1 == len(item[1]):
                            # # print(f"\t\t\t\t\titem can be completed! add to prev_symbols")
                            symbol_chart[curr_cell[0]][curr_cell[1]][item[0]] = item[3] + prev_symbols[progress_char]
                            add_to_symbols = True
                        else:
                            new_item = (item[0], item[1], item[2] + 1, item[3])
                            item_chart[curr_cell[0]][curr_cell[1]].append(new_item)

                while add_to_symbols:
                    add_to_symbols = False
                    curr_symbols = symbol_chart[curr_cell[0]][curr_cell[1]]
                    for rule in grammar:
                        if rule[1][0] in curr_symbols:
                            if len(rule[1]) == 1 and rule[0] not in curr_symbols:
                                symbol_chart[curr_cell[0]][curr_cell[1]][rule[0]] = 0
                                curr_symbols = symbol_chart[curr_cell[0]][curr_cell[1]]
                                add_to_symbols = True
                            elif (rule[0], rule[1], 1, 0) not in item_chart[curr_cell[0]][curr_cell[1]] and len(rule[1]) != 1:
                                item = (rule[0], rule[1], 1, 0)
                                item_chart[curr_cell[0]][curr_cell[1]].append(item)

    return (symbol_chart, item_chart)
