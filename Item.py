class Item():
    def __init__(self, start, result, state, error_metric, next_symbol, name=None):
        self.start = start
        self.result = result
        self.state = state
        self.error_metric = error_metric
        self.next_symbol = next_symbol
        self.signature = (self.start, self.result, self.state)
        self.name=None
    
    def __str__(self):
        return f"{self.start} -> {self.result[:self.state]}⋅{self.result[self.state:]}"

    def __repr__(self):
        return f"{self.start} -> {self.result[:self.state]}⋅{self.result[self.state:]}"

    def completes(self):
        "Returns True if progressing the item by 1 symbol will complete it, False otherwise."
        if self.state + 1 == len(self.result):
            return True
        return False
