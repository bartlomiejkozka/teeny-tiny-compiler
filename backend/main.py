from lexer import *
from parser import *  
import sys
import subprocess

def main():
    print("Tiny compiler:")
    if len(sys.argv) != 3:
        sys.exit("Compiler needs:\nargv[1]-> source file\nargv[2]-> output file\nas program arguments!")
    with open(sys.argv[1], "r") as inputFile:
        source = inputFile.read()
    
    l = lexer(source)
    p = parser(l, emitter(sys.argv[2]))
    p.program()
    p.emitter.writeFile()
    print("Parsing completed successfully!")

    compile = subprocess.run(["gcc", sys.argv[2], "-o", "output"], capture_output=True, text=True)
    if compile.returncode != 0:
        sys.exit("Compilation failed!: " + compile.stderr)
    else: print("Compilation completed successfully!\n")

    run = subprocess.run(["./output"], capture_output=True, text=True)
    print("Program output:")
    print(run.stdout)

    if run.stderr:
        print("Runtime Errors:")
        print(run.stderr)




main()