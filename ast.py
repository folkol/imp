class ArithmeticExpression(object):
    pass


class IntExp(ArithmeticExpression):
    def __init__(self, i):
        self.i = i

    def eval(self, ignored):
        return self.i


class Variable(ArithmeticExpression):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        if self.name in env:
            return env[self.name]
        else:
            return 0


class BinaryOperator(ArithmeticExpression):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '+':
            value = left_value + right_value
        elif self.op == '-':
            value = left_value - right_value
        elif self.op == '*':
            value = left_value * right_value
        elif self.op == '/':
            value = left_value / right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value


class BooleanExpression(object):
    pass


class RelationalExpression(BooleanExpression):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '<':
            value = left_value < right_value
        elif self.op == '<=':
            value = left_value <= right_value
        elif self.op == '>':
            value = left_value > right_value
        elif self.op == '>=':
            value = left_value >= right_value
        elif self.op == '=':
            value = left_value == right_value
        elif self.op == '!=':
            value = left_value != right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value


class And(BooleanExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value and right_value


class Or(BooleanExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value or right_value


class Not(BooleanExpression):
    def __init__(self, exp):
        self.exp = exp

    def eval(self, env):
        value = self.exp.eval(env)
        return not value


class Statement(object):
    pass


class Assignment(Statement):
    def __init__(self, name, aexp):
        self.name = name
        self.aexp = aexp

    def eval(self, env):
        value = self.aexp.eval(env)
        env[self.name] = value


class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.second = second
        self.first = first

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)


class If(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

    def eval(self, env):
        condition_value = self.condition.eval(env)
        if condition_value:
            self.true_stmt.eval(env)
        else:
            if self.false_stmt:
                self.false_stmt.eval(env)


class While(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def eval(self, env):
        condition_value = self.condition.eval(env)
        while condition_value:
            self.body.eval(env)
            condition_value = self.condition.eval(env)
