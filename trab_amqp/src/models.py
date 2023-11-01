from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base, engine


class Aluno(Base):
    __tablename__ = "aluno"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=True)
    email = Column(String)
    cpf = Column(String, nullable=True)
    endereco = Column(String, nullable=True)


class Professor(Base):
    __tablename__ = "professor"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=True)
    email = Column(String)
    cpf = Column(String, nullable=True)
    endereco = Column(String, nullable=True)


class Curso(Base):
    __tablename__ = "curso"
    id = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=True)


class CursoAluno(Base):
    __tablename__ = "cursoaluno"
    idAluno = Column(Integer, ForeignKey("aluno.id"), primary_key=True)
    idCurso = Column(Integer, ForeignKey("curso.id"), primary_key=True)
    curso = relationship(Curso)
    aluno = relationship(Aluno)


class CursoProfessor(Base):
    __tablename__ = "cursoprofessor"
    idProfessor = Column(Integer, ForeignKey("professor.id"), primary_key=True)
    idCurso = Column(Integer, ForeignKey("curso.id"), primary_key=True)
    curso = relationship(Curso)
    professor = relationship(Professor)


Base.metadata.create_all(engine)
