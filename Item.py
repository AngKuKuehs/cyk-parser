from Production import Production
#TODO: Remove metric from here, have it in item chart instead
class Item():
    def __init__(self, production: Production, dot: int, metric: int): # does hash 
        self.production = production # contains lhs, rhs, and name
        self.dot = dot
        self.metric = metric

    def completed(self):
        "Returns True if item is completed, False otherwise."
        return self.dot == len(self.production.rhs)
    
    def get_next_symbol(self):
        if self.dot < len(self.production.rhs):
            return self.production.rhs[self.dot]
        else:
            return None

    def progress(self, symbol, metric):
        if symbol == self.get_next_symbol():
            return Item(self.production, self.dot + 1, self.metric + metric)
        else:
            return None

    def __hash__(self) -> int:
        return hash((self.production, self.dot))

    def __eq__(self, value: object) -> bool:
        return (self.production, self.dot) == (value.production, value.dot)

    def __str__(self):
        return f"{self.production.lhs} -> {self.production.rhs[:self.dot]}⋅{self.production.rhs[self.dot:]}"

    def __repr__(self):
        return f"{self.production.lhs} -> {self.production.rhs[:self.dot]}⋅{self.production.rhs[self.dot:]}"
