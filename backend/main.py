from lexer import *
from parser import *  
import sys
import subprocess

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

# def main():
#     print("Tiny compiler:")
#     if len(sys.argv) != 3:
#         sys.exit("Compiler needs:\nargv[1]-> source file\nargv[2]-> output file\nas program arguments!")
#     with open(sys.argv[1], "r") as inputFile:
#         source = inputFile.read()
    
#     l = lexer(source)
#     p = parser(l, emitter(sys.argv[2]))
#     p.program()
#     p.emitter.writeFile()
#     print("Parsing completed successfully!")

#     compile = subprocess.run(["gcc", sys.argv[2], "-o", "output"], capture_output=True, text=True)
#     if compile.returncode != 0:
#         sys.exit("Compilation failed!: " + compile.stderr)
#     else: print("Compilation completed successfully!\n")

#     run = subprocess.run(["./output"], capture_output=True, text=True)
#     print("Program output:")
#     print(run.stdout)

#     if run.stderr:
#         print("Runtime Errors:")
#         print(run.stderr)

def compileCcode(sourceFile):
    compile = subprocess.run(["gcc", sourceFile, "-o", "output"], capture_output=True, text=True)
    if compile.returncode != 0:
        sys.exit("Compilation failed!: " + compile.stderr)
    else: print("Compilation completed successfully!\n")

    run = subprocess.run(["./output"], capture_output=True, text=True)
    return run.stdout


def start_frontend():
    # Start Python's built-in HTTP server for the frontend
    subprocess.Popen(["python3", "-m", "http.server", "8888", "--directory", "../frontend"])


app = FastAPI()

origins = [ "http://localhost:8888" ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"] 
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    frontend_process = subprocess.Popen(
        ["python3", "-m", "http.server", "8888", "--directory", "../frontend"]
    )
    try:
        yield 
    finally:
        frontend_process.terminate()
app.router.lifespan_context = lifespan


class Code(BaseModel):
    code: str

@app.post("/run_code")
def run_code(source: Code):
    source_code = source.code
    # input code processing
    p = parser(lexer(source_code), emitter("output.c"))
    p.program()
    p.emitter.writeFile()
    return {"code": compileCcode("output.c")}


if __name__ == "__main__":
    subprocess.run(["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"])


