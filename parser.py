from lexer import *
from emitter import *

class parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.currToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()
    
        self.VarDef = {}
        self.currLineText = ''


    def addToCurrLine(self, text):
        self.currLineText += text


    def addCurrLineToCode(self):
        self.emitter.emitLine(self.currLineText)
        self.currLineText = ''


    def addCurrLineToHeader(self):
        self.emitter.headerLine(self.currLineText)
        self.currLineText = ''


    def nextToken(self):
        self.currToken = self.peekToken
        self.peekToken = self.lexer.getToken()


    def checkToken(self, kind):
        return self.currToken.tokenKind == kind
    

    def checkPeek(self, kind):
        return self.peekToken.kind == kind
    

    def abort(self):
        sys.exit("Wrong syntax: \n" + "current Token: " + str(self.currToken) + "\n" + "next Token: " + str(self.peekToken))


    def matchToken(self, kind):
        if not self.checkToken(kind):
            self.abort()
        self.nextToken()

    
    def program(self):
        print("PROGRAM")
        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("#include <stdlib.h>")
        self.emitter.headerLine("int main() {")
        while not self.checkToken(TokenType.EOF):
            self.statement()
    
    def statement(self):
        if self.checkToken(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.nextToken()
            self.matchToken(TokenType.NUMBER)

        elif self.checkToken(TokenType.IF): # probably done
            print("STATEMENT-IF")
            self.emitter.emit("if(")
            self.nextToken()
            self.comparison()
            self.matchToken(TokenType.THEN)
            self.emitter.emit(") {")
            if any([self.checkToken(TokenType.GOTO), self.checkToken(TokenType.LET), self.checkToken(TokenType.PRINT)]):
                self.statement()
            else:
                self.expression()

        elif self.checkToken(TokenType.LET): # probably done
            print("STATEMENT-LET")
            self.nextToken()
            self.newIdent = self.currToken.tokenText
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
        # add the elif for the operation on defined variables
        
        self.nl()

    
    def comparison(self):
        print("COMPARISON")
        self.expression()
        if any([self.checkToken(TokenType.EQEQ), self.checkToken(TokenType.NOTEQ), self.checkToken(TokenType.LT), self.checkToken(TokenType.LTEQ), self.checkToken(TokenType.GT), self.checkToken(TokenType.GTEQ)]):
            self.emitter.emit(self.currToken.tokenText)
            self.nextToken()
        else: self.abort()
        self.expression()
        while any([self.checkToken(TokenType.EQEQ), self.checkToken(TokenType.NOTEQ), self.checkToken(TokenType.LT), self.checkToken(TokenType.LTEQ), self.checkToken(TokenType.GT), self.checkToken(TokenType.GTEQ)]):
            self.emitter.emit(self.currToken.tokenText)
            self.nextToken()
            self.expression()

    
    def expression(self):
        print("EXPRESSION")
        self.term()
        while any([self.checkToken(TokenType.PLUS), self.checkToken(TokenType.MINUS)]):
            #self.emitter.emit(self.currToken.tokenText)
            self.addToCurrLine(self.currToken.tokenText)
            self.nextToken()
            self.term()

    
    def term(self):
        print("TERM")
        self.semiUnary()
        while any([self.checkToken(TokenType.ASTERISK), self.checkToken(TokenType.SLASH)]):
            # self.emitter.emit(self.currToken.tokenText)
            self.addToCurrLine(self.currToken.tokenText)
            self.nextToken()
            self.semiUnary()


    def semiUnary(self):
        print("semiUnary (sqrt)")
        if self.checkToken(TokenType.SQRT) and (self.checkPeek(TokenType.IDENT) or self.checkPeek(TokenType.NUMBER)):
            self.addToCurrLine("sqrt(")
            # self.emitter.emit("sqrt(")
            self.nextToken()
            self.primary()
            self.addToCurrLine(")")
            # self.emitter.emit(")")
        else:
            self.unary()

    
    def unary(self):
        print("UNARY")
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.addToCurrLine(self.currToken.tokenText)
            # self.emitter.emit(self.currToken.tokenText)
            self.nextToken()
        self.primary()

    
    def primary(self):
        print("PRIMARY")
        if self.checkToken(TokenType.NUMBER) or self.checkToken(TokenType.IDENT):
            self.addToCurrLine(self.currToken.tokenText)
            # self.emitter.emit(self.currToken.tokenText)
            self.nextToken()
        else: self.abort()

    def nl(self):
        if self.checkToken(TokenType.EOF): return
        print("NEWLINE")
        self.matchToken(TokenType.NEWLINE)
    