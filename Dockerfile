FROM python:3.7-slim

RUN apt-get update && apt-get install -y curl python3-venv python3-pip
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"
