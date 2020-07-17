class Token():
    def __init__(self, clazz, lexeme):
        self.clazz = clazz
        self.lexeme = lexeme

    def __str__(self):
        return "<{} {}>".format(self.clazz, self.lexeme)
