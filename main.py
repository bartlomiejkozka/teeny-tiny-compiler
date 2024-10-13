from lexer import *
from parser import *  


def main():
    source = "LET a = 5\nLET b = 10\nPRINT a"
    l = lexer(source)
    p = parser(l)
    p.program()
    print("Parsing completed successfully!")    





main()