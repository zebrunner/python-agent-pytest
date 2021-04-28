FROM python:3.7-slim

RUN apt-get update && apt-get install -y curl python3-venv
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
