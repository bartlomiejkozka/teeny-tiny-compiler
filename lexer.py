from myToken import *
import sys
import re


class lexer:
    def __init__(self, source):
        self.source = source + '\0'
        self.currIdx = 0
        self.currChar = self.source[self.currIdx]

    def getToken(self):
        self.skipWhiteSpace()
        self.skipComment()
        token = None

        match self.currChar:
            case "=":
                if self.getNextChar() == "=": 
                    token = Token(tokenKind=TokenType.EQEQ)
                    self.next2Char()
                else:                         
                    token =  Token(tokenKind=TokenType.EQ)
                    self.nextChar()
            case ">":
                if self.getNextChar() == "=": 
                    token = Token(tokenKind=TokenType.GTEQ)
                    self.next2Char()
                else:                         
                    token = Token(tokenKind=TokenType.GT)
                    self.nextChar()
            case "<":
                if self.getNextChar() == "=": 
                    token = Token(tokenKind=TokenType.LTEQ)
                    self.next2Char()
                else:                         
                    token = Token(tokenKind=TokenType.LT)
                    self.nextChar()
            case "!":
                if self.getNextChar() == "=": 
                    token = Token(tokenKind=TokenType.NOTEQ)
                    self.next2Char()
                else:                         
                    raise Exception("Wrong syntax!")            #temporary resolution !!!
            case "*":
                token = Token(tokenKind=TokenType.ASTERISK)
                self.nextChar()
            case "/":
                token = Token(tokenKind=TokenType.SLASH)
                self.nextChar()
            case "+":
                token = Token(tokenKind=TokenType.PLUS)
                self.nextChar()
            case "-":
                token = Token(tokenKind=TokenType.MINUS)
                self.nextChar()
            case "\n":
                token = Token(tokenKind=TokenType.NEWLINE)
                self.nextChar()
            case "\0": 
                token = Token(tokenKind=TokenType.EOF)  # no need go to next line
            case "\"":
                self.nextChar()
                startIdx = self.currIdx
                while self.currChar != "\"":
                    self.nextChar()
                token = Token(self.source[startIdx : self.currIdx], TokenType.STRING)
                self.nextChar()
            case _ if re.match(r'[A-Za-z]', self.currChar):
                startIdx = self.currIdx
                while self.currChar.isalpha() is True:
                    self.nextChar()
                temp = self.source[startIdx:self.currIdx]
                match temp:
                    case TokenType.GOTO.name: token = Token(self.source[startIdx:self.currIdx], TokenType.GOTO)
                    case TokenType.LET.name:  token = Token(self.source[startIdx:self.currIdx], TokenType.LET)
                    case TokenType.IF.name:   token = Token(self.source[startIdx:self.currIdx], TokenType.IF)
                    case TokenType.SQRT.name: token = Token(self.source[startIdx:self.currIdx], TokenType.SQRT)
                    case TokenType.THEN.name: token = Token(self.source[startIdx:self.currIdx], TokenType.THEN)
                    case TokenType.PRINT.name: token = Token(self.source[startIdx:self.currIdx], TokenType.PRINT)
                    case _:                   token = Token(self.source[startIdx : self.currIdx], TokenType.IDENT)
                #self.nextChar()
            case _ if self.currChar.isnumeric() is True:
                startIdx = self.currIdx
                while self.currChar.isnumeric() is True or (self.currChar == "." and self.getNextChar().isnumeric() is True):
                    self.nextChar()
                token = Token(self.source[startIdx:self.currIdx], TokenType.NUMBER)
                #self.nextChar()
        
        return token

            

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
            self.nextChar()

    def skipComment(self):
        if self.currChar == '#' or self.currChar == '//':
            while self.currChar != '\n':
                self.nextChar()
        elif self.currChar == '/' and self.getNextChar() == '*':
            while self.currChar != '*' and self.nextChar != '/':
                self.nextChar()
            for _ in range(2): self.nextChar()
