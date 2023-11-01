import pika
import logging
import json
from models import Aluno
from sqlalchemy.orm import Session
from .config import config

logger = logging.getLogger(__name__)
logging.getLogger("pika").propagate = False
FORMAT = (
    "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
)
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


class Subscriber(object):
    def receive_msgs(self, db_session: Session):
        try:
            self.connection = self.create_connection()
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue="alunos")

            def callback(ch, method, properties, body):
                logger.debug(f"[x] Mensagem recebida: \n {body}")
                registrar_aluno_bd(body, db_session)

            self.channel.basic_consume(
                queue="alunos", on_message_callback=callback, auto_ack=True
            )
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print()
            logger.debug("O subscriber está sendo terminado...")
            self.stop_consuming()
            logger.debug("O subscriber foi terminado com sucesso...")

    def create_connection(self):
        params = pika.ConnectionParameters(host=config["host"], port=config["port"])
        return pika.BlockingConnection(params)

    def stop_consuming(self):
        self.channel.stop_consuming()
        self.connection.close()
        logger.debug("A conexão do subscriber foi interrompida com sucesso...")


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
