FROM python:3.7-slim

RUN apt-get update --quiet && apt-get upgrade -y --quiet
RUN apt-get install -y --quiet sqlite3 libsqlite3-dev
RUN pip install -U pip setuptools wheel
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

VOLUME .:/code
WORKDIR /code
