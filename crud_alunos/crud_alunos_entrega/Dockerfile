# Aluno: Gabriel Carneiro Marques Amado
# Matrícula: 12111ECP002
# ASA - CRUD estático de cadastro de alunos

FROM python:3.11
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code 
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
