# Aluno: Gabriel Carneiro Marques Amado
# Matrícula: 12111ECP002
# ASA - CRUD estático de cadastro de alunos

from fastapi import FastAPI
from pydantic import BaseModel
import logging
from logging.config import dictConfig
from src.config import log_config

dictConfig(log_config)

app = FastAPI(debug=True)
logger = logging.getLogger("Logger")


class Aluno(BaseModel):
    nome_completo: str
    matricula: str
    curso: str


@app.get("/")
async def root():
    return {"root_response": "Sistema CRUD para cadastro de alunos"}


@app.get("/alunos/{id_aluno}")
async def get_aluno_by_id(id_aluno):
    pass
    logger.info(f"Parâmetro correto recebido: {id_aluno}")
    return f"Este aluno tem ID {id_aluno}"


@app.post("/alunos")
async def create_aluno(aluno: Aluno):
    pass
    logger.info(msg={"aluno_criado": aluno})
    return f"O aluno de nome {aluno.nome_completo}, matrícula {aluno.matricula} e curso {aluno.curso} foi criado"


@app.delete("/alunos/{id_aluno}")
async def delete_aluno(id_aluno):
    pass
    logger.info(f"Parâmetro correto recebido: {id_aluno}")
    return f"O aluno de ID {id_aluno} foi deletado"


@app.put("/alunos/{id_aluno}")
async def update_aluno(id_aluno, novo_aluno: Aluno):
    pass
    logger.info(f"Novo aluno atualizado - ID {id_aluno}")
    return {"novo_aluno": novo_aluno}
