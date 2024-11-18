# CYK-Parser
Python Implementation of an error-correcting CYK parser with items and error metrics.

## Grammar Schema
Each grammar taken in by the parser must be written in a JSON format.

This format is a dictionary where the key is the starting symbol of a production while the value is a list whose first element is a dictionary of named productions (key: production name, value: prodcution result) and whose subsequent elements are a list of unnamed production results.

Production results are always stored in a list where each element of that list is a symbol of the result.

The empty string is represented by []

e.g.:
```
{
    "Start": [{"rule_1": ["A", "B"], "rule_2": ["C"]}, []],
    "A": [{"rule_3": ["B", "C"]}, ["a"]],
    "B": [{}, ["b"]],
    "C": [{"c_self": ["c"]}]
}
```

## Algorithm
```
input: string of terminals, s, with length of n.
input: list of tuples of productions rules, g, in the form ("A", "BC", Error Metric) for A -> BC

init a n by n by n list of list of [], item_chart, where each element is a tuple (Start, Result, State, Error Metric) e.g. (A, BC, 1, 0) for A -> B•C or 
init a n by n list of list of n maps, symbol_chart, where each key-value pair is a parsed symbol and its corresponding error metric

iterate i through through the range of 0 to n:
    add s[i] to symbol_chart[i][i]
    init a bool, add_to_symbols, and set to True
    while add_to_symbols:
        set add_to_symbol to False
        iterate through items in g:
            if first element of the item's Result is in symbol_chart[i][i] and the item's start is not in symbol_chart[i][i]:
                if Result has length of 1:
                    add Result to symbol_chart[i][i]
                    set add_to_symbols to True
                else if new item is not already in item_chart:
                    add (item start, item result, 1, item error metric) into item_chart

iterate skip through the range 1 to n:
    iterate row through the range of 0 to n - skip:
        set curr_cell to (row, row + skip)
        iterate i through the range of 1 to skip + 1: # get all combinations that can reach current cell
            set prev_items_cell to (curr_cell[0], curr_cell[1] - i)
            set prev_symbol_cell to (curr_cell[0] - (skip + 1 - i), curr_cell[1])

            # Add to curr_cell items/symbols from previous cells
            iterate through each item in item_chart[prev_item_cell[0]][prev_item_cell[1]]:
                if any symbols in symbol_chart[prev_symbol_cell[0]][prev_symbol_cell[1]] can progress item:
                    if item can be completed:
                        set add_to_symbols to True
                        add symbol to symbol_chart[curr_cell[0]][curr_cell[1]] with error metric
                    else:
                        add updated item to item_chart[curr_cell[0]][curr_cell[1]] like (Start, Result, state + 1, error_metric)

        # Add from all production rules based on symbols in curr_cell and rules from g
        while add_to_symbols:
            set add_to_symbol to False
            iterate through items in g:
                if first element of the item's Result is in symbol_chart[i][i] and the item's start is not in symbol_chart[i][i]:
                    if Result has length of 1:
                        add Result to symbol_chart[i][i]
                        set add_to_symbols to True
                    else if new item is not already in item_chart:
                        add (item start, item result, 1, item error metric) into item_chart

check if symbol_chart[0][n - 1] has starting symbol
```