FROM python:3.9

WORKDIR /app

RUN pip install poetry
COPY poetry.lock ./
COPY pyproject.toml ./
RUN python3 -m pip install cryptography
RUN poetry install

COPY . .
