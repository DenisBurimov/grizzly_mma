FROM python:3.9

WORKDIR /app

RUN pip install poetry
COPY poetry.lock ./
COPY pyproject.toml ./
RUN poetry install --no-dev

COPY . .

EXPOSE 5000
