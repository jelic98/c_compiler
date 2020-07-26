from src.visitor import Visitor
from src.symbols import Symbol
import re
import os


class Generator(Visitor):
    def __init__(self, ast):
        self.ast = ast
        self.py = ""
        self.level = 0

    def append(self, text):
        self.py += str(text)

    def newline(self):
        self.append('\n\r')

    def indent(self):
        for i in range(self.level):
            self.append('\t')

    def visit_Program(self, parent, node):
        for n in node.nodes:
            self.visit(node, n)
        self.append('if __name__ == "__main__":')
        self.newline()
        self.level += 1
        self.indent()
        self.append('main()')
        self.newline()
        self.level -= 1

    def visit_Decl(self, parent, node):
        pass

    def visit_ArrayDecl(self, parent, node):
        self.visit(node, node.id_)
        if node.size is not None:
            self.append(' = ')
            self.visit(node, node.size)
            self.append(' * [None]')
        elif node.elems is not None:
            self.append(' = [')
            self.visit(node, node.elems)
            self.append(']')

    def visit_ArrayElem(self, parent, node):
        self.visit(node, node.id_)
        self.append('[')
        self.visit(node, node.index)
        self.append(']')

    def visit_Assign(self, parent, node):
        self.visit(node, node.id_)
        self.append(' = ')
        self.visit(node, node.expr)

    def visit_If(self, parent, node):
        self.append('if ')
        self.visit(node, node.cond)
        self.append(':')
        self.visit(node, node.true)
        if node.false is not None:
            self.append('else:')
            self.visit(node, node.false)

    def visit_While(self, parent, node):
        self.append('while ')
        self.visit(node, node.cond)
        self.append(':')
        self.newline()
        self.visit(node, node.block)

    def visit_For(self, parent, node):
        self.visit(node, node.init)
        self.newline()
        self.indent()
        self.append('while ')
        self.visit(node, node.cond)
        self.append(':')
        self.newline()
        self.visit(node, node.block)
        self.level += 1
        self.indent()
        self.visit(node, node.step)
        self.level -= 1

    def visit_FuncImpl(self, parent, node):
        self.append('def ')
        self.append(node.id_.value)
        self.append('(')
        self.visit(node, node.params)
        self.append('):')
        self.newline()
        self.visit(node, node.block)

    def visit_FuncCall(self, parent, node):
        func = node.id_.value
        if func == 'printf':
            args = node.args.args
            format_ = args[0].value
            format_ = re.sub('%[dcs]', '{}', format_)
            self.append('print("')
            self.append(format_)
            self.append('"')
            if len(args) > 1:
                self.append('.format(')
                for i, a in enumerate(args[1:]):
                    if i > 0:
                        self.append(', ')
                    self.visit(node, a)
                self.append(')')
            self.append(', end="")')
        elif func == 'scanf':
            self.visit(node, node.args)
            self.append(' = input()')
        elif func == 'strlen':
            self.append('len(')
            self.visit(node, node.args)
            self.append(')')
        elif func == 'strcat':
            self.append(node.args[0])
            self.append(' + ')
            self.append(node.args[1])
        else:
            self.append(func)
            self.append('(')
            self.visit(node, node.args)
            self.append(')')

    def visit_Block(self, parent, node):
        self.level += 1
        for n in node.nodes:
            self.indent()
            self.visit(node, n)
            self.newline()
        self.level -= 1

    def visit_Params(self, parent, node):
        for i, p in enumerate(node.params):
            if i > 0:
                self.append(', ')
            self.visit(p, p.id_)

    def visit_Args(self, parent, node):
        for i, a in enumerate(node.args):
            if i > 0:
                self.append(', ')
            self.visit(node, a)

    def visit_Elems(self, parent, node):
        for i, e in enumerate(node.elems):
            if i > 0:
                self.append(', ')
            self.visit(node, e)

    def visit_Break(self, parent, node):
        self.append('break')

    def visit_Continue(self, parent, node):
        self.append('continue')

    def visit_Return(self, parent, node):
        self.append('return')
        if node.expr is not None:
            self.append(' ')
            self.visit(node, node.expr)

    def visit_Type(self, parent, node):
        pass

    def visit_Int(self, parent, node):
        self.append(node.value)

    def visit_Char(self, parent, node):
        self.append(ord(node.value))

    def visit_String(self, parent, node):
        self.append(node.value)

    def visit_Id(self, parent, node):
        self.append(node.value)

    def visit_BinOp(self, parent, node):
        first = self.visit(node, node.first)
        self.append(' ')
        self.append(node.symbol)
        self.append(' ')
        second = self.visit(node, node.second)

    def visit_UnOp(self, parent, node):
        self.append(node.symbol)
        first = self.visit(node, node.first)

    def generate(self):
        self.visit(None, self.ast)
        self.py = re.sub('\n\s*\n', '\n', self.py)
        path = os.path.dirname(os.path.realpath(__file__))
        dirs = os.path.splitext(path)[0].split(os.sep)
        dirs.insert(-1, 'out')
        dirs[-1] = 'main.py'
        main = os.sep.join(dirs)
        with open(main, 'w') as source:
            source.write(self.py)
