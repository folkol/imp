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
