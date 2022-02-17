FROM python:3.8.3-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 \
    && mkdir /src
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt