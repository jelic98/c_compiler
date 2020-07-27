class Symbol:
    def __init__(self, id_, type_, scope):
        self.id_ = id_
        self.type_ = type_
        self.scope = scope

    def __str__(self):
        return "<{} {} {}>".format(self.id_, self.type_, self.scope)

    def copy(self):
        return Symbol(self.id_, self.type_, self.scope)


class Symbols:
    def __init__(self):
        self.symbols = {}

    def put(self, id_, type_, scope):
        self.symbols[id_] = Symbol(id_, type_, scope)

    def get(self, id_):
        return self.symbols[id_]

    def contains(self, id_):
        return id_ in self.symbols

    def remove(self, id_):
        del self.symbols[id_]

    def __str__(self):
        out = ""
        for _, value in self.symbols.items():
            if len(out) > 0:
                out += "\n"
            out += str(value)
        return out

    def __iter__(self):
        return iter(self.symbols.values())

    def __next__(self):
        return next(self.symbols.values())
