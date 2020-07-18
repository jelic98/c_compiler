class Node:
    pass


class Program(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class Decl(Node):
    def __init__(self, type_, name, expr):
        self.type_ = type_
        self.name = name
        self.expr = expr


class ArrayDecl(Node):
    def __init__(self, type_, name, size, elems):
        self.type_ = type_
        self.name = name
        self.size = size
        self.elems = elems


class ArrayElem(Node):
    def __init__(self, array, index):
        self.array = array
        self.index = index


class Assign(Node):
    def __init__(self, name, expr):
        self.name = neame
        self.expr = expr


class If(Node):
    def __init__(self, cond, elses):
        self.cond = cond
        self.body = body
        self.elses = elses


class While(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body


class For(Node):
    def __init__(self, init, cond, step, body):
        self.init = init
        self.cond = cond
        self.step = step
        self.body = body


class FuncDecl(Node):
    def __init__(self, type_, name, params):
        self.type_ = type_
        self.name = name
        self.params = params


class FuncImpl(Node):
    def __init__(self, type_, name, params, body):
        self.type_ = type_
        self.name = name
        self.params = params
        self.body = body


class FuncCall(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args


class Params(Node):
    def __init__(self, params):
        self.params = params


class Args(Node):
    def __init__(self, args):
        self.args = args


class Break(Node):
    pass


class Continue(Node):
    pass


class Return(Node):
    def __init__(self, expr):
        self.expr = expr


class Type(Node):
    def __init__(self, value):
        self.value = value


class Int(Node):
    def __init__(self, value):
        self.value = value


class Char(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class Id(Node):
    def __init__(self, value):
        self.value = value


class BinOp(Node):
    def __init__(self, symbol, first, second):
        self.symbol = symbol
        self.first = first
        self.second = second


class UnOp(Node):
    def __init__(self, symbol, first):
        self.symbol = symbol
        self.first = first
