FROM python

COPY . /app
WORKDIR /app
RUN pip install poetry 
RUN poetry install 

CMD ["poetry", "run", "python", "-m", "src.main"]

EXPOSE 8080
