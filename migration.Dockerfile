# migration.Dockerfile
FROM python:3.12-slim

COPY . /app
WORKDIR /app
RUN pip install poetry
RUN poetry install --only=main

CMD ["poetry", "run", "python", "migrate.py"]