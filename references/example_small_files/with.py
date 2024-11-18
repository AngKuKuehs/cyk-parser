class GiveTuple(object):
    def __init__(self, item1, item2):
        self.item1 = item1
        self.item2 = item2
    
    def __enter__(self):
        return (self.item1, self.item2)

    def __exit__(self, *args):
        return

with GiveTuple('a', 'b') as item1:
    print(item1)

with GiveTuple('a', 'b') as (item1, item2):
    print(item1, item2)
