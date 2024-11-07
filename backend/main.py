from lexer import *
from parser import *  
from database import *

import sys
import subprocess
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
import webbrowser
import asyncio
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
import uuid
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


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
database = Database()        # CHANGE
database.create_tables()

origins = [ "http://localhost:8888" ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"] 
)

# Authentication user functions:
def isUserYet(user: User, db: Session = Depends(database.get_session)):
    return db.query(User).filter(User.login == user.login).first()

def isLoginPasswordCorrect(user: User, db: Session = Depends(database.get_session)):
    return db.query(User).filter(User.login == user.login).filter(User.password == user.password).first()

def get_current_user(request: Request):
    session_token = request.cookies.get("session_token")
    if session_token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    session = database.get_session()
    user_id = session.query(SessionToken).filter(SessionToken.token == session_token).first().user_id
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated01")
    
    return {"user_id": user_id}


@asynccontextmanager
async def lifespan(app: FastAPI):
    frontend_process = subprocess.Popen(
        ["python3", "-m", "http.server", "8888", "--directory", "../frontend/"]
    )
    # Give the server a moment to start
    await asyncio.sleep(1)
    # Open the frontend in the web browser
    webbrowser.open("http://localhost:8888")
    try:
        yield 
    finally:
        frontend_process.terminate()
app.router.lifespan_context = lifespan


class Code(BaseModel):
    code: str
class CodeName(BaseModel):
    name: str
class User(BaseModel):
    name: str
    login: str
    password: str


@app.post("/signup")
def register(user: User, db: Session = Depends(database.get_session)):
    if isUserYet(user) is not None:
        raise HTTPException(status_code=400, detail="User already exists!")
    db.add(User(name=user.name, login=user.login, password=user.password))
    db.commit()
    return {"user": "User registered successfully!"}


@app.post("/signin")
def login(user: User, db: Session = Depends(database.get_session)):
    if isLoginPasswordCorrect(user) is None:
        raise HTTPException(status_code=400, detail="Incorrect login or password!")
    
    session_token = str(uuid.uuid4())
    db.add(SessionToken(token=session_token, user_id=user.id))
    db.commit()
    #response = JSONResponse(content={"message": "Logged in successfully!"})
    response = RedirectResponse(url="/")
    response.set_cookie(key="session_token", value=session_token, httponly=True)
    return response


@app.get("/")
def read_root(request: Request, user: dict = Depends(get_current_user)):
    #return templates.TemplateResponse("home.html", {"request": request})
    
    


@app.post("/run_code")
def run_code(source: Code):
    source_code = source.code
    # input code processing
    p = parser(lexer(source_code), emitter("output.c"))
    p.program()
    p.emitter.writeFile()
    return {"code": compileCcode("output.c")}

# authentication required
@app.post("/save_code")
def save_code(source: Code, source_name: CodeName, db: Session = Depends(database.get_session), user: dict = Depends(get_current_user)):
    source_code = source.code
    db.add(Script(pesudo_code=source_code, user_id=user["user_id"]))
    db.commit()
    return {"code": "Code saved successfully!"}




if __name__ == "__main__":
    subprocess.run(["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"])


