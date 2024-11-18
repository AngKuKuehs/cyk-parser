from production import Production

class Item():
    def __init__(self, production: Production, dot: int, split: tuple[tuple[int, int], tuple[int, int]]): # does hash 
        self.production = production # contains lhs, rhs, and name
        self.dot = dot
        self.split = split
        self.children = [] # add symbols which progress item here

    def completed(self):
        "Returns True if item is completed, False otherwise."
        return self.dot == len(self.production.rhs)
    
    def get_next_symbol(self):
        if self.dot < len(self.production.rhs):
            return self.production.rhs[self.dot]
        else:
            return None

    def progress(self, symbol, split, symbol_tree):
        if symbol == self.get_next_symbol():
            new_item = Item(self.production, self.dot + 1, split)
            new_item.children += self.children
            new_item.children.append(symbol_tree)
            
            return new_item
        else:
            return None

    def __hash__(self) -> int: # add split here? to hash function
        return hash((self.production, self.dot))

    # TODO: include the split in the equality (note: don't include children, eq will become exp)
    def __eq__(self, value: object) -> bool:
        if value == None: # is this dodgy?
            return False
        return (self.production, self.dot, self.split) == (value.production, value.dot, value.split)

    def __str__(self):
        return f"{self.production.lhs} -> {self.production.rhs[:self.dot]}⋅{self.production.rhs[self.dot:]}"

    def __repr__(self):
        return f"{self.production.lhs} -> {self.production.rhs[:self.dot]}⋅{self.production.rhs[self.dot:]}"
