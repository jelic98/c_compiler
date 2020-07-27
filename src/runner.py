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
        self.call_stack = []
        self.search_new_call = False
        self.return_ = False

    def get_symbol(self, node):
        recursion = self.is_recursion() 
        ref = -2 if recursion and not self.search_new_call else -1
        id_ = node.value
        for scope in reversed(self.scope):
            if scope in self.local:
                curr_scope = self.local[scope][ref]
                if id_ in curr_scope:
                    return curr_scope[id_]
        return self.global_[id_]
    
    def init_scope(self, node):
        scope = id(node)
        if scope not in self.local:
            self.local[scope] = []
        self.local[scope].append({})
        for s in node.symbols:
            self.local[scope][-1][s.id_] = s.copy()

    def clear_scope(self, node):
        scope = id(node)
        self.local[scope].pop()

    def is_recursion(self):
        if len(self.call_stack) > 0:
            curr_call = self.call_stack[-1]
            prev_calls = self.call_stack[:-1]
            for call in reversed(prev_calls):
                if call == curr_call:
                    return True
        return False

    def visit_Program(self, parent, node):
        for s in node.symbols:
            self.global_[s.id_] = s.copy()
        for n in node.nodes:
            self.visit(node, n)

    def visit_Decl(self, parent, node):
        id_ = self.get_symbol(node.id_)
        id_.value = None

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
            self.init_scope(node.true)
            self.visit(node, node.true)
            self.clear_scope(node.true)
        else:
            if node.false is not None:
                self.init_scope(node.false)
                self.visit(node, node.false)
                self.clear_scope(node.false)

    def visit_While(self, parent, node):
        cond = self.visit(node, node.cond)
        while cond:
            self.init_scope(node.block)
            self.visit(node, node.block)
            self.clear_scope(node.block)
            cond = self.visit(node, node.cond)

    def visit_For(self, parent, node):
        self.visit(node, node.init)
        cond = self.visit(node, node.cond)
        while cond:
            self.init_scope(node.block)
            self.visit(node, node.block)
            self.clear_scope(node.block)
            self.visit(node, node.step)
            cond = self.visit(node, node.cond)

    def visit_FuncImpl(self, parent, node):
        id_ = self.get_symbol(node.id_)
        id_.params = node.params
        id_.block = node.block
        if node.id_.value == 'main':
            self.call_stack.append(node.id_.value)
            self.init_scope(node.block)
            self.visit(node, node.block)
            self.clear_scope(node.block)
            self.call_stack.pop()

    def visit_FuncCall(self, parent, node):
        func = node.id_.value
        args = node.args.args
        if func == 'printf':
            format_ = args[0].value
            format_ = format_.replace('\\n', '\n')
            for a in args[1:]:
                if isinstance(a, Int):
                    format_ = format_.replace('%d', a.value, 1)
                elif isinstance(a, Char):
                    format_ = format_.replace('%c', chr(a.value), 1)
                elif isinstance(a, String):
                    format_ = format_.replace('%s', a.value, 1)
                elif isinstance(a, Id) or isinstance(a, ArrayElem):
                    id_ = self.visit(node.args, a)
                    value = id_.value
                    if id_.type_ == 'char':
                        value = chr(value)
                    format_ = re.sub('%[dcs]', str(value), format_, 1)
                else:
                    value = self.visit(node.args, a)
                    format_ = re.sub('%[dcs]', str(value), format_, 1)
            print(format_, end='')
        elif func == 'scanf':
            format_ = args[0].value
            inputs = input().split()
            matches = re.findall('%[dcs]', format_)
            for i, m in enumerate(matches):
                id_ = self.visit(node.args, args[i + 1])
                if m == '%d':
                    id_.value = int(inputs[i])
                elif m == '%c':
                    id_.value = ord(inputs[i][0])
                else:
                    id_.value = inputs[i]
        elif func == 'strlen':
            if isinstance(a, String):
                return len(a.value)
        elif func == 'strcat':
            if isinstance(args[0], String) and isinstance(args[1], String):
                return str(args[0]) + str(args[1])
        else:
            impl = self.global_[func]
            self.call_stack.append(func)
            self.init_scope(impl.block)
            self.visit(node, node.args)
            self.visit(node, impl.block)
            self.clear_scope(impl.block)
            self.call_stack.pop()
            self.return_ = False

    def visit_Block(self, parent, node):
        scope = id(node)
        self.scope.append(scope)
        for n in node.nodes:
            if self.return_:
                break
            if isinstance(n, Break):
                break
            elif isinstance(n, Continue):
                continue
            elif isinstance(n, Return):
                self.return_ = True
            else:
                self.visit(node, n)
        self.scope.pop()

    def visit_Params(self, parent, node):
        pass

    def visit_Args(self, parent, node):
        func = parent.id_.value
        impl = self.global_[func]
        scope = id(impl.block)
        self.scope.append(scope)
        for p, a in zip(impl.params.params, node.args):
            self.search_new_call = True
            id_ = self.visit(impl.block, p.id_)
            self.search_new_call = False
            arg = self.visit(impl.block, a)
            id_.value = arg
            if isinstance(arg, Symbol):
                id_.value = arg.value
        self.scope.pop()

    def visit_Elems(self, parent, node):
        id_ = self.get_symbol(parent.id_)
        for i, e in enumerate(node.elems):
            value = self.visit(node, e)
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
            return int(first) <= int(second)
        elif node.symbol == '>=':
            return int(first) >= int(second)
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
        first = self.visit(node, node.first)
        backup_first = first
        if isinstance(first, Symbol):
            first = first.value
        if node.symbol == '-':
            return -first
        elif node.symbol == '!':
            bool_first = first != 0
            return not bool_first
        elif node.symbol == '&':
            return backup_first
        else:
            return None

    def run(self):
        self.visit(None, self.ast)
