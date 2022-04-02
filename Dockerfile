FROM python:3.9

WORKDIR /app

RUN apt-get update

RUN pip install poetry
COPY pyproject.toml ./
RUN poetry install

COPY . .

EXPOSE 5000
