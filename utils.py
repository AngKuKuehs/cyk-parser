import os
from charset_normalizer import detect

import graphviz
from lark.tree import Tree
from lark.lexer import Token

from symbol import Symbol

def read(fn, *args):
    kwargs = {'encoding': 'iso-8859-1'}
    with open(fn, *args, **kwargs) as f:
        return f.read()

def trim_children(children):
    """
    recursively removes terminals that start with '__' and "None"
    terminals
    """
    trimmed_children = []
    for tree in children:
        curr_val = tree.data
        if isinstance(curr_val, Symbol):
            curr_val = curr_val.value

        if curr_val.endswith("}"): # handles cases where there are multiple stuff
            curr_val = curr_val.split("{")[0]
        trim = trim_children(tree.children)

        if curr_val.startswith("__") or curr_val == "None" or (curr_val.startswith("_") and not curr_val[1].isupper()):
            trimmed_children += trim # removes current value from tree
        else:
            if isinstance(tree.data, Symbol):
                curr_val = Symbol(origin=tree.data.origin, value=curr_val, error=tree.data.error, row=tree.data.row, col=tree.data.col)
            trimmed_children.append(Tree(curr_val, trim)) # keeps curr value in tree
    return trimmed_children

def __strip_token(tkn):
    if isinstance(tkn, Token):
        if tkn.type == "RULE":
            tkn = tkn.value
        else:
            tkn = tkn.type

    return tkn

def convert_lark_tree(tree):
    node_val = tree.data
    children = tree.children
    new_children = []
    if isinstance(node_val, Token):
        node_val = __strip_token(node_val)

    for child in children:
        if isinstance(child, Tree):
            child = convert_lark_tree(child)
        elif isinstance(child, Token):
            child = Tree(__strip_token(child), [])
        elif isinstance(child, str):
            child = Tree(child, [])
        
        new_children.append(child)

    return Tree(node_val, new_children)

#TODO: strip deleted symbols from cyk tree

def save_tree(tree, path, text=None):
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
                node_val = child.data
                if child.children:
                    children_stack.append((str(counter), child.children))
            else:
                node_val = child

            # create new node
            #TODO: color node appropriately
            if isinstance(node_val, Symbol):
                if node_val.origin == "deleted":
                    dot.node(str(counter), repr(node_val), style="filled", fillcolor="red")
                elif node_val.origin == "inserted":
                    dot.node(str(counter), repr(node_val), style="filled", fillcolor="green")
                elif node_val.origin == "skipped to":
                    dot.node(str(counter), repr(node_val), style="filled", fillcolor="orange")
                elif node_val.origin == "sentence":
                    dot.node(str(counter), repr(node_val), style="filled", fillcolor="grey")
                else:
                    dot.node(str(counter), repr(node_val))
            else:
                dot.node(str(counter), repr(node_val))
            # connect new node to parent
            dot.edge(parent, str(counter))

        # get next node
        if children_stack:
            parent, curr_children = children_stack.pop()
        else:
            curr_children = None

    # check if text is provided, add to graph if so
    if text:
        dot.node("text", text, shape="box", style="dashed")

    # write tree to file
    dot.render(path)

def get_files_from_dir(directory):
    all_files = []    
    for subdir, _, files in os.walk(directory):
        for file_name in files:
            if file_name[-3:] != ".py":
                continue
            file_path = os.path.join(subdir, file_name)
            try:
                with open(file_path, "rb") as file:
                    raw_data = file.read()
                    detected = detect(raw_data)
                    encoding = detected["encoding"]
                with open(file_path, encoding=encoding) as file:
                    num_lines = sum(1 for _ in file)
                
                all_files.append((file_name, file_path, num_lines))
            except Exception as e:
                print(f"Failed to read {file_path}: {e}")
    
    return all_files

def convert_lark_tokens_for_cyk(tokens: list[Token]) -> list[str]:
    return list(map(lambda x: x.type, tokens))

def get_leaves(parse_tree, leaves=None, include_del=True):
    if leaves == None:
        leaves = []
    if not parse_tree.children:
        if include_del or parse_tree.data.origin != "deleted":
            leaves.append(parse_tree.data)
    else:
        for child in parse_tree.children:
            get_leaves(child, leaves, include_del=include_del)

    return list(map(lambda sym: sym.value, leaves))
