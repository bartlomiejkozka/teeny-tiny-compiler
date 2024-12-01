from backend.lexer import *

def test_getToken():
    assert lexer("*").getToken() == Token("*", TokenType.ASTERISK)
    assert lexer(">=").getToken() == Token(">=", TokenType.GTEQ)
    assert lexer("\"Hello Wrld\"").getToken() == Token("Hello Wrld", TokenType.STRING)
    assert lexer("123").getToken() == Token("123", TokenType.NUMBER)
    assert lexer("IF").getToken() == Token("IF", TokenType.IF)
    assert lexer("THEN").getToken() == Token("THEN", TokenType.THEN)
    assert lexer("PRINT").getToken()
    assert lexer("END").getToken() == Token("END", TokenType.END)
    assert lexer("GOTO").getToken() == Token("GOTO", TokenType.GOTO)
    assert lexer("LET").getToken() == Token("LET", TokenType.LET)
    assert lexer("==").getToken() == Token("==", TokenType.EQEQ)
    assert lexer("!=").getToken() == Token("!=", TokenType.NOTEQ)
    assert lexer("<=").getToken() == Token("<=", TokenType.LTEQ)
    assert lexer(">").getToken() == Token(">", TokenType.GT)
    assert lexer("<").getToken() == Token("<", TokenType.LT)
    assert lexer("=").getToken() == Token("=", TokenType.EQ)
    assert lexer("+").getToken() == Token("+", TokenType.PLUS)
    assert lexer("-").getToken() == Token("-", TokenType.MINUS)
    assert lexer("/").getToken() == Token("/", TokenType.SLASH)
    assert lexer("\n").getToken() == Token(tokenKind=TokenType.NEWLINE)
    
    