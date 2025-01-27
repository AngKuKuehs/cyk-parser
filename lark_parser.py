from io import open
from typing import (Iterator, Any)

from lark import Lark
from lark.indenter import PythonIndenter
from lark.lexer import LexerState, Lexer, Token

from utils import read

kwargs = dict(postlex=PythonIndenter(), start='file_input')
kwargs["maybe_placeholders"] = False # removes None placeholders in tree
kwargs["keep_all_tokens"] = True # keep all terminals in tree
lalr_parser = Lark.open_from_package('lark', 'python.lark', ['grammars'], parser="lalr", **kwargs)
combined_parser = Lark(read("references/python-pinned-unnamed.lark"), parser="earley", **kwargs) # pinned unnamed grammar

class ListLexer(Lexer):
    def __init__(self, tokens: Iterator[Token]):
        self.tokens = tokens

    def lex(self, lexer_state: LexerState, parser_state: Any) -> Iterator[Token]:
        return self.tokens

    def lex(self, lexer_state: LexerState) -> Iterator[Token]:
        return self.tokens

class LarkParser():
    def __init__(self):
        kwargs = dict(postlex=PythonIndenter(), start='file_input')
        self.lalr_parser = Lark.open_from_package('lark', 'python.lark', ['grammars'], parser="lalr", **kwargs)
        # self.earley_parser = Lark.open_from_package('lark', 'python.lark', ['grammars'], parser="earley", **kwargs)
        self.earley_parser = combined_parser # use pinned grammar that has does not trim trees

    def read(self, fn, *args):
        """
        Takes a path to a file and returns a Python string to be parsed.

        Parameters:
            fn (str): path to a file to be read
            args (list): list of non-keyword arguments to pass to open()

        Returns:
            str: file represented as a Python string
        """
        kwargs = {'encoding': 'iso-8859-1'}
        with open(fn, *args, **kwargs) as f:
            return f.read()

    def fix_underscore(self, token: Token):
        """
        Handles the namespace collision of Lark's internal grammar's underscore and Python's underscore.

        Parameters:
            token (Token): A token that is being prepared to be parsed

        Returns:
            None
        """
        if token.type == 'UNDERSCORE':
            token.type = 'NAME'

    def lex(self, text):
        """
        Takes a string, assigns a ListLexer object to self.lexer, and returns a list of tokens that represent that string.

        Parameters:
            text (str): the contents to be parsed

        Returns:
            tuple:
                list[str]: list of token types (which amount to terminals)
                list[Token]: list of tokens for passing into parse_from_tokens
        """
        # TODO: figure out how to do this in a cleaner way -> have two different functions for lexing for cyk and lexing for lark
        stream = self.lalr_parser.lex(text)
        tokens = [token for token in stream]
        for token in tokens:
            self.fix_underscore(token)
        self.lexer = ListLexer(tokens)
        return tokens

    def parse(self, text):
        """
        Takes a string and parses it, returning an AST.

        Parameters:
            text (str): the contents to be parsed

        Returns:
            Tree
        """
        self.lex(text)
        kw = {}
        return self.earley_parser.parser.parser.parse(self.lexer, self.earley_parser.parser._verify_start(), **kw)
    
    def parse_from_tokens(self, tokens):
        self.lexer = ListLexer(tokens)
        kw = {}
        return self.earley_parser.parser.parser.parse(self.lexer, self.earley_parser.parser._verify_start(), **kw)

