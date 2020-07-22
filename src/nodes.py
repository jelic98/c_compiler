class Node():
    pass


class Program(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class Decl(Node):
    def __init__(self, type_, id_):
        self.type_ = type_
        self.id_ = id_


class ArrayDecl(Node):
    def __init__(self, type_, id_, size, elems):
        self.type_ = type_
        self.id_ = id_
        self.size = size
        self.elems = elems


class ArrayElem(Node):
    def __init__(self, id_, index):
        self.id_ = id_
        self.index = index


class Assign(Node):
    def __init__(self, id_, expr):
        self.id_ = id_
        self.expr = expr


class If(Node):
    def __init__(self, cond, true, false):
        self.cond = cond
        self.true = true
        self.false = false


class While(Node):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block


class For(Node):
    def __init__(self, init, cond, step, block):
        self.init = init
        self.cond = cond
        self.step = step
        self.block = block


class FuncImpl(Node):
    def __init__(self, type_, id_, params, block):
        self.type_ = type_
        self.id_ = id_
        self.params = params
        self.block = block


class FuncCall(Node):
    def __init__(self, id_, args):
        self.id_ = id_
        self.args = args


class Block(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class Params(Node):
    def __init__(self, params):
        self.params = params


class Args(Node):
    def __init__(self, args):
        self.args = args


class Elems(Node):
    def __init__(self, elems):
        self.elems = elems


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
