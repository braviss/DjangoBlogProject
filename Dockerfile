FROM python:3.13

WORKDIR /app


RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-interaction --no-ansi

COPY . /app

RUN chmod +x /app/ops/scripts/start-server.sh


CMD ["bash", "/app/ops/scripts/start-server.sh"]