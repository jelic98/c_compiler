from src.token import Class, Token


class Lexer:
    def __init__(self, text):
        self.text = text
        self.len = len(text)
        self.pos = -1

    def read_space(self):
        while self.pos + 1 < self.len and self.text[self.pos + 1].isspace():
            self.next_char()

    def read_int(self):
        lexeme = self.text[self.pos]
        while self.pos + 1 < self.len and self.text[self.pos + 1].isdigit():
            lexeme += self.next_char()
        return int(lexeme)

    def read_char(self):
        self.pos += 1
        lexeme = self.text[self.pos]
        self.pos += 1
        return lexeme

    def read_string(self):
        lexeme = ''
        while self.pos + 1 < self.len and self.text[self.pos + 1] != '"':
            lexeme += self.next_char()
        self.pos += 1
        return lexeme

    def read_keyword(self):
        lexeme = self.text[self.pos]
        while self.pos + 1 < self.len and self.text[self.pos + 1].isalnum():
            lexeme += self.next_char()
        if lexeme == 'if':
            return Token(Clazz.IF, lexeme)
        elif lexeme == 'else':
            return Token(Clazz.ELSE, lexeme)
        elif lexeme == 'while':
            return Token(Clazz.WHILE, lexeme)
        elif lexeme == 'for':
            return Token(Clazz.FOR, lexeme)
        elif lexeme == 'break':
            return Token(Clazz.BREAK, lexeme)
        elif lexeme == 'continue':
            return Token(Clazz.CONTINUE, lexeme)
        elif lexeme == 'return':
            return Token(Clazz.RETURN, lexeme)
        elif lexeme == 'int' or lexeme == 'char' or lexeme == 'void':
            return Token(Clazz.TYPE, lexeme)
        return Token(Clazz.ID, lexeme)

    def next_char(self):
        self.pos += 1
        if self.pos >= self.len:
            return None
        return self.text[self.pos]

    def next_token(self):
        self.read_space()
        curr = self.next_char()
        if curr is None:
            return Token(Clazz.EOF, curr)
        token = None
        if curr.isalpha():
            token = self.read_keyword()
        elif curr.isdigit():
            token = Token(Clazz.INT, self.read_int())
        elif curr == '\'':
            token = Token(Clazz.CHAR, self.read_char())
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
            curr = self.next_char()
            if curr == '&':
                token = Token(Clazz.AND, curr)
            else:
                self.die(curr)
        elif curr == '|':
            curr = self.next_char()
            if curr == '|':
                token = Token(Clazz.OR, curr)
            else:
                self.die(curr)
        elif curr == '!':
            curr = self.next_char()
            if curr == '=':
                token = Token(Clazz.NEQ, '!=')
            else:
                token = Token(Clazz.NOT, '!')
                self.pos -= 1
        elif curr == '=':
            curr = self.next_char()
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
            curr = self.next_char()
            if curr == '=':
                token = Token(Clazz.LTE, curr)
            else:
                self.die(curr)
        elif curr == '>':
            curr = self.next_char()
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
            token = Token(Clazz.COMMA, curr)
        else:
            self.die(curr)
        return token

    def die(self, char):
        raise SystemExit("Unexpected character {}".format(char))
