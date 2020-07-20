from src.token import Class
from src.nodes import *
from functools import wraps
import pickle


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.curr = self.lexer.next_token()
        self.prev = None

    def restorable(call):
        @wraps(call)
        def wrapper(self, *args, **kwargs):
            state = pickle.dumps(self.__dict__)
            result = call(self, *args, **kwargs)
            self.__dict__ = pickle.loads(state)
            return result

        return wrapper

    def eat(self, class_):
        if self.curr.class_ == class_:
            self.prev = self.curr
            self.curr = self.lexer.next_token()
        else:
            self.die_type(class_.name, self.curr.class_.name)

    def program(self):
        nodes = []
        while self.curr.class_ != Class.EOF:
            if self.curr.class_ == Class.TYPE:
                nodes.append(self.decl())
            else:
                self.die_deriv(self.program.__name__)
        return Program(nodes)

    def id_(self):
        is_array_elem = self.prev.class_ != Class.TYPE
        id_ = Id(self.curr.lexeme)
        self.eat(Class.ID)
        if self.curr.class_ == Class.LPAREN and self.is_func_call():
            self.eat(Class.LPAREN)
            args = self.args()
            self.eat(Class.RPAREN)
            return FuncCall(id_, args)
        elif self.curr.class_ == Class.LBRACKET and is_array_elem:
            self.eat(Class.LBRACKET)
            index = self.expr()
            self.eat(Class.RBRACKET)
            id_ = ArrayElem(id_, index)
        if self.curr.class_ == Class.ASSIGN:
            self.eat(Class.ASSIGN)
            expr = self.expr()
            return Assign(id_, expr)
        else:
            return id_

    def decl(self):
        type_ = self.type_()
        id_ = self.id_()
        if self.curr.class_ == Class.LBRACKET:
            self.eat(Class.LBRACKET)
            size = None
            if self.curr.class_ != Class.RBRACKET:
                size = self.expr()
            self.eat(Class.RBRACKET)
            elems = None
            if self.curr.class_ == Class.ASSIGN:
                self.eat(Class.ASSIGN)
                self.eat(Class.LBRACE)
                elems = self.elems()
                self.eat(Class.RBRACE)
            self.eat(Class.SEMICOLON)
            return ArrayDecl(type_, id_, size, elems)
        elif self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            params = self.params()
            self.eat(Class.RPAREN)
            if self.curr.class_ == Class.LBRACE:
                self.eat(Class.LBRACE)
                block = self.block()
                self.eat(Class.RBRACE)
                return FuncImpl(type_, id_, params, block)
            else:
                self.eat(Class.SEMICOLON)
                return FuncDecl(type_, id_, params)
        else:
            self.eat(Class.SEMICOLON)
            return Decl(type_, id_)

    def if_(self):
        self.eat(Class.IF)
        self.eat(Class.LPAREN)
        cond = self.logic()
        self.eat(Class.RPAREN)
        self.eat(Class.LBRACE)
        true = self.block()
        self.eat(Class.RBRACE)
        self.eat(Class.ELSE)
        self.eat(Class.LBRACE)
        false = self.block()
        self.eat(Class.RBRACE)
        return If(cond, true, false)

    def while_(self):
        self.eat(Class.WHILE)
        self.eat(Class.LPAREN)
        cond = self.logic()
        self.eat(Class.RPAREN)
        self.eat(Class.LBRACE)
        block = self.block()
        self.eat(Class.RBRACE)
        return While(cond, block)

    def for_(self):
        self.eat(Class.FOR)
        self.eat(Class.LPAREN)
        init = self.id_()
        self.eat(Class.SEMICOLON)
        cond = self.logic()
        self.eat(Class.SEMICOLON)
        step = self.id_()
        self.eat(Class.RPAREN)
        self.eat(Class.LBRACE)
        block = self.block()
        self.eat(Class.RBRACE)
        return For(init, cond, step, block)

    def block(self):
        nodes = []
        while self.curr.class_ != Class.RBRACE:
            if self.curr.class_ == Class.IF:
                nodes.append(self.if_())
            elif self.curr.class_ == Class.WHILE:
                nodes.append(self.while_())
            elif self.curr.class_ == Class.FOR:
                nodes.append(self.for_())
            elif self.curr.class_ == Class.BREAK:
                nodes.append(self.break_())
            elif self.curr.class_ == Class.CONTINUE:
                nodes.append(self.continue_())
            elif self.curr.class_ == Class.RETURN:
                nodes.append(self.return_())
            elif self.curr.class_ == Class.TYPE:
                nodes.append(self.decl())
            elif self.curr.class_ == Class.ID:
                nodes.append(self.id_())
                self.eat(Class.SEMICOLON)
            else:
                self.die_deriv(self.block.__name__)
        return Block(nodes)

    def params(self):
        params = []
        while self.curr.class_ != Class.RPAREN:
            if len(params) > 0:
                self.eat(Class.COMMA)
            type_ = self.type_()
            id_ = self.id_()
            params.append(Decl(type_, id_))
        return Params(params)

    def args(self):
        args = []
        while self.curr.class_ != Class.RPAREN:
            if len(args) > 0:
                self.eat(Class.COMMA)
            args.append(self.expr())
            if self.curr.class_ == Class.INT:
                self.eat(Class.INT)
            elif self.curr.class_ == Class.CHAR:
                self.eat(Class.CHAR)
            elif self.curr.class_ == Class.STRING:
                self.eat(Class.STRING)
        return Args(args)

    def elems(self):
        elems = []
        while self.curr.class_ != Class.RBRACE:
            if len(elems) > 0:
                self.eat(Class.COMMA)
            elems.append(self.expr())
            if self.curr.class_ == Class.INT:
                self.eat(Class.INT)
            elif self.curr.class_ == Class.CHAR:
                self.eat(Class.CHAR)
            elif self.curr.class_ == Class.STRING:
                self.eat(Class.STRING)
        return Elems(elems)

    def return_(self):
        self.eat(Class.RETURN)
        expr = self.expr()
        self.eat(Class.SEMICOLON)
        return Return(expr)

    def break_(self):
        self.eat(Class.BREAK)
        self.eat(Class.SEMICOLON)
        return Break()

    def continue_(self):
        self.eat(Class.CONTINUE)
        self.eat(Class.SEMICOLON)
        return Continue()

    def type_(self):
        type_ = Type(self.curr.lexeme)
        self.eat(Class.TYPE)
        return type_

    def factor(self):
        if self.curr.class_ == Class.INT:
            value = Int(self.curr.lexeme)
            self.eat(Class.INT)
            return value
        elif self.curr.class_ == Class.CHAR:
            value = Char(self.curr.lexeme)
            self.eat(Class.CHAR)
            return value
        elif self.curr.class_ == Class.STRING:
            value = String(self.curr.lexeme)
            self.eat(Class.STRING)
            return value
        elif self.curr.class_ == Class.ID:
            return self.id_()
        elif self.curr.class_ in [Class.MINUS, Class.NOT]:
            op = self.curr
            if self.curr.class_ == Class.MINUS:
                self.eat(Class.MINUS)
            elif self.curr.class_ == Class.NOT:
                self.eat(Class.NOT)
            first = None
            if self.curr.class_ == Class.LPAREN:
                self.eat(Class.LPAREN)
                first = self.logic()
                self.eat(Class.RPAREN)
            else:
                first = self.factor()
            return UnOp(op.lexeme, first)
        elif self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            first = self.logic()
            self.eat(Class.RPAREN)
            return first
        elif self.curr.class_ == Class.ID:
            id_ = self.id_()
        else:
            self.die_deriv(self.factor.__name__)

    def term(self):
        first = self.factor()
        while self.curr.class_ in [Class.STAR, Class.FWDSLASH, Class.PERCENT]:
            if self.curr.class_ == Class.STAR:
                op = self.curr.lexeme
                self.eat(Class.STAR)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.FWDSLASH:
                op = self.curr.lexeme
                self.eat(Class.FWDSLASH)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.PERCENT:
                op = self.curr.lexeme
                self.eat(Class.PERCENT)
                second = self.factor()
                first = BinOp(op, first, second)
        return first

    def expr(self):
        first = self.term()
        while self.curr.class_ in [Class.PLUS, Class.MINUS]:
            if self.curr.class_ == Class.PLUS:
                op = self.curr.lexeme
                self.eat(Class.PLUS)
                second = self.term()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.MINUS:
                op = self.curr.lexeme
                self.eat(Class.MINUS)
                second = self.term()
                first = BinOp(op, first, second)
        return first

    def compare(self):
        first = self.expr()
        if self.curr.class_ == Class.EQ:
            op = self.curr.lexeme
            self.eat(Class.EQ)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.NEQ:
            op = self.curr.lexeme
            self.eat(Class.NEQ)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.LT:
            op = self.curr.lexeme
            self.eat(Class.LT)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.GT:
            op = self.curr.lexeme
            self.eat(Class.GT)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.LTE:
            op = self.curr.lexeme
            self.eat(Class.LTE)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.GTE:
            op = self.curr.lexeme
            self.eat(Class.GTE)
            second = self.expr()
            return BinOp(op, first, second)
        else:
            return first

    def logic(self):
        first = self.compare()
        if self.curr.class_ == Class.AND:
            op = self.curr.lexeme
            self.eat(Class.AND)
            second = self.compare()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.OR:
            op = self.curr.lexeme
            self.eat(Class.OR)
            second = self.compare()
            return BinOp(op, first, second)
        else:
            return first

    @restorable
    def is_func_call(self):
        self.eat(Class.LPAREN)
        self.args()
        self.eat(Class.RPAREN)
        return self.curr.class_ == Class.SEMICOLON

    def parse(self):
        return self.program()

    def die(self, text):
        raise SystemExit(text)

    def die_deriv(self, fun):
        self.die("Derivation error: {}".format(fun))

    def die_type(self, expected, found):
        self.die("Expected: {}, Found: {}".format(expected, found))
