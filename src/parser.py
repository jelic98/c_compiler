from src.token import Class
from functools import wraps
import pickle


class Parser:
#ok
    def __init__(self, lexer):
        self.lexer = lexer
        self.curr = self.lexer.next_token()

#ok
    def restorable(call):
        @wraps(call)
        def wrapper(self, *args, **kwargs):
            state = pickle.dumps(self.__dict__)
            result = call(self, *args, **kwargs)
            self.__dict__ = pickle.loads(state)
            return result

        return wrapper

#ok
    def eat(self, class_):
        if self.curr.class_ == class_:
            self.curr = self.lexer.next_token()
        else:
            self.die_type(class_.name, self.curr.class_.name)

#ok
    def jump(self, start, end):
        depth = 0
        while self.curr.class_ != Class.EOF:
            if self.curr.class_ == start:
                depth += 1
            elif self.curr.class_ == end:
                depth -= 1
                if depth < 0:
                    break
            self.eat(self.curr.class_)

    def program(self):
        nodes = []
        while self.curr.class_ != Class.EOF:
            if self.curr.class_ == POSTOJANJE_POCETAK:
                nodes.append(self.postojanje())
            elif self.curr.class_ == DODELA_POCETAK:
                nodes.append(self.dodela())
            elif self.curr.class_ == NAREDBA_POCETAK:
                nodes.append(self.naredba())
            elif self.curr.class_ == RUTINA_POCETAK:
                nodes.append(self.rutina())
            else:
                self.die_deriv(program.__name__)
        return Program(nodes)
    
#ok
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

#ok
    def while_(self):
        self.eat(Class.WHILE)
        self.eat(Class.LPAREN)
        cond = self.logic()
        self.eat(Class.RPAREN)
        self.eat(Class.LBRACE)
        block = self.block()
        self.eat(Class.RBRACE)
        return While(cond, block)

#ok
    def for_(self):
        self.eat(Class.FOR)
        self.eat(Class.LPAREN)
        init = self.assign()
        self.eat(Class.SEMICOLON)
        cond = self.logic()
        self.eat(Class.SEMICOLON)
        step = self.expr()
        self.eat(Class.RPAREN)
        self.eat(Class.LBRACE)
        block = self.block()
        self.eat(Class.RBRACE)
        return For(init, cond, step, block)

#ok
    def decl(self):
        type_ = self.type_()
        id_ = self.id_()

        if self.curr.class_ == Class.LBRACKET:
            self.eat(Class.LBRACKET)
            size = self.expr()
            self.eat(Class.RBRACKET)
            if self.curr.class_ == Class.ASSIGN:
                self.eat(Class.ASSIGN)
                self.eat(Class.LBRACE)
                elems = self.args()
                self.eat(Class.RBRACE)
                decl = ArrayDecl(type_, id_, size, elems)
        else:
            decl = Decl(type_, id_)
        return decl

#ok
    def func_impl(self):
        type_ = self.type_()
        id_ = self.id_()
        self.eat(Class.LPAREN)
        params = self.params()
        self.eat(Class.RPAREN)
        self.eat(Class.LBRACE)
        block = self.block()
        self.eat(Class.RBRACE)
        return FuncImpl(type_, id_, params, block)

#ok
    def block():
        self.eat(Class.LBRACE)
        block = []
        while self.curr.class_ != Class.RBRACE:
            if self.curr.class_ == Class.IF:
                block.append(self.if_())
            elif self.curr.class_ == Class.WHILE:
                block.append(self.while_())
            elif self.curr.class_ == Class.FOR:
                block.append(self.for_())
            elif self.curr.class_ == Class.BREAK:
                block.append(self.break_())
            elif self.curr.class_ == Class.CONTINUE:
                block.append(self.continue_())
            elif self.curr.class_ == Class.RETURN:
                block.append(self.return_())
            elif self.curr.class_ == Class.TYPE:
                block.append(self.decl())
                self.eat(Class.SEMICOLON)
            elif self.curr.class_ == Class.ID:
                block.append(self.id_())
                self.eat(Class.SEMICOLON)
            else:
                self.die_deriv(program.__name__)
        self.eat(Class.RBRACE)
        return Block(block)

    def args():
        self.eat(Class.LPAREN)
        args = []
        while self.curr.class_ != Class.RPAREN:
            args.append(self.logic())
            if self.curr.class_ == Class.INT:
                self.eat(Class.INT)
            elif self.curr.class_ == Class.CHAR:
                self.eat(Class.CHAR)
            elif self.curr.class_ == Class.STRING:
                self.eat(Class.STRING)
            elif self.curr.class_ == Class.COMMA:
                self.eat(Class.COMMA)
        self.eat(Class.RPAREN)
        return Args(args)

