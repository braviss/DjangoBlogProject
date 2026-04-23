FROM python:3.13

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock /app/

RUN uv sync --no-interaction --frozen --no-dev

COPY . /app

RUN chmod +x /app/ops/scripts/start-server.sh

CMD ["bash", "/app/ops/scripts/start-server.sh"]