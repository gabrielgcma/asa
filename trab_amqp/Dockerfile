FROM python:3.11
WORKDIR /trab_amqp
COPY ./requirements.txt /trab_amqp/requirements.txt
COPY ./src/ /trab_amqp/src/
RUN pip install --no-cache-dir --upgrade -r /trab_amqp/requirements.txt
CMD python3 src/main.py 