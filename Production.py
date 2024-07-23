import Item

class Production():
    def __init__(self, lhs: str, rhs: list, name=None):
        self.lhs = lhs
        self.rhs = rhs
        self.name = name

    def create_init_item(self):
        return Item.Item(production=self, dot=0, metric=0)

    def __repr__(self) -> str:
        if self.name:
            return f"{self.name}: {self.lhs} -> {self.rhs}"
        else:
            return f"{self.lhs} -> {self.rhs}"

    def __str__(self) -> str:
        if self.name:
            return f"{self.name}: {self.lhs} -> {self.rhs}"
        else:
            return f"{self.lhs} -> {self.rhs}"
