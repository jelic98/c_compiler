from src.visitor import Visitor
from src.nodes import *
import re


class Runner(Visitor):
    def __init__(self, ast):
        self.ast = ast
        self.global_ = {}
        self.local = {}

    def visit_Program(self, parent, node):
        for s in node.symbols:
            self.global_[s.id_] = s
        for n in node.nodes:
            self.visit(node, n)

    def visit_Decl(self, parent, node):
        pass

    def visit_ArrayDecl(self, parent, node):
        pass

    def visit_ArrayElem(self, parent, node):
        pass

    def visit_Assign(self, parent, node):
        pass

    def visit_If(self, parent, node):
        pass

    def visit_While(self, parent, node):
        pass

    def visit_For(self, parent, node):
        pass

    def visit_FuncImpl(self, parent, node):
        if node.id_.value == 'main':
            self.visit(node, node.block)

    def visit_FuncCall(self, parent, node):
        func = node.id_.value
        args = node.args.args
        if func == 'printf':
            out = args[0].value
            out = out.replace('\\n', '\n')
            for a in args[1:]:
                if isinstance(a, Int):
                    out = out.replace('%d', a.value, 1)
                elif isinstance(a, Char):
                    out = out.replace('%c', a.value, 1)
                elif isinstance(a, String):
                    out = out.replace('%s', a.value, 1)
                elif isinstance(a, Id):
                    value = '123'
                    out = re.sub('%[dcs]', value, out, 1)
            print(out, end='')
        else:
            impl = self.global_[func]
            self.visit(node, impl.block)

    def visit_Block(self, parent, node):
        block = id(node)
        if block not in self.local:
            self.local[block] = {}
        for s in node.symbols:
            self.local[block][s.id_] = s
        for n in node.nodes:
            self.visit(node, n)

    def visit_Params(self, parent, node):
        pass

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

    def run(self):
        self.visit(None, self.ast)
