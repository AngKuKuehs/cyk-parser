import graphviz
from lark.tree import Tree

def read(fn, *args):
    kwargs = {'encoding': 'iso-8859-1'}
    with open(fn, *args, **kwargs) as f:
        return f.read()

def save_tree(tree, path):
    counter = 0
    dot = graphviz.Digraph(comment="Tree")
    dot.node(str(counter), repr(tree.data))
    
    parent = "0"
    curr_children = tree.children
    children_stack = []
    while curr_children:
        # iterate through children of current node
        for child in curr_children:
            counter += 1
            if isinstance(child, Tree):
                # create new node and add children to of new node to curr_children
                dot.node(str(counter), repr(child.data))
                if child.children:
                    children_stack.append((str(counter), child.children))
            else:
                # create new node
                dot.node(str(counter), repr(child))
            # connect new node to parent
            dot.edge(parent, str(counter))
        # get next node
        if children_stack:
            parent, curr_children = children_stack.pop()
        else:
            curr_children = None
    # write tree to file
    dot.render(path)