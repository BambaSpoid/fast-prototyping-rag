FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-interaction --no-ansi

COPY src ./src

EXPOSE 8501

CMD ["streamlit", "run", "src/rag/ui/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
