from enum import Enum

class TokenType(Enum):
    # General token:
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2   # for example name of the variable
    STRING = 3
    # Keywords:
    GOTO = 101
    LET = 102
    IF = 103
    SQRT = 104
    THEN = 105
    PRINT = 106
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

class Token:
    def __init__(self, tokenText=None, tokenKind=None):
        self.tokenText = tokenText
        self.tokenKind = tokenKind
    
    def __repr__(self):
        return f"Token(value={self.tokenText}, type={self.tokenKind})"
    