from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")

class Aluno(BaseModel):
    nome: str
    matricula: str
    curso: str 

async def root():
    msg = {"response" : "HelloWorld"}
    return msg

@app.get("/parametro/{parametro_id}")
async def mostra_parametro(parametro_id):
    msg = f"O valor do parametro é {parametro_id}"
    return {"response" : msg}

@app.post("/alunos")
async def criar_aluno(aluno: Aluno):
    novo_aluno = Aluno(aluno.nome, aluno.matricula, aluno.curso)
    return {novo_aluno}  