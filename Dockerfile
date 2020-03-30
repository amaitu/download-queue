FROM python:3.8.2-buster

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN touch database.sqlite

ENTRYPOINT ["python"]

CMD ["app.py"]
