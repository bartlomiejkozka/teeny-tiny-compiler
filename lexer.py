class lexer:
    def __init__(self, source):
        self.source = source + '\n'
        self.currIdx = 0
        self.currChar = ''

    def getToken():
        pass

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
