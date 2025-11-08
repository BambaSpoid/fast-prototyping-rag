FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Installer poetry
RUN pip install --no-cache-dir poetry

# Copier fichiers de dépendances
COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-interaction --no-ansi

# Copier le code source
COPY src ./src

EXPOSE 8000

CMD ["uvicorn", "rag.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
