FROM python:3.13-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml /app
COPY uv.lock /app
COPY README.md /app
COPY src/ /app/

RUN uv sync --no-dev --compile-bytecode

CMD ["uv", "run", "--no-dev", "fastapi", "run", "taskapi/main.py", "--port", "80"]