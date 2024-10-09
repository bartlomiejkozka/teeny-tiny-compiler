from lexer import *

class parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.currToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()
    

    def nextToken(self):
        self.currToken = self.peekToken
        self.peekToken = self.lexer.getToken()


    def checkToken(self, kind):
        return self.currToken.kind == kind
    

    # def checkPeek(self, kind):
    #     return self.peekToken.kind == kind
    

    def abort(self):
        sys.exit("Wrong syntax: \n" + "current Token: " + self.currToken + "\n" + "next Token: " + self.peekToken)


    def matchToken(self, kind):
        if not self.checkToken(kind):
            self.abort()
        self.nextToken()

    
    def program(self):
        print("PROGRAM")
        while not self.checkToken(Token.EOF):
            self.statement()
    
    def statement(self):
        if self.checkToken(Token.GOTO):
            print("STATEMENT-GOTO")
            self.nextToken()
            self.matchToken(Token.NUMBER)
        elif self.checkToken(Token.IF):
            print("STATEMENT-IF")
            self.nextToken()
            self.comparison()
            self.matchToken(Token.THEN)
            self.expression()
        elif self.checkToken(Token.LET):
            print("STATEMENT-LET")
            self.nextToken()
            self.matchToken(Token.IDENT)
            self.matchToken(Token.EQ)
            self.expression()
        elif self.checkToken(Token.PRINT):
            self.nextToken()
            if self.checkToken(Token.STRING): self.nextToken()
            else: self.primary()
        
        self.nl()

    
    def comparison(self):
        print("COMPARISON")
        self.nextToken()
        self.expression()
        if any(self.checkToken(Token.EQEQ), self.checkToken(Token.NOTEQ), self.checkToken(Token.LT), self.checkToken(Token.LTEQ), self.checkToken(Token.GT), self.checkToken(Token.GTEQ)):
            self.nextToken()
        else: self.abort()
        self.expression()
        while any(self.checkToken(Token.EQEQ), self.checkToken(Token.NOTEQ), self.checkToken(Token.LT), self.checkToken(Token.LTEQ), self.checkToken(Token.GT), self.checkToken(Token.GTEQ)):
            self.nextToken()
            self.expression()

    
    def expression(self):
        print("EXPRESSION")
        self.term()
        while any(self.checkToken(Token.PLUS), self.checkToken(Token.MINUS)):
            self.nextToken()
            self.term()

    
    def term(self):
        print("TERM")
        self.unary()
        while any(self.checkToken(Token.ASTERISK), self.checkToken(Token.SLASH)):
            self.nextToken()
            self.unary()

    
    def unary(self):
        print("UNARY")
        if self.checkToken(Token.PLUS) or self.checkToken(Token.MINUS):
            self.nextToken()
        self.primary()

    
    def primary(self):
        print("PRIMARY")
        if self.checkToken(Token.NUMBER) or self.checkToken(Token.IDENT):
            self.nextToken()
        else: self.abort()

    def nl(self):
        print("NEWLINE")
        self.matchToken(Token.NEWLINE)
    