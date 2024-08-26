import item

class Production():
    def __init__(self, lhs: str, rhs: list, name=None):
        self.lhs = lhs
        self.rhs = rhs
        self.name = name

    def create_init_item(self):
        return item.Item(production=self, dot=0)
    
    def __hash__(self) -> int:
        return hash((self.lhs, tuple(self.rhs), self.name))

    def __eq__(self, value: object) -> bool:
        return (self.lhs, tuple(self.rhs), self.name) == (value.lhs, value.rhs, value.name)

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
