from functools import reduce

from ast import *
from combinators import *

RESERVED = 'RESERVED'
INT = 'INT'
ID = 'ID'


def keyword(kw):
    return Keyword(kw, RESERVED)


identifier = Tag(ID)
num = Tag(INT) ^ int


def aexp_value():
    return num ^ IntExp | identifier ^ Variable


def process_group(parsed):
    ((_, p), _) = parsed
    return p


def aexp_group():
    return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group


def aexp_term():
    return aexp_value() | aexp_group()


def process_binop(op):
    return lambda l, r: BinaryOperator(op, l, r)


def any_operator_in_list(ops):
    op_parsers = map(keyword, ops)
    parser = reduce((lambda l, r: l | r), op_parsers)
    return parser


aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
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


def process_relop(parsed):
    (left, op), right = parsed
    return RelationalExpression(op, left, right)


def bexp_relop():
    relops = ['<', '<=', '>', '>=', '=', '!=']
    return aexp() + any_operator_in_list(relops) + aexp() ^ process_relop


def bexp_not():
    return keyword('not') + Lazy(bexp_term) ^ (lambda parsed: Not(parsed[1]))


def bexp_group():
    return keyword('(') + Lazy(bexp) + keyword(')') ^ process_group


def bexp_term():
    return bexp_not() | bexp_relop() | bexp_group()


bexp_precedence_levels = [
    ['and'],
    ['or'],
]


def process_logic(op):
    if op == 'and':
        return lambda l, r: And(l, r)
    elif op == 'or':
        return lambda l, r: Or(l, r)
    else:
        raise RuntimeError('unknown logic operator: ' + op)


def bexp():
    return precedence(bexp_term(), bexp_precedence_levels, process_logic)


def assign_stmt():
    def process(parsed):
        (name, _), exp = parsed
        return Assignment(name, exp)

    return identifier + keyword(':=') + aexp() ^ process


def stmt_list():
    separator = keyword(';') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
    return Exp(stmt(), separator)


def if_stmt():
    def process(parsed):
        ((((_, condition), _), true_stmt), false_parsed), _ = parsed
        if false_parsed:
            _, false_stmt = false_parsed
        else:
            false_stmt = None
        return If(condition, true_stmt, false_stmt)

    return (keyword('if') + bexp() +
            keyword('then') + Lazy(stmt_list) +
            Optional(keyword('else') + Lazy(stmt_list)) +
            keyword('end') ^ process)


def while_stmt():
    def process(parsed):
        (((_, condition), _), body), _ = parsed
        return While(condition, body)

    return (keyword('while') + bexp() +
            keyword('do') + Lazy(stmt_list) +
            keyword('end') ^ process)


def stmt():
    return assign_stmt() | if_stmt() | while_stmt()


def parser():
    return Complete(stmt_list())
