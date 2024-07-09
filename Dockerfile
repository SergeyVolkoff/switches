# FROM ubuntu:latest
FROM python:3.9

RUN apt-get update -y
RUN  pip install --upgrade pip
WORKDIR /app 
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg
COPY . .
RUN cd manage_app2
CMD ["python", "manage_app2/app.py", "runserver"]