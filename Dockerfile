FROM python:3.12-slim

WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml poetry.lock ./

# Install poetry and dependencies
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only=main

# Copy application code
COPY . .

# Expose port (Railway will set PORT env var)
EXPOSE $PORT

# Use Railway's PORT environment variable
CMD ["sh", "-c", "poetry run python src/main.py --port ${PORT:-8080}"]