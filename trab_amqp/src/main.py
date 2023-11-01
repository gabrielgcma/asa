# Universidade Federal de Uberlândia - Engenharia de Computação - FEELT
# Arquitetura de Software Aplicada
# Aluno: Gabriel Carneiro Marques Amado
# Matrícula: 12111ECP002

from fastapi import FastAPI
from classes import Request_Aluno
from models import Aluno
from database import session
from amqp.publisher import Publisher
from amqp.subscriber import Subscriber
import logging
from database import session
import uvicorn
import multiprocessing

logger = logging.getLogger(__name__)
logging.getLogger("pika").propagate = False
FORMAT = (
    "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
)
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "Success", "data": "No data"}


@app.get("/alunos")
async def get_all_alunos():
    alunos_query = session.query(Aluno)
    alunos = alunos_query.all()
    return {"status": "SUCESS", "data": alunos}


@app.post("/alunos")
async def criar_aluno(request_aluno: Request_Aluno):
    aluno_json = request_aluno

    try:
        publisher = Publisher()
        logger.info("Enviando registro de aluno para o broker...")
        publisher.publish("routing-key", aluno_json.model_dump_json().encode())
    except Exception as e:
        logger.error(f"Erro ao enviar registro de aluno para o broker -- criar_aluno()")
        print(e)
    return {
        "status": "Registro de aluno enviado com sucesso para o broker!",
        "data": aluno_json,
    }


if __name__ == "__main__":
    try:
        subscriber = Subscriber()
        subscriber_process = multiprocessing.Process(
            target=subscriber.receive_msgs, daemon=True, args=([session])
        )
        subscriber_process.start()
        logger.debug(
            f"O subscriber está rodando em segundo plano... [PID: {subscriber_process.pid}]"
        )
        uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        logger.debug(e)
