from lexer import *
from emitter import *

class parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.currToken = None
        self.peekToken = None
        self.currLine = 1
        self.nextToken()
        self.nextToken()
    
        self.defVar = []
        self.gotoed = []
        self.gotoedFrom = []

        self.alreadyNewLine = False
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


    def abortVar(self):
        sys.exit("not defined variable: " + str(self.currToken))


    def matchToken(self, kind):
        if not self.checkToken(kind):
            self.abort()
        self.nextToken()

    
    def program(self):
        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("#include <stdlib.h>")
        self.emitter.headerLine("int main() {")
        while not self.checkToken(TokenType.EOF):
            if (self.currLine + 1) in self.gotoed:  # the while logic
                self.emitter.emit("}")
            self.statement()
            self.currLine += 1
        if self.defVar != []:
            self.emitter.headerLine("float " + ', '.join(self.defVar) + ";")
    

    def statement(self):
        if self.checkToken(TokenType.GOTO):  # probably done
            self.nextToken()
            tempNum = int(self.currToken.tokenText)
            tempNumFrom = self.currLine
            self.matchToken(TokenType.NUMBER)
            if tempNum not in self.gotoedFrom:
                self.gotoed.append(tempNum)
                self.gotoedFrom.append(tempNumFrom)

        elif self.checkToken(TokenType.IF): # probably done
            self.nextToken()
            
            # stupid method
            tempLexObj = lexer(self.lexer.source)
            tempLexObj.currIdx = self.lexer.currIdx
            tempLexObj.currChar = self.lexer.currChar
            isGoto = False
            currToken = tempLexObj.getToken().tokenKind
            while currToken != TokenType.NEWLINE:
                if currToken == TokenType.GOTO:
                    isGoto = True
                    break
                currToken = tempLexObj.getToken().tokenKind

            if isGoto: self.emitter.emit("while(")
            else: self.emitter.emit("if(")
            self.comparison()
            self.matchToken(TokenType.THEN)
            self.emitter.emit(") {")
            if any([self.checkToken(TokenType.GOTO), self.checkToken(TokenType.LET), self.checkToken(TokenType.PRINT)]):
                self.alreadyNewLine = True
                self.statement()
            else:
                self.expression()
            if not isGoto: self.emitter.emit("}")
            

        elif self.checkToken(TokenType.LET): # probably done
            self.nextToken()
            self.newIdent = self.currToken.tokenText
            self.matchToken(TokenType.IDENT)
            self.defVar.append(self.newIdent)
            self.emitter.emit(self.newIdent)
            self.matchToken(TokenType.EQ)
            self.emitter.emit(" = ")
            self.expression()
            self.emitter.emit(";")

        elif self.checkToken(TokenType.PRINT):  # probably done
            self.nextToken()
            if self.checkToken(TokenType.STRING): 
                self.emitter.emit(f'printf("%s\\n", "{self.currToken.tokenText}");')
                self.nextToken()
            else:
                self.emitter.emit("printf(\"%f\\n\", ") 
                self.primary()
                self.emitter.emit(");")

        elif self.checkToken(TokenType.IDENT):  # probably done 
            if(self.currToken.tokenText in self.defVar):
                self.emitter.emit(self.currToken.tokenText)
                self.nextToken()
                self.matchToken(TokenType.EQ)
                self.emitter.emit(" = ")
                self.expression()
                self.emitter.emit(";")
            else: 
                self.abortVar()

        elif self.checkToken(TokenType.END):    # probably done
            self.emitter.emitLine("return 0;")
            self.emitter.emit("}")
            self.nextToken()

        if not self.alreadyNewLine:
            self.nl() # prints new line
        else:
            self.alreadyNewLine = False

    
    def comparison(self):
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
        self.term()
        while any([self.checkToken(TokenType.PLUS), self.checkToken(TokenType.MINUS)]):
            self.emitter.emit(self.currToken.tokenText)
            self.nextToken()
            self.term()

    
    def term(self):
        self.semiUnary()
        while any([self.checkToken(TokenType.ASTERISK), self.checkToken(TokenType.SLASH)]):
            self.emitter.emit(self.currToken.tokenText)
            self.nextToken()
            self.semiUnary()


    def semiUnary(self):
        if self.checkToken(TokenType.SQRT) and (self.checkPeek(TokenType.IDENT) or self.checkPeek(TokenType.NUMBER)):
            self.emitter.emit("sqrt(")
            self.nextToken()
            self.primary()
            self.emitter.emit(")")
        else:
            self.unary()

    
    def unary(self):
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(self.currToken.tokenText)
            self.nextToken()
        self.primary()

    
    def primary(self):
        if self.checkToken(TokenType.NUMBER) or self.checkToken(TokenType.IDENT):
            self.emitter.emit(self.currToken.tokenText)
            self.nextToken()
        else: self.abort()


    def nl(self):
        if self.checkToken(TokenType.EOF) or self.checkToken(TokenType.END): return
        self.matchToken(TokenType.NEWLINE)
        self.emitter.emitLine('')
    