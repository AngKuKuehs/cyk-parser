from production import Production

class Item():
    def __init__(self, production: Production, dot: int, split: tuple[tuple[int, int], tuple[int, int]]): # does hash 
        self.production = production # contains lhs, rhs, and name
        self.dot = dot
        self.split = split
        self.children = [] # list of symbol trees, the roots of which progress this item in order

    def completed(self):
        """
        Checks if this instance of the Item has been completed.

        Parameters:
            self (Item): instance of Item

        Returns:
            Bool: True if this item is completed, False otherwise
        """
        return self.dot == len(self.production.rhs)
    
    def get_next_symbol(self):
        """
        Gets the next symbol needed to progress this instance of Item. Returns None if item is completed.

        Parameters:
            self (Item): instance of Item

        Returns:
            str | None: Returns next symbol as a string or None if the item is completed.
        """
        if self.dot < len(self.production.rhs):
            return self.production.rhs[self.dot]
        else:
            return None

    def progress(self, symbol, split, symbol_tree):
        """
        Progresses the item if the string provided is matches the next symbol needed to progress the item.

        Parameters:
            self (Item): instance of Item
            symbol (str): the symbol which may progress the item
            split (tuple[tuple[int, int], tuple[int, int]]): row and col of the item and symbol which last progressed it respectively
            symbol_tree (Tree | None): symbol tree of symbol param or None if make_tree is False

        Returns:
            str | None: Returns next symbol as a string or None if the item is completed.
        """
        if symbol == self.get_next_symbol():
            new_item = Item(self.production, self.dot + 1, split)
            if symbol_tree:
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
