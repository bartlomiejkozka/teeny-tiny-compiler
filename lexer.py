from token import Token
import re


class lexer:
    def __init__(self, source):
        self.source = source + '\n'
        self.currIdx = 0
        self.currChar = ''

    def getToken(self):
        self.skipWhiteSpace()
        self.skipComment()
        token = None

        match self.currChar:
            case "=":
                if self.getNextChar() == "=": 
                    token = Token(tokenKind=Token.EQEQ)
                    self.next2Char()
                else:                         
                    token =  Token(tokenKind=Token.EQ)
                    self.nextChar()
            case ">":
                if self.getNextChar() == "=": 
                    token = Token(tokenKind=Token.GTEQ)
                    self.next2Char()
                else:                         
                    token = Token(tokenKind=Token.GT)
                    self.nextChar()
            case "<":
                if self.getNextChar() == "=": 
                    token = Token(tokenKind=Token.LTEQ)
                    self.next2Char()
                else:                         
                    token = Token(tokenKind=Token.LT)
                    self.nextChar()
            case "!":
                if self.getNextChar() == "=": 
                    token = Token(tokenKind=Token.NOTEQ)
                    self.next2Char()
                else:                         
                    raise Exception("Wrong syntax!")            #temporary resolution !!!
            case "*":
                token = Token(tokenKind=Token.ASTERISK)
                self.nextChar()
            case "/":
                token = Token(tokenKind=Token.SLASH)
                self.nextChar()
            case "+":
                token = Token(tokenKind=Token.PLUS)
                self.nextChar()
            case "-":
                token = Token(tokenKind=Token.MINUS)
                self.nextChar()
            case "\\":
                if self.getNextChar() == "n":   
                    token = Token(tokenKind=Token.NEWLINE)
                    
                elif self.getNextChar() == "0": token = Token(tokenKind=Token.EOF)
                else:                           raise Exception("Wrong syntax!")
            case "\"":
                self.nextChar()
                startIdx = self.currIdx
                while self.currChar != "\"":
                    self.nextChar()
                token = Token(self.source[startIdx : self.currIdx], Token.STRING)
            case _ if re.match(r'[A-Za-z]', self.currChar):
                startIdx = self.currIdx
                while self.currChar.isalpha() is True:
                    self.nextChar()
                temp = self.source[startIdx:self.currIdx]
                match temp:
                    case Token.GOTO.__name__: token = Token(self.source[startIdx:self.currIdx], Token.GOTO)
                    case Token.END.__name__:  token = Token(self.source[startIdx:self.currIdx], Token.END)
                    case Token.IF.__name__:   token = Token(self.source[startIdx:self.currIdx], Token.IF)
                    case Token.SQRT.__name__: token = Token(self.source[startIdx:self.currIdx], Token.SQRT)
                    case Token.THEN.__name__: token = Token(self.source[startIdx:self.currIdx], Token.THEN)
                    case _:                   token = Token(self.source[startIdx : self.currIdx], Token.IDENT)
            case _ if self.currChar.isnumeric() is True:
                startIdx = self.currIdx
                while self.currChar.isnumeric() is True or (self.currChar == "." and self.getNextChar().isnumeric() is True):
                    self.nextChar()
                token = Token(self.source[startIdx:self.currIdx], Token.NUMBER)

        self.nextChar()

            

    def nextChar(self):
        self.currIdx += 1
        self.currChar = self.source[self.currIdx]
    
    def next2Char(self):
        self.currIdx += 2
        self.currChar = self.source[self.currIdx]

    def getNextChar(self): 
        return self.source[self.currIdx + 1] if self.source[self.currIdx] != '\n' else None

    def skipWhiteSpace(self):
        while self.currChar == ' ' or self.currChar == '\t':
            self.nextChar

    def skipComment(self):
        if self.currChar == '#' or self.currChar == '//':
            while self.currChar != '\n':
                self.nextChar()
        elif self.currChar == '/' and self.getNextChar() == '*':
            while self.currChar != '*' and self.nextChar != '/':
                self.nextChar()
            for _ in range(2): self.nextChar()
