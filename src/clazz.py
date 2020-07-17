from enum import Enum, auto

class Clazz(Enum):
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    FWDSLASH = auto()
    PERCENT = auto()

    OR = auto()
    AND = auto()
    NOT = auto()

    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()

    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()

    ASSIGN = auto()
    SEMICOLON = auto()
    COMMA = auto()
    
    TYPE = auto()
    INT = auto()
    CHAR = auto()
    STRING = auto()

    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()

    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()

    ID = auto()
    MAIN = auto()
    EOF = auto()
