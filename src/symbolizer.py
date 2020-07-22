from src.visitor import Visitor
from src.nodes import *


class Symbol:
    def __init__(self, id_, type_, value=None, params=None):
        self.id_ = id_
        self.type_ = type_
        self.value = value
        self.params = params

    def __str__(self):
        symbol = (self.id_, self.type_, self.value, self.params)
        return "<{} {} {} {}>".format(*symbol)


class Symbols:
    def __init__(self):
        self.symbols = {}

    def put(self, id_, type_, value=None, params=None):
        self.symbols[id_] = Symbol(id_, type_, value, params)

    def get(self, id_):
        return self.symbols[id_]

    def __str__(self):
        out = ""
        for _, value in self.symbols.items():
            if len(out) > 0:
                out += "\n"
            out += str(value)
        return out


class Symbolizer(Visitor):
    def __init__(self, ast):
        self.ast = ast

    def visit_Program(self, parent, node):
        node.symbols = Symbols()
        for n in node.nodes:
            self.visit(node, n)

    def visit_Decl(self, parent, node):
        parent.symbols.put(node.id_.value, node.type_.value)

    def visit_ArrayDecl(self, parent, node):
        parent.symbols.put(node.id_.value, node.type_.value)

    def visit_ArrayElem(self, parent, node):
        pass

    def visit_Assign(self, parent, node):
        pass

    def visit_If(self, parent, node):
        self.visit(node, node.true)
        self.visit(node, node.false)

    def visit_While(self, parent, node):
        self.visit(node, node.block)

    def visit_For(self, parent, node):
        self.visit(node, node.block)

    def visit_FuncImpl(self, parent, node):
        parent.symbols.put(node.id_.value, node.type_.value)
        self.visit(node, node.params)
        node.block.symbols = node.params.symbols
        node.params.symbols = None
        self.visit(node, node.block)

    def visit_FuncCall(self, parent, node):
        pass

    def visit_Block(self, parent, node):
        node.symbols = Symbols()
        for n in node.nodes:
            self.visit(node, n)

    def visit_Params(self, parent, node):
        node.symbols = Symbols()
        for p in node.params:
            self.visit(node, p)

    def visit_Args(self, parent, node):
        pass

    def visit_Elems(self, parent, node):
        pass

    def visit_Break(self, parent, node):
        pass

    def visit_Continue(self, parent, node):
        pass

    def visit_Return(self, parent, node):
        pass

    def visit_Type(self, parent, node):
        pass

    def visit_Int(self, parent, node):
        pass

    def visit_Char(self, parent, node):
        pass

    def visit_String(self, parent, node):
        pass

    def visit_Id(self, parent, node):
        pass

    def visit_BinOp(self, parent, node):
        pass

    def visit_UnOp(self, parent, node):
        pass

    def symbolize(self):
        self.visit(None, self.ast)
