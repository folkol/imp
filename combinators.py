class Result(object):
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos

    def __repr__(self):
        return f'Result({self.value}, {self.pos})'


class Parser(object):
    def __call__(self, tokens, pos):
        return None

    def __add__(self, other):
        return Concat(self, other)

    def __mul__(self, other):
        return Exp(self, other)

    def __or__(self, other):
        return Alternate(self, other)

    def __xor__(self, other):
        return Process(self, other)


class Reserved(Parser):
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, tokens, pos):
        value, tag = tokens[pos]
        if pos < len(tokens) and value == self.value and tag is self.tag:
            return Result(value, pos + 1)
        else:
            return None


class Tag(Parser):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, tokens, pos):
        value, tag = tokens[pos]
        if pos < len(tokens) and tag is self.tag:
            return Result(value, pos + 1)
        else:
            return None


class Concat(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left_result = self.left(tokens, pos)
        if left_result:
            right_result = self.right(tokens, left_result.pos)
            if right_result:
                combined_value = left_result.value, right_result.value
                return Result(combined_value, right_result.pos)
            else:
                return None


class Alternate(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        return self.left(tokens, pos) or self.right(tokens.pos)


class Optional(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        return self.parser(tokens, pos) or Result(None, pos)


class Repeat(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        results = []
        result = self.parser(tokens, pos)
        while result:
            results.append(result)
            pos = result.pos
            result = self.parser(tokens, pos)
        return Result(results, pos)


class Process(Parser):
    def __init__(self, parser, f):
        self.parser = parser
        self.f = f

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            result.value = self.f(result.value)
            return result


class Lazy(Parser):
    def __init__(self, parser_func):
        self.parser = None
        self.parser_func = parser_func

    def __call__(self, tokens, pos):
        if not self.parser_func:
            self.parser = self.parser_func()
        return self.parser(tokens, pos)


class Phrase(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result and result.pos == len(tokens):
            return result
        else:
            return None


class Exp(Parser):
    def __init__(self, parser, separator):
        self.separator = separator
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)

        def process_next(parsed):
            sepfunc, right = parsed
            return sepfunc(result.value, right)

        next_parser = self.separator + self.parser ^ process_next()
        next_result = result
        while next_result:
            next_result = next_parser(tokens, result.pos)
            if next_result:
                result = next_result
            return result
