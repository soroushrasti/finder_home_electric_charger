FROM python:3.12-slim

COPY . /app
WORKDIR /app
RUN pip install poetry 
RUN poetry install --no-dev

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 8080
