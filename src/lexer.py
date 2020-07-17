from src.clazz import Clazz
from src.token import Token


class Lexer():
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def read_space(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def read_char(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.die("")
        lexeme = self.text[self.pos]
        return lexeme

    def read_int(self):
        lexeme = ''
        while (self.pos < len(self.text) and self.text[self.pos].isdigit()):
            lexeme += self.text[self.pos]
            self.pos += 1
        self.pos -= 1
        return int(lexeme)

    def read_string(self):
        lexeme = ''
        self.pos += 1
        while (self.pos < len(self.text) and self.text[self.pos] != '"'):
            lexeme += self.text[self.pos]
            self.pos += 1
        return lexeme

    def read_keyword(self):
        curr = ''
        while (self.pos < len(self.text) and self.text[self.pos].isalpha()):
            curr += self.text[self.pos]
            self.pos += 1
        self.pos -= 1
        if curr == 'if':
            return Token(Clazz.IF, curr)
        elif curr == 'else':
            return Token(Clazz.ELSE, curr)
        elif curr == 'while':
            return Token(Clazz.WHILE, curr)
        elif curr == 'for':
            return Token(Clazz.FOR, curr)
        elif curr == 'break':
            return Token(Clazz.BREAK, curr)
        elif curr == 'continue':
            return Token(Clazz.CONTINUE, curr)
        elif curr == 'return':
            return Token(Clazz.RETURN, curr)
        elif curr == 'main':
            return Token(Clazz.MAIN, curr)
        elif curr == 'int' or curr == 'char' or curr == 'void':
            return Token(Clazz.TYPE, curr)
        return Token(Clazz.ID, curr)

    def next_token(self):
        self.read_space()
        if self.pos >= len(self.text):
            return Token(Clazz.EOF, None)
        curr = self.text[self.pos]
        token = None
        if curr.isalpha():
            token = self.read_keyword()
        elif curr.isdigit():
            token = Token(Clazz.INT, self.read_int())
        elif curr == '"':
            token = Token(Clazz.STRING, self.read_string())
        elif curr == '+':
            token = Token(Clazz.PLUS, curr)
        elif curr == '-':
            token = Token(Clazz.MINUS, curr)
        elif curr == '*':
            token = Token(Clazz.STAR, curr)
        elif curr == '/':
            token = Token(Clazz.FWDSLASH, curr)
        elif curr == '%':
            token = Token(Clazz.PERCENT, curr)
        elif curr == '&':
            curr = self.read_char()
            if curr == '&':
                token = Token(Clazz.AND, curr)
            else:
                self.die(curr)
        elif curr == '|':
            curr = self.read_char()
            if curr == '|':
                token = Token(Clazz.OR, curr)
            else:
                self.die(curr)
        elif curr == '!':
            curr = self.read_char()
            if curr == '=':
                token = Token(Clazz.NEQ, '!=')
            else:
                token = Token(Clazz.NOT, '!')
                self.pos -= 1
        elif curr == '=':
            curr = self.read_char()
            if curr == '=':
                token = Token(Clazz.EQ, '==')
            else:
                token = Token(Clazz.ASSIGN, '=')
                self.pos -= 1
        elif curr == '<':
            token = Token(Clazz.LT, curr)
        elif curr == '>':
            token = Token(Clazz.GT, curr)
        elif curr == '<':
            curr = self.read_char()
            if curr == '=':
                token = Token(Clazz.LTE, curr)
            else:
                self.die(curr)
        elif curr == '>':
            curr = self.read_char()
            if curr == '=':
                token = Token(Clazz.GTE, curr)
            else:
                self.die(curr)
        elif curr == '(':
            token = Token(Clazz.LPAREN, curr)
        elif curr == ')':
            token = Token(Clazz.RPAREN, curr)
        elif curr == '[':
            token = Token(Clazz.LBRACKET, curr)
        elif curr == ']':
            token = Token(Clazz.RBRACKET, curr)
        elif curr == '{':
            token = Token(Clazz.LBRACE, curr)
        elif curr == '}':
            token = Token(Clazz.RBRACE, curr)
        elif curr == ';':
            token = Token(Clazz.SEMICOLON, curr)
        elif curr == ',':
            token = Token(Clazz.SEMICOLON, curr)
        else:
            self.die(curr)
        self.pos += 1
        return token

    def die(self, char):
        raise SystemExit("Unexpected character {}".format(char))
