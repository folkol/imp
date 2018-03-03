from functools import reduce

from ast import IntAexp, VarAexp, BinopAexp
from combinators import Reserved, Tag, Lazy
from main import RESERVED, ID, INT


def keyword(kw):
    return Reserved(kw, RESERVED)


id = Tag(ID)
num = Tag(INT) ^ int


def aexp_value():
    return num ^ IntAexp | id ^ VarAexp


def process_group(parsed):
    ((_, p), _) = parsed
    return p


def aexp_group():
    return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group


def aexp_term():
    return aexp_value() | aexp_group()


def process_binop(op):
    return lambda l, r: BinopAexp(op, l, r)


def any_operator_in_list(ops):
    op_parsers = map(keyword, ops)
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser


aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-']
]


def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine

    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser


def aexp():
    return precedence(aexp_term(), aexp_precedence_levels, process_binop)
