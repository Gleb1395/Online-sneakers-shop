FROM python:3.12-slim-bullseye

RUN apt update


RUN mkdir /shop

WORKDIR /shop

COPY ./src ./src
COPY ./commands ./commands
COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip & pip install -r requirements.txt

CMD ["bash"]