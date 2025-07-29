FROM python

COPY . /app
WORKDIR /app
RUN pip install poetry 
RUN poetry install

CMD ["sh", "-c", "poetry run python migrate.py && poetry run python main.py"]
EXPOSE 8080
