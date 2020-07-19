from src.visitor import Visitor
from graphviz import Digraph


class Grapher(Visitor):
    def __init__(self, parser):
        self.parser = parser
        self._count = 1
        self.dot = Digraph()
        self.dot.node_attr['shape'] = 'box'
        self.dot.node_attr['height'] = '0.1'
        self.dot.edge_attr['arrowsize'] = '0.5'

    def add_node(self, parent, node):
        node._index = self._count
        self._count += 1
        self.dot.node('node{}'.format(node._index), type(node).__name__)
        if parent is not None:
            self.add_edge(parent, node)

    def add_edge(self, parent, node):
        src, dest = parent._index, node._index
        self.dot.edge('node{}'.format(src), 'node{}'.format(dest))

    def visit_Program(self, parent, node):
        self.add_node(parent, node)
        for n in node.nodes:
            self.visit(node, n)

    def visit_Decl(self, parent, node):
        self.add_node(parent, node)

    def visit_ArrayDecl(self, parent, node):
        self.add_node(parent, node)

    def visit_ArrayElem(self, parent, node):
        self.add_node(parent, node)

    def visit_Assign(self, parent, node):
        self.add_node(parent, node)

    def visit_If(self, parent, node):
        self.add_node(parent, node)

    def visit_While(self, parent, node):
        self.add_node(parent, node)

    def visit_For(self, parent, node):
        self.add_node(parent, node)

    def visit_FuncDecl(self, parent, node):
        self.add_node(parent, node)

    def visit_FuncImpl(self, parent, node):
        self.add_node(parent, node)
        self.visit(node, node.type_)
        self.visit(node, node.id_)
        self.visit(node, node.params)
        self.visit(node, node.block)

    def visit_FuncCall(self, parent, node):
        self.add_node(parent, node)

    def visit_Block(self, parent, node):
        self.add_node(parent, node)

    def visit_Params(self, parent, node):
        self.add_node(parent, node)

    def visit_Args(self, parent, node):
        self.add_node(parent, node)

    def visit_Break(self, parent, node):
        self.add_node(parent, node)

    def visit_Continue(self, parent, node):
        self.add_node(parent, node)

    def visit_Return(self, parent, node):
        self.add_node(parent, node)

    def visit_Type(self, parent, node):
        self.add_node(parent, node)

    def visit_Int(self, parent, node):
        self.add_node(parent, node)

    def visit_Char(self, parent, node):
        self.add_node(parent, node)

    def visit_String(self, parent, node):
        self.add_node(parent, node)

    def visit_Id(self, parent, node):
        self.add_node(parent, node)

    def visit_BinOp(self, parent, node):
        self.add_node(parent, node)

    def visit_UnOp(self, parent, node):
        self.add_node(parent, node)

    def graph(self):
        program = self.parser.program()
        self.visit(None, program)
        return self.dot.source
