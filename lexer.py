from token import Token


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
                    self.nextChar()
                else:                         
                    token =  Token(tokenKind=Token.EQEQ)
            case ">":
                if self.getNextChar() == "=": token = Token(tokenKind=Token.GTEQ)
                else:                         token = Token(tokenKind=Token.GT)
            case "<":
                if self.getNextChar() == "=": token = Token(tokenKind=Token.LTEQ)
                else:                         token = Token(tokenKind=Token.LT)
            case "!":
                if self.getNextChar() == "=": token = Token(tokenKind=Token.NOTEQ)
                else:                         raise Exception("Wrong syntax!")
            case "*":
                token = Token(tokenKind=Token.ASTERISK)
            case "/":
                token = Token(tokenKind=Token.SLASH)
            case "+":
                token = Token(tokenKind=Token.PLUS)
            case "-":
                token = Token(tokenKind=Token.MINUS)
            case "\\":
                if self.getNextChar() == "n":   token = Token(tokenKind=Token.NEWLINE)
                elif self.getNextChar() == "0": token = Token(tokenKind=Token.EOF)
                else:                           raise Exception("Wrong syntax!")
            case "\"":


        
        # if self.currChar == '=':
        #     if self.getNextChar() == "=":
        #         return Token(tokenKind=Token.EQEQ)
        #     else: return Token(tokenKind=Token.EQEQ)
        # elif self.currChar == ">":
        #     if self.getNextChar() == "=":
        #         return Token(tokenKind=Token.GTEQ)
        #     else: return Token(tokenKinf=Token.GT)
        # elif self.currChar == "<":
        #     if self.getNextChar() == "=":
        #         return Token(tokenKind=Token.LTEQ)
        #     else: return Token(tokenKinf=Token.LT)
        # elif self.currChar == "*":
        #     return Token(tokenKind=Token.ASTERISK)
        # elif self.currChar ==  



    def nextChar(self):
        self.currIdx += 1
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
