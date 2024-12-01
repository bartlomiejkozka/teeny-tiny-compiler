from backend.parser import *
import pytest

class TestParser:
    def test_print(self):
        parserT = parser(lexer("PRINT \"Hello World!\"\nEND"), emitter())
        parserT.program()
        assert parserT.emitter.code == "printf(\"%s\\n\", \"Hello World!\");\nreturn 0;\n}"

    def test_print_var(self):
        parserT = parser(lexer("PRINT a\n END"), emitter())
        parserT.program()
        assert parserT.emitter.code == "printf(\"%f\\n\", a);\nreturn 0;\n}"

    def test_let(self):
        parserT = parser(lexer("LET a = 5\n END"), emitter())
        parserT.program()
        assert parserT.emitter.code == "a = 5;\nreturn 0;\n}"

    def test_end(self):
        parserT = parser(lexer("END"), emitter())
        parserT.program()
        assert parserT.emitter.code == "return 0;\n}"

    def test_if(self):
        parserT = parser(lexer("IF a == 5 THEN PRINT a\n END"), emitter())
        parserT.program()
        assert parserT.emitter.code == "if(a==5) {printf(\"%f\\n\", a);}\nreturn 0;\n}"

    def test_goto(self):
        parserT = parser(lexer("LET a = 0\n IF a == 5 THEN GOTO 4\n a = a + 1\n PRINT a\n END"), emitter())
        parserT.program()
        assert parserT.emitter.code == "a = 0;\nwhile(!(a==5)) {\na = a+1;\n}\nprintf(\"%f\\n\", a);\nreturn 0;\n}"