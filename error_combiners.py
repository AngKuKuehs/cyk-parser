from item import Item
from symbol import Symbol

# TODO: Think about other things to add as well => the symbol itself? insertion count?

def simple_del_addition(item_error: int, item: Item, symbol_error: int, symbol: Symbol,  deletion_count: int):
    return item_error + symbol_error + deletion_count

def simple_ins_addition(item_error: int, item: Item, symbol_error: int, symbol: Symbol):
    return item_error + symbol_error

def simple_std_addition(item_error: int, item: Item, symbol_error: int, symbol: Symbol):
    return item_error + symbol_error

