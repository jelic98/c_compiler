import enum

class Clazz(enum.Enum):
    PLUS = 1
    MINUS = 2
    STAR = 3
    FWDSLASH = 4
    PERCENT = 5

    OR = 6
    AND = 7
    NOT = 8

    EQ = 9
    NEQ = 10
    LT = 11
    GT = 12
    LTE = 13
    GTE = 14

    LPAREN = 15
    RPAREN = 16
    LBRACKET = 17
    RBRACKET = 18
    LBRACE = 19
    RBRACE = 20

    SEMICOLON = 21
    
    INT = 22
    CHAR = 23
    STRING = 24
    VOID = 25

    IF = 26
    ELSE = 27
    WHILE = 28
    FOR = 29

    BREAK = 30
    CONTINUE = 31
    RETURN = 32

    ID = 33
    MAIN = 34
    EOF = 35
