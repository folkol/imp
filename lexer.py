import re
import sys


def lex(chars, token_exprs):
    pos = 0
    tokens = []
    while pos < len(chars):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(chars, pos)
            if match:
                text = match.groups(0)
                if tag:
                    token = text, tag
                    tokens.append(token)
                break
        if not match:
            print(f'Illegal characer: {chars[pos]}', file=sys.stderr)
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens
