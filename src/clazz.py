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

    ASSIGN = 21
    SEMICOLON = 22
    COMMA = 23
    
    TYPE = 24
    INT = 25
    CHAR = 26
    STRING = 27
    VOID = 28

    IF = 29
    ELSE = 30
    WHILE = 31
    FOR = 32

    BREAK = 33
    CONTINUE = 34
    RETURN = 35

    ID = 36
    MAIN = 37
    EOF = 38
