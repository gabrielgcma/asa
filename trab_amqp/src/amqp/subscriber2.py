import sys

sys.path.append("..")

import pika
import logging
import json
from sqlalchemy.orm import Session
from amqp.config import config
from database import session
import os

from models import Aluno

logger = logging.getLogger(__name__)
logging.getLogger("pika").propagate = False
FORMAT = (
    "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
)
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


def main():
    params = pika.ConnectionParameters(host=config["host"], port=config["port"])
    connection = pika.BlockingConnection(params)

    channel = connection.channel()

    channel.queue_declare(queue="alunos")

    def callback(ch, method, props, body):
        logger.debug(f"[x] Mensagem recebida: \n {body}")
        registrar_aluno_bd(body, session)

    channel.basic_consume(queue="alunos", on_message_callback=callback, auto_ack=True)

    logger.debug("\nEsperando por novos POSTs...")
    channel.start_consuming()


def registrar_aluno_bd(msg_aluno, db_session: Session):
    aluno_decoded = msg_aluno.decode("utf-8")
    aluno_json = json.loads(aluno_decoded)

    aluno_objeto = Aluno(**aluno_json)

    try:
        db_session.add(aluno_objeto)
        db_session.commit()
        return logger.debug(
            f"\nAluno {aluno_objeto.nome} criado com sucesso no banco de dados."
        )
    except Exception as e:
        logger.error(
            f"Erro ao criar o registro do aluno no banco de dados -- registrar_aluno_bd()"
        )
        print(e)
        db_session.rollback()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
