from enum import Enum

class Token(Enum):
    # General token:
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2   # for example name of the variable
    STRING = 3
    # Keywords:
    GOTO = 101
    END = 102
    IF = 103
    SQRT = 104
    THEN = 105
    # Operators:
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211

