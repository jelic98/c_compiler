from src.visitor import Visitor
from src.symbols import Symbol
from src.nodes import *
import re


class Runner(Visitor):
    def __init__(self, ast):
        self.ast = ast
        self.global_ = {}
        self.local = {}
        self.scope = []

    def get_symbol(self, node):
        id_ = node.value
        if len(self.scope) > 0:
            for scope in reversed(self.scope):
                if id_ in self.local[scope]:
                    return self.local[scope][id_]
        return self.global_[id_]
    
    def init_scope(self, node):
        scope = id(node)
        if scope not in self.local:
            self.local[scope] = {}
            for s in node.symbols:
                self.local[scope][s.id_] = s

    def visit_Program(self, parent, node):
        for s in node.symbols:
            self.global_[s.id_] = s
        for n in node.nodes:
            self.visit(node, n)

    def visit_Decl(self, parent, node):
        pass

    def visit_ArrayDecl(self, parent, node):
        id_ = self.get_symbol(node.id_)
        id_.symbols = node.symbols
        size, elems = node.size, node.elems
        if size is not None:
            for i in range(size.value):
                id_.symbols.put(i, id_.type_, None)
                id_.symbols.get(i).value = None
        elif elems is not None:
            self.visit(node, elems)

    def visit_ArrayElem(self, parent, node):
        id_ = self.get_symbol(node.id_)
        index = self.visit(node, node.index)
        return id_.symbols.get(index.value)

    def visit_Assign(self, parent, node):
        id_ = self.visit(node, node.id_)
        value = self.visit(node, node.expr)
        if isinstance(value, Symbol):
            value = value.value
        id_.value = value

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
        id_ = self.get_symbol(node.id_)
        id_.params = node.params
        id_.block = node.block
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
                    out = out.replace('%c', chr(a.value), 1)
                elif isinstance(a, String):
                    out = out.replace('%s', a.value, 1)
                elif isinstance(a, Id):
                    id_ = self.visit(node.args, a)
                    out = re.sub('%[dcs]', str(id_.value), out, 1)
            print(out, end='')
        elif func == 'scanf':
            pass
        elif func == 'strlen':
            if isinstance(a, String):
                return len(a.value)
        elif func == 'strcat':
            return str(args[0]) + str(args[1])
        else:
            impl = self.global_[func]
            self.visit(node, node.args)
            self.visit(node, impl.block)

    def visit_Block(self, parent, node):
        scope = id(node)
        self.init_scope(node)
        self.scope.append(scope)
        for n in node.nodes:
            if isinstance(n, Return) or isinstance(n, Break):
                break
            elif isinstance(n, Continue):
                continue
            else:
                self.visit(node, n)
        self.scope.pop()

    def visit_Params(self, parent, node):
        pass

    def visit_Args(self, parent, node):
        func = parent.id_.value
        impl = self.global_[func]
        block = impl.block
        scope = id(block)
        self.init_scope(block)
        self.scope.append(scope)
        for p, a in zip(impl.params.params, node.args):
            id_ = self.visit(block, p.id_)
            id_.value = self.visit(block, a).value
        self.scope.pop()

    def visit_Elems(self, parent, node):
        for i, e in enumerate(node.elems):
            value = self.visit(node, e)
            id_ = self.get_symbol(parent.id_)
            id_.symbols.put(i, id_.type_, None)
            id_.symbols.get(i).value = value

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
        return ord(node.value)

    def visit_String(self, parent, node):
        return node.value

    def visit_Id(self, parent, node):
        return self.get_symbol(node)

    def visit_BinOp(self, parent, node):
        first = self.visit(node, node.first)
        if isinstance(first, Symbol):
            first = first.value
        second = self.visit(node, node.second)
        if isinstance(second, Symbol):
            second = second.value
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
        first = self.visit(node, node.first).value
        if node.symbol == '-':
            return -first
        elif node.symbol == '!':
            bool_first = first != 0
            return not bool_first
        else:
            return None

    def run(self):
        self.visit(None, self.ast)
