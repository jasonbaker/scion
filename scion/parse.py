from pyparsing import (Suppress, Forward, nums, ZeroOrMore,
                       replaceWith, QuotedString, Word, alphas,
                       Keyword, Optional, Group, Combine,
                       nestedExpr, pythonStyleComment,
                       traceParseAction, alphanums, White,
                       OneOrMore)

LPAREN = Suppress('(')
RPAREN = Suppress(')')
TRUE = Keyword('True').setParseAction(replaceWith(True))
FALSE = Keyword('False').setParseAction(replaceWith(False))
NONE = Keyword('nil').setParseAction(replaceWith(None))
comment = pythonStyleComment

# Forward declaration of s-expressions
sexp = Forward()
list_sexp = Group(LPAREN + ZeroOrMore(sexp | Suppress(White())) + RPAREN)
num_sexp = Combine(Optional('-') + ( '0' | Word('123456789',nums)) +
                   Optional( '.' + Word(nums)) +
                   Optional( Word('eE',exact=1) + Word(nums+'+-',nums)))
str_sexp = QuotedString('"', escChar='\\', unquoteResults=False)
bool_sexp = (TRUE | FALSE)
atom = (num_sexp | str_sexp | bool_sexp |
        NONE)
extra_allowed_ident_chars = '+-=*/!?%'
var_sexp = Word(initChars=alphas + extra_allowed_ident_chars, bodyChars=alphanums + extra_allowed_ident_chars)
sexp << (atom | var_sexp | list_sexp).ignore(comment)
multi_sexp = OneOrMore(sexp)


def convert_num(s, l, toks):
    n = toks[0]
    try:
        return int(n)
    except ValueError:
        return float(n)
num_sexp.setParseAction(convert_num)

def get_syntax_tree(fname):
    infile = open(fname, 'r')
    try:
        file_text = infile.read()
        return get_syntax_tree_from_str(file_text).asList()
    finally:
        infile.close()

def get_syntax_tree_from_str(str):
    return multi_sexp.parseString(str, parseAll=True)
