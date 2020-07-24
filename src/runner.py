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
        id_ = self.visit(node, node.id_)
        id_.value = self.visit(node, node.expr)

    def visit_If(self, parent, node):
        cond = self.visit(node, node.cond)
        if cond:
            self.visit(node, node.true)
        else:
            self.visit(node, node.false)

    def visit_While(self, parent, node):
        cond = self.visit(node, node.cond)
        while cond:
            self.visit(node, node.block)
            cond = self.visit(node, node.cond)

    def visit_For(self, parent, node):
        self.visit(node, node.init)
        cond = self.visit(node, node.cond)
        while cond:
            self.visit(node, node.block)
            self.visit(node, node.step)
            cond = self.visit(node, node.cond)

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
                    id_ = self.visit(node.args, a)
                    out = re.sub('%[dcs]', str(id_.value), out, 1)
            print(out, end='')
        elif func == 'scanf':
            pass
        elif func == 'len':
            pass
        elif func == 'strcat':
            return str(args[0]) + str(args[1])
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
            if isinstance(n, Break):
                break
            if isinstance(n, Continue):
                continue
            if isinstance(n, Return):
                return
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
        return node.value

    def visit_Char(self, parent, node):
        return node.value

    def visit_String(self, parent, node):
        return node.value

    def visit_Id(self, parent, node):
        return self.global_[node.value]

    def visit_BinOp(self, parent, node):
        symbol_first = self.visit(node, node.first)
        first = symbol_first.value
        if symbol_first.type_ == 'char':
            first = ord(first)
        symbol_second = self.visit(node, node.second)
        second = symbol_second.value
        if symbol_second.type_ == 'char':
            second = ord(second)
        if node.symbol == '+':
            return int(first) + int(second)
        elif node.symbol == '-':
            return int(first) - int(second)
        elif node.symbol == '*':
            return int(first) * int(second)
        elif node.symbol == '/':
            return int(first) / int(second)
        elif node.symbol == '%':
            return int(first) % int(second) 
        elif node.symbol == '==':
            return first == second
        elif node.symbol == '!=':
            return int(first) != int(second)
        elif node.symbol == '<':
            return int(first) < int(second)
        elif node.symbol == '>':
            return int(first) > int(second)
        elif node.symbol == '<=':
            return int(first) >= int(second)
        elif node.symbol == '>=':
            return int(first) <= int(second)
        elif node.symbol == '&&':
            bool_first = first != 0
            bool_second = second != 0
            return bool_first and bool_second
        elif node.symbol == '||':
            bool_first = first != 0
            bool_second = second != 0
            return bool_first or bool_second
        else:
            return None

    def visit_UnOp(self, parent, node):
        symbol_first = self.visit(node, node.first)
        first = symbol_first.value
        if node.symbol == '-':
            return -first
        elif node.symbol == '!':
            bool_first = first != 0
            return not bool_first
        else:
            return None

    def run(self):
        self.visit(None, self.ast)
