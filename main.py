from lexer import *
from parser import *  
import sys

def main():
    print("Tiny compiler")
    if len(sys.argv) != 3:
        sys.exit("Compiler needs source file and output file as arguments!")
    with open(sys.argv[1], "r") as inputFile:
        source = inputFile.read()
    
    l = lexer(source)
    p = parser(l, emitter(sys.argv[2]))
    p.program()
    p.emitter.writeFile()
    print("Parsing completed successfully!")    





main()