FROM python

COPY . /app
WORKDIR /app
RUN pip install poetry 
RUN poetry install
ENV DATABASE_URL=${DATABASE_URL}
ENV DATABASE_URL_SQLALCHEMY=${DATABASE_URL}

RUN poetry run alembic upgrade head

CMD ["poetry", "run", "python", "-m", "src.main"]

EXPOSE 8080