#ok
    def return_(self):
        self.eat(Class.RETURN)
        expr = self.logic()
        self.eat(Class.SEMICOLON)
        return Return(expr)

#ok
    def break_(self):
        self.eat(Class.BREAK)
        self.eat(Class.SEMICOLON)
        return Break()

#ok
    def continue_(self):
        self.eat(Class.CONTINUE)
        self.eat(Class.SEMICOLON)
        return Continue()

#ok
    def type_(self):
        type_ = Type(self.curr.lexeme)
        self.eat(Class.TYPE)
        return type_
    
#ok
    def id_(self):
        id_ = Id(self.curr.lexeme)
        self.eat(Class.ID)
        if self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            args = self.args() 
            self.eat(Class.RPAREN)
            return FuncCall(id_, args)
        else:
            if self.curr.class_ == Class.LBRACKET:
                self.eat(Class.LBRACKET)
                index = self.expr()
                self.eat(Class.RBRACKET)
                return ArrayElem(id_, index)
            elif self.curr.class_ == Class.ASSIGN:
                self.eat(Class.ASSIGN)
                expr = self.logic()
                return Assign(id_, expr)
            else:
                return id_

#ok
    def factor(self):
        if self.curr.class_ == Class.INT:
            self.eat(Class.INT)
            return Int(self.curr.lexeme)
        elif self.curr.class_ == Class.CHAR:
            self.eat(Class.CHAR)
            return Char(self.curr.lexeme)
        elif self.curr.class_ == Class.STRING:
            self.eat(Class.STRING)
            return String(self.curr.lexeme)
        elif self.curr.class_ == Class.ID:
            return self.variable()
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
            self.die_deriv(factor.__name__)

#ok
    def term(self):
        first = self.factor()
        while self.curr.class_ in [Class.STAR, Class.FWDSLASH, Class.PERCENT]:
            if self.curr.class_ == Class.STAR:
                self.eat(Class.STAR)
                second = self.factor()
                first = BinOp(self.curr.lexeme, first, second)
            elif self.curr.class_ == Class.FWDSLASH:
                self.eat(Class.FWDSLASH)
                second = self.factor()
                first = BinOp(self.curr.lexeme, first, second)
            elif self.curr.class_ == Class.PERCENT:
                self.eat(Class.PERCENT)
                second = self.factor()
                first = BinOp(self.curr.lexeme, first, second)
        return first

#ok
    def expr(self):
        first = self.term()
        while self.curr.class_ in [Class.PLUS, Class.MINUS]:
            if self.curr.class_ == Class.PLUS:
                self.eat(PLUS)
                second = self.term()
                first = BinOp(self.curr.lexeme, first, second)
            elif self.curr.class_ == Class.MINUS:
                self.eat(MINUS)
                second = self.term()
                first = BinOp(self.curr.lexeme, first, second)
        return first

#ok
    def compare(self):
        first = self.expr()
        if self.curr.class_ == Class.EQ:
            self.eat(Class.EQ)
            second = self.expr()
            return BinOp(self.curr.lexeme, first, second)
        elif self.curr.class_ == Class.NEQ:
            self.eat(Class.NEQ)
            second = self.expr()
            return BinOp(self.curr.lexeme, first, second)
        elif self.curr.class_ == Class.LT:
            self.eat(Class.LT)
            second = self.expr()
            return BinOp(self.curr.lexeme, first, second)
        elif self.curr.class_ == Class.GT:
            self.eat(Class.GT)
            second = self.expr()
            return BinOp(self.curr.lexeme, first, second)
        elif self.curr.class_ == Class.LTE:
            self.eat(Class.LTE)
            second = self.expr()
            return BinOp(self.curr.lexeme, first, second)
        elif self.curr.class_ == Class.GTE:
            self.eat(Class.GTE)
            second = self.expr()
            return BinOp(self.curr.lexeme, first, second)
        else:
            return first
#ok
    def logic(self):
        first = self.compare()
        if self.curr.class_ == Class.AND:
            self.eat(Class.AND)
            second = self.compare()
            return BinOp('&&', first, second)
        elif self.curr.class_ == Class.OR:
            self.eat(Class.OR)
            second = self.compare()
            return BinOp('||', first, second)
        else:
            return first

#ok
    def die(self, text):
        raise SystemExit(text)

#ok
    def die_deriv(self, fun):
        nodes.append("Derivation error: {}".format(fun))

#ok
    def die_type(self, expected, found):
        self.die("Expected: {}, Found: {}".format(expected, found))
