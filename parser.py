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
        return self.currToken.tokenKind == kind
    

    # def checkPeek(self, kind):
    #     return self.peekToken.kind == kind
    

    def abort(self):
        sys.exit("Wrong syntax: \n" + "current Token: " + str(self.currToken) + "\n" + "next Token: " + str(self.peekToken))


    def matchToken(self, kind):
        if not self.checkToken(kind):
            self.abort()
        self.nextToken()

    
    def program(self):
        print("PROGRAM")
        while not self.checkToken(TokenType.EOF):
            self.statement()
    
    def statement(self):
        if self.checkToken(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.nextToken()
            self.matchToken(TokenType.NUMBER)
        elif self.checkToken(TokenType.IF):
            print("STATEMENT-IF")
            self.nextToken()
            self.comparison()
            self.matchToken(TokenType.THEN)
            self.expression()
        elif self.checkToken(TokenType.LET):
            print("STATEMENT-LET")
            self.nextToken()
            self.matchToken(TokenType.IDENT)
            self.matchToken(TokenType.EQ)
            self.expression()
        elif self.checkToken(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.nextToken()
            if self.checkToken(TokenType.STRING): self.nextToken()
            else: self.primary()
        elif self.checkToken(TokenType.EOF):
            pass
        
        self.nl()

    
    def comparison(self):
        print("COMPARISON")
        self.nextToken()
        self.expression()
        if any([self.checkToken(TokenType.EQEQ), self.checkToken(TokenType.NOTEQ), self.checkToken(TokenType.LT), self.checkToken(TokenType.LTEQ), self.checkToken(TokenType.GT), self.checkToken(TokenType.GTEQ)]):
            self.nextToken()
        else: self.abort()
        self.expression()
        while any([self.checkToken(TokenType.EQEQ), self.checkToken(TokenType.NOTEQ), self.checkToken(TokenType.LT), self.checkToken(TokenType.LTEQ), self.checkToken(TokenType.GT), self.checkToken(TokenType.GTEQ)]):
            self.nextToken()
            self.expression()

    
    def expression(self):
        print("EXPRESSION")
        self.term()
        while any([self.checkToken(TokenType.PLUS), self.checkToken(TokenType.MINUS)]):
            self.nextToken()
            self.term()

    
    def term(self):
        print("TERM")
        self.unary()
        while any([self.checkToken(TokenType.ASTERISK), self.checkToken(TokenType.SLASH)]):
            self.nextToken()
            self.unary()

    
    def unary(self):
        print("UNARY")
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
        self.primary()

    
    def primary(self):
        print("PRIMARY")
        if self.checkToken(TokenType.NUMBER) or self.checkToken(TokenType.IDENT):
            self.nextToken()
        else: self.abort()

    def nl(self):
        if self.checkToken(TokenType.EOF): return
        print("NEWLINE")
        self.matchToken(TokenType.NEWLINE)
    