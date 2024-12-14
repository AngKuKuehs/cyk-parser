import graphviz
from lark.tree import Tree
from lark.lexer import Token

def read(fn, *args):
    kwargs = {'encoding': 'iso-8859-1'}
    with open(fn, *args, **kwargs) as f:
        return f.read()

def trim_children(children):
    trimmed_children = []
    for tree in children:
        trim = trim_children(tree.children)
        if tree.data[0:2] == "__":
            trimmed_children += trim_children(tree.children)
        else:
            trimmed_children.append(Tree(tree.data, trim))
    return trimmed_children

def save_tree(tree, path):
    counter = 0
    dot = graphviz.Digraph(comment="Tree")
    if isinstance(tree.data, Token):
        dot.node(str(counter), repr(tree.data.value))
    else:
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
                node_val = child.data
                if isinstance(node_val, Token):
                    if node_val.type == "RULE":
                        node_val = node_val.value
                    else:
                        node_val = node_val.type
                dot.node(str(counter), repr(node_val))
                if child.children:
                    children_stack.append((str(counter), child.children))
            else:
                node_val = child
                if isinstance(node_val, Token):
                    if node_val.type == "RULE":
                        node_val = node_val.value
                    else:
                        node_val = node_val.type
                # create new node
                dot.node(str(counter), repr(node_val))
            # connect new node to parent
            dot.edge(parent, str(counter))
        # get next node
        if children_stack:
            parent, curr_children = children_stack.pop()
        else:
            curr_children = None
    # write tree to file
    dot.render(path)

