
class Symbol():
    def __init__(self, origin: str, value: str, error: int, row: int, col:int, sentence_val: str=None):
        self.origin = origin # sentence, parsed, deleted
        self.value = value
        self.error = error # need to display in tree
        self.row = row
        self.col = col
        if sentence_val:
            self.sentence_val = sentence_val # value of terminal in string

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, value):
        if isinstance(value, Symbol):
            return value.value == self.value
        if isinstance(value, str):
            return value == self.value
        if value == ():
            return self.value == ()
        if value == None:
            return False
        err_msg = f"Comparing Symbol with {type(value)} not allowed"
        raise TypeError(err_msg)

    def __str__(self):
        sentence_val = ""
        if hasattr(self, "sentence_val"):
            sentence_val = f": {self.sentence_val}"
        return f"Symbol(:'{self.value}'{sentence_val}, {self.error})"

    def __repr__(self):
        sentence_val = ""
        if hasattr(self, "sentence_val"):
            sentence_val = f": {self.sentence_val}"
        return f"Symbol('{self.value}'{sentence_val}, {self.error})"
