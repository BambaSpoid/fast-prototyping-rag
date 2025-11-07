FROM python:3.12-slim
WORKDIR /app
ENV POETRY_VIRTUALENVS_CREATE=false PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-interaction --no-ansi
COPY src ./src
EXPOSE 8501
CMD ["streamlit","run","src/rag/ui/app.py","--server.address=0.0.0.0","--server.port=8501"]