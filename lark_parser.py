from io import open
from typing import (Iterator, Any)

from lark import Lark
from lark.indenter import PythonIndenter
from lark.lexer import LexerState, Lexer, Token

from utils import read

kwargs = dict(postlex=PythonIndenter(), start='file_input')
kwargs["maybe_placeholders"] = False
kwargs["keep_all_tokens"] = True
lalr_parser = Lark.open_from_package('lark', 'python.lark', ['grammars'], parser="lalr", **kwargs)
# combined_parser = Lark.open_from_package('lark', 'python.lark', ['grammars'], parser="earley", **kwargs)
# combined_parser = Lark(read("references/python-pinned.lark"), parser="earley", **kwargs) # pinned grammar
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
        kwargs = {'encoding': 'iso-8859-1'}
        with open(fn, *args, **kwargs) as f:
            return f.read()

    def fix_underscore(self, token: Token):
        if token.type == 'UNDERSCORE':
            token.type = 'NAME'

    def lex(self, text):
        stream = self.lalr_parser.lex(text)
        tokens = [token for token in stream]
        for token in tokens:
            self.fix_underscore(token)
        self.lexer = ListLexer(tokens)
        return list(map(lambda x: x.type, tokens))

    def parse(self, text):
        self.lex(text)
        kw = {}
        return self.earley_parser.parser.parser.parse(self.lexer, self.earley_parser.parser._verify_start(), **kw)

