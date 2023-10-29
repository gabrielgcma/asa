from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# definindo a URL para conexão no banco
url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="banco",
    host="localhost",
    database="faculdade",
    port=5432,
)

# url = "postgresql+psycopg2://postgres:banco@localhost/postgres"

# nesse ponto são instanciados os objetos para conexão com o banco
engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    endereco = Column(String)
    numero = Column(String)
    complemento = Column(String)
    cidade = Column(String)
    estado = Column(String)


class Professor(Base):
    __tablename__ = "professores"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    endereco = Column(String)
    numero = Column(String)
    complemento = Column(String)
    cidade = Column(String)
    estado = Column(String)


class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    id_professor = Column(ForeignKey("professores.id"), nullable=False)


class CursoAluno(Base):
    __tablename__ = "curso_aluno"

    id_curso = Column(ForeignKey("cursos.id"), nullable=False)
    id_aluno = Column(ForeignKey("alunos.id"), nullable=False)


Base.metadata.create_all(engine)
