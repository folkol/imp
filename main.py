import sys

from lexer import lex
from parser import parser, RESERVED, INT, ID, aexp

token_exprs = [
    (r'[ \n\t]+', None),
    (r'#.*', None),
    (r':=', RESERVED),
    (r'\(', RESERVED),
    (r'\)', RESERVED),
    (r';', RESERVED),
    (r'\+', RESERVED),
    (r'-', RESERVED),
    (r'\*', RESERVED),
    (r'/', RESERVED),
    (r'<=', RESERVED),
    (r'<', RESERVED),
    (r'>=', RESERVED),
    (r'>', RESERVED),
    (r'=', RESERVED),
    (r'!=', RESERVED),
    (r'and', RESERVED),
    (r'or', RESERVED),
    (r'not', RESERVED),
    (r'if', RESERVED),
    (r'then', RESERVED),
    (r'else', RESERVED),
    (r'while', RESERVED),
    (r'do', RESERVED),
    (r'end', RESERVED),
    (r'[0-9]+', INT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID)
]


def imp_parse(tokens):
    return parser()(tokens, 0)


if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print(f'usage: {sys.argv[0]} filename')
    #     sys.exit(1)
    # filename = sys.argv[1]

    filename = 'foo.imp'

    with open(filename) as f:
        chars = f.read()
    tokens = lex(chars, token_exprs)
    # result = imp_parse(tokens)
    result = aexp()(tokens, 0)
    print(result)
