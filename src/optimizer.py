from src.visitor import Visitor


class Optimizer(Visitor):
    def __init__(self, ast, symbols):
        self.ast = ast
        self.symbols = symbols

    def visit_Program(self, parent, node):
        pass

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

    def visit_FuncDecl(self, parent, node):
        pass

    def visit_FuncImpl(self, parent, node):
        pass

    def visit_FuncCall(self, parent, node):
        pass

    def visit_Block(self, parent, node):
        pass

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

    def optimize(self):
        self.visit(None, self.ast)
