import os
from charset_normalizer import detect

import graphviz
from lark.tree import Tree
from lark.lexer import Token

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
        parent_val = tree.data
        if parent_val.endswith("}"):
            parent_val = parent_val.split("{")[0]
        trim = trim_children(tree.children)
        if parent_val.startswith("__") or parent_val == "None" or (parent_val.startswith("_") and not parent_val[1].isupper()):
            trimmed_children += trim
        else:
            trimmed_children.append(Tree(parent_val, trim))
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
                node_val = child.data
                if child.children:
                    children_stack.append((str(counter), child.children))
            else:
                node_val = child

            # create new node
            dot.node(str(counter), node_val)
            # connect new node to parent
            dot.edge(parent, str(counter))

        # get next node
        if children_stack:
            parent, curr_children = children_stack.pop()
        else:
            curr_children = None

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
