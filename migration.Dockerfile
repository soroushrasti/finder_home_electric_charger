# migration.Dockerfile
FROM python:3.12-slim

COPY . /app
WORKDIR /app
RUN pip install poetry
RUN poetry install

CMD ["poetry", "run", "python", "migrate.py"]