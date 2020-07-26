from src.visitor import Visitor


class Optimizer(Visitor):
    def __init__(self, ast):
        self.ast = ast
        self.global_ = None
        self.local = []
        self.remove_unused_symbols = False
        self.remove_current_symbol = False
        self.trash = []

    def remove_symbol(self, parent, node):
        if self.remove_unused_symbols:
            self.visit(node, node.id_)
            if self.remove_current_symbol:
                self.trash.append((parent, node))

    def visit_Program(self, parent, node):
        self.global_ = node.symbols
        for n in node.nodes:
            self.visit(node, n)
        self.remove_unused_symbols = True
        for n in node.nodes:
            self.visit(node, n)
        for parent, node in self.trash:
            parent.nodes.remove(node)

    def visit_Decl(self, parent, node):
        self.remove_symbol(parent, node)

    def visit_ArrayDecl(self, parent, node):
        self.remove_symbol(parent, node)
        if node.size is not None:
            self.visit(node, node.size)
        if node.elems is not None:
            self.visit(node, node.elems)

    def visit_ArrayElem(self, parent, node):
        self.visit(node, node.id_)
        self.visit(node, node.index)

    def visit_Assign(self, parent, node):
        self.visit(node, node.id_)
        self.visit(node, node.expr)

    def visit_If(self, parent, node):
        self.visit(node, node.cond)
        self.visit(node, node.true)
        self.visit(node, node.false)

    def visit_While(self, parent, node):
        self.visit(node, node.cond)
        self.visit(node, node.block)

    def visit_For(self, parent, node):
        self.visit(node, node.init)
        self.visit(node, node.cond)
        self.visit(node, node.block)
        self.visit(node, node.step)

    def visit_FuncImpl(self, parent, node):
        self.remove_symbol(parent, node)
        self.visit(node, node.block)

    def visit_FuncCall(self, parent, node):
        self.visit(node, node.id_)
        self.visit(node, node.args)

    def visit_Block(self, parent, node):
        self.local.append(node.symbols)
        for n in node.nodes:
            self.visit(node, n)
        self.local.pop()

    def visit_Params(self, parent, node):
        pass

    def visit_Args(self, parent, node):
        for a in node.args:
            self.visit(node, a)

    def visit_Elems(self, parent, node):
        for e in node.elems:
            self.visit(node, e)

    def visit_Break(self, parent, node):
        pass

    def visit_Continue(self, parent, node):
        pass

    def visit_Return(self, parent, node):
        if node.expr is not None:
            self.visit(node, node.expr)

    def visit_Type(self, parent, node):
        pass

    def visit_Int(self, parent, node):
        pass

    def visit_Char(self, parent, node):
        pass

    def visit_String(self, parent, node):
        pass

    def visit_Id(self, parent, node):
        id_ = node.value
        symbols = self.global_
        for scope in reversed(self.local):
            if scope.contains(id_):
                symbols = scope
                break
        if symbols.contains(id_):
            symbol = symbols.get(id_)
            if self.remove_unused_symbols:
                self.remove_current_symbol = False
                if not hasattr(symbol, 'used') and id_ != 'main':
                    self.remove_current_symbol = True
                    symbols.remove(id_)
            else:
                symbol.used = None

    def visit_BinOp(self, parent, node):
        self.visit(node, node.first)
        self.visit(node, node.second)

    def visit_UnOp(self, parent, node):
        self.visit(node, node.first)

    def optimize(self):
        self.visit(None, self.ast)
