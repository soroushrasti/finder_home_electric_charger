FROM python

COPY . /app
WORKDIR /app
RUN pip install poetry 
RUN poetry install
RUN poetry run alembic upgrade head

CMD ["poetry", "run", "python", "-m", "src.main"]

EXPOSE 8080
