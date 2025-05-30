from dataclasses import dataclass

from lark.tree import Tree

from item import Item
from symbol import Symbol

@dataclass
class MidDelParams():
    item: Item
    item_error: int
    symbol: Symbol
    symbol_error: int
    symbol_tree: Tree
    deletion_count: int

@dataclass
class StdParams():
    item: Item
    item_error: int
    symbol: Symbol
    symbol_error: int
    symbol_tree: Tree

@dataclass
class FrontEndDelParams():
    front_deletions: int
    end_deletions: int
    root_error: int
    parse_tree: int

# Simple metric combiners
def simple_del_addition(params: MidDelParams):
    return params.item_error + params.symbol_error + params.deletion_count

def simple_std_addition(params: StdParams):
    return params.item_error + params.symbol_error

def simple_front_end_del_addition(params: FrontEndDelParams):
    return params.front_deletions + params.end_deletions + params.root_error

# track insertions
def track_ins_del_addition(params: MidDelParams):
    e1 = params.item_error[0] + params.symbol_error[0] + params.deletion_count
    e2 = params.item_error[1] + params.symbol_error[1]
    return (e1, e2)

def track_ins_std_addition(params: StdParams):
    e1 = params.item_error[0] + params.symbol_error[0]
    e2 = params.item_error[1] + params.symbol_error[1]
    return (e1, e2)

def track_ins_front_end_del_addition(params: FrontEndDelParams):
    e1 = params.front_deletions + params.end_deletions + params.root_error[0]
    e2 = params.root_error[1]
    return e1, e2
