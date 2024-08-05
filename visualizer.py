import os
import re
import ast
import contextlib

import streamlit as st
from tabulate import tabulate

from CYK_parser import load_productions_from_json, parse

st.set_page_config(layout="wide", page_title="Chart Viewer")
st.title("Chart Viewer")

grammars = os.listdir("grammars")

def charts(output_file):
    with open(f"outputs/{output_file}") as f:
        output = f.read()

    item_charts = re.findall("Item Chart: .+", output)
    item_charts = list(map(lambda x: ast.literal_eval(x.replace("Item Chart: ", "").replace("{", "\"").replace("}", "\"")), item_charts))

    symbol_charts = re.findall("Symbol Chart: .+", output)
    symbol_charts = list(map(lambda x: ast.literal_eval(x.replace("Symbol Chart: ", "").replace("{", "\"").replace("}", "\"")), symbol_charts))


    return item_charts, symbol_charts

if 'prev_output_file' not in st.session_state:
    st.session_state.prev_output_file = None
if 'item_index' not in st.session_state:
    st.session_state.item_index = 0
if 'symbol_index' not in st.session_state:
    st.session_state.symbol_index = 0
if 'item_charts' not in st.session_state:
    st.session_state.item_charts = []
if 'symbol_charts' not in st.session_state:
    st.session_state.symbol_charts = []

with st.sidebar:
    st.session_state.output_file = st.selectbox("Output Folder", os.listdir("outputs"))
    if st.session_state.prev_output_file != st.session_state.output_file:
        st.session_state.item_charts, st.session_state.symbol_charts = charts(st.session_state.output_file)
        st.session_state.item_index = st.session_state.symbol_index = 0
        st.session_state.prev_output_file = st.session_state.output_file

item_col, symbol_col = st.columns([2, 1])

with item_col:
    st.subheader(f"item chart {st.session_state.item_index}")
    item_cont = st.container(height=600)
    with item_cont:
        item_html = tabulate(st.session_state.item_charts[st.session_state.item_index], tablefmt="html")
        st.markdown(item_html.replace("],", "]\n\n"),unsafe_allow_html=True)

    # if st.button("next"):
    #     st.session_state.item_index = (st.session_state.item_index + 1) % len(st.session_state.item_charts)
    
    # if st.button("prev"):
    #     st.session_state.item_index = (st.session_state.item_index - 1) % len(st.session_state.item_charts)
    
    # if new_value := st.selectbox("Select Item Chart", options=range(len(st.session_state.item_charts))):
    #     st.session_state.item_index = new_value
    # st.button("confirm")


with symbol_col:
    st.subheader(f"symbol chart {st.session_state.symbol_index}")
    symbol_cont = st.container(height=600)
    with symbol_cont:
        symbol_html = tabulate(st.session_state.symbol_charts[st.session_state.symbol_index], tablefmt="html")
        st.markdown(symbol_html.replace("],", "]\n\n"),unsafe_allow_html=True)

    # if st.button("next", key="sym_nxt"):
    #     st.session_state.symbol_index = (st.session_state.symbol_index + 1) % len(st.session_state.symbol_charts)
    
    # if st.button("prev", key="sym_prev"):
    #     st.session_state.symbol_index = (st.session_state.symbol_index - 1) % len(st.session_state.symbol_charts)
    
    # if new_value := st.selectbox("Select Symbol Chart", options=range(len(st.session_state.symbol_charts)), key="sym_sel"):
    #     st.session_state.symbol_index = new_value
    # st.button("confirm", key="sym_confirm")

if st.button("next", key="all_nxt"):
    st.session_state.item_index = st.session_state.symbol_index = (st.session_state.symbol_index + 1) % len(st.session_state.symbol_charts)

if st.button("prev", key="all_prev"):
    st.session_state.item_index = st.session_state.symbol_index = (st.session_state.symbol_index - 1) % len(st.session_state.symbol_charts)

if new_value := st.selectbox("Select Chart", options=range(len(st.session_state.symbol_charts)), key="all_sel"):
    st.session_state.symbol_index = new_value
    st.session_state.item_index = new_value
    
st.button("confirm", key="sym_confirm")

with st.form("Parse"):
    filename = st.text_input("filename")
    st.session_state.parser = st.selectbox("Parser", ["CYK Parser"])
    st.session_state.grammar = st.selectbox("Grammar", grammars)
    input_string = str(st.text_input("input string"))
    parse_submit = st.form_submit_button("parse")
    if parse_submit:
        prod, init_items = load_productions_from_json(f"grammars/{st.session_state.grammar}")
        with open(f"outputs/{filename}.txt", "w") as f:
            with contextlib.redirect_stdout(f):
                parse(input_string, prod, init_items, debug=True)
