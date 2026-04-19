FROM python:3.11-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen

COPY src/ ./src/

RUN mkdir -p logs

ENTRYPOINT ["uv", "run", "python", "-m", "src.main"]
