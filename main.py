import sys

from lexer import lex

RESERVED = 'RESERVED'
INT = 'INT'
ID = 'ID'

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

if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename) as f:
        chars = f.read()
    tokens = lex(chars, token_exprs)
    for token in tokens:
        print(token)
