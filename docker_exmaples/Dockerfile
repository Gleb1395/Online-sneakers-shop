FROM python:3.12.3-slim

RUN apt update
RUN python --version

RUN mkdir "/docker_example"

WORKDIR /docker_example

COPY ./meet_the_docker.py ./hello_world.py
COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip & pip install -r requirements.txt

CMD ["python", "hello_world.py"]