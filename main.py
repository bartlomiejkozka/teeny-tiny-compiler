from lexer import *
from parser import *  
import sys

def main():
    print("Tiny compiler")
    if len(sys.argv) != 2:
        sys.exit("Compiler needs source file as argument!")
    with open(sys.argv[1], "r") as inputFile:
        source = inputFile.read()
    
    l = lexer(source)
    p = parser(l)
    p.program()
    print("Parsing completed successfully!")    





main()