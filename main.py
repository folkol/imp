import sys

from lexer import lex
from parser import parser, RESERVED, INT, ID

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


def usage():
    sys.stderr.write('Usage: imp filename\\n')
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    filename = sys.argv[1]
    with open(filename) as f:
        text = f.read()

    tokens = lex(text, token_exprs)
    parse_result = parser()(tokens, 0)
    if not parse_result:
        print('Parse error!', file=sys.stderr)
        sys.exit(1)
    ast = parse_result.value
    env = {}
    ast.eval(env)

    print('Final variable values:')
    for name in env:
        print(name, env[name])
