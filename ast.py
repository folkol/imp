class Equality:
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class Aexp(Equality):
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return f'IntAxp({self.i})'


class VarAexp(Aexp):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'VarAexp({self.name})'


class BinopAexp(Aexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f'BinopAexp({self.op}, {self.left}, {self.right})'


class Bexp(Equality):
    pass


class RelopBexp(Bexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class AndBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class OrBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class NotBexp(Bexp):
    def __init__(self, exp):
        self.exp = exp


class Statement(Equality):
    pass


class AssignStatement(Statement):
    def __init__(self, name, aexp):
        self.name = name
        self.aexp = aexp


class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.second = second
        self.first = first


class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt


class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
