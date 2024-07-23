from Production import Production

class Item():
    def __init__(self, production: Production, dot: int, metric: int):
        self.production = production # contains lhs, rhs, and name
        self.dot = dot
        self.metric = metric

    def completed(self):
        "Returns True if item is completed, False otherwise."
        return self.dot == len(self.production.rhs)
    
    def next_symbol(self):
        if self.dot < len(self.production.rhs):
            return self.production.rhs[self.dot]
        else:
            return None

    def next_item(self, metric):
        return Item(self.production, self.dot + 1, self.metric + metric)

    def progress(self, symbol, metric):
        if symbol == self.next_symbol():
            return Item(self.production, self.dot + 1, self.metric + metric)
        else:
            return None

    def signature(self):
        return f"{self.production.lhs}, {self.production.rhs}, {self.dot}"

    def __hash__(self) -> int:
        return hash(self.signature())

    def __eq__(self, value: object) -> bool:
        return self.signature() == value.signature()

    def __str__(self):
        return f"{self.production.lhs} -> {self.production.rhs[:self.dot]}⋅{self.production.rhs[self.dot:]}"

    def __repr__(self):
        return f"{self.production.lhs} -> {self.production.rhs[:self.dot]}⋅{self.production.rhs[self.dot:]}"
